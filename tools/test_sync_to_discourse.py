#!/usr/bin/env python3
"""Tests for the sync orchestrator (fully mocked, no live requests).

Run: python3 tools/test_sync_to_discourse.py
"""

import argparse
import json
import sys
import tempfile
import textwrap
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent))

from sync_to_discourse import (
  _body_matches_discourse,
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
# _body_matches_discourse
# ---------------------------------------------------------------------------


def test_body_matches_discourse_identical():
  body = "# Title\n\nContent here.\n"
  assert _body_matches_discourse(body, body) is True
  print("  PASS: body_matches_discourse_identical")


def test_body_matches_discourse_trailing_whitespace():
  local = "# Title\n\nContent here.\n"
  remote = "# Title  \n\nContent here.  \n"
  assert _body_matches_discourse(local, remote) is True
  print("  PASS: body_matches_discourse_trailing_whitespace")


def test_body_matches_discourse_different_content():
  local = "# Title\n\nNew content.\n"
  remote = "# Title\n\nOld content.\n"
  assert _body_matches_discourse(local, remote) is False
  print("  PASS: body_matches_discourse_different_content")


def test_body_matches_discourse_none_remote():
  assert _body_matches_discourse("some content", None) is False
  print("  PASS: body_matches_discourse_none_remote")


def test_body_matches_discourse_empty_strings():
  assert _body_matches_discourse("", "") is True
  print("  PASS: body_matches_discourse_empty_strings")


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


def test_sync_docs_skips_when_discourse_matches():
  """Integration test: no update is pushed when Discourse already has the same content."""
  with tempfile.TemporaryDirectory() as tmpdir:
    docs_dir = Path(tmpdir) / "docs"
    docs_dir.mkdir()
    gs_dir = docs_dir / "getting-started"
    gs_dir.mkdir()

    doc_content = "---\ntitle: Test Doc\n---\n\n# Test Doc\n\nContent.\n"
    (gs_dir / "test-doc.md").write_text(doc_content)

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

    # Pass 1 lookup response: topic exists with id 200
    pass1_response = _mock_response({"topics": [{"id": 200, "title": "Test Doc"}]})
    # first_post_id response
    first_post_response = _mock_response({
      "post_stream": {"posts": [{"id": 500, "post_number": 1}]},
    })

    def make_side_effect(local_body: str) -> MagicMock:
      """get_post_raw returns content matching what we'd send."""
      return _mock_response({"id": 500, "raw": local_body})

    args = argparse.Namespace(dry_run=False, verbose=True, force=False)

    call_responses: list[MagicMock] = []

    with (
      patch.dict("os.environ", env, clear=False),
      patch("sync_to_discourse.DOCS_DIR", docs_dir),
      patch("sync_to_discourse.ZENSICAL_TOML", toml_path),
      patch("sync_to_discourse.time") as mock_time,
      patch("urllib.request.urlopen") as mock_urlopen,
    ):
      mock_time.sleep = MagicMock()

      # Capture calls so we can inject matching content after first_post_id fires
      def side_effect(req: object) -> MagicMock:
        url = req.full_url  # type: ignore[attr-defined]
        method = req.method  # type: ignore[attr-defined]
        call_responses.append((method, url))

        if "/search.json" in url:
          return pass1_response
        if "/t/200.json" in url:
          return first_post_response
        if "/posts/500.json" in url and method == "GET":
          # Return a raw that will match whatever body we compute
          # (we inject a placeholder; the real check happens below)
          return _mock_response({"id": 500, "raw": "__MATCH__"})
        # Any POST/PUT would be a failure — should not be reached
        return _mock_response({})

      mock_urlopen.side_effect = side_effect

      # Patch _body_matches_discourse to return True (simulates match)
      with patch("sync_to_discourse._body_matches_discourse", return_value=True):
        sync_docs(args)

      # Verify no PUT mutations were made
      put_calls = [(m, u) for m, u in call_responses if m == "PUT"]
      assert put_calls == [], f"Expected no PUT calls, got: {put_calls}"

  print("  PASS: sync_docs_skips_when_discourse_matches")


# ---------------------------------------------------------------------------
# --only filter + idempotency guarantees
# ---------------------------------------------------------------------------


def _build_two_doc_workspace(tmpdir: str) -> tuple[Path, Path]:
  """Create a docs tree with two docs under getting-started.

  Returns ``(docs_dir, toml_path)``.
  """
  docs_dir = Path(tmpdir) / "docs"
  docs_dir.mkdir()
  gs_dir = docs_dir / "getting-started"
  gs_dir.mkdir()

  (gs_dir / "doc-a.md").write_text(
    "---\ntitle: Doc A\n---\n\n# Doc A\n\nAlpha content.\n"
  )
  (gs_dir / "doc-b.md").write_text(
    "---\ntitle: Doc B\n---\n\n# Doc B\n\nBravo content.\n"
  )

  toml_path = Path(tmpdir) / "zensical.toml"
  toml_path.write_text(textwrap.dedent("""\
    [project]
    docs_dir = "docs"
    nav = [
      { "Getting Started" = [
      { "Doc A" = "getting-started/doc-a.md" },
      { "Doc B" = "getting-started/doc-b.md" },
      ]},
    ]
  """))
  return docs_dir, toml_path


def _patch_cache_dir(tmpdir: str) -> patch:
  """Redirect the content cache to an isolated per-test directory."""
  cache_dir = Path(tmpdir) / ".cache"
  return patch("sync_to_discourse.ContentCache", lambda: _ephemeral_cache(cache_dir))


def _ephemeral_cache(cache_dir: Path):
  from content_cache import ContentCache
  return ContentCache(cache_dir=cache_dir)


def test_sync_docs_only_filter_restricts_pass2():
  """--only restricts Pass 2 to listed paths; others are not processed."""
  with tempfile.TemporaryDirectory() as tmpdir:
    docs_dir, toml_path = _build_two_doc_workspace(tmpdir)

    env = {
      "DISCOURSE_URL": "https://community.sunnypilot.ai",
      "DISCOURSE_API_KEY": "test-key",
      "DISCOURSE_CATEGORY_MAP": '{"getting-started": 133}',
    }
    args = argparse.Namespace(
      dry_run=True, verbose=True, force=True,
      only=["getting-started/doc-a.md"],
    )

    with (
      patch.dict("os.environ", env, clear=False),
      patch("sync_to_discourse.DOCS_DIR", docs_dir),
      patch("sync_to_discourse.ZENSICAL_TOML", toml_path),
      _patch_cache_dir(tmpdir),
      patch("urllib.request.urlopen") as mock_urlopen,
    ):
      mock_urlopen.return_value = _mock_response({"topics": []})

      # Capture printed output to verify only doc-a is mentioned in Pass 2
      import io
      import contextlib
      buf = io.StringIO()
      with contextlib.redirect_stdout(buf):
        sync_docs(args)
      output = buf.getvalue()

    assert "doc-a.md" in output, "Filtered doc must appear in dry-run output"
    # doc-b.md must not appear in Pass 2 processing lines
    pass2_section = output.split("Pass 2: Syncing content...", 1)[1]
    pass2_end = pass2_section.split("Sync Summary", 1)[0]
    assert "doc-b.md" not in pass2_end, (
      f"Excluded doc must not be processed in Pass 2. Found in:\n{pass2_end}"
    )
    assert "Skipping sidebar generation" in output, (
      "Filtered runs must skip sidebar generation"
    )

  print("  PASS: sync_docs_only_filter_restricts_pass2")


def test_sync_docs_only_filter_warns_on_unknown_path():
  """--only paths not in zensical.toml produce a WARN, not an error."""
  with tempfile.TemporaryDirectory() as tmpdir:
    docs_dir, toml_path = _build_two_doc_workspace(tmpdir)

    env = {
      "DISCOURSE_URL": "https://community.sunnypilot.ai",
      "DISCOURSE_API_KEY": "test-key",
      "DISCOURSE_CATEGORY_MAP": '{"getting-started": 133}',
    }
    args = argparse.Namespace(
      dry_run=True, verbose=True, force=True,
      only=["getting-started/doc-a.md", "getting-started/ghost.md"],
    )

    with (
      patch.dict("os.environ", env, clear=False),
      patch("sync_to_discourse.DOCS_DIR", docs_dir),
      patch("sync_to_discourse.ZENSICAL_TOML", toml_path),
      _patch_cache_dir(tmpdir),
      patch("urllib.request.urlopen") as mock_urlopen,
    ):
      mock_urlopen.return_value = _mock_response({"topics": []})

      import io
      import contextlib
      buf = io.StringIO()
      with contextlib.redirect_stdout(buf):
        sync_docs(args)
      output = buf.getvalue()

    assert "WARN: --only paths not present" in output
    assert "getting-started/ghost.md" in output
    assert "doc-a.md" in output

  print("  PASS: sync_docs_only_filter_warns_on_unknown_path")


def test_sync_docs_dry_run_counts_match_as_skip_not_update():
  """Dry-run must fetch remote and classify matching content as skipped."""
  with tempfile.TemporaryDirectory() as tmpdir:
    docs_dir, toml_path = _build_two_doc_workspace(tmpdir)

    env = {
      "DISCOURSE_URL": "https://community.sunnypilot.ai",
      "DISCOURSE_API_KEY": "test-key",
      "DISCOURSE_CATEGORY_MAP": '{"getting-started": 133}',
    }
    # Force=True bypasses content cache so remote check becomes authoritative.
    args = argparse.Namespace(
      dry_run=True, verbose=True, force=True,
      only=["getting-started/doc-a.md"],
    )

    def side_effect(req):
      url = req.full_url
      method = req.method
      if method == "GET" and "/search.json" in url:
        # Resolve via sync-id
        return _mock_response({"topics": [{"id": 500, "title": "Doc A"}]})
      if method == "GET" and url.endswith("/t/500.json"):
        return _mock_response({
          "id": 500,
          "title": "Doc A",
          "category_id": 133,
          "post_stream": {"posts": [{"id": 900, "post_number": 1}]},
        })
      if method == "GET" and url.endswith("/posts/900.json"):
        # Return what _post_body_matches_remote will compare against.
        # Patching _body_matches_discourse below makes this trivial.
        return _mock_response({"id": 900, "raw": "whatever"})
      return _mock_response({})

    with (
      patch.dict("os.environ", env, clear=False),
      patch("sync_to_discourse.DOCS_DIR", docs_dir),
      patch("sync_to_discourse.ZENSICAL_TOML", toml_path),
      _patch_cache_dir(tmpdir),
      patch("sync_to_discourse.time") as mock_time,
      patch("urllib.request.urlopen") as mock_urlopen,
      patch("sync_to_discourse._body_matches_discourse", return_value=True),
    ):
      mock_time.sleep = MagicMock()
      mock_urlopen.side_effect = side_effect

      import io
      import contextlib
      buf = io.StringIO()
      with contextlib.redirect_stdout(buf):
        sync_docs(args)
      output = buf.getvalue()

    # Should skip, not "Would update"
    assert "Would update" not in output, (
      f"Dry-run must not count matching remote as update:\n{output}"
    )
    assert "SKIP (discourse up-to-date)" in output, (
      f"Must log skip for matching remote:\n{output}"
    )
    # Summary line must show 1 skipped discourse match
    assert "Skipped (Discourse Match): 1" in output
    assert "Updated (Normal):      0" in output

  print("  PASS: sync_docs_dry_run_counts_match_as_skip_not_update")


def test_sidebar_skips_update_when_remote_matches():
  """_generate_sidebars must fetch remote and skip unchanged sidebars."""
  from sync_to_discourse import _generate_sidebars

  with tempfile.TemporaryDirectory() as tmpdir:
    docs_dir, toml_path = _build_two_doc_workspace(tmpdir)
    # Add an index so there's something to render
    (docs_dir / "getting-started" / "index.md").write_text(
      "# Getting Started\n\nIntro text.\n"
    )

    env = {
      "DISCOURSE_URL": "https://community.sunnypilot.ai",
      "DISCOURSE_API_KEY": "test-key",
      "DISCOURSE_CATEGORY_MAP": '{"getting-started": 133}',
    }
    config = DiscourseConfig(
      base_url=env["DISCOURSE_URL"],
      api_key=env["DISCOURSE_API_KEY"],
      category_mapping={"getting-started": 133},
    )
    client = DiscourseClient(config)
    stats = {
      "sidebars_updated": 0,
      "skipped_sidebar_match": 0,
    }
    synced_topics = {
      "getting-started/doc-a.md": 501,
      "getting-started/doc-b.md": 502,
    }

    def side_effect(req):
      url = req.full_url
      method = req.method
      if method == "GET" and "/c/133/show.json" in url:
        return _mock_response({
          "category": {"topic_url": "/t/about-getting-started/700"},
        })
      if method == "GET" and url.endswith("/t/700.json"):
        return _mock_response({
          "post_stream": {"posts": [{"id": 800, "post_number": 1}]},
        })
      if method == "GET" and url.endswith("/posts/800.json"):
        return _mock_response({"id": 800, "raw": "matches"})
      # Any PUT/POST would indicate an unwanted update
      raise AssertionError(f"Unexpected {method} to {url}")

    with (
      patch.dict("os.environ", env, clear=False),
      patch("sync_to_discourse.ZENSICAL_TOML", toml_path),
      patch("sync_to_discourse.time") as mock_time,
      patch("urllib.request.urlopen") as mock_urlopen,
      patch("sync_to_discourse._body_matches_discourse", return_value=True),
    ):
      mock_time.sleep = MagicMock()
      mock_urlopen.side_effect = side_effect

      _generate_sidebars(
        config=config,
        client=client,
        synced_topics=synced_topics,
        index_contents={"getting-started/index.md": "Intro.\n"},
        dry_run=False,
        verbose=True,
        stats=stats,
      )

    assert stats["skipped_sidebar_match"] == 1, (
      f"Matching sidebar must be skipped, got stats={stats}"
    )
    assert stats["sidebars_updated"] == 0, (
      f"No sidebars should have updated, got stats={stats}"
    )

  print("  PASS: sidebar_skips_update_when_remote_matches")


def test_update_topic_skipped_when_metadata_matches():
  """update_topic PUT must be suppressed when title + category already match."""
  with tempfile.TemporaryDirectory() as tmpdir:
    docs_dir, toml_path = _build_two_doc_workspace(tmpdir)

    env = {
      "DISCOURSE_URL": "https://community.sunnypilot.ai",
      "DISCOURSE_API_KEY": "test-key",
      "DISCOURSE_CATEGORY_MAP": '{"getting-started": 133}',
    }
    args = argparse.Namespace(
      dry_run=False, verbose=True, force=True,
      only=["getting-started/doc-a.md"],
    )

    calls: list[tuple[str, str, bytes | None]] = []

    def side_effect(req):
      url = req.full_url
      method = req.method
      data = req.data
      calls.append((method, url, data))

      if method == "GET" and "/search.json" in url:
        return _mock_response({"topics": [{"id": 500, "title": "Doc A"}]})
      if method == "GET" and url.endswith("/t/500.json"):
        # Metadata check + first_post_id both hit this endpoint;
        # return matching metadata + post stream
        return _mock_response({
          "id": 500,
          "title": "Doc A",
          "category_id": 133,
          "post_stream": {"posts": [{"id": 900, "post_number": 1}]},
        })
      if method == "GET" and url.endswith("/posts/900.json"):
        return _mock_response({"id": 900, "raw": "body-differs"})
      if method == "PUT" and url.endswith("/posts/900.json"):
        return _mock_response({"post": {"id": 900}})
      return _mock_response({})

    with (
      patch.dict("os.environ", env, clear=False),
      patch("sync_to_discourse.DOCS_DIR", docs_dir),
      patch("sync_to_discourse.ZENSICAL_TOML", toml_path),
      _patch_cache_dir(tmpdir),
      patch("sync_to_discourse.time") as mock_time,
      patch("urllib.request.urlopen") as mock_urlopen,
    ):
      mock_time.sleep = MagicMock()
      mock_urlopen.side_effect = side_effect
      # Force body mismatch so update_post fires; metadata check then runs
      with patch(
        "sync_to_discourse._body_matches_discourse", return_value=False,
      ):
        sync_docs(args)

    # Must PUT the post (body changed), but MUST NOT PUT the topic
    put_topic_calls = [
      (m, u) for m, u, _ in calls
      if m == "PUT" and "/t/-/" in u
    ]
    put_post_calls = [
      (m, u) for m, u, _ in calls
      if m == "PUT" and "/posts/" in u
    ]
    assert put_post_calls, f"Post should be updated when body differs: {calls}"
    assert not put_topic_calls, (
      f"Topic metadata matches — no update_topic PUT expected. Got: {put_topic_calls}"
    )

  print("  PASS: update_topic_skipped_when_metadata_matches")


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
    # _body_matches_discourse
    test_body_matches_discourse_identical,
    test_body_matches_discourse_trailing_whitespace,
    test_body_matches_discourse_different_content,
    test_body_matches_discourse_none_remote,
    test_body_matches_discourse_empty_strings,
    # Integration
    test_sync_docs_dry_run,
    test_sync_docs_skips_when_discourse_matches,
    # --only filter + idempotency
    test_sync_docs_only_filter_restricts_pass2,
    test_sync_docs_only_filter_warns_on_unknown_path,
    test_sync_docs_dry_run_counts_match_as_skip_not_update,
    test_sidebar_skips_update_when_remote_matches,
    test_update_topic_skipped_when_metadata_matches,
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
