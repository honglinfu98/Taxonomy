"""Build the interactive is-a dashboard: output/is_a_dashboard.html.

    python -m taxonomy.dashboard

Embeds every Task B distribution (output/is_a.json) and the Task A term types into one
self-contained HTML page with a threshold slider. The page re-runs the same consolidation
as is_a.consolidate() in the browser (greedy acyclic is-a edges >= threshold, above the
child's P(none); same-as for near-symmetric mutual pairs), so you can watch the DAG change
across the whole 0..1 spectrum and inspect every node's distribution and rationales.
"""
from __future__ import annotations

import json
from pathlib import Path

from taxonomy.is_a import JSON_OUT as IS_A_JSON
from taxonomy.llm_context import ROOT
from taxonomy.term_types import JSON_OUT as TERM_TYPES_JSON

HTML_OUT = ROOT / "output" / "is_a_dashboard.html"
TEMPLATE = Path(__file__).with_name("dashboard_template.html")


def build_data() -> dict:
    tts = json.loads(TERM_TYPES_JSON.read_text(encoding="utf-8"))["term_types"]
    saved = json.loads(IS_A_JSON.read_text(encoding="utf-8"))
    by_id = {t["id"]: t for t in tts}
    nodes, edges = [], []
    for r in saved["is_a"]:
        t = by_id[r["child"]]
        p_none = 0.0
        for e in r["distribution"]:
            if e["parent"] == "none":
                p_none = e["probability"]
                continue
            edges.append({"c": r["child"], "p": e["parent"], "w": e["probability"],
                          "r": e.get("rationale", ""),
                          "cv": sum(1 for c in e.get("citations", []) if c.get("verified")),
                          "cn": len(e.get("citations", []))})
        nodes.append({"id": t["id"], "name": t["name"], "cat": t["applies_to"], "q": t["question"],
                      "pn": p_none, "vals": [v["value"] for v in t["values"]]})
    run = saved.get("run", {})
    return {"nodes": nodes, "edges": edges, "defaults": {"thr": 0.4, "margin": 0.1},
            "run": {"model": run.get("model"), "timestamp": run.get("timestamp"),
                    "children": run.get("children"), "citations": run.get("citations"),
                    "verified": run.get("citations_verified")}}


def main() -> None:
    data = build_data()
    html = TEMPLATE.read_text(encoding="utf-8").replace("__DATA__", json.dumps(data, ensure_ascii=False))
    HTML_OUT.write_text(html, encoding="utf-8")
    print(f"{len(data['nodes'])} nodes, {len(data['edges'])} weighted edges -> {HTML_OUT} ({HTML_OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
