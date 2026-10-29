"""RQ5 table: our catalogue against the baselines on size, faithfulness, agreement with ours
(lexical and LLM-judged), expert-key coverage, structure after Task B, downstream tagging,
and cost.

    python -m taxonomy.baselines.compare [--catalogues ours repeat zeroshot rag raptor tnt] [--judge-model claude-haiku-5-5]

Reads what the other modules wrote (term_types.json, dag.json, downstream.json), runs the
judge where its output is missing (output/baselines/judged/), and writes
output/baselines/rq5.{json,md} and paper/tables/rq5.tex.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from taxonomy.baselines.common import OUT, catalogue_path
from taxonomy.baselines.judge import judge
from taxonomy.establishment.agreement import compare as lexical
from taxonomy.evaluation.common import PAPER_TABLES, mean_sd
from taxonomy.llm_context import ROOT

NAMES = {"ours": "ours (whole corpus, one context)", "repeat": "ours, second run", "zeroshot": "zero-shot, no corpus",
         "rag": "chunked RAG (BM25, k=8)", "raptor": "RAPTOR (tree + BM25, k=8)", "tnt": "TnT-LLM (summarise, build, review)"}
PATHS = {"repeat": ROOT / "output" / "establishment" / "repeats" / "term_types.haiku_run2.json"}


def run_cost(run: dict) -> float | None:
    """cost_usd if recorded, else priced from the usage of a Task A run (SDK key names)."""
    if run.get("cost_usd") is not None:
        return run["cost_usd"]
    u = run.get("usage") or {}
    if not u:
        return None
    from taxonomy.evaluation.billing import price
    return round(price(u, run.get("model", "claude-haiku-5-5"), long_prompt=True)[0], 4)   # Task A: 235K-token corpus in context


def path_of(name: str) -> Path:
    return PATHS.get(name) or catalogue_path(name)


def load(name: str) -> dict:
    return json.loads(path_of(name).read_text(encoding="utf-8"))


def judged(a: str, b: str, model: str) -> dict:
    p = OUT / "judged" / f"{a}__{b}.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    res = judge(a, b, model, load(a)["term_types"], load(b)["term_types"])
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return res


def structure(name: str) -> dict | None:
    if name == "ours":
        d = json.loads((ROOT / "output" / "establishment" / "taxonomy_dag.json").read_text(encoding="utf-8"))
        from taxonomy.establishment.dag_metrics import summary
        return summary(d["metrics"]["overall"])
    p = OUT / name / "dag.json"
    return json.loads(p.read_text(encoding="utf-8"))["metrics"]["summary"] if p.exists() else None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--catalogues", nargs="*", default=["ours", "repeat", "zeroshot", "rag", "raptor", "tnt"])
    ap.add_argument("--judge-model", default="claude-haiku-5-5")
    a = ap.parse_args()
    down = json.loads((OUT / "downstream.json").read_text(encoding="utf-8"))["systems"] if (OUT / "downstream.json").exists() else {}
    key = load("expert_key")
    rows = {}
    for n in a.catalogues:
        if not path_of(n).exists():
            print(f"skip {n}: no catalogue")
            continue
        c = load(n)
        tts = c["term_types"]
        ver = json.loads(path_of(n).with_name(path_of(n).name.replace(".json", ".verification.json")).read_text(encoding="utf-8"))
        row = {"name": NAMES.get(n, n), "term_types": len(tts), "values": sum(len(t["values"]) for t in tts),
               "citations": ver["citations"], "citations_verified": ver["verified"],
               "verified_rate": round(ver["verified"] / ver["citations"], 3) if ver["citations"] else None,
               "cost_usd": run_cost(c["run"]), "wall_seconds": c["run"].get("wall_seconds") or c["run"].get("seconds") or c["run"].get("api_seconds"),
               "run": {k: c["run"].get(k) for k in ("model", "effort", "calls", "stop_reason")}}
        if n != "ours":
            lex = lexical(path_of("ours"), path_of(n))
            jd = judged("ours", n, a.judge_model)
            row["agreement_lexical"] = {"f1": lex["f1"], "recall_of_ours": lex["agreement_recall_of_a"], "precision": lex["agreement_precision_of_b"], "matched": lex["matched"]}
            row["agreement_judged"] = {"f1": jd["f1"], "recall_of_ours": jd["recall_of_a"], "precision": jd["precision_of_b"], "matched": jd["matched"]}
        jk = judged("expert_key", n, a.judge_model)
        row["expert_key"] = {"coverage": jk["recall_of_a"], "precision": jk["precision_of_b"], "matched": jk["matched"], "key_size": jk["term_types_a"]}
        row["structure"] = structure(n)
        if n in down:
            ms = [r["metrics"] for r in down[n]["runs"]]
            row["downstream"] = {"micro_f1": mean_sd([m["micro_f1"] for m in ms]), "macro_f1": mean_sd([m["macro_f1"] for m in ms]),
                                 "micro_p": mean_sd([m["micro_p"] for m in ms]), "micro_r": mean_sd([m["micro_r"] for m in ms]),
                                 "mapped_types": down[n]["mapped_types"], "runs": len(ms)}
        rows[n] = row
    res = {"judge_model": a.judge_model, "expert_key": {"size": len(key["term_types"]), "docs": key["run"].get("per_doc"),
                                                        "contaminated_for": [n for n in rows if n not in ("zeroshot",)]}, "catalogues": rows}
    (OUT / "rq5.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")

    def f(x, d=3):
        return "-" if x is None else (f"{x:.{d}f}" if isinstance(x, float) else str(x))

    md = ["# RQ5: our catalogue against expert taxonomies and LLM baselines", "",
          f"All catalogues from Haiku 5.5 on the same 24-document corpus (zero-shot sees only the document titles). Judge: {a.judge_model}, "
          "same-question matching in both directions, intersection. Expert key: the "
          f"{len(key['term_types'])} dimensions of the two taxonomy papers in the corpus (docs 1 and 2); contaminated for every corpus-based catalogue.", "",
          "| catalogue | term types | values | citations verified | agreement with ours, lexical F1 | judged F1 (recall of ours / precision) | expert coverage (precision) | bits/descent | AUC | eff. leaves | downstream type micro-F1 | macro-F1 | cost | time |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    tex = ["% generated by taxonomy.baselines.compare", "\\begin{tabular}{lrrrcccccc}", "\\toprule",
           "Catalogue & Types & Values & Cited & Agr.\\ F$_1$ & Expert cov. & Bits/desc. & AUC & Micro-F$_1$ & Macro-F$_1$ \\\\", "\\midrule"]
    PM_TEX = "$\\pm$"

    def ms(dw, key, sep):
        return f"{dw[key][0]:.3f} {sep} {dw[key][1]:.3f}" if dw else ("--" if sep == PM_TEX else "-")

    def ft(x, d=3):
        return "--" if x is None else f(x, d)

    for n, r in rows.items():
        aj, al, ek, st, dw = r.get("agreement_judged"), r.get("agreement_lexical"), r["expert_key"], r.get("structure") or {}, r.get("downstream")
        cited = f"{r['citations_verified']}/{r['citations']} ({r['verified_rate']:.0%})" if r["citations"] else "none"
        lex_s = f(al["f1"]) if al else "1 (self)"
        jud_s = f"{f(aj['f1'])} ({f(aj['recall_of_ours'])} / {f(aj['precision'])})" if aj else "1 (self)"
        md.append(f"| {r['name']} | {r['term_types']} | {r['values']} | {cited} | {lex_s} | {jud_s} | "
                  f"{f(ek['coverage'])} ({f(ek['precision'])}) | {f(st.get('bits_per_descent'), 2)} | {f(st.get('auc'))} | {f(st.get('effective_leaves'), 1)} | "
                  f"{ms(dw, 'micro_f1', '±')} | {ms(dw, 'macro_f1', '±')} | ${f(r['cost_usd'], 2)} | {f(r['wall_seconds'], 0)} s |")
        cited_tex = f"{r['verified_rate']:.0%}".replace("%", "\\%") if r["citations"] else "--"
        tex.append(f"{r['name']} & {r['term_types']} & {r['values']} & {cited_tex} & {f(aj['f1']) if aj else '--'} & {f(ek['coverage'], 2)} & "
                   f"{ft(st.get('bits_per_descent'), 2)} & {ft(st.get('auc'), 2)} & {ms(dw, 'micro_f1', PM_TEX)} & {ms(dw, 'macro_f1', PM_TEX)} " + chr(92) * 2)
    tex += ["\\bottomrule", "\\end{tabular}"]
    md += ["", "Columns: citations verified = Task A verifier over every quote (doc, section, verbatim); agreement = same-question matches with our catalogue "
           "(lexical: agreement.py; judged: both directions, intersection); expert coverage = share of the key's dimensions matched (precision = share of the catalogue's "
           "types that match a key dimension); structure after the unchanged Task B; downstream = type-level F1 tagging the 300 gold items with the catalogue "
           "(no is-a edges), baseline types mapped to gold types by the judge, mean ± sd over 3 runs."]
    (OUT / "rq5.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    PAPER_TABLES.mkdir(parents=True, exist_ok=True)
    (PAPER_TABLES / "rq5.tex").write_text("\n".join(tex) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
