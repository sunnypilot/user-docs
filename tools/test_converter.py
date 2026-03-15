#!/usr/bin/env python3
"""Tests for the MkDocs -> Discourse markdown converter.

Run: uv run python tools/test_converter.py
"""

import sys
from pathlib import Path

# Ensure the tools directory is importable
sys.path.insert(0, str(Path(__file__).parent))

from converter import (
  clean_blank_lines,
  convert,
  convert_admonitions,
  convert_emoji_shortcodes,
  convert_grid_cards,
  convert_tabs,
  resolve_internal_links,
  strip_front_matter,
  strip_legacy_footer,
  unescape_callout_brackets,
)

# ---------------------------------------------------------------------------
# 1. Strip YAML Front Matter
# ---------------------------------------------------------------------------


def test_strip_front_matter_basic():
  input_text = """---
title: My Page
description: A test page
---

# Hello
"""
  expected = """# Hello
"""
  result = strip_front_matter(input_text)
  assert result == expected, f"FAIL:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: strip_front_matter_basic")


def test_strip_front_matter_absent():
  input_text = "# Hello\n\nContent here.\n"
  result = strip_front_matter(input_text)
  assert result == input_text, f"FAIL:\n{result!r}\n!=\n{input_text!r}"
  print("  PASS: strip_front_matter_absent")


# ---------------------------------------------------------------------------
# 2. Convert Admonitions
# ---------------------------------------------------------------------------


def test_basic_warning():
  input_text = """!!! warning "Important"
    sunnypilot is a **driver assistance** system.
    Always pay attention.
"""
  expected = """> [!WARNING] Important
> sunnypilot is a **driver assistance** system.
> Always pay attention.
"""
  result = convert_admonitions(input_text)
  assert result == expected, f"FAIL basic_warning:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: basic_warning")


def test_info_no_title():
  input_text = """!!! info
    Content line 1
    Content line 2
"""
  expected = """> [!INFO]
> Content line 1
> Content line 2
"""
  result = convert_admonitions(input_text)
  assert result == expected, f"FAIL info_no_title:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: info_no_title")


def test_info_with_title():
  input_text = """!!! info "Requirements"
    - Longitudinal control must be available
    - ICBM must be enabled
"""
  expected = """> [!INFO] Requirements
> - Longitudinal control must be available
> - ICBM must be enabled
"""
  result = convert_admonitions(input_text)
  assert result == expected, f"FAIL info_with_title:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: info_with_title")


def test_danger():
  input_text = """!!! danger "Important"
    sunnypilot is a **driver assistance** system. It is **NOT** a self-driving system.
"""
  expected = """> [!DANGER] Important
> sunnypilot is a **driver assistance** system. It is **NOT** a self-driving system.
"""
  result = convert_admonitions(input_text)
  assert result == expected, f"FAIL danger:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: danger")


def test_tip():
  input_text = """!!! tip
    The more detail you provide, the faster we can diagnose and fix the issue.
"""
  expected = """> [!TIP]
> The more detail you provide, the faster we can diagnose and fix the issue.
"""
  result = convert_admonitions(input_text)
  assert result == expected, f"FAIL tip:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: tip")


def test_multiline_with_blank():
  input_text = """!!! warning
    Line 1

    Line 2 after blank
"""
  expected = """> [!WARNING]
> Line 1
>
> Line 2 after blank
"""
  result = convert_admonitions(input_text)
  assert result == expected, f"FAIL multiline_with_blank:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: multiline_with_blank")


def test_collapsible():
  input_text = """??? warning "Click to see"
    Hidden content
"""
  expected = """> [!WARNING] Click to see
> Hidden content
"""
  result = convert_admonitions(input_text)
  assert result == expected, f"FAIL collapsible:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: collapsible")


def test_collapsible_open():
  input_text = """???+ info "Open by default"
    Visible content
"""
  expected = """> [!INFO] Open by default
> Visible content
"""
  result = convert_admonitions(input_text)
  assert result == expected, f"FAIL collapsible_open:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: collapsible_open")


def test_surrounded_by_content():
  input_text = """Some text before.

!!! note "Note Title"
    Note content here.

Some text after.
"""
  expected = """Some text before.

> [!NOTE] Note Title
> Note content here.

Some text after.
"""
  result = convert_admonitions(input_text)
  assert result == expected, f"FAIL surrounded:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: surrounded_by_content")


def test_multiple_admonitions():
  input_text = """!!! info "Requirements"
    - Req 1
    - Req 2

!!! warning "Vehicle Restrictions"
    - Tesla: disabled on release
    - Rivian: always disabled
"""
  expected = """> [!INFO] Requirements
> - Req 1
> - Req 2

> [!WARNING] Vehicle Restrictions
> - Tesla: disabled on release
> - Rivian: always disabled
"""
  result = convert_admonitions(input_text)
  assert result == expected, f"FAIL multiple:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: multiple_admonitions")


def test_real_doc_snippet():
  """Test with an actual snippet from docs content."""
  input_text = """## Speed Limit Mode

| Property | Value |
|----------|-------|
| **Param** | `SpeedLimitMode` |
| **Type** | Multi-button selector |

!!! info "Requirements"
    - Longitudinal control must be available, **or** ICBM must be enabled

!!! warning "Vehicle Restrictions"
    - **Tesla:** Speed Limit Assist mode is disabled on release branches
    - **Rivian:** Speed Limit Assist mode is always disabled

---
"""
  expected = """## Speed Limit Mode

| Property | Value |
|----------|-------|
| **Param** | `SpeedLimitMode` |
| **Type** | Multi-button selector |

> [!INFO] Requirements
> - Longitudinal control must be available, **or** ICBM must be enabled

> [!WARNING] Vehicle Restrictions
> - **Tesla:** Speed Limit Assist mode is disabled on release branches
> - **Rivian:** Speed Limit Assist mode is always disabled

---
"""
  result = convert_admonitions(input_text)
  assert result == expected, f"FAIL real_doc:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: real_doc_snippet")


# ---------------------------------------------------------------------------
# 2b. Unescape Callout Brackets
# ---------------------------------------------------------------------------


def test_unescape_callout_basic():
  input_text = "> \\[!note\\]\n> Content here.\n"
  expected = "> [!note]\n> Content here.\n"
  result = unescape_callout_brackets(input_text)
  assert result == expected, f"FAIL unescape_basic:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: unescape_callout_basic")


def test_unescape_callout_with_title():
  input_text = "> \\[!note\\] sunnypilot not installed\n> Follow these steps.\n"
  expected = "> [!note] sunnypilot not installed\n> Follow these steps.\n"
  result = unescape_callout_brackets(input_text)
  assert result == expected, f"FAIL unescape_with_title:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: unescape_callout_with_title")


def test_unescape_callout_no_change():
  input_text = "> [!note]\n> Already unescaped.\n"
  result = unescape_callout_brackets(input_text)
  assert result == input_text, f"FAIL unescape_noop:\n{result!r}"
  print("  PASS: unescape_callout_no_change")


def test_unescape_callout_non_blockquote_untouched():
  input_text = "Regular \\[text\\] not in blockquote.\n"
  result = unescape_callout_brackets(input_text)
  assert result == input_text, f"FAIL unescape_non_bq:\n{result!r}"
  print("  PASS: unescape_callout_non_blockquote_untouched")


# ---------------------------------------------------------------------------
# 3. Convert Tabs
# ---------------------------------------------------------------------------


def test_tabs_basic():
  input_text = """=== "Tab One"
    Content for tab one.

=== "Tab Two"
    Content for tab two.
"""
  expected = """**Tab One**

Content for tab one.

---

**Tab Two**

Content for tab two.

---

"""
  result = convert_tabs(input_text)
  assert result == expected, f"FAIL tabs_basic:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: tabs_basic")


def test_tabs_multiline():
  input_text = """=== "Details"
    Line 1
    Line 2
    Line 3
"""
  expected = """**Details**

Line 1
Line 2
Line 3

---

"""
  result = convert_tabs(input_text)
  assert result == expected, f"FAIL tabs_multiline:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: tabs_multiline")


# ---------------------------------------------------------------------------
# 4. Convert Grid Cards
# ---------------------------------------------------------------------------


def test_grid_cards_stripped():
  input_text = """<div class="grid cards" markdown>

- **Card 1** - Description
- **Card 2** - Description

</div>
"""
  expected = """

- **Card 1** - Description
- **Card 2** - Description

"""
  result = convert_grid_cards(input_text)
  # Normalize whitespace for comparison
  assert result.strip() == expected.strip(), f"FAIL grid_cards:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: grid_cards_stripped")


# ---------------------------------------------------------------------------
# 5. Convert Emoji Shortcodes
# ---------------------------------------------------------------------------


def test_emoji_known():
  input_text = ":material-check: Supported | :material-close: Not supported"
  expected = "Y Supported | N Not supported"
  result = convert_emoji_shortcodes(input_text)
  assert result == expected, f"FAIL emoji_known:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: emoji_known")


def test_emoji_unknown_stripped():
  input_text = ":material-unknown-icon: Some text"
  expected = " Some text"
  result = convert_emoji_shortcodes(input_text)
  assert result == expected, f"FAIL emoji_unknown:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: emoji_unknown_stripped")


def test_emoji_in_grid_card():
  input_text = "- :material-rocket-launch: **[Feature](link.md)**"
  expected = "-  **[Feature](link.md)**"
  result = convert_emoji_shortcodes(input_text)
  assert result == expected, f"FAIL emoji_grid:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: emoji_in_grid_card")


# ---------------------------------------------------------------------------
# 6. Resolve Internal Links
# ---------------------------------------------------------------------------


def test_internal_link_relative():
  input_text = "See [ICBM](../features/cruise/icbm.md) for details."
  result = resolve_internal_links(
    input_text,
    file_path="settings/cruise/speed-limit.md",
  )
  assert "/search?q=" in result, f"FAIL internal_link missing search URL:\n{result!r}"
  assert "docs-sync-id" in result, f"FAIL internal_link missing sync-id:\n{result!r}"
  assert "features%2Fcruise%2Ficbm.md" in result or "features/cruise/icbm.md" in result, (
    f"FAIL internal_link wrong path:\n{result!r}"
  )
  print("  PASS: internal_link_relative")


def test_internal_link_with_anchor():
  input_text = "See [section](./safety.md#driver-responsibility)."
  result = resolve_internal_links(
    input_text,
    file_path="safety/index.md",
  )
  # Anchors are stripped — Discourse search cannot target sections
  assert "#driver-responsibility" not in result, f"FAIL anchor should be stripped:\n{result!r}"
  assert "docs-sync-id" in result, f"FAIL missing sync-id:\n{result!r}"
  assert "safety" in result, f"FAIL wrong path:\n{result!r}"
  print("  PASS: internal_link_with_anchor")


def test_internal_link_direct_topic_id():
  input_text = "See [ICBM](../cruise/icbm.md) for details."
  topic_map = {"features/cruise/icbm.md": 244}
  result = resolve_internal_links(
    input_text,
    file_path="features/steering/mads.md",
    topic_id_map=topic_map,
  )
  assert "/t/244" in result, f"FAIL direct_link missing /t/244:\n{result!r}"
  assert "/search?q=" not in result, f"FAIL direct_link should not use search:\n{result!r}"
  print("  PASS: internal_link_direct_topic_id")


def test_internal_link_direct_with_anchor():
  input_text = "See [section](./safety.md#driver-responsibility)."
  topic_map = {"safety/safety.md": 3698}
  result = resolve_internal_links(
    input_text,
    file_path="safety/index.md",
    topic_id_map=topic_map,
  )
  assert "/t/3698#driver-responsibility" in result, (
    f"FAIL direct_link anchor not preserved:\n{result!r}"
  )
  print("  PASS: internal_link_direct_with_anchor")


def test_internal_link_fallback_when_not_in_map():
  input_text = "See [ICBM](../features/cruise/icbm.md) for details."
  topic_map = {}  # Empty map — should fall back to search URL
  result = resolve_internal_links(
    input_text,
    file_path="settings/cruise/speed-limit.md",
    topic_id_map=topic_map,
  )
  assert "/search?q=" in result, f"FAIL fallback should use search:\n{result!r}"
  print("  PASS: internal_link_fallback_when_not_in_map")


def test_external_link_untouched():
  input_text = "Visit [GitHub](https://github.com/sunnypilot/sunnypilot)."
  result = resolve_internal_links(
    input_text,
    file_path="index.md",
  )
  assert result == input_text, f"FAIL external_link:\n{result!r}"
  print("  PASS: external_link_untouched")


# ---------------------------------------------------------------------------
# 7. Clean Blank Lines
# ---------------------------------------------------------------------------


def test_clean_blank_lines():
  input_text = "Line 1\n\n\n\n\nLine 2\n"
  expected = "Line 1\n\n\nLine 2\n"
  result = clean_blank_lines(input_text)
  assert result == expected, f"FAIL clean_blanks:\n{result!r}\n!=\n{expected!r}"
  print("  PASS: clean_blank_lines")


def test_clean_blank_lines_no_change():
  input_text = "Line 1\n\nLine 2\n"
  result = clean_blank_lines(input_text)
  assert result == input_text, f"FAIL clean_blanks_noop:\n{result!r}"
  print("  PASS: clean_blank_lines_no_change")


# ---------------------------------------------------------------------------
# 8. Strip Legacy Footer
# ---------------------------------------------------------------------------


def test_strip_legacy_footer_basic():
  input_text = (
    "Content here.\n\n"
    "---\n\n"
    '<small>This document is version controlled - suggest changes '
    '[on github](https://github.com/sunnypilot/sunnypilot/blob/master/docs_sp/setup/url-method.md).</small>\n'
  )
  result = strip_legacy_footer(input_text)
  assert "<small>" not in result, f"FAIL legacy_footer:\n{result!r}"
  assert "---" not in result, f"FAIL legacy_footer separator:\n{result!r}"
  assert "Content here." in result
  print("  PASS: strip_legacy_footer_basic")


def test_strip_legacy_footer_hyphenated():
  input_text = (
    "Content.\n\n"
    "---\n\n"
    '<small>This document is version-controlled. '
    'Suggest changes [on GitHub](https://example.com).</small>\n'
  )
  result = strip_legacy_footer(input_text)
  assert "<small>" not in result, f"FAIL legacy_footer_hyphen:\n{result!r}"
  assert "---" not in result, f"FAIL legacy_footer separator:\n{result!r}"
  print("  PASS: strip_legacy_footer_hyphenated")


def test_strip_legacy_footer_no_match():
  input_text = "Regular content with <small>other small text</small>.\n"
  result = strip_legacy_footer(input_text)
  assert result == input_text, f"FAIL legacy_footer_noop:\n{result!r}"
  print("  PASS: strip_legacy_footer_no_match")


# ---------------------------------------------------------------------------
# Integration: full convert()
# ---------------------------------------------------------------------------


def test_full_convert():
  input_text = """---
title: Test Doc
---

# Test Document

!!! warning "Important"
    Pay attention to the road.

See [safety info](../safety/safety.md) for more.

:material-check: Feature supported
"""
  result = convert(
    input_text,
    file_path="features/index.md",
  )
  # Front matter stripped
  assert "---\ntitle:" not in result, f"FAIL front matter not stripped:\n{result!r}"
  # Admonition converted
  assert "> [!WARNING] Important" in result, f"FAIL admonition:\n{result!r}"
  assert "> Pay attention to the road." in result, f"FAIL admonition content:\n{result!r}"
  # Link resolved to Discourse search
  assert "/search?q=" in result, f"FAIL link not converted to search:\n{result!r}"
  assert "docs-sync-id" in result, f"FAIL link missing sync-id:\n{result!r}"
  # Emoji converted
  assert ":material-check:" not in result, f"FAIL emoji:\n{result!r}"
  assert "Y Feature supported" in result, f"FAIL emoji replacement:\n{result!r}"
  print("  PASS: full_convert")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


if __name__ == "__main__":
  print("Testing MkDocs -> Discourse converter:")
  tests = [
    # 1. Front matter
    test_strip_front_matter_basic,
    test_strip_front_matter_absent,
    # 2. Admonitions
    test_basic_warning,
    test_info_no_title,
    test_info_with_title,
    test_danger,
    test_tip,
    test_multiline_with_blank,
    test_collapsible,
    test_collapsible_open,
    test_surrounded_by_content,
    test_multiple_admonitions,
    test_real_doc_snippet,
    # 2b. Unescape callout brackets
    test_unescape_callout_basic,
    test_unescape_callout_with_title,
    test_unescape_callout_no_change,
    test_unescape_callout_non_blockquote_untouched,
    # 3. Tabs
    test_tabs_basic,
    test_tabs_multiline,
    # 4. Grid cards
    test_grid_cards_stripped,
    # 5. Emoji
    test_emoji_known,
    test_emoji_unknown_stripped,
    test_emoji_in_grid_card,
    # 6. Internal links
    test_internal_link_relative,
    test_internal_link_with_anchor,
    test_internal_link_direct_topic_id,
    test_internal_link_direct_with_anchor,
    test_internal_link_fallback_when_not_in_map,
    test_external_link_untouched,
    # 7. Blank lines
    test_clean_blank_lines,
    test_clean_blank_lines_no_change,
    # 8. Legacy footer
    test_strip_legacy_footer_basic,
    test_strip_legacy_footer_hyphenated,
    test_strip_legacy_footer_no_match,
    # Integration
    test_full_convert,
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
