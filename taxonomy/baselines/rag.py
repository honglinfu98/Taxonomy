"""Chunked-RAG and RAPTOR baselines: Task A over retrieved passages instead of the whole corpus.

    python -m taxonomy.baselines.rag [--name rag] [--k 8] [--queries 40] [--workers 8]
    python -m taxonomy.baselines.rag --tree --name raptor        # RAPTOR: collapsed-tree retrieval

Pipeline (shared):
  1. queries   one model call, no corpus: N search queries, N/5 per category, saved to queries.json
               (the same file is reused by --tree so both baselines see identical queries);
  2. retrieve  BM25 top-k passages (sections split at ~900 words) per query; --tree adds the RAPTOR
               summary nodes to the pool (collapsed-tree retrieval, Sarthi et al. 2024);
  3. generate  per query, the Task A instructions and schema over the retrieved passages only,
               with the same citation rule (doc, section label, verbatim quote); summaries may inform
               a term type but cannot be quoted;
  4. consolidate one model call groups the per-query proposals that ask the same question; values
               and citations are unioned deterministically so every quote stays verbatim.
Every citation is verified against the full corpus with the Task A verifier.

RAPTOR tree (--tree): passages are embedded with TF-IDF (1-2 grams) + truncated SVD (50 dims),
clustered with k-means (k = n/5), each cluster summarised by the model (<= 350 words, keeping
defined terms and classification criteria), recursively until <= 3 nodes. Sentence-transformer
embeddings and UMAP + GMM (the original recipe) are replaced by TF-IDF + k-means because no
embedding endpoint is used anywhere else in this project; the summary tree is otherwise as described.
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor

from taxonomy.baselines.common import (CATEGORIES, OUT, BM25, Meter, clean_term_types, compact, dedupe_citations, extract_json, llm,
                                       merge_values, passages, save_catalogue)
from taxonomy.establishment.prompts import TAXONOMIST_INSTRUCTIONS
from taxonomy.llm_context import client

QUERY_INSTRUCTIONS = """\
You design search queries for a taxonomist. The target corpus holds crypto-asset and DLT laws, \
regulatory guidance and taxonomy papers (EU MiCA, AMLR, DORA; UK cryptoasset regulations; US \
Clarity Act, FIT21, GENIUS Act, FinCEN; FATF, Basel, FSB, IOSCO; two academic taxonomies). \
Output valid JSON only.
"""

QUERY_PROMPT = """\
Write {n} short keyword search queries (3-8 words each) that would retrieve passages defining or \
classifying (a) crypto-assets, digital assets and tokens, (b) DLT systems, networks and protocols, \
(c) actors, service providers and intermediaries, (d) activities, services and transactions, and \
(e) obligations, risks and regulatory treatments used as classification criteria. Give {per} \
queries per group, each targeting a different classification dimension (e.g. reference asset, \
consensus mechanism, custody arrangement, licensing status). Return {{"queries": [{{"category": \
"asset|technology|actor|activity|obligation_or_risk", "query": "..."}}]}}.
"""

GENERATE_PROMPT = """\
Task A over retrieved passages: enumerate the grounded term types in the passages above.

The passages were retrieved for the query: "{query}" (category focus: {category}). Produce every \
term type (classification dimension) that the passages explicitly use as a criterion or that \
their definitions discriminate along, relevant to any of: crypto-assets and tokens, DLT systems, \
actors, activities, obligations and risks. Do not restrict yourself to the query's wording.

Return a single JSON object with exactly this schema:

{{
  "term_types": [
    {{
      "id": "snake_case_identifier",
      "name": "Human-readable name",
      "applies_to": "asset | technology | actor | activity | obligation_or_risk",
      "question": "The one question this dimension answers",
      "description": "1-2 sentences on how the passages use this dimension.",
      "aliases": ["other names used for the same dimension"],
      "values": [
        {{"value": "short label", "definition": "at most 25 words",
          "citations": [{{"doc": 4, "section": "exact section label", "quote": "verbatim, at most 30 words"}}]}}
      ],
      "citations": [{{"doc": 4, "section": "exact section label", "quote": "verbatim, at most 30 words"}}]
    }}
  ]
}}

Citations may only quote <document> passages, never <summary> nodes. Document indexes and section \
labels present in the passages (copy exactly):
{manifest}
"""

CONSOLIDATE_INSTRUCTIONS = """\
You merge candidate classification dimensions (term types) proposed from different passages of \
one corpus into a single catalogue. Two candidates belong together when they ask the same \
question about the same kind of thing, even if named differently; candidates that ask different \
questions stay separate. Output valid JSON only.
"""

CONSOLIDATE_PROMPT = """\
Candidates (one per line: id [category] name — question — values):
{candidates}

Group the candidates into term types. Every candidate id must appear in exactly one group. Return:
{{"term_types": [{{"id": "snake_case", "name": "...", "applies_to": "asset | technology | actor | activity | obligation_or_risk",
  "question": "...", "description": "1-2 sentences", "aliases": ["..."], "members": ["candidate ids"]}}]}}
"""

SUMMARY_INSTRUCTIONS = """\
You summarise passages of crypto-asset and DLT legal and technical documents for later retrieval. \
Keep every defined term, classification criterion, category list and threshold, naming the \
document each comes from. Plain prose, at most 350 words, no preamble.
"""


def gen_queries(cl, model: str, n: int, meter: Meter) -> list[dict]:
    p = OUT / "queries.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))["queries"]
    r = llm(cl, QUERY_INSTRUCTIONS, QUERY_PROMPT.format(n=n, per=n // 5), model, "medium", 4000, meter=meter)
    qs = [q for q in extract_json(r["text"])["queries"] if q.get("query")]
    OUT.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"model": model, "queries": qs}, indent=1, ensure_ascii=False), encoding="utf-8")
    return qs


def build_tree(cl, model: str, leaves: list[dict], meter: Meter, workers: int) -> list[dict]:
    """RAPTOR: recursive cluster-and-summarise over the passages; returns the summary nodes."""
    import numpy as np
    from sklearn.cluster import KMeans
    from sklearn.decomposition import TruncatedSVD
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import normalize

    nodes, level, layer = [], 0, list(leaves)
    while len(layer) > 3:
        level += 1
        X = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True, stop_words="english").fit_transform([n["text"] for n in layer])
        X = normalize(TruncatedSVD(min(50, X.shape[1] - 1), random_state=0).fit_transform(X))
        k = max(2, round(len(layer) / 5))
        lab = KMeans(k, n_init=10, random_state=0).fit_predict(X)
        groups = [[layer[i] for i in np.where(lab == c)[0]] for c in range(k)]
        groups = [g for g in groups if g]

        def summarise(g: list[dict]) -> dict:
            body = "\n\n".join(f"[{'doc ' + str(n['doc']) + ' §' + n['section'] if 'doc' in n else 'summary ' + n['id']}]\n{n['text']}" for n in g)
            r = llm(cl, SUMMARY_INSTRUCTIONS, "Summarise:\n\n" + body[:60000], model, "medium", 1500, meter=meter)
            covers = sorted({c for n in g for c in (n.get("covers") or [f"doc {n['doc']} §{n['section']}"])})
            return {"id": f"s{level}_{len(nodes)}_{g[0]['id']}", "level": level, "text": r["text"].strip(), "covers": covers,
                    "children": [n["id"] for n in g]}

        with ThreadPoolExecutor(workers) as ex:
            new = list(ex.map(summarise, groups))
        print(f"  tree level {level}: {len(layer)} nodes -> {len(new)} summaries", file=sys.stderr)
        nodes += new
        layer = new
    return nodes


def render_pool(pool: list[dict]) -> tuple[str, str]:
    """XML block of the retrieved nodes plus the manifest of (doc, section) labels it contains."""
    parts, labels = ["<context_corpus retrieved=\"true\">"], {}
    for n in pool:
        if "doc" in n:
            parts.append(f'<document index="{n["doc"]}" title="{n["title"][:80]}">\n<section label="{n["section"]}" part="{n["part"]}">\n{n["text"]}\n</section>\n</document>')
            labels.setdefault(n["doc"], set()).add(n["section"])
        else:
            parts.append(f'<summary id="{n["id"]}" level="{n["level"]}" covers="{"; ".join(n["covers"])[:300]}">\n{n["text"]}\n</summary>')
    parts.append("</context_corpus>")
    manifest = "\n".join(f"doc {d}: " + " | ".join(f'"{s}"' for s in sorted(ss)) for d, ss in sorted(labels.items()))
    return "\n".join(parts), manifest


def consolidate(cl, model: str, proposals: list[dict], meter: Meter) -> list[dict]:
    cands = compact(proposals)
    r = llm(cl, CONSOLIDATE_INSTRUCTIONS, CONSOLIDATE_PROMPT.format(candidates=cands), model, "high", 60000, meter=meter)
    groups = extract_json(r["text"])["term_types"]
    by_id = {p["id"]: p for p in proposals}
    used, merged = set(), []
    for g in groups:
        members = [by_id[m] for m in (g.get("members") or []) if m in by_id and m not in used]
        if not members:
            continue
        used.update(m["id"] for m in members)
        merged.append({**g, "values": merge_values([m["values"] for m in members]),
                       "citations": dedupe_citations([c for m in members for c in m["citations"]]),
                       "aliases": sorted({a for m in members for a in m.get("aliases", [])} | set(g.get("aliases") or []) | {m["name"] for m in members} - {g.get("name")}),
                       "sources": {"documents": sorted({c.get("doc") for m in members for c in m["citations"] if isinstance(c.get("doc"), int)})},
                       "notes": f"merged from {len(members)} proposals over {len({m['query'] for m in members})} queries"})
    for p in proposals:                                   # the consolidation call missed it: keep as is
        if p["id"] not in used:
            merged.append({**p, "notes": "singleton proposal (not grouped by consolidation)"})
    return clean_term_types(merged)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--effort", default="high")
    ap.add_argument("--name", default=None)
    ap.add_argument("--tree", action="store_true", help="RAPTOR: add recursive summary nodes to the retrieval pool")
    ap.add_argument("--k", type=int, default=8, help="passages retrieved per query")
    ap.add_argument("--queries", type=int, default=40)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--max-words", type=int, default=900)
    a = ap.parse_args()
    name = a.name or ("raptor" if a.tree else "rag")
    d = OUT / name
    d.mkdir(parents=True, exist_ok=True)
    cl, meter = client(), Meter(a.model)

    leaves = passages(a.max_words)
    pool = list(leaves)
    tree_info = {}
    if a.tree:
        tp = d / "tree.json"
        if tp.exists():
            nodes = json.loads(tp.read_text(encoding="utf-8"))["nodes"]
        else:
            nodes = build_tree(cl, a.model, leaves, meter, a.workers)
            tp.write_text(json.dumps({"leaves": len(leaves), "nodes": nodes}, indent=1, ensure_ascii=False), encoding="utf-8")
        pool += nodes
        tree_info = {"summary_nodes": len(nodes), "levels": max(n["level"] for n in nodes)}
    index = BM25([n["text"] for n in pool])
    queries = gen_queries(cl, a.model, a.queries, meter)
    print(f"{name}: {len(leaves)} passages, pool {len(pool)}, {len(queries)} queries", file=sys.stderr)

    def one(q: dict) -> dict:
        hits = [pool[i] for i in index.search(q["query"], a.k)]
        block, manifest = render_pool(hits)
        prompt = GENERATE_PROMPT.format(query=q["query"], category=q.get("category", ""), manifest=manifest)
        r = llm(cl, TAXONOMIST_INSTRUCTIONS, prompt, a.model, a.effort, 16000, extra_system=[block], meter=meter)
        try:
            tts = clean_term_types(extract_json(r["text"]).get("term_types", []))
        except (ValueError, json.JSONDecodeError, AttributeError):
            tts = []
        return {"query": q["query"], "category": q.get("category"), "retrieved": [h["id"] for h in hits],
                "summaries_retrieved": sum("doc" not in h for h in hits), "term_types": tts, "stop_reason": r["stop_reason"]}

    with ThreadPoolExecutor(a.workers) as ex:
        per_query = list(ex.map(one, queries))
    (d / "per_query.json").write_text(json.dumps(per_query, indent=1, ensure_ascii=False), encoding="utf-8")

    proposals = []
    for qi, pq in enumerate(per_query):
        for t in pq["term_types"]:
            proposals.append({**t, "id": f"q{qi}_{t['id']}"[:70], "query": pq["query"]})
    print(f"{name}: {len(proposals)} proposals from {len(per_query)} queries; consolidating", file=sys.stderr)
    tts = consolidate(cl, a.model, proposals, meter)
    run = {"task": "A-" + name, "effort": a.effort, "k": a.k, "queries": len(queries), "passages": len(leaves), "pool": len(pool),
           "proposals": len(proposals), **tree_info, **meter.report()}
    save_catalogue(name, tts, run)


if __name__ == "__main__":
    main()
