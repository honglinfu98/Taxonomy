"""Graph-theoretic structure of the taxonomy DAG used for retrieval.

All sets of nodes are Python-int bitsets over the node index (bit i = node i), so
reachability tests and set algebra are single integer operations.

- transitive closure (descendants / ancestors) by dynamic programming in topological order;
- best is-a path strength s(d, a) = max over paths d -> ... -> a of the product of edge
  weights (the Task B probabilities), by relaxation on the ancestor subgraph;
- lowest common ancestors of a set of nodes (the common ancestors not dominated by
  another common ancestor), used to generalise a multi-node query;
- information content IC(y) = -log2 |C(y)| / N from the index, and the derived node
  similarities (Resnik, Lin, weighted-path), used for query expansion.
"""
from __future__ import annotations

import math
from collections import defaultdict


def bits(idx) -> int:
    x = 0
    for i in idx:
        x |= 1 << i
    return x


def iter_bits(x: int):
    while x:
        low = x & -x
        yield low.bit_length() - 1
        x ^= low


def popcount(x: int) -> int:
    return x.bit_count()


class TaxonomyGraph:
    def __init__(self, dag: dict):
        self.ids: list[str] = [n["id"] for n in dag["nodes"]]
        self.pos: dict[str, int] = {i: k for k, i in enumerate(self.ids)}
        self.node: dict[str, dict] = {n["id"]: n for n in dag["nodes"]}
        self.category: dict[str, str] = {n["id"]: n["category"] for n in dag["nodes"]}
        self.parents: dict[str, list[tuple[str, float]]] = defaultdict(list)
        self.children: dict[str, list[tuple[str, float]]] = defaultdict(list)
        for e in dag["edges"]:
            w = e.get("probability")
            w = 1.0 if w is None else float(w)
            self.parents[e["child"]].append((e["parent"], w))
            self.children[e["parent"]].append((e["child"], w))
        self.roots = [i for i in self.ids if not self.parents[i]]
        self.leaves = [i for i in self.ids if not self.children[i]]
        self.topo = self._topological()          # parents before children
        self.depth = self._depths()
        self.desc_bits, self.anc_bits = self._closures()
        self.strength = self._strengths()        # strength[d][a] = best path product d -> a (a ancestor of d), 1 at d

    # ---- structure -------------------------------------------------------------------
    def _topological(self) -> list[str]:
        indeg = {i: len(self.parents[i]) for i in self.ids}
        order, frontier = [], [i for i in self.ids if indeg[i] == 0]
        while frontier:
            x = frontier.pop(0)
            order.append(x)
            for c, _ in self.children[x]:
                indeg[c] -= 1
                if indeg[c] == 0:
                    frontier.append(c)
        if len(order) != len(self.ids):
            raise ValueError("DAG expected, cycle found")
        return order

    def _depths(self) -> dict[str, int]:
        d = {}
        for x in self.topo:
            d[x] = 0 if not self.parents[x] else 1 + max(d[p] for p, _ in self.parents[x])
        return d

    def _closures(self) -> tuple[dict[str, int], dict[str, int]]:
        desc: dict[str, int] = {}
        for x in reversed(self.topo):
            b = 1 << self.pos[x]
            for c, _ in self.children[x]:
                b |= desc[c]
            desc[x] = b
        anc: dict[str, int] = {}
        for x in self.topo:
            b = 1 << self.pos[x]
            for p, _ in self.parents[x]:
                b |= anc[p]
            anc[x] = b
        return desc, anc

    def _strengths(self) -> dict[str, dict[str, float]]:
        out: dict[str, dict[str, float]] = {}
        for d in self.ids:
            best = {d: 1.0}
            frontier = [d]
            while frontier:
                x = frontier.pop()
                for p, w in self.parents[x]:
                    s = best[x] * w
                    if s > best.get(p, 0.0):
                        best[p] = s
                        frontier.append(p)
            out[d] = best
        return out

    # ---- queries on the structure -------------------------------------------------------
    def descendants(self, y: str) -> int:
        return self.desc_bits[y]

    def ancestors(self, y: str) -> int:
        return self.anc_bits[y]

    def is_ancestor(self, a: str, d: str) -> bool:
        return bool(self.anc_bits[d] >> self.pos[a] & 1)

    def common_ancestors(self, nodes: list[str]) -> int:
        b = -1
        for n in nodes:
            b &= self.anc_bits[n]
        return b if nodes else 0

    def lca(self, nodes: list[str]) -> list[str]:
        """Lowest common ancestors: common ancestors that are not a proper ancestor of another."""
        ca = [self.ids[i] for i in iter_bits(self.common_ancestors(nodes))]
        return [a for a in ca if not any(b != a and self.is_ancestor(a, b) for b in ca)]

    def path_strength(self, d: str, a: str) -> float:
        return self.strength[d].get(a, 0.0)

    # ---- information content and similarity (need item counts from the index) ----------------
    def set_counts(self, closure_count: dict[str, int], n_items: int) -> None:
        self.n_items = n_items
        self.ic = {y: -math.log2(max(closure_count.get(y, 0), 0.5) / max(n_items, 1)) for y in self.ids}

    def resnik(self, a: str, b: str) -> float:
        return max((self.ic[self.ids[i]] for i in iter_bits(self.common_ancestors([a, b]))), default=0.0)

    def lin(self, a: str, b: str) -> float:
        den = self.ic[a] + self.ic[b]
        return 2 * self.resnik(a, b) / den if den > 0 else 0.0

    def weighted_sim(self, a: str, b: str) -> float:
        """max over common ancestors c of s(a,c) * s(b,c): how strongly both are kinds of one thing."""
        if a == b:
            return 1.0
        return max((self.strength[a][c] * self.strength[b][c] for c in self.strength[a] if c in self.strength[b]), default=0.0)

    def neighbours(self, y: str, k: int = 8) -> list[tuple[str, float]]:
        """Nodes ranked by weighted similarity to y (excluding y), for query expansion."""
        sims = [(z, self.weighted_sim(y, z)) for z in self.ids if z != y]
        sims = [(z, s) for z, s in sims if s > 0]
        sims.sort(key=lambda t: (-t[1], t[0]))
        return sims[:k]
