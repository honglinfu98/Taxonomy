# Part 2: classification (in progress)

Goal: tag incoming content with nodes of the Part 1 ontology and serve fast retrieval by
walking the DAG instead of searching flat text.

## Inputs from Part 1 (read-only here)

- `output/establishment/taxonomy_dag.json` — 93 term types (nodes), 279 weighted is-a
  edges, 5 roots, per-node information gain.
- `output/establishment/term_types.json` — each term type's question, values with
  definitions, and citations. The **values** are the tags a content item can receive.
- `context/taxonomy_corpus.txt` — stays available as cached grounding context.

## Proposed design (to confirm)

1. **Unit of content.** One tag set per item; an item is a passage of bounded length
   (a document is split into passages, tags roll up to the document).
2. **Task C, tagging.** For each item, descend the DAG from each root: at a node, the
   model decides which of its values apply to the item (multi-label, with a confidence
   and a supporting span from the item), and whether to descend into child term types.
   Descent stops when no value applies or at a leaf. Nodes are visited in order of their
   information gain so the cheapest discriminating questions come first.
3. **Task D, index and retrieval.** Items are indexed by (term type, value). A query is
   resolved by walking the DAG: pick a root, choose values, narrow to the subtree; the
   result set is the intersection of the item sets along the path. The AUC and expected
   depth from Part 1 bound how many steps a retrieval takes.
4. **Evaluation.** Tag precision/recall against a small gold set, retrieval hit rate, cost
   per item, and average descent length.

## Open questions

- What content is to be classified (source, format, volume) and what is one item?
- Is there a gold-labelled sample, or should a small one be built by review?
- Single-model tagging (Haiku 5.5 with the corpus cached) or a cheaper first pass?

Outputs will go to `output/classification/`.
