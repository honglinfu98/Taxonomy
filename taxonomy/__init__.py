"""taxonomy — flat package at the repo root; made importable by setup_repo.sh.

Modules:
  sources       what to take from each PDF (line ranges / regex markers + metadata)
  pdf_text      pdftotext wrapper, range selection, noise removal
  build_corpus  entry point: `python -m taxonomy.build_corpus` -> context/taxonomy_corpus.txt
  llm_context   client() from .env; build_request(...) kwargs with the corpus cached
  prompts       system instructions + per-task prompts (Task A term types, Task B is-a)
  dag_metrics   information gain / AUC / effective-leaf metrics on the is-a DAG
  dashboard     entry point: `python -m taxonomy.dashboard` -> output/is_a_dashboard.html
  is_a          entry point: `python -m taxonomy.is_a` -> output/is_a.json (is-a distributions)
  term_types    entry point: `python -m taxonomy.term_types` -> output/term_types.json (+ citation verification)
"""

__version__ = "0.1.0"
