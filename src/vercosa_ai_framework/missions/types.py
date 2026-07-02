"""Mission Runner domain types."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class MissionStatus(str, Enum):
    """Allowed Mission Runner states from Spec 0004."""

    QUEUED = "queued"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    CANCELLED = "cancelled"


def utc_now_iso() -> str:
    """Return an auditable UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True, slots=True)
class Mission:
    """Traceable unit of user or system intent."""

    title: str
    goal: str
    mission_id: str = field(default_factory=lambda: str(uuid4()))
    requested_by: str = "user"
    created_at: str = field(default_factory=utc_now_iso)
    workspace: str = "."
    status: MissionStatus = MissionStatus.QUEUED
    priority: int = 100
    spec_refs: tuple[str, ...] = field(default_factory=tuple)
    guardian_refs: tuple[str, ...] = field(default_factory=tuple)
    guardian_mode: str = "standard"
    constraints: dict[str, Any] = field(default_factory=dict)
    acceptance_criteria: tuple[str, ...] = field(default_factory=tuple)
    validation_policy: dict[str, Any] = field(default_factory=dict)
    security_policy: dict[str, Any] = field(default_factory=dict)
    budget_policy: dict[str, Any] = field(default_factory=dict)
    commit_policy: dict[str, Any] = field(default_factory=lambda: {"auto_commit": "disabled"})
    rollback_policy: dict[str, Any] = field(default_factory=lambda: {"mode": "none"})
    execution_limits: dict[str, Any] = field(default_factory=lambda: {"max_cycles": 1})
    audit_log_ref: str | None = None
    queued_at: str | None = None
    started_at: str | None = None
    finished_at: str | None = None
    attempt_count: int = 0
    max_attempts: int = 1
    cycle_count: int = 0
    max_cycles: int = 1
    locked_by: str | None = None
    last_error: str | None = None

    def with_status(self, status: MissionStatus, **changes: Any) -> "Mission":
        """Return a copy with a new status and additional field changes."""

        return replace(self, status=status, **changes)


@dataclass(frozen=True, slots=True)
class MissionResult:
    """Final or partial result for a mission execution cycle."""

    mission_id: str
    status: MissionStatus
    summary: str = ""
    artifacts: tuple[str, ...] = field(default_factory=tuple)
    changed_files: tuple[str, ...] = field(default_factory=tuple)
    validation_results: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
    requires_review: bool = False
    audit_log_ref: str | None = None
