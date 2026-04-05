#!/usr/bin/env python3
"""Sync orchestrator — one-way push from docs/ to Discourse.

Wires together nav_parser + content_cache + converter + discourse_client
to sync all documentation defined in zensical.toml to Discourse topics.

Usage:
  # Dry run (no API mutations):
  uv run --python 3.12 python tools/sync_to_discourse.py --dry-run --verbose

  # Full sync:
  uv run --python 3.12 python tools/sync_to_discourse.py

  # Force re-sync (bypass cache):
  uv run --python 3.12 python tools/sync_to_discourse.py --force
"""

from __future__ import annotations

import argparse
import os
import sys
import time
import tomllib
from pathlib import Path

# Ensure tools dir is importable
sys.path.insert(0, str(Path(__file__).parent))

from content_cache import ContentCache
from converter import convert
from discourse_client import DiscourseClient, DiscourseConfig
from nav_parser import NavEntry, parse_all

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
ZENSICAL_TOML = REPO_ROOT / "zensical.toml"
GITHUB_REF_NAME = os.environ.get("GITHUB_REF_NAME", "master")

SKIP_INDEX_FILES = frozenset({"index.md", "README.md"})

# Discourse rejects titles it deems "unclear" (too short, repeated letters, etc.).
# Override with longer, more descriptive titles for affected docs.
# Map new doc paths to their previous sync IDs so the sync can find
# existing Discourse topics after a file is moved.  Each entry is
# removed automatically once the topic is updated with the new sync ID.
PATH_REDIRECTS: dict[str, str] = {
  "technical/gas-interceptor.md": "how-to/gas-interceptor.md",
  "technical/zorro-steering-sensor.md": "how-to/zorro-steering-sensor.md",
}

DISCOURSE_TITLE_OVERRIDES: dict[str, str] = {
  "features/connected/sunnylink.md": "sunnylink Connected Services",
  "features/connected/osm-maps.md": "OSM Maps Integration",
  "settings/toggles.md": "Toggles Settings",
  "settings/toggles/index.md": "Toggles Settings",
  "settings/sunnylink.md": "sunnylink Settings",
  "setup/ssh-method.md": "SSH Installation Method",
}


def extract_title(content: str, fallback: str) -> str:
  """Extract title from YAML front matter or first heading."""
  for line in content.splitlines():
    s = line.strip()
    if s.startswith("title:"):
      return s[len("title:"):].strip().strip("\"'")
    if s.startswith("# "):
      return s[2:].strip()
  return fallback


def _body_matches_discourse(local_body: str, remote_raw: str | None) -> bool:
  """Return True if local_body matches what Discourse currently has.

  Normalizes trailing whitespace on each line before comparing so minor
  formatting differences introduced during Discourse roundtrips do not
  trigger false positives.

  Args:
    local_body: The fully rendered body we would send to Discourse.
    remote_raw: The raw markdown currently stored in Discourse, or None
      if the fetch failed (treat as not matching so we update).

  Returns:
    True only when the content is effectively identical.
  """
  if remote_raw is None:
    return False

  def _normalize(s: str) -> str:
    return "\n".join(line.rstrip() for line in s.splitlines()).rstrip()

  return _normalize(local_body) == _normalize(remote_raw)


def build_footer(doc_path: str) -> str:
  """Build the sync footer with GitHub link and sync ID."""
  gh_url = (
    f"https://github.com/sunnypilot/user-docs/blob/"
    f"{GITHUB_REF_NAME}/docs/{doc_path}"
  )
  return (
    "\n\n---\n"
    f"<small>This document is version-controlled. "
    f"Suggest changes [on GitHub]({gh_url}).</small>[^docs-sync]\n\n"
    f"[^docs-sync]: docs-sync-id: {doc_path}\n"
  )


def _strip_markdown_tables(text: str) -> str:
  """Remove markdown tables from text.

  Tables in index pages serve as navigation, which the sidebar replaces
  on Discourse.  Keeping both creates duplicate/confusing content in the
  About topic.
  """
  result_lines: list[str] = []
  in_table = False

  for line in text.splitlines():
    stripped = line.strip()
    is_table_line = stripped.startswith("|") and stripped.endswith("|")

    if is_table_line:
      in_table = True
      continue

    if in_table and not stripped:
      # Blank line after table — skip it too
      in_table = False
      continue

    in_table = False
    result_lines.append(line)

  return "\n".join(result_lines)


def _get_section_folder(items: list) -> str | None:
  """Extract the top-level section folder from nav items."""
  for item in items:
    if isinstance(item, str) and not item.startswith("http"):
      if "/" in item:
        return item.split("/")[0]
    if isinstance(item, dict):
      for _, value in item.items():
        if isinstance(value, str) and not value.startswith("http"):
          parts = value.split("/")
          if len(parts) > 1:
            return parts[0]
        if isinstance(value, list):
          result = _get_section_folder(value)
          if result:
            return result.split("/")[0]
  return None


def _resolve_topic_id(
  doc_path: str,
  synced_topics: dict[str, int],
  client: DiscourseClient,
) -> int | None:
  """Resolve a doc path to its Discourse topic ID."""
  if doc_path in synced_topics:
    return synced_topics[doc_path]

  # Look up via search API
  time.sleep(1.0)
  existing = client.find_topic_by_sync_id(doc_path)

  if existing is None and doc_path in PATH_REDIRECTS:
    time.sleep(1.0)
    existing = client.find_topic_by_sync_id(PATH_REDIRECTS[doc_path])

  if existing:
    topic_id = existing["id"]
    synced_topics[doc_path] = topic_id
    return topic_id

  return None


def _index_has_own_category(doc_path: str, config: DiscourseConfig) -> bool:
  """Check if an index file's directory has a dedicated Discourse category.

  An index at ``settings/device/index.md`` owns its category only if
  ``settings/device`` appears in the category mapping.  If it falls back
  to the parent ``settings`` category, the index should be treated as a
  regular topic rather than the category About topic.
  """
  parts = doc_path.split("/")
  dir_prefix = "/".join(parts[:-1])
  return dir_prefix in config.category_mapping


def _find_index_path(items: list) -> str | None:
  """Find the index.md path in a nav item list, if any."""
  for item in items:
    if isinstance(item, str) and Path(item).name in SKIP_INDEX_FILES:
      return item
  return None


def _walk_nav_for_sidebar(
  items: list,
  base_url: str,
  synced_topics: dict[str, int],
  client: DiscourseClient,
  lines: list[str],
) -> None:
  """Recursively walk nav tree to build sidebar in Discourse Docs plugin format.

  Sidebar items use: * Item Title: {full topic URL}
  Sections use: ## Section Title

  When a sub-section contains only an index.md (no child pages), it is
  rendered as a leaf item linking to the About topic instead of an empty
  section heading.  This ensures the Discourse Docs plugin sidebar shows
  all navigable sections.
  """
  for item in items:
    if isinstance(item, str):
      # Bare path (usually index.md) — skip for sidebar
      continue

    if not isinstance(item, dict):
      continue

    for title, value in item.items():
      if isinstance(value, str):
        # Leaf node (a doc page)
        if value.startswith("http"):
          continue
        if Path(value).name in SKIP_INDEX_FILES:
          continue

        topic_id = _resolve_topic_id(
          value, synced_topics, client,
        )
        if topic_id:
          lines.append(f"* {title}: {base_url}/t/{topic_id}")

      elif isinstance(value, list):
        # Sub-section — collect child items first to check if empty
        child_lines: list[str] = []
        _walk_nav_for_sidebar(
          value, base_url, synced_topics, client,
          child_lines,
        )

        if child_lines:
          # Has child items — render as section heading + items
          lines.append(f"## {title}")
          lines.extend(child_lines)
        else:
          # No child items (only index.md) — render as leaf link
          index_path = _find_index_path(value)
          if index_path:
            topic_id = _resolve_topic_id(
              index_path, synced_topics, client,
            )
            if topic_id:
              lines.append(f"* {title}: {base_url}/t/{topic_id}")


def _generate_sidebars(
  *,
  config: DiscourseConfig,
  client: DiscourseClient,
  synced_topics: dict[str, int],
  index_contents: dict[str, str],
  dry_run: bool,
  verbose: bool,
  stats: dict[str, int],
) -> None:
  """Generate sidebar indexes for each top-level nav section.

  Uses the Discourse Docs plugin format: bulleted lists with
  ``* Title: {full_topic_url}`` and ``## Section`` headers.
  Combines with the converted index.md content for each category.
  """
  with open(ZENSICAL_TOML, "rb") as f:
    toml_data = tomllib.load(f)

  nav = toml_data.get("project", {}).get("nav", [])
  base_url = config.base_url

  for item in nav:
    if not isinstance(item, dict):
      continue

    for section_title, section_value in item.items():
      if not isinstance(section_value, list):
        continue  # Skip leaf entries like Home

      section_folder = _get_section_folder(section_value)
      if not section_folder:
        continue

      if not config.has_category_for(f"{section_folder}/dummy.md"):
        if verbose:
          print(f"  SKIP sidebar (no category): {section_title}")
        continue

      category_id = config.category_id_for(f"{section_folder}/dummy.md")

      # Build sidebar content
      sidebar_lines: list[str] = []
      _walk_nav_for_sidebar(
        section_value, base_url, synced_topics, client,
        sidebar_lines,
      )

      sidebar_content = "\n".join(sidebar_lines)

      # Combine with index content if available.
      # Strip markdown tables from the index body — they duplicate the
      # sidebar navigation and create a messy About topic on Discourse.
      index_path = f"{section_folder}/index.md"
      index_body = index_contents.get(index_path, "")

      if index_body and sidebar_content:
        stripped = _strip_markdown_tables(index_body).rstrip()
        if stripped:
          combined = f"{stripped}\n\n{sidebar_content}\n"
        else:
          combined = f"Browse the **{section_title}** documentation:\n\n{sidebar_content}\n"
      elif index_body:
        combined = index_body
      else:
        # Discourse requires at least one paragraph in category descriptions
        combined = f"Browse the **{section_title}** documentation:\n\n{sidebar_content}\n"

      if dry_run:
        print(
          f"  [DRY RUN] Would update sidebar: {section_title} "
          f"(category {category_id}, {len(sidebar_lines)} items)"
        )
        stats["sidebars_updated"] += 1
        continue

      about_topic_id = client.get_category_about_topic_id(category_id)
      if about_topic_id is None:
        print(
          f"  FAIL: No About topic for sidebar "
          f"{section_title} (category {category_id})"
        )
        continue

      post_id = client.first_post_id(about_topic_id)
      if post_id is None:
        print(
          f"  FAIL: No first post for sidebar "
          f"About topic {about_topic_id}"
        )
        continue

      time.sleep(1.0)
      result = client.update_post(
        post_id, combined,
        edit_reason="Docs sync: sidebar index",
      )
      if result is None:
        print(f"  FAIL: Could not update sidebar for {section_title}")
        continue

      print(f"  Sidebar updated: {section_title} ({len(sidebar_lines)} items)")
      stats["sidebars_updated"] += 1


def _resolve_all_topic_ids(
  entries: list[NavEntry],
  *,
  config: DiscourseConfig,
  client: DiscourseClient,
  verbose: bool,
) -> dict[str, int]:
  """Pass 1: Resolve all doc paths to Discourse topic IDs.

  Populates a complete mapping before any content conversion, so that
  internal .md links can resolve to direct /t/{id} URLs.
  """
  topic_ids: dict[str, int] = {}

  print("Pass 1: Resolving topic IDs...")
  for entry in entries:
    label = f"[{entry.path}] {entry.title}"

    if not config.has_category_for(entry.path):
      continue

    is_index = Path(entry.path).name in SKIP_INDEX_FILES

    if is_index and _index_has_own_category(entry.path, config):
      # Index files with a dedicated category map to "About" topics.
      # Sub-section indexes without their own category fall through
      # to regular doc resolution below.
      category_id = config.category_id_for(entry.path)
      time.sleep(1.0)
      about_topic_id = client.get_category_about_topic_id(category_id)
      if about_topic_id is not None:
        topic_ids[entry.path] = about_topic_id
        if verbose:
          print(f"  Resolved index: {label} -> About topic {about_topic_id}")
      continue

    # Normal doc: sync-id search -> redirect fallback -> topic-map fallback
    time.sleep(1.0)
    existing = client.find_topic_by_sync_id(entry.path)
    resolved_via = "sync-id"

    if existing is None and entry.path in PATH_REDIRECTS:
      old_path = PATH_REDIRECTS[entry.path]
      time.sleep(1.0)
      existing = client.find_topic_by_sync_id(old_path)
      if existing is not None:
        resolved_via = f"redirect ({old_path})"

    if existing is None and entry.path in config.topic_mapping:
      mapped_id = config.topic_mapping[entry.path]
      existing = {"id": mapped_id}
      resolved_via = "topic-map"

    if existing is None:
      # Title-based fallback: find topics that pre-date the sync-id system
      # or were created outside the pipeline.
      file_path = DOCS_DIR / entry.path
      if file_path.exists():
        raw = file_path.read_text(encoding="utf-8")
        title = DISCOURSE_TITLE_OVERRIDES.get(
          entry.path,
          extract_title(raw, entry.title),
        )
        time.sleep(1.0)
        existing = client.find_topic_by_title(title)
        if existing is not None:
          resolved_via = f"title ({title})"

    if existing is not None:
      topic_id = existing["id"]
      topic_ids[entry.path] = topic_id
      if verbose:
        print(f"  Resolved: {label} -> topic {topic_id} (via {resolved_via})")

  print(f"  Resolved {len(topic_ids)} topic IDs")
  print()
  return topic_ids


def sync_docs(args: argparse.Namespace) -> None:
  """Main sync: two-pass approach for direct inter-topic links.

  Pass 1: Resolve all doc paths to Discourse topic IDs.
  Pass 2: Convert content (with topic ID map for direct links) and push.
  """
  config = DiscourseConfig.from_env()
  client = DiscourseClient(config)
  cache = ContentCache()

  entries = parse_all(ZENSICAL_TOML)

  stats: dict[str, int] = {
    "total": len(entries),
    "created": 0,
    "updated": 0,
    "updated_index": 0,
    "skipped_cached": 0,
    "skipped_discourse_match": 0,
    "skipped_no_category": 0,
    "failed": 0,
    "sidebars_updated": 0,
  }

  # Store converted index.md content for sidebar combination
  index_contents: dict[str, str] = {}

  print(f"Sync: {len(entries)} entries from zensical.toml")
  print(f"  Discourse: {config.base_url}")
  print(f"  Dry run: {args.dry_run}")
  print(f"  Force: {args.force}")
  print()

  # --- Pass 1: Resolve all topic IDs ---
  synced_topics = _resolve_all_topic_ids(
    entries, config=config, client=client, verbose=args.verbose,
  )

  # --- Pass 2: Convert and push ---
  print("Pass 2: Syncing content...")
  for entry in entries:
    label = f"[{entry.path}] {entry.title}"

    # Check category mapping
    if not config.has_category_for(entry.path):
      if args.verbose:
        print(f"  SKIP (no category): {label}")
      stats["skipped_no_category"] += 1
      continue

    category_id = config.category_id_for(entry.path)

    # Read file
    file_path = DOCS_DIR / entry.path
    if not file_path.exists():
      print(f"  FAIL (file not found): {label}")
      stats["failed"] += 1
      continue

    raw_content = file_path.read_text(encoding="utf-8")

    is_index = Path(entry.path).name in SKIP_INDEX_FILES
    is_about_topic = is_index and _index_has_own_category(entry.path, config)

    # Convert with topic ID map for direct inter-topic links
    converted = convert(
      raw_content, file_path=entry.path, topic_id_map=synced_topics,
    )
    body = converted.rstrip("\n") + build_footer(entry.path)

    # Always store index content for sidebar generation, even when cached
    if is_about_topic:
      index_contents[entry.path] = body

    # Cache check (skipped during dry run — always resolve for verification)
    cached = not cache.is_changed(entry.path, raw_content)
    if not args.dry_run and not args.force and cached:
      if args.verbose:
        print(f"  SKIP (cached): {label}")
      stats["skipped_cached"] += 1
      continue

    title = DISCOURSE_TITLE_OVERRIDES.get(
      entry.path,
      extract_title(raw_content, entry.title),
    )

    if is_about_topic:
      # Index files update the "About" topic for their category.
      # Each index.md maps to the most specific matching category
      # (e.g. features/cruise/index.md -> sub-category 140).
      about_topic_id = synced_topics.get(entry.path)
      if args.dry_run:
        cache_tag = " [cached]" if cached else ""
        if about_topic_id is not None:
          print(
            f"  [DRY RUN] Would update index{cache_tag}: {label}\n"
            f"            -> About topic {about_topic_id} "
            f"(category {category_id})\n"
            f"            -> {config.base_url}/t/{about_topic_id}"
          )
        else:
          print(
            f"  [DRY RUN] WARN: No About topic for "
            f"category {category_id}: {label}"
          )
        stats["updated_index"] += 1
      else:
        if about_topic_id is None:
          print(
            f"  FAIL: No About topic for "
            f"category {category_id}: {label}"
          )
          stats["failed"] += 1
          continue

        post_id = client.first_post_id(about_topic_id)
        if post_id is None:
          print(
            f"  FAIL: No first post for "
            f"About topic {about_topic_id}: {label}"
          )
          stats["failed"] += 1
          continue

        time.sleep(1.0)
        current_raw = client.get_post_raw(post_id)
        if _body_matches_discourse(body, current_raw):
          if args.verbose:
            print(f"  SKIP (discourse up-to-date): {label}")
          stats["skipped_discourse_match"] += 1
          cache.save(entry.path, raw_content)
          continue

        time.sleep(1.0)
        result = client.update_post(
          post_id, body,
          edit_reason="Docs sync: index page",
        )
        if result is None:
          print(
            f"  FAIL: Could not update "
            f"About topic {about_topic_id}: {label}"
          )
          stats["failed"] += 1
          continue

        print(f"  Updated index: {label} -> About topic {about_topic_id}")
        stats["updated_index"] += 1

      # Update cache for index pages
      if not args.dry_run:
        cache.save(entry.path, raw_content)
      continue

    # --- Normal doc: find or create ---
    topic_id = synced_topics.get(entry.path)

    if topic_id is not None:
      if args.dry_run:
        cache_tag = " [cached]" if cached else ""
        print(
          f"  [DRY RUN] Would update{cache_tag}: {label}\n"
          f"            -> topic {topic_id} "
          f"(category {category_id})\n"
          f"            -> {config.base_url}/t/{topic_id}"
        )
        stats["updated"] += 1
      else:
        post_id = client.first_post_id(topic_id)
        if post_id is None:
          print(f"  FAIL: No first post for topic {topic_id}: {label}")
          stats["failed"] += 1
          continue

        time.sleep(1.0)
        current_raw = client.get_post_raw(post_id)
        if _body_matches_discourse(body, current_raw):
          if args.verbose:
            print(f"  SKIP (discourse up-to-date): {label}")
          stats["skipped_discourse_match"] += 1
          cache.save(entry.path, raw_content)
          continue

        time.sleep(1.0)
        result = client.update_post(
          post_id, body,
          edit_reason="Docs sync",
        )
        if result is None:
          print(f"  FAIL: Could not update topic {topic_id}: {label}")
          stats["failed"] += 1
          continue

        # Update topic title and category
        time.sleep(1.0)
        client.update_topic(
          topic_id, title,
          category_id=category_id,
        )

        print(f"  Updated: {label} -> topic {topic_id}")
        stats["updated"] += 1
    else:
      # Pre-create title check: search for an existing topic by title
      # before attempting to create.  This catches topics that Pass 1
      # missed (e.g. search indexing delays, topics without sync-ids).
      time.sleep(1.0)
      existing_by_title = client.find_topic_by_title(title)

      if existing_by_title is not None:
        found_id = existing_by_title["id"]
        synced_topics[entry.path] = found_id

        if args.dry_run:
          cache_tag = " [cached]" if cached else ""
          print(
            f"  [DRY RUN] Would update (found by title){cache_tag}: "
            f"{label}\n"
            f"            -> topic {found_id} "
            f"(category {category_id})\n"
            f"            -> {config.base_url}/t/{found_id}"
          )
          stats["updated"] += 1
        else:
          post_id = client.first_post_id(found_id)
          if post_id is None:
            print(
              f"  FAIL: No first post for topic {found_id}: {label}"
            )
            stats["failed"] += 1
            continue

          time.sleep(1.0)
          current_raw = client.get_post_raw(post_id)
          if _body_matches_discourse(body, current_raw):
            if args.verbose:
              print(f"  SKIP (discourse up-to-date): {label}")
            stats["skipped_discourse_match"] += 1
            cache.save(entry.path, raw_content)
            continue

          time.sleep(1.0)
          result = client.update_post(
            post_id, body,
            edit_reason="Docs sync",
          )
          if result is None:
            print(
              f"  FAIL: Could not update topic {found_id}: {label}"
            )
            stats["failed"] += 1
            continue

          time.sleep(1.0)
          client.update_topic(
            found_id, title,
            category_id=category_id,
          )

          print(
            f"  Updated (found by title): {label} -> topic {found_id}"
          )
          stats["updated"] += 1

      elif args.dry_run:
        cache_tag = " [cached]" if cached else ""
        print(
          f"  [DRY RUN] Would create{cache_tag}: {label}\n"
          f"            -> NEW (category {category_id})"
        )
        stats["created"] += 1
      else:
        time.sleep(1.0)
        result = client.create_topic(
          title=title,
          raw=body,
          category_id=category_id,
          tags=["docs-auto-sync"],
        )
        if result is None:
          print(f"  FAIL: Could not create topic: {label}")
          stats["failed"] += 1
          continue

        new_topic_id = result.get("topic_id", 0)
        synced_topics[entry.path] = new_topic_id
        print(f"  Created: {label} -> topic {new_topic_id}")
        stats["created"] += 1

    # Update cache on success
    if not args.dry_run:
      cache.save(entry.path, raw_content)

  # --- Sidebar generation ---
  print()
  print("Generating sidebars...")
  _generate_sidebars(
    config=config,
    client=client,
    synced_topics=synced_topics,
    index_contents=index_contents,
    dry_run=args.dry_run,
    verbose=args.verbose,
    stats=stats,
  )

  # --- Summary ---
  print()
  print("=" * 60)
  print("Sync Summary")
  print("=" * 60)
  print(f"  Total Parsed:          {stats['total']}")
  print(f"  Created:               {stats['created']}")
  print(f"  Updated (Normal):      {stats['updated']}")
  print(f"  Updated (Index):       {stats['updated_index']}")
  print(f"  Skipped (Cached):      {stats['skipped_cached']}")
  print(f"  Skipped (Discourse Match): {stats['skipped_discourse_match']}")
  print(f"  Skipped (No Category): {stats['skipped_no_category']}")
  print(f"  Failed:                {stats['failed']}")
  print(f"  Sidebars Updated:      {stats['sidebars_updated']}")
  print("=" * 60)

  if stats["failed"] > 0:
    sys.exit(1)


def main() -> None:
  parser = argparse.ArgumentParser(description="Sync docs/ Markdown to Discourse topics.")
  parser.add_argument("--dry-run", action="store_true", help="Preview changes without making API calls.")
  parser.add_argument("--verbose", "-v", action="store_true", help="Print detailed progress for skipped entries.")
  parser.add_argument("--force", action="store_true", help="Bypass content cache and re-sync all entries.")
  args = parser.parse_args()
  sync_docs(args)


if __name__ == "__main__":
  main()
