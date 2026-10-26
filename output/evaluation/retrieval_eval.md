# Retrieval evaluation

Judged collection: 300 gold items; 110 queries ({'value': 60, 'node': 30, 'and': 20}); k = 10; 3 runs (mean ± sd over runs; each run uses that run's tag predictions). Latency is the mean per query on the judged collection; the full-index latency on 33581 items is in output/retrieval/benchmark.md.

| system | P@5 | P@10 | R@10 | NDCG@10 | MAP | NDCG@10 value q | node q | AND q | latency (us) |
|---|---|---|---|---|---|---|---|---|---|
| DAG index (ours, Haiku 5.5 tags) | 0.393 ± 0.029 | 0.292 ± 0.012 | 0.268 ± 0.012 | 0.413 ± 0.028 | 0.229 ± 0.016 | 0.427 ± 0.027 | 0.546 ± 0.043 | 0.169 ± 0.016 | 27 |
| DAG index (Sonnet 5.5 tags) | 0.559 ± 0.008 | 0.409 ± 0.003 | 0.395 ± 0.008 | 0.596 ± 0.011 | 0.373 ± 0.012 | 0.624 ± 0.011 | 0.723 ± 0.010 | 0.321 ± 0.025 | 24 |
| flat zero-shot tags, no closure | 0.342 ± 0.020 | 0.233 ± 0.013 | 0.260 ± 0.017 | 0.393 ± 0.016 | 0.225 ± 0.013 | 0.447 ± 0.009 | 0.368 ± 0.034 | 0.268 ± 0.023 | 303 |
| flat zero-shot tags, no closure (Sonnet 5.5) | 0.479 ± 0.009 | 0.316 ± 0.006 | 0.385 ± 0.008 | 0.539 ± 0.009 | 0.362 ± 0.006 | 0.649 ± 0.005 | 0.420 ± 0.027 | 0.384 ± 0.042 | 282 |
| supervised labels + DAG index | 0.315 ± 0.003 | 0.234 ± 0.001 | 0.173 ± 0.004 | 0.308 ± 0.006 | 0.145 ± 0.006 | 0.312 ± 0.007 | 0.372 ± 0.006 | 0.199 ± 0.008 | 25 |
| BM25 over text | 0.262 ± 0.000 | 0.226 ± 0.000 | 0.259 ± 0.000 | 0.313 ± 0.000 | 0.140 ± 0.000 | 0.369 ± 0.000 | 0.281 ± 0.000 | 0.194 ± 0.000 | 587 |
