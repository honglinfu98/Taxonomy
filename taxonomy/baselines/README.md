# RQ5 baselines: how else could the catalogue have been built?

RQ5 asks how our catalogue (Task A: the whole corpus in one cached context, a manifest of
section labels, and a verbatim-citation rule) compares with expert taxonomies and with the ways
reviewers already know for building a taxonomy with an LLM. Every baseline here is an
alternative Task A over the **same 24-document corpus** and the **same model** (Haiku 5.5,
thinking disabled), producing a catalogue in the same schema so that the same verifier,
matcher, Task B and tagger apply to all of them.

## Baselines (`output/baselines/<name>/term_types.json`)

| name | what it replaces | recipe |
|---|---|---|
| `zeroshot` | the corpus | the Task A prompt and schema, the 24 document titles, no document text; citations empty by construction (`zeroshot.py`) |
| `rag` | one long context | sections split into 129 passages of <= 900 words; 40 model-written keyword queries (8 per category); BM25 top-8 passages per query; the Task A instructions over the retrieved passages with the citation rule; one consolidation call groups the 498 per-query proposals by question, values and citations unioned deterministically (`rag.py`) |
| `raptor` | flat chunk retrieval | the RAG pipeline with a RAPTOR summary tree in the pool: TF-IDF + SVD embeddings, k-means (k = n/5), model summaries (<= 350 words) recursively to 33 summary nodes over 3 levels; collapsed-tree retrieval over passages and summaries; summaries may inform a term type but cannot be quoted (`rag.py --tree`) |
| `tnt` | top-down generation from documents | TnT-LLM: summarise every passage (<= 120 words), then build the taxonomy bottom-up over batches of 30 summaries (initial, then update), then one review pass; no citations by design (`tnt.py`) |
| `expert_key` | (reference) | the classification dimensions of the two published taxonomies in the corpus (Tasca & Tessone, doc 1; Zhang, Ibanez & Xu, doc 2), extracted per paper with a verified quote or a verbatim dimension name (`expert_key.py`) |

Our catalogue is `output/establishment/term_types.json` (93 term types) and its second run
`output/establishment/repeats/term_types.haiku_run2.json` is the run-to-run reference.

## Measurements (`compare.py` -> `output/baselines/rq5.{json,md}`, `paper/tables/rq5.tex`)

- **Size and faithfulness.** Term types, values, and the share of citations the Task A verifier
  finds verbatim in the cited section (`term_types.verification.json`). Zero-shot and TnT-LLM
  cannot cite.
- **Agreement with ours.** Lexical (`establishment/agreement.py`, name + question similarity,
  a lower bound) and LLM-judged (`judge.py`: both catalogues shown, pairs that ask the same
  question about the same kind of thing; run in both directions, intersection kept, one-to-one).
  Reported as F1 with recall of our types and precision of the baseline's.
- **Expert coverage.** The judged share of the key's dimensions a catalogue contains, and the
  precision (share of the catalogue's types matching a key dimension). *Contaminated* for every
  corpus-based catalogue, since both papers are in the corpus; uncontaminated only for zero-shot.
- **Structure.** The unchanged Task B (`structure.py`, corpus-grounded for every catalogue) and
  the Part 1 metrics: bits per descent, reach-a-leaf AUC, effective leaves.
- **Downstream.** Tag the 300 gold items with each catalogue (production tagger prompt, no is-a
  edges, Haiku 5.5, 3 runs); map each baseline's term types to the gold space (catalogue v6) with
  the judge; type-level micro/macro F1 against the gold term types (`downstream.py`). Predicted
  types that map to no gold type count as false positives.
- **Cost and time** per catalogue.

## Running

```
python -m taxonomy.baselines.zeroshot
python -m taxonomy.baselines.rag && python -m taxonomy.baselines.rag --tree
python -m taxonomy.baselines.tnt
python -m taxonomy.baselines.expert_key
python -m taxonomy.baselines.structure zeroshot rag raptor tnt
python -m taxonomy.baselines.downstream ours zeroshot rag raptor tnt
python -m taxonomy.baselines.compare
```

All catalogue generators default to `claude-haiku-5-5`; `--model` switches the generator and
`--judge-model` the matcher.

## Results (Haiku 5.5 everywhere, 2026-10-27)

Full table: `output/baselines/rq5.md`; LaTeX: `paper/tables/rq5.tex`; per-catalogue files under
`output/baselines/<name>/`. RQ5 cost $8.83 in total (billing.md rows prefixed RQ5), of which $5.8
is Task B over the four baseline catalogues at the long-prompt card.

| catalogue | types | values | citations verified | judged agreement with ours F1 (recall / precision) | expert coverage (precision) | bits/descent | AUC | downstream type micro-F1 | macro-F1 |
|---|---|---|---|---|---|---|---|---|---|
| ours | 93 | 317 | 98% | 1 | 0.667 (0.280) | 4.72 | 0.835 | 0.340 ± 0.007 | 0.195 ± 0.017 |
| ours, second run | 76 | 260 | 97% | 0.604 (0.548 / 0.671) | 0.667 (0.342) | | | | |
| zero-shot, no corpus | 32 | 102 | none | 0.304 (0.204 / 0.594) | 0.256 (0.312) | 3.61 | 0.621 | 0.203 ± 0.002 | 0.054 ± 0.001 |
| chunked RAG | 81 | 750 | 99% | 0.471 (0.441 / 0.506) | 0.590 (0.284) | 4.27 | 0.850 | 0.238 ± 0.002 | 0.111 ± 0.002 |
| RAPTOR | 65 | 631 | 87% | 0.430 (0.366 / 0.523) | 0.564 (0.338) | 4.87 | 0.727 | 0.178 ± 0.009 | 0.082 ± 0.007 |
| TnT-LLM | 170 | 485 | none | 0.327 (0.462 / 0.253) | 0.769 (0.176) | 5.85 | 0.823 | 0.123 ± 0.006 | 0.079 ± 0.013 |

What the numbers say:

- **The corpus is most of the catalogue.** Without it the same model and prompt produce 32
  dimensions, covering a fifth of our catalogue and a quarter of the expert key, and the
  obligation, actor and activity branches that only the legal instruments define are almost
  absent. Zero-shot is the one uncontaminated expert-coverage number (0.256).
- **Retrieval fragments the catalogue.** Chunked RAG proposes 498 term types over 40 queries;
  after consolidation it keeps 81 with 750 values (2.4x ours per type), of which the judge maps
  39 to gold dimensions, and its value lists are padded with near-duplicates from different
  passages. RAPTOR's summaries lose verbatim text (87% citations verified against 98-99% for the
  passage-based catalogues) and do not recover coverage (0.430 agreement with ours).
- **TnT-LLM over-generates.** Bottom-up from 129 summaries it accumulates 170 term types; the
  review pass removes none. It has the highest raw expert coverage (0.769, contaminated: the
  papers' sections are among its inputs) at the lowest precision (0.176), cannot cite, and is
  the worst downstream (0.123) because only 37 of its 170 types map to a gold dimension.
- **Run-to-run stability, judged.** Our second run agrees with the first at F1 0.604 by the
  judge (0.509 lexical): 51 of the 76 second-run types are the same question as a first-run
  type. This is the number to quote for RQ6's model-repeat row; the lexical 0.51 was a lower bound.
- **Expert key.** Our catalogue contains 26 of the 39 dimensions of the two taxonomy papers. The
  13 it misses are mostly Tasca & Tessone's engineering sub-dimensions (network topology,
  gossiping, latency, block-header data structure, server and block storage, scalability limits,
  intraoperability, data encryption, coding language, fee structure) plus Zhang et al.'s
  minting issuer, which our catalogue folds into issuer type. The task prompt asks for
  dimensions the sources use as legal, prudential or technical boundaries, which explains the
  engineering misses; whether to add them is a scope decision, not a defect of the method.

Caveats to carry into the paper:

1. **Downstream is biased toward our catalogue.** The gold labels were adjudicated with
   catalogue v6 in view, so the gold dimensions are our dimensions; a baseline is scored only
   through the judge's mapping of its types onto ours. The downstream column therefore measures
   how far each catalogue reproduces our dimensions on real items, not an independent task.
   An independent downstream task needs labels produced without any catalogue.
2. **Expert coverage is contaminated** for every corpus-based catalogue (the two papers are in
   the corpus). Only the zero-shot number is clean.
3. **The judge is Haiku 5.5** (same model as the generators). Re-running `compare.py` and
   `downstream.py` with `--judge-model claude-opus-5-5` costs about $3 and should be done
   before the numbers go into the paper.
4. **RAG and RAPTOR design choices** (BM25 instead of dense retrieval, k = 8, 40 model-written
   queries, TF-IDF + k-means instead of SBERT + UMAP + GMM) are the cheapest faithful versions;
   a reviewer can ask for the dense variants.

# RQ6 ablations: how much do the manifest, grounding strategy, prompt and model matter?

`ablate.py` runs Task A with one ingredient removed or changed (everything else as in the main
run: whole corpus in one cached context, Haiku 5.5, thinking disabled, effort high); `rq6.py`
scores each run like an RQ5 baseline (size, citation verification, section-label accuracy,
lexical and judged agreement with the main run, expert-key coverage, cost) and adds the model
repeats from `output/establishment/repeats/`. Outputs: `output/ablations/<variant>/`,
`output/ablations/rq6.{json,md}`, `paper/tables/rq6.tex`.

```
python -m taxonomy.baselines.ablate no_manifest no_citations no_definitions effort_low
python -m taxonomy.baselines.rq6
```

## Results (Haiku 5.5 unless stated, 2026-10-27; one run per variant)

| variant | ingredient | types | values | citations verified | label exact | judged agreement with main run F1 (recall / precision) | expert coverage (precision) | cost |
|---|---|---|---|---|---|---|---|---|
| main run | reference | 93 | 317 | 98% | 96% | 1 | 0.667 (0.280) | $0.23 |
| second run, same prompt | model | 76 | 260 | 97% | 96% | 0.604 (0.548 / 0.671) | 0.667 (0.342) | $0.42 |
| Sonnet 5.5, effort medium | model | 54 | 210 | 100% | 100% | 0.517 (0.409 / 0.704) | 0.590 (0.426) | $0.40 |
| Sonnet 5.5, effort high (truncated) | model | 72 | 308 | 100% | 100% | 0.570 (0.505 / 0.653) | 0.821 (0.444) | $2.21 |
| effort low | prompt | 46 | 165 | 100% | 99% | 0.532 (0.398 / 0.804) | 0.538 (0.457) | $0.34 |
| no manifest | manifest | 62 | 209 | 98% | 77% | 0.645 (0.538 / 0.806) | 0.718 (0.452) | $0.37 |
| no definitions block | prompt | 111 | 303 | 100% | 99% | 0.618 (0.677 / 0.568) | 0.821 (0.288) | $0.47 |
| no citation requirement | grounding | 39 | 193 | none | - | 0.500 (0.355 / 0.846) | 0.436 (0.436) | $0.30 |

What the numbers say:

- **The manifest fixes labels, not dimensions.** Without it 21% of citations cite a section
  label that had to be relabelled by the verifier (57/271) and 6 more fail outright, against
  1.5% relabelled with it; the catalogue itself (62 types, judged agreement 0.645) is within the
  run-to-run band. The paper's method section quotes the historical first run (9% wrong, 65
  types); this controlled rerun is worse on labels and should replace it.
- **The citation requirement is what makes the model read.** Without it the same model, prompt
  and corpus return 39 term types in 111 seconds, a third of the main run's recall (0.355) at the
  highest precision (0.846), and less than half the expert key. Having to quote forces a
  section-by-section pass; the quality rules alone do not. Removing citations does not produce
  ungrounded extras, it produces a short catalogue.
- **The definitions block controls granularity.** Without the definitions of term, term type and
  grounded the model returns 111 types with the highest recall of the main run (0.677) and the
  lowest precision (0.568): more splitting, more topic-like dimensions, 0.288 precision against
  the expert key.
- **Effort and model trade size for precision.** Effort low gives 46 types; Sonnet 5.5 at medium
  54, at high 72 before the output ceiling; all at 100% verified citations and higher precision
  against the main run than the Haiku repeat. The dimension set is model-dependent (agreement
  0.52-0.57 against 0.60 for a Haiku repeat); grounding is not.
- **Agreement cannot separate most variants from sampling noise.** Every variant's judged
  agreement with the main run (0.50-0.65) sits at or below the run-to-run level (0.60), so a
  single run per variant shows effects on size, label accuracy and precision, not on the
  identity of the dimensions. A second run per variant (about $1.50) would give the sd.

Caveats: one run per variant; judge is Haiku 5.5 (rerun `rq6.py --judge-model claude-opus-5-5`);
expert coverage contaminated as in RQ5; Sonnet high is truncated (72 complete types salvaged of an
output that hit the 127K ceiling). RQ6 cost $1.55 (four Task A calls $1.48, twelve judge calls).
