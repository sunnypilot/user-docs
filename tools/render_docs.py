#!/usr/bin/env python3
"""Render each nav doc the same way sync_to_discourse.py would, emit JSON.

Writes ``{<doc_path>: <sha256 of rendered body>}`` to stdout.  Used by
the PR preview CI job to detect which docs actually render
differently between the base branch and the PR HEAD without touching
Discourse.  An empty topic_id_map is passed to converter.convert so
internal .md links always fall back to search URLs — the goal is a
consistent, reproducible hash between refs, not a real sync body.

Env:
  DOCS_SYNC_REF_NAME   — ref used in the footer "Suggest changes" link.
  DISCOURSE_URL        — forum base URL used by converter for link rewrites.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from converter import convert
from nav_parser import parse_all
from sync_to_discourse import DOCS_DIR, ZENSICAL_TOML, build_footer


def _render(doc_path: str) -> str | None:
  file_path = DOCS_DIR / doc_path
  if not file_path.exists():
    return None
  content = file_path.read_text(encoding="utf-8")
  converted = convert(content, file_path=doc_path, topic_id_map={})
  return converted.rstrip("\n") + build_footer(doc_path)


def main() -> None:
  out: dict[str, str] = {}
  for entry in parse_all(ZENSICAL_TOML):
    body = _render(entry.path)
    if body is None:
      continue
    out[entry.path] = hashlib.sha256(body.encode("utf-8")).hexdigest()
  json.dump(out, sys.stdout, indent=2, sort_keys=True)
  sys.stdout.write("\n")


if __name__ == "__main__":
  main()
