"""Persistence Layer contract types.

These types describe storage-agnostic records and operation results only. They
do not access files, databases, providers, APIs, subprocesses, or runtimes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Generic, TypeVar
from uuid import uuid4


PayloadT = TypeVar("PayloadT")


def utc_now_iso() -> str:
    """Return an auditable UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True, slots=True)
class EntityRef:
    """Storage-agnostic reference to a domain entity or persisted record."""

    entity_type: str
    entity_id: str
    record_id: str | None = None
    schema_version: str = "1"
    content_hash: str | None = None


@dataclass(frozen=True, slots=True)
class PersistedRecord(Generic[PayloadT]):
    """Versioned, traceable envelope for a persisted domain payload."""

    record_type: str
    entity_ref: EntityRef
    payload: PayloadT
    record_id: str = field(default_factory=lambda: str(uuid4()))
    schema_version: str = "1"
    parent_refs: tuple[EntityRef, ...] = field(default_factory=tuple)
    content_hash: str | None = None
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)
    created_by: str | None = None
    updated_by: str | None = None
    sensitivity: str = "public"
    redactions_applied: tuple[str, ...] = field(default_factory=tuple)
    guardian_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    audit_log_refs: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def entity_id(self) -> str:
        """Return the referenced domain entity ID."""

        return self.entity_ref.entity_id

    @property
    def entity_type(self) -> str:
        """Return the referenced domain entity type."""

        return self.entity_ref.entity_type

    def ref(self) -> EntityRef:
        """Return a stable reference to this persisted record."""

        return EntityRef(
            entity_type=self.entity_type,
            entity_id=self.entity_id,
            record_id=self.record_id,
            schema_version=self.schema_version,
            content_hash=self.content_hash,
        )


@dataclass(frozen=True, slots=True)
class PersistenceResult(Generic[PayloadT]):
    """Normalized result for repository operations."""

    success: bool
    operation: str
    ref: EntityRef | None = None
    record: PersistedRecord[PayloadT] | None = None
    message: str = ""
    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
    audit_log_refs: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class QueryFilter:
    """Simple provider-neutral filter for listing persisted records."""

    record_type: str | None = None
    entity_type: str | None = None
    entity_id: str | None = None
    parent_ref: EntityRef | None = None
    schema_version: str | None = None
    sensitivity: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    limit: int | None = None
    offset: int = 0

    def __post_init__(self) -> None:
        if self.limit is not None and self.limit < 0:
            raise ValueError("query filter limit must be non-negative")
        if self.offset < 0:
            raise ValueError("query filter offset must be non-negative")


__all__ = [
    "EntityRef",
    "PayloadT",
    "PersistedRecord",
    "PersistenceResult",
    "QueryFilter",
    "utc_now_iso",
]
