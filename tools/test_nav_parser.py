#!/usr/bin/env python3
"""Tests for the zensical.toml nav parser.

Run: uv run python tools/test_nav_parser.py
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from nav_parser import NavEntry, parse, parse_all, _flatten_nav

ZENSICAL_TOML = Path(__file__).resolve().parent.parent.parent / "zensical.toml"


# ---------------------------------------------------------------------------
# Unit tests: _flatten_nav
# ---------------------------------------------------------------------------


def test_flatten_simple_dict():
  nav = [{"Page One": "page-one.md"}]
  result = _flatten_nav(nav)
  assert len(result) == 1
  assert result[0] == NavEntry(title="Page One", path="page-one.md", breadcrumb=("Page One",))
  print("  PASS: flatten_simple_dict")


def test_flatten_nested():
  nav = [
    {"Section": [
      {"Child A": "section/a.md"},
      {"Child B": "section/b.md"},
    ]},
  ]
  result = _flatten_nav(nav)
  assert len(result) == 2
  assert result[0].title == "Child A"
  assert result[0].path == "section/a.md"
  assert result[0].breadcrumb == ("Section", "Child A")
  assert result[1].breadcrumb == ("Section", "Child B")
  print("  PASS: flatten_nested")


def test_flatten_deep_nesting():
  nav = [
    {"L1": [
      {"L2": [
        {"L3": "deep/page.md"},
      ]},
    ]},
  ]
  result = _flatten_nav(nav)
  assert len(result) == 1
  assert result[0].breadcrumb == ("L1", "L2", "L3")
  assert result[0].path == "deep/page.md"
  print("  PASS: flatten_deep_nesting")


def test_flatten_skips_external_links():
  nav = [
    {"Docs": "docs.md"},
    {"Forum": "https://community.sunnypilot.ai"},
  ]
  result = _flatten_nav(nav)
  assert len(result) == 1
  assert result[0].title == "Docs"
  print("  PASS: flatten_skips_external_links")


def test_flatten_bare_string():
  nav = ["getting-started/index.md"]
  result = _flatten_nav(nav)
  assert len(result) == 1
  assert result[0].title == "Index"
  assert result[0].path == "getting-started/index.md"
  print("  PASS: flatten_bare_string")


def test_flatten_mixed():
  nav = [
    {"Home": "index.md"},
    {"Features": [
      "features/index.md",
      {"ICBM": "features/cruise/icbm.md"},
      {"Forum": "https://example.com"},
    ]},
  ]
  result = _flatten_nav(nav)
  assert len(result) == 3  # Home, features/index.md (bare), ICBM
  titles = [e.title for e in result]
  assert "Home" in titles
  assert "ICBM" in titles
  assert "Forum" not in titles
  print("  PASS: flatten_mixed")


# ---------------------------------------------------------------------------
# Unit tests: parse (filters index.md/README.md)
# ---------------------------------------------------------------------------


def test_parse_filters_index():
  """parse() should exclude index.md and README.md entries."""
  toml_content = b"""
[project]
nav = [
  {"Home" = "index.md"},
  {"Guide" = [
    "guide/index.md",
    {"Setup" = "guide/setup.md"},
  ]},
]
"""
  with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as f:
    f.write(toml_content)
    f.flush()
    result = parse(f.name)

  assert len(result) == 1
  assert result[0].title == "Setup"
  assert result[0].path == "guide/setup.md"
  print("  PASS: parse_filters_index")


def test_parse_all_includes_index():
  """parse_all() should include index.md entries."""
  toml_content = b"""
[project]
nav = [
  {"Home" = "index.md"},
  {"Setup" = "guide/setup.md"},
]
"""
  with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as f:
    f.write(toml_content)
    f.flush()
    result = parse_all(f.name)

  assert len(result) == 2
  titles = [e.title for e in result]
  assert "Home" in titles
  assert "Setup" in titles
  print("  PASS: parse_all_includes_index")


# ---------------------------------------------------------------------------
# Integration: parse real zensical.toml
# ---------------------------------------------------------------------------


def test_parse_real_zensical():
  """Parse the actual zensical.toml and verify structure."""
  if not ZENSICAL_TOML.exists():
    print("  SKIP: parse_real_zensical (zensical.toml not found)")
    return

  all_entries = parse_all(ZENSICAL_TOML)
  filtered_entries = parse(ZENSICAL_TOML)

  # Sanity checks on totals
  assert len(all_entries) > 50, f"Expected 50+ total entries, got {len(all_entries)}"
  assert len(filtered_entries) > 40, f"Expected 40+ filtered entries, got {len(filtered_entries)}"
  assert len(filtered_entries) < len(all_entries), "Filtering should remove some entries"

  # Every filtered entry should NOT be index.md or README.md
  for entry in filtered_entries:
    assert Path(entry.path).name not in ("index.md", "README.md"), (
      f"Filtered list contains {entry.path}"
    )

  # No external links should be present
  for entry in all_entries:
    assert not entry.path.startswith("http"), f"External link leaked: {entry.path}"

  # Check some known entries exist
  paths = {e.path for e in filtered_entries}
  assert "getting-started/what-is-sunnypilot.md" in paths, "Missing what-is-sunnypilot"
  assert "features/cruise/icbm.md" in paths, "Missing ICBM"
  assert "safety/safety.md" in paths, "Missing safety"

  # Check breadcrumbs are populated
  icbm = next(e for e in filtered_entries if e.path == "features/cruise/icbm.md")
  assert len(icbm.breadcrumb) >= 2, f"ICBM breadcrumb too short: {icbm.breadcrumb}"
  assert "Features" in icbm.breadcrumb or "Cruise Control" in icbm.breadcrumb

  print(f"  PASS: parse_real_zensical ({len(all_entries)} total, {len(filtered_entries)} filtered)")


def test_nav_entry_immutable():
  """NavEntry is frozen — attributes cannot be reassigned."""
  entry = NavEntry(title="Test", path="test.md", breadcrumb=("Test",))
  try:
    entry.title = "Modified"  # type: ignore[misc]
    assert False, "Should have raised FrozenInstanceError"
  except AttributeError:
    pass
  print("  PASS: nav_entry_immutable")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


if __name__ == "__main__":
  print("Testing nav parser:")
  tests = [
    # Unit
    test_flatten_simple_dict,
    test_flatten_nested,
    test_flatten_deep_nesting,
    test_flatten_skips_external_links,
    test_flatten_bare_string,
    test_flatten_mixed,
    test_parse_filters_index,
    test_parse_all_includes_index,
    test_nav_entry_immutable,
    # Integration
    test_parse_real_zensical,
  ]
  passed = 0
  failed = 0
  for test in tests:
    try:
      test()
      passed += 1
    except AssertionError as e:
      print(f"  FAIL: {test.__name__}: {e}")
      failed += 1
    except Exception as e:
      print(f"  ERROR: {test.__name__}: {e}")
      failed += 1

  print(f"\n{passed}/{passed + failed} tests passed")
  sys.exit(1 if failed > 0 else 0)
