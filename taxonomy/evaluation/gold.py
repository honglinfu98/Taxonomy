"""Held-out gold set for tagging and retrieval evaluation.

    python -m taxonomy.evaluation.gold select   [--size 300] [--seed 11]
    python -m taxonomy.evaluation.gold annotate [--model claude-opus-5-5] [--passes 2] [--version N] [--workers 4] [--limit M]

select: draws size/2 papers and size/2 patents from the sampled DLT-Corpus items (stratified,
seeded), writes output/evaluation/gold_items.jsonl with the texts. These ids are excluded from
the supervised baseline's training data.

annotate: a stronger model (default Opus 5.5, effort high, adaptive thinking) tags every gold item
`passes` times independently with the same catalogue block the system uses. Gold labels are the
(term type, value) pairs that every pass agrees on and whose evidence span is found verbatim in
the text in at least one pass. Writes gold_pass{p}.jsonl, gold.jsonl and gold_summary.json
(agreement between passes, label counts, cost, time). This is an LLM-adjudicated reference
standard: no human labels were used, which the paper must state.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from taxonomy.classification import catalogue as cat
from taxonomy.classification.prompts import TAG_PROMPT, TAGGER_INSTRUCTIONS
from taxonomy.classification.sample import sample_path
from taxonomy.classification.tag import catalogue_block, extract_json, validate
from taxonomy.evaluation.common import GOLD, GOLD_ITEMS, OUT, add_usage, call_llm, cost, label_set, micro_macro, read_jsonl, write_jsonl
from taxonomy.llm_context import client

GOLD_ADDENDUM = ("\nYou are producing reference labels for an evaluation. Be exhaustive and precise: tag every "
                 "(term type, value) the text clearly supports, and none that it does not. Evidence must be verbatim.")


def select(size: int, seed: int) -> None:
    rng = random.Random(seed)
    pools: dict[str, list[dict]] = {"paper": [], "patent": []}
    for k in cat.iterations():
        p = sample_path(k)
        if p.exists():
            for r in read_jsonl(p):
                r["iteration"] = k
                pools[r["source"]].append(r)
    picked = []
    for src, pool in pools.items():
        pool.sort(key=lambda r: r["id"])
        picked += rng.sample(pool, min(size // 2, len(pool)))
    write_jsonl(GOLD_ITEMS, picked)
    counts = ", ".join(f"{src}: {sum(1 for r in picked if r['source'] == src)}" for src in pools)
    print(f"{len(picked)} gold items ({counts}) -> {GOLD_ITEMS}")


def annotate(model: str, passes: int, version: int | None, workers: int, limit: int, effort: str) -> None:
    version = cat.latest_version() if version is None else version
    tts, dag, _ = cat.load_version(version)
    by_id = {t["id"]: t for t in tts}
    parent_of: dict[str, list[str]] = {}
    for e in dag["edges"]:
        parent_of.setdefault(e["child"], []).append(e["parent"])
    catalogue = catalogue_block(tts, dag)
    items = read_jsonl(GOLD_ITEMS)
    if limit:
        items = items[:limit]
    cl = client()
    summary = {"model": model, "effort": effort, "passes": passes, "catalogue_version": version, "items": len(items),
               "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"), "pass_stats": [], "usage": {}}
    runs: list[dict[str, dict]] = []
    for p in range(1, passes + 1):
        usage: dict = {}
        t0 = time.perf_counter()

        def one(item: dict) -> dict:
            prompt = TAG_PROMPT.format(item_id=item["id"], source=item["source"], year=f", {item['year']}" if item.get("year") else "",
                                       title=item["title"], text=item["text"])
            for attempt in range(3):
                try:
                    r = call_llm(cl, TAGGER_INSTRUCTIONS + GOLD_ADDENDUM, prompt, model, effort, [catalogue], max_tokens=8000)
                    parsed = extract_json(r["text"])
                    break
                except (json.JSONDecodeError, ValueError):
                    parsed = {"tags": [], "parse_error": True}
                except Exception as e:  # transient API error
                    if attempt == 2:
                        raise
                    time.sleep(2 * (attempt + 1))
                    continue
            out = validate(item, parsed, by_id, parent_of)
            out["usage"], out["seconds"] = r["usage"], r["seconds"]
            return out

        first = one(items[0])              # warm the catalogue cache once before fanning out
        with ThreadPoolExecutor(workers) as ex:
            results = [first] + list(ex.map(one, items[1:]))
        for r in results:
            add_usage(usage, r.pop("usage"))
        write_jsonl(OUT / f"gold_pass{p}.jsonl", results)
        runs.append({r["item_id"]: r for r in results})
        summary["pass_stats"].append({"pass": p, "tags": sum(len(r["tags"]) for r in results),
                                      "evidence_found": sum(1 for r in results for t in r["tags"] if t["evidence_found"]),
                                      "cost_usd": round(cost(usage, model), 4), "api_seconds": round(sum(r["seconds"] for r in results), 1),
                                      "wall_seconds": round(time.perf_counter() - t0, 1), "usage": usage})
        add_usage(summary["usage"], usage)
        print(f"pass {p}: {summary['pass_stats'][-1]['tags']} tags, ${summary['pass_stats'][-1]['cost_usd']}, {summary['pass_stats'][-1]['wall_seconds']} s")
    # adjudicate
    gold_rows = []
    for item in items:
        sets = [label_set(run[item["id"]]["tags"]) for run in runs]
        agreed = set.intersection(*sets) if sets else set()
        tags = []
        for (tt, v) in sorted(agreed):
            ev = [t for run in runs for t in run[item["id"]]["tags"] if (t["term_type"], t["value"]) == (tt, v)]
            if any(t["evidence_found"] for t in ev):
                tags.append({"term_type": tt, "category": by_id[tt]["applies_to"], "value": v,
                             "confidence": round(sum(t["confidence"] for t in ev) / len(ev), 3),
                             "evidence": next(t["evidence"] for t in ev if t["evidence_found"])})
        gold_rows.append({"item_id": item["id"], "source": item["source"], "title": item["title"],
                          "off_topic": all(run[item["id"]]["off_topic"] for run in runs), "tags": tags,
                          "dropped_disagreement": len(set.union(*sets) - agreed) if sets else 0,
                          "dropped_no_evidence": len(agreed) - len(tags)})
    write_jsonl(GOLD, gold_rows)
    if len(runs) >= 2:
        a = {i: label_set(r["tags"]) for i, r in runs[0].items()}
        b = {i: label_set(r["tags"]) for i, r in runs[1].items()}
        summary["pass_agreement"] = micro_macro(a, b)
    summary["gold"] = {"items": len(gold_rows), "off_topic": sum(1 for g in gold_rows if g["off_topic"]),
                       "labels": sum(len(g["tags"]) for g in gold_rows),
                       "labels_per_item": round(sum(len(g["tags"]) for g in gold_rows) / max(len(gold_rows), 1), 2),
                       "distinct_labels": len({(t["term_type"], t["value"]) for g in gold_rows for t in g["tags"]}),
                       "distinct_term_types": len({t["term_type"] for g in gold_rows for t in g["tags"]}),
                       "dropped_disagreement": sum(g["dropped_disagreement"] for g in gold_rows),
                       "dropped_no_evidence": sum(g["dropped_no_evidence"] for g in gold_rows)}
    summary["cost_usd"] = round(cost(summary["usage"], model), 4)
    (OUT / "gold_summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(f"gold: {summary['gold']}  agreement: {summary.get('pass_agreement', {}).get('micro_f1')}  cost ${summary['cost_usd']}")
    print(f"-> {GOLD}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["select", "annotate"])
    ap.add_argument("--size", type=int, default=300)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--model", default="claude-opus-5-5")
    ap.add_argument("--effort", default="high")
    ap.add_argument("--passes", type=int, default=2)
    ap.add_argument("--version", type=int, default=None)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    if a.cmd == "select":
        select(a.size, a.seed)
    else:
        if not GOLD_ITEMS.exists():
            sys.exit("run `select` first")
        annotate(a.model, a.passes, a.version, a.workers, a.limit, a.effort)


if __name__ == "__main__":
    main()
