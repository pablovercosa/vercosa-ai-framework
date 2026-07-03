"""Persistence Layer public contracts."""

from vercosa_ai_framework.persistence.filesystem import FilesystemRepository
from vercosa_ai_framework.persistence.repository import Repository
from vercosa_ai_framework.persistence.types import (
    EntityRef,
    PersistedRecord,
    PersistenceResult,
    QueryFilter,
)

__all__ = [
    "EntityRef",
    "FilesystemRepository",
    "PersistedRecord",
    "PersistenceResult",
    "QueryFilter",
    "Repository",
]
