"""LLM-judged matching of two catalogues of term types (which dimensions are the same question).

    python -m taxonomy.baselines.judge ours zeroshot [--judge-model claude-haiku-5-5]

The lexical matcher in establishment/agreement.py counts paraphrased dimensions as
disagreements, so it is a lower bound. Here the judge sees both catalogues (id, category, name,
question, values) and lists the pairs that ask the same question about the same kind of thing.
It is run in both directions (A then B, B then A) and only pairs found in both directions are
kept, then made one-to-one greedily in the judge's order. Reports precision of B, recall of A
and F1, like agreement.py, so the two can be compared.
"""
from __future__ import annotations

import argparse
import json

from taxonomy.baselines.common import OUT, Meter, compact, extract_json, llm, load_catalogue
from taxonomy.llm_context import client

JUDGE_INSTRUCTIONS = """\
You compare two catalogues of classification dimensions (term types) for crypto-asset and DLT \
content. Two term types MATCH when they ask the same question about the same kind of thing, so \
that their values would classify the same objects along the same axis, even if named or worded \
differently or if one lists more values than the other. They do not match when one is a \
broader or narrower question than the other, when they share values but ask different \
questions, or when they merely concern the same topic. Output valid JSON only.
"""

JUDGE_PROMPT = """\
Catalogue A:
{a}

Catalogue B:
{b}

List every matching pair (one-to-one: each id at most once). Return
{{"pairs": [{{"a": "<A id>", "b": "<B id>", "confidence": "high | medium"}}]}}
"""


def judge_pairs(cl, A: list[dict], B: list[dict], model: str, meter: Meter) -> list[dict]:
    """Intersection of the two directional judgements, one-to-one."""
    def one(X, Y):
        r = llm(cl, JUDGE_INSTRUCTIONS, JUDGE_PROMPT.format(a=compact(X), b=compact(Y)), model, "high", 16000, meter=meter)
        return [(str(p.get("a", "")).strip(), str(p.get("b", "")).strip(), p.get("confidence", "")) for p in extract_json(r["text"]).get("pairs", [])]
    ab = one(A, B)
    ba = {(b, a) for a, b, _ in one(B, A)}
    ids_a, ids_b = {t["id"] for t in A}, {t["id"] for t in B}
    used_a, used_b, out = set(), set(), []
    for a, b, c in ab:
        if (a, b) in ba and a in ids_a and b in ids_b and a not in used_a and b not in used_b:
            used_a.add(a)
            used_b.add(b)
            out.append({"a": a, "b": b, "confidence": c})
    return out


def judge(a_name: str, b_name: str, model: str, A: list[dict] | None = None, B: list[dict] | None = None) -> dict:
    A = A if A is not None else load_catalogue(a_name)["term_types"]
    B = B if B is not None else load_catalogue(b_name)["term_types"]
    meter = Meter(model)
    pairs = judge_pairs(client(), A, B, model, meter)
    n = len(pairs)
    return {"a": a_name, "b": b_name, "judge_model": model, "term_types_a": len(A), "term_types_b": len(B), "matched": n,
            "recall_of_a": round(n / max(len(A), 1), 3), "precision_of_b": round(n / max(len(B), 1), 3),
            "f1": round(2 * n / max(len(A) + len(B), 1), 3), "pairs": pairs,
            "unmatched_a": [t["id"] for t in A if t["id"] not in {p["a"] for p in pairs}],
            "unmatched_b": [t["id"] for t in B if t["id"] not in {p["b"] for p in pairs}], **meter.report()}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--judge-model", default="claude-haiku-5-5")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    res = judge(args.a, args.b, args.judge_model)
    dest = args.out or (OUT / "judged" / f"{args.a}__{args.b}.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{args.a} ({res['term_types_a']}) vs {args.b} ({res['term_types_b']}): matched {res['matched']}, F1 {res['f1']} "
          f"(recall of A {res['recall_of_a']}, precision of B {res['precision_of_b']}); ${res['cost_usd']} -> {dest}")


if __name__ == "__main__":
    main()
