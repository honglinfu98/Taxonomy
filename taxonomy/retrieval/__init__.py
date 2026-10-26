"""Part 3: optimisation. Index tagged content on the taxonomy DAG and retrieve it by graph
operations (reachability closure, weighted is-a paths, lowest common ancestors,
information content, facet gain) instead of flat text search.

    python -m taxonomy.retrieval.index        # build output/retrieval/index.pkl from all tagged iterations
    python -m taxonomy.retrieval.query ...    # evaluate a query, rank, suggest the next facet
    python -m taxonomy.retrieval.benchmark    # latency / navigation benchmark vs flat scans
"""
