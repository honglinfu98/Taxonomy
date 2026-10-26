"""Helpers for sending context/taxonomy_corpus.txt to the Claude API.

    from taxonomy.llm_context import build_request, client

    resp = client().messages.create(**build_request(
        instructions="You are a legal and technical taxonomist ...",
        user_prompt="List every distinct term type for 'stablecoin' across the corpus ...",
    ))
    print(resp.content[0].text)
    print(resp.usage)                        # cache_read_input_tokens > 0 on repeat calls

The corpus goes in the system prompt behind a 1-hour cache breakpoint, so every
prompt-engineering iteration pays only for the (small) uncached part.

ANTHROPIC_API_KEY is read from the repo-root .env (gitignored; see .env.example).
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
CORPUS_FILE = ROOT / "context" / "taxonomy_corpus.txt"
DEFAULT_MODEL = "claude-haiku-5-5"

load_dotenv(ROOT / ".env")


def client():
    """anthropic.Anthropic() with the key from .env; fails early if it is missing."""
    import anthropic  # imported lazily so build_corpus does not need the SDK

    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY not set: add it to .env (see .env.example)")
    return anthropic.Anthropic()


def load_corpus() -> str:
    return CORPUS_FILE.read_text(encoding="utf-8")


def build_request(instructions: str, user_prompt: str, *, model: str = DEFAULT_MODEL,
                  max_tokens: int = 16000, effort: str = "medium",
                  extra_system: list[str] | None = None, **extra) -> dict:
    """Return kwargs for client.messages.create(...).

    Keep `instructions` stable across calls: it sits before the cached corpus, and any
    change to it invalidates the cache. Put anything that varies in `user_prompt`.
    `extra_system` blocks (e.g. the Task A catalogue for Task B) go after the corpus, each
    behind its own 1-hour cache breakpoint, so the corpus cache survives when they change.
    Extra keyword arguments (e.g. thinking={"type": "disabled"}) are passed through.
    """
    cache = {"cache_control": {"type": "ephemeral", "ttl": "1h"}}
    return {
        **extra,
        "model": model,
        "max_tokens": max_tokens,
        "output_config": {"effort": effort},
        "system": [
            {"type": "text", "text": instructions},
            {"type": "text", "text": load_corpus(), **cache},
            *({"type": "text", "text": t, **cache} for t in (extra_system or [])),
        ],
        "messages": [{"role": "user", "content": user_prompt}],
    }
