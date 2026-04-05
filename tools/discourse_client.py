"""Minimal Discourse API client using only urllib (zero external deps).

Provides the operations needed by the docs sync orchestrator:
1. find_topic_by_sync_id(sync_id)
2. create_topic(title, raw, category_id, tags)
3. update_post(post_id, raw, edit_reason)
4. first_post_id(topic_id)
5. get_post_raw(post_id)

Configuration via environment variables:
  DISCOURSE_URL          - Base URL (e.g. https://community.sunnypilot.ai)
  DISCOURSE_API_KEY      - API key with topic create/update permissions
  DISCOURSE_API_USER     - Username for API requests (default: "system")
  DISCOURSE_CATEGORY_MAP - JSON mapping of doc section to Discourse category ID
               e.g. '{"getting-started": 115, "features": 116}'
               Falls back to parent category 114 for unmapped sections.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Any


DEFAULT_PARENT_CATEGORY_ID = 114

DEFAULT_CATEGORY_MAP: dict[str, int] = {}


@dataclass(frozen=True)
class DiscourseConfig:
  """Immutable configuration for the Discourse API client."""

  base_url: str
  api_key: str
  api_user: str = "system"
  category_mapping: dict[str, int] = field(default_factory=lambda: dict(DEFAULT_CATEGORY_MAP))
  topic_mapping: dict[str, int] = field(default_factory=dict)

  def category_id_for(self, doc_path: str) -> int:
    """Return the Discourse category ID for a given doc path.

    Uses longest-prefix matching: "features/cruise/icbm.md" matches
    "features/cruise" (sub-category) over "features" (parent).
    Falls back to the parent Documentation category (114).
    """
    return self._match_category(doc_path) or DEFAULT_PARENT_CATEGORY_ID

  def has_category_for(self, doc_path: str) -> bool:
    """Return True if the doc path matches any mapped category."""
    return self._match_category(doc_path) is not None

  def _match_category(self, doc_path: str) -> int | None:
    """Find the most specific category mapping for a doc path.

    Walks path segments from most specific to least specific:
      features/cruise/icbm.md -> features/cruise -> features
    Returns the first match, or None.
    """
    parts = doc_path.split("/")
    # Try progressively shorter prefixes (skip the filename itself)
    for i in range(len(parts) - 1, 0, -1):
      prefix = "/".join(parts[:i])
      if prefix in self.category_mapping:
        return self.category_mapping[prefix]
    return None

  @classmethod
  def from_env(cls) -> DiscourseConfig:
    """Build config from environment variables.

    Raises:
      ValueError: If required env vars are missing or map is invalid JSON.
    """
    base_url = os.environ.get("DISCOURSE_URL", "")
    api_key = os.environ.get("DISCOURSE_API_KEY", "")

    if not base_url:
      raise ValueError("DISCOURSE_URL environment variable is required")
    if not api_key:
      raise ValueError("DISCOURSE_API_KEY environment variable is required")

    category_map_str = os.environ.get("DISCOURSE_CATEGORY_MAP", "")
    if category_map_str:
      try:
        raw_map = json.loads(category_map_str)
      except json.JSONDecodeError as e:
        raise ValueError(f"DISCOURSE_CATEGORY_MAP must be valid JSON: {e}")
      if not isinstance(raw_map, dict):
        raise ValueError("DISCOURSE_CATEGORY_MAP must be a JSON object")
      category_mapping = {str(k): int(v) for k, v in raw_map.items()}
    else:
      category_mapping = dict(DEFAULT_CATEGORY_MAP)

    topic_map_str = os.environ.get("DISCOURSE_TOPIC_MAP", "")
    if topic_map_str:
      try:
        raw_topic_map = json.loads(topic_map_str)
      except json.JSONDecodeError as e:
        raise ValueError(f"DISCOURSE_TOPIC_MAP must be valid JSON: {e}")
      if not isinstance(raw_topic_map, dict):
        raise ValueError("DISCOURSE_TOPIC_MAP must be a JSON object")
      topic_mapping = {str(k): int(v) for k, v in raw_topic_map.items()}
    else:
      topic_mapping = {}

    return cls(
      base_url=base_url.rstrip("/"),
      api_key=api_key,
      api_user=os.environ.get("DISCOURSE_API_USER", "system"),
      category_mapping=category_mapping,
      topic_mapping=topic_mapping,
    )


class DiscourseClient:
  """Discourse API client for docs sync operations."""

  def __init__(self, config: DiscourseConfig) -> None:
    self._config = config

  @property
  def config(self) -> DiscourseConfig:
    return self._config

  # ----- Public API -----

  def find_topic_by_sync_id(self, sync_id: str) -> dict[str, Any] | None:
    """Find an existing topic by its embedded sync ID marker.

    Searches for topics containing the visible sync ID text
    ``docs-sync-id: {sync_id}``.  The marker must be visible (not an
    HTML comment) so that Discourse indexes it.

    Args:
      sync_id: The doc path used as sync identifier.

    Returns:
      Topic dict with at least 'id' key, or None if not found.
    """
    query = f'"docs-sync-id: {sync_id}"'
    encoded = urllib.parse.urlencode({"q": query})
    data = self._get(f"/search.json?{encoded}")
    if data is None:
      return None
    topics = data.get("topics", [])
    return topics[0] if topics else None

  def find_topic_by_title(self, title: str) -> dict[str, Any] | None:
    """Find an existing topic by its title (fallback for pre-sync-id topics).

    Searches for topics whose title matches exactly. Used as a fallback
    when find_topic_by_sync_id() returns no results (e.g. for topics
    migrated before the sync ID was introduced).

    Uses exact-phrase search (``"title"``) filtered by the
    ``docs-auto-sync`` tag to avoid matching unrelated community posts.
    The Discourse ``title:`` search operator is unreliable and may
    return empty results even when the topic exists.

    Args:
      title: The topic title to search for (exact match preferred).

    Returns:
      Topic dict with at least 'id' key, or None if not found.
    """
    encoded = urllib.parse.urlencode({
      "q": f'"{title}" tag:docs-auto-sync',
    })
    data = self._get(f"/search.json?{encoded}")
    if data is None:
      return None
    topics = data.get("topics", [])
    # Require exact title match to prevent overwriting unrelated topics
    for topic in topics:
      if topic.get("title", "").strip().lower() == title.strip().lower():
        return topic
    return None

  def create_topic(
    self,
    title: str,
    raw: str,
    category_id: int,
    tags: list[str] | None = None,
  ) -> dict[str, Any] | None:
    """Create a new topic in the specified category.

    Args:
      title: Topic title.
      raw: Markdown body content.
      category_id: Discourse category ID.
      tags: Optional list of tags.

    Returns:
      Response dict with 'topic_id', 'id' (post ID), etc., or None on failure.
    """
    payload: dict[str, Any] = {
      "title": title,
      "raw": raw,
      "category": category_id,
    }
    if tags:
      payload["tags"] = tags
    return self._post("/posts.json", payload)

  def update_post(
    self,
    post_id: int,
    raw: str,
    edit_reason: str = "Documentation sync",
  ) -> dict[str, Any] | None:
    """Update an existing post's content.

    Args:
      post_id: The Discourse post ID to update.
      raw: New markdown body content.
      edit_reason: Reason shown in edit history.

    Returns:
      Response dict, or None on failure.
    """
    payload = {
      "post": {
        "raw": raw,
        "edit_reason": edit_reason,
      },
    }
    return self._put(f"/posts/{post_id}.json", payload)

  def update_topic(
    self,
    topic_id: int,
    title: str,
    category_id: int,
  ) -> dict[str, Any] | None:
    """Update a topic's title and category.

    Args:
      topic_id: The Discourse topic ID to update.
      title: New topic title.
      category_id: New Discourse category ID.

    Returns:
      Response dict, or None on failure.
    """
    payload = {
      "title": title,
      "category_id": category_id,
    }
    return self._put(f"/t/-/{topic_id}.json", payload)

  def get_category_about_topic_id(self, category_id: int) -> int | None:
    """Get the auto-generated 'About' topic ID for a Discourse category.

    Uses the /c/{category_id}/show.json endpoint and extracts the
    topic ID from the category's topic_url field.

    Args:
      category_id: The Discourse category ID.

    Returns:
      Topic ID of the category's 'About' topic, or None if not found.
    """
    data = self._get(f"/c/{category_id}/show.json")
    if data is None:
      return None
    category = data.get("category", {})
    topic_url = category.get("topic_url", "")
    if not topic_url:
      return None
    # topic_url is like "/t/about-the-category-name/123"
    parts = topic_url.rstrip("/").split("/")
    try:
      return int(parts[-1])
    except (ValueError, IndexError):
      return None

  def first_post_id(self, topic_id: int) -> int | None:
    """Get the first post ID of a topic.

    Args:
      topic_id: The Discourse topic ID.

    Returns:
      Post ID of the first post, or None if not found.
    """
    data = self._get(f"/t/{topic_id}.json")
    if data is None:
      return None
    posts = data.get("post_stream", {}).get("posts", [])
    if not posts:
      return None
    return posts[0].get("id")

  def get_post_raw(self, post_id: int) -> str | None:
    """Fetch the current raw markdown content of a post.

    Used to compare against the locally rendered body before deciding
    whether to push an update.  Avoids unnecessary edits when the
    rendered content hasn't changed (e.g. after a cache eviction).

    Args:
      post_id: The Discourse post ID.

    Returns:
      Raw markdown string, or None if the request failed.
    """
    data = self._get(f"/posts/{post_id}.json")
    if data is None:
      return None
    return data.get("raw")

  # ----- HTTP helpers -----

  def _headers(self) -> dict[str, str]:
    return {
      "Content-Type": "application/json",
      "Api-Key": self._config.api_key,
      "Api-Username": self._config.api_user,
      "User-Agent": "Mozilla/5.0 (compatible; sunnypilot-docs-sync/1.0)",
    }

  def _get(self, path: str) -> dict[str, Any] | None:
    url = self._config.base_url + path
    req = urllib.request.Request(url, headers=self._headers(), method="GET")
    return self._send(req)

  def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any] | None:
    url = self._config.base_url + path
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=self._headers(), method="POST")
    return self._send(req)

  def _put(self, path: str, payload: dict[str, Any]) -> dict[str, Any] | None:
    url = self._config.base_url + path
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=self._headers(), method="PUT")
    return self._send(req)

  def _send(self, req: urllib.request.Request) -> dict[str, Any] | None:
    try:
      with urllib.request.urlopen(req) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
      # Log but don't crash — caller decides how to handle None
      status = e.code
      body = ""
      try:
        body = e.read().decode("utf-8", errors="replace")[:500]
      except Exception:
        pass
      print(f"  Discourse API error: {req.method} {req.full_url} -> {status}: {body}")
      return None
    except urllib.error.URLError as e:
      print(f"  Discourse connection error: {req.full_url} -> {e.reason}")
      return None
