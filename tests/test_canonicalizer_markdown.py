from __future__ import annotations

from vercosa_ai_framework.canonicalizer.markdown import (
    FRONTMATTER_WARNING,
    canonicalize_markdown_text,
    extract_title,
    normalize_title,
    split_markdown_frontmatter,
    text_to_markdown,
)


def test_split_markdown_frontmatter_parses_simple_yaml_without_dependency():
    frontmatter, body, warnings = split_markdown_frontmatter(
        """---
document_id: doc-1
domain: docs
title: Canonical Docs
rag_allowed: true
tags: [canonicalizer, markdown]
---
# Canonical Docs
"""
    )

    assert warnings == ()
    assert frontmatter["document_id"] == "doc-1"
    assert frontmatter["rag_allowed"] is True
    assert frontmatter["tags"] == ("canonicalizer", "markdown")
    assert body == "# Canonical Docs\n"


def test_split_markdown_frontmatter_warns_on_unclosed_block():
    frontmatter, body, warnings = split_markdown_frontmatter("---\ntitle: Broken\n# Body\n")

    assert frontmatter == {}
    assert body == "---\ntitle: Broken\n# Body\n"
    assert warnings == (FRONTMATTER_WARNING,)


def test_canonicalize_markdown_text_normalizes_line_endings_and_spacing():
    assert canonicalize_markdown_text("# Title\r\n\r\n\r\nBody\x00  \r\n") == "# Title\n\n\nBody\n"


def test_text_to_markdown_keeps_plain_text_as_canonical_markdown():
    assert text_to_markdown("Title\n\nBody") == "Title\n\nBody\n"


def test_extract_title_prefers_h1_then_first_useful_line():
    assert extract_title("# Main Title\n\nBody") == ("Main Title", "heading")
    assert extract_title("Plain title\nBody") == ("Plain title", "first_line")


def test_normalize_title_removes_markdown_and_control_characters():
    assert normalize_title("# **Title**\x00\nMore") == "Title More"
