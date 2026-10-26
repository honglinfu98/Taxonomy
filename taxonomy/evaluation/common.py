"""Shared helpers: paths, prices, LLM call, label sets, F1 and mean ± sd."""
from __future__ import annotations

import json
import math
import statistics
import time
from pathlib import Path

from taxonomy.llm_context import ROOT, build_request

OUT = ROOT / "output" / "evaluation"
PAPER_TABLES = ROOT / "paper" / "tables"
GOLD_ITEMS = OUT / "gold_items.jsonl"
GOLD = OUT / "gold.jsonl"

PRICES = {  # USD per token (prompts <= 100K tokens)
    "claude-haiku-5-5": {"input": 0.10e-6, "output": 0.50e-6, "cache_read": 0.01e-6, "cache_write": 0.125e-6},
    "claude-sonnet-5-5": {"input": 2e-6, "output": 10e-6, "cache_read": 0.2e-6, "cache_write": 4e-6},
    "claude-opus-5-5": {"input": 4e-6, "output": 20e-6, "cache_read": 0.4e-6, "cache_write": 8e-6},
}
NO_DISABLE = ("claude-opus-5-5", "claude-sonnet-5-5")   # thinking cannot be disabled on these; adaptive is used


def cost(usage: dict, model: str) -> float:
    p = PRICES.get(model, PRICES["claude-haiku-5-5"])
    return sum(usage.get(k, 0) * p[k] for k in p)


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").split("\n") if l.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def call_llm(cl, instructions: str, prompt: str, model: str, effort: str, extra_system: list[str] | None,
             max_tokens: int = 4000) -> dict:
    extra = {} if model in NO_DISABLE else {"thinking": {"type": "disabled"}}
    req = build_request(instructions, prompt, model=model, max_tokens=max_tokens, effort=effort,
                        extra_system=extra_system, corpus=False, **extra)
    t0 = time.perf_counter()
    msg = cl.messages.create(**req)
    u = msg.usage
    return {"text": "".join(b.text for b in msg.content if b.type == "text"), "stop_reason": msg.stop_reason,
            "seconds": round(time.perf_counter() - t0, 3),
            "usage": {"input": u.input_tokens, "output": u.output_tokens,
                      "cache_write": u.cache_creation_input_tokens or 0, "cache_read": u.cache_read_input_tokens or 0}}


def add_usage(total: dict, u: dict) -> None:
    for k, v in u.items():
        total[k] = total.get(k, 0) + v


# ---- labels and metrics ------------------------------------------------------------------
def label_set(tags: list[dict]) -> set[tuple[str, str]]:
    return {(t["term_type"], t["value"]) for t in tags}


def type_set(tags: list[dict]) -> set[str]:
    return {t["term_type"] for t in tags}


def prf(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f


def micro_macro(gold: dict[str, set], pred: dict[str, set]) -> dict:
    """gold/pred: item id -> set of labels. Macro-F1 over the labels that occur in the gold set."""
    tp = fp = fn = 0
    per_label: dict = {}
    labels = {l for s in gold.values() for l in s}
    for i, g in gold.items():
        p = pred.get(i, set())
        tp += len(g & p)
        fp += len(p - g)
        fn += len(g - p)
        for l in g | p:
            if l not in labels:
                continue
            c = per_label.setdefault(l, [0, 0, 0])
            if l in g and l in p:
                c[0] += 1
            elif l in p:
                c[1] += 1
            else:
                c[2] += 1
    mp, mr, mf = prf(tp, fp, fn)
    macro = statistics.mean(prf(*per_label[l])[2] for l in labels) if labels else 0.0
    return {"micro_p": round(mp, 4), "micro_r": round(mr, 4), "micro_f1": round(mf, 4), "macro_f1": round(macro, 4),
            "n_labels": len(labels), "tp": tp, "fp": fp, "fn": fn,
            "pred_per_item": round(sum(len(pred.get(i, set())) for i in gold) / max(len(gold), 1), 2)}


def mean_sd(xs: list[float]) -> tuple[float, float]:
    xs = [x for x in xs if x is not None]
    if not xs:
        return float("nan"), float("nan")
    return statistics.mean(xs), (statistics.stdev(xs) if len(xs) > 1 else 0.0)


def pm(xs: list[float], digits: int = 3) -> str:
    m, s = mean_sd(xs)
    return f"{m:.{digits}f} ± {s:.{digits}f}"


def pm_tex(xs: list[float], digits: int = 3) -> str:
    m, s = mean_sd(xs)
    return f"{m:.{digits}f} $\\pm$ {s:.{digits}f}"


def ndcg_at_k(ranked_grades: list[int], all_grades: list[int], k: int) -> float:
    dcg = sum((2 ** g - 1) / math.log2(i + 2) for i, g in enumerate(ranked_grades[:k]))
    ideal = sorted(all_grades, reverse=True)[:k]
    idcg = sum((2 ** g - 1) / math.log2(i + 2) for i, g in enumerate(ideal))
    return dcg / idcg if idcg else 0.0
