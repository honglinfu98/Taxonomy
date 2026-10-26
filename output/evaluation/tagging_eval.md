# Tagging evaluation

Gold: 12 items, 50 labels (4.17 per item), 31 distinct (term type, value) labels over 18 term types; catalogue v3; 1 runs per system (mean ± sd).

| system | label micro-F1 | label macro-F1 | label P | label R | type micro-F1 | type macro-F1 | tags/item | cost/run | wall/run |
|---|---|---|---|---|---|---|---|---|---|
| DAG-guided LLM (ours) | 0.424 ± 0.000 | 0.419 ± 0.000 | 0.429 ± 0.000 | 0.420 ± 0.000 | 0.494 ± 0.000 | 0.451 ± 0.000 | 4.08 ± 0.00 | $0.01 | 8 s |
| zero-shot LLM, flat labels | 0.376 ± 0.000 | 0.416 ± 0.000 | 0.372 ± 0.000 | 0.380 ± 0.000 | 0.447 ± 0.000 | 0.448 ± 0.000 | 4.25 ± 0.00 | $0.01 | 8 s |
| supervised TF-IDF + LR | 0.444 ± 0.000 | 0.284 ± 0.000 | 0.449 ± 0.000 | 0.440 ± 0.000 | 0.486 ± 0.000 | 0.277 ± 0.000 | 4.08 ± 0.00 | $0.00 | 20 s |

## Per category (label micro-F1, mean ± sd)

| system | asset | technology | actor | activity | obligation_or_risk |
|---|---|---|---|---|---|
| DAG-guided LLM (ours) | 0.308 ± 0.000 | 0.458 ± 0.000 | - | 0.000 ± 0.000 | 0.000 ± 0.000 |
| zero-shot LLM, flat labels | 0.500 ± 0.000 | 0.342 ± 0.000 | - | 1.000 ± 0.000 | 0.000 ± 0.000 |
| supervised TF-IDF + LR | 0.182 ± 0.000 | 0.494 ± 0.000 | - | 0.000 ± 0.000 | 0.000 ± 0.000 |

Gold labels are adjudicated from two independent passes of claude-opus-5-5 (pass agreement micro-F1 0.9009); no human labels.
