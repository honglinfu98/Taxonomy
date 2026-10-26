"""Versioned catalogue (term types + DAG) and the evolution log.

output/evolution/
  v0/                 the seed: Part 1's term_types.json and taxonomy_dag.json, copied once
  v1/, v2/, ...       catalogue after each accepted evolution step (evolve.py)
  iter_01/, ...       one folder per classification iteration: sample used, tags, summary,
                      maintenance report, discovery candidates
  evolution.json/.md  one entry per iteration: catalogue used, items, objectives, cost, time,
                      candidates accepted, catalogue produced

Every version holds term_types.json (the list used by the tagger's catalogue block) and
dag.json (nodes, edges, metrics) plus meta.json (provenance). Nodes, edges and values added
by evolution carry "status": "candidate" so seed and discovered structure stay separable.
"""
from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from taxonomy.establishment.dag_metrics import dag_metrics
from taxonomy.establishment.is_a import CATEGORIES, DAG_OUT as SEED_DAG
from taxonomy.establishment.term_types import JSON_OUT as SEED_TERM_TYPES
from taxonomy.llm_context import ROOT

EVOL = ROOT / "output" / "evolution"
LOG = EVOL / "evolution.json"
LOG_MD = EVOL / "evolution.md"


def version_dir(n: int) -> Path:
    return EVOL / f"v{n}"


def iter_dir(k: int) -> Path:
    return EVOL / f"iter_{k:02d}"


def versions() -> list[int]:
    return sorted(int(m.group(1)) for p in EVOL.glob("v*") if (m := re.fullmatch(r"v(\d+)", p.name)))


def iterations() -> list[int]:
    return sorted(int(m.group(1)) for p in EVOL.glob("iter_*") if (m := re.fullmatch(r"iter_(\d+)", p.name)))


def latest_version() -> int:
    init_seed()
    return versions()[-1]


def init_seed() -> Path:
    """Copy the Part 1 outputs to v0 once; the seed is never modified afterwards."""
    d = version_dir(0)
    if (d / "dag.json").exists():
        return d
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(SEED_TERM_TYPES, d / "term_types.json")
    shutil.copy(SEED_DAG, d / "dag.json")
    dag = json.loads((d / "dag.json").read_text(encoding="utf-8"))
    (d / "meta.json").write_text(json.dumps({
        "version": 0, "role": "seed", "source": {"term_types": str(SEED_TERM_TYPES.relative_to(ROOT)),
                                                  "dag": str(SEED_DAG.relative_to(ROOT))},
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "nodes": len(dag["nodes"]), "edges": len(dag["edges"]),
        "values": sum(len(t["values"]) for t in json.loads((d / "term_types.json").read_text(encoding="utf-8"))["term_types"]),
    }, indent=1), encoding="utf-8")
    return d


def load_version(n: int) -> tuple[list[dict], dict, dict]:
    init_seed()
    d = version_dir(n)
    tts = json.loads((d / "term_types.json").read_text(encoding="utf-8"))["term_types"]
    dag = json.loads((d / "dag.json").read_text(encoding="utf-8"))
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    return tts, dag, meta


def save_version(n: int, tts: list[dict], dag: dict, meta: dict) -> Path:
    """Write v{n}; recomputes the DAG's prior metrics (candidate edges count with weight 1)."""
    d = version_dir(n)
    d.mkdir(parents=True, exist_ok=True)
    parents: dict[str, list[tuple[str, float]]] = {nd["id"]: [] for nd in dag["nodes"]}
    for e in dag["edges"]:
        parents[e["child"]].append((e["parent"], e["probability"] if e.get("probability") is not None else 1.0))
    cats = {nd["id"]: nd["category"] for nd in dag["nodes"]}
    dag["metrics"] = {"overall": dag_metrics(parents),
                      "by_category": {c: dag_metrics(parents, [i for i in parents if cats[i] == c]) for c in CATEGORIES
                                      if any(cats[i] == c for i in parents)}}
    (d / "term_types.json").write_text(json.dumps({"term_types": tts}, indent=1, ensure_ascii=False), encoding="utf-8")
    (d / "dag.json").write_text(json.dumps(dag, indent=1, ensure_ascii=False), encoding="utf-8")
    meta = {**meta, "version": n, "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "nodes": len(dag["nodes"]), "edges": len(dag["edges"]), "values": sum(len(t["values"]) for t in tts),
            "candidate_nodes": sum(1 for nd in dag["nodes"] if nd.get("status") == "candidate"),
            "candidate_values": sum(1 for t in tts for v in t["values"] if v.get("status") == "candidate")}
    (d / "meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
    return d


def read_log() -> list[dict]:
    return json.loads(LOG.read_text(encoding="utf-8")) if LOG.exists() else []


def write_log(entries: list[dict]) -> None:
    EVOL.mkdir(parents=True, exist_ok=True)
    LOG.write_text(json.dumps(entries, indent=1, ensure_ascii=False), encoding="utf-8")
    LOG_MD.write_text(render_log(entries), encoding="utf-8")


def upsert_log(entry: dict) -> None:
    entries = [e for e in read_log() if e.get("iteration") != entry["iteration"]]
    entries.append(entry)
    entries.sort(key=lambda e: e["iteration"])
    write_log(entries)


def render_log(entries: list[dict]) -> str:
    lines = ["# Evolution of the taxonomy DAG", "",
             "Seed = v0, the Part 1 DAG (never modified). Each iteration tags a disjoint batch of DLT-Corpus items "
             "with the catalogue version in force, measures the DAG on that content, discovers candidates at impure "
             "nodes, and consolidates the accepted ones into the next version.", "",
             "| iter | catalogue | items | tags/item | bits/descent (tags) | AUC (tags) | eff. leaves/nodes (tags) | "
             "candidates (accepted) | produced | nodes / edges / values | API cost | API time |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for e in entries:
        o, c, t = e.get("objectives", {}), e.get("cost", {}), e.get("time", {})
        out = e.get("produced_version")
        lines.append(f"| {e['iteration']} | v{e['catalogue_version']} | {e.get('items')} | {e.get('tags_per_item')} | "
                     f"{o.get('bits_per_descent')} | {o.get('auc')} | {o.get('effective_leaves_over_nodes')} | "
                     f"{e.get('candidates')} ({e.get('accepted')}) | {('v' + str(out)) if out is not None else '-'} | "
                     f"{e.get('result_nodes')} / {e.get('result_edges')} / {e.get('result_values')} | "
                     f"${c.get('total_usd')} | {t.get('api_seconds')} s API, {t.get('wall_seconds')} s wall |")
    for e in entries:
        lines += ["", f"## Iteration {e['iteration']} (catalogue v{e['catalogue_version']}, {e.get('timestamp', '')[:10]})", ""]
        lines.append(f"Sample: {e.get('sample')} ({e.get('items')} items; {e.get('sources')}). Tags: {e.get('tags')} "
                     f"({e.get('tags_per_item')} per item), evidence verified {e.get('evidence_verified')}, off-topic {e.get('off_topic')}.")
        o = e.get("objectives", {})
        lines.append(f"Objectives from tags: {o.get('bits_per_descent')} bits/descent, AUC {o.get('auc')}, expected depth "
                     f"{o.get('expected_depth')}, effective leaves {o.get('effective_leaves')} ({o.get('effective_leaves_over_nodes')} per node); "
                     f"prior (is-a weights): {o.get('prior_bits_per_descent')} bits, AUC {o.get('prior_auc')}.")
        lines.append(f"Nodes with items {e.get('nodes_with_items')}/{e.get('nodes')}; dormant {e.get('dormant')}; collapsed {e.get('collapsed')}; "
                     f"discovery targets {e.get('discovery_targets')}; candidates {e.get('candidates')}, accepted {e.get('accepted')}.")
        c, t = e.get("cost", {}), e.get("time", {})
        lines.append(f"API: {c.get('requests')} requests, {c.get('input_tokens')} input + {c.get('cache_read_tokens')} cached + "
                     f"{c.get('output_tokens')} output tokens, ${c.get('total_usd')} (tagging ${c.get('tagging_usd')}, discovery ${c.get('discovery_usd')}, "
                     f"consolidation ${c.get('evolve_usd')}); time {t.get('api_seconds')} s in API calls"
                     + (f" (mean {t.get('mean_request_s')} s, p95 {t.get('p95_request_s')} s per request)" if t.get("mean_request_s") is not None
                        else " (per-request latency not recorded)")
                     + f", {t.get('wall_seconds')} s wall with {t.get('workers')} workers.")
        if e.get("added_term_types") or e.get("added_values"):
            lines.append("Added to the catalogue:")
            lines += [f"- term type **{a['name']}** `{a['id']}` under `{', '.join(a['parents'])}`: {a['question']} "
                      f"(values: {', '.join(a['values'])}; from {a.get('merged_from', 1)} candidate(s), {a.get('support')} items)"
                      for a in e.get("added_term_types", [])]
            lines += [f"- value **{a['value']}** of `{a['term_type']}`: {a['definition']} ({a.get('support')} items)"
                      for a in e.get("added_values", [])]
        elif e.get("produced_version") is None:
            lines.append("No candidate accepted; catalogue unchanged.")
    return "\n".join(lines)
