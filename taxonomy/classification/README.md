# Part 2: classification and DAG self-maintenance (in progress)

The DAG is the label space. Content is tagged onto its nodes (Task C), the node statistics
drive the three maintenance objectives, information gain, AUC of the reach-a-leaf curve and
effective leaves / nodes, and entropy impurity at a node marks where new values or term
types are discovered (Task E). The pilot uses an LLM with the DAG in its prompt; the tagged
items are the training set for a cheaper in-house classifier later. Retrieval (Task D) is
deferred.

## Content: DLT-Corpus

Hernandez Cruz et al. (2026), Hugging Face collection `ExponentialScience/dlt-corpus`:
scientific literature (37,440 papers, 5 parquet shards), USPTO patents (49,023, 13
shards) and tweets (22M, 14 shards). The pilot uses the first shard of papers and of
patents, downloaded to `data/dlt_corpus/raw/` (gitignored):

```bash
mkdir -p data/dlt_corpus/raw && cd data/dlt_corpus/raw
curl -L -o sci-00000.parquet https://huggingface.co/datasets/ExponentialScience/DLT-Scientific-Literature/resolve/main/data/train-00000-of-00005.parquet
curl -L -o pat-00000.parquet https://huggingface.co/datasets/ExponentialScience/DLT-Patents/resolve/main/data/train-00000-of-00013.parquet
```

Both datasets contain off-topic documents (the paper shard has oceanography and sensor
network papers), so the sampler keeps only English items whose title or abstract mentions
a DLT term; about 40% of papers and 49% of patents pass.

## Pipeline (one iteration)

```bash
python -m taxonomy.classification.sample --iter 2 --fraction 0.1   # disjoint batch -> data/dlt_corpus/sample_iter02.jsonl
python -m taxonomy.classification.tag --iter 2                     # Task C with the latest catalogue -> output/evolution/iter_02/
python -m taxonomy.classification.maintain --iter 2                # label space, objectives, discovery (Task E)
python -m taxonomy.classification.evolve --iter 2                  # consolidate accepted candidates -> next version, log
```

The mechanism is specified in **`MAINTENANCE.md`** (objects, measurements, acceptance
rule, evolution, cost accounting, parameters, limitations). Versions, iterations and the
evolution log live in `output/evolution/` (`v0/` is the Part 1 seed, never modified).

| File | Role |
|---|---|
| `sample.py` | Draws a disjoint batch per iteration (`--iter`, `--fraction` of each dataset's size or `--per-source`). An item = title + abstract (patents: the `### Abstract` section), capped at 450 words; English, on-topic by keyword. |
| `prompts.py` | `TAGGER_INSTRUCTIONS` (what a tag asserts, closed value lists, evidence rule, novel proposals) and the per-item `TAG_PROMPT`. |
| `catalogue.py` | Versioned catalogue (`v0` seed copied from Part 1, `v{n}` evolved), iteration folders, evolution log. |
| `maintain.py` | Label space, empirical objectives, deterministic proposals, Task E discovery with gain-scored acceptance. |
| `evolve.py` | Consolidates accepted candidates (merge, placement) into the next version; appends the evolution log entry with cost and time. |
| `tag.py` | Task C runner. Builds the **catalogue block** from Part 1 (every term type with question, value codes `v1..vn` with definitions, and its is-a parents from the DAG), caches it, and tags items in parallel. No corpus is sent. |

Per item the model returns `tags` (term type id, value code, confidence, evidence span of
at most 20 words copied from the item) and `novel` proposals (a missing value of an
existing term type, or a missing term type), plus an `off_topic` flag. The runner:

- resolves value codes or labels to catalogue values (exact, then fuzzy at 0.85), rejecting
  unknown ids;
- verifies each evidence span against the item text with the same matcher as Part 1;
- adds `implied_term_types`: the is-a ancestors of every tagged term type (a text tagged
  under a specialised dimension is classified by the general ones too), which is what
  retrieval by DAG walk will use;
- writes `tags.jsonl`, `tags_summary.json` (counts per (term type, value), coverage per
  term type and category, API cost and per-request latency), `novel_proposals.json`
  (grouped by target term type, seeds for discovery) and `tags.md`.

Cost: Haiku 5.5 with the ~24K-token catalogue cached, about $0.0014 per item.

## Pilot results (2026-10-26, 300 items: 150 papers, 150 patents)

1,065 tags (3.55 per item; papers 3.64, patents 3.46), 1,026 evidence spans verified
(96%), 2 tags rejected, 20 items off-topic, 6 responses unparseable, 13 novel proposals.
64 of 93 term types used. Items tagged per category: technology 242, asset 169, actor 27,
activity 21, obligation/risk 6. Most frequent tags: blockchain data structure (122),
cryptographically secured recording (110), public/permissionless (48), transactions
stored on chain (38). Cost $0.14 for the run, $0.0005 per item with the catalogue cached.

Reading: the DLT-Corpus is technical literature, so the technology and asset dimensions
dominate and the legal dimensions (actor, activity, obligation) are rarely exercised;
those parts of the DAG need a regulatory content source to be tested. Novel proposals
include an `application_domain` term type (sector the DLT is applied in) and values such
as mutable block history and post-quantum signatures, which Part 3 can evaluate.

## Maintenance loop (`maintain.py`)

```bash
python -m taxonomy.classification.maintain [--no-discover] [--min-items 5] [--min-residual 0.3] [--min-gain 0.1]
```

1. **Label space.** Every item is placed on the term-type nodes it was tagged with and, by
   is-a, on their ancestors (closure). Per node: `n_direct`, `n_closure`, the value
   distribution of its direct tags with its **value entropy** (impurity of the node's own
   split; 0 bits = one value absorbs everything), the **branching gain** (entropy of the
   split of its closure items over its child term types plus a stop mass), and the
   **residual** (closure items on no child term type: the stop mass).
2. **Objectives from content.** A random descent starts at a root with probability
   proportional to its closure, and at each node stops with the residual share or moves to
   a child in proportion to the child's closure. This gives bits per descent, reach-a-leaf
   AUC, expected depth and effective leaves / nodes from the tags, beside the Part 1 values
   from the model's prior weights.
3. **Deterministic proposals.** Dormant nodes (no items), collapsed nodes (>= 10 items with
   one value >= 85%), highest-gain nodes, and discovery targets (residual >= 30% and >= 5
   items).
4. **Discovery (Task E).** For each target the model sees the node, its values and
   children, the tagger's novel seeds for it, and up to 40 residual items with their
   evidence spans, and proposes missing values or child term types with supporting item
   ids. Each candidate is scored by the branching-gain increase it would bring at that
   node and accepted when it clears `--min-gain` bits with `--min-items` supporting items
   and a verified evidence span. Accepted candidates go to `dag_v2_proposal.json` as
   status "candidate" nodes and values; Part 1 files are never modified.

### Iteration 1 (pilot, 300 items on v0)

| metric | from tags | from Part 1 prior |
|---|---|---|
| bits per descent | 6.92 | 4.72 |
| AUC of reach-a-leaf | 0.794 | 0.835 |
| expected depth | 3.37 | 2.81 |
| effective leaves | 19.7 | 14.0 |
| effective leaves / nodes | 0.212 | 0.150 |

80 of 93 nodes received items; 13 dormant (mostly legal dimensions this content does not
exercise). Collapsed: DLT data structure (124 items, 95% "blockchain") and recording and
cryptographic linkage (113 items, 97% one value), which are also the largest residual
pools, so the discovery step targeted them. 15 targets, 15 calls, $0.01, 32 candidates,
8 accepted and consolidated into **v1** (99 nodes, 285 edges, 351 values): privacy
mechanism family under privacy features (0.83 bits), identity binding mechanism (with a
device-identity value) under the identity layer, ledger partitioning topology under DLT
data structure, ledger purpose under recording, and two application-domain dimensions
under the smart-contract nodes that the consolidation step should have merged (see
`MAINTENANCE.md`, limitations). Rejected candidates mostly had 2-4 supporting items,
below `--min-items` on a 300-item batch. Full log: `output/evolution/evolution.md`.

### Iteration 2 (10% of the DLT-Corpus, 8,646 items on v1)

Batch: 3,744 papers + 4,902 patents (10% of each dataset's size, drawn from the on-topic
pool of all 18 shards, disjoint from iteration 1). Tagging: 35,100 tags (4.06 per item),
98 of 99 nodes received items; the six v1 candidate nodes were used heavily (ledger purpose
4,890 items, smart-contract usage domain 1,347, identity binding 994, privacy mechanism
613) with value entropies of 1.9-2.5 bits, i.e. they discriminate on this content.

| metric | iter 1 (v0, 300 items) | iter 2 (v1, 8,646 items) | v1 prior |
|---|---|---|---|
| bits per descent | 6.92 | 6.96 | 4.82 |
| AUC of reach-a-leaf | 0.794 | 0.771 | 0.843 |
| expected depth | 3.37 | 3.70 | 2.70 |
| effective leaves / nodes | 0.212 | 0.215 | 0.187 |

Maintenance: 1 dormant node, 11 collapsed (DLT data structure 2,377 items at 96%
"blockchain"; recording 2,316 at 97%; several legal nodes at 100% on one value), 32
discovery targets, 81 candidates, 21 accepted, consolidated into **v2** (107 nodes, 293
edges, 396 values): 8 new term types (cross-chain transfer mechanism, key custody and
control model, finality mechanism, key isolation from network, payment settlement
mechanism, key splitting scheme, expressiveness claim basis, key management control
model) and 13 new values, several of them refining the v1 nodes (ledger purpose gains
supply-chain provenance, credentials and health records).

Cost and time of the iteration: 8,679 API requests, $4.29 (tagging $4.25, discovery
$0.04, consolidation $0.004); 15,927 s of summed API time, 2,021 s wall with 8 workers;
mean 1.83 s and p95 2.84 s per tagging request. At this rate the whole paper and patent
corpus (86K documents, ~36K on-topic) would cost about $18 and 70 minutes of wall time
at 8 workers.

Correction made during this iteration: the gain test originally used raw support counts,
but discovery shows at most 40 residual items, so against residual pools of thousands no
candidate could clear the threshold (10 accepted of 76 on the first pass). Support is
now extrapolated from the shown sample to the whole residual; the rerun accepted 21 of 81.

Full per-iteration log with costs: `output/evolution/evolution.md`.

## Next

- Iteration 3 on v2 with the next 10% batch; watch whether the three objectives settle.
- Tighten consolidation so same-question candidates at different nodes are merged
  (iteration 1 kept two application-domain dimensions); add a similarity check before
  the model call.
- Re-estimate is-a weights for candidate nodes (Task B on the new children) instead of
  weight 1.0.
- Add a regulatory content source so the actor / activity / obligation branches are
  exercised; decide prune/merge for collapsed nodes across batches (Part 3).
- Gold review of a slice of `tags.jsonl` for precision/recall; then train an in-house
  multi-label classifier on the tagged items to replace the LLM for bulk tagging.
- Task D retrieval by DAG walk is deferred.

## Full run: six iterations over the whole on-topic DLT-Corpus (2026-10-26)

After the pilot and the 10% batch, iterations 3 to 6 processed the remaining on-topic items
(three 10% batches and the remainder) at 24 workers, about 710 items per minute.

| iteration | items | catalogue | accepted / candidates | produced | nodes / edges / values | cost | wall |
|---|---|---|---|---|---|---|---|
| 1 | 300 | v0 | 8 / 32 | v1 | 99 / 285 / 351 | $0.15 | 1.8 min |
| 2 | 8,646 | v1 | 21 / 81 | v2 | 107 / 293 / 396 | $4.29 | 33.7 min (8 workers) |
| 3 | 8,646 | v2 | 17 / 87 | v3 | 113 / 300 / 433 | $4.45 | 12.4 min |
| 4 | 8,646 | v3 | 18 / 106 | v4 | 124 / 311 / 491 | $4.59 | 13.2 min |
| 5 | 8,646 | v4 | 24 / 127 | v5 | 128 / 316 / 529 | $4.73 | 12.7 min |
| 6 | 1,818 | v5 | 6 / 79 | v6 | 132 / 320 / 549 | $1.07 | 2.9 min |

36,702 items, 150,414 tags, $19.3 in total. The seed's 93 term types and 317 values grew to
132 and 549. Content-measured bits per descent rose from 6.92 to 7.06 while AUC stayed near
0.77 and effective leaves per node drifted down from 0.21 to 0.18 as nodes were added faster
than the content spread over them. Candidates proposed per iteration rose (87, 106, 127) while
acceptances stayed between 17 and 24. Per-version structure, per-iteration objectives and the
later usage of every discovered term type: `output/evolution/evolution_track.md`; dashboard
`python -m taxonomy.classification.evolution_dashboard` (published at
https://claude.ai/artifact/Q6EXEjugt2w64dsTo6a5yS).
