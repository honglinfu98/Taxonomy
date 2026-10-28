"""Zero-shot baseline: Task A from the model's parametric knowledge, with no corpus.

    python -m taxonomy.baselines.zeroshot [--model claude-haiku-5-5] [--effort high] [--name zeroshot]

The model sees the same task, schema and definitions as Task A and the titles of the 24 corpus
documents (so it knows which laws and frameworks the corpus covers), but none of their text.
Citations are impossible, so the schema asks for empty citation lists; faithfulness cannot be
scored and the catalogue is compared on agreement, expert coverage, structure and downstream use.
"""
from __future__ import annotations

import argparse

from taxonomy.baselines.common import OUT, Meter, clean_term_types, doc_meta, extract_json, llm, save_catalogue
from taxonomy.establishment.prompts import TASK_A_PROMPT
from taxonomy.llm_context import client

ZEROSHOT_INSTRUCTIONS = """\
You are an expert taxonomist of crypto-asset and distributed-ledger (DLT) terminology, \
working across law, financial regulation and computer science.

You are NOT given any documents. Answer from your own knowledge of the laws, regulatory \
frameworks and technical literature on crypto-assets and DLT. The target corpus (not shown) \
consists of the documents listed in the user message; cover the classification dimensions \
such documents define or rely on.

Definitions used in this work:
- A TERM is a word or phrase such documents define or classify, e.g. "crypto-asset", \
"stablecoin", "VASP", "permissioned ledger".
- A TERM TYPE is a classification dimension: a question along which definitions and \
classification criteria discriminate between things, e.g. "issuer type", "reference asset", \
"legal status", "consensus mechanism", "custody arrangement". A term type is not a term. \
Each term type has VALUES: the categories a thing can take on that dimension.

Rules:
1. No citations are available: every "citations" list must be empty ([]).
2. One dimension per term type. Do not merge two distinct questions into one term type, \
and do not split one question into two because two sources name it differently; list other \
names in "aliases".
3. Where jurisdictions or sources disagree on the values or thresholds of a dimension, \
keep the dimension once and record the disagreement in "notes".
4. Prefer dimensions that recur across sources or that a source relies on to draw a \
legal, prudential or technical boundary, but give coverage priority.
5. Output valid JSON only: no prose before or after it, no markdown code fences, no comments.
"""


def prompt() -> str:
    meta = doc_meta()
    titles = "\n".join(f"doc {i}: [{m.get('type', '')}{', ' + m['jurisdiction'] if m.get('jurisdiction') else ''}"
                       f"{', ' + m['year'] if m.get('year') else ''}] {m.get('title', '')}" for i, m in meta.items())
    p = TASK_A_PROMPT.replace("Read the whole corpus. ", "No corpus is provided: work from your own knowledge. ")
    p = p.replace("Return a single JSON object", "Leave every \"citations\" list empty. Return a single JSON object")
    return p + "\nThe (unseen) corpus consists of these documents; cover the dimensions they would define or use:\n" + titles


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--effort", default="high")
    ap.add_argument("--max-tokens", type=int, default=120000)
    ap.add_argument("--name", default="zeroshot")
    ap.add_argument("--reparse", action="store_true", help="re-read raw.txt instead of calling the API")
    a = ap.parse_args()
    meter = Meter(a.model)
    if a.reparse:
        import json as _json
        old = _json.loads((OUT / a.name / "term_types.json").read_text(encoding="utf-8"))["run"]
        r = {"text": (OUT / a.name / "raw.txt").read_text(encoding="utf-8"), "stop_reason": old["stop_reason"], "usage": old["usage"], "seconds": old["api_seconds"]}
        meter.add(r)
    else:
        r = llm(client(), ZEROSHOT_INSTRUCTIONS, prompt(), a.model, a.effort, a.max_tokens, meter=meter)
    (OUT / a.name).mkdir(parents=True, exist_ok=True)
    (OUT / a.name / "raw.txt").write_text(r["text"], encoding="utf-8")
    parsed = extract_json(r["text"])
    tts = clean_term_types(parsed.get("term_types", []))
    for t in tts:                                   # citations are impossible by construction
        t["citations"] = []
        for v in t["values"]:
            v["citations"] = []
    save_catalogue(a.name, tts, {"task": "A-zeroshot", "effort": a.effort, "stop_reason": r["stop_reason"], **meter.report()},
                   {"coverage_notes": parsed.get("coverage_notes", "") if isinstance(parsed, dict) else "",
                    "truncated": bool(isinstance(parsed, dict) and parsed.get("truncated"))})


if __name__ == "__main__":
    main()
