# Evaluation

What WWW reviewers expect from a taxonomy paper: tagging accuracy as Micro-F1 and Macro-F1 on a
held-out gold set against a zero-shot LLM baseline and a supervised baseline, over three or more
runs with standard deviation; retrieval as P@k and NDCG@k on judged queries beside latency.
Code: `taxonomy/evaluation/`. Outputs: `output/evaluation/` and `paper/tables/eval_*.tex`.

```bash
python -m taxonomy.evaluation.gold select --size 300 --seed 11          # held-out items (150 papers, 150 patents)
python -m taxonomy.evaluation.gold annotate --model claude-opus-5-5 --passes 2 --workers 4
python -m taxonomy.evaluation.tagging_eval --runs 3 --workers 16        # dag / flat / supervised
python -m taxonomy.evaluation.retrieval_eval --runs 3 --k 10            # dag_index / flat_tags / supervised / bm25
```

## 1. Gold set (`gold.py`)

300 items drawn with a fixed seed from the sampled DLT-Corpus items, stratified by source. They
are excluded from the supervised baseline's training data. Labels come from two independent
passes of a stronger model (Opus 5.5, effort high, adaptive thinking) given the same catalogue
block the system uses; a (term type, value) label is gold when both passes assert it and its
evidence span is found verbatim in the text in at least one pass. `gold_summary.json` records
the agreement between passes (micro-F1 of pass 1 against pass 2), the labels dropped for
disagreement or missing evidence, and the cost. This is an LLM-adjudicated reference standard
with no human labels; the paper states this, and a human check of a subset is the obvious next
step.

## 2. Tagging (`tagging_eval.py`)

| system | what it is |
|---|---|
| `dag` (ours) | Haiku 5.5 with the catalogue block: questions, value definitions, is-a parents with weights; effort medium |
| `flat` | zero-shot baseline: same model and output format, label space given as a flat list of ids and value labels, no definitions, no hierarchy |
| `supervised` | TF-IDF (word 1-2 grams) + one-vs-rest logistic regression trained on the production tags of every tagged item outside the gold set; threshold tuned on 10% of the training items |

Metrics: Micro-F1 and Macro-F1 (macro over the labels that occur in gold) at the label level
(term type, value) and at the term-type level, precision, recall, tags per item, cost and time
per run; per-category label micro-F1. LLM runs differ by sampling; supervised runs by seed. Mean
± sd over runs. Predictions of every run are kept (`pred_{system}_run{r}.jsonl`) for retrieval.

## 3. Retrieval (`retrieval_eval.py`)

Judged collection = the gold items; relevance from gold labels (value query: 2 if the item
carries the label; node query: 2 for a gold tag at the node, 1 for a tag at a descendant via
is-a; AND query: minimum over atoms). Queries: every value with at least 3 relevant items, every
node with 5 to half the collection relevant, and 20 seeded two-atom AND queries with at least 3
relevant items. Systems: our DAG index on the `dag` tags of run r (bitsets, confidence x is-a
path strength ranking); boolean match on the `flat` tags without closure; the supervised labels
through the DAG index; BM25 over title and text with the query rendered as the term type name,
question and value labels. Metrics: P@5, P@10, R@10, NDCG@10 (graded), MAP, NDCG@10 per query
kind, mean latency per query. Mean ± sd over the tag runs. Full-index latency (8,205 items) is
in `output/retrieval/benchmark.md`.

## 4. Outputs

`gold_items.jsonl`, `gold_pass{1,2}.jsonl`, `gold.jsonl`, `gold_summary.json`,
`pred_*_run*.jsonl`, `tagging_eval.{json,md}`, `retrieval_queries.json`,
`retrieval_eval.{json,md}`; LaTeX tables `paper/tables/eval_tagging.tex` and
`paper/tables/eval_retrieval.tex`.
