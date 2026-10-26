"""taxonomy — flat package at the repo root; made importable by setup_repo.sh.

Subpackages (one per stage of the system; see README.md at the repo root):
  corpus          PDFs -> context/taxonomy_corpus.txt  (`python -m taxonomy.corpus.build_corpus`)
  establishment   Part 1, done: term types (Task A), is-a DAG (Task B), DAG metrics, dashboard
                  -> output/establishment/
  classification  Part 2, in progress: tag content with taxonomy nodes, retrieve by node
                  -> output/classification/
Shared:
  llm_context     client() from .env; build_request(...) with the corpus behind a cache breakpoint
"""

__version__ = "0.2.0"
