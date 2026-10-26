"""Part 2 maintenance loop: the DAG as label space, empirical metrics from tags, discovery.

    python -m taxonomy.classification.maintain [--iter K] [--min-items 5] [--min-residual 0.3] [--no-discover]

Reads iteration K's tags (output/evolution/iter_K/tags.jsonl; default: latest iteration) and
the catalogue version that iteration was tagged with
and treats the DAG as the label space: every item sits on the term-type nodes it was tagged
with, and on their is-a ancestors (closure). From the item sets it computes, per node,

  n_direct / n_closure   items tagged at the node / at the node or any descendant
  value entropy          bits over the node's values among its direct tags (impurity of the
                         node's own split: ~0 means one value absorbs everything)
  branching gain         bits of the empirical split of the node's closure items over its
                         child term types plus a "stop" mass (items that go no deeper)
  residual               closure items on no child term type: the stop mass. A large
                         residual with many items is where a child dimension may be missing.

and, for the whole DAG, the same three maintenance objectives as Part 1 but driven by the
content instead of the model's prior weights: bits per random descent (information gain),
AUC of the reach-a-leaf curve, and effective leaves / nodes. A descent starts at a root with
probability proportional to its closure size and at each node either stops (residual
share) or moves to a child in proportion to the child's closure share.

Maintenance proposals (deterministic): dormant nodes (no items), collapsed nodes (many
items, one value), high-gain nodes, and discovery targets (residual >= --min-residual and
>= --min-items items). Discovery (Task E) sends each target's residual items to the model,
which proposes missing values or child term types with supporting item ids. The shown items
are a sample of the residual (at most --max-items), so the candidate's support share among
them is extrapolated to the whole residual; a candidate is scored by the branching-gain
increase that estimated support would bring at the node and accepted when it clears
--min-gain bits with >= --min-items supporting items among those shown.

Outputs (output/evolution/iter_K/): maintenance.json, maintenance.md. Accepted candidates
are consolidated into the next catalogue version by evolve.py; no version is modified here.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

from taxonomy.classification import catalogue as cat
from taxonomy.classification.prompts import DISCOVER_INSTRUCTIONS, DISCOVER_PROMPT
from taxonomy.classification.tag import CATEGORIES, PRICE, extract_json, latency_stats, load_taxonomy
from taxonomy.establishment.term_types import quote_found
from taxonomy.llm_context import ROOT, build_request, client


def H(ps) -> float:
    return -sum(p * math.log2(p) for p in ps if p > 0)


# ---------------------------------------------------------------- label space
def label_space(tts: list[dict], dag: dict, rows: list[dict]) -> dict:
    ids = [t["id"] for t in tts]
    children: dict[str, list[str]] = defaultdict(list)
    weight: dict[tuple[str, str], float] = {}
    for e in dag["edges"]:
        children[e["parent"]].append(e["child"])
        weight[(e["child"], e["parent"])] = e["probability"]
    direct: dict[str, set[str]] = {i: set() for i in ids}
    values: dict[str, dict[str, set[str]]] = {i: defaultdict(set) for i in ids}
    for r in rows:
        for t in r["tags"]:
            direct[t["term_type"]].add(r["item_id"])
            values[t["term_type"]][t["value"]].add(r["item_id"])
    closure: dict[str, set[str]] = {}

    def clos(n: str) -> set[str]:
        if n not in closure:
            s = set(direct[n])
            for c in children.get(n, []):
                s |= clos(c)
            closure[n] = s
        return closure[n]

    for i in ids:
        clos(i)
    return {"ids": ids, "children": children, "weight": weight, "direct": direct, "values": values, "closure": closure,
            "roots": [i for i in ids if not any(c == i for cs in children.values() for c in cs)]}


def node_stats(space: dict, by_id: dict[str, dict]) -> dict[str, dict]:
    out = {}
    for y in space["ids"]:
        I, D = space["closure"][y], space["direct"][y]
        kids = space["children"].get(y, [])
        covered = set().union(*(space["closure"][c] for c in kids)) if kids else set()
        residual = I - covered
        shares = {c: len(space["closure"][c]) / len(I) for c in kids if I}
        stop = len(residual) / len(I) if I else 0.0
        Z = sum(shares.values()) + stop
        q = {c: s / Z for c, s in shares.items() if Z} | ({"stop": stop / Z} if Z else {})
        vals = {v: len(s) for v, s in space["values"][y].items()}
        nv = sum(vals.values())
        out[y] = {"name": by_id[y]["name"], "category": by_id[y]["applies_to"],
                  "n_direct": len(D), "n_closure": len(I), "n_children": len(kids),
                  "value_counts": dict(sorted(vals.items(), key=lambda kv: -kv[1])),
                  "value_entropy_bits": round(H([c / nv for c in vals.values()]), 4) if nv else None,
                  "value_dominance": round(max(vals.values()) / nv, 3) if nv else None,
                  "branching_gain_bits": round(H(list(q.values())), 4) if I else 0.0,
                  "residual_items": sorted(residual), "residual_frac": round(stop, 3)}
    return out


def descent_metrics(space: dict, stats: dict[str, dict]) -> dict:
    """Empirical random descent over the label space (see module docstring)."""
    roots = [r for r in space["roots"] if space["closure"][r]]
    tot = sum(len(space["closure"][r]) for r in roots)
    if not tot:
        return {}
    mass = {r: len(space["closure"][r]) / tot for r in roots}
    stop_at: dict[str, float] = defaultdict(float)
    stopped_by_depth: list[float] = []
    bits = depth_sum = 0.0
    d = 0
    while mass:
        nxt: dict[str, float] = defaultdict(float)
        stopped = 0.0
        for y, m in mass.items():
            I = space["closure"][y]
            kids = [c for c in space["children"].get(y, []) if space["closure"][c]]
            shares = {c: len(space["closure"][c]) / len(I) for c in kids}
            stop = stats[y]["residual_frac"] if kids else 1.0
            Z = sum(shares.values()) + stop
            qs = {c: s / Z for c, s in shares.items()}
            qstop = stop / Z
            bits += m * H(list(qs.values()) + [qstop])
            stop_at[y] += m * qstop
            stopped += m * qstop
            depth_sum += m * qstop * d
            for c, qc in qs.items():
                nxt[c] += m * qc
        stopped_by_depth.append(stopped)
        mass = {k: v for k, v in nxt.items() if v > 1e-12}
        d += 1
        if d > len(space["ids"]):
            break
    D = len(stopped_by_depth) - 1
    F, acc = [], 0.0
    for s in stopped_by_depth:
        acc += s
        F.append(acc)
    auc = 1.0 if D == 0 else sum((F[i] + F[i + 1]) / 2 for i in range(D)) / D
    r = sorted(stop_at.values(), reverse=True)
    eff = 2 ** H(r)
    n_used = sum(1 for i in space["ids"] if space["closure"][i])
    return {"bits_per_descent": round(bits, 4), "auc": round(auc, 4), "expected_depth": round(depth_sum, 4),
            "max_depth": D, "effective_leaves": round(eff, 3), "nodes": len(space["ids"]), "nodes_with_items": n_used,
            "effective_leaves_over_nodes": round(eff / len(space["ids"]), 4),
            "effective_leaves_over_nodes_with_items": round(eff / n_used, 4) if n_used else None,
            "stop_mass_top": {k: round(v, 4) for k, v in sorted(stop_at.items(), key=lambda kv: -kv[1])[:15]}}


# ---------------------------------------------------------------- discovery (Task E)
def candidate_gain(stats_y: dict, space: dict, y: str, supporting: set[str], shown: int) -> tuple[float, int]:
    """Branching-gain change at y if a new child captured the candidate's items.

    Discovery shows at most `shown` residual items, so the support count is a sample: the
    share of shown items that support the candidate is extrapolated to the whole residual
    (estimated support), and the gain is computed with that estimate. Returns (gain, est)."""
    I = space["closure"][y]
    residual = set(stats_y["residual_items"])
    if not I or not residual:
        return 0.0, 0
    n_shown = max(1, min(shown, len(residual)))
    est = len(supporting & residual) if n_shown >= len(residual) else round(len(supporting & residual) / n_shown * len(residual))
    est = min(est, len(residual))
    kids = space["children"].get(y, [])
    shares = [len(space["closure"][c]) / len(I) for c in kids]
    before = shares + [len(residual) / len(I)]
    after = shares + [est / len(I), (len(residual) - est) / len(I)]
    Zb, Za = sum(before), sum(after)
    return H([p / Za for p in after]) - H([p / Zb for p in before]), est


def discover(cl, y: str, stats_y: dict, by_id: dict, space: dict, items: dict[str, dict], rows_by_id: dict,
             seeds: list[str], model: str, max_items: int) -> dict:
    t = by_id[y]
    resid = stats_y["residual_items"]
    # show the residual items with the most confident tags at y first
    def conf(iid: str) -> float:
        return max((g["confidence"] for g in rows_by_id[iid]["tags"] if g["term_type"] == y), default=0)
    shown = sorted(resid, key=lambda i: -conf(i))[:max_items]
    lines = []
    for iid in shown:
        it = items[iid]
        ev = "; ".join(g["evidence"] for g in rows_by_id[iid]["tags"] if g["term_type"] == y)[:200]
        lines.append(f'- id={iid} | {it["title"][:100]} | tagged: {ev} | text: {" ".join(it["text"].split()[:60])}')
    prompt = DISCOVER_PROMPT.format(
        node_id=y, name=t["name"], question=t["question"], category=t["applies_to"],
        values="; ".join(v["value"] for v in t["values"]),
        children="; ".join(f'{c} ({by_id[c]["name"]})' for c in space["children"].get(y, [])) or "none",
        seeds="; ".join(seeds) or "none", n=len(shown), total=len(resid), items="\n".join(lines))
    req = build_request(DISCOVER_INSTRUCTIONS, prompt, model=model, max_tokens=3000, effort="medium",
                        corpus=False, thinking={"type": "disabled"})
    t0 = time.perf_counter()
    msg = cl.messages.create(**req)
    u = msg.usage
    text = "".join(b.text for b in msg.content if b.type == "text")
    try:
        parsed = extract_json(text)
    except (json.JSONDecodeError, ValueError):
        parsed = {"candidates": []}
    return {"node": y, "shown": shown, "raw": parsed, "seconds": round(time.perf_counter() - t0, 3),
            "usage": {"input": u.input_tokens, "output": u.output_tokens,
            "cache_write": u.cache_creation_input_tokens or 0, "cache_read": u.cache_read_input_tokens or 0}}


# ---------------------------------------------------------------- report
def render_md(m: dict, stats: dict, by_id: dict) -> str:
    e, p = m["empirical"], m["prior_reference"]
    lines = ["# Part 2 maintenance: the DAG as label space", "",
             f"{m['items']} tagged items placed on {e['nodes_with_items']}/{e['nodes']} nodes "
             f"({m['tags']} tags, {m['closure_placements']} closure placements).", "",
             "## Objectives: content-driven vs Part 1 prior", "",
             "| metric | from tags (empirical) | from is-a weights (Part 1) |", "|---|---|---|",
             f"| bits per descent (information gain) | {e['bits_per_descent']} | {p['bits_per_descent']} |",
             f"| AUC of reach-a-leaf | {e['auc']} | {p['auc']} |",
             f"| expected depth | {e['expected_depth']} | {p['expected_depth']} |",
             f"| effective leaves | {e['effective_leaves']} | {p['effective_leaves']} |",
             f"| effective leaves / nodes | {e['effective_leaves_over_nodes']} | {p['effective_leaves_over_nodes']} |", "",
             "## Where descents stop (top stop mass)", ""]
    lines += [f"- {by_id[k]['name']} `{k}`: {v}" for k, v in e["stop_mass_top"].items()]
    lines += ["", "## Node statistics (nodes with items, by closure size)", "",
              "| node | cat | direct | closure | children | value entropy | dominance | branching gain | residual |",
              "|---|---|---|---|---|---|---|---|---|"]
    for y, s in sorted(stats.items(), key=lambda kv: -kv[1]["n_closure"]):
        if s["n_closure"]:
            lines.append(f"| {s['name'][:38]} | {s['category'][:5]} | {s['n_direct']} | {s['n_closure']} | {s['n_children']} | "
                         f"{s['value_entropy_bits'] if s['value_entropy_bits'] is not None else '-'} | {s['value_dominance'] if s['value_dominance'] is not None else '-'} | "
                         f"{s['branching_gain_bits']} | {len(s['residual_items'])} ({s['residual_frac']}) |")
    pr = m["proposals"]
    lines += ["", "## Maintenance proposals", "",
              f"**Dormant nodes ({len(pr['dormant'])})**, no items in this batch: " + ", ".join(f"`{x}`" for x in pr["dormant"]), "",
              f"**Collapsed nodes ({len(pr['collapsed'])})**, many items but one value absorbs them (merge or re-split candidates):"]
    lines += [f"- {by_id[x['node']]['name']} `{x['node']}`: {x['n_direct']} items, dominance {x['dominance']} ({x['top_value']})" for x in pr["collapsed"]]
    lines += ["", f"**Highest-gain nodes**:"] + [f"- {by_id[x['node']]['name']} `{x['node']}`: {x['bits']} bits over {x['n_closure']} items" for x in pr["high_gain"]]
    lines += ["", f"**Discovery targets ({len(pr['discovery_targets'])})**, residual >= threshold:"]
    lines += [f"- {by_id[x['node']]['name']} `{x['node']}`: {x['residual']} residual of {x['n_closure']} ({x['frac']})" for x in pr["discovery_targets"]]
    lines += ["", "## Discovery (Task E) candidates", ""]
    for c in m["discovery"]["candidates"]:
        st = "ACCEPTED" if c["accepted"] else "rejected"
        lines.append(f"- [{st}] at `{c['node']}`: new {c['kind']} **{c['label']}** — {c['definition']} "
                     f"(supports {c['n_support']} of {c.get('n_shown')} shown, est. {c.get('estimated_support')} of {c.get('n_residual')} residual, "
                     f"gain {c['gain_bits']} bits, evidence {'verified' if c['evidence_found'] else 'unverified'})"
                     + (f"; values: {', '.join(c['values'])}" if c.get("values") else ""))
    if not m["discovery"]["candidates"]:
        lines.append("(no discovery run or no candidates)")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--min-items", type=int, default=5, help="min residual/supporting items")
    ap.add_argument("--min-residual", type=float, default=0.3, help="residual share that marks a discovery target")
    ap.add_argument("--min-gain", type=float, default=0.1, help="bits a candidate must add at its node")
    ap.add_argument("--max-items", type=int, default=40, help="residual items shown per discovery call")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--no-discover", action="store_true", help="metrics and deterministic proposals only")
    ap.add_argument("--iter", type=int, default=None, help="iteration to maintain (default: latest)")
    args = ap.parse_args()
    k = args.iter if args.iter is not None else (cat.iterations()[-1] if cat.iterations() else 1)
    out_dir = cat.iter_dir(k)
    TAGS_OUT, NOVEL_OUT = out_dir / "tags.jsonl", out_dir / "novel_proposals.json"
    MAINT_OUT, MD_OUT = out_dir / "maintenance.json", out_dir / "maintenance.md"
    if not TAGS_OUT.exists():
        sys.exit(f"{TAGS_OUT} missing: run python -m taxonomy.classification.tag --iter {k} first")
    run_meta = json.loads((out_dir / "tags_summary.json").read_text(encoding="utf-8"))["run"]
    version = run_meta["catalogue_version"]
    rows = [json.loads(l) for l in TAGS_OUT.read_text(encoding="utf-8").split("\n") if l.strip()]
    rows_by_id = {r["item_id"]: r for r in rows}
    sample_file = ROOT / run_meta["sample"]
    items = {it["id"]: it for it in (json.loads(l) for l in sample_file.read_text(encoding="utf-8").split("\n") if l.strip())}
    tts, dag = load_taxonomy(version)
    print(f"iteration {k}: maintaining catalogue v{version} on {len(rows)} tagged items", file=sys.stderr)
    by_id = {t["id"]: t for t in tts}
    space = label_space(tts, dag, rows)
    stats = node_stats(space, by_id)
    emp = descent_metrics(space, stats)
    prior = dag["metrics"]["overall"]
    prior_ref = {"bits_per_descent": prior["information_gain"]["bits_per_descent"], "auc": prior["auc"]["value"],
                 "expected_depth": prior["auc"]["expected_depth"], "effective_leaves": prior["leaves_needed"]["effective_leaves"],
                 "effective_leaves_over_nodes": round(prior["leaves_needed"]["effective_leaves"] / prior["nodes"], 4)}

    # deterministic proposals
    dormant = [y for y in space["ids"] if not space["closure"][y]]
    collapsed = [{"node": y, "n_direct": s["n_direct"], "dominance": s["value_dominance"], "top_value": next(iter(s["value_counts"]))}
                 for y, s in stats.items() if s["n_direct"] >= 2 * args.min_items and s["value_dominance"] is not None and s["value_dominance"] >= 0.85]
    high_gain = [{"node": y, "bits": s["branching_gain_bits"], "n_closure": s["n_closure"]}
                 for y, s in sorted(stats.items(), key=lambda kv: -kv[1]["branching_gain_bits"])[:8] if s["branching_gain_bits"] > 0]
    targets = [{"node": y, "residual": len(s["residual_items"]), "n_closure": s["n_closure"], "frac": s["residual_frac"]}
               for y, s in stats.items() if len(s["residual_items"]) >= args.min_items and s["residual_frac"] >= args.min_residual]
    targets.sort(key=lambda x: -x["residual"])

    # discovery
    disc = {"calls": 0, "usage": {key: 0 for key in PRICE}, "cost_usd": 0.0, "candidates": [], "latencies": []}
    if not args.no_discover and targets:
        novel = json.loads(NOVEL_OUT.read_text(encoding="utf-8")) if NOVEL_OUT.exists() else {}
        cl = client()
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {}
            for tg in targets:
                y = tg["node"]
                seeds = [f'{n["kind"]}: {n["proposal"]}' for n in novel.get(y, [])]
                if y in space["roots"]:
                    seeds += [f'term_type: {n["proposal"]}' for n in novel.get("NEW_TERM_TYPE", [])]
                futs[ex.submit(discover, cl, y, stats[y], by_id, space, items, rows_by_id, seeds[:6], args.model, args.max_items)] = y
            for f in as_completed(futs):
                res = f.result()
                disc["calls"] += 1
                disc["latencies"].append(res["seconds"])
                for key in disc["usage"]:
                    disc["usage"][key] += res["usage"][key]
                y = res["node"]
                resid = set(stats[y]["residual_items"])
                for c in res["raw"].get("candidates", []) or []:
                    support = {str(i) for i in (c.get("item_ids") or [])} & resid
                    gain, est = candidate_gain(stats[y], space, y, support, len(res["shown"]))
                    gain = round(gain, 4)
                    ev = str(c.get("evidence", "") or "")
                    ev_ok = any(quote_found(ev, items[i]["title"] + " " + items[i]["text"]) for i in support) if ev and support else False
                    disc["candidates"].append({
                        "node": y, "kind": c.get("kind"), "label": c.get("label"), "question": c.get("question", ""),
                        "definition": c.get("definition", ""), "values": c.get("values") or [],
                        "item_ids": sorted(support), "n_support": len(support), "n_shown": len(res["shown"]),
                        "n_residual": len(resid), "estimated_support": est, "gain_bits": gain,
                        "evidence": ev, "evidence_found": ev_ok,
                        "accepted": len(support) >= args.min_items and gain >= args.min_gain and ev_ok})
        disc["cost_usd"] = round(sum(disc["usage"][key] * PRICE[key] for key in PRICE), 4)
        disc["seconds"] = round(time.time() - t0, 1)
        disc["time"] = latency_stats(disc.pop("latencies"), time.time() - t0, args.workers)
        disc["candidates"].sort(key=lambda c: (-c["accepted"], -c["gain_bits"]))

    disc.pop("latencies", None)
    out = {"run": {"timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"), "model": args.model,
                   "iteration": k, "catalogue_version": version,
                   "min_items": args.min_items, "min_residual": args.min_residual, "min_gain": args.min_gain},
           "items": len(rows), "tags": sum(len(r["tags"]) for r in rows),
           "closure_placements": sum(len(s) for s in space["closure"].values()),
           "empirical": emp, "prior_reference": prior_ref, "nodes": stats,
           "proposals": {"dormant": dormant, "collapsed": collapsed, "high_gain": high_gain, "discovery_targets": targets},
           "discovery": disc}
    MAINT_OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    MD_OUT.write_text(render_md(out, stats, by_id), encoding="utf-8")

    print(f"items {len(rows)}; nodes with items {emp['nodes_with_items']}/{emp['nodes']}")
    print(f"empirical: {emp['bits_per_descent']} bits/descent, AUC {emp['auc']}, E[depth] {emp['expected_depth']}, "
          f"effective leaves {emp['effective_leaves']} (/nodes {emp['effective_leaves_over_nodes']})")
    print(f"prior:     {prior_ref['bits_per_descent']} bits/descent, AUC {prior_ref['auc']}, E[depth] {prior_ref['expected_depth']}, "
          f"effective leaves {prior_ref['effective_leaves']} (/nodes {prior_ref['effective_leaves_over_nodes']})")
    print(f"dormant {len(dormant)}, collapsed {len(collapsed)}, discovery targets {len(targets)}, "
          f"discovery calls {disc['calls']} (${disc['cost_usd']}), candidates {len(disc['candidates'])}, "
          f"accepted {sum(c['accepted'] for c in disc['candidates'])}")
    print(f"-> {MAINT_OUT}\n-> {MD_OUT}")


if __name__ == "__main__":
    main()
