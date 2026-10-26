# Part 3: optimisation (retrieval over the DAG)

Part 1 established the taxonomy DAG, Part 2 tagged content onto its nodes and let the DAG
grow from the content. Part 3 turns the tagged content into an index on the DAG and retrieves
it with graph operations instead of flat text search. Code: `taxonomy/retrieval/`. Data:
`output/retrieval/`.

```bash
python -m taxonomy.retrieval.index                       # build index.pkl from every tagged iteration (0.2 s)
python -m taxonomy.retrieval.query 'consensus_mechanism="proof of stake" AND privacy_enhancement' -k 10
python -m taxonomy.retrieval.query --text "zero-knowledge proofs for private payments"   # lexical routing; --llm for the model
python -m taxonomy.retrieval.query --like paper:ecbd4b6758cdfbde08e9522a51e7b00e1a7d9a5f  # more like this item
python -m taxonomy.retrieval.query --node ledger_purpose                                  # node card: counts, parents, children, values, facets
python -m taxonomy.retrieval.benchmark                   # latency vs flat scans, navigation by facet gain
```

## 1. The index (`index.py`)

Items are the DLT-Corpus texts tagged in Part 2 (every `output/evolution/iter_*/tags.jsonl`,
off-topic and untagged items skipped), placed on the latest catalogue version. Items are
numbered 0..N-1 and every posting list is a Python int bitset (bit i = item i), so set
algebra on postings is one integer operation.

| posting | contents |
|---|---|
| `direct[y]` | items tagged directly at node y, any value |
| `pair[(y, v)]` | items tagged at y with value v |
| `closure[y]` | items anywhere in the subtree of y: OR of `direct` over the descendants of y |
| `cat[c]` | items with any tag in category c |

Per item the index keeps its tagged nodes with confidence, its (node, value) pairs, the
evidence span per (item, node), and a byte offset into the sample file for the text (the
text itself stays in the gitignored `data/`). The index on v2 holds 8,205 items and 35,884
tags, builds in 0.2 s and is 9 MB (`index.pkl`, rebuildable, not committed).

## 2. Graph structures (`graph.py`)

| structure | definition | use |
|---|---|---|
| transitive closure | descendants / ancestors of every node as bitsets, by dynamic programming in topological order | `closure[y]`, subtree and ancestor tests in O(1) |
| best is-a path strength s(d, a) | max over paths d -> a of the product of the Task B edge weights | weights a closure match: an item tagged at d is a weaker answer to a query at a when the is-a chain is weak |
| lowest common ancestors | common ancestors of the query nodes not dominated by another common ancestor | the generalisation of a multi-node query ("zoom out") |
| information content IC(y) | -log2 (closure size / N) from the index | specificity of a node; weights item vectors |
| node similarity | weighted-path: max over common ancestors c of s(a, c) s(b, c); also Resnik and Lin on IC | query expansion to neighbouring nodes when a query has too few hits |

## 3. Queries (`query.py`)

Atoms combine with AND, OR, NOT and parentheses (a space is AND):

| atom | items |
|---|---|
| `node` | the subtree of node (reachability closure) |
| `node!` | tagged directly at node |
| `node=v3`, `node="value label"` | tagged at node with that value |
| `node~0.3` | subtree restricted to descendants with path strength >= 0.3 to node |
| `@technology` | any tag in that category |

Evaluation walks the parse tree over bitsets. Ranking: an item's score is the sum over the
positive atoms of its match strength, where a direct or value match is the tag confidence and
a closure match is max over the item's tagged descendants d of confidence(d) x s(d, node);
`via` reports the node the match came through.

**Facets.** For the result set and the query nodes, the engine lists the child subtrees and
the value splits with the expected narrowing each gives, sum over options of
p(option) x log2(n / |option|) with options picked in proportion to size, so an option that
covers the whole set narrows by 0 bits. The top facet is the best next question to ask to
reach the target fastest; this is the retrieval-time counterpart of the information gain
that Part 2 uses to maintain the DAG.

**Expansion.** When fewer than k items match, items from the nodes most similar to the
query nodes (weighted-path similarity) are appended, scored by similarity x match strength
and marked `expanded` with the node they came through.

**More like this.** An item is a vector over nodes: for each tagged node d and each ancestor
a, confidence(d) x s(d, a) x IC(a); cosine similarity over the items that share a tagged node.

**Free text.** `--text` routes a request to a query lexically (idf-weighted overlap of the
request's tokens with node names, questions, aliases and value labels); `--llm` asks the
model for the query string with the catalogue as a cached system block instead.

## 4. Benchmark (`benchmark.py`, `output/retrieval/benchmark.md`)

Latency per query on one core, index on v2 (8,205 items), all results checked identical
to the flat scans:

| workload | queries | mean result | bitset (us) | flat scan (us) | flat, no closure (us) | speedup |
|---|---|---|---|---|---|---|
| closure, 1 node | 107 | 1474 | 2.1 | 5131 | 4515 | 2400x |
| direct, 1 node | 91 | 360 | 2.1 | 1991 | 2506 | 935x |
| value | 285 | 126 | 2.8 | 6488 | 6949 | 2300x |
| closure, strength >= 0.3 | 107 | 579 | 4.9 | 5423 | 4817 | 1100x |
| AND, 2 atoms | 300 | 63 | 5.6 | 7315 | 7492 | 1300x |
| OR, 2 atoms | 300 | 1071 | 5.7 | 12534 | 12783 | 2200x |
| AND NOT | 300 | 476 | 6.9 | 7485 | 7621 | 1100x |
| 3 atoms, mixed | 200 | 53 | 9.9 | 14204 | 14479 | 1400x |

The flat scan is what a tag table without an inverted index costs (one predicate test per
item, ancestor sets precomputed); "no closure" also enumerates the subtree per query.

Navigation: 300 random target items, narrowing the whole collection by picking, at each
step, the option of the offered facet that contains the target, until at most k = 10 items
remain (ideal 9.68 bits):

| facet policy | mean steps | bits resolved | bits / step | reached k | mean final size |
|---|---|---|---|---|---|
| highest expected narrowing | 8.2 | 10.2 | 1.25 | 86% | 18 |
| random facet | 14.3 | 5.7 | 0.40 | 20% | 793 |

## 5. Known limitations

- Closures through light is-a edges are large (the scope-criteria root reaches 82% of the
  items); path-strength weighting in the ranking and `node~s` in queries compensate, and
  Part 2's re-estimation of candidate edge weights will tighten them.
- Bitsets are Python ints: ideal to a few hundred thousand items; beyond that, swap for
  roaring bitmaps behind the same `Index` interface.
- Rankings use tag confidence from the LLM tagger; no learned relevance yet.
- The lexical router is a bag-of-words baseline; `--llm` routing costs one small model call.
