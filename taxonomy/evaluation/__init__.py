"""Evaluation of tagging and retrieval against a held-out gold set.

    python -m taxonomy.evaluation.gold select        # held-out items
    python -m taxonomy.evaluation.gold annotate      # two-pass strong-model annotation, adjudicated
    python -m taxonomy.evaluation.tagging_eval       # Micro/Macro-F1: DAG-guided LLM, zero-shot flat LLM, supervised; 3 runs
    python -m taxonomy.evaluation.retrieval_eval     # P@k, NDCG@k, latency on judged queries; DAG index vs BM25 vs flat tags
"""
