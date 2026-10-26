#!/usr/bin/env python3
"""Flag mechanical prose patterns in an academic text or Markdown file.

Usage: tells.py FILE [FILE...]        (or pipe text on stdin)

Reports, with line numbers: em dashes, colon splits inside sentences,
"not X, it's Y" constructions, hyphenated compound adjectives, words from
references/wordlist.txt, bullet density, paragraphs that end on a summary,
and rough passive-voice hits. It flags; a human decides. Fenced code blocks
and inline code are skipped. LaTeX, mathematics, citations, and bibliographies
are not parsed; disregard hits in those passages. Hits are review prompts,
not evidence of authorship or instructions to change technical terminology.
"""
import re
import sys
from collections import Counter
from pathlib import Path

WORDLIST = Path(__file__).resolve().parent.parent / "references" / "wordlist.txt"

# Conventional technical compounds; the list is illustrative, not exhaustive.
OK_HYPHENS = {
    "well-known", "open-source", "read-only", "write-only", "side-channel",
    "zero-knowledge", "constant-time", "non-interactive", "one-time", "two-factor",
    "multi-party", "post-quantum", "pre-image", "re-entrancy", "on-chain",
    "off-chain", "so-called", "built-in", "pull-request", "follow-up", "trade-off",
    "up-to-date", "self-contained", "run-time", "compile-time", "denial-of-service",
    "man-in-the-middle", "brute-force", "hard-coded", "user-supplied",
    "attacker-controlled", "proof-of-concept", "elliptic-curve", "public-key",
    "private-key", "look-up", "set-up", "co-author",
    "peer-reviewed", "double-blind", "single-blind", "cross-sectional",
    "case-control", "finite-dimensional", "infinite-dimensional",
    "well-defined", "well-posed", "ill-posed", "non-linear", "time-dependent",
    "mixed-effects", "fixed-effects", "random-effects", "evidence-based",
    "dose-response", "long-term", "short-term", "self-reported",
}

SUMMARY_OPENERS = re.compile(
    r"^(in short|in summary|to summarize|to sum up|overall|ultimately|all in all|"
    r"in conclusion|this ensures|this means that|this makes|this guarantees|"
    r"this way|as a result|the result is)\b", re.I)

NOT_BUT = re.compile(
    r"\b(?:is not|isn't|it's not|not|rather than|less)\b[^.\n;]{1,70}?"
    r"[,;]\s*(?:but|it's|it is|rather|instead)\b", re.I)
NOT_ONLY = re.compile(r"\bnot only\b[^.\n]{1,80}\bbut(?: also)?\b", re.I)
COLON_SPLIT = re.compile(r"[^\s:]:\s+[a-z]")          # colon followed by lowercase prose
HYPHEN = re.compile(r"\b([a-z]+-[a-z]+(?:-[a-z]+)?)\b", re.I)
PASSIVE = re.compile(r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?\w+(?:ed|en)\b", re.I)
BULLET = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
CODE_FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")


def load_wordlist():
    words = []
    if WORDLIST.exists():
        for raw in WORDLIST.read_text().splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            words.append(line.lower())
    return words


def strip_code(lines):
    """Blank out YAML frontmatter, fenced code blocks and inline code; keep line numbers stable."""
    out, in_fence = [], False
    if lines and lines[0].strip() == "---":
        end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
        if end is not None:
            lines = [""] * (end + 1) + lines[end + 1:]
    for line in lines:
        if CODE_FENCE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else INLINE_CODE.sub("", line))
    return out


def analyse(name, text):
    raw_lines = text.splitlines()
    lines = strip_code(raw_lines)
    words = load_wordlist()
    word_re = {w: re.compile(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", re.I) for w in words}

    hits = {k: [] for k in ("em dash", "colon split", "not X but Y", "hyphenated compound",
                            "wordlist", "closing summary", "passive (rough)")}
    hyphens = Counter()
    bullets = 0
    prose_lines = 0

    for i, line in enumerate(lines, 1):
        if not line.strip():
            continue
        prose_lines += 1
        if BULLET.match(line):
            bullets += 1
        if "—" in line or " -- " in line:
            hits["em dash"].append((i, line.strip()))
        if COLON_SPLIT.search(line) and not BULLET.match(line) and not line.lstrip().startswith("|"):
            hits["colon split"].append((i, line.strip()))
        if NOT_BUT.search(line) or NOT_ONLY.search(line):
            hits["not X but Y"].append((i, line.strip()))
        for m in HYPHEN.finditer(line):
            h = m.group(1).lower()
            if h not in OK_HYPHENS and not re.fullmatch(r"\d.*", h):
                hyphens[h] += 1
                hits["hyphenated compound"].append((i, h))
        for w, rx in word_re.items():
            if rx.search(line):
                hits["wordlist"].append((i, w))
        if PASSIVE.search(line):
            hits["passive (rough)"].append((i, line.strip()))

    # closing summaries: last sentence of each paragraph
    para, start = [], None
    paragraphs = []
    for i, line in enumerate(lines, 1):
        if line.strip():
            if start is None:
                start = i
            para.append(line.strip())
        elif para:
            paragraphs.append((start, " ".join(para)))
            para, start = [], None
    if para:
        paragraphs.append((start, " ".join(para)))
    for start, p in paragraphs:
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", p) if s.strip()]
        if len(sentences) >= 2 and SUMMARY_OPENERS.match(sentences[-1]):
            hits["closing summary"].append((start, sentences[-1]))

    print(f"== {name}: {prose_lines} non-empty lines, {len(paragraphs)} paragraphs, "
          f"{bullets} bullet lines ({(100 * bullets // prose_lines) if prose_lines else 0}%)")
    order = ["em dash", "colon split", "not X but Y", "hyphenated compound", "wordlist",
             "closing summary", "passive (rough)"]
    for key in order:
        items = hits[key]
        if not items:
            continue
        print(f"\n-- {key}: {len(items)}")
        if key == "hyphenated compound":
            for h, n in hyphens.most_common():
                where = ", ".join(str(l) for l, x in items if x == h)
                print(f"   {h} x{n}  (lines {where})")
        elif key == "wordlist":
            c = Counter(w for _, w in items)
            for w, n in c.most_common():
                where = ", ".join(str(l) for l, x in items if x == w)
                print(f"   {w} x{n}  (lines {where})")
        else:
            for l, s in items[:40]:
                print(f"   {l}: {s[:140]}")
            if len(items) > 40:
                print(f"   ... {len(items) - 40} more")
    print()


def main(argv):
    if len(argv) < 2:
        analyse("stdin", sys.stdin.read())
        return
    for path in argv[1:]:
        analyse(path, Path(path).read_text(errors="replace"))


if __name__ == "__main__":
    main(sys.argv)
