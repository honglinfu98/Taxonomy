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
| RQ5 baseline catalogue: zeroshot | claude-haiku-5-5 | 2,575 | 0 | 0 | 13,538 | 0.01 | 53.7 | 1 calls |
| RQ5 Task B over zeroshot | claude-haiku-5-5 | 36,595 | 7,430,948 | 239,708 | 25,209 | 0.69 | 49.7 | 32 calls |
| RQ5 baseline catalogue: rag | claude-haiku-5-5 | 69,004 | 0 | 664,803 | 354,791 | 0.27 | 221.7 | 42 calls |
| RQ5 Task B over rag | claude-haiku-5-5 | 178,035 | 21,153,106 | 26,531 | 61,282 | 1.33 | 101.2 | 81 calls |
| RQ5 baseline catalogue: raptor | claude-haiku-5-5 | 320,148 | 17,302 | 578,904 | 338,716 | 0.27 | 237.8 | 74 calls |
| RQ5 Task B over raptor | claude-haiku-5-5 | 132,067 | 16,665,730 | 21,785 | 49,909 | 1.05 | 81.4 | 65 calls |
| RQ5 baseline catalogue: tnt | claude-haiku-5-5 | 472,617 | 0 | 0 | 243,491 | 0.17 | 650.0 | 135 calls |
| RQ5 Task B over tnt | claude-haiku-5-5 | 441,980 | 43,745,686 | 22,514 | 115,903 | 2.72 | 131.2 | 170 calls |
| RQ5 baseline catalogue: expert_key | claude-haiku-5-5 | 669 | 57,817 | 0 | 15,642 | 0.01 | 51.6 | 2 calls |
| RQ5 downstream: ours run 1 (300 items) | claude-haiku-5-5 | 233,972 | 6,163,586 | 20,614 | 97,344 | 0.14 | 105.4 |  |
| RQ5 downstream: ours run 2 (300 items) | claude-haiku-5-5 | 233,972 | 6,184,200 | 0 | 95,570 | 0.13 | 102.9 |  |
| RQ5 downstream: ours run 3 (300 items) | claude-haiku-5-5 | 233,972 | 6,184,200 | 0 | 99,183 | 0.13 | 98.2 |  |
| RQ5 downstream: rag run 1 (300 items) | claude-haiku-5-5 | 233,972 | 11,928,605 | 39,895 | 93,893 | 0.19 | 110.6 |  |
| RQ5 downstream: rag run 2 (300 items) | claude-haiku-5-5 | 233,972 | 11,968,500 | 0 | 97,177 | 0.19 | 110.9 |  |
| RQ5 downstream: rag run 3 (300 items) | claude-haiku-5-5 | 233,972 | 11,968,500 | 0 | 95,615 | 0.19 | 103.4 |  |
| RQ5 judge: map rag to gold | claude-haiku-5-5 | 46,080 | 0 | 0 | 6,171 | 0.01 | 22.1 |  |
| RQ5 downstream: raptor run 1 (300 items) | claude-haiku-5-5 | 233,972 | 9,642,451 | 32,249 | 95,255 | 0.17 | 112.4 |  |
| RQ5 downstream: raptor run 2 (300 items) | claude-haiku-5-5 | 233,972 | 9,674,700 | 0 | 94,618 | 0.17 | 109.6 |  |
| RQ5 downstream: raptor run 3 (300 items) | claude-haiku-5-5 | 233,972 | 9,674,700 | 0 | 95,489 | 0.17 | 102.9 |  |
| RQ5 judge: map raptor to gold | claude-haiku-5-5 | 42,610 | 0 | 0 | 4,987 | 0.01 | 18.1 |  |
| RQ5 downstream: tnt run 1 (300 items) | claude-haiku-5-5 | 233,972 | 7,764,731 | 25,969 | 110,856 | 0.16 | 85.5 |  |
| RQ5 downstream: tnt run 2 (300 items) | claude-haiku-5-5 | 233,972 | 7,790,700 | 0 | 109,316 | 0.16 | 83.6 |  |
| RQ5 downstream: tnt run 3 (300 items) | claude-haiku-5-5 | 233,972 | 7,790,700 | 0 | 111,500 | 0.16 | 86.3 |  |
| RQ5 judge: map tnt to gold | claude-haiku-5-5 | 53,772 | 0 | 0 | 9,509 | 0.01 | 34.1 |  |
| RQ5 downstream: zeroshot run 1 (300 items) | claude-haiku-5-5 | 233,972 | 1,749,449 | 5,851 | 98,878 | 0.09 | 99.3 |  |
| RQ5 downstream: zeroshot run 2 (300 items) | claude-haiku-5-5 | 233,972 | 1,755,300 | 0 | 100,838 | 0.09 | 105.2 |  |
| RQ5 downstream: zeroshot run 3 (300 items) | claude-haiku-5-5 | 233,972 | 1,755,300 | 0 | 97,771 | 0.09 | 96.1 |  |
| RQ5 judge: map zeroshot to gold | claude-haiku-5-5 | 33,344 | 0 | 0 | 2,699 | 0.00 | 12.2 |  |
| RQ6 judge: expert_key vs effort_low | claude-haiku-5-5 | 14,916 | 0 | 0 | 2,034 | 0.00 | 7.9 |  |
| RQ6 judge: expert_key vs no_citations | claude-haiku-5-5 | 13,800 | 0 | 0 | 1,767 | 0.00 | 6.6 |  |
| RQ6 judge: expert_key vs no_definitions | claude-haiku-5-5 | 29,972 | 0 | 0 | 3,077 | 0.00 | 11.6 |  |
| RQ6 judge: expert_key vs no_manifest | claude-haiku-5-5 | 18,912 | 0 | 0 | 3,781 | 0.00 | 12.1 |  |
| RQ5 judge: expert_key vs ours | claude-haiku-5-5 | 25,476 | 0 | 0 | 2,411 | 0.00 | 10.9 |  |
| RQ5 judge: expert_key vs rag | claude-haiku-5-5 | 24,266 | 0 | 0 | 2,759 | 0.00 | 9.2 |  |
| RQ5 judge: expert_key vs raptor | claude-haiku-5-5 | 20,796 | 0 | 0 | 2,196 | 0.00 | 7.8 |  |
| RQ5 judge: expert_key vs repeat | claude-haiku-5-5 | 23,406 | 0 | 0 | 2,221 | 0.00 | 7.8 |  |
| RQ6 judge: expert_key vs sonnet | claude-haiku-5-5 | 19,902 | 0 | 0 | 2,698 | 0.00 | 9.5 |  |
| RQ6 judge: expert_key vs sonnet_medium | claude-haiku-5-5 | 14,000 | 0 | 0 | 2,309 | 0.00 | 8.0 |  |
| RQ5 judge: expert_key vs tnt | claude-haiku-5-5 | 31,958 | 0 | 0 | 2,731 | 0.00 | 9.9 |  |
| RQ5 judge: expert_key vs zeroshot | claude-haiku-5-5 | 11,530 | 0 | 0 | 1,597 | 0.00 | 6.0 |  |
| RQ6 judge: ours vs effort_low | claude-haiku-5-5 | 28,006 | 0 | 0 | 3,840 | 0.00 | 14.4 |  |
| RQ6 judge: ours vs no_citations | claude-haiku-5-5 | 26,890 | 0 | 0 | 3,443 | 0.00 | 12.6 |  |
| RQ6 judge: ours vs no_definitions | claude-haiku-5-5 | 43,062 | 0 | 0 | 8,433 | 0.01 | 26.8 |  |
| RQ6 judge: ours vs no_manifest | claude-haiku-5-5 | 32,002 | 0 | 0 | 6,157 | 0.01 | 18.5 |  |
| RQ5 judge: ours vs rag | claude-haiku-5-5 | 37,356 | 0 | 0 | 5,658 | 0.01 | 17.8 |  |
| RQ5 judge: ours vs raptor | claude-haiku-5-5 | 33,886 | 0 | 0 | 4,555 | 0.01 | 16.5 |  |
| RQ5 judge: ours vs repeat | claude-haiku-5-5 | 36,496 | 0 | 0 | 5,394 | 0.01 | 18.9 |  |
| RQ6 judge: ours vs sonnet | claude-haiku-5-5 | 32,992 | 0 | 0 | 5,102 | 0.01 | 16.6 |  |
| RQ6 judge: ours vs sonnet_medium | claude-haiku-5-5 | 27,090 | 0 | 0 | 4,689 | 0.01 | 16.2 |  |
| RQ5 judge: ours vs tnt | claude-haiku-5-5 | 45,048 | 0 | 0 | 8,119 | 0.01 | 29.1 |  |
| RQ5 judge: ours vs zeroshot | claude-haiku-5-5 | 24,620 | 0 | 0 | 2,343 | 0.00 | 8.4 |  |
| RQ6 ablation: effort_low | claude-haiku-5-5 | 2,542 | 0 | 234,945 | 41,636 | 0.34 | 142.0 | full prompt at effort low |
| RQ6 ablation: no_citations | claude-haiku-5-5 | 2,443 | 0 | 234,830 | 27,266 | 0.30 | 111.4 | grounding rules and citation fields removed (no citation requirement) |
| RQ6 ablation: no_definitions | claude-haiku-5-5 | 2,542 | 0 | 234,675 | 94,578 | 0.47 | 320.3 | definitions of term, term type and grounded removed from the instructions |
| RQ6 ablation: no_manifest | claude-haiku-5-5 | 699 | 0 | 234,945 | 53,113 | 0.37 | 195.6 | task prompt without the manifest of section labels |
| RQ7 classify onto run 1 (378 items) | claude-haiku-5-5 | 145,620 | 12,119,042 | 32,146 | 126,718 | 0.20 | 101.6 |  |
| RQ7 classify onto run 2 (378 items) | claude-haiku-5-5 | 145,620 | 12,151,188 | 0 | 128,029 | 0.20 | 104.3 |  |
| RQ7 classify onto run 3 (378 items) | claude-haiku-5-5 | 145,620 | 12,151,188 | 0 | 125,602 | 0.20 | 102.3 |  |
| RQ7 tagger (catalogue v6) run 1 (378 items) | claude-haiku-5-5 | 232,565 | 12,134,499 | 32,187 | 223,584 | 0.26 | 139.0 |  |
| RQ7 classify tags run 1 (378 items) | claude-haiku-5-5 | 737,768 | 0 | 0 | 18,234 | 0.08 | 196.3 |  |
| RQ7 tagger (catalogue v6) run 2 (378 items) | claude-haiku-5-5 | 232,565 | 12,166,686 | 0 | 219,868 | 0.25 | 138.7 |  |
| RQ7 classify tags run 2 (378 items) | claude-haiku-5-5 | 729,545 | 0 | 0 | 18,282 | 0.08 | 189.7 |  |
| RQ7 tagger (catalogue v6) run 3 (378 items) | claude-haiku-5-5 | 232,565 | 12,166,686 | 0 | 222,613 | 0.26 | 133.8 |  |
| RQ7 classify tags run 3 (378 items) | claude-haiku-5-5 | 736,378 | 0 | 0 | 18,623 | 0.08 | 186.4 |  |
| RQ7 classify text run 1 (378 items) | claude-haiku-5-5 | 281,700 | 0 | 0 | 20,159 | 0.04 | 50.8 |  |
| RQ7 classify text run 2 (378 items) | claude-haiku-5-5 | 281,700 | 0 | 0 | 20,076 | 0.04 | 51.6 |  |
| RQ7 classify text run 3 (378 items) | claude-haiku-5-5 | 281,700 | 0 | 0 | 20,239 | 0.04 | 53.1 |  |

**Total: $72.82**
