# Retrieval evaluation

Judged collection: 12 gold items; 27 queries ({'value': 4, 'node': 3, 'and': 20}); k = 10; 1 runs (mean ± sd over runs; each run uses that run's tag predictions). Latency is the mean per query on the judged collection; the full-index latency on 8205 items is in output/retrieval/benchmark.md.

| system | P@5 | P@10 | R@10 | NDCG@10 | MAP | NDCG@10 value q | node q | AND q | latency (us) |
|---|---|---|---|---|---|---|---|---|---|
| DAG index (ours) | 0.141 ± 0.000 | 0.070 ± 0.000 | 0.144 ± 0.000 | 0.173 ± 0.000 | 0.139 ± 0.000 | 0.566 ± 0.000 | 0.803 ± 0.000 | 0.000 ± 0.000 | 8 |
| flat zero-shot tags, no closure | 0.052 ± 0.000 | 0.026 ± 0.000 | 0.056 ± 0.000 | 0.071 ± 0.000 | 0.056 ± 0.000 | 0.435 ± 0.000 | 0.063 ± 0.000 | 0.000 ± 0.000 | 22 |
| supervised labels + DAG index | 0.370 ± 0.000 | 0.189 ± 0.000 | 0.515 ± 0.000 | 0.612 ± 0.000 | 0.502 ± 0.000 | 0.829 ± 0.000 | 0.678 ± 0.000 | 0.558 ± 0.000 | 10 |
| BM25 over text | 0.370 ± 0.000 | 0.289 ± 0.000 | 0.810 ± 0.000 | 0.746 ± 0.000 | 0.608 ± 0.000 | 0.819 ± 0.000 | 0.744 ± 0.000 | 0.732 ± 0.000 | 36 |
