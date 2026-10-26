"""Draw the pilot sample of DLT-Corpus items to classify.

    python -m taxonomy.classification.sample --iter K [--fraction 0.1 | --per-source N] [--seed 7]

Writes data/dlt_corpus/sample_iter{K}.jsonl. --fraction draws that share of each source
dataset's full size (papers 37,440; patents 49,023) from the on-topic pool, excluding every
item already drawn in earlier sample files, so iterations are disjoint batches.

Reads the downloaded DLT-Corpus shards in data/dlt_corpus/raw/ (Hugging Face
ExponentialScience/DLT-Scientific-Literature and DLT-Patents) and writes
data/dlt_corpus/sample.jsonl, one item per line:

    {"id", "source": "paper"|"patent", "title", "text", "year", "meta": {...}}

An item is the title plus the abstract (papers: the `abstract` field; patents: the
"### Abstract" section of `text`), falling back to the first --max-words words of the body.
Text is always capped at --max-words words so every item costs about the same to tag.
Only English papers are kept, and only items whose title or abstract mentions a DLT term
(--keywords regex), because both source datasets contain off-topic documents. Sampling is
uniform at random with a fixed seed within the downloaded shards; download more shards into
raw/ to widen the pool.
"""
from __future__ import annotations

import argparse
import json
import random
import re
from pathlib import Path

import pyarrow.parquet as pq

from taxonomy.llm_context import ROOT

RAW = ROOT / "data" / "dlt_corpus" / "raw"
KEYWORDS = (r"blockchain|distributed ledger|\bDLT\b|crypto[- ]?(currenc|asset|token)|bitcoin|ethereum|smart contract|"
            r"\btokeni[sz]|stablecoin|\bDeFi\b|decentrali[sz]ed (finance|exchange|application|ledger)|"
            r"consensus (protocol|mechanism|algorithm)|proof[- ]of[- ](work|stake)|\bNFT\b|digital asset|virtual asset|\bledger\b")
SAMPLE = ROOT / "data" / "dlt_corpus" / "sample.jsonl"
DATASET_SIZE = {"paper": 37440, "patent": 49023}      # DLT-Corpus paper (Hernandez Cruz et al. 2026)


def sample_path(k: int) -> Path:
    return ROOT / "data" / "dlt_corpus" / f"sample_iter{k:02d}.jsonl"


def already_sampled() -> set[str]:
    ids = set()
    for f in (ROOT / "data" / "dlt_corpus").glob("sample*.jsonl"):
        ids |= {json.loads(l)["id"] for l in f.read_text(encoding="utf-8").split("\n") if l.strip()}
    return ids


def cap(text: str, max_words: int) -> str:
    words = re.sub(r"\s+", " ", text or "").strip().split(" ")
    return " ".join(words[:max_words])


def patent_abstract(text: str) -> str:
    m = re.search(r"###\s*Abstract\s*\n(.*?)(?:\n#{1,3}\s|\Z)", text or "", re.S)
    return m.group(1).strip() if m else ""


def load_papers() -> list[dict]:
    items = []
    for f in sorted(RAW.glob("sci-*.parquet")):
        t = pq.read_table(f, columns=["paperId", "title", "abstract", "text", "year", "venue", "lang", "fieldsOfStudy"])
        for r in t.to_pylist():
            if (r.get("lang") or "") != "en" or not r.get("title"):
                continue
            body = r.get("abstract") or ""
            items.append({"id": f"paper:{r['paperId']}", "source": "paper", "title": r["title"].strip(),
                          "body": body if len(body.split()) >= 40 else (r.get("text") or "")[:6000],
                          "year": r.get("year"), "meta": {"venue": r.get("venue") or "", "fields": r.get("fieldsOfStudy") or []}})
    return items


def load_patents() -> list[dict]:
    items = []
    for f in sorted(RAW.glob("pat-*.parquet")):
        t = pq.read_table(f, columns=["Patent Number", "Title", "text", "Date Published", "CPCI", "Assignee"])
        for r in t.to_pylist():
            if not r.get("Title"):
                continue
            body = patent_abstract(r.get("text") or "")
            year = re.search(r"(19|20)\d{2}", r.get("Date Published") or "")
            items.append({"id": f"patent:{r['Patent Number']}", "source": "patent", "title": r["Title"].strip(),
                          "body": body if len(body.split()) >= 40 else (r.get("text") or "")[:6000],
                          "year": int(year.group(0)) if year else None,
                          "meta": {"cpc": r.get("CPCI") or "", "assignee": r.get("Assignee") or ""}})
    return items


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--per-source", type=int, default=None, help="items per source (overrides --fraction)")
    ap.add_argument("--fraction", type=float, default=None, help="share of each dataset's full size, e.g. 0.1")
    ap.add_argument("--iter", type=int, default=None, help="iteration number; output sample_iter{K}.jsonl")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--max-words", type=int, default=450)
    ap.add_argument("--keywords", default=KEYWORDS, help="regex an item's title or text must match")
    args = ap.parse_args()
    rng = random.Random(args.seed + (args.iter or 0))
    kw = re.compile(args.keywords, re.I)
    out_file = sample_path(args.iter) if args.iter else SAMPLE
    taken = already_sampled() if args.iter else set()
    out = []
    for name, loader in (("paper", load_papers), ("patent", load_patents)):
        pool_all = loader()
        pool = [it for it in pool_all if kw.search(it["title"] + " " + cap(it["body"], args.max_words)) and it["id"] not in taken]
        n = args.per_source if args.per_source else (round(args.fraction * DATASET_SIZE[name]) if args.fraction else 150)
        print(f"{name}: {len(pool)}/{len(pool_all)} on-topic and unused in the downloaded shards; drawing {n}")
        pick = rng.sample(pool, min(n, len(pool)))
        for it in pick:
            text = cap(it.pop("body"), args.max_words)
            out.append({**it, "text": text, "words": len(text.split())})
        print(f"{name}: pool {len(pool)} -> sample {len(pick)}")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with out_file.open("w", encoding="utf-8") as f:
        for it in out:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    print(f"{len(out)} items, {sum(i['words'] for i in out)} words -> {out_file}")


if __name__ == "__main__":
    main()
