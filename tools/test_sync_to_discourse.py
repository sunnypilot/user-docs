#!/usr/bin/env python3
"""Tests for the sync orchestrator (fully mocked, no live requests).

Run: python3 tools/test_sync_to_discourse.py
"""

import argparse
import json
import sys
import tempfile
import textwrap
import urllib.request
from pathlib import Path
from unittest.mock import MagicMock, call, patch

sys.path.insert(0, str(Path(__file__).parent))

from sync_to_discourse import (
  _get_section_folder,
  _resolve_topic_id,
  _walk_nav_for_sidebar,
  build_footer,
  extract_title,
  sync_docs,
)
from discourse_client import DiscourseClient, DiscourseConfig

TEST_CONFIG = DiscourseConfig(
  base_url="https://community.sunnypilot.ai",
  api_key="test-key",
  api_user="system",
  category_mapping={"getting-started": 133, "features": 135},
)


# ---------------------------------------------------------------------------
# extract_title
# ---------------------------------------------------------------------------


def test_extract_title_from_front_matter():
  content = "---\ntitle: Alpha Longitudinal\n---\n\n# Alpha Longitudinal\n"
  assert extract_title(content, "fallback") == "Alpha Longitudinal"
  print("  PASS: extract_title_from_front_matter")


def test_extract_title_from_heading():
  content = "# Neural Network Lateral Control\n\nSome content."
  assert extract_title(content, "fallback") == "Neural Network Lateral Control"
  print("  PASS: extract_title_from_heading")


def test_extract_title_fallback():
  content = "No title here, just content.\n"
  assert extract_title(content, "My Fallback") == "My Fallback"
  print("  PASS: extract_title_fallback")


def test_extract_title_quoted():
  content = '---\ntitle: "Quoted Title"\n---\n'
  assert extract_title(content, "fallback") == "Quoted Title"
  print("  PASS: extract_title_quoted")


# ---------------------------------------------------------------------------
# build_footer
# ---------------------------------------------------------------------------


def test_build_footer_contains_sync_id():
  footer = build_footer("features/cruise/icbm.md")
  assert "[^docs-sync]: docs-sync-id: features/cruise/icbm.md" in footer
  assert "[^docs-sync]" in footer.split("[^docs-sync]:")[0]  # reference before definition
  print("  PASS: build_footer_contains_sync_id")


def test_build_footer_contains_github_link():
  footer = build_footer("getting-started/what-is-sunnypilot.md")
  assert "github.com/sunnypilot/user-docs/blob/" in footer
  assert "docs/getting-started/what-is-sunnypilot.md" in footer
  print("  PASS: build_footer_contains_github_link")


def test_build_footer_starts_with_separator():
  footer = build_footer("test.md")
  assert footer.startswith("\n\n---\n")
  print("  PASS: build_footer_starts_with_separator")


# ---------------------------------------------------------------------------
# _get_section_folder
# ---------------------------------------------------------------------------


def test_get_section_folder_from_index():
  items = [
    "getting-started/index.md",
    {"What is sunnypilot?": "getting-started/what-is-sunnypilot.md"},
  ]
  assert _get_section_folder(items) == "getting-started"
  print("  PASS: get_section_folder_from_index")


def test_get_section_folder_from_dict():
  items = [
    {"ICBM": "features/cruise/icbm.md"},
  ]
  assert _get_section_folder(items) == "features"
  print("  PASS: get_section_folder_from_dict")


def test_get_section_folder_nested():
  items = [
    "features/index.md",
    {"Cruise Control": [
      "features/cruise/index.md",
      {"ICBM": "features/cruise/icbm.md"},
    ]},
  ]
  assert _get_section_folder(items) == "features"
  print("  PASS: get_section_folder_nested")


def test_get_section_folder_external_link():
  items = [
    {"Forum": "https://community.sunnypilot.ai"},
  ]
  assert _get_section_folder(items) is None
  print("  PASS: get_section_folder_external_link")


def test_get_section_folder_empty():
  assert _get_section_folder([]) is None
  print("  PASS: get_section_folder_empty")


# ---------------------------------------------------------------------------
# _resolve_topic_id
# ---------------------------------------------------------------------------


def test_resolve_topic_id_cached():
  synced = {"features/cruise/icbm.md": 244}
  client = DiscourseClient(TEST_CONFIG)

  result = _resolve_topic_id("features/cruise/icbm.md", synced, client)
  assert result == 244
  print("  PASS: resolve_topic_id_cached")


@patch("urllib.request.urlopen")
def test_resolve_topic_id_api_lookup(mock_urlopen: MagicMock):
  mock_urlopen.return_value = _mock_response({
    "topics": [{"id": 244, "title": "ICBM"}],
  })
  synced: dict[str, int] = {}
  client = DiscourseClient(TEST_CONFIG)

  result = _resolve_topic_id("features/cruise/icbm.md", synced, client)
  assert result == 244
  assert synced["features/cruise/icbm.md"] == 244
  print("  PASS: resolve_topic_id_api_lookup")


@patch("urllib.request.urlopen")
def test_resolve_topic_id_not_found(mock_urlopen: MagicMock):
  mock_urlopen.return_value = _mock_response({"topics": []})
  synced: dict[str, int] = {}
  client = DiscourseClient(TEST_CONFIG)

  result = _resolve_topic_id("nonexistent.md", synced, client)
  assert result is None
  print("  PASS: resolve_topic_id_not_found")


# ---------------------------------------------------------------------------
# _walk_nav_for_sidebar
# ---------------------------------------------------------------------------


def test_walk_nav_simple():
  items = [
    "getting-started/index.md",
    {"What is sunnypilot?": "getting-started/what-is-sunnypilot.md"},
    {"Use sunnypilot": "getting-started/use-sunnypilot-in-a-car.md"},
  ]
  synced = {
    "getting-started/what-is-sunnypilot.md": 252,
    "getting-started/use-sunnypilot-in-a-car.md": 251,
  }
  client = DiscourseClient(TEST_CONFIG)
  lines: list[str] = []

  _walk_nav_for_sidebar(
    items, "https://community.sunnypilot.ai",
    synced, client, lines,
  )

  assert len(lines) == 2
  assert "* What is sunnypilot?: https://community.sunnypilot.ai/t/252" in lines[0]
  assert "* Use sunnypilot: https://community.sunnypilot.ai/t/251" in lines[1]
  print("  PASS: walk_nav_simple")


def test_walk_nav_nested_sections():
  items = [
    "features/index.md",
    {"Cruise Control": [
      "features/cruise/index.md",
      {"ICBM": "features/cruise/icbm.md"},
      {"SCC-V": "features/cruise/scc-v.md"},
    ]},
    {"Steering": [
      "features/steering/index.md",
      {"MADS": "features/steering/mads.md"},
    ]},
  ]
  synced = {
    "features/cruise/icbm.md": 244,
    "features/cruise/scc-v.md": 248,
    "features/steering/mads.md": 245,
  }
  client = DiscourseClient(TEST_CONFIG)
  lines: list[str] = []

  _walk_nav_for_sidebar(
    items, "https://community.sunnypilot.ai",
    synced, client, lines,
  )

  assert "## Cruise Control" in lines
  assert "* ICBM: https://community.sunnypilot.ai/t/244" in lines
  assert "* SCC-V: https://community.sunnypilot.ai/t/248" in lines
  assert "## Steering" in lines
  assert "* MADS: https://community.sunnypilot.ai/t/245" in lines
  print("  PASS: walk_nav_nested_sections")


def test_walk_nav_skips_external_links():
  items = [
    {"Forum": "https://community.sunnypilot.ai"},
    {"Doc": "community/contributing.md"},
  ]
  synced = {"community/contributing.md": 236}
  client = DiscourseClient(TEST_CONFIG)
  lines: list[str] = []

  _walk_nav_for_sidebar(
    items, "https://community.sunnypilot.ai",
    synced, client, lines,
  )

  assert len(lines) == 1
  assert "Forum" not in lines[0]
  assert "Doc" in lines[0]
  assert "/t/236" in lines[0]
  print("  PASS: walk_nav_skips_external_links")


def test_walk_nav_skips_missing_topic_ids():
  items = [
    {"Known": "features/cruise/icbm.md"},
    {"Unknown": "features/cruise/nonexistent.md"},
  ]
  synced = {"features/cruise/icbm.md": 244}
  client = DiscourseClient(TEST_CONFIG)
  lines: list[str] = []

  _walk_nav_for_sidebar(
    items, "https://community.sunnypilot.ai",
    synced, client, lines,
  )

  assert len(lines) == 1
  assert "ICBM" in lines[0] or "Known" in lines[0]
  print("  PASS: walk_nav_skips_missing_topic_ids")


# ---------------------------------------------------------------------------
# Integration: sync_docs with mocked API
# ---------------------------------------------------------------------------


def _mock_response(data: dict) -> MagicMock:
  """Create a mock urllib response with JSON body."""
  body = json.dumps(data).encode("utf-8")
  resp = MagicMock()
  resp.read.return_value = body
  resp.__enter__ = lambda s: s
  resp.__exit__ = MagicMock(return_value=False)
  return resp


def test_sync_docs_dry_run():
  """Integration test: dry run makes read-only lookups but no mutations."""
  with tempfile.TemporaryDirectory() as tmpdir:
    # Create minimal docs structure
    docs_dir = Path(tmpdir) / "docs"
    docs_dir.mkdir()
    gs_dir = docs_dir / "getting-started"
    gs_dir.mkdir()

    # Create a test doc
    (gs_dir / "test-doc.md").write_text(
      "---\ntitle: Test Doc\n---\n\n# Test Doc\n\nContent.\n"
    )

    # Create minimal zensical.toml
    toml_path = Path(tmpdir) / "zensical.toml"
    toml_path.write_text(textwrap.dedent("""\
      [project]
      docs_dir = "docs"
      nav = [
        { "Getting Started" = [
        { "Test Doc" = "getting-started/test-doc.md" },
        ]},
      ]
    """))

    env = {
      "DISCOURSE_URL": "https://community.sunnypilot.ai",
      "DISCOURSE_API_KEY": "test-key",
      "DISCOURSE_CATEGORY_MAP": '{"getting-started": 133}',
    }

    args = argparse.Namespace(dry_run=True, verbose=True, force=True)

    with (
      patch.dict("os.environ", env, clear=False),
      patch("sync_to_discourse.DOCS_DIR", docs_dir),
      patch("sync_to_discourse.ZENSICAL_TOML", toml_path),
      patch("urllib.request.urlopen") as mock_urlopen,
    ):
      # Return "no topics found" for read-only lookups
      mock_urlopen.return_value = _mock_response({"topics": []})

      sync_docs(args)

      # Dry run should only make GET (search) calls, never POST/PUT
      for c in mock_urlopen.call_args_list:
        req = c[0][0]
        assert req.method == "GET", (
          f"Dry run must not mutate: {req.method} {req.full_url}"
        )

  print("  PASS: sync_docs_dry_run")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
  print("Testing sync orchestrator:")
  tests = [
    # extract_title
    test_extract_title_from_front_matter,
    test_extract_title_from_heading,
    test_extract_title_fallback,
    test_extract_title_quoted,
    # build_footer
    test_build_footer_contains_sync_id,
    test_build_footer_contains_github_link,
    test_build_footer_starts_with_separator,
    # _get_section_folder
    test_get_section_folder_from_index,
    test_get_section_folder_from_dict,
    test_get_section_folder_nested,
    test_get_section_folder_external_link,
    test_get_section_folder_empty,
    # _resolve_topic_id
    test_resolve_topic_id_cached,
    test_resolve_topic_id_api_lookup,
    test_resolve_topic_id_not_found,
    # _walk_nav_for_sidebar
    test_walk_nav_simple,
    test_walk_nav_nested_sections,
    test_walk_nav_skips_external_links,
    test_walk_nav_skips_missing_topic_ids,
    # Integration
    test_sync_docs_dry_run,
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
