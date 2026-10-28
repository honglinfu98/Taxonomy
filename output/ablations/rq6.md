# RQ6: how much do the manifest, grounding strategy, prompt and model matter?

Each row is one Task A run over the same cached corpus that differs from the main run in one ingredient. Judge: claude-haiku-5-5 (same-question matching, both directions, intersection). Expert key: the 39 dimensions of the two taxonomy papers in the corpus (contaminated: both papers are in the corpus).

| variant | group | term types | values | citations verified | section label exact | agreement with main run: lexical F1 | judged F1 (recall of main / precision) | expert coverage (precision) | cost | time |
|---|---|---|---|---|---|---|---|---|---|---|
| full prompt, Haiku 5.5, effort high (main run) | reference | 93 | 317 | 470/480 (98%) | 0.965 | 1 (self) | 1 (self) | 0.667 (0.280) | $0.23 | 302 s |
| same prompt, Haiku 5.5, second run | model | 76 | 260 | 387/399 (97%) | 0.962 | 0.509 | 0.604 (0.548 / 0.671) | 0.667 (0.342) | $0.42 | 257 s |
| same prompt, Sonnet 5.5, effort medium | model | 54 | 210 | 264/264 (100%) | 1.000 | 0.395 | 0.517 (0.409 / 0.704) | 0.590 (0.426) | $0.40 | 174 s |
| same prompt, Sonnet 5.5, effort high (truncated at the output limit) | model | 72 | 308 | 414/414 (100%) | 1.000 | 0.545 | 0.570 (0.505 / 0.653) | 0.821 (0.444) | $2.21 | 701 s |
| same prompt, Haiku 5.5, effort low | prompt | 46 | 165 | 211/211 (100%) | 0.986 | 0.403 | 0.532 (0.398 / 0.804) | 0.538 (0.457) | $0.34 | 142 s |
| no manifest of section labels | manifest | 62 | 209 | 265/271 (98%) | 0.768 | 0.439 | 0.645 (0.538 / 0.806) | 0.718 (0.452) | $0.37 | 196 s |
| no definitions of term, term type, grounded | prompt | 111 | 303 | 412/414 (100%) | 0.988 | 0.422 | 0.618 (0.677 / 0.568) | 0.821 (0.288) | $0.47 | 320 s |
| no citation requirement | grounding | 39 | 193 | none | - | 0.439 | 0.500 (0.355 / 0.846) | 0.436 (0.436) | $0.30 | 111 s |

Columns: citations verified = Task A verifier (document and section exist, quote verbatim); section label exact = share of citations whose section label needed no relabelling; agreement = same-question matches with the main run; expert coverage = share of the key's dimensions matched (precision = share of the variant's types that match a key dimension). Cost at the Haiku long-prompt card (Sonnet at its list card).
