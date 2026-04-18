#!/usr/bin/env python3
"""Render each nav doc and emit {path: sha256} JSON.

Used by the PR preview CI job to detect which docs render differently
between the base branch and the PR HEAD without touching Discourse.
Link rewriting uses an empty topic_id_map so the hash is reproducible
across refs.
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


def main() -> None:
  out: dict[str, str] = {}
  for entry in parse_all(ZENSICAL_TOML):
    fp = DOCS_DIR / entry.path
    if not fp.exists():
      continue
    converted = convert(
      fp.read_text(encoding="utf-8"),
      file_path=entry.path, topic_id_map={},
    )
    body = converted.rstrip("\n") + build_footer(entry.path)
    out[entry.path] = hashlib.sha256(body.encode("utf-8")).hexdigest()
  json.dump(out, sys.stdout, sort_keys=True)
  sys.stdout.write("\n")


if __name__ == "__main__":
  main()
