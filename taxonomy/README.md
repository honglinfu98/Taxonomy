# taxonomy package: LLM context extraction

Builds the Claude-API-ready corpus used to extract cryptocurrency / DLT term
types for the taxonomy.

```bash
. venv/bin/activate
python -m taxonomy.build_corpus      # from the repo root
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
235K tokens as counted by Haiku 5.5 (always on its >100K-token rate card). Rebuild it after changing any PDF or `sources.py`.

## Files

| File | Role |
|---|---|
| `sources.py` | **Source of truth** for what is extracted: per-section line ranges or regex markers for each PDF, plus document metadata. |
| `pdf_text.py` | `pdftotext` wrapper, range selection, footer / line-number noise removal. |
| `build_corpus.py` | Entry point. Extracts everything and writes the corpus. |
| `prompts.py` | System instructions (stable, before the cached corpus) and per-task user prompts. `TASKS["A"]` is term type generation. |
| `term_types.py` | Task A runner: `python -m taxonomy.term_types` streams the answer, parses the JSON, verifies every `[doc, section, quote]` citation against the corpus, writes `output/term_types*.json`. |
| `llm_context.py` | `client()` returns an `anthropic.Anthropic` using the key from `.env`; `build_request(instructions, user_prompt)` returns kwargs for `messages.create`, placing the corpus in the system prompt behind a 1-hour prompt-cache breakpoint (default model `claude-haiku-5-5`). |

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
python -m taxonomy.term_types                 # ~7 min, ~86K output tokens on Haiku 5.5
python -m taxonomy.term_types --verify-only   # re-run only the citation check on the saved output
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

## Notes on the sources


- Line numbers in `sources.py` refer to plain `pdftotext` output split on `\n`
  only; form feeds are stripped so page breaks do not shift numbering.
- US bills are extracted with `pdftotext -layout` and located by regex markers,
  because their two-column line-number typesetting scrambles plain output.
- The Senate-reported CLARITY print reproduces the House-passed text before the
  Senate substitute; Title I is taken once (from the House file) and only the
  substitute's Sec. 2 definitions and Sec. 105 are taken from the Senate file.
- Paper tables (e.g. the 100-asset mapping) and reference lists are dropped.
- Bill page footers such as `HR 4763 RFS` are filtered; if a new bill leaks a footer,
  add it to `NOISE` in `pdf_text.py` and rebuild.
