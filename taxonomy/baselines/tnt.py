"""TnT-LLM baseline (Wan et al. 2024): taxonomy generation from content summaries, bottom-up.

    python -m taxonomy.baselines.tnt [--name tnt] [--batch 30] [--workers 8]

Phase 1  every corpus passage (sections split at ~900 words) is summarised in <= 120 words,
         keeping the defined terms and classification criteria it contains;
Phase 2  the summaries are shuffled (seed 0) and fed in batches: the first batch produces an
         initial taxonomy of term types (question + values), each later batch updates it
         (add, merge, split, rename; the full taxonomy is returned each time);
Phase 3  one review call enforces the rules (one question per term type, no duplicates, 2-12 values).
TnT-LLM names and describes labels; it does not cite, so every citation list is empty and
faithfulness cannot be scored. The term types are compared by agreement, expert coverage,
structure (Task B) and downstream tagging like every other catalogue.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from concurrent.futures import ThreadPoolExecutor

from taxonomy.baselines.common import OUT, Meter, clean_term_types, extract_json, llm, passages, save_catalogue
from taxonomy.llm_context import client

SUMMARY_INSTRUCTIONS = """\
You summarise one passage of a crypto-asset or DLT legal or technical document. In at most 120 \
words, state which things the passage defines or classifies and along which criteria (the \
questions it asks and the categories it distinguishes). Plain prose, no preamble.
"""

TAXONOMY_INSTRUCTIONS = """\
You build a taxonomy of classification dimensions for crypto-asset and distributed-ledger (DLT) \
content, from summaries of a document corpus. A TERM TYPE is a classification dimension: a \
question along which definitions and classification criteria discriminate between things \
(e.g. "reference asset", "consensus mechanism", "custody arrangement"); it has VALUES, the \
categories a thing can take on that dimension. One question per term type; never merge two \
questions into one term type; never duplicate a question under two names. Each term type \
applies to one of: asset, technology, actor, activity, obligation_or_risk. Output valid JSON \
only, no prose, no markdown fences.
"""

SCHEMA = """\
{"term_types": [{"id": "snake_case", "name": "...", "applies_to": "asset | technology | actor | activity | obligation_or_risk",
  "question": "the one question this dimension answers", "description": "1-2 sentences", "aliases": ["..."],
  "values": [{"value": "short label", "definition": "at most 25 words"}]}]}"""

INIT_PROMPT = """\
Summaries of corpus passages (batch 1):
{batch}

Generate the initial taxonomy: every classification dimension these summaries use or imply, \
with its values. Aim for completeness (several dozen term types are expected over the whole \
corpus). Return exactly this schema:
{schema}
"""

UPDATE_PROMPT = """\
Current taxonomy:
{taxonomy}

Summaries of further corpus passages (batch {k}):
{batch}

Update the taxonomy so it also covers these summaries: add missing term types and values, \
merge term types that ask the same question, split a term type that mixes two questions, and \
refine names, questions and definitions. Keep everything still supported. Return the FULL \
updated taxonomy in exactly this schema:
{schema}
"""

REVIEW_PROMPT = """\
Taxonomy:
{taxonomy}

Review it as a whole: one question per term type, no two term types asking the same question, \
each term type in the right category, 2-12 values per term type, every value a category of \
that question (not an example or a synonym of another value). Return the FULL corrected \
taxonomy in exactly this schema:
{schema}
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--effort", default="high")
    ap.add_argument("--name", default="tnt")
    ap.add_argument("--batch", type=int, default=30)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--max-words", type=int, default=900)
    a = ap.parse_args()
    d = OUT / a.name
    d.mkdir(parents=True, exist_ok=True)
    cl, meter = client(), Meter(a.model)

    leaves = passages(a.max_words)
    sp = d / "summaries.json"
    if sp.exists():
        summaries = json.loads(sp.read_text(encoding="utf-8"))
    else:
        def one(p: dict) -> dict:
            r = llm(cl, SUMMARY_INSTRUCTIONS, f"Document {p['doc']} ({p['title'][:80]}), section \"{p['section']}\":\n\n{p['text']}",
                    a.model, "medium", 600, meter=meter)
            return {"id": p["id"], "doc": p["doc"], "section": p["section"], "summary": r["text"].strip()}
        with ThreadPoolExecutor(a.workers) as ex:
            summaries = list(ex.map(one, leaves))
        sp.write_text(json.dumps(summaries, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{a.name}: {len(summaries)} summaries", file=sys.stderr)

    order = list(range(len(summaries)))
    random.Random(0).shuffle(order)
    batches = [[summaries[i] for i in order[j:j + a.batch]] for j in range(0, len(order), a.batch)]
    taxonomy: list[dict] = []
    trace = []
    for k, b in enumerate(batches, 1):
        batch = "\n".join(f"- [{s['id']}, doc {s['doc']}] {s['summary']}" for s in b)
        if k == 1:
            prompt = INIT_PROMPT.format(batch=batch, schema=SCHEMA)
        else:
            prompt = UPDATE_PROMPT.format(taxonomy=json.dumps({"term_types": taxonomy}, ensure_ascii=False), k=k, batch=batch, schema=SCHEMA)
        r = llm(cl, TAXONOMY_INSTRUCTIONS, prompt, a.model, a.effort, 60000, meter=meter)
        try:
            taxonomy = clean_term_types(extract_json(r["text"]).get("term_types", []))
        except (ValueError, json.JSONDecodeError, AttributeError) as e:
            print(f"  batch {k}: unparseable ({e}); taxonomy kept", file=sys.stderr)
        trace.append({"batch": k, "summaries": len(b), "term_types": len(taxonomy), "values": sum(len(t["values"]) for t in taxonomy),
                      "stop_reason": r["stop_reason"]})
        print(f"  batch {k}/{len(batches)}: {len(taxonomy)} term types", file=sys.stderr)
    r = llm(cl, TAXONOMY_INSTRUCTIONS, REVIEW_PROMPT.format(taxonomy=json.dumps({"term_types": taxonomy}, ensure_ascii=False), schema=SCHEMA),
            a.model, a.effort, 60000, meter=meter)
    try:
        taxonomy = clean_term_types(extract_json(r["text"]).get("term_types", []))
    except (ValueError, json.JSONDecodeError, AttributeError) as e:
        print(f"  review: unparseable ({e}); taxonomy kept", file=sys.stderr)
    trace.append({"batch": "review", "term_types": len(taxonomy), "values": sum(len(t["values"]) for t in taxonomy), "stop_reason": r["stop_reason"]})
    for t in taxonomy:
        t["citations"] = []
        for v in t["values"]:
            v["citations"] = []
    (d / "trace.json").write_text(json.dumps(trace, indent=1), encoding="utf-8")
    save_catalogue(a.name, taxonomy, {"task": "A-tnt", "effort": a.effort, "batch": a.batch, "summaries": len(summaries),
                                      "batches": len(batches), **meter.report()})


if __name__ == "__main__":
    main()
