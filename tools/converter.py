"""Zensical -> Discourse-compatible Markdown converter.

Converts Zensical/MkDocs Material syntax to Discourse-friendly markdown:
1. Strip YAML front matter
2. Convert admonitions (!!!/???/???+) to Discourse callouts (> [!TYPE])
3. Convert Material tabs (=== "Tab Name") to bold headings + ---
4. Strip grid card HTML (<div class="grid cards" markdown>)
5. Convert Material emoji shortcodes (:material-*:) to Unicode or strip
6. Resolve internal .md links to Discourse search URLs (via docs-sync-id)
7. Clean up excessive blank lines
"""

from __future__ import annotations

import os
import re
import urllib.parse
from pathlib import Path

DISCOURSE_FORUM_URL = os.environ.get(
  "DISCOURSE_URL", "https://community.sunnypilot.ai"
).rstrip("/")

ADMONITION_MAP: dict[str, str] = {
  "note": "NOTE",
  "abstract": "ABSTRACT",
  "info": "INFO",
  "tip": "TIP",
  "success": "SUCCESS",
  "question": "QUESTION",
  "warning": "WARNING",
  "failure": "FAILURE",
  "danger": "DANGER",
  "bug": "BUG",
  "example": "EXAMPLE",
  "quote": "QUOTE",
}

EMOJI_MAP: dict[str, str] = {
  ":material-rocket-launch:": "",
  ":material-cog:": "",
  ":material-car:": "",
  ":material-shield:": "",
  ":material-download:": "",
  ":material-check:": "Y",
  ":material-close:": "N",
  ":material-alert:": "!",
  ":material-information:": "i",
  ":material-help-circle:": "?",
  ":material-star:": "*",
  ":material-link:": "",
  ":material-eye:": "",
  ":material-map:": "",
  ":material-wifi:": "",
  ":material-cellphone:": "",
  ":material-steering:": "",
  ":material-speedometer:": "",
}

_ADMONITION_RE = re.compile(r"^(\s*)(!{3}|\?{3}\+?)\s+(\w+)(?:\s+\"([^\"]*)\")?\s*$")
_TAB_RE = re.compile(r'^(\s*)===\s+"([^"]+)"\s*$')
_FRONT_MATTER_RE = re.compile(r"\A---\n.*?\n---\n*", re.DOTALL)
_GRID_CARD_OPEN_RE = re.compile(r'<div\s+class="grid\s+cards"\s*(?:markdown)?\s*>')
_GRID_CARD_CLOSE_RE = re.compile(r"</div>")
_INTERNAL_LINK_RE = re.compile(r"\]\(([^)]+\.md(?:#[^)]*)?)\)")
_EMOJI_SHORTCODE_RE = re.compile(r":material-[\w-]+:")
_ESCAPED_CALLOUT_RE = re.compile(r"^(\s*>\s*)\\\[(![\w]+)\\\]", re.MULTILINE)
_EXCESSIVE_BLANKS_RE = re.compile(r"\n{4,}")
_LEGACY_FOOTER_RE = re.compile(
  r"\n*---\n+<small>This document is version[- ]controlled.*?</small>\n?",
  re.IGNORECASE,
)


def convert(
  content: str,
  *,
  file_path: str,
  topic_id_map: dict[str, int] | None = None,
) -> str:
  """Convert Zensical markdown to Discourse-compatible markdown.

  Args:
    content: Raw markdown content.
    file_path: Path to the source file relative to docs/
      (e.g. "getting-started/what-is-sunnypilot.md").
      Used for resolving relative internal links.
    topic_id_map: Optional mapping of doc paths to Discourse topic IDs.
      When provided, internal .md links resolve to direct /t/{id} URLs.
      When None, falls back to Discourse search URLs.

  Returns:
    Converted markdown string.
  """
  result = content

  result = strip_front_matter(result)
  result = convert_admonitions(result)
  result = unescape_callout_brackets(result)
  result = convert_tabs(result)
  result = convert_grid_cards(result)
  result = convert_emoji_shortcodes(result)
  result = resolve_internal_links(
    result, file_path=file_path, topic_id_map=topic_id_map,
  )
  result = strip_legacy_footer(result)
  result = clean_blank_lines(result)

  return result.strip() + "\n"


def strip_front_matter(content: str) -> str:
  """Remove YAML front matter (--- ... ---) from the start of content."""
  return _FRONT_MATTER_RE.sub("", content)


def convert_admonitions(content: str) -> str:
  """Convert MkDocs admonitions to Discourse/Obsidian callouts.

  Input:
    !!! warning "Title"
      Content line 1
      Content line 2

  Output:
    > [!WARNING] Title
    > Content line 1
    > Content line 2
  """
  lines = content.splitlines(keepends=True)
  result: list[str] = []
  i = 0

  while i < len(lines):
    line = lines[i]
    m = _ADMONITION_RE.match(line)

    if m:
      indent = m.group(1)
      marker = m.group(2)
      ad_type = m.group(3).lower()
      title = m.group(4)

      callout_type = ADMONITION_MAP.get(ad_type, ad_type.upper())

      header = f"{indent}> [!{callout_type}]"
      if title:
        header += f" {title}"

      if marker.startswith("???"):
        collapsed = "+" not in marker
        if not title:
          action = "expand" if collapsed else "collapse"
          header += f" *(click to {action})*"

      result.append(header + "\n")
      i += 1

      content_indent = indent + "    "
      while i < len(lines):
        content_line = lines[i]
        if content_line.startswith(content_indent):
          stripped = content_line[len(content_indent):]
          result.append(f"{indent}> {stripped}")
          i += 1
        elif content_line.strip() == "":
          # Check if blank line is internal to the admonition
          j = i + 1
          while j < len(lines) and lines[j].strip() == "":
            j += 1
          if j < len(lines) and lines[j].startswith(content_indent):
            result.append(f"{indent}>\n")
            i += 1
          else:
            break
        else:
          break
    else:
      result.append(line)
      i += 1

  return "".join(result)


def unescape_callout_brackets(content: str) -> str:
  """Unescape brackets in GitHub-style callouts.

  Converts ``> \\[!note\\]`` to ``> [!note]`` so Discourse renders
  them as callouts instead of showing literal backslash-bracket text.
  """
  return _ESCAPED_CALLOUT_RE.sub(r"\1[\2]", content)


def convert_tabs(content: str) -> str:
  """Convert Material tabs to bold headings with horizontal rules.

  Input:
    === "Tab Name"
      Content

  Output:
    **Tab Name**

    Content

    ---
  """
  lines = content.splitlines(keepends=True)
  result: list[str] = []
  i = 0

  while i < len(lines):
    line = lines[i]
    m = _TAB_RE.match(line)

    if m:
      indent = m.group(1)
      tab_name = m.group(2)

      result.append(f"{indent}**{tab_name}**\n")
      result.append("\n")
      i += 1

      content_indent = indent + "    "
      while i < len(lines):
        content_line = lines[i]
        if content_line.startswith(content_indent) or content_line.strip() == "":
          if content_line.strip() == "":
            result.append("\n")
          else:
            stripped = content_line[len(content_indent):]
            result.append(f"{indent}{stripped}")
          i += 1
        else:
          break

      # Ensure blank line before the horizontal rule
      if result and result[-1] != "\n":
        result.append("\n")
      result.append(f"{indent}---\n")
      result.append("\n")
    else:
      result.append(line)
      i += 1

  return "".join(result)


def convert_grid_cards(content: str) -> str:
  """Strip grid card HTML wrappers (Discourse doesn't support them)."""
  result = _GRID_CARD_OPEN_RE.sub("", content)
  result = _GRID_CARD_CLOSE_RE.sub("", result)
  return result


def convert_emoji_shortcodes(content: str) -> str:
  """Convert Material emoji shortcodes to plain text equivalents."""
  result = content
  for shortcode, replacement in EMOJI_MAP.items():
    result = result.replace(shortcode, replacement)
  # Strip any remaining :material-*: shortcodes not in the map
  result = _EMOJI_SHORTCODE_RE.sub("", result)
  return result


def resolve_internal_links(
  content: str,
  *,
  file_path: str,
  topic_id_map: dict[str, int] | None = None,
) -> str:
  """Resolve internal .md links to Discourse URLs.

  When *topic_id_map* is provided, links resolve to direct topic URLs:
    [text](../features/icbm.md) -> [text](https://…/t/244)

  Otherwise falls back to Discourse search URLs (for compatibility):
    [text](../features/icbm.md) -> [text](https://…/search?q=…)

  Anchors are preserved as fragment identifiers when using direct links,
  and stripped when using search URLs (search cannot target sections).
  """
  current_dir = str(Path(file_path).parent)

  def _replace_link(match: re.Match[str]) -> str:
    raw_path = match.group(1)
    # Skip external URLs
    if raw_path.startswith("http"):
      return match.group(0)

    # Separate anchor from path
    anchor = ""
    path_part = raw_path
    if "#" in raw_path:
      path_part, anchor = raw_path.rsplit("#", 1)

    # Resolve relative path from current file's directory
    resolved = os.path.normpath(os.path.join(current_dir, path_part))

    # Direct link via topic ID map
    if topic_id_map and resolved in topic_id_map:
      topic_id = topic_id_map[resolved]
      url = f"{DISCOURSE_FORUM_URL}/t/{topic_id}"
      if anchor:
        url += f"#{anchor}"
      return f"]({url})"

    # Fallback: Discourse search URL (anchors stripped)
    query = urllib.parse.quote(f'"docs-sync-id: {resolved}"', safe="")
    return f"]({DISCOURSE_FORUM_URL}/search?q={query})"

  return _INTERNAL_LINK_RE.sub(_replace_link, content)


def strip_legacy_footer(content: str) -> str:
  """Remove hardcoded legacy footer from source files.

  Some source files contain an inline ``<small>This document is
  version controlled …</small>`` footer that duplicates the footer
  appended by the sync orchestrator.  Strip it so the final output
  has only one footer.
  """
  return _LEGACY_FOOTER_RE.sub("", content)


def clean_blank_lines(content: str) -> str:
  """Collapse 4+ consecutive blank lines down to 3."""
  return _EXCESSIVE_BLANKS_RE.sub("\n\n\n", content)
