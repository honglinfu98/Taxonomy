"""Part 2, Task C: tag DLT-Corpus items with (term type, value) nodes of the Part 1 taxonomy.

    python -m taxonomy.classification.tag [--version N] [--iter K] [--sample path] [--limit N] [--workers 6]

Uses catalogue version N (default: latest in output/evolution/) and writes to
output/evolution/iter_K/ (default: next iteration). The sample defaults to
data/dlt_corpus/sample_iter{K}.jsonl, falling back to sample.jsonl.

Context per request = TAGGER_INSTRUCTIONS + one cached catalogue block (every term type with
its question, value codes and definitions, and its is-a parents from the DAG). The corpus is
not sent: tagging needs the catalogue only, so a request is ~15K cached tokens plus the item.

Per item the model returns tags (term type, value code, confidence, evidence span) and
optional "novel" proposals (values or term types the catalogue lacks: the discovery signal
for Part 3). The runner validates term-type ids and value codes against the catalogue
(accepting exact labels and close fuzzy matches), checks that each evidence span occurs in
the item, and adds the is-a ancestors implied by each tagged term type.

Outputs (output/evolution/iter_K/):
  tags.jsonl            one line per item: validated tags, implied ancestors, novel proposals
  tags_summary.json     tag counts per (term type, value), coverage per term type, API cost
                        and time (per-request latency mean/p50/p95, wall time)
  novel_proposals.json  all novel proposals grouped by target term type
  tags.md               readable summary
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import time
from pathlib import Path
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

from taxonomy.classification import catalogue as cat
from taxonomy.classification.prompts import TAGGER_INSTRUCTIONS, TAG_PROMPT
from taxonomy.classification.sample import SAMPLE, sample_path
from taxonomy.establishment.term_types import quote_found
from taxonomy.llm_context import ROOT, build_request, client

CATEGORIES = ["asset", "technology", "actor", "activity", "obligation_or_risk"]

# Haiku 5.5 list price, prompts <= 100K tokens (USD per token)
PRICE = {"input": 0.10e-6, "output": 0.50e-6, "cache_read": 0.01e-6, "cache_write": 0.125e-6}


def load_taxonomy(version: int | None = None) -> tuple[list[dict], dict]:
    tts, dag, _ = cat.load_version(cat.latest_version() if version is None else version)
    return tts, dag


def latency_stats(lat: list[float], wall: float, workers: int) -> dict:
    if not lat:
        return {}
    s = sorted(lat)
    return {"requests": len(s), "api_seconds": round(sum(s), 1), "mean_request_s": round(sum(s) / len(s), 2),
            "p50_request_s": round(s[len(s) // 2], 2), "p95_request_s": round(s[int(0.95 * (len(s) - 1))], 2),
            "max_request_s": round(s[-1], 2), "wall_seconds": round(wall, 1), "workers": workers}


def catalogue_block(tts: list[dict], dag: dict) -> str:
    """The cached system block: every term type with value codes and its is-a parents."""
    parents: dict[str, list[str]] = defaultdict(list)
    for e in dag["edges"]:
        parents[e["child"]].append(f'{e["parent"]} ({e["probability"]:.2f})')
    lines = ['<taxonomy_catalogue source="Part 1 taxonomy establishment">',
             "Term types grouped by category. Each line: id | question | refines: is-a parents with weight.",
             "Values are listed as code: label (definition). Tag with the term type id and the value code.", ""]
    for cat in CATEGORIES:
        lines.append(f"## {cat}")
        for t in tts:
            if t["applies_to"] != cat:
                continue
            ref = "; ".join(parents.get(t["id"], [])) or "none (root)"
            lines.append(f'- {t["id"]} | {t["question"]} | refines: {ref}')
            for i, v in enumerate(t["values"], 1):
                lines.append(f'    v{i}: {v["value"]} ({v["definition"]})')
        lines.append("")
    lines.append("</taxonomy_catalogue>")
    return "\n".join(lines)


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def resolve_value(t: dict, raw: str) -> tuple[str | None, str]:
    """Map the model's value field to a catalogue value label. Returns (label, how)."""
    raw = str(raw).strip()
    m = re.fullmatch(r"v?(\d{1,2})", raw.lower())
    if m and 1 <= int(m.group(1)) <= len(t["values"]):
        return t["values"][int(m.group(1)) - 1]["value"], "code"
    labels = [v["value"] for v in t["values"]]
    for lab in labels:
        if norm(lab) == norm(raw):
            return lab, "label"
    best = difflib.get_close_matches(norm(raw), [norm(lab) for lab in labels], n=1, cutoff=0.85)
    if best:
        return labels[[norm(lab) for lab in labels].index(best[0])], "fuzzy"
    return None, "unknown"


def ancestors(tt_id: str, parent_of: dict[str, list[str]]) -> list[str]:
    seen, stack = [], list(parent_of.get(tt_id, []))
    while stack:
        n = stack.pop()
        if n not in seen:
            seen.append(n)
            stack.extend(parent_of.get(n, []))
    return seen


def extract_json(text: str) -> dict:
    text = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", text.strip())
    return json.loads(text[text.find("{"):text.rfind("}") + 1])


def validate(item: dict, raw: dict, by_id: dict[str, dict], parent_of: dict[str, list[str]]) -> dict:
    tags, rejected = [], []
    seen = set()
    for g in raw.get("tags", []) or []:
        tt = by_id.get(str(g.get("term_type", "")).strip())
        if tt is None:
            rejected.append({"reason": "unknown term type", **g})
            continue
        label, how = resolve_value(tt, g.get("value", ""))
        if label is None:
            rejected.append({"reason": "unknown value", **g})
            continue
        if (tt["id"], label) in seen:
            continue
        seen.add((tt["id"], label))
        ev = str(g.get("evidence", "") or "")
        tags.append({"term_type": tt["id"], "category": tt["applies_to"], "value": label,
                     "confidence": max(0.0, min(1.0, float(g.get("confidence", 0) or 0))),
                     "evidence": ev, "evidence_found": bool(ev) and quote_found(ev, item["title"] + " " + item["text"]),
                     "value_match": how})
    tagged = {t["term_type"] for t in tags}
    implied = sorted({a for t in tagged for a in ancestors(t, parent_of)} - tagged)
    novel = []
    for n in raw.get("novel", []) or []:
        ev = str(n.get("evidence", "") or "")
        novel.append({"kind": n.get("kind"), "term_type": n.get("term_type"), "proposal": n.get("proposal"),
                      "definition": n.get("definition", ""), "evidence": ev,
                      "evidence_found": bool(ev) and quote_found(ev, item["title"] + " " + item["text"])})
    return {"item_id": item["id"], "source": item["source"], "title": item["title"], "off_topic": bool(raw.get("off_topic")),
            "tags": sorted(tags, key=lambda t: -t["confidence"]), "implied_term_types": implied,
            "novel": novel, "rejected": rejected}


def ask(cl, catalogue: str, item: dict, model: str, effort: str) -> dict:
    prompt = TAG_PROMPT.format(item_id=item["id"], source=item["source"], year=f", {item['year']}" if item.get("year") else "",
                               title=item["title"], text=item["text"])
    req = build_request(TAGGER_INSTRUCTIONS, prompt, model=model, max_tokens=3000, effort=effort,
                        extra_system=[catalogue], corpus=False, thinking={"type": "disabled"})
    t0 = time.perf_counter()
    msg = cl.messages.create(**req)
    u = msg.usage
    return {"text": "".join(b.text for b in msg.content if b.type == "text"), "stop_reason": msg.stop_reason,
            "seconds": round(time.perf_counter() - t0, 3),
            "usage": {"input": u.input_tokens, "output": u.output_tokens,
                      "cache_write": u.cache_creation_input_tokens or 0, "cache_read": u.cache_read_input_tokens or 0}}


def summarise(results: list[dict], tts: list[dict], usage: dict, meta: dict) -> dict:
    by_id = {t["id"]: t for t in tts}
    pair_counts = Counter((t["term_type"], t["value"]) for r in results for t in r["tags"])
    tt_items = Counter(tt for r in results for tt in {t["term_type"] for t in r["tags"]})
    cat_items = Counter(c for r in results for c in {t["category"] for t in r["tags"]})
    n = len(results)
    cost = sum(usage[k] * PRICE[k] for k in PRICE)
    return {
        "run": {**meta, "usage": usage, "cost_usd": round(cost, 4), "cost_per_item_usd": round(cost / n, 5) if n else None},
        "items": n, "off_topic": sum(r["off_topic"] for r in results),
        "tags_total": sum(len(r["tags"]) for r in results),
        "tags_per_item": round(sum(len(r["tags"]) for r in results) / n, 2) if n else None,
        "evidence_verified": sum(t["evidence_found"] for r in results for t in r["tags"]),
        "value_match": dict(Counter(t["value_match"] for r in results for t in r["tags"])),
        "rejected_tags": sum(len(r["rejected"]) for r in results),
        "novel_proposals": sum(len(r["novel"]) for r in results),
        "term_types_used": len(tt_items), "term_types_total": len(tts),
        "coverage_by_category": {c: cat_items.get(c, 0) for c in CATEGORIES},
        "term_type_item_counts": {k: v for k, v in tt_items.most_common()},
        "pair_counts": [{"term_type": k[0], "name": by_id[k[0]]["name"], "value": k[1], "items": v} for k, v in pair_counts.most_common()],
        "by_source": {s: {"items": sum(1 for r in results if r["source"] == s),
                          "tags_per_item": round(sum(len(r["tags"]) for r in results if r["source"] == s) /
                                                 max(1, sum(1 for r in results if r["source"] == s)), 2)}
                      for s in sorted({r["source"] for r in results})},
    }


def render_md(summary: dict, results: list[dict], tts: list[dict]) -> str:
    by_id = {t["id"]: t for t in tts}
    s = summary
    sources = ", ".join(f"{k}: {v['items']}" for k, v in s["by_source"].items())
    lines = ["# Part 2, Task C: tagging the DLT-Corpus sample", "",
             f"{s['items']} items ({sources}), "
             f"{s['tags_total']} tags ({s['tags_per_item']} per item), {s['off_topic']} off-topic, "
             f"{s['evidence_verified']}/{s['tags_total']} evidence spans verified, {s['rejected_tags']} tags rejected, "
             f"{s['novel_proposals']} novel proposals. {s['term_types_used']}/{s['term_types_total']} term types used. "
             f"Cost ${s['run']['cost_usd']} (${s['run']['cost_per_item_usd']} per item).", "",
             "## Items tagged per category", ""]
    lines += [f"- {c}: {v}" for c, v in s["coverage_by_category"].items()]
    lines += ["", "## Most frequent (term type, value) tags", "", "| term type | value | items |", "|---|---|---|"]
    lines += [f"| {p['name']} | {p['value']} | {p['items']} |" for p in s["pair_counts"][:40]]
    unused = [t for t in tts if t["id"] not in s["term_type_item_counts"]]
    lines += ["", f"## Term types never used ({len(unused)})", ""]
    lines += [f"- {t['name']} `{t['id']}` ({t['applies_to']})" for t in unused]
    lines += ["", "## Examples", ""]
    for r in results[:6]:
        lines.append(f"**{r['title'][:90]}** ({r['source']})")
        for t in r["tags"][:6]:
            lines.append(f"- {by_id[t['term_type']]['name']} = {t['value']} ({t['confidence']:.2f}) — \"{t['evidence'][:80]}\"")
        if r["novel"]:
            lines += [f"- novel: {n['kind']} {n['proposal']!r} for {n['term_type']}" for n in r["novel"]]
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--effort", default="medium", choices=["low", "medium", "high"])
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0, help="tag only the first N sample items")
    ap.add_argument("--version", type=int, default=None, help="catalogue version (default: latest)")
    ap.add_argument("--iter", type=int, default=None, help="iteration number (default: next)")
    ap.add_argument("--sample", default=None, help="sample file (default: data/dlt_corpus/sample_iter{K}.jsonl)")
    args = ap.parse_args()
    version = cat.latest_version() if args.version is None else args.version
    k = args.iter if args.iter is not None else (cat.iterations()[-1] + 1 if cat.iterations() else 1)
    out_dir = cat.iter_dir(k)
    out_dir.mkdir(parents=True, exist_ok=True)
    sample_file = Path(args.sample) if args.sample else (sample_path(k) if sample_path(k).exists() else SAMPLE)
    if not sample_file.exists():
        sys.exit(f"{sample_file} missing: run python -m taxonomy.classification.sample --iter {k} first")
    items = [json.loads(l) for l in sample_file.read_text(encoding="utf-8").splitlines() if l.strip()]
    items = items[: args.limit or None]
    tts, dag = load_taxonomy(version)
    print(f"iteration {k}: catalogue v{version} ({len(tts)} term types), {len(items)} items from {sample_file.name} -> {out_dir}",
          file=sys.stderr)
    by_id = {t["id"]: t for t in tts}
    parent_of: dict[str, list[str]] = defaultdict(list)
    for e in dag["edges"]:
        parent_of[e["child"]].append(e["parent"])
    catalogue = catalogue_block(tts, dag)
    cl = client()
    t0 = time.time()

    first = ask(cl, catalogue, items[0], args.model, args.effort)      # warm the cache before fanning out
    print(f"warm-up: cache_write={first['usage']['cache_write']} cache_read={first['usage']['cache_read']} "
          f"input={first['usage']['input']} ({time.time() - t0:.0f}s)", file=sys.stderr)
    raw = {items[0]["id"]: first}
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(ask, cl, catalogue, it, args.model, args.effort): it["id"] for it in items[1:]}
        for i, f in enumerate(as_completed(futs), 2):
            raw[futs[f]] = f.result()
            if i % 25 == 0 or i == len(items):
                print(f"  {i}/{len(items)}", file=sys.stderr)

    usage = {key: 0 for key in PRICE}
    results, unparsed, latencies = [], 0, []
    for it in items:
        r = raw[it["id"]]
        latencies.append(r["seconds"])
        for key in usage:
            usage[key] += r["usage"][key]
        try:
            parsed = extract_json(r["text"])
        except (json.JSONDecodeError, ValueError):
            parsed, unparsed = {"tags": [], "novel": [], "off_topic": False}, unparsed + 1
        results.append(validate(it, parsed, by_id, parent_of))
    meta = {"task": "C", "iteration": k, "catalogue_version": version, "sample": str(sample_file.relative_to(ROOT)),
            "model": args.model, "effort": args.effort, "items": len(items), "unparsed": unparsed,
            "seconds": round(time.time() - t0, 1), "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "catalogue_chars": len(catalogue), "time": latency_stats(latencies, time.time() - t0, args.workers)}
    summary = summarise(results, tts, usage, meta)
    TAGS_OUT, SUMMARY_OUT, NOVEL_OUT, MD_OUT = (out_dir / n for n in ("tags.jsonl", "tags_summary.json", "novel_proposals.json", "tags.md"))

    with TAGS_OUT.open("w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    SUMMARY_OUT.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    novel: dict[str, list] = defaultdict(list)
    for r in results:
        for n in r["novel"]:
            novel[str(n.get("term_type") or "NEW_TERM_TYPE")].append({"item_id": r["item_id"], **n})
    NOVEL_OUT.write_text(json.dumps(novel, indent=2, ensure_ascii=False), encoding="utf-8")
    MD_OUT.write_text(render_md(summary, results, tts), encoding="utf-8")

    s = summary
    print(f"\n{s['items']} items, {s['tags_total']} tags ({s['tags_per_item']}/item), evidence verified "
          f"{s['evidence_verified']}/{s['tags_total']}, rejected {s['rejected_tags']}, novel {s['novel_proposals']}, "
          f"off-topic {s['off_topic']}, unparsed {unparsed}; term types used {s['term_types_used']}/{s['term_types_total']}")
    t = meta["time"]
    print(f"usage {usage}; cost ${s['run']['cost_usd']} (${s['run']['cost_per_item_usd']}/item); "
          f"API time {t.get('api_seconds')}s over {t.get('requests')} requests (mean {t.get('mean_request_s')}s, p95 {t.get('p95_request_s')}s), "
          f"wall {meta['seconds']}s with {args.workers} workers")
    print(f"-> {TAGS_OUT}\n-> {SUMMARY_OUT}\n-> {NOVEL_OUT}\n-> {MD_OUT}")


if __name__ == "__main__":
    main()
