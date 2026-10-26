# Billing

Usage recorded by each runner, priced at list rates (USD). Haiku 5.5 long-prompt card for Task A and Task B.

| stage | model | input | cache read | cache write | output | USD | seconds | note |
|---|---|---|---|---|---|---|---|---|
| Task A term types (run 1) | claude-haiku-5-5 | 2,542 | 235,298 | 0 | 85,729 | 0.23 | 302.1 | high effort, 1 streamed call |
| Task B is-a distributions | claude-haiku-5-5 | 196,567 | 23,331,933 | 0 | 68,156 | 1.44 | 104.3 | 93 calls |
| Iteration 1: tag 300 items + discovery + consolidation | claude-haiku-5-5 | 319,014 | 7,229,700 | 0 | 99,719 | 0.15 | 107.1 | tagging $0.1413, discovery $0.0107, consolidation $0.0021 |
| Iteration 2: tag 8646 items + discovery + consolidation | claude-haiku-5-5 | 6,980,250 | 215,995,325 | 0 | 2,858,174 | 4.29 | 2023.9 | tagging $4.2509, discovery $0.0357, consolidation $0.0036 |
| Iteration 3: tag 8646 items + discovery + consolidation | claude-haiku-5-5 | 6,940,563 | 230,709,115 | 0 | 2,897,818 | 4.45 | 742.6 | tagging $4.415, discovery $0.0356, consolidation $0.0028 |
| Iteration 4: tag 8646 items + discovery + consolidation | claude-haiku-5-5 | 6,982,643 | 242,630,570 | 0 | 2,923,586 | 4.59 | 789.5 | tagging $4.544, discovery $0.0425, consolidation $0.0034 |
| Gold annotation: 12 items x 2 passes | claude-opus-5-5 | 19,098 | 562,560 | 112,512 | 20,964 | 1.62 | 55.6 | high effort, adaptive thinking |
| Evaluation: dag run 1 (12 items) | claude-haiku-5-5 | 9,549 | 336,792 | 0 | 3,956 | 0.01 | 7.5 |  |
| Evaluation: flat run 1 (12 items) | claude-haiku-5-5 | 9,549 | 55,488 | 27,744 | 4,695 | 0.01 | 8.5 |  |

**Total: $16.78**
