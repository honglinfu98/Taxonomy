"""Track how the taxonomy DAG evolves as content is fed in.

    python -m taxonomy.classification.track

Reads every catalogue version in output/evolution/ and the evolution log and writes
output/evolution/evolution_track.{json,md}: per version the structure (nodes, edges, values,
candidates, roots, leaves, depth, prior objectives), per iteration the content-driven
objectives, discovery counts, cost and time, and the lineage of every discovered term type
(iteration, parent, items tagged on it in later iterations).
"""
from __future__ import annotations

import json
from collections import Counter

from taxonomy.classification import catalogue as cat
from taxonomy.retrieval.graph import TaxonomyGraph


def version_row(n: int) -> dict:
    tts, dag, meta = cat.load_version(n)
    g = TaxonomyGraph(dag)
    m = dag.get("metrics", {}).get("overall", {})
    cand_nodes = [nd["id"] for nd in dag["nodes"] if nd.get("status") == "candidate"]
    return {"version": n, "iteration": meta.get("iteration"), "nodes": len(dag["nodes"]), "edges": len(dag["edges"]),
            "values": sum(len(t["values"]) for t in tts),
            "candidate_nodes": len(cand_nodes), "candidate_values": sum(1 for t in tts for v in t["values"] if v.get("status") == "candidate"),
            "roots": len(g.roots), "leaves": len(g.leaves), "max_depth": max(g.depth.values()),
            "mean_parents": round(sum(len(v) for v in g.parents.values()) / len(g.ids), 2),
            "by_category": dict(Counter(nd["category"] for nd in dag["nodes"])),
            "prior_bits_per_descent": m.get("information_gain", {}).get("bits_per_descent"),
            "prior_auc": m.get("auc", {}).get("value"), "prior_expected_depth": m.get("auc", {}).get("expected_depth"),
            "prior_effective_leaves": m.get("leaves_needed", {}).get("effective_leaves"),
            "new_term_types": [{"id": t["id"], "name": t["name"], "category": t["applies_to"],
                                "parents": [e["parent"] for e in dag["edges"] if e["child"] == t["id"]],
                                "values": len(t["values"])} for t in tts if t.get("status") == "candidate"
                               and t.get("origin", {}).get("iteration") == meta.get("iteration")]}


def usage_of_candidates(versions: list[dict]) -> dict[str, dict]:
    """Items tagged directly on each discovered term type in every later iteration."""
    use: dict[str, dict] = {}
    for k in cat.iterations():
        f = cat.iter_dir(k) / "tags.jsonl"
        if not f.exists():
            continue
        counts = Counter()
        for line in f.read_text(encoding="utf-8").split("\n"):
            if not line.strip():
                continue
            r = json.loads(line)
            for y in {t["term_type"] for t in r.get("tags", [])}:
                counts[y] += 1
        for v in versions:
            for t in v["new_term_types"]:
                use.setdefault(t["id"], {"discovered_in_iteration": v["iteration"], "version": v["version"], "parents": t["parents"], "usage": {}})
                if k > (v["iteration"] or 0):
                    use[t["id"]]["usage"][f"iter_{k}"] = counts.get(t["id"], 0)
    return use


def render_md(track: dict) -> str:
    L = ["# Evolution of the taxonomy DAG as content is fed in", "",
         "Seed v0 is the Part 1 DAG; each later version is produced by one iteration of tagging a disjoint "
         "DLT-Corpus batch, measuring the DAG on it, discovering candidates at impure nodes and consolidating "
         "the accepted ones. Cumulative items = items tagged before the version existed.", "",
         "## Structure per version", "",
         "| version | from iteration | cumulative items | nodes (candidate) | edges | values (candidate) | roots | leaves | max depth | mean parents | prior bits/descent | prior AUC | prior eff. leaves |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    cum = 0
    items_by_iter = {e["iteration"]: e["items"] for e in track["iterations"]}
    for v in track["versions"]:
        if v["iteration"] is not None:
            cum += items_by_iter.get(v["iteration"], 0)
        L.append(f"| v{v['version']} | {v['iteration'] if v['iteration'] is not None else 'seed'} | {cum} | {v['nodes']} ({v['candidate_nodes']}) | {v['edges']} | "
                 f"{v['values']} ({v['candidate_values']}) | {v['roots']} | {v['leaves']} | {v['max_depth']} | {v['mean_parents']} | "
                 f"{v['prior_bits_per_descent']} | {v['prior_auc']} | {v['prior_effective_leaves']} |")
    L += ["", "## Content-driven objectives per iteration", "",
          "| iteration | catalogue | items | tags/item | bits/descent | AUC | expected depth | eff. leaves | eff. leaves / nodes | collapsed | targets | candidates | accepted | cost | wall |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for e in track["iterations"]:
        o, c, t = e.get("objectives", {}), e.get("cost", {}), e.get("time", {})
        L.append(f"| {e['iteration']} | v{e['catalogue_version']} | {e['items']} | {e.get('tags_per_item')} | {o.get('bits_per_descent')} | {o.get('auc')} | "
                 f"{o.get('expected_depth')} | {o.get('effective_leaves')} | {o.get('effective_leaves_over_nodes')} | {e.get('collapsed')} | "
                 f"{e.get('discovery_targets')} | {e.get('candidates')} | {e.get('accepted')} | ${c.get('total_usd')} | {round((t.get('wall_seconds') or 0) / 60, 1)} min |")
    L += ["", "## Discovered term types and their later usage", "",
          "| term type | discovered in | version | parent(s) | items tagged on it in later iterations |", "|---|---|---|---|---|"]
    for tid, u in track["candidate_usage"].items():
        usage = ", ".join(f"{k}: {n}" for k, n in u["usage"].items()) or "none yet"
        L.append(f"| `{tid}` | iteration {u['discovered_in_iteration']} | v{u['version']} | {', '.join(u['parents'])} | {usage} |")
    L += ["", "## Nodes by category per version", "", "| version | " + " | ".join(track["categories"]) + " |", "|---|" + "---|" * len(track["categories"])]
    for v in track["versions"]:
        L.append(f"| v{v['version']} | " + " | ".join(str(v["by_category"].get(c, 0)) for c in track["categories"]) + " |")
    return "\n".join(L) + "\n"


def main() -> None:
    versions = [version_row(n) for n in cat.versions()]
    track = {"versions": versions, "iterations": cat.read_log(), "candidate_usage": usage_of_candidates(versions),
             "categories": ["asset", "technology", "actor", "activity", "obligation_or_risk"]}
    (cat.EVOL / "evolution_track.json").write_text(json.dumps(track, indent=1, ensure_ascii=False), encoding="utf-8")
    md = render_md(track)
    (cat.EVOL / "evolution_track.md").write_text(md, encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()
