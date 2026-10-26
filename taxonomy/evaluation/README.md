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

## 5. Results (catalogue v6, 2026-10-26)

Gold: 300 items, two Opus 5.5 passes, pass agreement micro-F1 0.88, 1,168 labels (3.89 per
item) over 209 distinct labels and 84 term types; 309 labels dropped for disagreement; $20.8.

| tagging system | label micro-F1 | label macro-F1 | type micro-F1 | cost / run |
|---|---|---|---|---|
| DAG-guided, Haiku 5.5 (production) | 0.379 ± 0.006 | 0.316 ± 0.002 | 0.493 ± 0.005 | $0.17 |
| flat zero-shot, Haiku 5.5 | 0.387 ± 0.009 | 0.321 ± 0.012 | 0.485 ± 0.006 | $0.11 |
| supervised TF-IDF + LR | 0.388 ± 0.003 | 0.160 ± 0.002 | 0.482 ± 0.002 | 0 |
| DAG-guided, Sonnet 5.5 | 0.595 ± 0.004 | 0.505 ± 0.008 | 0.658 ± 0.006 | $3.20 |
| flat zero-shot, Sonnet 5.5 | 0.594 ± 0.006 | 0.518 ± 0.002 | 0.668 ± 0.009 | $1.84 |

The catalogue block (definitions, hierarchy) does not raise tagging accuracy over a flat label
list at either model; the model does (+0.21 micro-F1 from Haiku to Sonnet). The supervised
classifier matches the LLMs on micro-F1 but halves macro-F1: it learns the frequent labels.

| retrieval system (110 judged queries) | P@10 | NDCG@10 | MAP | node queries NDCG@10 | latency (us) |
|---|---|---|---|---|---|
| DAG index, Sonnet 5.5 tags | 0.409 ± 0.003 | 0.596 ± 0.011 | 0.373 ± 0.012 | 0.723 ± 0.010 | 24 |
| flat Sonnet 5.5 tags, no closure | 0.316 ± 0.006 | 0.539 ± 0.009 | 0.362 ± 0.006 | 0.420 ± 0.027 | 282 |
| DAG index, Haiku 5.5 tags | 0.292 ± 0.012 | 0.413 ± 0.028 | 0.229 ± 0.016 | 0.546 ± 0.043 | 27 |
| flat Haiku 5.5 tags, no closure | 0.233 ± 0.013 | 0.393 ± 0.016 | 0.225 ± 0.013 | 0.368 ± 0.034 | 303 |
| supervised labels + DAG index | 0.234 ± 0.001 | 0.308 ± 0.006 | 0.145 ± 0.006 | 0.372 ± 0.006 | 25 |
| BM25 over text | 0.226 | 0.313 | 0.140 | 0.281 | 587 |

The hierarchy is what retrieval gains from the DAG: with the same tags, is-a closure lifts node
queries from 0.42 to 0.72 NDCG@10 and P@10 from 0.32 to 0.41 at a tenth of the latency; every
tag-based index beats BM25 over the text. Full tables: `output/evaluation/tagging_eval.md`,
`retrieval_eval.md`; billing for every stage: `billing.md` ($60.7 for everything recorded).

Task A repeats (`output/establishment/repeats/`, `taxonomy/establishment/agreement.py`): a second
Haiku run gives 76 term types and agreement F1 0.51 with run 1 (43 matched, value Jaccard 0.32);
Sonnet 5.5 at effort high is truncated at the 127K output ceiling (72 types, F1 0.55), at medium
complete with 54 types (F1 0.40). The matcher is lexical (name + question), so these are lower
bounds on semantic agreement.
