"""Collect token descriptions and site-assigned categories from CoinGecko's public API.

    python -m taxonomy.rq7.collect [--pages 3] [--per-page 250] [--sleep 3]

Top coins by market cap (pages of /coins/markets), then /coins/{id} for the English description,
the categories, and the homepage. Appends to output/rq7/coins.jsonl and skips ids already
there, so it can be resumed. Backs off on HTTP 429. No API key is needed for these endpoints.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timezone

from taxonomy.llm_context import ROOT

OUT = ROOT / "output" / "rq7"
COINS = OUT / "coins.jsonl"
API = "https://api.coingecko.com/api/v3"


def get(path: str, params: dict, sleep: float) -> dict | list:
    """GET via curl (the venv's Python has no CA bundle); backs off on 429 and transient errors."""
    url = f"{API}{path}?{urllib.parse.urlencode(params)}"
    for attempt in range(8):
        r = subprocess.run(["curl", "-s", "-m", "30", "-w", "\n%{http_code}", "-A", "taxonomy-rq7/1.0", url], capture_output=True, text=True)
        body, _, code = r.stdout.rpartition("\n")
        if code == "200":
            try:
                data = json.loads(body)
                time.sleep(sleep)
                return data
            except json.JSONDecodeError:
                pass
        wait = 65 if code == "429" else 10 * (attempt + 1)
        print(f"HTTP {code or 'none'} on {path}; waiting {wait}s", file=sys.stderr, flush=True)
        time.sleep(wait)
    raise SystemExit(f"gave up on {path}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pages", type=int, default=3)
    ap.add_argument("--per-page", type=int, default=250)
    ap.add_argument("--sleep", type=float, default=3.0)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    done = set()
    if COINS.exists():
        done = {json.loads(l)["id"] for l in COINS.read_text(encoding="utf-8").split("\n") if l.strip()}
    markets = []
    for page in range(1, a.pages + 1):
        markets += get("/coins/markets", {"vs_currency": "usd", "order": "market_cap_desc", "per_page": a.per_page, "page": page}, a.sleep)
    print(f"{len(markets)} coins listed, {len(done)} already collected", flush=True)
    with COINS.open("a", encoding="utf-8") as f:
        for i, m in enumerate(markets, 1):
            if m["id"] in done:
                continue
            c = get(f"/coins/{m['id']}", {"localization": "false", "tickers": "false", "market_data": "false",
                                           "community_data": "false", "developer_data": "false", "sparkline": "false"}, a.sleep)
            row = {"id": c["id"], "symbol": c.get("symbol"), "name": c.get("name"), "market_cap_rank": m.get("market_cap_rank"),
                   "categories": c.get("categories") or [], "description": (c.get("description") or {}).get("en", "") or "",
                   "homepage": next((u for u in (c.get("links") or {}).get("homepage", []) if u), None),
                   "genesis_date": c.get("genesis_date"), "hashing_algorithm": c.get("hashing_algorithm"),
                   "collected": datetime.now(timezone.utc).isoformat(timespec="seconds")}
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            f.flush()
            if i % 25 == 0:
                print(f"{i}/{len(markets)} {c['id']}: {len(row['description'].split())} words, {len(row['categories'])} categories", flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()
