"""Tagging accuracy against the gold set: Micro-F1 and Macro-F1 over (term type, value) labels
and over term types, three systems, several runs with standard deviation.

    python -m taxonomy.evaluation.tagging_eval [--systems dag flat supervised] [--runs 3] [--version N] [--workers 16] [--limit M]

Systems:
  dag         the production tagger: Haiku 5.5 with the catalogue block (questions, value definitions,
              is-a parents with weights) as a cached system block; effort medium.
  flat        zero-shot LLM baseline: the same model and output format, but the label space is a flat
              list of term type ids with their value labels; no questions, no definitions, no hierarchy.
  supervised  TF-IDF (word 1-2 grams) + one-vs-rest logistic regression trained on the production tags
              of every tagged item outside the gold set; the decision threshold is tuned on a held-out
              10% of the training items (not on gold). Runs differ by seed (split and solver).

LLM runs differ by sampling (temperature 1). Every run's predictions are saved to
output/evaluation/pred_{system}_run{r}.jsonl so the retrieval evaluation can reuse them.
Writes tagging_eval.{json,md} and paper/tables/eval_tagging.tex.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from taxonomy.classification import catalogue as cat
from taxonomy.classification.prompts import TAG_PROMPT, TAGGER_INSTRUCTIONS
from taxonomy.classification.sample import sample_path
from taxonomy.classification.tag import CATEGORIES, catalogue_block, extract_json, validate
from taxonomy.evaluation.common import (GOLD, GOLD_ITEMS, OUT, PAPER_TABLES, add_usage, call_llm, cost, label_set, mean_sd,
                                        micro_macro, pm, pm_tex, read_jsonl, type_set, write_jsonl)
from taxonomy.llm_context import client

FLAT_INSTRUCTIONS = """\
You are a classifier for texts about distributed-ledger technology (DLT) and crypto-assets. \
You assign labels from a fixed flat list. Each label is a term type id with a value code. \
Tag every label the text clearly supports; a passing mention is not enough. Each tag carries a \
confidence in [0, 1] and an evidence span of at most 20 words copied verbatim from the text. \
Use only ids and codes from the list. Output valid JSON only, no prose, no markdown fences.
"""


def flat_block(tts: list[dict]) -> str:
    lines = ["<labels>"]
    for t in tts:
        lines.append(f'{t["id"]}: ' + "; ".join(f"v{i + 1} {v['value']}" for i, v in enumerate(t["values"])))
    lines.append("</labels>")
    return "\n".join(lines)


def llm_system(name: str, items: list[dict], tts: list[dict], dag: dict, model: str, effort: str, workers: int) -> tuple[list[dict], dict]:
    by_id = {t["id"]: t for t in tts}
    parent_of: dict[str, list[str]] = {}
    for e in dag["edges"]:
        parent_of.setdefault(e["child"], []).append(e["parent"])
    block = catalogue_block(tts, dag) if name == "dag" else flat_block(tts)
    instr = TAGGER_INSTRUCTIONS if name == "dag" else FLAT_INSTRUCTIONS
    cl = client()
    usage: dict = {}
    t0 = time.perf_counter()

    def one(item: dict) -> dict:
        prompt = TAG_PROMPT.format(item_id=item["id"], source=item["source"], year=f", {item['year']}" if item.get("year") else "",
                                   title=item["title"], text=item["text"])
        parsed, r = {"tags": [], "parse_error": True}, None
        for attempt in range(3):
            try:
                r = call_llm(cl, instr, prompt, model, effort, [block], max_tokens=3000)
                parsed = extract_json(r["text"])
                break
            except (json.JSONDecodeError, ValueError):
                break
            except Exception:
                if attempt == 2:
                    raise
                time.sleep(2 * (attempt + 1))
        out = validate(item, parsed, by_id, parent_of)
        out["usage"], out["seconds"] = (r["usage"], r["seconds"]) if r else ({}, 0.0)
        return out

    first = one(items[0])                  # warm the cached block once before fanning out
    with ThreadPoolExecutor(workers) as ex:
        rows = [first] + list(ex.map(one, items[1:]))
    for r in rows:
        add_usage(usage, r.pop("usage"))
    secs = [r.pop("seconds") for r in rows]
    return rows, {"cost_usd": round(cost(usage, model), 4), "api_seconds": round(sum(secs), 1),
                  "wall_seconds": round(time.perf_counter() - t0, 1), "usage": usage, "model": model, "effort": effort}


def supervised_system(items: list[dict], tts: list[dict], seed: int, min_support: int = 5) -> tuple[list[dict], dict]:
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.multiclass import OneVsRestClassifier
    from sklearn.preprocessing import MultiLabelBinarizer

    t0 = time.perf_counter()
    gold_ids = {it["id"] for it in items}
    by_id = {t["id"]: t for t in tts}
    texts, labels = [], []
    for k in cat.iterations():
        tf = cat.iter_dir(k) / "tags.jsonl"
        sp = sample_path(k)
        if not tf.exists() or not sp.exists():
            continue
        text_of = {r["id"]: r["title"] + " " + r.get("text", "") for r in read_jsonl(sp)}
        for r in read_jsonl(tf):
            if r["item_id"] in gold_ids or r.get("off_topic") or r["item_id"] not in text_of:
                continue
            labs = [(t["term_type"], t["value"]) for t in r["tags"] if t["term_type"] in by_id]
            if labs:
                texts.append(text_of[r["item_id"]])
                labels.append(labs)
    from collections import Counter
    support = Counter(l for ls in labels for l in ls)
    keep = {l for l, n in support.items() if n >= min_support}
    labels = [[l for l in ls if l in keep] for ls in labels]
    rng = random.Random(seed)
    idx = list(range(len(texts)))
    rng.shuffle(idx)
    n_val = max(1, len(idx) // 10)
    val_idx, tr_idx = idx[:n_val], idx[n_val:]
    mlb = MultiLabelBinarizer(classes=sorted(keep))
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200000, sublinear_tf=True)
    X_tr = vec.fit_transform([texts[i] for i in tr_idx])
    Y_tr = mlb.fit_transform([labels[i] for i in tr_idx])
    clf = OneVsRestClassifier(LogisticRegression(C=4.0, max_iter=300, solver="liblinear", random_state=seed), n_jobs=-1)
    clf.fit(X_tr, Y_tr)
    P_val = clf.predict_proba(vec.transform([texts[i] for i in val_idx]))
    Y_val = mlb.transform([labels[i] for i in val_idx])
    best_t, best_f = 0.5, -1.0
    for t in [0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]:
        pred = P_val >= t
        tp = int((pred & (Y_val == 1)).sum()); fp = int((pred & (Y_val == 0)).sum()); fn = int((~pred & (Y_val == 1)).sum())
        f = 2 * tp / (2 * tp + fp + fn) if tp else 0.0
        if f > best_f:
            best_t, best_f = t, f
    P = clf.predict_proba(vec.transform([it["title"] + " " + it.get("text", "") for it in items]))
    rows = []
    for it, probs in zip(items, P):
        tags = [{"term_type": l[0], "category": by_id[l[0]]["applies_to"], "value": l[1], "confidence": round(float(p), 4), "evidence": ""}
                for l, p in zip(mlb.classes_, probs) if p >= best_t]
        rows.append({"item_id": it["id"], "source": it["source"], "title": it["title"], "off_topic": False,
                     "tags": sorted(tags, key=lambda t: -t["confidence"])})
    return rows, {"train_items": len(tr_idx), "val_items": len(val_idx), "labels": len(keep), "threshold": best_t,
                  "val_micro_f1": round(best_f, 4), "features": X_tr.shape[1], "wall_seconds": round(time.perf_counter() - t0, 1), "cost_usd": 0.0}


def evaluate(gold: dict[str, dict], rows: list[dict]) -> dict:
    g_lab = {i: label_set(g["tags"]) for i, g in gold.items()}
    p_lab = {r["item_id"]: label_set(r["tags"]) for r in rows}
    g_typ = {i: type_set(g["tags"]) for i, g in gold.items()}
    p_typ = {r["item_id"]: type_set(r["tags"]) for r in rows}
    out = {"label": micro_macro(g_lab, p_lab), "type": micro_macro(g_typ, p_typ)}
    for c in CATEGORIES:
        gc = {i: {l for l in s if any(t["term_type"] == l[0] and t["category"] == c for t in gold[i]["tags"])} for i, s in g_lab.items()}
        cats = {t["term_type"]: t["category"] for g in gold.values() for t in g["tags"]}
        cats.update({t["term_type"]: t["category"] for r in rows for t in r["tags"]})
        gc = {i: {l for l in s if cats.get(l[0]) == c} for i, s in g_lab.items()}
        pc = {i: {l for l in s if cats.get(l[0]) == c} for i, s in p_lab.items()}
        if any(gc.values()):
            out[f"label_{c}"] = micro_macro(gc, pc)
    return out


def render(res: dict) -> tuple[str, str]:
    systems = res["systems"]
    names = {"dag": "DAG-guided LLM (ours)", "flat": "zero-shot LLM, flat labels", "supervised": "supervised TF-IDF + LR"}
    md = ["# Tagging evaluation", "",
          f"Gold: {res['gold']['items']} items, {res['gold']['labels']} labels ({res['gold']['labels_per_item']} per item), "
          f"{res['gold']['distinct_labels']} distinct (term type, value) labels over {res['gold']['distinct_term_types']} term types; "
          f"catalogue v{res['catalogue_version']}; {res['runs']} runs per system (mean ± sd).", "",
          "| system | label micro-F1 | label macro-F1 | label P | label R | type micro-F1 | type macro-F1 | tags/item | cost/run | wall/run |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    tex = ["% generated by taxonomy.evaluation.tagging_eval", "\\begin{tabular}{lcccccc}", "\\toprule",
           "System & Micro-F1 & Macro-F1 & P & R & Type Micro-F1 & Type Macro-F1 \\\\", "\\midrule"]
    for s, runs in systems.items():
        m = [r["metrics"] for r in runs]
        md.append(f"| {names.get(s, s)} | {pm([x['label']['micro_f1'] for x in m])} | {pm([x['label']['macro_f1'] for x in m])} | "
                  f"{pm([x['label']['micro_p'] for x in m])} | {pm([x['label']['micro_r'] for x in m])} | "
                  f"{pm([x['type']['micro_f1'] for x in m])} | {pm([x['type']['macro_f1'] for x in m])} | "
                  f"{pm([x['label']['pred_per_item'] for x in m], 2)} | ${mean_sd([r['run_info'].get('cost_usd', 0) for r in runs])[0]:.2f} | "
                  f"{mean_sd([r['run_info'].get('wall_seconds', 0) for r in runs])[0]:.0f} s |")
        tex.append(f"{names.get(s, s)} & {pm_tex([x['label']['micro_f1'] for x in m])} & {pm_tex([x['label']['macro_f1'] for x in m])} & "
                   f"{pm_tex([x['label']['micro_p'] for x in m])} & {pm_tex([x['label']['micro_r'] for x in m])} & "
                   f"{pm_tex([x['type']['micro_f1'] for x in m])} & {pm_tex([x['type']['macro_f1'] for x in m])} \\\\")
    tex += ["\\bottomrule", "\\end{tabular}"]
    md += ["", "## Per category (label micro-F1, mean ± sd)", "", "| system | " + " | ".join(CATEGORIES) + " |", "|---|" + "---|" * len(CATEGORIES)]
    for s, runs in systems.items():
        m = [r["metrics"] for r in runs]
        md.append(f"| {names.get(s, s)} | " + " | ".join(pm([x.get(f'label_{c}', {}).get('micro_f1') for x in m]) if any(f"label_{c}" in x for x in m) else "-" for c in CATEGORIES) + " |")
    md += ["", "Gold labels are adjudicated from two independent passes of " + res["gold"].get("model", "a stronger model") +
           f" (pass agreement micro-F1 {res['gold'].get('pass_agreement')}); no human labels."]
    return "\n".join(md) + "\n", "\n".join(tex) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--systems", nargs="*", default=["dag", "flat", "supervised"])
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--version", type=int, default=None)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    if not GOLD.exists():
        sys.exit("gold.jsonl missing: run taxonomy.evaluation.gold select / annotate first")
    gsum = json.loads((OUT / "gold_summary.json").read_text(encoding="utf-8"))
    version = a.version if a.version is not None else gsum["catalogue_version"]
    tts, dag, _ = cat.load_version(version)
    items = read_jsonl(GOLD_ITEMS)
    gold = {g["item_id"]: g for g in read_jsonl(GOLD)}
    if a.limit:
        items = items[:a.limit]
    gold = {i: gold[i] for i in gold if i in {it["id"] for it in items}}
    res = {"catalogue_version": version, "runs": a.runs, "gold": {**gsum["gold"], "model": gsum["model"],
           "pass_agreement": gsum.get("pass_agreement", {}).get("micro_f1")}, "systems": {}}
    for s in a.systems:
        res["systems"][s] = []
        for r in range(1, a.runs + 1):
            if s == "supervised":
                rows, info = supervised_system(items, tts, seed=100 + r)
            else:
                rows, info = llm_system(s, items, tts, dag, a.model, a.effort, a.workers)
            write_jsonl(OUT / f"pred_{s}_run{r}.jsonl", rows)
            m = evaluate(gold, rows)
            res["systems"][s].append({"run": r, "metrics": m, "run_info": info})
            print(f"{s} run {r}: label micro-F1 {m['label']['micro_f1']}  macro-F1 {m['label']['macro_f1']}  type micro-F1 {m['type']['micro_f1']}  "
                  f"({info.get('cost_usd', 0)} USD, {info.get('wall_seconds')} s)")
    (OUT / "tagging_eval.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    md, tex = render(res)
    (OUT / "tagging_eval.md").write_text(md, encoding="utf-8")
    PAPER_TABLES.mkdir(parents=True, exist_ok=True)
    (PAPER_TABLES / "eval_tagging.tex").write_text(tex, encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()
