"""Prompts for Part 2 (classification). The catalogue of term types and values is a cached
system block (built by tag.catalogue_block); the per-item text is the user prompt."""

TAGGER_INSTRUCTIONS = """\
You are a classifier for texts about distributed-ledger technology (DLT) and crypto-assets. \
You tag each text with nodes of a fixed taxonomy.

The taxonomy is a set of TERM TYPES (classification dimensions, each phrased as a question) \
organised in an is-a DAG, each with a closed list of VALUES (the categories a thing can take on \
that dimension). Tagging a text with (term type, value) asserts that the text is about, \
describes, or clearly exhibits that category: for example a text describing a proof-of-work \
validator receives (consensus_mechanism, proof of work). A text that merely uses a word in \
passing is not tagged with it.

Rules:
1. Use only term-type ids and value codes from the catalogue. Never invent values inside "tags".
2. Tag every (term type, value) the text clearly supports; several values of one term type may \
apply. Leave out term types the text does not address.
3. Each tag carries a confidence in [0, 1] and an evidence span: at most 20 words copied \
verbatim from the text.
4. Prefer the most specific term types that apply; the is-a structure (listed as "refines") \
means a text tagged under a specialised term type is implicitly classified by its more \
general ancestors, so do not repeat ancestors unless they carry a value of their own.
5. If the text clearly exhibits a category the catalogue lacks, either a missing value of an \
existing term type or a missing term type altogether, put it under "novel" with the same \
evidence rule. Propose at most 3, only when confident; most texts need none.
6. Output valid JSON only, no prose, no markdown fences.
"""

TAG_PROMPT = """\
Classify the following text with the taxonomy in the catalogue.

ITEM {item_id} ({source}{year}):
Title: {title}
Text: {text}

Return a single JSON object:
{{
  "item_id": "{item_id}",
  "tags": [
    {{"term_type": "<term type id>", "value": "<value code, e.g. v2>", "confidence": 0.0,
     "evidence": "<= 20 words verbatim from the text"}}
  ],
  "novel": [
    {{"kind": "value" | "term_type", "term_type": "<existing term type id, or null for a new term type>",
     "proposal": "<short label>", "definition": "<= 25 words", "evidence": "<= 20 words verbatim"}}
  ],
  "off_topic": false
}}

Set "off_topic" to true (with empty tags) when the text is not about DLT or crypto-assets at all.
"""


# Task E: discovery at an impure node. The node's residual items (tagged at the node but at
# none of its child term types) are shown; the model proposes missing values or child term types.
DISCOVER_INSTRUCTIONS = """\
You maintain a taxonomy of distributed-ledger technology (DLT) and crypto-asset concepts: \
TERM TYPES (classification dimensions phrased as questions) organised in an is-a DAG, each \
with a closed list of VALUES. You are shown one node of the DAG and a set of texts that were \
tagged at that node but at none of its child term types ("residual" texts). Your job is to \
say whether those texts share classification dimensions or categories the taxonomy lacks.

Rules:
1. Propose a NEW VALUE of the shown node when the residual texts clearly exhibit a category \
of that node's question that its value list lacks.
2. Propose a NEW CHILD TERM TYPE (a dimension that refines the node's question) when the \
residual texts can be split by a question the taxonomy does not ask, and give it 2-6 values.
3. Every proposal lists the ids of the residual texts that support it (at least 3) and one \
evidence span (at most 20 words, verbatim) from one of them.
4. Propose at most 4 candidates, most useful first. If the residual texts are simply the \
natural end of this branch, return an empty list.
5. Output valid JSON only, no prose, no markdown fences.
"""

DISCOVER_PROMPT = """\
NODE: {node_id} | {name}
Question: {question}
Category: {category}
Existing values: {values}
Existing child term types: {children}
Novel labels the tagger suggested while tagging (seeds, may be wrong): {seeds}

RESIDUAL TEXTS ({n} shown of {total}):
{items}

Return a single JSON object:
{{
  "node_id": "{node_id}",
  "candidates": [
    {{"kind": "value" | "child_term_type", "label": "short label", "question": "only for child_term_type",
     "definition": "<= 25 words", "values": ["only for child_term_type: 2-6 value labels"],
     "item_ids": ["..."], "evidence": "<= 20 words verbatim"}}
  ]
}}
"""
