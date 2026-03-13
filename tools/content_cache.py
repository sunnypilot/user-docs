"""SHA-256 content cache for skipping unchanged docs on re-sync.

Stores one .sha256 file per doc in .discourse_sync_cache/. On re-run,
compares the current file hash against the cached hash to determine
whether the doc needs syncing.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

DEFAULT_CACHE_DIR = Path(__file__).resolve().parent.parent / ".discourse_sync_cache"


class ContentCache:
  """File-based SHA-256 content cache."""

  def __init__(self, cache_dir: str | Path = DEFAULT_CACHE_DIR) -> None:
    self._cache_dir = Path(cache_dir)

  @property
  def cache_dir(self) -> Path:
    return self._cache_dir

  @staticmethod
  def compute_hash(content: str) -> str:
    """Compute SHA-256 hex digest of content."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

  def _cache_path(self, doc_path: str) -> Path:
    """Map a doc path (e.g. 'features/cruise/icbm.md') to its cache file."""
    slug = doc_path.replace("/", "_").replace(".md", "")
    return self._cache_dir / f"{slug}.sha256"

  def is_changed(self, doc_path: str, content: str) -> bool:
    """Return True if content differs from the cached hash (or no cache exists)."""
    content_hash = self.compute_hash(content)
    cached = self._cache_path(doc_path)
    if not cached.exists():
      return True
    return cached.read_text().strip() != content_hash

  def save(self, doc_path: str, content: str) -> None:
    """Save the SHA-256 hash of content to the cache file."""
    content_hash = self.compute_hash(content)
    self._cache_dir.mkdir(parents=True, exist_ok=True)
    self._cache_path(doc_path).write_text(content_hash + "\n")

  def clear(self) -> int:
    """Remove all cached hashes. Returns the number of files removed."""
    if not self._cache_dir.exists():
      return 0
    count = 0
    for f in self._cache_dir.glob("*.sha256"):
      f.unlink()
      count += 1
    return count
