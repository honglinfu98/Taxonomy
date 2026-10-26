"""PDF -> text utilities: extraction, range selection, noise removal."""
from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

# Page headers / footers / typesetting artefacts dropped from every extracted line.
NOISE = re.compile(
    r"^\s*("
    r"VerDate|Jkt |PO 00000|Frm 0|Fmt |Sfmt |\S+ on \S+PROD with|•HR |HR \d+ (RFS|IH|RH|EH|RS)\s*$|E:\\BILLS|Insert offset|"  # congress footers
    r"PUBLIC LAW 119|139 STAT\.|"                                                               # statutes at large
    r"Federal Register / Vol\.|"                                                                 # EO
    r"EN\s*$|OJ L[, ]|ELI: |L \d+/\d+\s*$|\d{1,2}\.\d{1,2}\.\d{4}\s*$|Official Journal of the European Union|"  # EU OJ
    r"F I N C E N|G U I D A N C E|"                                                              # FinCEN
    r"©|Prudential treatment of cryptoasset exposures\s*$|UPDATED GUIDANCE: A RISK-BASED|"
    r"STRENGTHENING AMERICAN LEADERSHIP|FATF/OECD|Targeted Update on Implementation|"
    r"VIRTUAL ASSETS AND VIRTUAL ASSET SERVICE PROVIDERS|VIRTUAL ASSETS: TARGETED UPDATE|"
    r"STREN ?GTH ?EN ?I ?N ?G AMERI ?CAN|.*•\ufeff\s*$|"                                        # PWG report
    r"arXiv:\d{4}\.\d{4,5}v\d"                                                                   # arXiv stamp
    r")"
)
ONLY_NUMBER = re.compile(r"^\s*\d{1,4}\s*$")           # bare page numbers
BILL_LINE_NO = re.compile(r"^\s*\d{1,2}\s+(?=\S)")     # congress line numbers (layout mode)
SIDE_NOTE = re.compile(r"\s{3,}\d+ USC \d+.*$")        # Statutes-at-Large margin notes


def pdf_to_lines(pdf: Path, layout: bool) -> list[str]:
    """Run pdftotext (optionally -layout) and return the lines."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    cmd = ["pdftotext"] + (["-layout"] if layout else []) + [str(pdf), str(tmp_path)]
    subprocess.run(cmd, check=True)
    text = tmp_path.read_text(encoding="utf-8", errors="replace")
    tmp_path.unlink()
    # NB: split on '\n' only; str.splitlines() would also split on form feeds
    # and shift every line number by one per page.
    return text.replace("\x0c", "").split("\n")


def select(lines: list[str], start: int | str, end: int | str) -> list[str]:
    """Slice by 1-indexed line numbers and/or regex markers (end is exclusive for regex,
    inclusive for an int). A regex end that never matches runs to end of file."""
    if isinstance(start, int):
        s = start - 1
    else:
        s_re = re.compile(start)
        s = next(i for i, ln in enumerate(lines) if s_re.search(ln))
    if isinstance(end, int):
        return lines[s:end]
    e_re = re.compile(end)
    e = next((i for i in range(s + 1, len(lines)) if e_re.search(lines[i])), len(lines))
    return lines[s:e]


def clean(lines: list[str], layout: bool) -> str:
    """Drop noise lines; in layout mode also strip bill line numbers and rejoin hyphenation."""
    out: list[str] = []
    for ln in lines:
        s = ln.rstrip()
        if ONLY_NUMBER.match(s) or NOISE.search(s):
            continue
        if layout:
            s = SIDE_NOTE.sub("", s)
            s = BILL_LINE_NO.sub("", s)
            s = re.sub(r"\s{2,}", " ", s.strip())
        out.append(s)
    text = "\n".join(out)
    if layout:
        text = re.sub(r"(\w)-\n\s*(?=[a-z])", r"\1", text)  # rejoin hyphenated breaks
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
