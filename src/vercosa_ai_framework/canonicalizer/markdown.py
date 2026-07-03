"""Markdown normalization helpers for the Canonicalizer MVP.

The helpers are deterministic and dependency-free. They parse only a small,
auditable YAML frontmatter subset and never call external APIs or converters.
"""

from __future__ import annotations

import re
from typing import Any


FRONTMATTER_WARNING = "canonicalizer.frontmatter.invalid"

_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_H1_PATTERN = re.compile(r"^#\s+(.+?)\s*#*\s*$", re.M)


def split_markdown_frontmatter(markdown: str) -> tuple[dict[str, Any], str, tuple[str, ...]]:
    """Return simple YAML frontmatter, body, and parsing warnings."""

    normalized = normalize_line_endings(markdown)
    lines = normalized.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, normalized, ()

    end_index = next((index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"), None)
    if end_index is None:
        return {}, normalized, (FRONTMATTER_WARNING,)

    frontmatter, warnings = parse_simple_yaml(lines[1:end_index])
    body = "\n".join(lines[end_index + 1 :])
    return frontmatter, body, warnings


def parse_simple_yaml(lines: list[str]) -> tuple[dict[str, Any], tuple[str, ...]]:
    """Parse a conservative YAML subset: scalar key/value pairs and inline lists."""

    metadata: dict[str, Any] = {}
    warnings: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped or stripped.startswith("-"):
            warnings.append(FRONTMATTER_WARNING)
            continue
        key, raw_value = stripped.split(":", 1)
        clean_key = key.strip()
        if not clean_key:
            warnings.append(FRONTMATTER_WARNING)
            continue
        metadata[clean_key] = _parse_scalar(raw_value.strip())
    return metadata, tuple(dict.fromkeys(warnings))


def canonicalize_markdown_text(markdown: str) -> str:
    """Normalize Markdown body text without changing document semantics aggressively."""

    text = normalize_line_endings(markdown)
    text = remove_unsafe_control_chars(text)
    lines = [line.rstrip() for line in text.split("\n")]

    collapsed: list[str] = []
    blank_count = 0
    for line in lines:
        if line.strip():
            blank_count = 0
            collapsed.append(line)
            continue
        blank_count += 1
        if blank_count <= 2:
            collapsed.append("")

    return "\n".join(collapsed).strip() + "\n"


def text_to_markdown(text: str) -> str:
    """Convert plain text to minimal canonical Markdown."""

    return canonicalize_markdown_text(text)


def normalize_title(value: object) -> str:
    """Return a safe plain-text title candidate."""

    title = remove_unsafe_control_chars(str(value or ""))
    title = re.sub(r"[`*_#\[\]()>]", "", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title[:160]


def extract_title(markdown: str, *, fallback: str = "Untitled") -> tuple[str, str]:
    """Extract a title from the first H1 or first useful text line."""

    match = _H1_PATTERN.search(markdown)
    if match:
        title = normalize_title(match.group(1))
        if title:
            return title, "heading"

    for line in markdown.splitlines():
        stripped = normalize_title(line)
        if stripped and not stripped.startswith("---"):
            return stripped, "first_line"
    return fallback, "fallback"


def normalize_line_endings(text: str) -> str:
    """Normalize text to Unix line endings."""

    return text.replace("\r\n", "\n").replace("\r", "\n")


def remove_unsafe_control_chars(text: str) -> str:
    """Remove null bytes and unsafe control characters while preserving tabs/newlines."""

    return _CONTROL_CHARS.sub("", text)


def _parse_scalar(value: str) -> Any:
    if value in {"", "null", "Null", "NULL", "~"}:
        return None
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if value.startswith("[") and value.endswith("]"):
        return tuple(part.strip().strip("'\"") for part in value[1:-1].split(",") if part.strip())
    try:
        return int(value)
    except ValueError:
        return value.strip("'\"")


__all__ = [
    "FRONTMATTER_WARNING",
    "canonicalize_markdown_text",
    "extract_title",
    "normalize_line_endings",
    "normalize_title",
    "parse_simple_yaml",
    "remove_unsafe_control_chars",
    "split_markdown_frontmatter",
    "text_to_markdown",
]
