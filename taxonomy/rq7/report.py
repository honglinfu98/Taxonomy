"""RQ7 table and failure cases.

    python -m taxonomy.rq7.report

Reads classify_<system>.json, supervised.json and the prediction files; writes
output/rq7/rq7.{json,md}, output/rq7/failure_cases.md and paper/tables/rq7.tex.
"""
from __future__ import annotations

import json
from collections import Counter

from taxonomy.evaluation.common import PAPER_TABLES, mean_sd, read_jsonl
from taxonomy.rq7.labels import ITEMS, LABELS, OUT

NAMES = {"text": "LLM, description only (no ontology)", "onto": "LLM, description + catalogue (ontology as context)",
         "tags": "LLM, ontology tags only (no description)", "tfidf": "LR on TF-IDF words",
         "ontology_tags": "LR on ontology tags", "tfidf+ontology_tags": "LR on words + ontology tags"}


PM = "$" + chr(92) + "pm$"


def ms(x, sep="±", d=3):
    return f"{x[0]:.{d}f} {sep} {x[1]:.{d}f}"


def main() -> None:
    lab = json.loads(LABELS.read_text(encoding="utf-8"))
    items = read_jsonl(ITEMS)
    rows = {}
    for s in ("text", "onto", "tags"):
        p = OUT / f"classify_{s}.json"
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        m = [r["metrics"] for r in d["runs"]]
        rows[s] = {"kind": "llm", "model": d["runs"][0]["run_info"]["model"], "runs": len(m),
                   "micro_f1": mean_sd([x["micro_f1"] for x in m]), "macro_f1": mean_sd([x["macro_f1"] for x in m]),
                   "micro_p": mean_sd([x["micro_p"] for x in m]), "micro_r": mean_sd([x["micro_r"] for x in m]),
                   "pred_per_item": mean_sd([x["pred_per_item"] for x in m]),
                   "cost_usd": round(sum(r["run_info"]["cost_usd"] + r["run_info"].get("tagger", {}).get("cost_usd", 0) for r in d["runs"]), 2)}
    sup = json.loads((OUT / "supervised.json").read_text(encoding="utf-8")) if (OUT / "supervised.json").exists() else {"systems": {}}
    for s, d in sup["systems"].items():
        m = d["runs"]
        rows[s] = {"kind": "supervised", "model": f"{sup['folds']}-fold CV", "runs": len(m), "micro_f1": tuple(d["micro_f1"]), "macro_f1": tuple(d["macro_f1"]),
                   "micro_p": mean_sd([x["micro_p"] for x in m]), "micro_r": mean_sd([x["micro_r"] for x in m]),
                   "pred_per_item": mean_sd([x["pred_per_item"] for x in m]), "cost_usd": 0.0}
    # per-label F1 for the LLM systems (run 1) and the failure cases
    per_label, cases = {}, {"text_right_onto_wrong": [], "onto_right_text_wrong": [], "tags_right_text_wrong": []}
    preds = {s: {r["item_id"]: r for r in read_jsonl(OUT / f"pred_{s}_run1.jsonl")} for s in rows if rows[s]["kind"] == "llm"}
    for s, pr in preds.items():
        c = {}
        for it in items:
            g, p = set(it["gold"]), set(pr[it["id"]]["pred"])
            for l in g | p:
                x = c.setdefault(l, [0, 0, 0])
                x[0 if l in g and l in p else 1 if l in p else 2] += 1
        per_label[s] = {l: round(2 * tp / max(2 * tp + fp + fn, 1), 3) for l, (tp, fp, fn) in c.items() if l in lab["labels"]}
    if "text" in preds and "onto" in preds:
        for it in items:
            g = set(it["gold"])
            t, o = set(preds["text"][it["id"]]["pred"]), set(preds["onto"][it["id"]]["pred"])
            rec = {"id": it["id"], "title": it["title"], "gold": sorted(g), "text": sorted(t), "onto": sorted(o),
                   "dimensions": preds["onto"][it["id"]].get("dimensions", [])[:8], "snippet": it["text"][:300]}
            if t == g and o != g:
                cases["text_right_onto_wrong"].append(rec)
            elif o == g and t != g:
                cases["onto_right_text_wrong"].append(rec)
            if "tags" in preds:
                k = set(preds["tags"][it["id"]]["pred"])
                if k == g and t != g:
                    cases["tags_right_text_wrong"].append({**rec, "tags": sorted(k)})
    res = {"items": len(items), "items_with_gold": lab["items_with_gold"], "labels": len(lab["labels"]), "label_counts": lab["labels"],
           "systems": rows, "per_label_f1_run1": per_label, "failure_case_counts": {k: len(v) for k, v in cases.items()}}
    (OUT / "rq7.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")

    md = ["# RQ7: site categories from Web token descriptions, with and without the ontology", "",
          f"{len(items)} CoinGecko token descriptions (top coins by market cap with >= {lab['min_words']} words of description), "
          f"{lab['items_with_gold']} with at least one of the {len(lab['labels'])} retained site categories (categories carried by >= {lab['min_count']} items, "
          "ecosystem / index / portfolio / listing categories excluded). Gold = the site's own categories. LLM systems: Haiku 5.5, 3 runs, mean ± sd; "
          f"supervised: {sup.get('folds', '-')}-fold CV, {sup.get('seeds', '-')} shuffles. Catalogue v6 (132 term types, 320 edges).", "",
          "| system | micro-F1 | macro-F1 | P | R | pred/item | cost |", "|---|---|---|---|---|---|---|"]
    tex = ["% generated by taxonomy.rq7.report", "\\begin{tabular}{lcccc}", "\\toprule", "System & Micro-$F_1$ & Macro-$F_1$ & P & R \\\\", "\\midrule"]
    for s, r in rows.items():
        md.append(f"| {NAMES[s]} | {ms(r['micro_f1'])} | {ms(r['macro_f1'])} | {ms(r['micro_p'])} | {ms(r['micro_r'])} | {ms(r['pred_per_item'], d=2)} | ${r['cost_usd']:.2f} |")
        tex.append(f"{NAMES[s]} & {ms(r['micro_f1'], PM)} & {ms(r['macro_f1'], PM)} & {r['micro_p'][0]:.3f} & {r['micro_r'][0]:.3f} " + chr(92) * 2)
    tex += ["\\bottomrule", "\\end{tabular}"]
    if per_label:
        md += ["", "Per-label F1 (run 1), labels by frequency:", "", "| label | n | " + " | ".join(s for s in per_label) + " |", "|---|---|" + "---|" * len(per_label)]
        for l, n in lab["labels"].items():
            md.append(f"| {l} | {n} | " + " | ".join(f"{per_label[s].get(l, 0.0):.2f}" for s in per_label) + " |")
    md += ["", "Failure cases: " + ", ".join(f"{k} {len(v)}" for k, v in cases.items()) + " (see failure_cases.md)."]
    (OUT / "rq7.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    PAPER_TABLES.mkdir(parents=True, exist_ok=True)
    (PAPER_TABLES / "rq7.tex").write_text("\n".join(tex) + "\n", encoding="utf-8")
    fc = ["# RQ7 failure cases (run 1)", ""]
    for k, v in cases.items():
        fc += [f"## {k} ({len(v)})", ""]
        for rec in v[:6]:
            fc += [f"**{rec['title']}** ({rec['id']}): gold {rec['gold']}; text-only {rec['text']}; with catalogue {rec['onto']}"
                   + (f"; tags-only {rec['tags']}" if "tags" in rec else ""),
                   f"- dimensions claimed: {', '.join(d['term_type'] + '=' + str(d.get('value')) for d in rec['dimensions']) or '-'}",
                   f"- text: {rec['snippet']}...", ""]
    (OUT / "failure_cases.md").write_text("\n".join(fc) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
