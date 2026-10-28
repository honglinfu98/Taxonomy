"""Task B (is-a DAG) over a baseline catalogue, so its structure can be measured like ours.

    python -m taxonomy.baselines.structure zeroshot [rag raptor tnt] [--workers 8]

Runs the unchanged Task B prompt (cached corpus + the catalogue as a second cached block, one
call per term type over the candidates of its category), consolidates the acyclic DAG and
computes the same metrics (bits per descent, reach-a-leaf AUC, effective leaves). Writes
output/baselines/<name>/dag.json in the evolution dag.json shape. Task B is corpus-grounded for
every catalogue, including the zero-shot and TnT-LLM ones that were built without it: the
comparison is of the Task A stage, with the hierarchy stage held fixed.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from taxonomy.baselines.common import OUT, load_catalogue
from taxonomy.establishment.dag_metrics import summary
from taxonomy.establishment.is_a import all_metrics, ask, catalogue_block, consolidate, extract_json, normalise, verify_citations
from taxonomy.establishment.prompts import TASKS
from taxonomy.establishment.term_types import parse_corpus
from taxonomy.evaluation.billing import price
from taxonomy.llm_context import client, load_corpus


def run(name: str, model: str, effort: str, k: int, workers: int) -> dict:
    tts = load_catalogue(name)["term_types"]
    by_id = {t["id"]: t for t in tts}
    instructions, template = TASKS["B"]
    catalogue = catalogue_block(tts)
    docs = parse_corpus(load_corpus())
    cl = client()
    t0 = time.time()

    def cands(t):
        return [c for c in tts if c["applies_to"] == t["applies_to"] and c["id"] != t["id"]]

    first = ask(cl, instructions, template, catalogue, tts[0], cands(tts[0]), k, model, effort)   # warm both caches
    raw = {tts[0]["id"]: first}
    with ThreadPoolExecutor(workers) as ex:
        for t, r in zip(tts[1:], ex.map(lambda t: ask(cl, instructions, template, catalogue, t, cands(t), k, model, effort), tts[1:])):
            raw[t["id"]] = r
    results, n_cit, usage = [], [0, 0], {}
    for t in tts:
        r = raw[t["id"]]
        for key, v in r["usage"].items():
            usage[key] = usage.get(key, 0) + (v or 0)
        allowed = {c["id"] for c in cands(t)} | {"none"}
        try:
            dist, p_none, dropped = normalise(extract_json(r["text"]).get("distribution", []), allowed)
        except (json.JSONDecodeError, ValueError) as e:
            dist, p_none, dropped = [], 0.0, [f"unparseable: {e}"]
        n, ok = verify_citations(dist, docs)
        n_cit[0] += n
        n_cit[1] += ok
        results.append({"child": t["id"], "name": t["name"], "category": t["applies_to"], "distribution": dist, "p_none": p_none,
                        "dropped_parents": dropped})
    dag = consolidate(results)
    metrics = all_metrics(results, dag)
    nodes = dag["nodes"]
    u = {"input": usage.get("input_tokens", 0), "output": usage.get("output_tokens", 0),
         "cache_write": usage.get("cache_creation_input_tokens", 0), "cache_read": usage.get("cache_read_input_tokens", 0)}
    out = {"relation": "is-a", "catalogue": name, "run": {"task": "B", "model": model, "effort": effort, "k": k, "calls": len(tts),
                                                         "citations": n_cit[0], "citations_verified": n_cit[1], "usage": u,
                                                         "cost_usd": round(price(u, model, long_prompt=True)[0], 4), "wall_seconds": round(time.time() - t0, 1)},
           "nodes": [{"id": c, "name": by_id[c]["name"], "category": by_id[c]["applies_to"], "question": by_id[c]["question"],
                      "root": not nodes[c]["parents"], "p_none": nodes[c]["p_none"]} for c in nodes],
           "edges": [{"child": c, "parent": q, "probability": p} for c in nodes for q, p in nodes[c]["parents"]],
           "ties": dag["ties"], "dropped_for_cycle": dag["dropped_for_cycle"],
           "metrics": {"overall": metrics["overall"], "by_category": metrics["by_category"], "summary": summary(metrics["overall"])}}
    (OUT / name / "dag.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    s = out["metrics"]["summary"]
    print(f"{name}: {s['nodes']} nodes, {s['edges']} edges, {s['roots']} roots, {s['leaves']} leaves, depth {s['max_depth']}, "
          f"{s['bits_per_descent']} bits/descent, AUC {s['auc']}, effective leaves {s['effective_leaves']}; "
          f"citations {n_cit[1]}/{n_cit[0]}; ${out['run']['cost_usd']}, {out['run']['wall_seconds']} s", flush=True)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("names", nargs="+")
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--effort", default="high")
    ap.add_argument("--k", type=int, default=6)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    for n in a.names:
        run(n, a.model, a.effort, a.k, a.workers)


if __name__ == "__main__":
    main()
