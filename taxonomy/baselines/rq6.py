"""RQ6 table: how much do the manifest, the grounding strategy, the prompt and the model matter?

    python -m taxonomy.baselines.rq6 [--judge-model claude-haiku-5-5]

Rows are Task A runs that differ from the main run in one ingredient: the model repeats in
output/establishment/repeats/ (Haiku second run, Sonnet 5.5 at high and medium effort) and the
prompt ablations in output/ablations/ (ablate.py). Each row is scored like an RQ5 baseline:
size, citation verification and label accuracy, agreement with the main run (lexical and
LLM-judged), coverage of the expert key, cost and time. Judge outputs are cached in
output/baselines/judged/. Writes output/ablations/rq6.{json,md} and paper/tables/rq6.tex.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from taxonomy.baselines.ablate import OUT as ABL
from taxonomy.baselines.common import OUT, catalogue_path
from taxonomy.baselines.judge import judge
from taxonomy.establishment.agreement import compare as lexical
from taxonomy.evaluation.billing import price
from taxonomy.evaluation.common import PAPER_TABLES
from taxonomy.llm_context import ROOT

REP = ROOT / "output" / "establishment" / "repeats"
ROWS = [  # (name, judge cache key, group, label)
    ("ours", "ours", "reference", "full prompt, Haiku 5.5, effort high (main run)"),
    ("haiku_run2", "repeat", "model", "same prompt, Haiku 5.5, second run"),
    ("sonnet_medium", "sonnet_medium", "model", "same prompt, Sonnet 5.5, effort medium"),
    ("sonnet", "sonnet", "model", "same prompt, Sonnet 5.5, effort high (truncated at the output limit)"),
    ("effort_low", "effort_low", "prompt", "same prompt, Haiku 5.5, effort low"),
    ("no_manifest", "no_manifest", "manifest", "no manifest of section labels"),
    ("no_definitions", "no_definitions", "prompt", "no definitions of term, term type, grounded"),
    ("no_citations", "no_citations", "grounding", "no citation requirement"),
]
PATHS = {"ours": catalogue_path("ours"), "haiku_run2": REP / "term_types.haiku_run2.json", "sonnet": REP / "term_types.sonnet.json",
         "sonnet_medium": REP / "term_types.sonnet_medium.json"}


def path_of(name: str) -> Path:
    return PATHS.get(name) or ABL / name / "term_types.json"


def load(name: str) -> dict:
    return json.loads(path_of(name).read_text(encoding="utf-8"))


def judged(a: str, b_key: str, b_name: str, model: str) -> dict:
    p = OUT / "judged" / f"{a}__{b_key}.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    A = load("ours")["term_types"] if a == "ours" else json.loads(catalogue_path(a).read_text(encoding="utf-8"))["term_types"]
    res = judge(a, b_key, model, A, load(b_name)["term_types"])
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return res


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--judge-model", default="claude-haiku-5-5")
    a = ap.parse_args()
    key = json.loads(catalogue_path("expert_key").read_text(encoding="utf-8"))
    rows = []
    for name, ck, group, label in ROWS:
        if not path_of(name).exists():
            print(f"skip {name}: no run")
            continue
        c = load(name)
        tts, run = c["term_types"], c["run"]
        ver = json.loads(path_of(name).with_name(path_of(name).name.replace(".json", ".verification.json")).read_text(encoding="utf-8"))
        cost = run.get("cost_usd") if run.get("cost_usd") is not None else round(price(run["usage"], run["model"], long_prompt=True)[0], 4)
        row = {"name": name, "group": group, "label": label, "model": run["model"], "effort": run.get("effort"), "stop_reason": run.get("stop_reason"),
               "term_types": len(tts), "values": sum(len(t.get("values", [])) for t in tts),
               "citations": ver["citations"], "citations_verified": ver["verified"], "citations_exact": ver["exact"],
               "verified_rate": round(ver["verified"] / ver["citations"], 3) if ver["citations"] else None,
               "label_exact_rate": round(ver["exact"] / ver["citations"], 3) if ver["citations"] else None,
               "cost_usd": cost, "seconds": run.get("seconds")}
        if name != "ours":
            lex = lexical(path_of("ours"), path_of(name))
            jd = judged("ours", ck, name, a.judge_model)
            row["agreement_lexical"] = {"f1": lex["f1"], "matched": lex["matched"]}
            row["agreement_judged"] = {"f1": jd["f1"], "recall_of_ours": jd["recall_of_a"], "precision": jd["precision_of_b"], "matched": jd["matched"]}
        jk = judged("expert_key", ck, name, a.judge_model)
        row["expert_key"] = {"coverage": jk["recall_of_a"], "precision": jk["precision_of_b"], "matched": jk["matched"]}
        rows.append(row)
    res = {"judge_model": a.judge_model, "expert_key_size": len(key["term_types"]), "rows": rows}
    (ABL / "rq6.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")

    def f(x, d=3, blank="-"):
        return blank if x is None else (f"{x:.{d}f}" if isinstance(x, float) else str(x))

    md = ["# RQ6: how much do the manifest, grounding strategy, prompt and model matter?", "",
          f"Each row is one Task A run over the same cached corpus that differs from the main run in one ingredient. Judge: {a.judge_model} "
          "(same-question matching, both directions, intersection). Expert key: the "
          f"{len(key['term_types'])} dimensions of the two taxonomy papers in the corpus (contaminated: both papers are in the corpus).", "",
          "| variant | group | term types | values | citations verified | section label exact | agreement with main run: lexical F1 | judged F1 (recall of main / precision) | expert coverage (precision) | cost | time |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    tex = ["% generated by taxonomy.baselines.rq6", "\\begin{tabular}{llrrrrccc}", "\\toprule",
           "Ingredient & Variant & Types & Values & Cited & Label exact & Agr.\\ $F_1$ & Expert cov. & USD \\\\", "\\midrule"]
    for r in rows:
        aj, al, ek = r.get("agreement_judged"), r.get("agreement_lexical"), r["expert_key"]
        cited = f"{r['citations_verified']}/{r['citations']} ({r['verified_rate']:.0%})" if r["citations"] else "none"
        md.append(f"| {r['label']} | {r['group']} | {r['term_types']} | {r['values']} | {cited} | {f(r['label_exact_rate'])} | "
                  f"{f(al['f1']) if al else '1 (self)'} | {f(aj['f1']) + ' (' + f(aj['recall_of_ours']) + ' / ' + f(aj['precision']) + ')' if aj else '1 (self)'} | "
                  f"{f(ek['coverage'])} ({f(ek['precision'])}) | ${f(r['cost_usd'], 2)} | {f(r['seconds'], 0)} s |")
        cited_tex = f"{r['verified_rate']:.0%}".replace("%", "\\%") if r["citations"] else "--"
        lab_tex = f"{r['label_exact_rate']:.0%}".replace("%", "\\%") if r["citations"] else "--"
        tex.append(f"{r['group']} & {r['label']} & {r['term_types']} & {r['values']} & {cited_tex} & {lab_tex} & "
                   f"{f(aj['f1'], 2) if aj else '--'} & {f(ek['coverage'], 2)} & {f(r['cost_usd'], 2)} " + chr(92) * 2)
    tex += ["\\bottomrule", "\\end{tabular}"]
    md += ["", "Columns: citations verified = Task A verifier (document and section exist, quote verbatim); section label exact = share of citations whose "
           "section label needed no relabelling; agreement = same-question matches with the main run; expert coverage = share of the key's dimensions matched "
           "(precision = share of the variant's types that match a key dimension). Cost at the Haiku long-prompt card (Sonnet at its list card)."]
    (ABL / "rq6.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    PAPER_TABLES.mkdir(parents=True, exist_ok=True)
    (PAPER_TABLES / "rq6.tex").write_text("\n".join(tex) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
