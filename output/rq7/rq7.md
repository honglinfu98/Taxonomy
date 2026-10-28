# RQ7: site categories from Web token descriptions, with and without the ontology

378 CoinGecko token descriptions (top coins by market cap with >= 40 words of description), 351 with at least one of the 28 retained site categories (categories carried by >= 10 items, ecosystem / index / portfolio / listing categories excluded). Gold = the site's own categories. LLM systems: Haiku 5.5, 3 runs, mean ± sd; supervised: 5-fold CV, 3 shuffles. Catalogue v6 (132 term types, 320 edges).

| system | micro-F1 | macro-F1 | P | R | pred/item | cost |
|---|---|---|---|---|---|---|
| LLM, description only (no ontology) | 0.571 ± 0.002 | 0.563 ± 0.000 | 0.447 ± 0.001 | 0.789 ± 0.002 | 3.99 ± 0.01 | $0.11 |
| LLM, description + catalogue (ontology as context) | 0.570 ± 0.007 | 0.557 ± 0.007 | 0.459 ± 0.006 | 0.751 ± 0.008 | 3.70 ± 0.01 | $0.60 |
| LLM, ontology tags only (no description) | 0.535 ± 0.007 | 0.511 ± 0.010 | 0.444 ± 0.005 | 0.674 ± 0.010 | 3.44 ± 0.02 | $1.02 |
| LR on TF-IDF words | 0.487 ± 0.002 | 0.257 ± 0.001 | 0.828 ± 0.011 | 0.345 ± 0.002 | 0.94 ± 0.02 | $0.00 |
| LR on ontology tags | 0.478 ± 0.004 | 0.402 ± 0.003 | 0.440 ± 0.004 | 0.523 ± 0.004 | 2.69 ± 0.01 | $0.00 |
| LR on words + ontology tags | 0.514 ± 0.002 | 0.423 ± 0.011 | 0.508 ± 0.006 | 0.519 ± 0.003 | 2.31 ± 0.04 | $0.00 |

Per-label F1 (run 1), labels by frequency:

| label | n | text | onto | tags |
|---|---|---|---|---|
| Smart Contract Platform | 120 | 0.77 | 0.75 | 0.66 |
| Layer 1 (L1) | 75 | 0.76 | 0.73 | 0.69 |
| Real World Assets (RWA) | 72 | 0.79 | 0.81 | 0.77 |
| Decentralized Finance (DeFi) | 69 | 0.54 | 0.50 | 0.42 |
| Tokenized Assets | 46 | 0.63 | 0.68 | 0.63 |
| Stablecoins | 42 | 0.71 | 0.75 | 0.68 |
| Artificial Intelligence (AI) | 42 | 0.68 | 0.58 | 0.53 |
| Infrastructure | 38 | 0.27 | 0.27 | 0.29 |
| Proof of Stake (PoS) | 33 | 0.46 | 0.43 | 0.34 |
| Governance | 33 | 0.38 | 0.36 | 0.36 |
| Exchange-based Tokens | 26 | 0.25 | 0.28 | 0.27 |
| USD Stablecoin | 25 | 0.64 | 0.78 | 0.62 |
| Meme | 25 | 0.96 | 0.91 | 0.84 |
| DePIN | 24 | 0.61 | 0.60 | 0.65 |
| Proof of Work (PoW) | 17 | 0.83 | 0.79 | 0.74 |
| Fiat-backed Stablecoin | 17 | 0.67 | 0.65 | 0.50 |
| Decentralized Exchange (DEX) | 16 | 0.59 | 0.67 | 0.70 |
| Layer 2 (L2) | 16 | 0.45 | 0.41 | 0.52 |
| Gaming (GameFi) | 15 | 0.65 | 0.65 | 0.62 |
| NFT | 14 | 0.52 | 0.44 | 0.35 |
| Privacy | 13 | 0.48 | 0.47 | 0.54 |
| Yield Farming | 13 | 0.28 | 0.31 | 0.28 |
| Tokenized Credit | 13 | 0.39 | 0.49 | 0.44 |
| Privacy Blockchain | 11 | 0.48 | 0.40 | 0.50 |
| Centralized Exchange (CEX) Token | 10 | 0.60 | 0.67 | 0.25 |
| Zero Knowledge (ZK) | 10 | 0.44 | 0.52 | 0.44 |
| Wallets | 10 | 0.50 | 0.64 | 0.64 |
| AI Framework | 10 | 0.44 | 0.26 | 0.00 |

Failure cases: text_right_onto_wrong 14, onto_right_text_wrong 18, tags_right_text_wrong 18 (see failure_cases.md).
