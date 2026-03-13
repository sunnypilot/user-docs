"""Parse zensical.toml nav structure into a flat list of doc entries.

Reads the nav tree from zensical.toml and produces a flat list of
{title, path, breadcrumb} dicts suitable for the sync orchestrator.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

SKIP_FILES = frozenset({"index.md", "README.md"})


@dataclass(frozen=True)
class NavEntry:
  """A single navigable documentation page."""

  title: str
  path: str
  breadcrumb: tuple[str, ...] = field(default_factory=tuple)


def parse(config_path: str | Path) -> list[NavEntry]:
  """Parse zensical.toml and return all nav entries.

  Args:
    config_path: Path to zensical.toml.

  Returns:
    Flat list of NavEntry for every page in the nav tree,
    excluding index.md, README.md, and external links.
  """
  config_path = Path(config_path)
  with config_path.open("rb") as f:
    config = tomllib.load(f)

  nav = config.get("project", {}).get("nav", [])
  entries = _flatten_nav(nav)
  return [e for e in entries if Path(e.path).name not in SKIP_FILES]


def parse_all(config_path: str | Path) -> list[NavEntry]:
  """Like parse(), but includes index.md and README.md entries."""
  config_path = Path(config_path)
  with config_path.open("rb") as f:
    config = tomllib.load(f)

  nav = config.get("project", {}).get("nav", [])
  return _flatten_nav(nav)


def _flatten_nav(
  items: list[dict[str, str | list] | str],
  breadcrumb: tuple[str, ...] = (),
) -> list[NavEntry]:
  """Recursively flatten the nav tree into NavEntry objects."""
  result: list[NavEntry] = []

  for item in items:
    if isinstance(item, dict):
      for title, value in item.items():
        if isinstance(value, str):
          # Skip external links
          if value.startswith("http"):
            continue
          result.append(NavEntry(
            title=title,
            path=value,
            breadcrumb=breadcrumb + (title,),
          ))
        elif isinstance(value, list):
          result.extend(
            _flatten_nav(value, breadcrumb + (title,))
          )
    elif isinstance(item, str):
      # Bare path without title
      if item.startswith("http"):
        continue
      name = Path(item).stem.replace("-", " ").capitalize()
      result.append(NavEntry(
        title=name,
        path=item,
        breadcrumb=breadcrumb + (name,),
      ))

  return result
