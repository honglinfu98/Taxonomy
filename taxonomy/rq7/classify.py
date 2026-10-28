"""RQ7 LLM classifiers: site categories from a token description, with and without the ontology.

    python -m taxonomy.rq7.classify text onto tags [--runs 3] [--model claude-haiku-5-5] [--workers 8] [--limit N]

Systems:
  text   the description and the list of categories; no ontology (the "without" condition)
  onto   the same plus the catalogue block (term types, values, is-a edges) in a cached system
         block, with the instruction to first state the catalogue values the description
         instantiates and then choose categories (the ontology as context)
  tags   two stages: the unchanged production tagger (catalogue v6, Haiku) tags the description;
         a second call sees only those tags, rendered with their definitions, and the category
         list, never the description (the ontology as the only evidence)

Writes output/rq7/pred_<system>_run<r>.jsonl (and tags_run<r>.jsonl for the tagger stage) and
output/rq7/classify_<system>.json with per-run metrics and usage.
"""
from __future__ import annotations

import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor

from taxonomy.classification import catalogue as cat
from taxonomy.classification.tag import catalogue_block, extract_json
from taxonomy.evaluation.common import add_usage, call_llm, cost, micro_macro, read_jsonl, write_jsonl
from taxonomy.evaluation.tagging_eval import llm_system
from taxonomy.llm_context import client
from taxonomy.rq7.labels import ITEMS, LABELS, OUT

CATALOGUE_VERSION = 6

TEXT_INSTRUCTIONS = """\
You classify crypto-asset projects into the categories a market-data website uses. You are given \
a project's name and its description as published on the Web, and the closed list of categories. \
Assign every category that applies to the project; most projects have one to three, a few have none. \
Use only names from the list, spelled exactly. Output valid JSON only, no prose, no markdown fences.
"""

ONTO_INSTRUCTIONS = """\
You classify crypto-asset projects into the categories a market-data website uses. You are given \
a project's name and its description as published on the Web, the closed list of categories, and \
a taxonomy catalogue of classification dimensions (term types with values, organised in an is-a \
DAG). Classify in two steps: first, for each term type the description clearly addresses, state the \
value the project instantiates (term type id and value code from the catalogue); second, assign \
every category that the description together with those dimensions supports. Most projects have one \
to three categories, a few have none. Use only category names from the list, spelled exactly. \
Output valid JSON only, no prose, no markdown fences.
"""

TAGS_INSTRUCTIONS = """\
You classify crypto-asset projects into the categories a market-data website uses. You do not see \
the project's description: you see only the classification tags that a taxonomy-based tagger \
assigned to it (term type, value, definition, and the tagger's evidence span), the project's name, \
and the closed list of categories. Assign every category those tags support; if the tags do not \
support any category, return an empty list. Use only names from the list, spelled exactly. Output \
valid JSON only, no prose, no markdown fences.
"""

CATEGORY_BLOCK = "<categories>\n{cats}\n</categories>"
TEXT_PROMPT = """\
Project: {title}
Description: {text}

Return {{"categories": ["<category name>", ...]}}
"""
ONTO_PROMPT = """\
Project: {title}
Description: {text}

Return {{"dimensions": [{{"term_type": "<term type id>", "value": "<value code>"}}], "categories": ["<category name>", ...]}}
"""
TAGS_PROMPT = """\
Project: {title}
Tags assigned by the taxonomy tagger:
{tags}

Return {{"categories": ["<category name>", ...]}}
"""


def render_tags(row: dict, by_id: dict[str, dict]) -> str:
    lines = []
    for t in row["tags"]:
        tt = by_id[t["term_type"]]
        v = next((v for v in tt["values"] if v["value"] == t["value"]), None)
        d = f' ({v["definition"]})' if v and v.get("definition") else ""
        lines.append(f'- {tt["name"]} [{tt["question"]}]: {t["value"]}{d}; confidence {t["confidence"]:.2f}; evidence: "{t["evidence"]}"')
    for a in row.get("implied_term_types", []):
        lines.append(f"- implied by the is-a hierarchy: {by_id[a]['name']}")
    return "\n".join(lines) or "- (no tags)"


def canon(labels: list[str]) -> dict[str, str]:
    return {l.lower().strip(): l for l in labels}


def run_system(system: str, items: list[dict], labels: list[str], r: int, model: str, effort: str, workers: int) -> dict:
    tts, dag, _ = cat.load_version(CATALOGUE_VERSION)
    by_id = {t["id"]: t for t in tts}
    cmap = canon(labels)
    blocks = [CATEGORY_BLOCK.format(cats="\n".join(labels))]
    cl = client()
    usage: dict = {}
    t0 = time.perf_counter()
    tag_info = None
    tag_rows: dict[str, dict] = {}
    if system == "tags":
        p = OUT / f"tags_run{r}.jsonl"
        rows = read_jsonl(p) if p.exists() else []
        if {x["item_id"] for x in rows} != {i["id"] for i in items}:   # stale or partial (e.g. a --limit smoke test): redo
            rows, tag_info = llm_system("dag", items, tts, dag, model, "medium", workers)
            write_jsonl(p, rows)
        tag_rows = {x["item_id"]: x for x in rows}
        instr = TAGS_INSTRUCTIONS
    elif system == "onto":
        instr = ONTO_INSTRUCTIONS
        blocks = [catalogue_block(tts, dag)] + blocks
    else:
        instr = TEXT_INSTRUCTIONS

    def one(item: dict) -> dict:
        if system == "tags":
            prompt = TAGS_PROMPT.format(title=item["title"], tags=render_tags(tag_rows[item["id"]], by_id))
        elif system == "onto":
            prompt = ONTO_PROMPT.format(title=item["title"], text=item["text"])
        else:
            prompt = TEXT_PROMPT.format(title=item["title"], text=item["text"])
        out = {"item_id": item["id"], "title": item["title"], "gold": item["gold"], "pred": [], "unknown": [], "dimensions": []}
        for attempt in range(3):
            try:
                res = call_llm(cl, instr, prompt, model, effort, blocks, max_tokens=1500)
                parsed = extract_json(res["text"])
                break
            except (json.JSONDecodeError, ValueError):
                out["parse_error"] = True
                res, parsed = res if "res" in dir() else {"usage": {}, "seconds": 0}, {}
                break
            except Exception:
                if attempt == 2:
                    raise
                time.sleep(2 * (attempt + 1))
        for c in parsed.get("categories", []) or []:
            k = str(c).lower().strip()
            (out["pred"] if k in cmap else out["unknown"]).append(cmap.get(k, str(c)))
        out["pred"] = sorted(set(out["pred"]))
        if system == "onto":
            out["dimensions"] = [d for d in (parsed.get("dimensions") or []) if isinstance(d, dict) and d.get("term_type") in by_id]
        out["usage"], out["seconds"] = res.get("usage", {}), res.get("seconds", 0)
        return out

    first = one(items[0])
    with ThreadPoolExecutor(workers) as ex:
        rows = [first] + list(ex.map(one, items[1:]))
    for x in rows:
        add_usage(usage, x["usage"])
    write_jsonl(OUT / f"pred_{system}_run{r}.jsonl", rows)
    m = micro_macro({x["item_id"]: set(x["gold"]) for x in rows}, {x["item_id"]: set(x["pred"]) for x in rows})
    m["pred_per_item"] = round(sum(len(x["pred"]) for x in rows) / len(rows), 3)
    m["unknown_names"] = sum(len(x["unknown"]) for x in rows)
    m["parse_errors"] = sum(1 for x in rows if x.get("parse_error"))
    info = {"model": model, "effort": effort, "usage": usage, "cost_usd": round(cost(usage, model), 4), "wall_seconds": round(time.perf_counter() - t0, 1)}
    if tag_info:
        info["tagger"] = tag_info
    return {"run": r, "metrics": m, "run_info": info}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("systems", nargs="+", choices=["text", "onto", "tags"])
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    items = read_jsonl(ITEMS)[: a.limit or None]
    labels = list(json.loads(LABELS.read_text(encoding="utf-8"))["labels"])
    for system in a.systems:
        runs = []
        for r in range(1, a.runs + 1):
            res = run_system(system, items, labels, r, a.model, a.effort, a.workers)
            runs.append(res)
            m, i = res["metrics"], res["run_info"]
            print(f"{system} run {r}: micro-F1 {m['micro_f1']} macro-F1 {m['macro_f1']} P {m['micro_p']} R {m['micro_r']} "
                  f"pred/item {m['pred_per_item']} unknown names {m['unknown_names']} (${i['cost_usd']}, {i['wall_seconds']} s)", flush=True)
        (OUT / f"classify_{system}.json").write_text(json.dumps({"system": system, "items": len(items), "labels": len(labels),
                                                                  "catalogue_version": CATALOGUE_VERSION, "runs": runs}, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
