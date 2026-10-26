"""Build the Claude-API-ready corpus for term-type extraction.

Run from the repo root with the venv active (pdftotext from poppler must be on PATH):

    python -m taxonomy.build_corpus

Writes context/taxonomy_corpus.txt: the definitions / glossary sections of every
PDF in legal/ plus the three papers in context/, as XML-tagged <document> blocks.
What is taken from each PDF is specified in taxonomy/sources.py.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from taxonomy.pdf_text import clean, pdf_to_lines, select
from taxonomy.sources import PAPERS, SOURCES

ROOT = Path(__file__).resolve().parents[1]
LEGAL = ROOT / "legal"
CONTEXT = ROOT / "context"
CORPUS_OUT = CONTEXT / "taxonomy_corpus.txt"

PREAMBLE = (
    '<context_corpus purpose="source material for extracting cryptocurrency / DLT term types for a taxonomy">\n'
    "<readme>\n"
    "This corpus has two kinds of documents. Documents of type taxonomy_framework and\n"
    "domain_corpus_paper are academic papers (reference lists removed) that propose\n"
    "classification dimensions for blockchains and crypto-assets. Documents of type\n"
    "legal_instrument are the definitions articles, glossaries, classification criteria\n"
    "and business-model descriptions from statutes, regulations and standard-setter\n"
    "guidance in the EU, UK, US and international bodies (FATF, Basel, FSB, IOSCO, UN,\n"
    "Council of Europe). Each document is split into labelled sections. Text is machine-\n"
    "extracted from PDF: tables may read as one value per line and some words carry\n"
    "typesetting breaks. Cite documents by their index and section label.\n"
    "</readme>\n\n"
)


def extract_sections(pdf: Path, layout: bool, ranges) -> list[tuple[str, str]]:
    if not pdf.exists():
        sys.exit(f"missing {pdf}")
    lines = pdf_to_lines(pdf, layout)
    return [(label, clean(select(lines, start, end), layout)) for start, end, label in ranges]


def legal_meta(title: str, pdf: Path) -> dict[str, str]:
    jurisdiction, instrument = [p.strip() for p in title.split("|", 1)]
    year = re.search(r"(?<!\d)(19|20)\d{2}(?!\d)", pdf.name) or re.search(r"(19|20)\d{2}", instrument)
    return {"type": "legal_instrument", "jurisdiction": jurisdiction, "title": instrument,
            "year": year.group(0) if year else "", "source_file": pdf.name}


def attr(s: str) -> str:
    return s.replace('"', "'")


def render(index: int, meta: dict[str, str], sections: list[tuple[str, str]]) -> str:
    attrs = " ".join(f'{k}="{attr(v)}"' for k, v in meta.items())
    body = "\n\n".join(f'<section label="{attr(label)}">\n{text}\n</section>' for label, text in sections)
    return f'<document index="{index}" {attrs}>\n{body}\n</document>'


def build() -> list[tuple[dict[str, str], list[tuple[str, str]]]]:
    """Return (metadata, sections) for every document: papers first, then legal instruments."""
    docs = []
    for stem, meta, ranges in PAPERS:
        pdf = CONTEXT / f"{stem}.pdf"
        docs.append(({**meta, "source_file": pdf.name}, extract_sections(pdf, False, ranges)))
    for stem, title, layout, ranges in SOURCES:
        pdf = LEGAL / f"{stem}.pdf"
        docs.append((legal_meta(title, pdf), extract_sections(pdf, layout, ranges)))
    return docs


def main() -> None:
    CONTEXT.mkdir(exist_ok=True)
    docs = build()
    rendered = [render(i, meta, secs) for i, (meta, secs) in enumerate(docs, start=1)]
    CORPUS_OUT.write_text(PREAMBLE + "\n\n".join(rendered) + "\n</context_corpus>\n", encoding="utf-8")

    total = 0
    for meta, secs in docs:
        words = sum(len(t.split()) for _, t in secs)
        total += words
        label = f"{meta['jurisdiction']} | {meta['title']}" if "jurisdiction" in meta else meta["title"]
        print(f"{words:7d} words  {label}")
    print(f"TOTAL {total} words in {len(docs)} documents -> {CORPUS_OUT}")


if __name__ == "__main__":
    main()
