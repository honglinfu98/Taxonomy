# Tagging evaluation

Gold: 300 items, 1168 labels (3.89 per item), 209 distinct (term type, value) labels over 84 term types; catalogue v6; 3 runs per system (mean ± sd).

| system | label micro-F1 | label macro-F1 | label P | label R | type micro-F1 | type macro-F1 | tags/item | cost/run | wall/run |
|---|---|---|---|---|---|---|---|---|---|
| DAG-guided LLM (ours, Haiku 5.5) | 0.379 ± 0.006 | 0.316 ± 0.002 | 0.364 ± 0.003 | 0.394 ± 0.008 | 0.493 ± 0.005 | 0.390 ± 0.005 | 4.21 ± 0.06 | $0.17 | 44 s |
| zero-shot LLM, flat labels (Haiku 5.5) | 0.387 ± 0.009 | 0.321 ± 0.012 | 0.347 ± 0.010 | 0.439 ± 0.006 | 0.485 ± 0.006 | 0.388 ± 0.020 | 4.92 ± 0.08 | $0.11 | 43 s |
| supervised TF-IDF + LR | 0.388 ± 0.003 | 0.160 ± 0.002 | 0.371 ± 0.005 | 0.406 ± 0.002 | 0.482 ± 0.002 | 0.203 ± 0.001 | 4.26 ± 0.06 | $0.00 | 45 s |
| DAG-guided LLM (Sonnet 5.5) | 0.595 ± 0.004 | 0.505 ± 0.008 | 0.673 ± 0.003 | 0.532 ± 0.005 | 0.658 ± 0.006 | 0.544 ± 0.009 | 3.08 ± 0.03 | $3.20 | 52 s |
| zero-shot LLM, flat labels (Sonnet 5.5) | 0.593 ± 0.006 | 0.518 ± 0.002 | 0.651 ± 0.006 | 0.545 ± 0.007 | 0.668 ± 0.009 | 0.540 ± 0.003 | 3.26 ± 0.04 | $1.84 | 54 s |

## Per category (label micro-F1, mean ± sd)

| system | asset | technology | actor | activity | obligation_or_risk |
|---|---|---|---|---|---|
| DAG-guided LLM (ours, Haiku 5.5) | 0.345 ± 0.019 | 0.397 ± 0.009 | 0.138 ± 0.079 | 0.129 ± 0.051 | 0.472 ± 0.108 |
| zero-shot LLM, flat labels (Haiku 5.5) | 0.317 ± 0.025 | 0.427 ± 0.012 | 0.158 ± 0.028 | 0.222 ± 0.031 | 0.307 ± 0.062 |
| supervised TF-IDF + LR | 0.303 ± 0.006 | 0.420 ± 0.003 | 0.131 ± 0.002 | 0.000 ± 0.000 | 0.063 ± 0.055 |
| DAG-guided LLM (Sonnet 5.5) | 0.527 ± 0.012 | 0.611 ± 0.003 | 0.481 ± 0.028 | 0.420 ± 0.070 | 0.727 ± 0.025 |
| zero-shot LLM, flat labels (Sonnet 5.5) | 0.501 ± 0.027 | 0.610 ± 0.005 | 0.464 ± 0.010 | 0.524 ± 0.033 | 0.614 ± 0.030 |

Gold labels are adjudicated from two independent passes of claude-opus-5-5 (pass agreement micro-F1 0.8832); no human labels.
