"""Retrieval quality on judged queries: P@k, NDCG@k, MAP and latency, several runs with sd.

    python -m taxonomy.evaluation.retrieval_eval [--k 10] [--runs 3] [--seed 5]

Judged collection: the gold items; relevance of an item to a query is derived from its gold labels
(value query: 2 if the item carries that (term type, value); node query: 2 if a gold tag sits at the
node, 1 if only at a descendant through is-a; AND query: the minimum over atoms). Queries are every
value with >= 3 relevant items, every node with >= 5 relevant items that is not trivially satisfied
by more than half the collection, and a seeded sample of 2-atom AND queries with >= 3 relevant items.

Systems (run r uses the tag predictions of run r from tagging_eval):
  dag_index    our index built from the DAG-guided tags: bitset evaluation, rank by confidence x is-a path strength
  flat_tags    boolean match on the flat zero-shot tags, no closure, rank by confidence
  supervised   the supervised baseline's labels through the DAG index (confidence = probability)
  bm25         text baseline: BM25 over title + text with the query rendered as natural language
               (term type name, question and value labels); no taxonomy
Latency is the mean per query on the judged collection. Writes retrieval_eval.{json,md} and
paper/tables/eval_retrieval.tex.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import re
import sys
import time
from collections import Counter

from taxonomy.classification import catalogue as cat
from taxonomy.evaluation.common import GOLD, GOLD_ITEMS, OUT, PAPER_TABLES, mean_sd, ndcg_at_k, pm, pm_tex, read_jsonl
from taxonomy.retrieval.graph import iter_bits
from taxonomy.retrieval.index import Index
from taxonomy.retrieval.query import Engine, parse, tokenize


# ---- judgments and queries ------------------------------------------------------------------
def build_queries(gold: list[dict], g: Index, k: int, seed: int, max_value_q: int = 60, max_node_q: int = 30, n_and: int = 20) -> list[dict]:
    graph = g.graph
    direct: dict[str, set[str]] = {}
    pairs: dict[tuple[str, str], set[str]] = {}
    for row in gold:
        for t in row["tags"]:
            direct.setdefault(t["term_type"], set()).add(row["item_id"])
            pairs.setdefault((t["term_type"], t["value"]), set()).add(row["item_id"])
    n = len(gold)
    rng = random.Random(seed)

    def node_grades(y: str) -> dict[str, int]:
        grades: dict[str, int] = {}
        for kk in iter_bits(graph.desc_bits[y]):
            d = graph.ids[kk]
            for i in direct.get(d, ()):
                grades[i] = max(grades.get(i, 0), 2 if d == y else 1)
        return grades

    qs = []
    vq = [(p, ids) for p, ids in pairs.items() if len(ids) >= 3]
    rng.shuffle(vq)
    for (y, v), ids in sorted(vq[:max_value_q]):
        qs.append({"kind": "value", "query": f'{y}="{v}"', "text": f"{g.by_id[y]['name']}: {v}", "grades": {i: 2 for i in ids}})
    nq = []
    for y in graph.ids:
        gr = node_grades(y)
        if len(gr) >= 5 and len(gr) <= n // 2:
            nq.append((y, gr))
    rng.shuffle(nq)
    for y, gr in sorted(nq[:max_node_q]):
        qs.append({"kind": "node", "query": y, "text": f"{g.by_id[y]['name']}. {g.by_id[y]['question']}", "grades": gr})
    cands = [p for p, ids in pairs.items() if len(ids) >= 3]
    tries, seen = 0, set()
    while sum(1 for q in qs if q["kind"] == "and") < n_and and tries < 2000 and len(cands) >= 2:
        tries += 1
        (y1, v1), (y2, v2) = sorted(rng.sample(cands, 2))
        if y1 == y2 or ((y1, v1), (y2, v2)) in seen:
            continue
        seen.add(((y1, v1), (y2, v2)))
        ids = pairs[(y1, v1)] & pairs[(y2, v2)]
        if len(ids) >= 3:
            qs.append({"kind": "and", "query": f'{y1}="{v1}" AND {y2}="{v2}"', "text": f"{g.by_id[y1]['name']}: {v1}; {g.by_id[y2]['name']}: {v2}",
                       "grades": {i: 2 for i in ids}})
    return qs


# ---- systems -----------------------------------------------------------------------------------
def make_index(version: int, tts: list[dict], dag: dict, items: list[dict], rows: list[dict]) -> Index:
    idx = Index(version, tts, dag)
    by = {r["item_id"]: r for r in rows}
    for it in items:
        r = by.get(it["id"])
        idx.add_item({"id": it["id"], "source": it["source"], "title": it["title"]}, r["tags"] if r and not r.get("off_topic") else [])
    idx.finalise()
    return idx


class FlatTags:
    """Boolean match on exact (term type, value) or term type tags, ranked by confidence; no closure."""

    def __init__(self, rows: list[dict]):
        self.tags = {r["item_id"]: {(t["term_type"], t["value"]): t["confidence"] for t in r["tags"]} for r in rows}

    def search(self, tree, k: int) -> list[str]:
        scored = []
        for i, tg in self.tags.items():
            s = self.score(tree, tg)
            if s is not None:
                scored.append((-s, i))
        return [i for _, i in sorted(scored)[:k]]

    def score(self, tree, tg) -> float | None:
        from taxonomy.retrieval.query import Atom
        if isinstance(tree, Atom):
            if tree.value is not None:
                m = [c for (y, v), c in tg.items() if y == tree.node and v.lower() == tree.value.lower()]
            else:
                m = [c for (y, _), c in tg.items() if y == tree.node]
            return max(m) if m else None
        if tree[0] == "AND":
            a, b = self.score(tree[1], tg), self.score(tree[2], tg)
            return None if a is None or b is None else a + b
        if tree[0] == "OR":
            a, b = self.score(tree[1], tg), self.score(tree[2], tg)
            return None if a is None and b is None else (a or 0) + (b or 0)
        return None


class BM25:
    def __init__(self, items: list[dict], k1: float = 1.2, b: float = 0.75):
        self.ids = [it["id"] for it in items]
        self.docs = [self.tok(it["title"] + " " + it.get("text", "")) for it in items]
        self.k1, self.b = k1, b
        self.avgdl = sum(len(d) for d in self.docs) / max(len(self.docs), 1)
        self.df: Counter = Counter()
        self.tf = []
        for d in self.docs:
            c = Counter(d)
            self.tf.append(c)
            self.df.update(c.keys())
        self.N = len(self.docs)

    @staticmethod
    def tok(s: str) -> list[str]:
        return re.findall(r"[a-z0-9]+", s.lower())

    def search(self, text: str, k: int) -> list[str]:
        q = self.tok(text)
        scores = []
        for i, c in enumerate(self.tf):
            dl = len(self.docs[i])
            s = 0.0
            for w in q:
                if w in c:
                    idf = math.log(1 + (self.N - self.df[w] + 0.5) / (self.df[w] + 0.5))
                    s += idf * c[w] * (self.k1 + 1) / (c[w] + self.k1 * (1 - self.b + self.b * dl / self.avgdl))
            scores.append((-s, self.ids[i]))
        return [i for s, i in sorted(scores)[:k] if s < 0]


# ---- metrics -------------------------------------------------------------------------------------
def judge(ranked: list[str], grades: dict[str, int], k: int) -> dict:
    rel = [grades.get(i, 0) for i in ranked]
    n_rel = sum(1 for v in grades.values() if v > 0)
    p5 = sum(1 for v in rel[:5] if v > 0) / 5
    pk = sum(1 for v in rel[:k] if v > 0) / k
    rk = sum(1 for v in rel[:k] if v > 0) / max(n_rel, 1)
    hits, ap = 0, 0.0
    for r, v in enumerate(rel, 1):
        if v > 0:
            hits += 1
            ap += hits / r
    return {"p5": p5, f"p{k}": pk, f"r{k}": rk, f"ndcg{k}": ndcg_at_k(rel, list(grades.values()), k), "ap": ap / max(n_rel, 1)}


def run_system(name: str, queries: list[dict], k: int, searcher) -> dict:
    per_q, lat = [], []
    for q in queries:
        t0 = time.perf_counter()
        ranked = searcher(q)
        lat.append(time.perf_counter() - t0)
        per_q.append(judge(ranked, q["grades"], k))
    keys = per_q[0].keys() if per_q else []
    out = {m: round(sum(x[m] for x in per_q) / len(per_q), 4) for m in keys}
    out["latency_us"] = round(sum(lat) / len(lat) * 1e6, 1)
    for kind in ("value", "node", "and"):
        sub = [x for x, q in zip(per_q, queries) if q["kind"] == kind]
        if sub:
            out[f"ndcg{k}_{kind}"] = round(sum(x[f"ndcg{k}"] for x in sub) / len(sub), 4)
    return out


def render(res: dict, k: int) -> tuple[str, str]:
    names = {"dag_index": "DAG index (ours, Haiku 5.5 tags)", "flat_tags": "flat zero-shot tags, no closure", "supervised": "supervised labels + DAG index",
             "bm25": "BM25 over text", "dag_index@claude-sonnet-5-5": "DAG index (Sonnet 5.5 tags)",
             "flat_tags@claude-sonnet-5-5": "flat zero-shot tags, no closure (Sonnet 5.5)"}
    md = ["# Retrieval evaluation", "",
          f"Judged collection: {res['items']} gold items; {res['n_queries']} queries ({res['query_kinds']}); k = {k}; "
          f"{res['runs']} runs (mean ± sd over runs; each run uses that run's tag predictions). "
          f"Latency is the mean per query on the judged collection; the full-index latency on {res['full_index_items']} items is in output/retrieval/benchmark.md.", "",
          f"| system | P@5 | P@{k} | R@{k} | NDCG@{k} | MAP | NDCG@{k} value q | node q | AND q | latency (us) |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    tex = ["% generated by taxonomy.evaluation.retrieval_eval", "\\begin{tabular}{lccccc}", "\\toprule",
           f"System & P@{k} & NDCG@{k} & MAP & R@{k} & Latency ($\\mu$s) \\\\", "\\midrule"]
    for s, runs in res["systems"].items():
        g = lambda m: [r.get(m) for r in runs]
        md.append(f"| {names.get(s, s)} | {pm(g('p5'))} | {pm(g(f'p{k}'))} | {pm(g(f'r{k}'))} | {pm(g(f'ndcg{k}'))} | {pm(g('ap'))} | "
                  f"{pm(g(f'ndcg{k}_value'))} | {pm(g(f'ndcg{k}_node'))} | {pm(g(f'ndcg{k}_and'))} | {mean_sd(g('latency_us'))[0]:.0f} |")
        tex.append(f"{names.get(s, s)} & {pm_tex(g(f'p{k}'))} & {pm_tex(g(f'ndcg{k}'))} & {pm_tex(g('ap'))} & {pm_tex(g(f'r{k}'))} & {mean_sd(g('latency_us'))[0]:.0f} \\\\")
    tex += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(md) + "\n", "\n".join(tex) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--seed", type=int, default=5)
    a = ap.parse_args()
    if not GOLD.exists():
        sys.exit("gold.jsonl missing")
    tsum = json.loads((OUT / "tagging_eval.json").read_text(encoding="utf-8"))
    version = tsum["catalogue_version"]
    tts, dag, _ = cat.load_version(version)
    items = read_jsonl(GOLD_ITEMS)
    gold = read_jsonl(GOLD)
    gold_ids = {g["item_id"] for g in gold}
    items = [it for it in items if it["id"] in gold_ids]
    gold_idx = make_index(version, tts, dag, items, gold)
    queries = build_queries(gold, gold_idx, a.k, a.seed)
    (OUT / "retrieval_queries.json").write_text(json.dumps(queries, indent=1, ensure_ascii=False), encoding="utf-8")
    bm25 = BM25(items)
    res = {"items": len(items), "n_queries": len(queries), "query_kinds": dict(Counter(q["kind"] for q in queries)), "k": a.k,
           "runs": a.runs, "catalogue_version": version, "systems": {}, "full_index_items": None}
    try:
        res["full_index_items"] = json.loads((cat.EVOL.parent / "retrieval" / "index_summary.json").read_text())["items"]
    except Exception:
        pass
    parsed = {q["query"]: parse(tokenize(q["query"])) for q in queries}
    for r in range(1, a.runs + 1):
        preds = {p.name[len("pred_"):-len(f"_run{r}.jsonl")]: read_jsonl(p) for p in sorted(OUT.glob(f"pred_*_run{r}.jsonl"))}
        for s2, rows2 in preds.items():
            if s2.startswith("flat@"):         # second-model flat tags, no closure
                ft2 = FlatTags(rows2)
                res["systems"].setdefault(f"flat_tags@{s2.split('@', 1)[1]}", []).append(run_system(
                    s2, queries, a.k, lambda q, ft2=ft2: ft2.search(parsed[q["query"]], a.k)))
            if s2.startswith("dag@"):          # second-model tags through the DAG index
                idx3 = make_index(version, tts, dag, items, rows2)
                eng3 = Engine(idx3)
                res["systems"].setdefault(f"dag_index@{s2.split('@', 1)[1]}", []).append(run_system(
                    s2, queries, a.k, lambda q, idx3=idx3, eng3=eng3: [idx3.items[x["i"]]["id"] for x in eng3.rank(eng3.evaluate(parsed[q["query"]]), eng3.positive_atoms(parsed[q["query"]]), a.k)]))
        if "dag" in preds:
            idx = make_index(version, tts, dag, items, preds["dag"])
            eng = Engine(idx)
            res["systems"].setdefault("dag_index", []).append(run_system(
                "dag_index", queries, a.k, lambda q: [idx.items[x["i"]]["id"] for x in eng.rank(eng.evaluate(parsed[q["query"]]), eng.positive_atoms(parsed[q["query"]]), a.k)]))
        if "flat" in preds:
            ft = FlatTags(preds["flat"])
            res["systems"].setdefault("flat_tags", []).append(run_system("flat_tags", queries, a.k, lambda q: ft.search(parsed[q["query"]], a.k)))
        if "supervised" in preds:
            idx2 = make_index(version, tts, dag, items, preds["supervised"])
            eng2 = Engine(idx2)
            res["systems"].setdefault("supervised", []).append(run_system(
                "supervised", queries, a.k, lambda q: [idx2.items[x["i"]]["id"] for x in eng2.rank(eng2.evaluate(parsed[q["query"]]), eng2.positive_atoms(parsed[q["query"]]), a.k)]))
        if r == 1 or True:
            res["systems"].setdefault("bm25", []).append(run_system("bm25", queries, a.k, lambda q: bm25.search(q["text"], a.k)))
    order = ["dag_index", "dag_index@claude-sonnet-5-5", "flat_tags", "flat_tags@claude-sonnet-5-5", "supervised", "bm25"]
    res["systems"] = {k: res["systems"][k] for k in order if k in res["systems"]} | {k: v for k, v in res["systems"].items() if k not in order}
    (OUT / "retrieval_eval.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    md, tex = render(res, a.k)
    (OUT / "retrieval_eval.md").write_text(md, encoding="utf-8")
    PAPER_TABLES.mkdir(parents=True, exist_ok=True)
    (PAPER_TABLES / "eval_retrieval.tex").write_text(tex, encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()
