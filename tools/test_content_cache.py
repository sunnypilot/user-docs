#!/usr/bin/env python3
"""Tests for the SHA-256 content cache.

Run: python3 tools/test_content_cache.py
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from content_cache import ContentCache


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_cache(tmp: str) -> ContentCache:
  return ContentCache(cache_dir=Path(tmp) / ".discourse_sync_cache")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_compute_hash_deterministic():
  """Same content always produces the same hash."""
  h1 = ContentCache.compute_hash("hello world")
  h2 = ContentCache.compute_hash("hello world")
  assert h1 == h2
  assert len(h1) == 64  # SHA-256 hex digest length
  print("  PASS: compute_hash_deterministic")


def test_compute_hash_differs():
  """Different content produces different hashes."""
  h1 = ContentCache.compute_hash("hello world")
  h2 = ContentCache.compute_hash("hello world!")
  assert h1 != h2
  print("  PASS: compute_hash_differs")


def test_is_changed_no_cache():
  """First run (no cache file) should report changed."""
  with tempfile.TemporaryDirectory() as tmp:
    cache = make_cache(tmp)
    assert cache.is_changed("features/icbm.md", "content")
  print("  PASS: is_changed_no_cache")


def test_is_changed_after_save():
  """After saving, same content should report unchanged."""
  with tempfile.TemporaryDirectory() as tmp:
    cache = make_cache(tmp)
    cache.save("features/icbm.md", "content v1")
    assert not cache.is_changed("features/icbm.md", "content v1")
  print("  PASS: is_changed_after_save")


def test_is_changed_after_modification():
  """After saving, different content should report changed."""
  with tempfile.TemporaryDirectory() as tmp:
    cache = make_cache(tmp)
    cache.save("features/icbm.md", "content v1")
    assert cache.is_changed("features/icbm.md", "content v2")
  print("  PASS: is_changed_after_modification")


def test_separate_paths_independent():
  """Different doc paths have independent caches."""
  with tempfile.TemporaryDirectory() as tmp:
    cache = make_cache(tmp)
    cache.save("features/icbm.md", "content A")
    cache.save("safety/safety.md", "content B")

    assert not cache.is_changed("features/icbm.md", "content A")
    assert not cache.is_changed("safety/safety.md", "content B")
    assert cache.is_changed("features/icbm.md", "content B")
    assert cache.is_changed("safety/safety.md", "content A")
  print("  PASS: separate_paths_independent")


def test_cache_dir_created_on_save():
  """Cache directory is created automatically on first save."""
  with tempfile.TemporaryDirectory() as tmp:
    cache_dir = Path(tmp) / "nested" / "cache"
    cache = ContentCache(cache_dir=cache_dir)
    assert not cache_dir.exists()

    cache.save("test.md", "content")
    assert cache_dir.exists()
    assert (cache_dir / "test.sha256").exists()
  print("  PASS: cache_dir_created_on_save")


def test_cache_file_naming():
  """Cache files use slug derived from doc path."""
  with tempfile.TemporaryDirectory() as tmp:
    cache = make_cache(tmp)
    cache.save("settings/cruise/speed-limit/source.md", "content")

    expected_name = "settings_cruise_speed-limit_source.sha256"
    cached_files = list(cache.cache_dir.glob("*.sha256"))
    assert len(cached_files) == 1
    assert cached_files[0].name == expected_name
  print("  PASS: cache_file_naming")


def test_clear_removes_all():
  """clear() removes all .sha256 files and returns count."""
  with tempfile.TemporaryDirectory() as tmp:
    cache = make_cache(tmp)
    cache.save("a.md", "aaa")
    cache.save("b.md", "bbb")
    cache.save("c.md", "ccc")

    removed = cache.clear()
    assert removed == 3
    assert list(cache.cache_dir.glob("*.sha256")) == []
  print("  PASS: clear_removes_all")


def test_clear_empty_cache():
  """clear() on nonexistent cache dir returns 0."""
  with tempfile.TemporaryDirectory() as tmp:
    cache = make_cache(tmp)
    assert cache.clear() == 0
  print("  PASS: clear_empty_cache")


def test_overwrite_on_resave():
  """Saving again overwrites the previous hash."""
  with tempfile.TemporaryDirectory() as tmp:
    cache = make_cache(tmp)
    cache.save("doc.md", "version 1")
    assert not cache.is_changed("doc.md", "version 1")
    assert cache.is_changed("doc.md", "version 2")

    cache.save("doc.md", "version 2")
    assert cache.is_changed("doc.md", "version 1")
    assert not cache.is_changed("doc.md", "version 2")
  print("  PASS: overwrite_on_resave")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


if __name__ == "__main__":
  print("Testing content cache:")
  tests = [
    test_compute_hash_deterministic,
    test_compute_hash_differs,
    test_is_changed_no_cache,
    test_is_changed_after_save,
    test_is_changed_after_modification,
    test_separate_paths_independent,
    test_cache_dir_created_on_save,
    test_cache_file_naming,
    test_clear_removes_all,
    test_clear_empty_cache,
    test_overwrite_on_resave,
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
