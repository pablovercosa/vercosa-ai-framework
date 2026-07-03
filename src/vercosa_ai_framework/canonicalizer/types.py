"""Canonicalizer contract types.

These contracts are provider agnostic and side-effect free. They do not convert
binary formats, call APIs, invoke subprocesses, or access external runtimes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from typing import Any
from uuid import uuid4


class CanonicalSourceType(str, Enum):
    """Supported source type identifiers for the initial Canonicalizer contract."""

    TEXT = "text"
    MARKDOWN = "markdown"
    PDF = "pdf"
    DOCX = "docx"
    HTML = "html"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    UNKNOWN = "unknown"


class CanonicalizationStatus(str, Enum):
    """Canonicalization result statuses from Spec 0012."""

    SUCCESS = "success"
    BLOCKED = "blocked"
    DUPLICATE = "duplicate"
    PARTIAL = "partial"
    FAILED = "failed"


def utc_now_iso() -> str:
    """Return an auditable UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True, slots=True)
class CanonicalSource:
    """Traceable source metadata for content entering the Canonicalizer."""

    source_uri: str
    source_type: CanonicalSourceType = CanonicalSourceType.UNKNOWN
    domain: str = "unknown"
    source_id: str = field(default_factory=lambda: str(uuid4()))
    title: str | None = None
    language: str = "und"
    sensitivity: str = "public"
    trust_level: str = "unknown"
    source_hash: str | None = None
    size_bytes: int | None = None
    provenance: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)


@dataclass(frozen=True, slots=True)
class CanonicalMetadata:
    """Metadata and policy envelope attached to canonicalized content."""

    domain: str = "unknown"
    title: str = ""
    language: str = "und"
    sensitivity: str = "public"
    trust_level: str = "unknown"
    usage_policy: dict[str, Any] = field(default_factory=dict)
    privacy_policy: dict[str, Any] = field(default_factory=dict)
    conversion_policy: dict[str, Any] = field(default_factory=dict)
    redaction_policy: dict[str, Any] = field(default_factory=dict)
    deduplication_policy: dict[str, Any] = field(default_factory=dict)
    tags: tuple[str, ...] = field(default_factory=tuple)
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class CanonicalDocument:
    """Canonical Markdown representation of a source document."""

    document_id: str
    content: str
    source_uri: str
    source_type: CanonicalSourceType
    domain: str
    title: str
    canonical_uri: str | None = None
    version: str = "1"
    content_hash: str = ""
    source_hash: str | None = None
    canonical_format: str = "markdown"
    language: str = "und"
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)
    canonicalized_at: str = field(default_factory=utc_now_iso)
    sensitivity: str = "public"
    trust_level: str = "unknown"
    frontmatter: dict[str, Any] = field(default_factory=dict)
    metadata: CanonicalMetadata = field(default_factory=CanonicalMetadata)
    provenance: dict[str, Any] = field(default_factory=dict)
    conversion_confidence: float = 1.0
    warnings: tuple[str, ...] = field(default_factory=tuple)
    redactions_applied: tuple[str, ...] = field(default_factory=tuple)
    prompt_injection_warnings: tuple[str, ...] = field(default_factory=tuple)
    guardian_decision_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.canonical_format != "markdown":
            raise ValueError("canonical_format must be markdown for the initial Canonicalizer contract")
        if not self.content_hash:
            object.__setattr__(self, "content_hash", canonical_content_hash(self.content))


@dataclass(frozen=True, slots=True)
class CanonicalizationRequest:
    """Governed request to transform a source into a CanonicalDocument."""

    source: CanonicalSource
    request_id: str = field(default_factory=lambda: str(uuid4()))
    mission_id: str | None = None
    title_hint: str | None = None
    language_hint: str | None = None
    sensitivity_hint: str | None = None
    trust_level_hint: str | None = None
    usage_policy: dict[str, Any] = field(default_factory=dict)
    privacy_policy: dict[str, Any] = field(default_factory=dict)
    conversion_policy: dict[str, Any] = field(default_factory=dict)
    redaction_policy: dict[str, Any] = field(default_factory=dict)
    deduplication_policy: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    guardian_decision_refs: tuple[str, ...] = field(default_factory=tuple)

    @property
    def source_uri(self) -> str:
        """Return the requested source URI for audit-friendly access."""

        return self.source.source_uri

    @property
    def source_type(self) -> CanonicalSourceType:
        """Return the requested source type."""

        return self.source.source_type

    @property
    def domain(self) -> str:
        """Return the requested source domain."""

        return self.source.domain


@dataclass(frozen=True, slots=True)
class CanonicalizationResult:
    """Traceable result returned by a CanonicalizerAdapter."""

    request_id: str
    status: CanonicalizationStatus
    document: CanonicalDocument | None = None
    duplicate_of: str | None = None
    content_hash: str | None = None
    source_hash: str | None = None
    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
    redactions_applied: tuple[str, ...] = field(default_factory=tuple)
    prompt_injection_warnings: tuple[str, ...] = field(default_factory=tuple)
    conversion_confidence: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
    provenance: dict[str, Any] = field(default_factory=dict)
    guardian_decision_refs: tuple[str, ...] = field(default_factory=tuple)

    @property
    def success(self) -> bool:
        """Return whether canonicalization produced a usable document."""

        return self.status == CanonicalizationStatus.SUCCESS and self.document is not None

    @property
    def blocked(self) -> bool:
        """Return whether canonicalization was blocked by policy or validation."""

        return self.status == CanonicalizationStatus.BLOCKED


def canonical_content_hash(content: str) -> str:
    """Return a stable SHA-256 hash for canonical Markdown content."""

    return sha256(content.encode("utf-8")).hexdigest()


__all__ = [
    "CanonicalDocument",
    "CanonicalMetadata",
    "CanonicalSource",
    "CanonicalSourceType",
    "CanonicalizationRequest",
    "CanonicalizationResult",
    "CanonicalizationStatus",
    "canonical_content_hash",
]
