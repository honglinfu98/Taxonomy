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

## Pipeline

```bash
python -m taxonomy.classification.sample --per-source 150   # -> data/dlt_corpus/sample.jsonl
python -m taxonomy.classification.tag                       # -> output/classification/
```

| File | Role |
|---|---|
| `sample.py` | Draws the pilot sample. An item = title + abstract (patents: the `### Abstract` section), capped at 450 words; uniform random with a fixed seed; `--per-source`, `--seed`, `--keywords`. |
| `prompts.py` | `TAGGER_INSTRUCTIONS` (what a tag asserts, closed value lists, evidence rule, novel proposals) and the per-item `TAG_PROMPT`. |
| `maintain.py` | Label space, empirical objectives, deterministic proposals, Task E discovery, `dag_v2_proposal.json`. |
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
  term type and category, cost), `novel_proposals.json` (grouped by target term type, the
  discovery signal for Part 3) and `tags.md`.

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

### Pilot maintenance results (300 items)

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
8 accepted: a privacy-mechanism family under privacy features (0.83 bits), identity
binding mechanism and a device-identity value under the identity layer, a ledger
partitioning topology under DLT data structure, a ledger-purpose dimension under
recording, and application-domain dimensions proposed independently under smart contract
scope and script expressiveness. The same "application domain" question surfacing at
three nodes is the signal for one cross-cutting term type at a root rather than three
children; merging candidates across nodes is the next step of the loop. Rejected
candidates mostly had 2-4 supporting items, below `--min-items` on a 300-item batch.

## Next

- Close the loop: merge near-duplicate candidates across nodes, add accepted candidates to
  the catalogue, re-tag the next batch with the v2 catalogue, and track the three
  objectives per iteration.
- Widen the batch (more shards) so support counts clear the thresholds; add a regulatory
  content source so the actor / activity / obligation branches are exercised.
- Gold review of a slice of `tags.jsonl` for precision/recall; then train an in-house
  multi-label classifier on the tagged items to replace the LLM for bulk tagging.
- Task D retrieval by DAG walk is deferred.
