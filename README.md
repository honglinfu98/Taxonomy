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
| **1. Taxonomy** | Establish the graph from a grounded corpus of legal instruments and academic taxonomies. | **in progress (this repo)** |
| **2. Classification** | Tag incoming content (documents, transactions, news, code) with taxonomy nodes; serve retrieval by node. | not started |
| **3. Optimization** | Keep the graph self-maintaining: merge / split / prune nodes from classification feedback and retrieval usage, ingest new sources, re-verify citations. | not started |

## Part 1: taxonomy establishment

The LLM (Claude, default `claude-haiku-5-5`) is fed one fixed context, the
**taxonomy corpus** (`context/taxonomy_corpus.txt`), built from 21 legal PDFs in
`legal/` and three taxonomy papers in `context/`. The corpus (~235K tokens) sits behind a
1-hour prompt-cache breakpoint, so each task is a cheap query on top of the same context.

| Task | Question to the LLM | Output |
|---|---|---|
| **A. Term type generation** (done 2026-10-26) | Which *classification dimensions* (term types) does the corpus use, explicitly or implicitly, to classify assets, technologies, actors, activities and obligations? Every dimension and value must cite `[doc index, section label]` with a verbatim quote. | `output/term_types.json`: 93 term types, 480 citations, 98% verified against the corpus (`output/term_types.verification.json`) |
| **B. Is-a hierarchy** (done 2026-10-26) | For each term type X, over the other term types Y in its category: how probable is it that *X is-a Y* (Y is the more general dimension X specialises)? Answer is a probability distribution over candidate parents plus `none` (top-level), each entry with rationale and citations. Context = the same corpus plus the Task A catalogue. | `output/taxonomy_dag.json` (the DAG: 93 nodes, 55 is-a edges at threshold 0.4, with metrics), `output/is_a.md` (tree view), `output/is_a.json` (all distributions), `output/dag_metrics.json` (metrics across thresholds), dashboard `output/is_a_dashboard.html` |

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
python -m taxonomy.build_corpus      # rebuild context/taxonomy_corpus.txt from the PDFs
python -m taxonomy.term_types        # Task A -> output/term_types.json
python -m taxonomy.is_a              # Task B -> output/is_a.json, taxonomy_dag.json, dag_metrics.json
python -m taxonomy.dashboard         # interactive DAG viewer -> output/is_a_dashboard.html
```

`taxonomy/README.md` documents the package (corpus construction, API helpers,
prompts, runners).

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
legal/        21 source PDFs (EU, UK, US, FATF, Basel, FSB, IOSCO, UN, CoE)
context/      3 taxonomy papers (PDF) + taxonomy_corpus.txt (derived, API-ready)
taxonomy/     the package: corpus builder, API helpers, prompts, task runners
output/       task results (JSON) and verification reports
paper/        the write-up (LaTeX)
```
