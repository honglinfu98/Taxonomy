"""RQ6 ablations of Task A: one ingredient of the prompt removed or changed, everything else as
in the main run (whole corpus in one cached context, Haiku 5.5, thinking disabled).

    python -m taxonomy.baselines.ablate no_manifest no_citations no_definitions effort_low [--model ...]

Variants:
  no_manifest     the task prompt without the manifest of exact section labels (the model has to
                  reproduce labels from the context); measures label accuracy and the catalogue
  no_citations    grounding rules 1-3 and the citation fields removed; the corpus is still declared
                  the only source of truth; citations empty by construction
  no_definitions  the definitions block (term, term type, grounded) removed from the system
                  instructions, so the model works from the words "term type" alone
  effort_low      the full prompt at effort low instead of high

Writes output/ablations/<variant>/term_types.{json,verification.json} and term_types.raw.txt in
the Task A shape, priced at the long-prompt card. `rq6.py` scores the rows.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone

from taxonomy.establishment.prompts import TASKS, with_manifest
from taxonomy.establishment.term_types import extract_json, manifest, parse_corpus, verify
from taxonomy.evaluation.billing import price
from taxonomy.evaluation.common import NO_DISABLE
from taxonomy.llm_context import ROOT, build_request, client, load_corpus

OUT = ROOT / "output" / "ablations"

VARIANTS = {
    "no_manifest": "task prompt without the manifest of section labels",
    "no_citations": "grounding rules and citation fields removed (no citation requirement)",
    "no_definitions": "definitions of term, term type and grounded removed from the instructions",
    "effort_low": "full prompt at effort low",
}


def no_citations(instructions: str, prompt: str) -> tuple[str, str]:
    head, rest = instructions.split("Grounding rules (strict):", 1)
    quality = rest.split("Quality rules:", 1)[1]
    quality = re.sub(r"^(\d)\.", lambda m: f"{int(m.group(1)) - 3}.", quality, flags=re.M)
    instr = (head + "Grounding rule: propose only dimensions the corpus itself uses as a criterion or defines "
             "several terms along; do not add dimensions from outside knowledge.\n\nQuality rules:" + quality)
    p = "\n".join(l for l in prompt.split("\n") if '"citations"' not in l)
    p = re.sub(r",(\s*\n\s*[}\]])", r"\1", p)                      # trailing commas left by the removed lines
    p = p.replace(" Keep quotes short and verbatim.", "")
    return instr, p


def no_definitions(instructions: str, prompt: str) -> tuple[str, str]:
    head, rest = instructions.split("Definitions used in this work:", 1)
    return head + "Grounding rules (strict):" + rest.split("Grounding rules (strict):", 1)[1], prompt


def build(variant: str) -> tuple[str, str, str]:
    """(instructions, prompt, effort) for a variant."""
    instructions, prompt = TASKS["A"]
    effort = "high"
    corpus = load_corpus()
    man = manifest(corpus, parse_corpus(corpus))
    if variant == "no_manifest":
        return instructions, prompt, effort
    if variant == "no_citations":
        instructions, prompt = no_citations(instructions, prompt)
    elif variant == "no_definitions":
        instructions, prompt = no_definitions(instructions, prompt)
    elif variant == "effort_low":
        effort = "low"
    elif variant != "full":
        raise SystemExit(f"unknown variant {variant}")
    return instructions, with_manifest(prompt, man), effort


def run(variant: str, model: str, max_tokens: int) -> None:
    instructions, prompt, effort = build(variant)
    d = OUT / variant
    d.mkdir(parents=True, exist_ok=True)
    (d / "prompt.txt").write_text("### SYSTEM INSTRUCTIONS\n" + instructions + "\n\n### USER PROMPT\n" + prompt, encoding="utf-8")
    extra = {} if model in NO_DISABLE else {"thinking": {"type": "disabled"}}
    req = build_request(instructions, prompt, model=model, max_tokens=max_tokens, effort=effort, **extra)
    t0 = time.time()
    with client().messages.stream(**req) as stream:
        msg = stream.get_final_message()
    secs = time.time() - t0
    text = "".join(b.text for b in msg.content if b.type == "text")
    (d / "term_types.raw.txt").write_text(text, encoding="utf-8")
    u = msg.usage
    usage = {"input_tokens": u.input_tokens, "output_tokens": u.output_tokens,
             "cache_creation_input_tokens": u.cache_creation_input_tokens or 0, "cache_read_input_tokens": u.cache_read_input_tokens or 0}
    result = extract_json(text)
    emitted = 0
    if variant == "no_citations":                                   # citations empty by construction
        for t in result["term_types"]:
            emitted += len(t.pop("citations", []) or [])
            t["citations"] = []
            for v in t.get("values", []):
                emitted += len(v.pop("citations", []) or [])
                v["citations"] = []
    meta = {"task": "A", "variant": variant, "description": VARIANTS[variant], "model": msg.model, "effort": effort,
            "thinking": False, "stop_reason": msg.stop_reason, "seconds": round(secs, 1),
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"), "usage": usage,
            "cost_usd": round(price(usage, model, long_prompt=True)[0], 4), "citations_emitted_and_dropped": emitted}
    report = verify(result, parse_corpus(load_corpus()))
    (d / "term_types.json").write_text(json.dumps({"run": meta, **result}, indent=2, ensure_ascii=False), encoding="utf-8")
    (d / "term_types.verification.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    if msg.stop_reason == "max_tokens":
        print("WARNING: output truncated at max_tokens", file=sys.stderr)
    print(f"{variant}: {len(result['term_types'])} term types, {sum(len(t.get('values', [])) for t in result['term_types'])} values; "
          f"citations {report['verified']}/{report['citations']} verified ({report['exact']} exact, {report['relabelled']} relabelled); "
          f"${meta['cost_usd']}, {meta['seconds']} s, stop={msg.stop_reason} -> {d / 'term_types.json'}", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("variants", nargs="+", choices=list(VARIANTS))
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--max-tokens", type=int, default=120000)
    a = ap.parse_args()
    for v in a.variants:
        run(v, a.model, a.max_tokens)


if __name__ == "__main__":
    main()
