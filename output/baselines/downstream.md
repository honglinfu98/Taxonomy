# Downstream tagging with each catalogue (gold term types, type level)

300 gold items; gold in catalogue v6 space; tagger Haiku 5.5, catalogue block without is-a edges; baseline term types mapped to gold term types by the LLM judge; mean ± sd over runs.

| catalogue | term types | mapped to gold | micro-F1 | macro-F1 | P | R | pred types/item | mapped share of predictions |
|---|---|---|---|---|---|---|---|---|
| ours | 93 | 93 | 0.340 ± 0.007 | 0.195 ± 0.017 | 0.331 ± 0.002 | 0.348 ± 0.013 | 3.63 ± 0.12 | 1.000 ± 0.000 |
| rag | 81 | 39 | 0.238 ± 0.002 | 0.111 ± 0.002 | 0.241 ± 0.005 | 0.235 ± 0.003 | 3.36 ± 0.10 | 0.723 ± 0.016 |
| raptor | 65 | 36 | 0.178 ± 0.009 | 0.082 ± 0.007 | 0.181 ± 0.008 | 0.176 ± 0.009 | 3.36 ± 0.06 | 0.660 ± 0.014 |
| tnt | 170 | 37 | 0.123 ± 0.006 | 0.079 ± 0.013 | 0.114 ± 0.006 | 0.133 ± 0.007 | 4.02 ± 0.06 | 0.486 ± 0.003 |
| zeroshot | 32 | 21 | 0.203 ± 0.002 | 0.054 ± 0.001 | 0.197 ± 0.002 | 0.209 ± 0.003 | 3.67 ± 0.03 | 0.714 ± 0.006 |
