"""Local Markdown ingestion helpers for the Knowledge Hub MVP.

This module is intentionally local, deterministic, and dependency-free. It
does not generate embeddings, access databases, call APIs, or execute commands.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from vercosa_ai_framework.knowledge.store import InMemoryKnowledgeStore, KnowledgeStore
from vercosa_ai_framework.knowledge.types import KnowledgeDocument, KnowledgeDomain, KnowledgeSource, split_frontmatter


PROMPT_INJECTION_WARNING = "knowledge.prompt_injection.suspicious_content"

_PROMPT_INJECTION_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions\b", re.I),
    re.compile(r"\bdisregard\s+(?:all\s+)?(?:previous|prior|above)\s+instructions\b", re.I),
    re.compile(r"\breveal\s+(?:the\s+)?(?:system|developer)\s+(?:prompt|message|instructions)\b", re.I),
    re.compile(r"\b(?:system|developer)\s+(?:prompt|message)\s*:", re.I),
    re.compile(r"\b(?:override|bypass)\s+(?:policy|policies|spec|specs|guardian|security)\b", re.I),
    re.compile(r"\b(?:exfiltrate|leak|send)\s+(?:secrets?|tokens?|credentials?)\b", re.I),
    re.compile(r"\brun\s+(?:this\s+)?command\b", re.I),
)


def read_markdown_file(path: str | Path, *, encoding: str = "utf-8") -> str:
    """Read a local Markdown file as text.

    The caller supplies the path explicitly. No provider, database, API, or
    subprocess is used.
    """

    return Path(path).read_text(encoding=encoding)


def parse_markdown_frontmatter(markdown: str) -> tuple[dict[str, Any], str]:
    """Extract simple YAML frontmatter from Markdown text."""

    return split_frontmatter(markdown)


def detect_prompt_injection_warnings(markdown: str) -> tuple[str, ...]:
    """Return deterministic warning IDs for suspicious document instructions."""

    if any(pattern.search(markdown) for pattern in _PROMPT_INJECTION_PATTERNS):
        return (PROMPT_INJECTION_WARNING,)
    return ()


def markdown_to_document(
    markdown: str,
    *,
    document_id: str | None = None,
    source_uri: str | None = None,
    domain: KnowledgeDomain | str | None = None,
    tags: tuple[str, ...] = (),
    metadata: dict[str, Any] | None = None,
) -> KnowledgeDocument:
    """Create a canonical KnowledgeDocument from Markdown text."""

    frontmatter, _content = parse_markdown_frontmatter(markdown)
    resolved_domain = _resolve_domain(domain or frontmatter.get("domain"))
    warnings = detect_prompt_injection_warnings(markdown)
    merged_metadata: dict[str, Any] = dict(metadata or {})
    if warnings:
        merged_metadata["warnings"] = tuple(dict.fromkeys((*_metadata_warnings(merged_metadata), *warnings)))
        merged_metadata["prompt_injection_suspected"] = True

    source = KnowledgeSource(
        source_uri=source_uri or str(frontmatter.get("source_uri") or ""),
        source_type=str(frontmatter.get("source_type") or "markdown"),
        domain=resolved_domain,
        title=str(frontmatter.get("title") or "") or None,
        version=str(frontmatter.get("version") or "1"),
        language=str(frontmatter.get("language") or "und"),
        sensitivity=str(frontmatter.get("sensitivity") or "public"),
        trust_level=str(frontmatter.get("trust_level") or "unknown"),
        tags=tags,
    )
    document = KnowledgeDocument.from_markdown(
        markdown,
        document_id=document_id,
        domain=resolved_domain,
        source=source,
        tags=tags,
        metadata=merged_metadata,
    )
    return document


def load_markdown_document(
    path: str | Path,
    *,
    document_id: str | None = None,
    domain: KnowledgeDomain | str | None = None,
    tags: tuple[str, ...] = (),
    metadata: dict[str, Any] | None = None,
    encoding: str = "utf-8",
) -> KnowledgeDocument:
    """Read a local Markdown file and return a KnowledgeDocument."""

    local_path = Path(path)
    markdown = read_markdown_file(local_path, encoding=encoding)
    return markdown_to_document(
        markdown,
        document_id=document_id,
        source_uri=str(local_path),
        domain=domain,
        tags=tags,
        metadata=metadata,
    )


def ingest_markdown_file(
    path: str | Path,
    store: KnowledgeStore | None = None,
    *,
    document_id: str | None = None,
    domain: KnowledgeDomain | str | None = None,
    tags: tuple[str, ...] = (),
    metadata: dict[str, Any] | None = None,
    encoding: str = "utf-8",
) -> KnowledgeDocument:
    """Read, canonicalize, and index a local Markdown file in a KnowledgeStore."""

    target_store = store or InMemoryKnowledgeStore()
    document = load_markdown_document(
        path,
        document_id=document_id,
        domain=domain,
        tags=tags,
        metadata=metadata,
        encoding=encoding,
    )
    return target_store.add_document(document)


def _resolve_domain(value: KnowledgeDomain | str | None) -> KnowledgeDomain:
    if isinstance(value, KnowledgeDomain):
        return value
    if value is None:
        return KnowledgeDomain.UNKNOWN
    try:
        return KnowledgeDomain(str(value))
    except ValueError:
        return KnowledgeDomain.UNKNOWN


def _metadata_warnings(metadata: dict[str, Any]) -> tuple[str, ...]:
    value = metadata.get("warnings", ())
    if isinstance(value, str):
        return (value,)
    if isinstance(value, tuple | list | set):
        return tuple(str(item) for item in value)
    return ()


__all__ = [
    "PROMPT_INJECTION_WARNING",
    "detect_prompt_injection_warnings",
    "ingest_markdown_file",
    "load_markdown_document",
    "markdown_to_document",
    "parse_markdown_frontmatter",
    "read_markdown_file",
]
