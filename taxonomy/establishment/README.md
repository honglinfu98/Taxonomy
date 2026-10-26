# Part 1: taxonomy establishment (complete, 2026-10-26)

From the legal and academic PDFs to a term-type ontology with weighted is-a edges.
Code: `taxonomy/corpus/` (corpus construction) and `taxonomy/establishment/` (Tasks A
and B, metrics, dashboard). Outputs: `context/taxonomy_corpus.txt` and
`output/establishment/`.

```bash
. venv/bin/activate
python -m taxonomy.corpus.build_corpus          # corpus
python -m taxonomy.establishment.term_types     # Task A
python -m taxonomy.establishment.is_a           # Task B + DAG + metrics
python -m taxonomy.establishment.dashboard      # viewer
```

Requires `pdftotext` (poppler, `brew install poppler`) on PATH. No API key is
needed to build. Calling the API needs `anthropic` (in requirements.txt) and
`ANTHROPIC_API_KEY` in the repo-root `.env` (gitignored; template in `.env.example`),
which `llm_context` loads automatically.

## Inputs

- `legal/*.pdf` – 21 statutes, regulations and standard-setter documents
  (EU, UK, US, FATF, Basel, FSB, IOSCO, UN, Council of Europe).
- `context/*.pdf` – three papers: Tasca & Tessone (2018) blockchain taxonomy,
  Zhang, Ibañez & Xu (2026) crypto-asset taxonomy, Hernandez Cruz et al. (2026)
  DLT-Corpus.

## Output

`context/taxonomy_corpus.txt` is the single derived artefact and the file to send
to the API: the definitions articles, glossaries, classification criteria and
business-model sections of every legal PDF, plus the three papers (reference
lists removed), as XML-tagged `<document index=… type=… jurisdiction=… title=…
year=…>` blocks, each split into `<section label=…>` blocks. ~98K words, about
235K tokens as counted by Haiku 5.5 (always on its >100K-token rate card). Rebuild it after changing any PDF or `corpus/sources.py`.

## Files

| File | Role |
|---|---|
| `corpus/sources.py` | **Source of truth** for what is extracted: per-section line ranges or regex markers for each PDF, plus document metadata. |
| `corpus/pdf_text.py` | `pdftotext` wrapper, range selection, footer / line-number noise removal. |
| `corpus/build_corpus.py` | Entry point. Extracts everything and writes the corpus. |
| `establishment/prompts.py` | System instructions (stable, before the cached corpus) and per-task user prompts. `TASKS["A"]` is term type generation. |
| `establishment/dashboard.py` + `dashboard_template.html` | `python -m taxonomy.establishment.dashboard` embeds `output/establishment/is_a.json` into `output/establishment/is_a_dashboard.html`: an interactive DAG viewer with a threshold slider that reruns the consolidation in the browser. Rebuild after any Task B run. |
| `establishment/dag_metrics.py` | Information gain, reach-a-leaf AUC and effective-leaf metrics on the DAG, overall / per category / across thresholds. |
| `establishment/is_a.py` | Task B runner: `python -m taxonomy.establishment.is_a` asks, per term type, for a probability distribution over is-a parents in its category; verifies citations; writes `output/establishment/is_a*.{json,csv,md}`. |
| `establishment/term_types.py` | Task A runner: `python -m taxonomy.establishment.term_types` streams the answer, parses the JSON, verifies every `[doc, section, quote]` citation against the corpus, writes `output/establishment/term_types*.json`. |
| `../llm_context.py` | `client()` returns an `anthropic.Anthropic` using the key from `.env`; `build_request(instructions, user_prompt)` returns kwargs for `messages.create`, placing the corpus in the system prompt behind a 1-hour prompt-cache breakpoint (default model `claude-haiku-5-5`). |

## Calling the API

```python
from taxonomy.llm_context import build_request, client

resp = client().messages.create(**build_request(
    instructions="You are a taxonomist of crypto-asset and DLT terminology ...",
    user_prompt="Extract every term type used to classify stablecoins ...",
))
print(resp.content[0].text)
print(resp.usage)                                 # cache_read_input_tokens > 0 on repeat calls
```

Keep `instructions` fixed between calls (it precedes the cached corpus); put
everything that varies in `user_prompt`.

## Task A: term type generation

```bash
python -m taxonomy.establishment.term_types   # ~7 min, ~86K output tokens on Haiku 5.5
python -m taxonomy.establishment.term_types --verify-only   # re-run only the citation check on the saved output
```

Flags: `--model`, `--effort low|medium|high` (default high), `--max-tokens` (default
120000; the model's ceiling is 128K), `--thinking` (adaptive thinking; off by default).

How the run is put together:

- System prompt = `prompts.TAXONOMIST_INSTRUCTIONS` (what a term type is, grounding
  rules, JSON-only) followed by the cached corpus.
- User prompt = `prompts.TASK_A_PROMPT` (scope, JSON schema, ordering) plus a
  **manifest** of every document index and exact section label, generated from the
  corpus at run time so citations copy labels verbatim.
- Thinking is **off**: Haiku 5.5 thinks by default and on this corpus adaptive thinking
  consumed 100K+ tokens without emitting text. With thinking off the model answers
  directly and a full pass is ~60-90K tokens; `--max-tokens` must leave room for it.
- Output is streamed, parsed, and if truncated every complete term type is salvaged
  (`"truncated": true` is then set in the JSON).
- **Verification** (desideratum D1, faithfulness): each `{doc, section, quote}` is
  checked against the corpus. Quote matching lower-cases and strips everything but
  alphanumerics, then requires an exact substring or >=80% of 12-character shingles
  inside one window twice the quote's length (tolerates footnote markers and PDF
  spacing, rejects paraphrase). A quote found under another label of the same document
  is repaired (`section` corrected, model's label kept in `cited_section`, status
  `relabelled`). Every citation gets `"verified": true|false`; the report lists the rest.

Results so far (2026-10-26): 93 term types (asset 21, technology 24, actor 19,
activity 10, obligation_or_risk 19); 480 citations, 463 exact + 7 relabelled, 10
rejected (2.1%). A first run without the manifest gave 65 coarser term types with 9%
label errors; ids are not stable across runs, so reconciliation across runs/sources is
later work (Part 3).

## Task B: is-a hierarchy

```bash
python -m taxonomy.establishment.is_a         # all 93 children, 4 parallel requests
python -m taxonomy.establishment.is_a --only asset --limit 3   # smoke test
```

Flags: `--k` (max entries per distribution incl. `none`, default 6), `--workers`,
`--only <categories>`, `--limit N`, `--model`, `--effort`.

- Context = system instructions + cached corpus + a second cached block holding the
  Task A catalogue (id, name, category, question, values, aliases of every term type),
  so each per-child call reads ~251K tokens from cache and sends only the child's full
  record and the candidate list (the other term types in its category).
- The model returns `{"child", "distribution": [{"parent", "probability", "rationale",
  "citations"}]}`. The runner drops parents not in the candidate set, merges duplicates,
  renormalises to sum 1, and verifies citations exactly as in Task A.
- **Consolidation into a DAG.** The model's `none` entry is removed and each child's
  weights are renormalised over its candidate parents so they sum to exactly 1 (the
  original P(none) is kept as `p_none`). No probability threshold: every weighted edge is
  kept, taken in decreasing weight, unless it would close a cycle, so a mutual pair
  resolves to the stronger direction (an exact tie resolves by id order and is listed under
  `ties`). The first kept edge is the primary parent (tree in `is_a.md`), later ones are
  extra parents. The ontology has term types and is-a only. Acyclicity is asserted.
  `--render-only` redoes this from the saved JSON. Outputs: `is_a.md`, `taxonomy_dag.json`
  (nodes, edges, ties, edges dropped for cycles, metrics), `is_a.dot`, `is_a_edges.csv`
  (every weighted edge with a `kept_in_dag` flag), `dag_metrics.json` (metrics of the
  sub-DAG obtained by hiding edges below each weight 0.00-1.00, a what-if view for Part 3).

- **Metrics for self-maintenance** (`dag_metrics.py`). At a node y the kept edge weights
  of its children are normalised into a branching distribution q_y; a *random descent*
  starts at a uniformly chosen root and follows q_y until a leaf.
  - *Information gain*: H(q_y) in bits per node (0 for leaves and single-child nodes),
    summed (`total_bits`) and expected along a descent (`bits_per_descent`).
  - *AUC*: F(d) = P(descent has reached a leaf by depth d); AUC = area under F over
    [0, max depth] / max depth. 1.0 means every root is a leaf; lower means branches run
    deeper. `expected_depth` = E[d].
  - *Leaves needed*: leaf count, `effective_leaves` = 2^H(leaf-reach distribution), and
    `leaves_for_90pct`, the fewest leaves holding 90% of descents.
  These are reported overall and per category, and for every display weight so Part 3
  can trade information gain against depth and leaf count when choosing edges.

Results (2026-10-26, 93 children, 104 s, ~23M cached tokens read, 213/253 citations
verified). Full DAG: 279 of 401 weighted edges kept, 119 dropped for cycles, 5 roots (one
per category), 18 leaves, max depth 14; 90.5 bits total, 4.72 bits per descent; AUC 0.835,
expected depth 2.81; 14.0 effective leaves, 12 leaves hold 90% of descents. Hiding edges
below 0.4 leaves 64 edges and 30 roots. The model's weights are coarse (top values
0.3/0.42/0.55/0.62), so treat them as rankings.

## Reviewing the DAG

`python -m taxonomy.establishment.dashboard` writes `output/establishment/is_a_dashboard.html` (published copy:
https://claude.ai/artifact/4fCD72T7CAUmyLzjmcpFne). It carries every distribution and
replays `consolidate()` and `dag_metrics` in JavaScript. All edges are drawn (width and
opacity follow the weight); a display-only slider hides edges below a weight, swept
across 0..1 while the five category graphs, the edge/root/leaf counts and a spectrum
chart update live, together with bits per descent, AUC and effective leaves (a second
chart shows the three metrics across the spectrum). Dashed edges are those within 0.1
below the display weight when the checkbox is on; clicking a node shows its full
distribution with rationales, citation counts and why each entry was kept or not (hidden by
display weight, would cycle).

## Notes on the sources




- Line numbers in `corpus/sources.py` refer to plain `pdftotext` output split on `\n`
  only; form feeds are stripped so page breaks do not shift numbering.
- US bills are extracted with `pdftotext -layout` and located by regex markers,
  because their two-column line-number typesetting scrambles plain output.
- The Senate-reported CLARITY print reproduces the House-passed text before the
  Senate substitute; Title I is taken once (from the House file) and only the
  substitute's Sec. 2 definitions and Sec. 105 are taken from the Senate file.
- Paper tables (e.g. the 100-asset mapping) and reference lists are dropped.
- Bill page footers such as `HR 4763 RFS` are filtered; if a new bill leaks a footer,
  add it to `NOISE` in `corpus/pdf_text.py` and rebuild.
