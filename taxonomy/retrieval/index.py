"""Build the retrieval index: tagged items placed on the taxonomy DAG as bitset postings.

    python -m taxonomy.retrieval.index [--version N] [--iters 1 2 ...]

Reads the catalogue version (default: latest) and every iteration's tags.jsonl under
output/evolution/, joins the item metadata from the sample files, and writes
output/retrieval/index.pkl plus index_summary.{json,md}.

Postings (items are numbered 0..N-1; a posting is an int bitset):
  direct[y]        items tagged directly at node y (any value)
  pair[(y, v)]     items tagged at y with value v
  closure[y]       items anywhere in the subtree of y  = OR of direct over descendants(y)
  cat[c]           items with any tag in category c
Per item: its tagged nodes with confidence, and evidence spans per (item, node) for display.
The DAG structure (closures, path strengths, LCA, information content) is a TaxonomyGraph.
"""
from __future__ import annotations

import argparse
import json
import pickle
import time
from collections import defaultdict
from pathlib import Path

from taxonomy.classification import catalogue as cat
from taxonomy.classification.sample import sample_path
from taxonomy.llm_context import ROOT
from taxonomy.retrieval.graph import TaxonomyGraph, iter_bits, popcount

OUT = ROOT / "output" / "retrieval"
INDEX = OUT / "index.pkl"
SUMMARY = OUT / "index_summary.json"
SUMMARY_MD = OUT / "index_summary.md"


class Index:
    def __init__(self, version: int, tts: list[dict], dag: dict):
        self.version = version
        self.tts = tts
        self.by_id = {t["id"]: t for t in tts}
        self.graph = TaxonomyGraph(dag)
        self.values: dict[str, list[str]] = {t["id"]: [v["value"] for v in t["values"]] for t in tts}
        self.items: list[dict] = []
        self.item_pos: dict[str, int] = {}
        self.direct: dict[str, int] = defaultdict(int)
        self.pair: dict[tuple[str, str], int] = defaultdict(int)
        self.closure: dict[str, int] = {}
        self.cat: dict[str, int] = defaultdict(int)
        self.item_nodes: list[dict[str, float]] = []           # per item: node -> max confidence
        self.item_values: list[dict[tuple[str, str], float]] = []  # per item: (node, value) -> confidence
        self.evidence: dict[tuple[int, str], str] = {}
        self.all = 0
        self.n = 0
        self.stats: dict = {}

    # ---- building ------------------------------------------------------------------
    def add_item(self, meta: dict, tags: list[dict]) -> None:
        i = len(self.items)
        self.items.append(meta)
        self.item_pos[meta["id"]] = i
        bit = 1 << i
        nodes: dict[str, float] = {}
        vals: dict[tuple[str, str], float] = {}
        for g in tags:
            y, v, c = g["term_type"], g["value"], float(g.get("confidence") or 0.0)
            if y not in self.by_id:
                continue
            nodes[y] = max(nodes.get(y, 0.0), c)
            vals[(y, v)] = max(vals.get((y, v), 0.0), c)
            self.direct[y] |= bit
            self.pair[(y, v)] |= bit
            self.cat[self.graph.category[y]] |= bit
            if (i, y) not in self.evidence and g.get("evidence"):
                self.evidence[(i, y)] = g["evidence"]
        self.item_nodes.append(nodes)
        self.item_values.append(vals)

    def finalise(self) -> None:
        self.n = len(self.items)
        self.all = (1 << self.n) - 1
        g = self.graph
        self.direct = dict(self.direct)
        self.pair = dict(self.pair)
        self.cat = dict(self.cat)
        for y in g.ids:
            b = 0
            for k in iter_bits(g.desc_bits[y]):
                b |= self.direct.get(g.ids[k], 0)
            self.closure[y] = b
        g.set_counts({y: popcount(self.closure[y]) for y in g.ids}, self.n)

    # ---- access ----------------------------------------------------------------------
    def item_text(self, i: int) -> str:
        ref = self.items[i].get("text_ref")
        if not ref:
            return ""
        with open(ref[0], "rb") as f:
            f.seek(ref[1])
            return json.loads(f.readline().decode("utf-8")).get("text", "")

    def save(self, path: Path = INDEX) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)


def load(path: Path = INDEX) -> Index:
    if not path.exists():
        raise SystemExit(f"{path} missing: run python -m taxonomy.retrieval.index")
    with open(path, "rb") as f:
        return pickle.load(f)


def scan_sample(k: int) -> dict[str, tuple[dict, tuple[str, int]]]:
    """id -> (metadata, (file, byte offset)) for iteration k's sample file."""
    p = sample_path(k)
    out = {}
    if not p.exists():
        return out
    with open(p, "rb") as f:
        off = 0
        for line in f:
            r = json.loads(line.decode("utf-8"))
            out[r["id"]] = ({"id": r["id"], "source": r.get("source"), "title": r.get("title"), "year": r.get("year"),
                             "meta": r.get("meta") or {}, "words": len((r.get("text") or "").split())}, (str(p), off))
            off += len(line)
    return out


def build(version: int | None, iters: list[int] | None) -> Index:
    t0 = time.perf_counter()
    version = cat.latest_version() if version is None else version
    tts, dag, _ = cat.load_version(version)
    idx = Index(version, tts, dag)
    iters = iters or cat.iterations()
    skipped = {"off_topic": 0, "no_tags": 0, "duplicate": 0}
    n_tags = 0
    for k in iters:
        tags_file = cat.iter_dir(k) / "tags.jsonl"
        if not tags_file.exists():
            continue
        metas = scan_sample(k)
        for line in tags_file.read_text(encoding="utf-8").split("\n"):
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("off_topic"):
                skipped["off_topic"] += 1
                continue
            tags = [g for g in r.get("tags", []) if g.get("term_type") in idx.by_id]
            if not tags:
                skipped["no_tags"] += 1
                continue
            if r["item_id"] in idx.item_pos:
                skipped["duplicate"] += 1
                continue
            meta, ref = metas.get(r["item_id"], ({"id": r["item_id"], "source": r.get("source"), "title": r.get("title")}, None))
            meta = {**meta, "iteration": k, "text_ref": ref}
            idx.add_item(meta, tags)
            n_tags += len(tags)
    idx.finalise()
    g = idx.graph
    closure_sizes = {y: popcount(idx.closure[y]) for y in g.ids}
    direct_sizes = {y: popcount(idx.direct.get(y, 0)) for y in g.ids}
    idx.stats = {
        "catalogue_version": version, "iterations": iters, "items": idx.n, "tags": n_tags,
        "tags_per_item": round(n_tags / max(idx.n, 1), 2), "skipped": skipped,
        "nodes": len(g.ids), "edges": sum(len(v) for v in g.parents.values()), "roots": len(g.roots), "leaves": len(g.leaves),
        "nodes_with_items": sum(1 for y in g.ids if direct_sizes[y]), "pairs_with_items": len(idx.pair),
        "postings": {"direct": len(idx.direct), "pair": len(idx.pair), "closure": len(idx.closure)},
        "closure_size_top": sorted(closure_sizes.items(), key=lambda t: -t[1])[:15],
        "direct_size_top": sorted(direct_sizes.items(), key=lambda t: -t[1])[:15],
        "information_content_top": sorted(((y, round(g.ic[y], 2)) for y in g.ids if direct_sizes[y]), key=lambda t: -t[1])[:15],
        "by_source": dict(sorted(((s, sum(1 for it in idx.items if it.get("source") == s)) for s in {it.get("source") for it in idx.items}))),
        "build_seconds": round(time.perf_counter() - t0, 2),
    }
    return idx


def render_md(s: dict) -> str:
    lines = ["# Retrieval index", "",
             f"Catalogue v{s['catalogue_version']}, iterations {s['iterations']}: {s['items']} items, {s['tags']} tags "
             f"({s['tags_per_item']} per item), skipped {s['skipped']}. Sources: {s['by_source']}.",
             f"DAG: {s['nodes']} nodes, {s['edges']} edges, {s['roots']} roots, {s['leaves']} leaves; "
             f"{s['nodes_with_items']} nodes carry direct tags, {s['pairs_with_items']} (node, value) pairs are used.",
             f"Postings: {s['postings']}. Build time {s['build_seconds']} s.", "",
             "| largest closures | items | | most direct tags | items | | highest information content (bits) | IC |",
             "|---|---|---|---|---|---|---|---|"]
    for (a, na), (b, nb), (c, ic) in zip(s["closure_size_top"], s["direct_size_top"], s["information_content_top"]):
        lines.append(f"| `{a}` | {na} | | `{b}` | {nb} | | `{c}` | {ic} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--version", type=int, default=None)
    ap.add_argument("--iters", type=int, nargs="*", default=None)
    args = ap.parse_args()
    idx = build(args.version, args.iters)
    idx.save()
    OUT.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text(json.dumps(idx.stats, indent=1), encoding="utf-8")
    SUMMARY_MD.write_text(render_md(idx.stats), encoding="utf-8")
    s = idx.stats
    print(f"indexed {s['items']} items, {s['tags']} tags on v{s['catalogue_version']} ({s['nodes']} nodes) in {s['build_seconds']} s")
    print(f"-> {INDEX}\n-> {SUMMARY_MD}")


if __name__ == "__main__":
    # run through the imported module so the pickled Index class is taxonomy.retrieval.index.Index
    from taxonomy.retrieval.index import main as _main
    _main()
