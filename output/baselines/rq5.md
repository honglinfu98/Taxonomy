# RQ5: our catalogue against expert taxonomies and LLM baselines

All catalogues from Haiku 5.5 on the same 24-document corpus (zero-shot sees only the document titles). Judge: claude-haiku-5-5, same-question matching in both directions, intersection. Expert key: the 39 dimensions of the two taxonomy papers in the corpus (docs 1 and 2); contaminated for every corpus-based catalogue.

| catalogue | term types | values | citations verified | agreement with ours, lexical F1 | judged F1 (recall of ours / precision) | expert coverage (precision) | bits/descent | AUC | eff. leaves | downstream type micro-F1 | macro-F1 | cost | time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ours (whole corpus, one context) | 93 | 317 | 470/480 (98%) | 1 (self) | 1 (self) | 0.667 (0.280) | 4.72 | 0.835 | 14.0 | 0.340 ± 0.007 | 0.195 ± 0.017 | $0.23 | 302 s |
| ours, second run | 76 | 260 | 387/399 (97%) | 0.509 | 0.604 (0.548 / 0.671) | 0.667 (0.342) | - | - | - | - | - | $0.42 | 257 s |
| zero-shot, no corpus | 32 | 102 | none | 0.176 | 0.304 (0.204 / 0.594) | 0.256 (0.312) | 3.61 | 0.621 | 5.0 | 0.203 ± 0.002 | 0.054 ± 0.001 | $0.01 | 54 s |
| chunked RAG (BM25, k=8) | 81 | 750 | 1431/1439 (99%) | 0.483 | 0.471 (0.441 / 0.506) | 0.590 (0.284) | 4.27 | 0.850 | 12.3 | 0.238 ± 0.002 | 0.111 ± 0.002 | $0.27 | 222 s |
| RAPTOR (tree + BM25, k=8) | 65 | 631 | 1185/1359 (87%) | 0.380 | 0.430 (0.366 / 0.523) | 0.564 (0.338) | 4.87 | 0.727 | 8.2 | 0.178 ± 0.009 | 0.082 ± 0.007 | $0.27 | 238 s |
| TnT-LLM (summarise, build, review) | 170 | 485 | none | 0.175 | 0.327 (0.462 / 0.253) | 0.769 (0.176) | 5.85 | 0.823 | 19.5 | 0.123 ± 0.006 | 0.079 ± 0.013 | $0.17 | 650 s |

Columns: citations verified = Task A verifier over every quote (doc, section, verbatim); agreement = same-question matches with our catalogue (lexical: agreement.py; judged: both directions, intersection); expert coverage = share of the key's dimensions matched (precision = share of the catalogue's types that match a key dimension); structure after the unchanged Task B; downstream = type-level F1 tagging the 300 gold items with the catalogue (no is-a edges), baseline types mapped to gold types by the judge, mean ± sd over 3 runs.
