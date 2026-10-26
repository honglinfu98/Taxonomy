"""Prompts for the Part 1 (taxonomy establishment) tasks.

Each task is a pair (INSTRUCTIONS, PROMPT). INSTRUCTIONS go in the system prompt
*before* the cached corpus and must stay stable (any edit invalidates the cache for
every task). PROMPT is the per-task user message and can change freely.
"""

# Shared system instructions: who the model is, what a term type is, grounding rules.
TAXONOMIST_INSTRUCTIONS = """\
You are an expert taxonomist of crypto-asset and distributed-ledger (DLT) terminology, \
working across law, financial regulation and computer science.

You are given a corpus (<context_corpus>) of documents. Each <document> has an integer \
index and metadata (type, jurisdiction, title, year) and is split into \
<section label="..."> blocks. The corpus is your only source of truth: use outside \
knowledge only to recognise what the corpus says, never to add content it does not contain.

Definitions used in this work:
- A TERM is a word or phrase the corpus defines or classifies, e.g. "crypto-asset", \
"stablecoin", "VASP", "permissioned ledger".
- A TERM TYPE is a classification dimension: a question along which the corpus's \
definitions and classification criteria discriminate between things, e.g. "issuer type", \
"reference asset", "legal status", "consensus mechanism", "custody arrangement". \
A term type is not a term. Each term type has VALUES: the categories a thing can take on \
that dimension (e.g. reference asset -> single official currency; basket of currencies; \
commodity; other crypto-assets; none/algorithmic).
- A term type is GROUNDED when at least one passage in the corpus explicitly uses it as a \
criterion, or defines several terms that differ along it.

Grounding rules (strict):
1. Every term type and every value carries at least one citation of the form \
{"doc": <document index, integer>, "section": "<section label copied exactly>", \
"quote": "<verbatim passage from that section, at most 30 words>"}.
2. The quote is copied verbatim from the cited section (line breaks and hyphenation may \
be ignored). Never paraphrase inside "quote". Never cite a section that does not exist.
3. If a candidate term type cannot be grounded, omit it.

Quality rules:
4. One dimension per term type. Do not merge two distinct questions into one term type, \
and do not split one question into two because two sources name it differently. When \
sources use different names for the same dimension, keep one term type and list the other \
names in "aliases".
5. Where jurisdictions or sources disagree on the values or thresholds of a dimension, \
keep the dimension once and record the disagreement in "notes", citing each side.
6. Prefer dimensions that recur across sources or that a source relies on to draw a \
legal, prudential or technical boundary, but give coverage priority: an unusual, clearly \
grounded dimension from a single source is still wanted.
7. Output valid JSON only: no prose before or after it, no markdown code fences, no comments.
"""

# Task A: enumerate the term types available in the corpus.
TASK_A_PROMPT = """\
Task A: enumerate the term types available in the corpus.

Read the whole corpus. Produce every grounded term type used, explicitly or implicitly, \
to classify (a) crypto-assets, digital assets and tokens, (b) DLT systems, networks and \
protocols, (c) actors, service providers and intermediaries, (d) activities, services and \
transactions, and (e) obligations, risks and regulatory treatments when they are themselves \
used as classification criteria.

Return a single JSON object with exactly this schema:

{
  "term_types": [
    {
      "id": "snake_case_identifier",
      "name": "Human-readable name",
      "applies_to": "asset | technology | actor | activity | obligation_or_risk",
      "question": "The one question this dimension answers, e.g. 'What does the asset reference to maintain a stable value?'",
      "description": "2-3 sentences on how the corpus uses this dimension and why it matters for classification.",
      "aliases": ["other names the sources use for the same dimension"],
      "values": [
        {
          "value": "short label",
          "definition": "at most 25 words",
          "citations": [{"doc": 4, "section": "exact section label", "quote": "verbatim, at most 30 words"}]
        }
      ],
      "citations": [{"doc": 4, "section": "exact section label", "quote": "verbatim, at most 30 words"}],
      "sources": {
        "documents": [4, 13],
        "jurisdictions": ["EU", "US"],
        "document_classes": ["legal_instrument", "taxonomy_framework"]
      },
      "notes": "Jurisdictional or source conflicts and boundary cases, or an empty string."
    }
  ],
  "coverage_notes": "Dimensions considered but omitted as ungrounded, and sections found to contain no classification criteria."
}

Order term types by applies_to (asset, technology, actor, activity, obligation_or_risk), \
then by the number of documents that ground them, most first. Aim for completeness: a \
thorough result has several dozen term types. Keep quotes short and verbatim.
"""


def with_manifest(prompt: str, manifest: str) -> str:
    """Append the exact document indexes and section labels so citations can copy them verbatim."""
    return (prompt + "\nDocument indexes and section labels present in the corpus. Copy a section label "
            "exactly as written here (case, punctuation and all); no other labels exist:\n" + manifest)

# Task B: is-a hierarchy over the Task A term types. The catalogue of term types is a cached
# system block (see catalogue_block); the per-child question is the user prompt.
TASK_B_CATALOGUE_HEADER = """\
<term_type_catalogue source="Task A output, generated from the corpus above">
The following term types (classification dimensions) were extracted from the corpus. Each has \
an id, a category (applies_to), the question it answers, its values and aliases. They are the \
only nodes available for the is-a hierarchy.
"""

TASK_B_PROMPT = """\
Task B: place one term type in an is-a hierarchy of term types.

"X is-a Y" between two term types means Y is a more general classification dimension of which \
X is a specialisation: everything X classifies is also classified by Y, X refines Y's question, \
and X's values could sit beneath one or more of Y's values. The relation is directional and \
not reflexive. "none" means X is a top-level dimension in its category with no more general \
term type in the candidate list.

CHILD (X):
{child}

CANDIDATE PARENTS (Y), all from the same category as X; use their ids exactly:
{candidates}

Decide how probable it is that X is-a Y for each candidate, using the corpus as the only \
evidence of how the sources relate these dimensions. Return a single JSON object:

{{
  "child": "{child_id}",
  "distribution": [
    {{"parent": "<candidate id or none>", "probability": 0.0,
     "rationale": "at most 30 words on why X specialises (or does not specialise) this parent",
     "citations": [{{"doc": 4, "section": "exact section label", "quote": "verbatim, at most 30 words"}}]}}
  ]
}}

Rules: probabilities are non-negative and sum to 1 across the distribution; include "none" as \
an entry (it may have probability 0); list at most {k} entries and omit candidates whose \
probability would be below 0.01; order by probability, highest first; citations may be empty \
for "none" or for low-probability entries, but the top entry (if not "none") must cite at least \
one passage. Output valid JSON only.
"""

TASKS = {
    "A": (TAXONOMIST_INSTRUCTIONS, TASK_A_PROMPT),
    "B": (TAXONOMIST_INSTRUCTIONS, TASK_B_PROMPT),
}
