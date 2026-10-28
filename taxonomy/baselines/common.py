"""Shared pieces for the RQ5 baselines: corpus passages, BM25 over passages, LLM calls with
usage accounting, and saving a baseline catalogue in the Task A schema so the same
verification, agreement and tagging code applies to every catalogue.

Catalogues live in output/baselines/<name>/term_types.json (+ verification.json, log.json).
"""
from __future__ import annotations

import difflib
import json
import math
import re
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from taxonomy.establishment.term_types import DOC_RE, parse_corpus, verify
from taxonomy.evaluation.common import NO_DISABLE, add_usage, cost
from taxonomy.llm_context import ROOT, build_request, load_corpus

OUT = ROOT / "output" / "baselines"
CATEGORIES = ["asset", "technology", "actor", "activity", "obligation_or_risk"]


# ---- corpus -------------------------------------------------------------------------------
def doc_meta() -> dict[int, dict]:
    text = load_corpus()
    out = {}
    for m in DOC_RE.finditer(text):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(2)))
        out[int(m.group(1))] = attrs
    return out


def passages(max_words: int = 900) -> list[dict]:
    """Split every section into passages of at most max_words words on sentence boundaries.
    A passage keeps its doc index and section label, so a citation of (doc, section, quote)
    taken from a passage verifies against the full section exactly as Task A citations do."""
    docs = parse_corpus(load_corpus())
    meta = doc_meta()
    out = []
    for d, secs in docs.items():
        for label, txt in secs.items():
            sents = re.split(r"(?<=[.;:])\s+(?=[A-Z(\[\"'“])", txt)
            buf: list[str] = []
            n = 0
            k = 0

            def flush():
                nonlocal buf, n, k
                if buf:
                    out.append({"id": f"d{d}s{len([p for p in out if p['doc'] == d])}", "doc": d, "section": label,
                                "title": meta[d].get("title", ""), "part": k, "text": " ".join(buf)})
                    buf, n, k = [], 0, k + 1

            units = []
            for s in sents:                      # a run without sentence boundaries (tables) is cut by words
                ws = s.split()
                units += [" ".join(ws[i:i + max_words]) for i in range(0, len(ws), max_words)] or [s]
            for s in units:
                w = len(s.split())
                if n + w > max_words and buf:
                    flush()
                buf.append(s)
                n += w
            flush()
    return out


class BM25:
    def __init__(self, texts: list[str], k1: float = 1.2, b: float = 0.75):
        self.docs = [self.tok(t) for t in texts]
        self.k1, self.b = k1, b
        self.avgdl = sum(len(d) for d in self.docs) / max(len(self.docs), 1)
        self.df: Counter = Counter()
        self.tf = []
        for d in self.docs:
            c = Counter(d)
            self.tf.append(c)
            self.df.update(c.keys())
        self.N = len(self.docs)

    @staticmethod
    def tok(s: str) -> list[str]:
        return re.findall(r"[a-z0-9]+", s.lower())

    def search(self, text: str, k: int) -> list[int]:
        q = self.tok(text)
        scores = []
        for i, c in enumerate(self.tf):
            dl = len(self.docs[i])
            s = 0.0
            for w in q:
                if w in c:
                    idf = math.log(1 + (self.N - self.df[w] + 0.5) / (self.df[w] + 0.5))
                    s += idf * c[w] * (self.k1 + 1) / (c[w] + self.k1 * (1 - self.b + self.b * dl / self.avgdl))
            scores.append((-s, i))
        return [i for s, i in sorted(scores)[:k] if s < 0]


# ---- LLM ----------------------------------------------------------------------------------
class Meter:
    """Accumulates usage, cost, API seconds and call count for one baseline run."""

    def __init__(self, model: str):
        self.model, self.usage, self.calls, self.api_seconds = model, {}, 0, 0.0
        self.t0 = time.perf_counter()

    def add(self, r: dict) -> None:
        add_usage(self.usage, r["usage"])
        self.calls += 1
        self.api_seconds += r["seconds"]

    def report(self) -> dict:
        return {"model": self.model, "calls": self.calls, "usage": self.usage, "cost_usd": round(cost(self.usage, self.model), 4),
                "api_seconds": round(self.api_seconds, 1), "wall_seconds": round(time.perf_counter() - self.t0, 1)}


def llm(cl, instructions: str, prompt: str, model: str, effort: str = "high", max_tokens: int = 16000,
        extra_system: list[str] | None = None, corpus: bool = False, meter: Meter | None = None) -> dict:
    """One call; long outputs stream so there is no request timeout. Thinking is disabled where possible."""
    extra = {} if model in NO_DISABLE else {"thinking": {"type": "disabled"}}
    req = build_request(instructions, prompt, model=model, max_tokens=max_tokens, effort=effort,
                        extra_system=extra_system, corpus=corpus, **extra)
    t0 = time.perf_counter()
    with cl.messages.stream(**req) as stream:
        msg = stream.get_final_message()
    u = msg.usage
    r = {"text": "".join(b.text for b in msg.content if b.type == "text"), "stop_reason": msg.stop_reason,
         "seconds": round(time.perf_counter() - t0, 3),
         "usage": {"input": u.input_tokens, "output": u.output_tokens,
                   "cache_write": u.cache_creation_input_tokens or 0, "cache_read": u.cache_read_input_tokens or 0}}
    if meter is not None:
        meter.add(r)
    return r


def extract_json(text: str) -> dict | list:
    text = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", text.strip())
    s = min(i for i in (text.find("{"), text.find("[")) if i >= 0) if ("{" in text or "[" in text) else -1
    if s < 0:
        raise ValueError("no JSON in model output")
    e = max(text.rfind("}"), text.rfind("]"))
    try:
        return json.loads(text[s:e + 1])
    except json.JSONDecodeError:
        return salvage_term_types(text)


def salvage_term_types(text: str) -> dict:
    """Malformed or truncated Task A style output: decode every complete object that starts at a
    `{"id":` and has a "values" list, skipping anything nested inside an object already taken."""
    dec, items, pos = json.JSONDecoder(), [], 0
    for m in re.finditer(r'\{\s*"id"\s*:', text):
        if m.start() < pos:
            continue
        try:
            obj, end = dec.raw_decode(text, m.start())
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and isinstance(obj.get("values"), list):
            items.append(obj)
            pos = end
    if not items:
        raise ValueError("unparseable JSON")
    return {"term_types": items, "truncated": True}


# ---- catalogue hygiene ---------------------------------------------------------------------
def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(s or "").lower()).strip()


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(s or "").lower()).strip("_")[:60] or "term_type"


def clean_term_types(raw: list[dict]) -> list[dict]:
    """Coerce model output into the Task A schema: unique snake_case ids, a known category,
    string fields present, values with labels and definitions, citation lists present."""
    out, seen = [], set()
    for t in raw or []:
        if not isinstance(t, dict) or not t.get("values"):
            continue
        tid = slug(t.get("id") or t.get("name"))
        base, k = tid, 2
        while tid in seen:
            tid, k = f"{base}_{k}", k + 1
        seen.add(tid)
        cat = str(t.get("applies_to", "")).strip().lower().replace(" ", "_")
        if cat not in CATEGORIES:
            cat = next((c for c in CATEGORIES if c in cat), "technology")
        vals, vseen = [], set()
        for v in t["values"]:
            if isinstance(v, str):
                v = {"value": v, "definition": ""}
            if not isinstance(v, dict) or not v.get("value"):
                continue
            if norm(v["value"]) in vseen:
                continue
            vseen.add(norm(v["value"]))
            vals.append({"value": str(v["value"]).strip(), "definition": str(v.get("definition", "") or "")[:300],
                         "citations": [c for c in (v.get("citations") or []) if isinstance(c, dict)]})
        if not vals:
            continue
        out.append({"id": tid, "name": str(t.get("name") or tid.replace("_", " ")).strip(), "applies_to": cat,
                    "question": str(t.get("question", "") or "").strip(), "description": str(t.get("description", "") or "").strip(),
                    "aliases": [str(a) for a in (t.get("aliases") or []) if a], "values": vals,
                    "citations": [c for c in (t.get("citations") or []) if isinstance(c, dict)],
                    "sources": t.get("sources", {}) if isinstance(t.get("sources"), dict) else {},
                    "notes": str(t.get("notes", "") or "")})
    return out


def merge_values(groups: list[list[dict]]) -> list[dict]:
    """Union of value lists, deduplicated by label (normalised equality or ratio >= 0.85)."""
    out: list[dict] = []
    for vals in groups:
        for v in vals:
            n = norm(v["value"])
            hit = next((o for o in out if norm(o["value"]) == n or difflib.SequenceMatcher(None, norm(o["value"]), n).ratio() >= 0.85), None)
            if hit is None:
                out.append({"value": v["value"], "definition": v.get("definition", ""), "citations": list(v.get("citations", []))})
            else:
                seen = {(c.get("doc"), c.get("section"), c.get("quote")) for c in hit["citations"]}
                hit["citations"] += [c for c in v.get("citations", []) if (c.get("doc"), c.get("section"), c.get("quote")) not in seen]
                if not hit["definition"] and v.get("definition"):
                    hit["definition"] = v["definition"]
    return out


def dedupe_citations(cites: list[dict]) -> list[dict]:
    seen, out = set(), []
    for c in cites:
        key = (c.get("doc"), c.get("section"), norm(c.get("quote", "")))
        if key not in seen:
            seen.add(key)
            out.append({k: c[k] for k in ("doc", "section", "quote") if k in c})
    return out


# ---- save / load ---------------------------------------------------------------------------
def save_catalogue(name: str, term_types: list[dict], run: dict, extras: dict | None = None) -> dict:
    """Write the catalogue in the Task A schema and verify every citation against the corpus."""
    d = OUT / name
    d.mkdir(parents=True, exist_ok=True)
    result = {"term_types": term_types, **(extras or {})}
    report = verify(result, parse_corpus(load_corpus()))
    run = {**run, "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"), "baseline": name}
    (d / "term_types.json").write_text(json.dumps({"run": run, **result}, indent=2, ensure_ascii=False), encoding="utf-8")
    (d / "term_types.verification.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{name}: {len(term_types)} term types, {sum(len(t['values']) for t in term_types)} values; "
          f"citations {report['verified']}/{report['citations']} verified; cost ${run.get('cost_usd', 0)}; "
          f"{run.get('wall_seconds', 0)} s -> {d / 'term_types.json'}")
    return report


def load_catalogue(name: str) -> dict:
    p = (OUT / name / "term_types.json") if name not in ("ours", "seed") else ROOT / "output" / "establishment" / "term_types.json"
    return json.loads(p.read_text(encoding="utf-8"))


def catalogue_path(name: str) -> Path:
    return (OUT / name / "term_types.json") if name not in ("ours", "seed") else ROOT / "output" / "establishment" / "term_types.json"


def compact(tts: list[dict], prefix: str = "") -> str:
    """One line per term type for prompts that compare or merge catalogues."""
    return "\n".join(f'{prefix}{t["id"]} [{t["applies_to"]}] {t["name"]} — {t.get("question", "")} — values: '
                     + "; ".join(v["value"] for v in t["values"][:12]) + ("; ..." if len(t["values"]) > 12 else "") for t in tts)
