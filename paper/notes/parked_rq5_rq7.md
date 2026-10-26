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

- **Manifest.** Done (Section 5.2 of the draft).
- **Model.** Partly done. Task A repeats in `output/establishment/repeats/`:
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

As written it assumes a separate dataset of Web-sourced token descriptions that was never
collected. The gold-set tagging evaluation (`taxonomy/evaluation/`) answers the same question
on DLT-Corpus items: flat-label LLM = without the ontology (no definitions, no hierarchy),
DAG-guided tagger = with, supervised TF-IDF + LR = learned alternative, Macro-F1 over three runs.
A failure case can be taken from `output/evaluation/pred_*_run*.jsonl`. If a token-description
dataset is collected later, the same scripts apply unchanged with a new gold set.

## Cost to revive the cheap parts

Zero-shot-without-corpus Task A, two prompt ablations, expert-dimension coverage with the
contamination note: about $2 and an hour of API time.
