"""Task B runner: is-a hierarchy over the Task A term types.

    python -m taxonomy.is_a [--workers 4] [--k 6] [--only asset,actor] [--limit N]

For every term type X in output/term_types.json, asks the model (same cached corpus, plus the
Task A catalogue as a second cached system block) for a probability distribution over
"X is-a Y" with Y ranging over the other term types in X's category, plus "none".
Writes output/is_a.json (all distributions, verified citations), output/is_a_edges.csv
(child, parent, probability) and output/is_a.md (per-category hierarchy by argmax parent).
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

from taxonomy.llm_context import ROOT, build_request, client, load_corpus
from taxonomy.prompts import TASK_B_CATALOGUE_HEADER, TASKS
from taxonomy.term_types import JSON_OUT as TERM_TYPES_JSON, parse_corpus, quote_found

OUT_DIR = ROOT / "output"
JSON_OUT = OUT_DIR / "is_a.json"
EDGES_OUT = OUT_DIR / "is_a_edges.csv"
MD_OUT = OUT_DIR / "is_a.md"
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


def normalise(dist: list[dict], allowed: set[str]) -> tuple[list[dict], list[str]]:
    """Drop unknown parents, clamp negatives, merge duplicates, renormalise to sum 1."""
    merged: dict[str, dict] = {}
    dropped = []
    for e in dist:
        pid = str(e.get("parent", "")).strip()
        if pid not in allowed:
            dropped.append(pid)
            continue
        p = max(float(e.get("probability", 0) or 0), 0.0)
        if pid in merged:
            merged[pid]["probability"] += p
        else:
            merged[pid] = {"parent": pid, "probability": p, "rationale": e.get("rationale", ""),
                           "citations": e.get("citations", []) or []}
    if "none" not in merged:
        merged["none"] = {"parent": "none", "probability": 0.0, "rationale": "", "citations": []}
    total = sum(e["probability"] for e in merged.values())
    for e in merged.values():
        e["probability"] = round(e["probability"] / total, 4) if total > 0 else round(1 / len(merged), 4)
    return sorted(merged.values(), key=lambda e: -e["probability"]), dropped


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


def render_md(results: list[dict], by_id: dict[str, dict]) -> str:
    lines = ["# Task B output: is-a hierarchy of term types", "",
             "For each term type X (child), the most probable parent Y with P(X is-a Y); `none` means "
             "X is top-level in its category. Full distributions are in `output/is_a.json`.", ""]
    for cat in CATEGORIES:
        rows = [r for r in results if r["category"] == cat]
        if not rows:
            continue
        lines += [f"## {cat}", ""]
        parent_of = {r["child"]: r["distribution"][0]["parent"] for r in rows}
        children: dict[str, list[str]] = {}
        for c, p in parent_of.items():
            children.setdefault(p, []).append(c)
        probs = {r["child"]: r["distribution"][0]["probability"] for r in rows}

        def walk(node: str, depth: int, seen: set[str]) -> None:
            for c in sorted(children.get(node, []), key=lambda x: -probs[x]):
                if c in seen:          # cycle guard
                    lines.append("  " * depth + f"- {by_id[c]['name']} `{c}` (cycle)")
                    continue
                tag = "" if node == "none" else f"  (p={probs[c]})"
                lines.append("  " * depth + f"- {by_id[c]['name']} `{c}`{tag}")
                walk(c, depth + 1, seen | {c})

        walk("none", 0, set())
        # nodes unreachable from the roots (members of cycles)
        reachable = set()
        stack = list(children.get("none", []))
        while stack:
            n = stack.pop()
            if n not in reachable:
                reachable.add(n)
                stack.extend(children.get(n, []))
        for r in rows:
            if r["child"] not in reachable:
                lines.append(f"- {by_id[r['child']]['name']} `{r['child']}` is-a `{parent_of[r['child']]}` "
                             f"(p={probs[r['child']]}) — in a cycle, no root")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--effort", default="high", choices=["low", "medium", "high"])
    ap.add_argument("--k", type=int, default=6, help="max entries in each distribution, incl. none")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--only", default="", help="comma-separated categories to run")
    ap.add_argument("--limit", type=int, default=0, help="run only the first N children (smoke test)")
    args = ap.parse_args()
    OUT_DIR.mkdir(exist_ok=True)

    tts = load_term_types()
    by_id = {t["id"]: t for t in tts}
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
            dist, dropped = normalise(extract_json(r["text"]).get("distribution", []), allowed)
        except (json.JSONDecodeError, ValueError) as e:
            dist, dropped = normalise([], allowed), [f"unparseable: {e}"]
        n, ok = verify_citations(dist, docs)
        n_cit[0] += n
        n_cit[1] += ok
        results.append({"child": t["id"], "name": t["name"], "category": t["applies_to"], "distribution": dist,
                        "dropped_parents": dropped, "stop_reason": r["stop_reason"]})

    meta = {"task": "B", "model": args.model, "effort": args.effort, "k": args.k, "children": len(children),
            "seconds": round(time.time() - t0, 1), "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "usage": usage, "citations": n_cit[0], "citations_verified": n_cit[1]}
    JSON_OUT.write_text(json.dumps({"run": meta, "is_a": results}, indent=2, ensure_ascii=False), encoding="utf-8")
    with EDGES_OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["child", "parent", "probability", "category"])
        for r in results:
            for e in r["distribution"]:
                w.writerow([r["child"], e["parent"], e["probability"], r["category"]])
    MD_OUT.write_text(render_md(results, by_id), encoding="utf-8")

    for r in results:
        top = r["distribution"][0]
        print(f"{r['child'][:38]:38} is-a {top['parent'][:38]:38} p={top['probability']:.2f}"
              + (f"  dropped={r['dropped_parents']}" if r["dropped_parents"] else ""))
    roots = sum(1 for r in results if r["distribution"][0]["parent"] == "none")
    print(f"\n{len(results)} children, {roots} top-level; citations {n_cit[1]}/{n_cit[0]} verified; "
          f"usage {usage}; {meta['seconds']}s\n-> {JSON_OUT}\n-> {EDGES_OUT}\n-> {MD_OUT}")


if __name__ == "__main__":
    main()
