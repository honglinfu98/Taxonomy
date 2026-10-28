"""RQ7 supervised comparison: logistic regression on TF-IDF words, on ontology tags, and on both.

    python -m taxonomy.rq7.supervised [--folds 5] [--seeds 3] [--tags tags_run1.jsonl]

Ontology-tag features are binary indicators of (term type, value), of the term type alone, and
of the ancestors implied by the is-a DAG, from the production tagger's output for the same items.
Cross-validated (k folds, repeated with several shuffles); micro and macro F1 over the folds'
pooled predictions, mean ± sd over seeds. Writes output/rq7/supervised.json.
"""
from __future__ import annotations

import argparse
import json

import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer

from taxonomy.evaluation.common import mean_sd, micro_macro, read_jsonl
from taxonomy.rq7.labels import ITEMS, LABELS, OUT


def tag_features(row: dict) -> list[str]:
    f = []
    for t in row["tags"]:
        f += [f'{t["term_type"]}={t["value"]}', f'type:{t["term_type"]}']
    f += [f"type:{a}" for a in row.get("implied_term_types", [])]
    return f


def fit_predict(X, Y, folds: int, seed: int):
    pred = np.zeros_like(Y)
    for tr, te in KFold(folds, shuffle=True, random_state=seed).split(X):
        cols = [j for j in range(Y.shape[1]) if 0 < Y[tr, j].sum() < len(tr)]
        clf = OneVsRestClassifier(LogisticRegression(C=4.0, max_iter=500, solver="liblinear", class_weight="balanced"), n_jobs=-1)
        clf.fit(X[tr], Y[tr][:, cols])
        pred[np.ix_(te, cols)] = clf.predict(X[te])
    return pred


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--tags", default="tags_run1.jsonl")
    a = ap.parse_args()
    items = read_jsonl(ITEMS)
    labels = list(json.loads(LABELS.read_text(encoding="utf-8"))["labels"])
    tags = {r["item_id"]: r for r in read_jsonl(OUT / a.tags)}
    mlb = MultiLabelBinarizer(classes=labels)
    Y = mlb.fit_transform([i["gold"] for i in items])
    X_text = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True).fit_transform([i["title"] + " " + i["text"] for i in items])
    tag_mlb = MultiLabelBinarizer()
    X_tags = csr_matrix(tag_mlb.fit_transform([tag_features(tags[i["id"]]) for i in items]).astype(float))
    feats = {"tfidf": X_text, "ontology_tags": X_tags, "tfidf+ontology_tags": hstack([X_text, X_tags]).tocsr()}
    res = {"items": len(items), "labels": len(labels), "folds": a.folds, "seeds": a.seeds, "tag_features": len(tag_mlb.classes_),
           "tfidf_features": X_text.shape[1], "systems": {}}
    for name, X in feats.items():
        runs = []
        for seed in range(a.seeds):
            P = fit_predict(X, Y, a.folds, seed)
            g = {i["id"]: set(i["gold"]) for i in items}
            p = {i["id"]: {labels[j] for j in np.nonzero(P[k])[0]} for k, i in enumerate(items)}
            m = micro_macro(g, p)
            m["pred_per_item"] = round(float(P.sum(1).mean()), 3)
            runs.append(m)
        res["systems"][name] = {"runs": runs, "micro_f1": mean_sd([r["micro_f1"] for r in runs]), "macro_f1": mean_sd([r["macro_f1"] for r in runs])}
        print(f"{name}: micro-F1 {res['systems'][name]['micro_f1']} macro-F1 {res['systems'][name]['macro_f1']} ({X.shape[1]} features)", flush=True)
    (OUT / "supervised.json").write_text(json.dumps(res, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
