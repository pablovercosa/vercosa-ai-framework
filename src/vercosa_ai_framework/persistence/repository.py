"""Persistence repository abstract contract."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic

from vercosa_ai_framework.persistence.types import (
    EntityRef,
    PayloadT,
    PersistedRecord,
    PersistenceResult,
    QueryFilter,
)


class Repository(Generic[PayloadT], ABC):
    """Abstract storage-agnostic repository port for persisted records."""

    @abstractmethod
    def save(self, record: PersistedRecord[PayloadT]) -> PersistenceResult[PayloadT]:
        """Persist or update a record through an adapter implementation."""

    @abstractmethod
    def get(self, ref: EntityRef) -> PersistedRecord[PayloadT] | None:
        """Return a record by reference, or None when it is not present."""

    @abstractmethod
    def list(self, query_filter: QueryFilter | None = None) -> tuple[PersistedRecord[PayloadT], ...]:
        """Return records matching a storage-agnostic filter."""

    @abstractmethod
    def delete(self, ref: EntityRef) -> PersistenceResult[PayloadT]:
        """Delete or tombstone a record through an adapter implementation."""


__all__ = ["Repository"]
