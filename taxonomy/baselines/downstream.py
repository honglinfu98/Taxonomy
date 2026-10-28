"""Downstream use of each catalogue: tag the 300 gold items with it and score against the gold
term types.

    python -m taxonomy.baselines.downstream ours zeroshot rag raptor tnt [--runs 3] [--workers 12]

Every catalogue is used the same way: the production tagger prompt with the catalogue block
and no is-a edges (a baseline catalogue has no DAG until Task B is run; holding the hierarchy
out keeps the comparison to the Task A stage). "ours" is the seed catalogue v0.

The gold labels live in the space of catalogue v6, so a baseline's term types are first mapped
to v6 term types by the LLM judge (same-question matching, both directions, intersection);
v0's ids are a subset of v6's and map to themselves. Scoring is at the term-type level: a
predicted type that maps to no gold-space type counts as a false positive (the catalogue
asks a question the gold does not), and a gold type no baseline type maps to can only be a
false negative. Value-level F1 is not comparable across catalogues (different value lists) and
is not reported. Three runs differ by sampling; mean ± sd.
"""
from __future__ import annotations

import argparse
import json

from taxonomy.baselines.common import OUT, Meter, catalogue_path, load_catalogue
from taxonomy.baselines.judge import judge_pairs
from taxonomy.classification import catalogue as cat
from taxonomy.evaluation.common import GOLD, GOLD_ITEMS, micro_macro, pm, read_jsonl, type_set, write_jsonl
from taxonomy.evaluation.tagging_eval import llm_system
from taxonomy.llm_context import client


def mapping(name: str, tts: list[dict], gold_tts: list[dict], judge_model: str) -> tuple[dict[str, str], dict]:
    gold_ids = {t["id"] for t in gold_tts}
    if name in ("ours", "seed"):
        return {t["id"]: t["id"] for t in tts if t["id"] in gold_ids}, {"judge": "identity"}
    p = OUT / name / "map_to_gold.json"
    if p.exists():
        m = json.loads(p.read_text(encoding="utf-8"))
        return m["map"], m["info"]
    meter = Meter(judge_model)
    pairs = judge_pairs(client(), gold_tts, tts, judge_model, meter)
    m = {q["b"]: q["a"] for q in pairs}
    info = {"judge": judge_model, "gold_types": len(gold_tts), "catalogue_types": len(tts), "matched": len(pairs), **meter.report()}
    p.write_text(json.dumps({"map": m, "info": info, "pairs": pairs}, indent=1, ensure_ascii=False), encoding="utf-8")
    return m, info


def score(gold: dict[str, dict], rows: list[dict], m: dict[str, str]) -> dict:
    g = {i: type_set(x["tags"]) for i, x in gold.items()}
    p = {r["item_id"]: {m.get(t, "unmapped:" + t) for t in type_set(r["tags"])} for r in rows}
    res = micro_macro(g, p)
    n_pred = sum(len(type_set(r["tags"])) for r in rows)
    res["mapped_share"] = round(sum(1 for r in rows for t in type_set(r["tags"]) if t in m) / max(n_pred, 1), 3)
    return res


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("names", nargs="+")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--judge-model", default="claude-haiku-5-5")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    gsum = json.loads((OUT.parent / "evaluation" / "gold_summary.json").read_text(encoding="utf-8"))
    gold_tts, _, _ = cat.load_version(gsum["catalogue_version"])
    items = read_jsonl(GOLD_ITEMS)[: a.limit or None]
    gold = {g["item_id"]: g for g in read_jsonl(GOLD) if g["item_id"] in {it["id"] for it in items}}
    for name in a.names:
        tts = load_catalogue(name)["term_types"]
        m, info = mapping(name, tts, gold_tts, a.judge_model)
        runs = []
        for r in range(1, a.runs + 1):
            rows, run_info = llm_system("dag", items, tts, {"edges": []}, a.model, a.effort, a.workers)
            write_jsonl(OUT / name / f"pred_gold_run{r}.jsonl", rows)
            s = score(gold, rows, m)
            runs.append({"run": r, "metrics": s, "run_info": run_info})
            print(f"{name} run {r}: type micro-F1 {s['micro_f1']} macro-F1 {s['macro_f1']} P {s['micro_p']} R {s['micro_r']} "
                  f"mapped {s['mapped_share']} (${run_info['cost_usd']}, {run_info['wall_seconds']} s)", flush=True)
        (OUT / name).mkdir(parents=True, exist_ok=True)
        (OUT / name / "downstream.json").write_text(json.dumps({"gold_version": gsum["catalogue_version"], "items": len(items), "term_types": len(tts),
                                                                "mapped_types": len(m), "mapping": info, "runs": runs}, indent=1), encoding="utf-8")
    # aggregate every catalogue that has a result (runs of other catalogues may be in flight in other processes)
    res = {"gold_version": gsum["catalogue_version"], "items": len(items), "systems": {}}
    for q in sorted(OUT.glob("*/downstream.json")):
        res["systems"][q.parent.name] = json.loads(q.read_text(encoding="utf-8"))
    (OUT / "downstream.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    md = ["# Downstream tagging with each catalogue (gold term types, type level)", "",
          f"{res['items']} gold items; gold in catalogue v{res['gold_version']} space; tagger Haiku 5.5, catalogue block without is-a edges; "
          "baseline term types mapped to gold term types by the LLM judge; mean ± sd over runs.", "",
          "| catalogue | term types | mapped to gold | micro-F1 | macro-F1 | P | R | pred types/item | mapped share of predictions |", "|---|---|---|---|---|---|---|---|---|"]
    for n, s in res["systems"].items():
        ms = [r["metrics"] for r in s["runs"]]
        md.append(f"| {n} | {s['term_types']} | {s['mapped_types']} | {pm([x['micro_f1'] for x in ms])} | {pm([x['macro_f1'] for x in ms])} | "
                  f"{pm([x['micro_p'] for x in ms])} | {pm([x['micro_r'] for x in ms])} | {pm([x['pred_per_item'] for x in ms], 2)} | {pm([x['mapped_share'] for x in ms])} |")
    (OUT / "downstream.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
