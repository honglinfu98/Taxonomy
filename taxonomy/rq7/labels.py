"""Build the RQ7 dataset: items with a usable description and the retained site categories.

    python -m taxonomy.rq7.labels [--min-words 40] [--max-words 400] [--min-count 10]

CoinGecko attaches many categories that are not classification dimensions of the asset
(ecosystem membership, index constituents, investor portfolios, launchpads, exchange listings).
Those are excluded by name pattern (EXCLUDE); of the rest, categories carried by at least
--min-count items are kept as the label space. Items with no retained category are kept with an
empty gold set (a correct classifier predicts nothing for them). Writes output/rq7/items.jsonl
(tagger item shape: id, source, title, text, year, gold) and output/rq7/labels.json.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter

from taxonomy.evaluation.common import read_jsonl, write_jsonl
from taxonomy.rq7.collect import COINS, OUT

ITEMS = OUT / "items.jsonl"
LABELS = OUT / "labels.json"
EXCLUDE = re.compile(r"ecosystem|index|portfolio|launchpad|launchpool|holdings|alleged|capital|ventures|labs\b|fund\b|alpha\b|"
                     r"selection|trending|made in|treasury|listing|\bhub\b|^top |spot etf|airdrop|hodler|megadrop|points|season|"
                     r"^bridged |^wrapped |native\b|spotlight|club\b", re.I)


def clean_text(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)                    # html
    s = re.sub(r"\s+", " ", s).strip()
    return s


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--min-words", type=int, default=40)
    ap.add_argument("--max-words", type=int, default=400)
    ap.add_argument("--min-count", type=int, default=10)
    a = ap.parse_args()
    coins = read_jsonl(COINS)
    usable = []
    for c in coins:
        text = clean_text(c["description"])
        words = text.split()
        if len(words) < a.min_words:
            continue
        usable.append({**c, "text": " ".join(words[: a.max_words])})
    raw = Counter(cat for c in usable for cat in c["categories"])
    excluded = {cat: n for cat, n in raw.items() if EXCLUDE.search(cat)}
    counts = {cat: n for cat, n in raw.items() if cat not in excluded}
    kept = {cat: n for cat, n in counts.items() if n >= a.min_count}
    rare = {cat: n for cat, n in counts.items() if n < a.min_count}
    items = []
    for c in usable:
        gold = sorted(cat for cat in c["categories"] if cat in kept)
        items.append({"id": c["id"], "source": "coingecko", "title": c["name"], "year": (c.get("genesis_date") or "")[:4] or None,
                      "market_cap_rank": c["market_cap_rank"], "text": c["text"], "gold": gold, "all_categories": c["categories"]})
    write_jsonl(ITEMS, items)
    LABELS.write_text(json.dumps({"coins_collected": len(coins), "items": len(items), "items_with_gold": sum(1 for i in items if i["gold"]),
                                  "min_words": a.min_words, "max_words": a.max_words, "min_count": a.min_count,
                                  "labels": dict(sorted(kept.items(), key=lambda x: -x[1])),
                                  "excluded_by_pattern": dict(sorted(excluded.items(), key=lambda x: -x[1])),
                                  "rare": dict(sorted(rare.items(), key=lambda x: -x[1]))}, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{len(coins)} coins, {len(items)} with >= {a.min_words} words, {sum(1 for i in items if i['gold'])} with a retained category; "
          f"{len(kept)} labels kept, {len(excluded)} category names excluded by pattern, {len(rare)} rare")
    for cat, n in sorted(kept.items(), key=lambda x: -x[1]):
        print(f"  {n:4d}  {cat}")
    print("mean gold labels per item:", round(sum(len(i["gold"]) for i in items) / max(len(items), 1), 2))


if __name__ == "__main__":
    main()
