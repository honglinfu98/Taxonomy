# The self-maintenance mechanism (Part 2)

This document specifies how the taxonomy DAG maintains itself from classified content:
what is measured, how candidates are discovered and accepted, how versions evolve, and
what each run costs. Code: `taxonomy/classification/`. Data: `output/evolution/`.

## 1. Objects

**Catalogue version v{n}.** A set of term types and a DAG. A *term type* is a
classification dimension with an id, a question, a category (asset, technology, actor,
activity, obligation_or_risk) and a closed list of *values*. The DAG's edges are *is-a*
relations between term types (child refines parent) with a weight in (0, 1]. v0 is the
seed: the Part 1 DAG built from the legal and academic corpus (93 term types, 317 values,
279 edges). It is copied once to `output/evolution/v0/` and never modified. Later
versions add nodes, edges and values marked `"status": "candidate"`, so seed and
discovered structure remain distinguishable.

**Iteration k.** One pass over a batch of content with the version in force:
`sample -> tag -> maintain -> evolve`. Its files live in `output/evolution/iter_{k}/`.
Batches are disjoint (the sampler excludes every previously drawn item).

**Label space.** The DAG itself. Tagging an item with (term type, value) places the item
on that node; by is-a, the item is also placed on every ancestor. For node y:

- `S(y)`: items tagged directly at y (with any value);
- `C(y)`: closure, `S(y)` plus the closure of every child of y;
- `R(y)`: residual, items in `C(y)` that are on no child of y (they go no deeper than y).

## 2. Tagging (Task C, `tag.py`)

The model receives one cached system block, the *catalogue block*: every term type with
its question, its values as codes `v1..vn` with definitions, and its is-a parents with
weights ("refines"). The corpus of Part 1 is not sent. Per item it returns tags
`(term type id, value code, confidence, evidence span <= 20 words)`, optional `novel`
proposals (a missing value or term type it noticed) and an `off_topic` flag.

Validation: unknown ids are rejected; value codes or labels are resolved to catalogue
values (exact, then fuzzy at 0.85); every evidence span is checked against the item text
(same matcher as Part 1); `implied_term_types` records the is-a ancestors of each tag.

## 3. Measurements (`maintain.py`)

Per node, from the tags:

| statistic | definition | reading |
|---|---|---|
| `n_direct`, `n_closure` | `|S(y)|`, `|C(y)|` | usage of the node and of its branch |
| value entropy | H of the value distribution of `S(y)` (bits) | impurity of the node's own split; 0 = one value absorbs everything |
| value dominance | share of the most frequent value | >= 0.85 with >= 10 items marks a *collapsed* node |
| branching gain | H over `{|C(c)| / |C(y)| for children c} ∪ {|R(y)| / |C(y)|}`, normalised | bits resolved by descending one step from y |
| residual fraction | `|R(y)| / |C(y)|` | stop mass at y; large with many items marks a *discovery target* |

For the whole DAG, a **random descent** starts at a root with probability proportional
to `|C(root)|`, and at node y stops with the residual share or moves to child c with
probability proportional to `|C(c)|` (all shares normalised to sum to 1). From the descent:

- **information gain** = expected bits resolved along a descent (sum of the branching
  entropies met, weighted by the probability of reaching each node);
- **AUC of the reach-a-leaf curve**: F(d) = P(descent has stopped by depth d), AUC = area
  under F over [0, max depth] divided by max depth; 1.0 means every descent ends at
  depth 0, lower means deeper branches;
- **effective leaves / nodes** = 2^H(stop distribution over nodes) divided by the number
  of nodes; how many end points the content actually uses per node of structure.

The same three objectives computed from the model's is-a weights in Part 1 are reported
beside the content-driven values as the *prior reference*.

## 4. Proposals

Deterministic, from the measurements: **dormant** nodes (`|C(y)| = 0`), **collapsed**
nodes (dominance >= 0.85, `|S(y)| >= 10`), **highest-gain** nodes, and **discovery
targets** (`|R(y)| >= min_items` and residual fraction >= `min_residual`; defaults 5 and
0.3). Dormant and collapsed nodes are reported, not removed: on technical content the
legal branches are dormant by nature of the batch, and pruning is a Part 3 decision made
across batches.

## 5. Discovery (Task E, `maintain.py`)

For each discovery target the model is shown the node (question, values, child term
types), the tagger's novel seeds for that node, and up to 40 residual items (title,
evidence spans of the tags at that node, first 60 words). It proposes at most 4
candidates: a **new value** of the node, or a **new child term type** with 2-6 values,
each with supporting item ids and one evidence span.

**Acceptance rule.** A candidate is accepted when all three hold:

1. support: at least `min_items` of its item ids are residual items of the node (among
   the at most `max_items` shown);
2. gain: the shown items are a sample of the residual, so the candidate's support share
   among them is extrapolated to the whole residual (estimated support), and the branching
   gain at the node must rise by at least `min_gain` bits (0.1) if the candidate became a
   child capturing that estimated support out of the residual. Without the extrapolation
   a node with thousands of residual items could never accept anything, since support is
   capped by the 40 items shown;
3. evidence: its span is found verbatim in one of the supporting items.

## 6. Evolution (`evolve.py`)

Accepted candidates of iteration k are consolidated by one model call into the next
version: candidates asking the same question at different nodes are merged (values and
item ids unioned), each new term type is placed under the existing node(s) it refines,
and duplicate values are dropped. The answer is validated (parents must exist, ids
unique, at least two values) and written as v{n+1} with candidate edges at weight 1.0
until Task B re-estimates them. The DAG's prior metrics are recomputed for the new
version. If nothing was accepted the version is unchanged.

Every iteration appends one entry to `output/evolution/evolution.json` (rendered in
`evolution.md`): catalogue used, sample, items, tags, objectives from tags and from the
prior, dormant / collapsed / target counts, candidates and accepted, what was added and
the resulting node / edge / value counts, and the API cost and time of the iteration.

## 7. Cost and time accounting

Every API call records its tokens (input, cached, output) and wall latency. Each
iteration's log entry sums them for tagging, discovery and consolidation, prices them at
Haiku 5.5 list prices (prompts <= 100K tokens: $0.10 / $0.50 per MTok input / output,
cache reads at 10%), and reports total API seconds, mean and p95 latency per request,
wall time and the number of parallel workers.

## 8. Parameters

| parameter | where | default | effect |
|---|---|---|---|
| `--fraction` / `--per-source` | sample | 0.1 / 150 | batch size per source |
| `--max-words` | sample | 450 | item length cap |
| `--workers` | tag, maintain | 6 / 4 | parallel requests |
| `--min-items` | maintain | 5 | min residual and supporting items |
| `--min-residual` | maintain | 0.3 | residual share marking a target |
| `--min-gain` | maintain | 0.1 | bits a candidate must add |
| `--max-items` | maintain | 40 | residual items shown per discovery call |

## 9. Known limitations

- Consolidation does not always merge candidates that ask the same question at different
  nodes (iteration 1 kept two "application domain" dimensions under two smart-contract
  nodes); a similarity check before the model call is the planned fix.
- Candidate edges carry weight 1.0 until Task B re-estimates is-a probabilities for the
  new nodes against the corpus.
- The implied-ancestor closure uses every is-a edge of the DAG, including light ones, so
  closure counts of high nodes are generous.
- Objectives from tags depend on the content mix of the batch; compare iterations on the
  same source mix.
