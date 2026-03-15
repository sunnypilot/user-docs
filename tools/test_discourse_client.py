#!/usr/bin/env python3
"""Tests for the Discourse API client (fully mocked, no live requests).

Run: uv run python tools/test_discourse_client.py
"""

import io
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent))

from discourse_client import DiscourseClient, DiscourseConfig

TEST_CONFIG = DiscourseConfig(
  base_url="https://community.sunnypilot.ai",
  api_key="test-api-key-123",
  api_user="docs-bot",
  category_mapping={
    "getting-started": 115,
    "features": 116,
    "features/cruise": 140,
    "features/steering": 141,
  },
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def mock_response(data: dict, status: int = 200) -> MagicMock:
  """Create a mock urllib response with JSON body."""
  body = json.dumps(data).encode("utf-8")
  resp = MagicMock()
  resp.read.return_value = body
  resp.status = status
  resp.__enter__ = lambda s: s
  resp.__exit__ = MagicMock(return_value=False)
  return resp


def mock_http_error(status: int, body: str = "") -> urllib.error.HTTPError:
  """Create a mock HTTPError."""
  return urllib.error.HTTPError(
    url="https://community.sunnypilot.ai/test",
    code=status,
    msg=f"HTTP {status}",
    hdrs={},  # type: ignore[arg-type]
    fp=io.BytesIO(body.encode("utf-8")),
  )


# ---------------------------------------------------------------------------
# DiscourseConfig tests
# ---------------------------------------------------------------------------


def test_config_from_env():
  env = {
    "DISCOURSE_URL": "https://forum.example.com/",
    "DISCOURSE_API_KEY": "secret-key",
    "DISCOURSE_API_USER": "bot",
    "DISCOURSE_CATEGORY_MAP": '{"getting-started": 115, "features": 116}',
  }
  with patch.dict("os.environ", env, clear=False):
    config = DiscourseConfig.from_env()

  assert config.base_url == "https://forum.example.com"  # trailing slash stripped
  assert config.api_key == "secret-key"
  assert config.api_user == "bot"
  assert config.category_mapping == {"getting-started": 115, "features": 116}
  print("  PASS: config_from_env")


def test_config_from_env_defaults():
  env = {
    "DISCOURSE_URL": "https://forum.example.com",
    "DISCOURSE_API_KEY": "key",
  }
  with patch.dict("os.environ", env, clear=True):
    config = DiscourseConfig.from_env()

  assert config.api_user == "system"
  assert config.category_mapping == {}
  print("  PASS: config_from_env_defaults")


def test_config_invalid_category_map_json():
  env = {
    "DISCOURSE_URL": "https://forum.example.com",
    "DISCOURSE_API_KEY": "key",
    "DISCOURSE_CATEGORY_MAP": "not-valid-json",
  }
  with patch.dict("os.environ", env, clear=True):
    try:
      DiscourseConfig.from_env()
      assert False, "Should have raised ValueError"
    except ValueError as e:
      assert "DISCOURSE_CATEGORY_MAP" in str(e)
  print("  PASS: config_invalid_category_map_json")


def test_config_invalid_category_map_type():
  env = {
    "DISCOURSE_URL": "https://forum.example.com",
    "DISCOURSE_API_KEY": "key",
    "DISCOURSE_CATEGORY_MAP": "[1, 2, 3]",
  }
  with patch.dict("os.environ", env, clear=True):
    try:
      DiscourseConfig.from_env()
      assert False, "Should have raised ValueError"
    except ValueError as e:
      assert "DISCOURSE_CATEGORY_MAP" in str(e)
  print("  PASS: config_invalid_category_map_type")


def test_category_id_for_mapped():
  assert TEST_CONFIG.category_id_for("getting-started/what-is-sunnypilot.md") == 115
  assert TEST_CONFIG.category_id_for("features/icbm.md") == 116
  # Sub-category: most specific prefix wins
  assert TEST_CONFIG.category_id_for("features/cruise/icbm.md") == 140
  assert TEST_CONFIG.category_id_for("features/steering/mads.md") == 141
  # Falls back to parent when no sub-category match
  assert TEST_CONFIG.category_id_for("features/models.md") == 116
  print("  PASS: category_id_for_mapped")


def test_category_id_for_unmapped():
  assert TEST_CONFIG.category_id_for("unknown-section/doc.md") == 114
  print("  PASS: category_id_for_unmapped")


def test_has_category_for_mapped():
  assert TEST_CONFIG.has_category_for("getting-started/what-is-sunnypilot.md") is True
  assert TEST_CONFIG.has_category_for("features/cruise/icbm.md") is True
  print("  PASS: has_category_for_mapped")


def test_has_category_for_unmapped():
  assert TEST_CONFIG.has_category_for("unknown-section/doc.md") is False
  assert TEST_CONFIG.has_category_for("safety/prohibited.md") is False
  print("  PASS: has_category_for_unmapped")


def test_config_missing_url():
  env = {"DISCOURSE_API_KEY": "key"}
  with patch.dict("os.environ", env, clear=True):
    try:
      DiscourseConfig.from_env()
      assert False, "Should have raised ValueError"
    except ValueError as e:
      assert "DISCOURSE_URL" in str(e)
  print("  PASS: config_missing_url")


def test_config_missing_api_key():
  env = {"DISCOURSE_URL": "https://forum.example.com"}
  with patch.dict("os.environ", env, clear=True):
    try:
      DiscourseConfig.from_env()
      assert False, "Should have raised ValueError"
    except ValueError as e:
      assert "DISCOURSE_API_KEY" in str(e)
  print("  PASS: config_missing_api_key")


def test_config_topic_map():
  env = {
    "DISCOURSE_URL": "https://forum.example.com",
    "DISCOURSE_API_KEY": "key",
    "DISCOURSE_TOPIC_MAP": '{"getting-started/what-is-sunnypilot.md": 2452}',
  }
  with patch.dict("os.environ", env, clear=True):
    config = DiscourseConfig.from_env()

  assert config.topic_mapping == {"getting-started/what-is-sunnypilot.md": 2452}
  print("  PASS: config_topic_map")


def test_config_topic_map_default_empty():
  env = {
    "DISCOURSE_URL": "https://forum.example.com",
    "DISCOURSE_API_KEY": "key",
  }
  with patch.dict("os.environ", env, clear=True):
    config = DiscourseConfig.from_env()

  assert config.topic_mapping == {}
  print("  PASS: config_topic_map_default_empty")


def test_config_immutable():
  try:
    TEST_CONFIG.base_url = "https://other.com"  # type: ignore[misc]
    assert False, "Should have raised"
  except AttributeError:
    pass
  print("  PASS: config_immutable")


# ---------------------------------------------------------------------------
# find_topic_by_sync_id
# ---------------------------------------------------------------------------


@patch("urllib.request.urlopen")
def test_find_topic_found(mock_urlopen: MagicMock):
  mock_urlopen.return_value = mock_response({
    "topics": [{"id": 101, "title": "ICBM Docs"}],
  })
  client = DiscourseClient(TEST_CONFIG)

  result = client.find_topic_by_sync_id("features/cruise/icbm.md")

  assert result is not None
  assert result["id"] == 101
  call_args = mock_urlopen.call_args[0][0]
  assert "/search.json?" in call_args.full_url
  assert "docs-sync-id" in call_args.full_url
  print("  PASS: find_topic_found")


@patch("urllib.request.urlopen")
def test_find_topic_not_found(mock_urlopen: MagicMock):
  mock_urlopen.return_value = mock_response({"topics": []})
  client = DiscourseClient(TEST_CONFIG)

  result = client.find_topic_by_sync_id("nonexistent.md")
  assert result is None
  print("  PASS: find_topic_not_found")


@patch("urllib.request.urlopen")
def test_find_topic_api_error(mock_urlopen: MagicMock):
  mock_urlopen.side_effect = mock_http_error(500, "Internal Server Error")
  client = DiscourseClient(TEST_CONFIG)

  result = client.find_topic_by_sync_id("features/icbm.md")
  assert result is None
  print("  PASS: find_topic_api_error")


# ---------------------------------------------------------------------------
# find_topic_by_title
# ---------------------------------------------------------------------------


@patch("urllib.request.urlopen")
def test_find_topic_by_title_exact_match(mock_urlopen: MagicMock):
  mock_urlopen.return_value = mock_response({
    "topics": [
      {"id": 300, "title": "Other Topic"},
      {"id": 244, "title": "ICBM - sunnypilot Docs"},
    ],
  })
  client = DiscourseClient(TEST_CONFIG)

  result = client.find_topic_by_title("ICBM - sunnypilot Docs")

  assert result is not None
  assert result["id"] == 244
  call_args = mock_urlopen.call_args[0][0]
  assert "/search.json?" in call_args.full_url
  decoded_url = urllib.parse.unquote_plus(call_args.full_url)
  assert "ICBM - sunnypilot Docs" in decoded_url
  assert "tag:docs-auto-sync" in decoded_url
  print("  PASS: find_topic_by_title_exact_match")


@patch("urllib.request.urlopen")
def test_find_topic_by_title_no_exact_match_returns_none(mock_urlopen: MagicMock):
  mock_urlopen.return_value = mock_response({
    "topics": [{"id": 244, "title": "ICBM Docs (close match)"}],
  })
  client = DiscourseClient(TEST_CONFIG)

  result = client.find_topic_by_title("ICBM - sunnypilot Docs")

  assert result is None  # No exact match -> None (prevents false positives)
  print("  PASS: find_topic_by_title_no_exact_match_returns_none")


@patch("urllib.request.urlopen")
def test_find_topic_by_title_not_found(mock_urlopen: MagicMock):
  mock_urlopen.return_value = mock_response({"topics": []})
  client = DiscourseClient(TEST_CONFIG)

  result = client.find_topic_by_title("Nonexistent Topic")
  assert result is None
  print("  PASS: find_topic_by_title_not_found")


# ---------------------------------------------------------------------------
# create_topic
# ---------------------------------------------------------------------------


@patch("urllib.request.urlopen")
def test_create_topic_success(mock_urlopen: MagicMock):
  mock_urlopen.return_value = mock_response({
    "id": 501,
    "topic_id": 201,
    "topic_slug": "icbm-sunnypilot-docs",
  })
  client = DiscourseClient(TEST_CONFIG)

  result = client.create_topic(
    title="ICBM - sunnypilot Docs",
    raw="# ICBM\n\nDoc content here.",
    category_id=42,
    tags=["docs", "auto-sync"],
  )

  assert result is not None
  assert result["topic_id"] == 201

  call_args = mock_urlopen.call_args[0][0]
  assert call_args.method == "POST"
  assert "/posts.json" in call_args.full_url

  sent_payload = json.loads(call_args.data.decode("utf-8"))
  assert sent_payload["title"] == "ICBM - sunnypilot Docs"
  assert sent_payload["category"] == 42
  assert sent_payload["tags"] == ["docs", "auto-sync"]
  assert "ICBM" in sent_payload["raw"]
  print("  PASS: create_topic_success")


@patch("urllib.request.urlopen")
def test_create_topic_no_tags(mock_urlopen: MagicMock):
  mock_urlopen.return_value = mock_response({"id": 502, "topic_id": 202})
  client = DiscourseClient(TEST_CONFIG)

  client.create_topic(title="Test", raw="body", category_id=1)

  sent_payload = json.loads(mock_urlopen.call_args[0][0].data.decode("utf-8"))
  assert "tags" not in sent_payload
  print("  PASS: create_topic_no_tags")


@patch("urllib.request.urlopen")
def test_create_topic_failure(mock_urlopen: MagicMock):
  mock_urlopen.side_effect = mock_http_error(422, '{"errors":["Title too short"]}')
  client = DiscourseClient(TEST_CONFIG)

  result = client.create_topic(title="X", raw="body", category_id=1)
  assert result is None
  print("  PASS: create_topic_failure")


# ---------------------------------------------------------------------------
# update_post
# ---------------------------------------------------------------------------


@patch("urllib.request.urlopen")
def test_update_post_success(mock_urlopen: MagicMock):
  mock_urlopen.return_value = mock_response({"post": {"id": 501, "version": 2}})
  client = DiscourseClient(TEST_CONFIG)

  result = client.update_post(post_id=501, raw="Updated content")

  assert result is not None
  call_args = mock_urlopen.call_args[0][0]
  assert call_args.method == "PUT"
  assert "/posts/501.json" in call_args.full_url

  sent_payload = json.loads(call_args.data.decode("utf-8"))
  assert sent_payload["post"]["raw"] == "Updated content"
  assert sent_payload["post"]["edit_reason"] == "Documentation sync"
  print("  PASS: update_post_success")


@patch("urllib.request.urlopen")
def test_update_post_custom_reason(mock_urlopen: MagicMock):
  mock_urlopen.return_value = mock_response({"post": {"id": 501}})
  client = DiscourseClient(TEST_CONFIG)

  client.update_post(post_id=501, raw="content", edit_reason="Manual fix")

  sent_payload = json.loads(mock_urlopen.call_args[0][0].data.decode("utf-8"))
  assert sent_payload["post"]["edit_reason"] == "Manual fix"
  print("  PASS: update_post_custom_reason")


@patch("urllib.request.urlopen")
def test_update_post_not_found(mock_urlopen: MagicMock):
  mock_urlopen.side_effect = mock_http_error(404)
  client = DiscourseClient(TEST_CONFIG)

  result = client.update_post(post_id=99999, raw="content")
  assert result is None
  print("  PASS: update_post_not_found")


# ---------------------------------------------------------------------------
# update_topic
# ---------------------------------------------------------------------------


@patch("urllib.request.urlopen")
def test_update_topic_success(mock_urlopen: MagicMock):
  mock_urlopen.return_value = mock_response({
    "basic_topic": {"id": 201, "title": "New Title", "category_id": 116},
  })
  client = DiscourseClient(TEST_CONFIG)

  result = client.update_topic(topic_id=201, title="New Title", category_id=116)

  assert result is not None
  call_args = mock_urlopen.call_args[0][0]
  assert call_args.method == "PUT"
  assert "/t/-/201.json" in call_args.full_url

  sent_payload = json.loads(call_args.data.decode("utf-8"))
  assert sent_payload["title"] == "New Title"
  assert sent_payload["category_id"] == 116
  print("  PASS: update_topic_success")


@patch("urllib.request.urlopen")
def test_update_topic_not_found(mock_urlopen: MagicMock):
  mock_urlopen.side_effect = mock_http_error(404)
  client = DiscourseClient(TEST_CONFIG)

  result = client.update_topic(topic_id=99999, title="Title", category_id=1)
  assert result is None
  print("  PASS: update_topic_not_found")


# ---------------------------------------------------------------------------
# first_post_id
# ---------------------------------------------------------------------------


@patch("urllib.request.urlopen")
def test_get_category_about_topic_id_success(mock_urlopen: MagicMock):
  mock_urlopen.return_value = mock_response({
    "category": {
      "id": 133,
      "name": "Getting Started",
      "topic_url": "/t/about-the-getting-started-category/500",
    },
  })
  client = DiscourseClient(TEST_CONFIG)

  result = client.get_category_about_topic_id(133)
  assert result == 500

  call_args = mock_urlopen.call_args[0][0]
  assert "/c/133/show.json" in call_args.full_url
  print("  PASS: get_category_about_topic_id_success")


@patch("urllib.request.urlopen")
def test_get_category_about_topic_id_not_found(mock_urlopen: MagicMock):
  mock_urlopen.side_effect = mock_http_error(404)
  client = DiscourseClient(TEST_CONFIG)

  result = client.get_category_about_topic_id(99999)
  assert result is None
  print("  PASS: get_category_about_topic_id_not_found")


@patch("urllib.request.urlopen")
def test_get_category_about_topic_id_no_topic_url(mock_urlopen: MagicMock):
  mock_urlopen.return_value = mock_response({
    "category": {"id": 133, "name": "Test"},
  })
  client = DiscourseClient(TEST_CONFIG)

  result = client.get_category_about_topic_id(133)
  assert result is None
  print("  PASS: get_category_about_topic_id_no_topic_url")


@patch("urllib.request.urlopen")
def test_first_post_id_found(mock_urlopen: MagicMock):
  mock_urlopen.return_value = mock_response({
    "post_stream": {
      "posts": [
        {"id": 501, "post_number": 1},
        {"id": 502, "post_number": 2},
      ],
    },
  })
  client = DiscourseClient(TEST_CONFIG)

  result = client.first_post_id(topic_id=201)
  assert result == 501
  print("  PASS: first_post_id_found")


@patch("urllib.request.urlopen")
def test_first_post_id_empty_stream(mock_urlopen: MagicMock):
  mock_urlopen.return_value = mock_response({"post_stream": {"posts": []}})
  client = DiscourseClient(TEST_CONFIG)

  result = client.first_post_id(topic_id=201)
  assert result is None
  print("  PASS: first_post_id_empty_stream")


@patch("urllib.request.urlopen")
def test_first_post_id_topic_not_found(mock_urlopen: MagicMock):
  mock_urlopen.side_effect = mock_http_error(404)
  client = DiscourseClient(TEST_CONFIG)

  result = client.first_post_id(topic_id=99999)
  assert result is None
  print("  PASS: first_post_id_topic_not_found")


# ---------------------------------------------------------------------------
# Headers / auth
# ---------------------------------------------------------------------------


@patch("urllib.request.urlopen")
def test_headers_set_correctly(mock_urlopen: MagicMock):
  mock_urlopen.return_value = mock_response({"topics": []})
  client = DiscourseClient(TEST_CONFIG)

  client.find_topic_by_sync_id("test.md")

  req = mock_urlopen.call_args[0][0]
  assert req.get_header("Api-key") == "test-api-key-123"
  assert req.get_header("Api-username") == "docs-bot"
  assert req.get_header("Content-type") == "application/json"
  assert "Mozilla" in req.get_header("User-agent")
  print("  PASS: headers_set_correctly")


# ---------------------------------------------------------------------------
# Connection error
# ---------------------------------------------------------------------------


@patch("urllib.request.urlopen")
def test_connection_error_returns_none(mock_urlopen: MagicMock):
  mock_urlopen.side_effect = urllib.error.URLError("Connection refused")
  client = DiscourseClient(TEST_CONFIG)

  result = client.find_topic_by_sync_id("test.md")
  assert result is None
  print("  PASS: connection_error_returns_none")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

import os  # noqa: E402 (needed for test_config_from_env_defaults)

if __name__ == "__main__":
  print("Testing Discourse API client:")
  tests = [
    # Config
    test_config_from_env,
    test_config_from_env_defaults,
    test_config_invalid_category_map_json,
    test_config_invalid_category_map_type,
    test_config_missing_url,
    test_config_missing_api_key,
    test_config_topic_map,
    test_config_topic_map_default_empty,
    test_config_immutable,
    test_category_id_for_mapped,
    test_category_id_for_unmapped,
    test_has_category_for_mapped,
    test_has_category_for_unmapped,
    # find_topic_by_sync_id
    test_find_topic_found,
    test_find_topic_not_found,
    test_find_topic_api_error,
    # find_topic_by_title
    test_find_topic_by_title_exact_match,
    test_find_topic_by_title_no_exact_match_returns_none,
    test_find_topic_by_title_not_found,
    # create_topic
    test_create_topic_success,
    test_create_topic_no_tags,
    test_create_topic_failure,
    # update_post
    test_update_post_success,
    test_update_post_custom_reason,
    test_update_post_not_found,
    # update_topic
    test_update_topic_success,
    test_update_topic_not_found,
    # get_category_about_topic_id
    test_get_category_about_topic_id_success,
    test_get_category_about_topic_id_not_found,
    test_get_category_about_topic_id_no_topic_url,
    # first_post_id
    test_first_post_id_found,
    test_first_post_id_empty_stream,
    test_first_post_id_topic_not_found,
    # Misc
    test_headers_set_correctly,
    test_connection_error_returns_none,
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
