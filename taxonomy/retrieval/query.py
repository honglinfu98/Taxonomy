"""Retrieve items from the DAG index with graph operations.

    python -m taxonomy.retrieval.query 'consensus_mechanism="proof of stake" AND privacy_enhancement' [-k 10]
    python -m taxonomy.retrieval.query --text "zero-knowledge proofs for private payments" [--llm]
    python -m taxonomy.retrieval.query --like paper:ecbd4b67...   [-k 10]
    python -m taxonomy.retrieval.query --node ledger_purpose        # describe a node and its facets

Query language (atoms combine with AND, OR, NOT and parentheses; a space is AND):
  node                 every item in the subtree of node (reachability closure of the is-a DAG)
  node!                items tagged directly at node only
  node=v3              items tagged at node with value code v3 (or node="value label")
  node~0.3             subtree of node restricted to descendants whose best is-a path strength
                       to node is at least 0.3 (product of Task B edge weights)
  @technology          every item with any tag in that category

Ranking: an item's score is the sum over positive atoms of its match strength, where a
direct or value match is the tag confidence and a closure match is max over the item's
tagged descendants d of confidence(d) x path_strength(d -> node). Facets: for the result set
the engine reports the child subtrees and value splits of the query nodes with the
expected narrowing in bits each would give (sum over options of p(option) x log2(n / |option|),
options picked in proportion to their size), i.e. the best next question to narrow the set, and the lowest common ancestors of the query nodes as the generalisation.
When fewer than k items match, the query is expanded to the nodes most similar to the
query nodes (weighted-path similarity) and the extra items are marked with the node they
came through.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import time
from collections import Counter, defaultdict

from taxonomy.retrieval.graph import iter_bits, popcount
from taxonomy.retrieval.index import Index, load

TOKEN = re.compile(r"""\s*(?:(\()|(\))|\b(AND|OR|NOT)\b|(@?[A-Za-z0-9_]+!?)(?:~(\d*\.?\d+))?(?:=(?:"([^"]*)"|([^\s()]+)))?)""")


class Atom:
    def __init__(self, text: str, strength: float | None, value: str | None):
        self.category = text[1:] if text.startswith("@") else None
        self.direct = text.endswith("!")
        self.node = text.rstrip("!") if not self.category else None
        self.min_strength = strength
        self.value = value
        self.text = text + (f"~{strength}" if strength is not None else "") + (f'="{value}"' if value else "")

    def __repr__(self) -> str:
        return self.text


def tokenize(q: str) -> list:
    out, pos = [], 0
    q = q.strip()
    while pos < len(q):
        m = TOKEN.match(q, pos)
        if not m or m.end() == pos:
            raise ValueError(f"cannot parse query at: {q[pos:pos + 30]!r}")
        pos = m.end()
        if m.group(1) or m.group(2):
            out.append(m.group(1) or m.group(2))
        elif m.group(3):
            out.append(m.group(3).upper())
        elif m.group(4):
            out.append(Atom(m.group(4), float(m.group(5)) if m.group(5) else None,
                            m.group(6) if m.group(6) is not None else m.group(7)))
    return out


def parse(tokens: list):
    """-> nested tuples ('AND'|'OR', a, b), ('NOT', a) or Atom."""
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def expr():
        left = conj()
        while peek() == "OR":
            nonlocal pos
            pos += 1
            left = ("OR", left, conj())
        return left

    def conj():
        nonlocal pos
        left = unary()
        while peek() is not None and peek() not in ("OR", ")"):
            if peek() == "AND":
                pos += 1
            left = ("AND", left, unary())
        return left

    def unary():
        nonlocal pos
        t = peek()
        if t == "NOT":
            pos += 1
            return ("NOT", unary())
        if t == "(":
            pos += 1
            e = expr()
            if peek() != ")":
                raise ValueError("missing )")
            pos += 1
            return e
        if isinstance(t, Atom):
            pos += 1
            return t
        raise ValueError(f"unexpected token {t!r}")

    tree = expr()
    if pos != len(tokens):
        raise ValueError(f"trailing tokens {tokens[pos:]}")
    return tree


class Engine:
    def __init__(self, idx: Index):
        self.idx = idx
        self.g = idx.graph

    # ---- atom evaluation -----------------------------------------------------------
    def resolve_value(self, node: str, raw: str) -> str:
        vals = self.idx.values[node]
        m = re.fullmatch(r"v(\d+)", raw)
        if m and 1 <= int(m.group(1)) <= len(vals):
            return vals[int(m.group(1)) - 1]
        low = raw.lower()
        for v in vals:
            if v.lower() == low:
                return v
        cands = [v for v in vals if low in v.lower()]
        if len(cands) == 1:
            return cands[0]
        raise ValueError(f"unknown value {raw!r} for {node}; values: " + "; ".join(f"v{i + 1}={v}" for i, v in enumerate(vals)))

    def atom_bits(self, a: Atom) -> int:
        idx, g = self.idx, self.g
        if a.category:
            if a.category not in idx.cat:
                raise ValueError(f"unknown category {a.category!r}")
            return idx.cat[a.category]
        if a.node not in g.pos:
            raise ValueError(f"unknown node {a.node!r}")
        if a.value is not None:
            return idx.pair.get((a.node, self.resolve_value(a.node, a.value)), 0)
        if a.direct:
            return idx.direct.get(a.node, 0)
        if a.min_strength is not None:
            b = 0
            for k in iter_bits(g.desc_bits[a.node]):
                d = g.ids[k]
                if g.path_strength(d, a.node) >= a.min_strength:
                    b |= idx.direct.get(d, 0)
            return b
        return idx.closure[a.node]

    def evaluate(self, tree) -> int:
        if isinstance(tree, Atom):
            return self.atom_bits(tree)
        op = tree[0]
        if op == "NOT":
            return self.idx.all & ~self.evaluate(tree[1])
        l, r = self.evaluate(tree[1]), self.evaluate(tree[2])
        return l & r if op == "AND" else l | r

    @staticmethod
    def positive_atoms(tree, neg: bool = False) -> list[Atom]:
        if isinstance(tree, Atom):
            return [] if neg else [tree]
        if tree[0] == "NOT":
            return Engine.positive_atoms(tree[1], not neg)
        return Engine.positive_atoms(tree[1], neg) + Engine.positive_atoms(tree[2], neg)

    # ---- ranking ---------------------------------------------------------------------
    def match_strength(self, i: int, a: Atom) -> tuple[float, str]:
        """(strength, via node) of item i for atom a."""
        idx, g = self.idx, self.g
        nodes = idx.item_nodes[i]
        if a.category:
            best = max(((c, nodes[n]) for n in nodes for c in [n] if g.category[n] == a.category), key=lambda t: t[1], default=(None, 0.0))
            return best[1], best[0]
        if a.value is not None:
            return idx.item_values[i].get((a.node, self.resolve_value(a.node, a.value)), 0.0), a.node
        if a.direct:
            return nodes.get(a.node, 0.0), a.node
        best, via = 0.0, a.node
        for d, c in nodes.items():
            s = c * g.path_strength(d, a.node)
            if s > best:
                best, via = s, d
        return best, via

    def rank(self, result: int, atoms: list[Atom], k: int) -> list[dict]:
        rows = []
        for i in iter_bits(result):
            score, via = 0.0, []
            for a in atoms:
                s, v = self.match_strength(i, a)
                score += s
                if v and v != a.node and v != a.category:
                    via.append(v)
            rows.append({"i": i, "score": round(score, 4), "via": sorted(set(via))})
        rows.sort(key=lambda r: (-r["score"], self.idx.items[r["i"]]["id"]))
        return rows[:k]

    # ---- facets: best next question over a result set -------------------------------------
    @staticmethod
    def narrowing_bits(n: int, counts: list[int]) -> float:
        """Expected bits of narrowing when an option is picked with probability proportional to its
        size: sum_o p_o * log2(n / m_o). Options may overlap (child subtrees); an option that covers
        the whole set narrows nothing and contributes 0."""
        tot = sum(counts)
        return sum(m / tot * math.log2(n / m) for m in counts if m) if tot and n else 0.0

    def facets(self, result: int, focus: list[str], top: int = 6) -> list[dict]:
        idx, g = self.idx, self.g
        n = popcount(result)
        out = []
        if not n:
            return out
        for y in focus:
            # child subtrees of y
            kids = [(c, popcount(idx.closure[c] & result), w) for c, w in g.children[y]]
            kids = [(c, m, w) for c, m, w in kids if m]
            if kids:
                covered = 0
                for c, _, _ in kids:
                    covered |= idx.closure[c] & result
                residual = n - popcount(covered)
                gain = self.narrowing_bits(n, [m for _, m, _ in kids] + [residual])
                out.append({"node": y, "kind": "child_term_types", "gain_bits": round(gain, 3),
                            "options": sorted(({"node": c, "items": m, "is_a_weight": w} for c, m, w in kids), key=lambda o: -o["items"]),
                            "residual": residual})
            # values of y
            vals = [(v, popcount(idx.pair.get((y, v), 0) & result)) for v in idx.values[y]]
            vals = [(v, m) for v, m in vals if m]
            if vals:
                untagged = n - popcount(idx.direct.get(y, 0) & result)
                gain = self.narrowing_bits(n, [m for _, m in vals] + [untagged])
                out.append({"node": y, "kind": "values", "gain_bits": round(gain, 3),
                            "options": sorted(({"value": v, "items": m} for v, m in vals), key=lambda o: -o["items"]),
                            "residual": untagged})
        out.sort(key=lambda f: -f["gain_bits"])
        return out[:top]

    def expand(self, result: int, atoms: list[Atom], need: int, per_node: int = 6) -> tuple[int, dict[int, tuple[str, float]]]:
        """Add items from nodes similar to the query nodes until `need` items; returns (bits, item -> (via, sim))."""
        extra: dict[int, tuple[str, float]] = {}
        cands = []
        for a in atoms:
            if a.node:
                for z, s in self.g.neighbours(a.node, per_node):
                    cands.append((s, z, a.node))
        cands.sort(key=lambda t: (-t[0], t[1]))
        bits = result
        for s, z, src in cands:
            if popcount(bits) >= need:
                break
            new = self.idx.closure[z] & ~bits
            for i in iter_bits(new):
                extra[i] = (z, round(s, 3))
            bits |= new
        return bits, extra

    # ---- item similarity ("more like this") --------------------------------------------
    def item_vector(self, i: int) -> dict[str, float]:
        g = self.g
        vec: dict[str, float] = {}
        for d, c in self.idx.item_nodes[i].items():
            for a, s in g.strength[d].items():
                w = c * s * g.ic[a]
                if w > vec.get(a, 0.0):
                    vec[a] = w
        return vec

    def similar(self, i: int, k: int) -> list[dict]:
        v = self.item_vector(i)
        nv = math.sqrt(sum(x * x for x in v.values())) or 1.0
        cand = 0
        for d in self.idx.item_nodes[i]:
            cand |= self.idx.direct.get(d, 0)
        rows = []
        for j in iter_bits(cand):
            if j == i:
                continue
            u = self.item_vector(j)
            dot = sum(x * u[a] for a, x in v.items() if a in u)
            nu = math.sqrt(sum(x * x for x in u.values())) or 1.0
            shared = sorted(set(self.idx.item_nodes[i]) & set(self.idx.item_nodes[j]))
            rows.append({"i": j, "score": round(dot / (nv * nu), 4), "via": shared})
        rows.sort(key=lambda r: (-r["score"], self.idx.items[r["i"]]["id"]))
        return rows[:k]

    # ---- free text to query ------------------------------------------------------------
    def route_text(self, text: str, top: int = 3) -> str:
        """Lexical routing: score nodes and values by idf-weighted token overlap with their labels."""
        toks = [t for t in re.findall(r"[a-z0-9]+", text.lower()) if len(t) > 2]
        docs: dict[tuple, set[str]] = {}
        for t in self.idx.tts:
            base = set(re.findall(r"[a-z0-9]+", " ".join([t["name"], t["question"], t.get("description", "")] + list(t.get("aliases") or [])).lower()))
            docs[(t["id"], None)] = base
            for v in t["values"]:
                docs[(t["id"], v["value"])] = set(re.findall(r"[a-z0-9]+", (v["value"] + " " + (v.get("definition") or "")).lower()))
        df = Counter(w for d in docs.values() for w in d)
        nd = len(docs)
        scored = []
        for key, words in docs.items():
            s = sum(math.log(nd / df[w]) for w in set(toks) if w in words)
            if s > 0:
                scored.append((s, key))
        scored.sort(key=lambda t: -t[0])
        atoms = []
        for s, (node, val) in scored[:top]:
            atoms.append(node if val is None else f'{node}="{val}"')
        return " OR ".join(atoms)

    def route_text_llm(self, text: str, model: str) -> str:
        from taxonomy.classification.tag import catalogue_block
        from taxonomy.llm_context import build_request, client
        instructions = ("You translate a retrieval request into a boolean query over a taxonomy catalogue. Atoms: a term type id "
                        "(all items in its subtree), id=\"value label\" (items with that value), combined with AND, OR, NOT and "
                        "parentheses. Use only ids and value labels from the catalogue. Answer with the query string only.")
        req = build_request(instructions, f"Request: {text}\nQuery:", model=model, max_tokens=300, effort="low", corpus=False,
                            extra_system=[catalogue_block(self.idx.tts, {"edges": [
                                {"child": c, "parent": p, "probability": w} for p, ch in self.g.children.items() for c, w in ch]})],
                            thinking={"type": "disabled"})
        msg = client().messages.create(**req)
        return "".join(b.text for b in msg.content if b.type == "text").strip().strip("`")

    # ---- the full query -----------------------------------------------------------------
    def search(self, q: str, k: int = 10, expand: bool = True, with_facets: bool = True) -> dict:
        t0 = time.perf_counter()
        tree = parse(tokenize(q))
        result = self.evaluate(tree)
        atoms = self.positive_atoms(tree)
        t_eval = time.perf_counter() - t0
        n = popcount(result)
        expanded: dict[int, tuple[str, float]] = {}
        bits = result
        if expand and n < k and atoms:
            bits, expanded = self.expand(result, atoms, k)
        ranked = self.rank(result, atoms, k)
        if expanded:
            ex_rows = []
            for i, (z, s) in expanded.items():
                strength, _ = self.match_strength(i, Atom(z, None, None))
                ex_rows.append({"i": i, "score": round(s * strength, 4), "via": [f"{z} (sim {s})"], "expanded": True})
            ex_rows.sort(key=lambda r: (-r["score"], self.idx.items[r["i"]]["id"]))
            ranked = (ranked + ex_rows)[:k]
        focus = list(dict.fromkeys([a.node for a in atoms if a.node]
                                   or [r for r in self.g.roots if any(a.category == self.g.category[r] for a in atoms)]))
        facets = self.facets(result, focus) if with_facets else []
        t_all = time.perf_counter() - t0
        return {"query": q, "atoms": [a.text for a in atoms], "matches": n, "expanded_to": popcount(bits) if expanded else None,
                "results": [self.describe(r) for r in ranked],
                "generalisation": self.g.lca([a.node for a in atoms if a.node]) if len({a.node for a in atoms if a.node}) > 1 else [],
                "facets": facets, "eval_us": round(t_eval * 1e6, 1), "total_ms": round(t_all * 1e3, 2)}

    def describe(self, r: dict) -> dict:
        it = self.idx.items[r["i"]]
        tags = sorted(self.idx.item_nodes[r["i"]].items(), key=lambda t: -t[1])
        return {"id": it["id"], "source": it.get("source"), "year": it.get("year"), "title": it.get("title"),
                "score": r["score"], "via": r["via"], "expanded": r.get("expanded", False),
                "tags": [{"node": y, "confidence": c, "evidence": self.idx.evidence.get((r["i"], y), "")} for y, c in tags[:4]]}

    def node_card(self, y: str) -> dict:
        idx, g = self.idx, self.g
        t = idx.by_id[y]
        return {"id": y, "name": t["name"], "question": t["question"], "category": g.category[y], "depth": g.depth[y],
                "status": t.get("status", "seed"), "direct_items": popcount(idx.direct.get(y, 0)), "closure_items": popcount(idx.closure[y]),
                "information_content_bits": round(g.ic[y], 3),
                "parents": [{"node": p, "weight": w} for p, w in g.parents[y]],
                "children": [{"node": c, "weight": w, "closure_items": popcount(idx.closure[c])} for c, w in g.children[y]],
                "values": [{"code": f"v{i + 1}", "value": v, "items": popcount(idx.pair.get((y, v), 0))} for i, v in enumerate(idx.values[y])],
                "similar_nodes": [{"node": z, "sim": round(s, 3)} for z, s in g.neighbours(y, 6)],
                "facets": self.facets(idx.closure[y], [y])}


# ---- CLI ---------------------------------------------------------------------------------
def print_search(res: dict, idx: Index, show_text: bool) -> None:
    print(f"query: {res['query']}   matches: {res['matches']}" + (f" (expanded to {res['expanded_to']})" if res.get("expanded_to") else "")
          + f"   eval {res['eval_us']} us, total {res['total_ms']} ms")
    if res["generalisation"]:
        print(f"generalisation (LCA of query nodes): {', '.join(res['generalisation'])}")
    for n, r in enumerate(res["results"], 1):
        via = f"  via {', '.join(r['via'])}" if r["via"] else ""
        print(f"{n:>3}. [{r['score']:.3f}] {r['id']} ({r['source']} {r.get('year') or ''}) {r['title']}{via}" + ("  [expanded]" if r["expanded"] else ""))
        for t in r["tags"][:2]:
            print(f"       {t['node']} ({t['confidence']}): {t['evidence'][:100]}")
        if show_text:
            print("       " + idx.item_text(idx.item_pos[r["id"]])[:600].replace("\n", " "))
    if res["facets"]:
        print("next facet (information gain over the result set):")
        for f in res["facets"][:4]:
            opts = ", ".join(f"{o.get('node') or o.get('value')} ({o['items']})" for o in f["options"][:5])
            print(f"  {f['gain_bits']:.2f} bits  {f['node']} / {f['kind']}: {opts}; residual {f['residual']}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("query", nargs="?", default=None)
    ap.add_argument("--text", default=None, help="free-text request routed to a query")
    ap.add_argument("--llm", action="store_true", help="route --text with the model instead of lexically")
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--like", default=None, help="item id: rank the most similar items")
    ap.add_argument("--node", default=None, help="describe a node: counts, parents, children, values, facets")
    ap.add_argument("-k", type=int, default=10)
    ap.add_argument("--no-expand", action="store_true")
    ap.add_argument("--no-facets", action="store_true")
    ap.add_argument("--show-text", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    idx = load()
    eng = Engine(idx)
    if args.node:
        card = eng.node_card(args.node)
        print(json.dumps(card, indent=1, ensure_ascii=False))
        return
    if args.like:
        i = idx.item_pos.get(args.like)
        if i is None:
            sys.exit(f"unknown item {args.like}")
        t0 = time.perf_counter()
        rows = eng.similar(i, args.k)
        out = {"like": idx.items[i]["title"], "results": [eng.describe(r) for r in rows], "total_ms": round((time.perf_counter() - t0) * 1e3, 2)}
        if args.json:
            print(json.dumps(out, indent=1, ensure_ascii=False))
        else:
            print(f"more like: {out['like']}   ({out['total_ms']} ms)")
            for n, r in enumerate(out["results"], 1):
                print(f"{n:>3}. [{r['score']:.3f}] {r['id']} ({r['source']} {r.get('year') or ''}) {r['title']}  shared: {', '.join(r['via'][:4])}")
        return
    q = args.query
    if args.text:
        q = eng.route_text_llm(args.text, args.model) if args.llm else eng.route_text(args.text)
        print(f"routed query: {q}")
    if not q:
        ap.error("give a query, --text, --like or --node")
    try:
        res = eng.search(q, args.k, expand=not args.no_expand, with_facets=not args.no_facets)
    except ValueError as e:
        sys.exit(f"query error: {e}")
    if args.json:
        print(json.dumps(res, indent=1, ensure_ascii=False))
    else:
        print_search(res, idx, args.show_text)


if __name__ == "__main__":
    main()
