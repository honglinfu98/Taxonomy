"""Metrics on the is-a DAG that the optimisation part (Part 3) will steer by.

The DAG is {child: [(parent, p), ...]} with p = P(child is-a parent) for every kept edge.
At a node y with children C(y), the edge weights are normalised into a branching
distribution q_y(c) = p(c->y) / sum over C(y). A *random descent* starts at a root, stops
at a leaf, and otherwise moves to a child drawn from q_y.

information_gain      per node: H(q_y) in bits, the information resolved by choosing one
                      child at y (0 for leaves and single-child nodes). `total_bits` sums
                      it over nodes; `bits_per_descent` is its expectation along a random
                      descent, i.e. how much a full walk root->leaf discriminates.
auc                   F(d) = P(a random descent has reached a leaf by depth d), d = 0..D.
                      auc = area under F over [0, D] divided by D (1.0 when every root is
                      a leaf; smaller when branches run deep). `expected_depth` is E[d].
leaves                leaf count, plus how many leaves the descents actually use:
                      `effective_leaves` = 2^H(r) where r is the distribution of the leaf a
                      descent ends at, and `leaves_for_90pct` = smallest number of leaves
                      holding 90% of that mass.
"""
from __future__ import annotations

import math

Parents = dict[str, list[tuple[str, float]]]


def _children(parents: Parents, ids: set[str]) -> dict[str, list[tuple[str, float]]]:
    kids: dict[str, list[tuple[str, float]]] = {i: [] for i in ids}
    for c in ids:
        for q, p in parents[c]:
            if q in ids:
                kids[q].append((c, p))
    return kids


def _entropy(ps: list[float]) -> float:
    return -sum(p * math.log2(p) for p in ps if p > 0)


def dag_metrics(parents: Parents, ids: list[str] | None = None) -> dict:
    """Metrics for the sub-DAG induced by `ids` (default: every node)."""
    ids_set = set(ids) if ids is not None else set(parents)
    if not ids_set:
        return {}
    kids = _children(parents, ids_set)
    roots = [i for i in ids_set if not any(q in ids_set for q, _ in parents[i])]
    leaves = [i for i in ids_set if not kids[i]]

    # branching distributions and per-node information gain
    q: dict[str, list[tuple[str, float]]] = {}
    ig: dict[str, float] = {}
    for y in ids_set:
        tot = sum(p for _, p in kids[y])
        q[y] = [(c, p / tot) for c, p in kids[y]] if tot > 0 else []
        ig[y] = _entropy([w for _, w in q[y]])

    # random descent: probability mass reaching each node at each depth
    # mass[d][node]; roots uniform at depth 0
    mass = [{r: 1.0 / len(roots) for r in roots}]
    reach_leaf: dict[str, float] = {}
    stopped_by_depth: list[float] = []
    bits = 0.0
    depth_sum = 0.0
    d = 0
    while mass[d]:
        nxt: dict[str, float] = {}
        stopped = 0.0
        for y, m in mass[d].items():
            if not q[y]:
                reach_leaf[y] = reach_leaf.get(y, 0.0) + m
                stopped += m
                depth_sum += m * d
            else:
                bits += m * ig[y]
                for c, w in q[y]:
                    nxt[c] = nxt.get(c, 0.0) + m * w
        stopped_by_depth.append(stopped)
        mass.append(nxt)
        d += 1
        if d > len(ids_set):           # safety: a DAG cannot be deeper than its node count
            break
    D = len(stopped_by_depth) - 1       # max depth at which a descent can stop
    F = []
    acc = 0.0
    for s in stopped_by_depth:
        acc += s
        F.append(acc)
    auc = 1.0 if D == 0 else sum((F[i] + F[i + 1]) / 2 for i in range(D)) / D

    r = sorted(reach_leaf.values(), reverse=True)
    eff = 2 ** _entropy(r)
    acc, n90 = 0.0, 0
    for v in r:
        acc += v
        n90 += 1
        if acc >= 0.9 - 1e-12:
            break

    return {
        "nodes": len(ids_set), "edges": sum(1 for c in ids_set for q_, _ in parents[c] if q_ in ids_set),
        "roots": len(roots), "leaves": len(leaves), "max_depth": D,
        "information_gain": {"total_bits": round(sum(ig.values()), 4), "bits_per_descent": round(bits, 4),
                             "per_node": {y: round(v, 4) for y, v in ig.items() if v > 0}},
        "auc": {"value": round(auc, 4), "expected_depth": round(depth_sum, 4),
                "reach_leaf_by_depth": [round(x, 4) for x in F]},
        "leaves_needed": {"leaves": len(leaves), "effective_leaves": round(eff, 3), "leaves_for_90pct": n90,
                          "leaf_mass": {k: round(v, 4) for k, v in sorted(reach_leaf.items(), key=lambda kv: -kv[1])}},
    }


def summary(m: dict) -> dict:
    """The scalar part of dag_metrics, for tables and the threshold spectrum."""
    if not m:
        return {}
    return {"nodes": m["nodes"], "edges": m["edges"], "roots": m["roots"], "leaves": m["leaves"],
            "max_depth": m["max_depth"], "total_bits": m["information_gain"]["total_bits"],
            "bits_per_descent": m["information_gain"]["bits_per_descent"], "auc": m["auc"]["value"],
            "expected_depth": m["auc"]["expected_depth"], "effective_leaves": m["leaves_needed"]["effective_leaves"],
            "leaves_for_90pct": m["leaves_needed"]["leaves_for_90pct"]}
