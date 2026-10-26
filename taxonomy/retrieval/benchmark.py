"""Benchmark the DAG index: query latency against flat scans, and navigation by facet gain.

    python -m taxonomy.retrieval.benchmark [--seed 7] [--repeat 5] [--targets 300] [--k 10]

Latency: every single-node closure query, every direct-node and (node, value) query, a
strength-restricted closure per node, and random 2- and 3-atom AND / OR / NOT queries are
evaluated by (a) the bitset engine, (b) a flat scan of the item tag table that tests each item
against the query using precomputed ancestor sets, and (c) a flat scan without a precomputed
closure (descendants enumerated per query). Results are checked to be identical.

Navigation: for random target items, a simulated user starts from the whole collection and
at each step is offered the facets (child subtrees or value splits) of every node the remaining
items carry tags on; the engine orders them by expected narrowing (bits), the user picks the
option containing the target. Steps and bits
resolved until the result set has at most k items are compared with picking facets at random.
Writes output/retrieval/benchmark.{json,md}.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import statistics
import time

from taxonomy.retrieval.graph import iter_bits, popcount
from taxonomy.retrieval.index import OUT, load
from taxonomy.retrieval.query import Atom, Engine, parse, tokenize

BENCH = OUT / "benchmark.json"
BENCH_MD = OUT / "benchmark.md"


# ---- flat baselines ----------------------------------------------------------------------
class FlatScan:
    """No inverted index: test every item against the query. Ancestor sets precomputed from the DAG."""

    def __init__(self, eng: Engine):
        self.eng, self.idx, self.g = eng, eng.idx, eng.g
        self.anc = {y: {self.g.ids[k] for k in iter_bits(self.g.anc_bits[y])} for y in self.g.ids}

    def atom(self, a: Atom, nodes: dict, vals: dict) -> bool:
        if a.category:
            return any(self.g.category[n] == a.category for n in nodes)
        if a.value is not None:
            return (a.node, self.eng.resolve_value(a.node, a.value)) in vals
        if a.direct:
            return a.node in nodes
        if a.min_strength is not None:
            return any(a.node in self.anc[d] and self.g.path_strength(d, a.node) >= a.min_strength for d in nodes)
        return any(a.node in self.anc[d] for d in nodes)

    def test(self, tree, nodes, vals) -> bool:
        if isinstance(tree, Atom):
            return self.atom(tree, nodes, vals)
        if tree[0] == "NOT":
            return not self.test(tree[1], nodes, vals)
        if tree[0] == "AND":
            return self.test(tree[1], nodes, vals) and self.test(tree[2], nodes, vals)
        return self.test(tree[1], nodes, vals) or self.test(tree[2], nodes, vals)

    def run(self, tree) -> int:
        b = 0
        for i in range(self.idx.n):
            if self.test(tree, self.idx.item_nodes[i], self.idx.item_values[i]):
                b |= 1 << i
        return b


class FlatNoClosure(FlatScan):
    """Flat scan where the subtree of a query node is enumerated per query (no precomputed closure)."""

    def descendants(self, y: str) -> set[str]:
        seen, stack = set(), [y]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            stack.extend(c for c, _ in self.g.children[x])
        return seen

    def run(self, tree) -> int:
        cache: dict[str, set[str]] = {}

        def atom(a: Atom, nodes, vals):
            if a.category or a.value is not None or a.direct:
                return self.atom(a, nodes, vals)
            if a.node not in cache:
                cache[a.node] = self.descendants(a.node)
            if a.min_strength is not None:
                return any(d in cache[a.node] and self.g.path_strength(d, a.node) >= a.min_strength for d in nodes)
            return any(d in cache[a.node] for d in nodes)

        def test(tree, nodes, vals):
            if isinstance(tree, Atom):
                return atom(tree, nodes, vals)
            if tree[0] == "NOT":
                return not test(tree[1], nodes, vals)
            if tree[0] == "AND":
                return test(tree[1], nodes, vals) and test(tree[2], nodes, vals)
            return test(tree[1], nodes, vals) or test(tree[2], nodes, vals)

        b = 0
        for i in range(self.idx.n):
            if test(tree, self.idx.item_nodes[i], self.idx.item_values[i]):
                b |= 1 << i
        return b


# ---- workloads ---------------------------------------------------------------------------
def workloads(eng: Engine, rng: random.Random) -> dict[str, list[str]]:
    idx, g = eng.idx, eng.g
    used = [y for y in g.ids if idx.direct.get(y, 0)]
    pairs = [f'{y}="{v}"' for (y, v) in idx.pair]
    w = {"closure (1 node)": list(g.ids),
         "direct (node!)": [f"{y}!" for y in used],
         "value (node=value)": pairs,
         "closure, strength >= 0.3": [f"{y}~0.3" for y in g.ids]}
    atoms = list(g.ids) + pairs

    def pick():
        return rng.choice(atoms)

    w["AND (2 atoms)"] = [f"{pick()} AND {pick()}" for _ in range(300)]
    w["OR (2 atoms)"] = [f"{pick()} OR {pick()}" for _ in range(300)]
    w["AND NOT"] = [f"{pick()} AND NOT {pick()}" for _ in range(300)]
    w["3 atoms, mixed"] = [f"({pick()} OR {pick()}) AND {pick()}" for _ in range(200)]
    return w


def time_fn(fn, repeat: int) -> float:
    best = math.inf
    for _ in range(repeat):
        t0 = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - t0)
    return best


def latency(eng: Engine, rng: random.Random, repeat: int) -> dict:
    flat, noclo = FlatScan(eng), FlatNoClosure(eng)
    out = {}
    for name, qs in workloads(eng, rng).items():
        t_bits, t_flat, t_noclo, sizes, mism = [], [], [], [], 0
        for q in qs:
            tree = parse(tokenize(q))
            r = eng.evaluate(tree)
            if r != flat.run(tree) or r != noclo.run(tree):
                mism += 1
            sizes.append(popcount(r))
            t_bits.append(time_fn(lambda: eng.evaluate(parse(tokenize(q))), repeat))
            t_flat.append(time_fn(lambda: flat.run(tree), 1))
            t_noclo.append(time_fn(lambda: noclo.run(tree), 1))
        q_us = lambda xs, p: statistics.quantiles(xs, n=100)[p - 1] * 1e6 if len(xs) > 1 else xs[0] * 1e6
        out[name] = {"queries": len(qs), "mismatches": mism, "mean_result_size": round(statistics.mean(sizes), 1),
                     "bitset_us_mean": round(statistics.mean(t_bits) * 1e6, 1), "bitset_us_p95": round(q_us(t_bits, 95), 1),
                     "flat_scan_us_mean": round(statistics.mean(t_flat) * 1e6, 1),
                     "flat_no_closure_us_mean": round(statistics.mean(t_noclo) * 1e6, 1),
                     "speedup_vs_flat": round(statistics.mean(t_flat) / statistics.mean(t_bits), 1),
                     "speedup_vs_no_closure": round(statistics.mean(t_noclo) / statistics.mean(t_bits), 1)}
    return out


# ---- navigation --------------------------------------------------------------------------
def navigate(eng: Engine, target: int, policy: str, rng: random.Random, k: int, max_steps: int = 15) -> dict:
    idx, g = eng.idx, eng.g
    result = idx.all
    used: set[tuple[str, str]] = set()
    steps, trace = 0, []
    while popcount(result) > k and steps < max_steps:
        # the best next question anywhere: facets of every node the remaining items still carry tags on
        focus = [y for y in g.ids if idx.direct.get(y, 0) & result or any(idx.closure[c] & result for c, _ in g.children[y])]
        facets = [f for f in eng.facets(result, focus, top=500) if (f["node"], f["kind"]) not in used and f["gain_bits"] > 0]
        if not facets:
            break
        f = facets[0] if policy == "gain" else rng.choice(facets)
        used.add((f["node"], f["kind"]))
        steps += 1
        before = popcount(result)
        if f["kind"] == "values":
            hit = [o for o in f["options"] if (f["node"], o["value"]) in idx.item_values[target]]
            if hit:
                result &= idx.pair[(f["node"], hit[0]["value"])]
                trace.append(f'{f["node"]}={hit[0]["value"]}')
            else:
                result &= ~idx.direct.get(f["node"], 0)
                trace.append(f'{f["node"]}: not tagged')
        else:
            hit = [o for o in f["options"] if idx.closure[o["node"]] >> target & 1]
            if hit:
                c = max(hit, key=lambda o: g.ic[o["node"]])["node"]   # the most specific child containing the target
                result &= idx.closure[c]
                trace.append(f"-> {c}")
            else:
                covered = 0
                for o in f["options"]:
                    covered |= idx.closure[o["node"]]
                result &= ~covered
                trace.append(f'{f["node"]}: residual')
    n_final = popcount(result)
    return {"steps": steps, "final_size": n_final, "bits": round(math.log2(idx.n / max(n_final, 1)), 3),
            "reached_k": n_final <= k, "trace": trace}


def navigation(eng: Engine, rng: random.Random, n_targets: int, k: int) -> dict:
    targets = rng.sample(range(eng.idx.n), n_targets)
    out = {"targets": n_targets, "k": k, "ideal_bits": round(math.log2(eng.idx.n / k), 3)}
    for policy in ("gain", "random"):
        t0 = time.perf_counter()
        runs = [navigate(eng, t, policy, rng, k) for t in targets]
        out[policy] = {"mean_steps": round(statistics.mean(r["steps"] for r in runs), 2),
                       "mean_bits": round(statistics.mean(r["bits"] for r in runs), 2),
                       "bits_per_step": round(statistics.mean(r["bits"] for r in runs) / max(statistics.mean(r["steps"] for r in runs), 1e-9), 2),
                       "reached_k": round(statistics.mean(r["reached_k"] for r in runs), 3),
                       "mean_final_size": round(statistics.mean(r["final_size"] for r in runs), 1),
                       "ms_per_target": round((time.perf_counter() - t0) * 1e3 / n_targets, 2),
                       "example_trace": runs[0]["trace"]}
    return out


def render_md(b: dict) -> str:
    s = b["index"]
    lines = ["# Retrieval benchmark", "",
             f"Index: catalogue v{s['catalogue_version']}, {s['items']} items, {s['tags']} tags, {s['nodes']} nodes. "
             f"Latencies are per query on one core (best of {b['repeat']} for the bitset engine, single run for the scans).", "",
             "## Query latency", "",
             "| workload | queries | mean result | bitset mean (us) | p95 (us) | flat scan (us) | flat, no closure (us) | speedup vs flat | vs no closure | mismatches |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for name, r in b["latency"].items():
        lines.append(f"| {name} | {r['queries']} | {r['mean_result_size']} | {r['bitset_us_mean']} | {r['bitset_us_p95']} | "
                     f"{r['flat_scan_us_mean']} | {r['flat_no_closure_us_mean']} | {r['speedup_vs_flat']}x | {r['speedup_vs_no_closure']}x | {r['mismatches']} |")
    n = b["navigation"]
    lines += ["", "## Navigation by facet gain", "",
              f"{n['targets']} random target items; the collection is narrowed by picking the facet option that contains the target "
              f"until at most k = {n['k']} items remain (ideal: {n['ideal_bits']} bits).", "",
              "| policy | mean steps | bits resolved | bits / step | reached k | mean final size | ms / target |", "|---|---|---|---|---|---|---|"]
    for p in ("gain", "random"):
        r = n[p]
        lines.append(f"| {p} | {r['mean_steps']} | {r['mean_bits']} | {r['bits_per_step']} | {r['reached_k']} | {r['mean_final_size']} | {r['ms_per_target']} |")
    lines += ["", f"Example trace (gain policy): {' ; '.join(n['gain']['example_trace'])}", ""]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--repeat", type=int, default=5)
    ap.add_argument("--targets", type=int, default=300)
    ap.add_argument("--k", type=int, default=10)
    args = ap.parse_args()
    idx = load()
    eng = Engine(idx)
    rng = random.Random(args.seed)
    t0 = time.perf_counter()
    lat = latency(eng, rng, args.repeat)
    nav = navigation(eng, rng, args.targets, args.k)
    b = {"index": {k: idx.stats[k] for k in ("catalogue_version", "items", "tags", "nodes")}, "seed": args.seed, "repeat": args.repeat,
         "latency": lat, "navigation": nav, "seconds": round(time.perf_counter() - t0, 1)}
    BENCH.write_text(json.dumps(b, indent=1), encoding="utf-8")
    BENCH_MD.write_text(render_md(b), encoding="utf-8")
    print(render_md(b))
    print(f"-> {BENCH}\n-> {BENCH_MD}")


if __name__ == "__main__":
    main()
