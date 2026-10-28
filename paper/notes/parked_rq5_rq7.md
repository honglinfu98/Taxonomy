# Parked research questions RQ5 to RQ7 (removed from the draft on 2026-10-26)

The experiments section now answers RQ1 to RQ4 plus the gold-set tagging and retrieval
evaluation. The three questions below were in the draft as planned evaluations; they are parked
here with what each would need, so they can be revived for a journal version or a rebuttal.

## Original placeholder text

> RQ5: How does the ontology compare with expert taxonomies and LLM baselines given the same
> corpus? RQ6: How much do the manifest, grounding strategy and model matter? RQ7: Does the
> ontology improve a downstream classification of Web-sourced token descriptions?
>
> TODO: RQ5: expert taxonomies and LLM baselines (zero-shot, chunked RAG, RAPTOR, TnT-LLM) on
> the same corpus. RQ6: ablation rows for grounding strategy, model and prompt beside the
> manifest result of Section 5.2. RQ7: macro-F1 with and without the ontology, with one failure
> case.
>
> TODO (metrics): for RQ5 add precision and recall of term types against an expert gold set, an
> LLM judge calibrated against the experts (Zheng et al. 2023), and coverage of each expert
> taxonomy's dimensions.

## RQ5: expert taxonomies and LLM baselines

**In the paper since 2026-10-27** as Section 5.6 (`sections/5_experiments.tex`, `tables/rq5.tex`), with the baselines in the setup paragraphs and one sentence each in the abstract, contributions and conclusion. RQ6 is in the paper since 2026-10-27 as Section 5.7 (`tables/rq6.tex`). Only RQ7 (an independent downstream task) remains parked.

**Run on 2026-10-27 with Haiku 5.5** (`taxonomy/baselines/`, results in `output/baselines/rq5.md`, table `paper/tables/rq5.tex`, caveats in `taxonomy/baselines/README.md`). The notes below describe the state before the run.

- **Expert gold set.** The only expert taxonomies available are the three academic papers in
  `context/`, and they are inside the corpus the model read when it generated the term types.
  Coverage of their dimensions is measurable (extract each paper's dimensions into a list, match
  with `taxonomy/establishment/agreement.py`) but contaminated: it can only be reported as recall
  of dimensions the corpus itself contains. An independent expert list, or human annotation, is
  needed for an uncontaminated number.
- **Zero-shot without the corpus.** One Task A call with no corpus block (parametric knowledge
  only). About $0.10 and ten minutes. Faithfulness cannot be scored (no citations); term-type
  agreement with the grounded run and expert-dimension coverage can. Not run.
- **Chunked RAG.** Needs a chunk index over the corpus, a query set, and a merge step for term
  types proposed per retrieved chunk set; about a day, with design choices reviewers can dispute.
  Not run.
- **RAPTOR.** Chunked RAG plus a recursive summary tree. Not run.
- **TnT-LLM.** Taxonomy-from-content (summarise, cluster, name); a baseline for Part 2's
  discovery rather than for Task A. Not run.

## RQ6: ablations

**In the paper since 2026-10-27** as Section 5.7 "RQ6: What Each Ingredient Contributes" (`sections/5_experiments.tex`, `tables/rq6.tex`), with the variants in the setup paragraphs, the RQ1 stability paragraph shortened to point at it, and one sentence each in the abstract, contributions and conclusion. The method section still quotes the uncontrolled first run (9%, 65 types); RQ6 reports the controlled rerun (21% relabelled, 62 types) and names the difference.

**Run on 2026-10-27 with Haiku 5.5** (`taxonomy/baselines/ablate.py` + `rq6.py`, results in
`output/ablations/rq6.md`, table `paper/tables/rq6.tex`, findings and caveats in
`taxonomy/baselines/README.md`). One run per variant: no manifest 62 types with 21% of citations
relabelled (the method section's "9%, 65 types" is the historical first run; this controlled rerun
should replace it); no citation requirement 39 types (recall of main 0.36, precision 0.85); no
definitions block 111 types (recall 0.68, precision 0.57); effort low 46; Sonnet medium 54 (judged
0.52), Sonnet high truncated 72 (0.57); Haiku repeat 76 (0.60). Agreement alone cannot separate
the variants from run-to-run noise; size, label accuracy and precision can. The notes below
describe the state before the run.

- **Manifest.** Done (Section 5.2 of the draft).
- **Model.** Partly done. LLM-judged run-to-run agreement (judge.py, Haiku): F1 0.604 for the Haiku repeat (lexical 0.51). Task A repeats in `output/establishment/repeats/`:
  Haiku 5.5 second run with the same prompt: 76 term types, 387/399 citations verified,
  agreement with run 1 F1 0.51 (43 matched), value Jaccard 0.32.
  Sonnet 5.5 at effort high: truncated at the 127K output ceiling (thinking cannot be disabled on
  Sonnet 5.5), 72 complete term types salvaged, 414/414 citations verified, agreement F1 0.55.
  Sonnet 5.5 at effort medium: complete, 54 term types, 264/264 verified.
  The matcher pairs term types by name and question wording at threshold 0.55; paraphrased
  dimensions count as disagreements, so an LLM-judged matching pass is needed before quoting
  these as run-to-run agreement.
- **Grounding strategy and prompt.** Each is one Task A run via
  `python -m taxonomy.establishment.term_types --tag <name>` with a prompt variant (no citation
  requirement, no definitions-first ordering, lower effort), about $0.50 and fifteen minutes.
  Not run.

## RQ7: downstream classification with and without the ontology

**Run on 2026-10-28 with Haiku 5.5** (`taxonomy/rq7/`, results in `output/rq7/rq7.md`, table
`paper/tables/rq7.tex`, failure cases `output/rq7/failure_cases.md`, findings and caveats in
`taxonomy/rq7/README.md`). Dataset collected: 378 CoinGecko descriptions of the top 500 coins,
gold = the site's own 28 retained categories (independent of our catalogue). Catalogue as prompt
context: no gain (0.570 vs 0.571 micro-F1). Ontology tags alone (no description): 0.535. Supervised:
tag features 0.478 / 0.402 (micro / macro) vs TF-IDF 0.487 / 0.257, both 0.514 / 0.423. Failure
case: Stacks (Bitcoin L2) classed Layer 1 through the catalogue, which has no layer-2 value.
The notes below describe the state before the run.

As written it assumes a separate dataset of Web-sourced token descriptions that was never
collected. The gold-set tagging evaluation (`taxonomy/evaluation/`) answers the same question
on DLT-Corpus items: flat-label LLM = without the ontology (no definitions, no hierarchy),
DAG-guided tagger = with, supervised TF-IDF + LR = learned alternative, Macro-F1 over three runs.
A failure case can be taken from `output/evaluation/pred_*_run*.jsonl`. If a token-description
dataset is collected later, the same scripts apply unchanged with a new gold set.

## Cost to revive the cheap parts

Zero-shot-without-corpus Task A, two prompt ablations, expert-dimension coverage with the
contamination note: about $2 and an hour of API time.
