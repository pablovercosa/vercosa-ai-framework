"""Knowledge Hub contract types.

These initial contracts are text-only and provider agnostic. They do not create
embeddings, call APIs, access databases, invoke providers, or use subprocesses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from typing import Any
from uuid import uuid4


class KnowledgeDomain(str, Enum):
    """Initial Knowledge Hub domains from Spec 0011."""

    SPECS = "specs"
    ADRS = "adrs"
    DOCS = "docs"
    CODE = "code"
    LEGAL = "legal"
    BOOKS = "books"
    CONVERSATIONS = "conversations"
    DECISIONS = "decisions"
    PROJECTS = "projects"
    AGENTS = "agents"
    SKILLS = "skills"
    COMMANDS = "commands"
    HOOKS = "hooks"
    GUARDIAN = "guardian"
    ARCHITECTURE = "architecture"
    UNKNOWN = "unknown"


def utc_now_iso() -> str:
    """Return an auditable UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True, slots=True)
class KnowledgeSource:
    """Declarative source metadata for knowledge that can be canonicalized."""

    source_uri: str
    source_type: str
    domain: KnowledgeDomain = KnowledgeDomain.UNKNOWN
    source_id: str = field(default_factory=lambda: str(uuid4()))
    title: str | None = None
    version: str | None = None
    language: str = "und"
    sensitivity: str = "public"
    trust_level: str = "unknown"
    usage_policy: dict[str, Any] = field(default_factory=dict)
    provenance: dict[str, Any] = field(default_factory=dict)
    tags: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)


@dataclass(frozen=True, slots=True)
class KnowledgeDocument:
    """Canonical Markdown document stored by the Knowledge Hub."""

    document_id: str
    content: str
    domain: KnowledgeDomain = KnowledgeDomain.UNKNOWN
    title: str = ""
    source: KnowledgeSource | None = None
    canonical_uri: str | None = None
    source_uri: str | None = None
    source_type: str = "markdown"
    version: str = "1"
    canonical_format: str = "markdown"
    language: str = "und"
    sensitivity: str = "public"
    trust_level: str = "unknown"
    frontmatter: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    provenance: dict[str, Any] = field(default_factory=dict)
    tags: tuple[str, ...] = field(default_factory=tuple)
    redactions_applied: tuple[str, ...] = field(default_factory=tuple)
    guardian_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    content_hash: str = ""
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)
    ingested_at: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        if not self.content_hash:
            object.__setattr__(self, "content_hash", content_hash(self.content))
        if self.source is not None:
            if self.source_uri is None:
                object.__setattr__(self, "source_uri", self.source.source_uri)
            if self.source_type == "markdown" and self.source.source_type:
                object.__setattr__(self, "source_type", self.source.source_type)

    @classmethod
    def from_markdown(
        cls,
        markdown: str,
        *,
        document_id: str | None = None,
        domain: KnowledgeDomain | str | None = None,
        source: KnowledgeSource | None = None,
        tags: tuple[str, ...] = (),
        metadata: dict[str, Any] | None = None,
    ) -> "KnowledgeDocument":
        """Build a KnowledgeDocument from Markdown and optional frontmatter."""

        frontmatter, content = split_frontmatter(markdown)
        resolved_domain = _domain_from(domain or frontmatter.get("domain") or (source.domain if source else None))
        resolved_tags = _tuple_of_strings(tags or _metadata_tags(frontmatter))
        merged_metadata = {**frontmatter, **(metadata or {})}
        return cls(
            document_id=str(document_id or frontmatter.get("document_id") or uuid4()),
            content=content,
            domain=resolved_domain,
            title=str(frontmatter.get("title") or (source.title if source else "") or ""),
            source=source,
            source_type=str(frontmatter.get("source_type") or (source.source_type if source else "markdown")),
            version=str(frontmatter.get("version") or (source.version if source and source.version else "1")),
            language=str(frontmatter.get("language") or (source.language if source else "und")),
            sensitivity=str(frontmatter.get("sensitivity") or (source.sensitivity if source else "public")),
            trust_level=str(frontmatter.get("trust_level") or (source.trust_level if source else "unknown")),
            frontmatter=frontmatter,
            metadata=merged_metadata,
            tags=resolved_tags,
        )

    def has_tags(self, tags: tuple[str, ...]) -> bool:
        """Return whether all requested tags are present in the document."""

        document_tags = set(self.tags) | set(_metadata_tags(self.frontmatter)) | set(_metadata_tags(self.metadata))
        return all(tag in document_tags for tag in tags)


@dataclass(frozen=True, slots=True)
class KnowledgeQuery:
    """Text and metadata query for Knowledge Hub retrieval."""

    query_text: str = ""
    domains: tuple[KnowledgeDomain, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    source_types: tuple[str, ...] = field(default_factory=tuple)
    filters: dict[str, Any] = field(default_factory=dict)
    top_k: int = 10
    token_budget: int | None = None
    ranking_policy: str = "text_match"
    sensitivity_allowed: tuple[str, ...] = ("public", "internal")
    trust_level_min: str | None = None
    include_citations: bool = True
    mission_id: str | None = None
    task_id: str | None = None
    guardian_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    query_id: str = field(default_factory=lambda: str(uuid4()))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class KnowledgeSearchResult:
    """Traceable search result returned by a KnowledgeStore."""

    query_id: str
    domain: KnowledgeDomain
    document_id: str
    title: str
    snippet: str
    score: float
    rank: int
    result_id: str = field(default_factory=lambda: str(uuid4()))
    chunk_id: str | None = None
    citations: tuple[str, ...] = field(default_factory=tuple)
    source_uri: str | None = None
    content_hash: str | None = None
    sensitivity: str = "public"
    trust_level: str = "unknown"
    warnings: tuple[str, ...] = field(default_factory=tuple)
    redactions_applied: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)


def content_hash(content: str) -> str:
    """Return a stable SHA-256 hash for canonical text content."""

    return sha256(content.encode("utf-8")).hexdigest()


def split_frontmatter(markdown: str) -> tuple[dict[str, Any], str]:
    """Extract a small YAML frontmatter subset from Markdown text."""

    lines = markdown.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, markdown
    end_index = next((index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"), None)
    if end_index is None:
        return {}, markdown
    metadata = _parse_simple_yaml(lines[1:end_index])
    content = "\n".join(lines[end_index + 1 :])
    if markdown.endswith("\n") and content:
        content += "\n"
    return metadata, content


def _parse_simple_yaml(lines: list[str]) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, raw_value = stripped.split(":", 1)
        metadata[key.strip()] = _parse_scalar(raw_value.strip())
    return metadata


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


def _metadata_tags(metadata: dict[str, Any]) -> tuple[str, ...]:
    value = metadata.get("tags", ())
    return _tuple_of_strings(value)


def _tuple_of_strings(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, tuple | list | set):
        return tuple(str(item) for item in value)
    return (str(value),)


def _domain_from(value: KnowledgeDomain | str | None) -> KnowledgeDomain:
    if isinstance(value, KnowledgeDomain):
        return value
    if value is None:
        return KnowledgeDomain.UNKNOWN
    try:
        return KnowledgeDomain(str(value))
    except ValueError:
        return KnowledgeDomain.UNKNOWN


__all__ = [
    "KnowledgeDocument",
    "KnowledgeDomain",
    "KnowledgeQuery",
    "KnowledgeSearchResult",
    "KnowledgeSource",
    "content_hash",
    "split_frontmatter",
]
