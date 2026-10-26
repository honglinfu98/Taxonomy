"""Agreement between two Task A runs (same prompt, same or different model).

    python -m taxonomy.establishment.agreement output/establishment/term_types.json output/establishment/repeats/term_types.haiku_run2.json

Term types are matched greedily, within the same category first, by the similarity of their
name + question (difflib ratio on normalised text; threshold 0.55) and alias overlap; values of
matched term types are matched by label (exact after normalisation, else ratio >= 0.8).
Reports: term types in each run, matched, agreement = matched / run A (recall of A's types)
and matched / run B (precision of B's types), the mean value agreement (Jaccard) over matched
pairs, the citation verification rate of each run, and the unmatched term types.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
from pathlib import Path


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", " ", (s or "").lower()).strip()


def sim(a: dict, b: dict) -> float:
    ta = norm(a["name"] + " " + a.get("question", ""))
    tb = norm(b["name"] + " " + b.get("question", ""))
    r = difflib.SequenceMatcher(None, ta, tb).ratio()
    al = {norm(x) for x in (a.get("aliases") or [])} | {norm(a["name"])}
    bl = {norm(x) for x in (b.get("aliases") or [])} | {norm(b["name"])}
    if al & bl:
        r = max(r, 0.9)
    if norm(a["id"].replace("_", " ")) == norm(b["id"].replace("_", " ")):
        r = 1.0
    return r


def match_values(va: list[str], vb: list[str]) -> tuple[int, int, int]:
    na, nb = [norm(v) for v in va], [norm(v) for v in vb]
    used, hit = set(), 0
    for x in na:
        best, bi = 0.0, -1
        for j, y in enumerate(nb):
            if j in used:
                continue
            r = 1.0 if x == y else difflib.SequenceMatcher(None, x, y).ratio()
            if r > best:
                best, bi = r, j
        if best >= 0.8:
            used.add(bi)
            hit += 1
    return hit, len(na), len(nb)


def compare(a_path: Path, b_path: Path, threshold: float = 0.55) -> dict:
    A = json.loads(a_path.read_text(encoding="utf-8"))
    B = json.loads(b_path.read_text(encoding="utf-8"))
    ta, tb = A["term_types"], B["term_types"]
    pairs = []
    for i, x in enumerate(ta):
        for j, y in enumerate(tb):
            s = sim(x, y)
            if s >= threshold:
                pairs.append((s + (0.05 if x.get("applies_to") == y.get("applies_to") else 0.0), i, j))
    pairs.sort(reverse=True)
    used_a, used_b, matched = set(), set(), []
    for s, i, j in pairs:
        if i in used_a or j in used_b:
            continue
        used_a.add(i)
        used_b.add(j)
        hit, na, nb = match_values([v["value"] for v in ta[i]["values"]], [v["value"] for v in tb[j]["values"]])
        matched.append({"a": ta[i]["id"], "b": tb[j]["id"], "similarity": round(min(s, 1.0), 3), "same_category": ta[i].get("applies_to") == tb[j].get("applies_to"),
                        "values_a": na, "values_b": nb, "values_matched": hit, "value_jaccard": round(hit / max(na + nb - hit, 1), 3)})

    def verif(p: Path) -> dict | None:
        v = p.with_name(p.name.replace(".json", ".verification.json"))
        if not v.exists():
            return None
        r = json.loads(v.read_text(encoding="utf-8"))
        return {k: r.get(k) for k in ("citations", "verified", "exact", "relabelled", "rejection_rate")}

    out = {"a": str(a_path), "b": str(b_path), "model_a": A.get("run", {}).get("model"), "model_b": B.get("run", {}).get("model"),
           "term_types_a": len(ta), "term_types_b": len(tb), "matched": len(matched),
           "agreement_recall_of_a": round(len(matched) / max(len(ta), 1), 3), "agreement_precision_of_b": round(len(matched) / max(len(tb), 1), 3),
           "f1": round(2 * len(matched) / max(len(ta) + len(tb), 1), 3),
           "same_category_share": round(sum(m["same_category"] for m in matched) / max(len(matched), 1), 3),
           "values_a": sum(len(t["values"]) for t in ta), "values_b": sum(len(t["values"]) for t in tb),
           "mean_value_jaccard": round(sum(m["value_jaccard"] for m in matched) / max(len(matched), 1), 3),
           "values_matched_total": sum(m["values_matched"] for m in matched),
           "verification_a": verif(a_path), "verification_b": verif(b_path),
           "usage_b": B.get("run", {}).get("usage"), "seconds_b": B.get("run", {}).get("seconds"),
           "unmatched_a": [t["id"] for i, t in enumerate(ta) if i not in used_a],
           "unmatched_b": [t["id"] for j, t in enumerate(tb) if j not in used_b], "pairs": matched}
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--threshold", type=float, default=0.55)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out = compare(Path(args.a), Path(args.b), args.threshold)
    dest = Path(args.out) if args.out else Path(args.b).with_name(Path(args.b).stem + ".agreement.json")
    dest.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{out['model_a']} ({out['term_types_a']} types) vs {out['model_b']} ({out['term_types_b']} types): matched {out['matched']}, "
          f"agreement F1 {out['f1']} (recall of A {out['agreement_recall_of_a']}, precision of B {out['agreement_precision_of_b']}), "
          f"mean value Jaccard {out['mean_value_jaccard']}; unmatched A {len(out['unmatched_a'])}, B {len(out['unmatched_b'])}")
    print(f"-> {dest}")


if __name__ == "__main__":
    main()
