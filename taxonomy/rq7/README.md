# RQ7: does the ontology improve a downstream classification of Web-sourced token descriptions?

The parked question assumed a dataset of token descriptions from the Web. This directory
collects one and runs the comparison. Everything here is Haiku 5.5 with catalogue v6
(132 term types, 320 is-a edges, the version the gold set was adjudicated against).

## Data (`collect.py`, `labels.py` -> `output/rq7/`)

- `coins.jsonl`: the top 500 coins by market cap on CoinGecko (public API, no key, 2026-10-28)
  with the English description the project or the site published, the site's category tags,
  homepage, genesis date and hashing algorithm.
- `items.jsonl`: the 378 coins with at least 40 words of description (capped at 400 words), in
  the tagger's item shape, with `gold` = the retained site categories.
- `labels.json`: the label space. CoinGecko attaches categories that are not properties of the
  asset (ecosystem membership, index constituents, investor portfolios, launchpads, exchange
  listings, chain-native lists); 215 such names are excluded by pattern. Of the remaining
  categories, the 28 carried by at least 10 items are kept (Smart Contract Platform 120 ...
  AI Framework 10; 130 rarer ones are dropped). 351 items have at least one retained category;
  2.26 gold labels per item on average.

The gold labels are assigned by the site, not by us and not with our catalogue in view, so unlike
the RQ5 downstream column this task does not favour our label space.

## Systems (`classify.py`, `supervised.py`)

| system | sees | role |
|---|---|---|
| LLM, description only | name, description, category list | without the ontology |
| LLM, description + catalogue | the same plus the catalogue block (questions, value definitions, is-a edges) in a cached system block, instructed to state the catalogue values first and then the categories | the ontology as context |
| LLM, ontology tags only | the production tagger's tags for the item (term type, value, definition, evidence span) and the category list, never the description | the ontology as the only evidence |
| LR on TF-IDF words | 1-2 gram TF-IDF (8,334 features), one-vs-rest logistic regression, 5-fold CV | learned, no ontology |
| LR on ontology tags | binary indicators of (term type, value), term type, and implied ancestors from the tagger's run 1 (432 features) | learned, ontology only |
| LR on words + ontology tags | both feature sets | learned, combined |

LLM systems: 3 runs, mean ± sd. Supervised: 5 folds, 3 shuffles, class-weight balanced.
Predicted names that are not in the label list are dropped and counted.

```
python -m taxonomy.rq7.collect --sleep 12 --pages 2     # ~100 min at the public rate limit
python -m taxonomy.rq7.labels
python -m taxonomy.rq7.classify text onto tags --runs 3
python -m taxonomy.rq7.supervised
python -m taxonomy.rq7.report                            # output/rq7/rq7.{json,md}, failure_cases.md, paper/tables/rq7.tex
```

## Results (2026-10-28)

| system | micro-F1 | macro-F1 | P | R | pred/item | cost |
|---|---|---|---|---|---|---|
| LLM, description only (no ontology) | 0.571 ± 0.002 | 0.563 ± 0.000 | 0.447 | 0.789 | 3.99 | $0.11 |
| LLM, description + catalogue (ontology as context) | 0.570 ± 0.007 | 0.557 ± 0.007 | 0.459 | 0.751 | 3.70 | $0.60 |
| LLM, ontology tags only (no description) | 0.535 ± 0.007 | 0.511 ± 0.010 | 0.444 | 0.674 | 3.44 | $1.02 |
| LR on TF-IDF words | 0.487 ± 0.002 | 0.257 ± 0.001 | 0.828 | 0.345 | 0.94 | - |
| LR on ontology tags | 0.478 ± 0.004 | 0.402 ± 0.003 | 0.440 | 0.523 | 2.69 | - |
| LR on words + ontology tags | 0.514 ± 0.002 | 0.423 ± 0.011 | 0.508 | 0.519 | 2.31 | - |

What the numbers say:

- **As prompt context the ontology does not help.** Description + catalogue equals description
  only (0.570 vs 0.571 micro, 0.557 vs 0.563 macro), at five times the cost. This repeats the
  gold-set tagging result on DLT-Corpus: the model, not the catalogue in the prompt, sets the
  accuracy of an LLM classifier.
- **The ontology tags carry the category information.** A model that sees only the tagger's
  output and never the description reaches 94% of the description-only micro-F1 (0.535 vs
  0.571). In the supervised setting 432 binary tag features match 8,334 TF-IDF features on
  micro-F1 (0.478 vs 0.487) and beat them by 15 points on macro-F1 (0.402 vs 0.257): the
  words classifier only learns the frequent categories, the tag classifier generalises to the
  rare ones because a tag such as (asset_reference_type, single official currency) is the same
  feature for every stablecoin whatever words its description uses. Adding the tags to the words
  gives the best learned classifier (0.514 / 0.423).
- **The LLMs over-predict.** All three LLM systems return about 3.4 to 4 categories per item
  against 2.26 gold, so recall is high (0.67 to 0.79) and precision low (0.44 to 0.46); the
  site's own category assignment is sparser than what the descriptions support.
- **Failure case (catalogue gap).** Stacks, a Bitcoin layer 2 (gold: Infrastructure, Layer 2,
  Smart Contract Platform). Description only is exactly right; with the catalogue the model
  claims dlt_architecture = v1 and returns Layer 1. Catalogue v6 has no value for a second-layer
  or rollup architecture (the only mention is a ZK-proof role), so classifying through the
  catalogue forces a base-chain reading. The same mechanism works the other way for KuCoin:
  the actor dimensions (exchange_venue_type, crypto_asset_service_type) lead the catalogue
  prompt to the gold Exchange-based Tokens, which the description-only prompt misses.
  14 items are right only without the catalogue and 18 only with it (`failure_cases.md`).

Caveats: the label space is one site's editorial categories, several of which are marketing
themes rather than classification dimensions (AI Framework, DePIN, Meme), which caps every
system; the tagger's tags are a single Haiku run; the supervised classifiers are not tuned;
one site, 378 items. RQ7 cost $1.73.
