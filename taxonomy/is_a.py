"""Task B runner: is-a hierarchy over the Task A term types.

    python -m taxonomy.is_a [--workers 4] [--k 6] [--only asset,actor] [--limit N] [--render-only]

For every term type X in output/term_types.json, asks the model (same cached corpus, plus the
Task A catalogue as a second cached system block) for a probability distribution over
"X is-a Y" with Y ranging over the other term types in X's category, plus "none".
Writes output/is_a.json (all distributions, verified citations), output/is_a_edges.csv
(child, parent, probability) and output/is_a.md: per category, the consolidated DAG.

Consolidation into a DAG. The model's "none" entry is removed and each child's weights are
renormalised over its candidate parents so they sum to exactly 1 (the original P(none) is
kept as `p_none` for reference). No probability threshold is applied: every weighted edge
is kept, in decreasing weight, unless it would close a cycle (a mutual pair resolves to the
stronger direction; an exact tie resolves by id order and is listed under "ties"). The
first kept edge is the primary parent, later ones are extra parents. --render-only redoes
this step from the saved is_a.json without calling the API.

Metrics (taxonomy/dag_metrics.py): information gain per node and per descent, AUC of the
reach-a-leaf curve, expected depth, leaves and effective leaves; computed overall, per
category, and (output/dag_metrics.json) for the sub-DAGs obtained by hiding edges below a
display weight 0..1, for Part 3 to optimise.

Outputs: is_a.json (distributions + dag), is_a_edges.csv (all weighted edges), is_a.md (tree
view + metrics), taxonomy_dag.json (nodes/edges/metrics, verified acyclic), is_a.dot,
dag_metrics.json (metrics across display weights).
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

from taxonomy.dag_metrics import dag_metrics, summary
from taxonomy.llm_context import ROOT, build_request, client, load_corpus
from taxonomy.prompts import TASK_B_CATALOGUE_HEADER, TASKS
from taxonomy.term_types import JSON_OUT as TERM_TYPES_JSON, parse_corpus, quote_found

OUT_DIR = ROOT / "output"
JSON_OUT = OUT_DIR / "is_a.json"
EDGES_OUT = OUT_DIR / "is_a_edges.csv"
MD_OUT = OUT_DIR / "is_a.md"
DAG_OUT = OUT_DIR / "taxonomy_dag.json"
DOT_OUT = OUT_DIR / "is_a.dot"
METRICS_OUT = OUT_DIR / "dag_metrics.json"
CATEGORIES = ["asset", "technology", "actor", "activity", "obligation_or_risk"]


def load_term_types() -> list[dict]:
    if not TERM_TYPES_JSON.exists():
        sys.exit(f"{TERM_TYPES_JSON} missing: run python -m taxonomy.term_types first")
    return json.loads(TERM_TYPES_JSON.read_text(encoding="utf-8"))["term_types"]


def catalogue_block(tts: list[dict]) -> str:
    """Compact catalogue of all term types: the cached system block for Task B."""
    rows = [{"id": t["id"], "name": t["name"], "applies_to": t["applies_to"], "question": t["question"],
             "values": [v["value"] for v in t["values"]], "aliases": t.get("aliases", [])} for t in tts]
    return TASK_B_CATALOGUE_HEADER + json.dumps(rows, ensure_ascii=False, indent=0) + "\n</term_type_catalogue>\n"


def child_text(t: dict) -> str:
    return json.dumps({"id": t["id"], "name": t["name"], "applies_to": t["applies_to"], "question": t["question"],
                       "description": t["description"], "aliases": t.get("aliases", []),
                       "values": [{"value": v["value"], "definition": v["definition"]} for v in t["values"]]},
                      ensure_ascii=False, indent=1)


def candidates_text(cands: list[dict]) -> str:
    return "\n".join(f'- {c["id"]}: {c["name"]} — {c["question"]}' for c in cands)


def extract_json(text: str) -> dict:
    text = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", text.strip())
    return json.loads(text[text.find("{"):text.rfind("}") + 1])


def normalise(dist: list[dict], allowed: set[str]) -> tuple[list[dict], float, list[str]]:
    """Drop unknown parents and the "none" entry, clamp negatives, merge duplicates, and
    renormalise over candidate parents to sum exactly 1. Returns (distribution, p_none, dropped)."""
    merged: dict[str, dict] = {}
    dropped, p_none = [], 0.0
    for e in dist:
        pid = str(e.get("parent", "")).strip()
        p = max(float(e.get("probability", 0) or 0), 0.0)
        if pid == "none":
            p_none += p
            continue
        if pid not in allowed:
            dropped.append(pid)
            continue
        if pid in merged:
            merged[pid]["probability"] += p
        else:
            merged[pid] = {"parent": pid, "probability": p, "rationale": e.get("rationale", ""),
                           "citations": e.get("citations", []) or []}
    total = sum(e["probability"] for e in merged.values())
    for e in merged.values():
        e["probability"] = round(e["probability"] / total, 4) if total > 0 else round(1 / len(merged), 4)
    out = sorted(merged.values(), key=lambda e: -e["probability"])
    if out:
        out[0]["probability"] = round(out[0]["probability"] + (1.0 - sum(e["probability"] for e in out)), 4)
    return out, round(p_none, 4), dropped


def verify_citations(dist: list[dict], docs) -> tuple[int, int]:
    n = ok = 0
    for e in dist:
        for c in e["citations"]:
            n += 1
            doc = docs.get(c.get("doc"), {})
            hit = c.get("section") in doc and quote_found(c.get("quote", ""), doc[c["section"]])
            if not hit:
                lab = next((l for l, txt in doc.items() if quote_found(c.get("quote", ""), txt)), None)
                if lab:
                    c["cited_section"], c["section"], hit = c.get("section"), lab, True
            c["verified"] = bool(hit)
            ok += hit
    return n, ok


def ask(cl, instructions: str, template: str, catalogue: str, child: dict, cands: list[dict],
        k: int, model: str, effort: str) -> dict:
    prompt = template.format(child=child_text(child), candidates=candidates_text(cands),
                             child_id=child["id"], k=k)
    req = build_request(instructions, prompt, model=model, max_tokens=4000, effort=effort,
                        extra_system=[catalogue], thinking={"type": "disabled"})
    msg = cl.messages.create(**req)
    text = "".join(b.text for b in msg.content if b.type == "text")
    u = msg.usage
    return {"text": text, "stop_reason": msg.stop_reason,
            "usage": {"input_tokens": u.input_tokens, "output_tokens": u.output_tokens,
                      "cache_creation_input_tokens": u.cache_creation_input_tokens,
                      "cache_read_input_tokens": u.cache_read_input_tokens}}


def consolidate(results: list[dict]) -> dict:
    """Greedy acyclic selection over every weighted edge.
    Returns {"nodes": {child: {"parents": [(parent, p), ...], "p_none": float}}, "ties": [...],
             "dropped_for_cycle": [[child, parent, p], ...]}; an empty parents list means root."""
    p_none = {r["child"]: r.get("p_none", 0.0) for r in results}
    P = {(r["child"], e["parent"]): e["probability"] for r in results for e in r["distribution"]}
    parents: dict[str, list[tuple[str, float]]] = {r["child"]: [] for r in results}
    dropped: list[list] = []

    def reaches(src: str, dst: str) -> bool:        # is dst an ancestor-or-self of src?
        stack, seen = [src], set()
        while stack:
            n = stack.pop()
            if n == dst:
                return True
            if n not in seen:
                seen.add(n)
                stack.extend(pp for pp, _ in parents.get(n, []))
        return False

    for p, (child, parent) in sorted(((p, k) for k, p in P.items()), reverse=True):
        if p <= 0:
            continue
        if reaches(parent, child):                   # parent already descends from child -> cycle
            dropped.append([child, parent, p])
            continue
        parents[child].append((parent, p))

    ties = [[c, q, p] for c, ps in parents.items() for q, p in ps
            if P.get((q, c)) is not None and abs(P[(q, c)] - p) < 1e-9]

    indeg = {c: len(ps) for c, ps in parents.items()}
    kids: dict[str, list[str]] = {}
    for c, ps in parents.items():
        for q, _ in ps:
            kids.setdefault(q, []).append(c)
    order, queue = [], [c for c, d in indeg.items() if d == 0]
    while queue:
        n = queue.pop()
        order.append(n)
        for k in kids.get(n, []):
            indeg[k] -= 1
            if indeg[k] == 0:
                queue.append(k)
    assert len(order) == len(parents), "consolidated graph is not acyclic"
    return {"nodes": {c: {"parents": ps, "p_none": p_none[c]} for c, ps in parents.items()},
            "ties": ties, "dropped_for_cycle": dropped}


def prune(dag: dict, min_w: float) -> dict:
    """Sub-DAG keeping only edges with weight >= min_w (a display/what-if filter, not a rule)."""
    return {"nodes": {c: {"parents": [(q, p) for q, p in n["parents"] if p >= min_w - 1e-12], "p_none": n["p_none"]}
                      for c, n in dag["nodes"].items()}, "ties": dag["ties"], "dropped_for_cycle": dag["dropped_for_cycle"]}


def all_metrics(results: list[dict], dag: dict) -> dict:
    parents = {c: n["parents"] for c, n in dag["nodes"].items()}
    cats = {r["child"]: r["category"] for r in results}
    return {"overall": dag_metrics(parents),
            "by_category": {cat: dag_metrics(parents, [c for c in parents if cats[c] == cat]) for cat in CATEGORIES
                            if any(cats[c] == cat for c in parents)}}


def metrics_spectrum(results: list[dict], dag: dict, step: float = 0.01) -> list[dict]:
    out = []
    n = int(round(1 / step))
    for i in range(n + 1):
        thr = round(i * step, 4)
        m = all_metrics(results, prune(dag, thr))
        out.append({"min_weight": thr, **summary(m["overall"]),
                    "by_category": {cat: summary(v) for cat, v in m["by_category"].items()}})
    return out


def _metric_line(m: dict) -> str:
    return (f"{m['nodes']} nodes, {m['edges']} is-a edges, {m['roots']} roots, {m['leaves']} leaves, max depth {m['max_depth']}; "
            f"information gain {m['information_gain']['total_bits']:.2f} bits total, {m['information_gain']['bits_per_descent']:.2f} bits per descent; "
            f"AUC {m['auc']['value']:.3f}, expected depth {m['auc']['expected_depth']:.2f}; "
            f"effective leaves {m['leaves_needed']['effective_leaves']:.1f}, {m['leaves_needed']['leaves_for_90pct']} leaves hold 90% of descents.")


def render_md(results: list[dict], by_id: dict[str, dict], dag: dict, metrics: dict) -> str:
    nodes = dag["nodes"]
    lines = ["# Task B output: is-a DAG of term types", "",
             "Each child's weights over its candidate parents sum to 1 (the model's `none` entry is removed and recorded as "
             "P(none)). Every weighted edge is kept unless it would close a cycle; edges are taken greedily by weight, so a "
             "mutual pair resolves to the stronger direction. The first kept parent is the tree position; further parents "
             "appear as *also under*. Roots have no kept parent. Full distributions: `output/is_a.json`; DAG as "
             "nodes/edges/metrics: `output/taxonomy_dag.json`, `output/is_a.dot`; metrics when hiding edges below a weight: "
             "`output/dag_metrics.json`.", "",
             "**Overall.** " + _metric_line(metrics["overall"]),
             f"Edges dropped to keep the graph acyclic: {len(dag['dropped_for_cycle'])}.", ""]
    if dag["ties"]:
        lines += ["Exact ties resolved by id order (review): " + "; ".join(f"`{c}` is-a `{q}` ({p:.2f}, reverse equal)" for c, q, p in dag["ties"]), ""]
    for cat in CATEGORIES:
        ids = [r["child"] for r in results if r["category"] == cat]
        if not ids:
            continue
        children: dict[str, list[str]] = {}
        for c in ids:
            prim = nodes[c]["parents"][0][0] if nodes[c]["parents"] else "none"
            children.setdefault(prim, []).append(c)
        lines += [f"## {cat}", "", _metric_line(metrics["by_category"][cat]), ""]
        ig = metrics["by_category"][cat]["information_gain"]["per_node"]

        def walk(node: str, depth: int) -> None:
            kids = children.get(node, [])
            kids.sort(key=lambda x: -(nodes[x]["parents"][0][1] if nodes[x]["parents"] else nodes[x]["p_none"]))
            for c in kids:
                ps = nodes[c]["parents"]
                tag = f"  (w={ps[0][1]:.2f})" if ps else "  (root)"
                also = "; also under " + ", ".join(f"`{q}` (p={pq:.2f})" for q, pq in ps[1:]) if len(ps) > 1 else ""
                bits = f"; IG {ig[c]:.2f} bits" if c in ig else ""
                lines.append("  " * depth + f"- {by_id[c]['name']} `{c}`{tag}{also}{bits}")
                walk(c, depth + 1)

        walk("none", 0)
        lines.append("")
    return "\n".join(lines)


def export_dag(results: list[dict], by_id: dict[str, dict], dag: dict, metrics: dict) -> None:
    nodes = dag["nodes"]
    out = {"relation": "is-a", "threshold": None,
           "nodes": [{"id": c, "name": by_id[c]["name"], "category": by_id[c]["applies_to"],
                      "question": by_id[c]["question"], "root": not nodes[c]["parents"], "p_none": nodes[c]["p_none"]}
                     for c in nodes],
           "edges": [{"child": c, "parent": q, "probability": p} for c in nodes for q, p in nodes[c]["parents"]],
           "ties": dag["ties"], "dropped_for_cycle": dag["dropped_for_cycle"], "metrics": metrics}
    DAG_OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    dot = ["digraph is_a {", "  rankdir=BT; node [shape=box, fontsize=10];"]
    for cat in CATEGORIES:
        ids = [c for c in nodes if by_id[c]["applies_to"] == cat]
        if ids:
            dot.append(f'  subgraph "cluster_{cat}" {{ label="{cat}";')
            dot += [f'    "{c}" [label="{by_id[c]["name"].replace(chr(34), "")}"];' for c in ids]
            dot.append("  }")
    dot += [f'  "{c}" -> "{q}" [label="{p:.2f}"];' for c in nodes for q, p in nodes[c]["parents"]]
    dot.append("}")
    DOT_OUT.write_text("\n".join(dot), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--effort", default="high", choices=["low", "medium", "high"])
    ap.add_argument("--k", type=int, default=6, help="max entries in each distribution, incl. none")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--only", default="", help="comma-separated categories to run")
    ap.add_argument("--limit", type=int, default=0, help="run only the first N children (smoke test)")
    ap.add_argument("--render-only", action="store_true", help="rebuild the DAG and is_a.md from saved is_a.json")
    args = ap.parse_args()
    OUT_DIR.mkdir(exist_ok=True)

    tts = load_term_types()
    by_id = {t["id"]: t for t in tts}
    if args.render_only:
        saved = json.loads(JSON_OUT.read_text(encoding="utf-8"))
        results = saved["is_a"]
        for r in results:                      # saved by an older run? strip "none" and renormalise over parents
            allowed = {t["id"] for t in tts if t["applies_to"] == r["category"] and t["id"] != r["child"]}
            dist, p_none, _ = normalise(r["distribution"], allowed)
            r["distribution"], r["p_none"] = dist, r.get("p_none", p_none)
        finish(results, by_id, saved)
        return
    cats = [c for c in args.only.split(",") if c] or CATEGORIES
    children = [t for t in tts if t["applies_to"] in cats][: args.limit or None]
    instructions, template = TASKS["B"]
    catalogue = catalogue_block(tts)
    docs = parse_corpus(load_corpus())
    cl = client()

    # warm the caches once (corpus + catalogue) before fanning out
    t0 = time.time()
    first = ask(cl, instructions, template, catalogue, children[0],
                [t for t in tts if t["applies_to"] == children[0]["applies_to"] and t["id"] != children[0]["id"]],
                args.k, args.model, args.effort)
    print(f"warm-up: cache_creation={first['usage']['cache_creation_input_tokens']} "
          f"cache_read={first['usage']['cache_read_input_tokens']} ({time.time() - t0:.0f}s)", file=sys.stderr)

    raw: dict[str, dict] = {children[0]["id"]: first}
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(ask, cl, instructions, template, catalogue, t,
                          [c for c in tts if c["applies_to"] == t["applies_to"] and c["id"] != t["id"]],
                          args.k, args.model, args.effort): t["id"] for t in children[1:]}
        for i, f in enumerate(as_completed(futs), 2):
            raw[futs[f]] = f.result()
            print(f"  {i}/{len(children)} {futs[f]}", file=sys.stderr)

    results, n_cit = [], [0, 0]
    usage = {"input_tokens": 0, "output_tokens": 0, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}
    for t in children:
        r = raw[t["id"]]
        for key in usage:
            usage[key] += r["usage"][key]
        allowed = {c["id"] for c in tts if c["applies_to"] == t["applies_to"] and c["id"] != t["id"]} | {"none"}
        try:
            dist, p_none, dropped = normalise(extract_json(r["text"]).get("distribution", []), allowed)
        except (json.JSONDecodeError, ValueError) as e:
            dist, p_none, dropped = [], 0.0, [f"unparseable: {e}"]
        n, ok = verify_citations(dist, docs)
        n_cit[0] += n
        n_cit[1] += ok
        results.append({"child": t["id"], "name": t["name"], "category": t["applies_to"], "distribution": dist,
                        "p_none": p_none, "dropped_parents": dropped, "stop_reason": r["stop_reason"]})

    meta = {"task": "B", "model": args.model, "effort": args.effort, "k": args.k, "children": len(children),
            "seconds": round(time.time() - t0, 1), "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "usage": usage, "citations": n_cit[0], "citations_verified": n_cit[1]}
    finish(results, by_id, {"run": meta, "is_a": results})
    print(f"citations {n_cit[1]}/{n_cit[0]} verified; usage {usage}; {meta['seconds']}s")


def finish(results: list[dict], by_id: dict[str, dict], saved: dict) -> None:
    """Consolidate, measure, and write every output file."""
    dag = consolidate(results)
    metrics = all_metrics(results, dag)
    saved["dag"] = {"threshold": None, **dag}
    JSON_OUT.write_text(json.dumps(saved, indent=2, ensure_ascii=False), encoding="utf-8")
    with EDGES_OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["child", "parent", "weight", "category", "kept_in_dag"])
        kept = {(c, q) for c, n in dag["nodes"].items() for q, _ in n["parents"]}
        for r in results:
            for e in r["distribution"]:
                w.writerow([r["child"], e["parent"], e["probability"], r["category"], (r["child"], e["parent"]) in kept])
    MD_OUT.write_text(render_md(results, by_id, dag, metrics), encoding="utf-8")
    export_dag(results, by_id, dag, metrics)
    METRICS_OUT.write_text(json.dumps({"step": 0.01, "note": "metrics of the sub-DAG keeping edges with weight >= min_weight",
                                       "spectrum": metrics_spectrum(results, dag)}, indent=1), encoding="utf-8")
    print_dag(results, dag, metrics)
    print(f"-> {JSON_OUT}\n-> {EDGES_OUT}\n-> {MD_OUT}\n-> {DAG_OUT}\n-> {DOT_OUT}\n-> {METRICS_OUT}")


def print_dag(results: list[dict], dag: dict, metrics: dict) -> None:
    nodes = dag["nodes"]
    for r in results:
        ps = nodes[r["child"]]["parents"]
        head = f"{ps[0][0][:36]:36} w={ps[0][1]:.2f}" if ps else f"{'ROOT':36} (P(none) was {nodes[r['child']]['p_none']:.2f})"
        extra = f"  +{len(ps) - 1} more parent(s)" if len(ps) > 1 else ""
        print(f"{r['child'][:38]:38} is-a {head}{extra}")
    sums = [round(sum(e["probability"] for e in r["distribution"]), 4) for r in results]
    m = metrics["overall"]
    print(f"\nacyclic: yes; every distribution sums to 1: {all(x == 1.0 for x in sums)}; ties: {len(dag['ties'])}; "
          f"edges dropped for cycles: {len(dag['dropped_for_cycle'])}")
    print("overall: " + _metric_line(m))
    for cat, v in metrics["by_category"].items():
        print(f"  {cat:18} " + _metric_line(v))


if __name__ == "__main__":
    main()
