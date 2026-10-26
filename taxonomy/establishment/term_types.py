"""Task A runner: generate term types from the cached corpus and verify every citation.

    python -m taxonomy.establishment.term_types [--model claude-haiku-5-5] [--effort high] [--max-tokens 120000] [--thinking]

Writes output/term_types.raw.txt (model text), output/term_types.json (parsed result plus
run metadata) and output/term_types.verification.json (per-citation check: the cited
document and section exist and the quote occurs in that section).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone

from taxonomy.llm_context import ROOT, build_request, client, load_corpus
from taxonomy.establishment.prompts import TASKS, with_manifest

OUT_DIR = ROOT / "output" / "establishment"
RAW_OUT = OUT_DIR / "term_types.raw.txt"
JSON_OUT = OUT_DIR / "term_types.json"
VERIFY_OUT = OUT_DIR / "term_types.verification.json"

DOC_RE = re.compile(r'<document index="(\d+)"([^>]*)>\n(.*?)\n</document>', re.S)
SEC_RE = re.compile(r'<section label="([^"]*)">\n(.*?)\n</section>', re.S)


def parse_corpus(text: str) -> dict[int, dict[str, str]]:
    """{doc index: {section label: section text}} from the XML-tagged corpus."""
    return {int(m.group(1)): {s.group(1): s.group(2) for s in SEC_RE.finditer(m.group(3))}
            for m in DOC_RE.finditer(text)}


def manifest(text: str, docs: dict[int, dict[str, str]]) -> str:
    """One line per document: index, title, and its exact section labels."""
    titles = {int(m.group(1)): re.search(r'title="([^"]*)"', m.group(2)).group(1) for m in DOC_RE.finditer(text)}
    return "\n".join(f"doc {i} ({titles[i][:70]}): " + " | ".join(f'"{lab}"' for lab in secs)
                     for i, secs in docs.items())


def norm(s: str) -> str:
    """Lower-case alphanumerics only, no spaces: immune to line breaks, hyphenation, spacing
    artefacts of PDF extraction ('ve hicle', 'protocol-\nengineered') and punctuation."""
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def quote_found(quote: str, section: str, shingle: int = 12, threshold: float = 0.8) -> bool:
    """Exact (normalised) substring, else >= 80% of the quote's 12-char shingles occur inside one
    window of the section twice the quote's length. Localising the matches tolerates footnote
    markers and short insertions but rejects paraphrases stitched from phrases found elsewhere."""
    q, sec = norm(quote), norm(section)
    if len(q) < shingle:
        return bool(q) and q in sec
    if q in sec:
        return True
    grams = [q[i:i + shingle] for i in range(0, len(q) - shingle + 1)]
    hits = sorted({(m.start(), i) for i, g in enumerate(grams) for m in re.finditer(re.escape(g), sec)})
    if not hits:
        return False
    window, best, j = 2 * len(q), 0, 0
    for i, (pos, _) in enumerate(hits):
        while hits[j][0] < pos - window:
            j += 1
        best = max(best, len({gi for _, gi in hits[j:i + 1]}))
    return best / len(grams) >= threshold


def verify(result: dict, docs: dict[int, dict[str, str]]) -> dict:
    """Check every citation in place. Sets c["verified"] on each citation; when the quote is
    found in the cited document under a different label, repairs c["section"] and keeps the
    model's label in c["cited_section"] (status "relabelled", counted as verified)."""
    checks = []
    for tt in result.get("term_types", []):
        cites = [("type", c) for c in tt.get("citations", [])]
        for v in tt.get("values", []):
            cites += [(f"value:{v.get('value', '')}", c) for c in v.get("citations", [])]
        for where, c in cites:
            doc = docs.get(c.get("doc"))
            quote = c.get("quote", "")
            if doc is None:
                status = "no_such_document"
            elif c.get("section") in doc and quote_found(quote, doc[c["section"]]):
                status = "ok"
            else:
                hit = next((lab for lab, txt in doc.items() if quote_found(quote, txt)), None)
                if hit is not None:
                    c["cited_section"], c["section"], status = c.get("section"), hit, "relabelled"
                else:
                    status = "no_such_section" if c.get("section") not in doc else "quote_not_found"
            c["verified"] = status in ("ok", "relabelled")
            checks.append({"term_type": tt.get("id"), "where": where, "status": status, **c})
    n = len(checks)
    ok = sum(1 for c in checks if c["verified"])
    return {"citations": n, "verified": ok, "exact": sum(1 for c in checks if c["status"] == "ok"),
            "relabelled": sum(1 for c in checks if c["status"] == "relabelled"),
            "rejection_rate": round(1 - ok / n, 4) if n else None,
            "rejected": [c for c in checks if not c["verified"]]}


def extract_json(text: str) -> dict:
    """Parse the model's JSON; if it is truncated, salvage every complete term type."""
    text = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", text.strip())
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < 0:
        sys.exit("model output contains no JSON object; see " + str(RAW_OUT))
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        pass
    arr = text.find("[", text.find('"term_types"'))
    dec, pos, items = json.JSONDecoder(), arr + 1, []
    while True:
        m = re.compile(r"\s*,?\s*").match(text, pos)
        pos = m.end()
        if pos >= len(text) or text[pos] != "{":
            break
        try:
            obj, pos = dec.raw_decode(text, pos)
        except json.JSONDecodeError:
            break
        items.append(obj)
    print(f"WARNING: JSON truncated; salvaged {len(items)} complete term types", file=sys.stderr)
    return {"term_types": items, "coverage_notes": "", "truncated": True}


def run(model: str, effort: str, max_tokens: int, thinking: bool) -> tuple[str, object, float]:
    instructions, prompt = TASKS["A"]
    corpus = load_corpus()
    prompt = with_manifest(prompt, manifest(corpus, parse_corpus(corpus)))
    # Haiku 5.5 thinks by default; on this 235K-token corpus adaptive thinking ran past 100K
    # tokens without emitting any text, so thinking is off unless --thinking is given.
    req = build_request(instructions, prompt, model=model, max_tokens=max_tokens, effort=effort,
                        thinking={"type": "adaptive"} if thinking else {"type": "disabled"})
    t0 = time.time()
    with client().messages.stream(**req) as stream:      # streaming: long outputs, no request timeout
        msg = stream.get_final_message()
    text = "".join(b.text for b in msg.content if b.type == "text")
    return text, msg, time.time() - t0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--effort", default="high", choices=["low", "medium", "high"])
    ap.add_argument("--max-tokens", type=int, default=120000)  # model ceiling is 128K; a full pass is ~60-70K
    ap.add_argument("--thinking", action="store_true", help="enable adaptive thinking (counts toward max-tokens)")
    ap.add_argument("--verify-only", action="store_true", help="re-verify output/term_types.raw.txt without calling the API")
    args = ap.parse_args()
    OUT_DIR.mkdir(exist_ok=True)

    if args.verify_only:
        text, meta = RAW_OUT.read_text(encoding="utf-8"), json.loads(JSON_OUT.read_text())["run"]
    else:
        text, msg, secs = run(args.model, args.effort, args.max_tokens, args.thinking)
        RAW_OUT.write_text(text, encoding="utf-8")
        u = msg.usage
        meta = {"task": "A", "model": msg.model, "effort": args.effort, "thinking": args.thinking, "stop_reason": msg.stop_reason,
                "seconds": round(secs, 1), "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "usage": {"input_tokens": u.input_tokens, "output_tokens": u.output_tokens,
                          "cache_creation_input_tokens": u.cache_creation_input_tokens,
                          "cache_read_input_tokens": u.cache_read_input_tokens}}
        if msg.stop_reason == "max_tokens":
            print("WARNING: output truncated at max_tokens; raise --max-tokens", file=sys.stderr)

    result = extract_json(text)
    report = verify(result, parse_corpus(load_corpus()))
    JSON_OUT.write_text(json.dumps({"run": meta, **result}, indent=2, ensure_ascii=False), encoding="utf-8")
    VERIFY_OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"{'id':40} {'applies_to':18} vals cites docs")
    for tt in result["term_types"]:
        n_c = len(tt.get("citations", [])) + sum(len(v.get("citations", [])) for v in tt.get("values", []))
        print(f"{tt['id'][:40]:40} {tt.get('applies_to', '')[:18]:18} {len(tt.get('values', [])):4d} {n_c:5d} "
              f"{len(tt.get('sources', {}).get('documents', [])):4d}")
    print(f"\n{len(result['term_types'])} term types; citations {report['verified']}/{report['citations']} verified "
          f"({report['exact']} exact, {report['relabelled']} relabelled; rejection rate {report['rejection_rate']}); "
          f"usage {meta['usage']}; stop={meta['stop_reason']}")
    print(f"-> {JSON_OUT}\n-> {VERIFY_OUT}")


if __name__ == "__main__":
    main()
