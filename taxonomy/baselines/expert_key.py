"""Expert key: the classification dimensions proposed by the two published taxonomies in the
corpus (doc 1, Tasca & Tessone; doc 2, Zhang, Ibanez & Xu), extracted with verified quotes.

    python -m taxonomy.baselines.expert_key [--model claude-haiku-5-5]

Each paper is shown alone, in full, and the model lists the dimensions THE PAPER ITSELF proposes
as part of its taxonomy (not those it reviews from prior work), each with its question, its
values and one verbatim quote; quotes are verified against the section with the Task A
verifier and dimensions whose quote fails are dropped. Writes output/baselines/expert_key/.

Caveat, stated wherever the key is used: both papers are inside the corpus every corpus-based
catalogue was generated from, so coverage of this key is contaminated for those catalogues (it
measures recall of dimensions the corpus contains, not independent expert agreement). It is
uncontaminated only for the zero-shot baseline. An independent key needs held-out taxonomies
or expert annotation.
"""
from __future__ import annotations

import argparse
import json
import re

from taxonomy.baselines.common import OUT, Meter, clean_term_types, doc_meta, extract_json, llm, save_catalogue
from taxonomy.establishment.term_types import parse_corpus, quote_found
from taxonomy.llm_context import client, load_corpus

KEY_DOCS = [1, 2]

KEY_INSTRUCTIONS = """\
You extract the classification dimensions that a published taxonomy paper proposes. You are \
given one paper. List only the dimensions (components, layers, criteria, attributes) that the \
paper's OWN taxonomy uses to classify its objects, not dimensions it merely reviews from other \
work. A dimension is a question with a closed set of values (categories). Keep the paper's own \
names and value labels. Every dimension carries one verbatim quote (at most 30 words) from the \
paper that introduces or defines it. Output valid JSON only, no prose, no markdown fences.
"""

KEY_PROMPT = """\
The paper is in the system context as <document index="{doc}"> with sections <section label="...">.

Return {{"term_types": [{{"id": "snake_case", "name": "the paper's name for the dimension",
  "applies_to": "asset | technology | actor | activity | obligation_or_risk",
  "question": "the question the dimension answers", "description": "1 sentence",
  "aliases": [], "values": [{{"value": "the paper's label", "definition": "at most 20 words", "citations": []}}],
  "citations": [{{"doc": {doc}, "section": "exact section label", "quote": "verbatim, at most 30 words"}}]}}]}}

Section labels in this document (copy exactly): {labels}
Be exhaustive: include every dimension of the paper's taxonomy, including sub-dimensions it \
treats as separate classification axes.
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--effort", default="high")
    a = ap.parse_args()
    docs = parse_corpus(load_corpus())
    meta = doc_meta()
    cl, meter = client(), Meter(a.model)
    tts, dropped, per_doc = [], [], {}
    full = {d: re.sub(r"[^a-z0-9]+", "", " ".join(docs[d].values()).lower()) for d in KEY_DOCS}
    for d in KEY_DOCS:
        block = f'<document index="{d}" title="{meta[d].get("title", "")}">\n' + "\n".join(
            f'<section label="{lab}">\n{txt}\n</section>' for lab, txt in docs[d].items()) + "\n</document>"
        labels = " | ".join(f'"{lab}"' for lab in docs[d])
        r = llm(cl, KEY_INSTRUCTIONS, KEY_PROMPT.format(doc=d, labels=labels), a.model, a.effort, 30000, extra_system=[block], meter=meter)
        (OUT / "expert_key").mkdir(parents=True, exist_ok=True)
        (OUT / "expert_key" / f"raw_doc{d}.txt").write_text(r["text"], encoding="utf-8")
        found = clean_term_types(extract_json(r["text"]).get("term_types", []))
        kept = []
        for t in found:
            t["id"] = f"d{d}_{t['id']}"[:70]
            t["source_doc"] = d
            t["quote_verified"] = any(c.get("doc") == d and any(quote_found(c.get("quote", ""), txt) for txt in docs[d].values()) for c in t["citations"])
            t["name_verified"] = re.sub(r"[^a-z0-9]+", "", t["name"].lower()) in full[d]
            (kept if t["quote_verified"] or t["name_verified"] else dropped).append(t)
        per_doc[d] = {"title": meta[d].get("title", ""), "extracted": len(found), "kept": len(kept),
                      "quote_verified": sum(t["quote_verified"] for t in kept), "name_only": sum(not t["quote_verified"] for t in kept)}
        tts += kept
        print(f"doc {d}: {len(found)} dimensions extracted, {len(kept)} with a verified quote", flush=True)
    save_catalogue("expert_key", tts, {"task": "expert-key", "docs": KEY_DOCS, "per_doc": per_doc, "dropped_unverified": [t["id"] for t in dropped],
                                       "effort": a.effort, **meter.report()})


if __name__ == "__main__":
    main()
