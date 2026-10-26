# Billing

Usage recorded by each runner, priced at list rates (USD). Haiku 5.5 long-prompt card for Task A and Task B.

| stage | model | input | cache read | cache write | output | USD | seconds | note |
|---|---|---|---|---|---|---|---|---|
| Task A term types (run 1) | claude-haiku-5-5 | 2,542 | 235,298 | 0 | 85,729 | 0.23 | 302.1 | high effort, 1 streamed call |
| Task A term types (haiku_run2) | claude-haiku-5-5 | 2,542 | 0 | 234,945 | 72,645 | 0.42 | 257.0 | repeat |
| Task A term types (sonnet) | claude-sonnet-5-5 | 2,542 | 0 | 234,946 | 127,000 | 2.21 | 701.3 | repeat |
| Task A term types (sonnet_medium) | claude-sonnet-5-5 | 2,542 | 234,946 | 0 | 34,648 | 0.40 | 173.7 | repeat |
| Task B is-a distributions | claude-haiku-5-5 | 196,567 | 23,331,933 | 0 | 68,156 | 1.44 | 104.3 | 93 calls |
| Iteration 1: tag 300 items + discovery + consolidation | claude-haiku-5-5 | 319,014 | 7,229,700 | 0 | 99,719 | 0.15 | 107.1 | tagging $0.1413, discovery $0.0107, consolidation $0.0021 |
| Iteration 2: tag 8646 items + discovery + consolidation | claude-haiku-5-5 | 6,980,250 | 215,995,325 | 0 | 2,858,174 | 4.29 | 2023.9 | tagging $4.2509, discovery $0.0357, consolidation $0.0036 |
| Iteration 3: tag 8646 items + discovery + consolidation | claude-haiku-5-5 | 6,940,563 | 230,709,115 | 0 | 2,897,818 | 4.45 | 742.6 | tagging $4.415, discovery $0.0356, consolidation $0.0028 |
| Iteration 4: tag 8646 items + discovery + consolidation | claude-haiku-5-5 | 6,982,643 | 242,630,570 | 0 | 2,923,586 | 4.59 | 789.5 | tagging $4.544, discovery $0.0425, consolidation $0.0034 |
| Iteration 5: tag 8646 items + discovery + consolidation | claude-haiku-5-5 | 7,033,233 | 258,407,695 | 0 | 2,878,424 | 4.73 | 762.0 | tagging $4.678, discovery $0.0485, consolidation $0.0039 |
| Iteration 6: tag 1818 items + discovery + consolidation | claude-haiku-5-5 | 1,732,478 | 57,355,422 | 0 | 635,959 | 1.07 | 175.4 | tagging $1.0366, discovery $0.0302, consolidation $0.0019 |
| Gold annotation: 300 items x 2 passes | claude-opus-5-5 | 467,944 | 19,317,151 | 32,249 | 545,111 | 20.76 | 882.2 | high effort, adaptive thinking |
| Evaluation: dag run 1 (300 items) | claude-haiku-5-5 | 233,972 | 9,623,913 | 32,187 | 103,640 | 0.18 | 43.4 |  |
| Evaluation: dag run 2 (300 items) | claude-haiku-5-5 | 233,972 | 9,656,100 | 0 | 102,543 | 0.17 | 45.9 |  |
| Evaluation: dag run 3 (300 items) | claude-haiku-5-5 | 233,972 | 9,656,100 | 0 | 104,664 | 0.17 | 42.8 |  |
| Evaluation: flat run 1 (300 items) | claude-haiku-5-5 | 233,972 | 2,604,888 | 8,712 | 117,243 | 0.11 | 41.6 |  |
| Evaluation: flat run 2 (300 items) | claude-haiku-5-5 | 233,972 | 2,613,600 | 0 | 119,288 | 0.11 | 45.2 |  |
| Evaluation: flat run 3 (300 items) | claude-haiku-5-5 | 233,972 | 2,613,600 | 0 | 118,220 | 0.11 | 42.6 |  |
| Evaluation: dag@claude-sonnet-5-5 run 1 (300 items) | claude-sonnet-5-5 | 233,972 | 9,624,212 | 32,188 | 76,129 | 3.28 | 55.6 |  |
| Evaluation: dag@claude-sonnet-5-5 run 2 (300 items) | claude-sonnet-5-5 | 233,972 | 9,656,400 | 0 | 76,032 | 3.16 | 50.7 |  |
| Evaluation: dag@claude-sonnet-5-5 run 3 (300 items) | claude-sonnet-5-5 | 233,972 | 9,656,400 | 0 | 76,956 | 3.17 | 49.1 |  |
| Evaluation: flat@claude-sonnet-5-5 run 1 (300 items) | claude-sonnet-5-5 | 233,972 | 2,605,187 | 8,713 | 85,057 | 1.87 | 59.0 |  |
| Evaluation: flat@claude-sonnet-5-5 run 2 (300 items) | claude-sonnet-5-5 | 233,972 | 2,613,900 | 0 | 82,885 | 1.82 | 51.3 |  |
| Evaluation: flat@claude-sonnet-5-5 run 3 (300 items) | claude-sonnet-5-5 | 233,972 | 2,613,900 | 0 | 83,947 | 1.83 | 51.1 |  |

**Total: $60.72**
