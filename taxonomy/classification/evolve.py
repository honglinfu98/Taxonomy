"""Consolidate an iteration's accepted discovery candidates into the next catalogue version
and append the iteration to the evolution log.

    python -m taxonomy.classification.evolve [--iter K] [--dry-run]

Reads output/evolution/iter_K/maintenance.json (accepted candidates) and tags_summary.json
(items, cost, time), asks the model once to merge duplicate candidates across nodes and to
place each new term type under the existing node(s) it refines, validates the answer
(parents must exist, ids unique, values non-empty), and writes v{N+1} where N is the
catalogue version iteration K was tagged with. New nodes, edges and values carry
"status": "candidate"; candidate edges get weight 1.0 until Task B re-estimates them.
If nothing was accepted, no version is written but the iteration is still logged.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone

from taxonomy.classification import catalogue as cat
from taxonomy.classification.prompts import EVOLVE_INSTRUCTIONS, EVOLVE_PROMPT
from taxonomy.classification.tag import CATEGORIES, PRICE, extract_json
from taxonomy.llm_context import build_request, client


def consolidate(cl, tts: list[dict], candidates: list[dict], model: str) -> tuple[dict, dict, float]:
    nodes = "\n".join(f"- {t['id']} | {t['applies_to']} | {t['name']} | {t['question']}"
                      for c in CATEGORIES for t in tts if t["applies_to"] == c)
    cands = "\n".join(
        f"- [{c['kind']}] at {c['node']}: label={c['label']!r}; question={c.get('question', '')!r}; definition={c['definition']!r}; "
        f"values={c.get('values') or []}; gain={c['gain_bits']} bits; item_ids={c['item_ids']}"
        for c in candidates)
    req = build_request(EVOLVE_INSTRUCTIONS, EVOLVE_PROMPT.format(nodes=nodes, candidates=cands), model=model,
                        max_tokens=6000, effort="high", corpus=False, thinking={"type": "disabled"})
    t0 = time.perf_counter()
    msg = cl.messages.create(**req)
    secs = time.perf_counter() - t0
    u = msg.usage
    usage = {"input": u.input_tokens, "output": u.output_tokens,
             "cache_write": u.cache_creation_input_tokens or 0, "cache_read": u.cache_read_input_tokens or 0}
    text = "".join(b.text for b in msg.content if b.type == "text")
    try:
        parsed = extract_json(text)
    except (json.JSONDecodeError, ValueError):
        sys.exit("consolidation answer was not JSON:\n" + text[:800])
    return parsed, usage, secs


def apply(tts: list[dict], dag: dict, plan: dict, iteration: int) -> tuple[list[dict], dict, list[dict], list[dict]]:
    ids = {t["id"] for t in tts}
    by_id = {t["id"]: t for t in tts}
    added_tt, added_vals = [], []
    for n in plan.get("term_types", []) or []:
        nid = re.sub(r"[^a-z0-9]+", "_", str(n.get("id") or n.get("name") or "").lower()).strip("_")
        parents = [p for p in (n.get("parents") or []) if p in ids]
        vals = [v for v in dict.fromkeys(str(x).strip() for x in (n.get("values") or [])) if v]
        if not nid or nid in ids or not parents or len(vals) < 2 or n.get("category") not in CATEGORIES:
            print(f"  skipped term type {nid!r}: needs unique id, existing parents, >=2 values, valid category", file=sys.stderr)
            continue
        tt = {"id": nid, "name": n.get("name", nid), "applies_to": n["category"], "question": n.get("question", ""),
              "description": n.get("description", ""), "aliases": [], "status": "candidate", "origin": {"iteration": iteration,
              "merged_from": n.get("merged_from") or [], "item_ids": n.get("item_ids") or []},
              "values": [{"value": v, "definition": "", "citations": [], "status": "candidate"} for v in vals],
              "citations": [], "sources": {"documents": [], "jurisdictions": [], "document_classes": ["content_discovery"]}, "notes": ""}
        tts.append(tt)
        ids.add(nid)
        by_id[nid] = tt
        dag["nodes"].append({"id": nid, "name": tt["name"], "category": tt["applies_to"], "question": tt["question"],
                             "root": False, "p_none": None, "status": "candidate"})
        for p in parents:
            dag["edges"].append({"child": nid, "parent": p, "probability": 1.0, "status": "candidate", "iteration": iteration})
        added_tt.append({"id": nid, "name": tt["name"], "question": tt["question"], "values": vals, "parents": parents,
                         "merged_from": len(n.get("merged_from") or []) or 1, "support": len(n.get("item_ids") or [])})
    for v in plan.get("values", []) or []:
        t = by_id.get(str(v.get("term_type", "")))
        label = str(v.get("value", "")).strip()
        if t is None or not label or any(x["value"].lower() == label.lower() for x in t["values"]):
            continue
        t["values"].append({"value": label, "definition": v.get("definition", ""), "citations": [], "status": "candidate",
                            "origin": {"iteration": iteration, "item_ids": v.get("item_ids") or []}})
        added_vals.append({"term_type": t["id"], "value": label, "definition": v.get("definition", ""),
                           "support": len(v.get("item_ids") or [])})
    return tts, dag, added_tt, added_vals


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--iter", type=int, default=None)
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--dry-run", action="store_true", help="consolidate and print, write nothing")
    args = ap.parse_args()
    k = args.iter if args.iter is not None else cat.iterations()[-1]
    d = cat.iter_dir(k)
    maint = json.loads((d / "maintenance.json").read_text(encoding="utf-8"))
    summ = json.loads((d / "tags_summary.json").read_text(encoding="utf-8"))
    version = maint["run"]["catalogue_version"]
    tts, dag, _ = cat.load_version(version)
    accepted = [c for c in maint["discovery"]["candidates"] if c["accepted"]]

    plan, usage, secs = ({"term_types": [], "values": [], "dropped": []}, {key: 0 for key in PRICE}, 0.0)
    if accepted:
        plan, usage, secs = consolidate(client(), tts, accepted, args.model)
    evolve_cost = round(sum(usage[key] * PRICE[key] for key in PRICE), 4)
    produced = None
    added_tt, added_vals = [], []
    if accepted and not args.dry_run:
        tts, dag, added_tt, added_vals = apply(tts, dag, plan, k)
        if added_tt or added_vals:
            produced = version + 1
            cat.save_version(produced, tts, dag, {"role": "evolved", "from_version": version, "iteration": k,
                                                  "accepted_candidates": len(accepted), "plan": plan})
    elif accepted:
        print(json.dumps(plan, indent=1, ensure_ascii=False))

    # evolution log entry
    run, emp, pr = summ["run"], maint["empirical"], maint["prior_reference"]
    tag_u, disc_u = run["usage"], maint["discovery"]["usage"]
    tag_t, disc_t = run.get("time", {}), maint["discovery"].get("time", {})
    disc_cost = maint["discovery"]["cost_usd"]
    entry = {
        "iteration": k, "catalogue_version": version, "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sample": run.get("sample"), "items": summ["items"], "sources": summ["by_source"],
        "tags": summ["tags_total"], "tags_per_item": summ["tags_per_item"],
        "evidence_verified": f"{summ['evidence_verified']}/{summ['tags_total']}", "off_topic": summ["off_topic"],
        "nodes": emp["nodes"], "nodes_with_items": emp["nodes_with_items"],
        "dormant": len(maint["proposals"]["dormant"]), "collapsed": len(maint["proposals"]["collapsed"]),
        "discovery_targets": len(maint["proposals"]["discovery_targets"]),
        "candidates": len(maint["discovery"]["candidates"]), "accepted": len(accepted),
        "objectives": {"bits_per_descent": emp["bits_per_descent"], "auc": emp["auc"], "expected_depth": emp["expected_depth"],
                       "effective_leaves": emp["effective_leaves"], "effective_leaves_over_nodes": emp["effective_leaves_over_nodes"],
                       "prior_bits_per_descent": pr["bits_per_descent"], "prior_auc": pr["auc"]},
        "cost": {"requests": tag_t.get("requests", summ["items"]) + maint["discovery"]["calls"] + (1 if accepted else 0),
                 "input_tokens": tag_u["input"] + disc_u["input"] + usage["input"],
                 "cache_read_tokens": tag_u["cache_read"] + disc_u["cache_read"] + usage["cache_read"],
                 "output_tokens": tag_u["output"] + disc_u["output"] + usage["output"],
                 "tagging_usd": run["cost_usd"], "discovery_usd": disc_cost, "evolve_usd": evolve_cost,
                 "total_usd": round(run["cost_usd"] + disc_cost + evolve_cost, 4)},
        "time": {"api_seconds": round((tag_t.get("api_seconds") or 0) + (disc_t.get("api_seconds") or 0) + secs, 1),
                 "wall_seconds": round((run.get("seconds") or 0) + (maint["discovery"].get("seconds") or 0) + secs, 1),
                 "note": tag_t.get("note"),
                 "mean_request_s": tag_t.get("mean_request_s"), "p95_request_s": tag_t.get("p95_request_s"),
                 "workers": tag_t.get("workers")},
        "produced_version": produced, "added_term_types": added_tt, "added_values": added_vals,
        "dropped": plan.get("dropped", []),
        "result_nodes": len(dag["nodes"]), "result_edges": len(dag["edges"]), "result_values": sum(len(t["values"]) for t in tts),
    }
    if not args.dry_run:
        cat.upsert_log(entry)
    print(f"iteration {k} on v{version}: {len(accepted)} accepted candidates -> "
          + (f"v{produced}: +{len(added_tt)} term types, +{len(added_vals)} values" if produced else "no new version")
          + f"; consolidation ${evolve_cost}, {secs:.1f}s")
    for a in added_tt:
        print(f"  + {a['id']} under {a['parents']}: {a['question'][:80]} | {a['values']}")
    for a in added_vals:
        print(f"  + value {a['value']!r} of {a['term_type']}")
    print(f"-> {cat.LOG}\n-> {cat.LOG_MD}")


if __name__ == "__main__":
    main()
