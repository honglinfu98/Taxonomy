# Taxonomy

## Aim

Build a **dynamically self-maintaining DAG taxonomy** of cryptocurrency / DLT
concepts, used to **tag content** and to **retrieve it fast** by walking the graph
instead of searching flat text. Nodes are concepts (terms and the classification
dimensions that organise them), edges are "is a kind of" / "is classified by"
relations, and the graph is a DAG because a concept can sit under more than one
parent (a payment stablecoin is both an *asset referencing a fiat currency* and a
*regulated payment instrument*). Every node is grounded in cited source passages,
so the taxonomy can be audited and regenerated when the sources change.

## The three parts

| Part | Role | Status |
|---|---|---|
| **1. Taxonomy establishment** | Establish the graph from a grounded corpus of legal instruments and academic taxonomies. | **complete (2026-10-26)**: `taxonomy/establishment/`, `output/establishment/` |
| **2. Classification** | Tag content onto DAG nodes; maintain the DAG from node statistics (information gain, reach-a-leaf AUC, effective leaves / nodes) and discover new nodes from impurity. | **complete for the on-topic DLT-Corpus (2026-10-26)**: `taxonomy/classification/`; 6 iterations, 36,702 items, seed v0 -> v6 (93 -> 132 term types, 317 -> 549 values), $19.3 |
| **3. Optimization** | Index the tagged content on the DAG and retrieve it by graph operations: reachability closure, weighted is-a paths, lowest common ancestors, information content, facet gain for the best next question. | **first version (2026-10-26)**: `taxonomy/retrieval/`, `output/retrieval/`; 33,581 items indexed, queries in 2 to 11 us (3,400 to 10,000x faster than flat scans); NDCG@10 0.60 on judged queries vs 0.31 for BM25 |

## Part 1: taxonomy establishment (complete)

The LLM (Claude, default `claude-haiku-5-5`) is fed one fixed context, the
**taxonomy corpus** (`context/taxonomy_corpus.txt`), built from 21 legal PDFs in
`legal/` and three taxonomy papers in `context/`. The corpus (~235K tokens) sits behind a
1-hour prompt-cache breakpoint, so each task is a cheap query on top of the same context.

| Task | Question to the LLM | Output |
|---|---|---|
| **A. Term type generation** (done 2026-10-26) | Which *classification dimensions* (term types) does the corpus use, explicitly or implicitly, to classify assets, technologies, actors, activities and obligations? Every dimension and value must cite `[doc index, section label]` with a verbatim quote. | `output/term_types.json`: 93 term types, 480 citations, 98% verified against the corpus (`output/term_types.verification.json`) |
| **B. Is-a hierarchy** (done 2026-10-26) | For each term type X, over the other term types Y in its category: how probable is it that *X is-a Y* (Y is the more general dimension X specialises)? Answer is a probability distribution over candidate parents (renormalised to sum to 1 after removing the model's `none` entry), each entry with rationale and citations. Context = the same corpus plus the Task A catalogue. | `output/taxonomy_dag.json` (the DAG: 93 nodes, all 279 acyclic weighted edges, no threshold, with metrics), `output/is_a.md` (tree view), `output/is_a.json` (all distributions), `output/dag_metrics.json` (metrics when hiding edges below each weight), dashboard `output/is_a_dashboard.html` |

The ontology is term types connected by **is-a** only. Each edge carries P(X is-a Y) so
that Part 3 can maintain the graph by **information gain** (bits resolved per node and per
root-to-leaf descent), **AUC** of the reach-a-leaf curve (how quickly branches end) and
**how many leaves are needed** (effective leaves), all computed in `taxonomy/dag_metrics.py`.

A **term type** is a classification dimension along which definitions
discriminate, e.g. *issuer type*, *reference asset*, *legal status*, *consensus
mechanism*. A **term** is a thing classified (e.g. *e-money token*). Task A yields
the dimensions; later tasks populate and link the terms under them.

### Run

```bash
. venv/bin/activate
python -m taxonomy.corpus.build_corpus          # rebuild context/taxonomy_corpus.txt from the PDFs
python -m taxonomy.establishment.term_types     # Task A -> output/establishment/term_types.json
python -m taxonomy.establishment.is_a           # Task B -> is_a.json, taxonomy_dag.json, dag_metrics.json
python -m taxonomy.establishment.dashboard      # DAG viewer -> output/establishment/is_a_dashboard.html
```

`taxonomy/establishment/README.md` documents Part 1 in full (corpus construction,
prompts, runners, consolidation rules, metrics, results). The published DAG viewer is
https://claude.ai/artifact/4fCD72T7CAUmyLzjmcpFne.

## Part 2: classification (in progress)

The DAG is the label space. Content is tagged onto its nodes; node statistics drive the
three self-maintenance objectives (information gain, AUC of the reach-a-leaf curve,
effective leaves / nodes); entropy impurity at a node marks where new values or term
types are discovered from the content. Retrieval over the DAG is Part 3. Content: the **DLT-Corpus** (scientific
literature and USPTO patents from `ExponentialScience/dlt-corpus` on Hugging Face), sampled
in proportion for cost. The pilot tags items with Haiku 5.5 and the catalogue of term types
and values (with is-a parents) cached in the prompt; the tagged items will train an
in-house classifier to replace the LLM for bulk tagging.

```bash
python -m taxonomy.classification.sample     # pilot sample -> data/dlt_corpus/sample.jsonl
python -m taxonomy.classification.tag        # Task C tagging -> output/classification/
python -m taxonomy.classification.maintain   # label space, objectives, discovery at impure nodes
python -m taxonomy.classification.evolve     # consolidate accepted candidates -> next catalogue version + log
```

Mechanism: `taxonomy/classification/MAINTENANCE.md`. Pipeline, data and results:
`taxonomy/classification/README.md`. DAG evolution from the v0 seed: `output/evolution/evolution.md`.

## Part 3: optimisation (retrieval over the DAG)

Tagged items become bitset postings on the DAG nodes (direct, per value, and subtree
closure). Queries are boolean combinations of nodes, values, strength-restricted subtrees
and categories, evaluated with integer set algebra; results are ranked by tag confidence
weighted by the best is-a path strength (Task B weights), generalised by the lowest common
ancestor of the query nodes, expanded to similar nodes when few items match, and narrowed
by the facet with the highest expected information gain, which is the retrieval-time use
of the same objective that maintains the DAG in Part 2.

```bash
python -m taxonomy.retrieval.index        # index.pkl from all tagged iterations
python -m taxonomy.retrieval.query 'consensus_mechanism="proof of stake" AND privacy_enhancement'
python -m taxonomy.retrieval.query --text "zero-knowledge proofs for private payments"
python -m taxonomy.retrieval.benchmark    # output/retrieval/benchmark.md
```

Details and results: `taxonomy/retrieval/README.md`.

## Evaluation

Held-out gold set (300 items, two-pass strong-model annotation, adjudicated), tagging
Micro-F1 / Macro-F1 for the DAG-guided tagger against a zero-shot flat-label LLM and a
supervised TF-IDF + logistic regression baseline over three runs with sd, and retrieval
P@k / NDCG@k on judged queries with latency for the DAG index against flat tags and BM25.

```bash
python -m taxonomy.evaluation.gold select && python -m taxonomy.evaluation.gold annotate
python -m taxonomy.evaluation.tagging_eval --runs 3
python -m taxonomy.evaluation.retrieval_eval --runs 3
```

Protocol and results: `taxonomy/evaluation/README.md`, `output/evaluation/`, `paper/tables/eval_*.tex`.

### RQ5: catalogue baselines (`taxonomy/baselines/`, Haiku 5.5)

Four alternative ways to build the catalogue from the same corpus, scored on citations verified,
LLM-judged agreement with ours, coverage of the 39 dimensions of the two taxonomy papers in the
corpus, structure after Task B, and type-level F1 when tagging the gold items (table:
`output/baselines/rq5.md`, `paper/tables/rq5.tex`). Zero-shot without the corpus reaches 32
types and 0.30 judged agreement with ours; chunked RAG 81 types at 0.47; RAPTOR 65 at 0.43;
TnT-LLM 170 at 0.33 with no citations. Our run-to-run agreement is 0.60 by the judge. Downstream
type micro-F1: ours 0.34, RAG 0.24, zero-shot 0.20, RAPTOR 0.18, TnT-LLM 0.12 (biased toward ours:
the gold is in our label space). RQ5 cost $8.83.

### RQ6: Task A ablations (`taxonomy/baselines/ablate.py`, `rq6.py`)

One Task A run per ingredient removed or changed, scored like the RQ5 baselines (table:
`output/ablations/rq6.md`, `paper/tables/rq6.tex`). No manifest: 62 types, 21% of citations
relabelled (1.5% with it). No citation requirement: 39 types, recall of the main run 0.36. No
definitions block: 111 types, precision 0.57. Effort low: 46 types. Model repeats: Haiku 76
(judged agreement 0.60), Sonnet medium 54 (0.52), Sonnet high 72 truncated (0.57). RQ6 cost $1.55.

### RQ7: Web-sourced token descriptions (`taxonomy/rq7/`)

378 CoinGecko token descriptions classified into the site's own 28 categories (independent gold).
As prompt context the catalogue does not raise an LLM classifier (micro-F1 0.570 vs 0.571
without it). The ontology tags alone, without the description, reach 0.535; as features for
logistic regression 432 tag indicators match 8,334 TF-IDF features on micro-F1 and beat them on
macro-F1 (0.40 vs 0.26); words + tags is best (0.51 / 0.42). Table `output/rq7/rq7.md`,
`paper/tables/rq7.tex`, failure cases `output/rq7/failure_cases.md`. RQ7 cost $1.73.

## Setup

```bash
chmod +x setup_repo.sh
./setup_repo.sh
. venv/bin/activate
cp .env.example .env   # fill in ANTHROPIC_API_KEY (and HPC_* / SMTP_* if used)
```

`setup_repo.sh` creates a local `venv/`, installs `requirements.txt`, and drops a
`.pth` file into the venv so `import taxonomy` works from anywhere once the venv
is active. There is no `pyproject.toml`; the package lives flat at the repo root.
`pdftotext` (poppler) must be on PATH to rebuild the corpus.

## Layout

```
legal/                     21 source PDFs (EU, UK, US, FATF, Basel, FSB, IOSCO, UN, CoE)
context/                   3 taxonomy papers (PDF) + taxonomy_corpus.txt (derived, API-ready)
taxonomy/
  llm_context.py           shared Claude client + cached-corpus request builder
  corpus/                  PDF extraction spec and corpus builder
  establishment/           Part 1: prompts, Task A/B runners, DAG metrics, dashboard
  classification/          Part 2: sampler, prompts, Task C tagging, maintenance, evolution
  retrieval/               Part 3: DAG index, graph structures, query engine, benchmark
  evaluation/              gold set, tagging F1 with baselines, retrieval P@k / NDCG@k
  baselines/               RQ5: zero-shot, chunked RAG, RAPTOR, TnT-LLM catalogues, expert key, comparison
                           RQ6: Task A ablations (ablate.py, rq6.py)
  rq7/                     RQ7: CoinGecko descriptions, site categories, LLM and supervised classifiers
data/dlt_corpus/           downloaded DLT-Corpus shards and the pilot sample (gitignored)
output/
  establishment/           Part 1 results: term types, is-a distributions, DAG, metrics, viewer
  classification/          Part 2 pilot outputs (superseded by evolution/iter_01)
  evolution/               v0 seed, v1.. evolved catalogues, iter_XX batches, evolution log
  retrieval/               Part 3: index summary, benchmark (index.pkl is rebuilt, not committed)
  evaluation/              gold set, predictions per run, tagging and retrieval results
  baselines/, ablations/   RQ5 baseline catalogues and RQ6 ablation runs with their tables
  rq7/                     RQ7 dataset (coins, items, labels), predictions, tables
paper/                     the write-up (LaTeX)
```
