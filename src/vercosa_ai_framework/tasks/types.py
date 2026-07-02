"""Provider-neutral Task Queue contract types.

These contracts model internal Workflow Engine task queue state only. They do
not execute runtimes, call OpenCode, choose concrete models, or contact external
providers.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from enum import Enum, IntEnum
from typing import Any
from uuid import uuid4


def utc_now_iso() -> str:
    """Return an auditable UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


class TaskPriority(IntEnum):
    """Stable queue priorities where lower numeric values run first."""

    CRITICAL = 0
    HIGH = 50
    NORMAL = 100
    LOW = 200


class TaskQueueState(str, Enum):
    """Allowed Task Queue item states from Spec 0007."""

    QUEUED = "queued"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class Task:
    """Operational queue representation of a planned workflow task."""

    title: str
    goal: str
    workflow_id: str
    mission_id: str
    task_id: str = field(default_factory=lambda: str(uuid4()))
    queue_item_id: str = field(default_factory=lambda: str(uuid4()))
    state: TaskQueueState = TaskQueueState.QUEUED
    priority: int = int(TaskPriority.NORMAL)
    dependencies: tuple[str, ...] = field(default_factory=tuple)
    blocked_by: tuple[str, ...] = field(default_factory=tuple)
    task_type: str = "generic"
    risk_level: str = "low"
    required_capabilities: tuple[str, ...] = field(default_factory=tuple)
    context_refs: tuple[str, ...] = field(default_factory=tuple)
    artifact_refs: tuple[str, ...] = field(default_factory=tuple)
    guardian_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    runtime_request_ref: str | None = None
    agent_assignment_ref: str | None = None
    attempt_count: int = 0
    max_attempts: int = 1
    next_attempt_at: str | None = None
    last_error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)
    queued_at: str = field(default_factory=utc_now_iso)
    started_at: str | None = None
    finished_at: str | None = None
    updated_at: str = field(default_factory=utc_now_iso)
    audit_log_ref: str | None = None

    def with_state(self, state: TaskQueueState, **changes: Any) -> "Task":
        """Return a copy with a new queue state and additional field changes."""

        return replace(self, state=state, updated_at=utc_now_iso(), **changes)


@dataclass(frozen=True, slots=True)
class TaskAttempt:
    """Traceable attempt to execute a queued task."""

    task_id: str
    workflow_id: str
    mission_id: str
    attempt_number: int
    attempt_id: str = field(default_factory=lambda: str(uuid4()))
    state: TaskQueueState = TaskQueueState.RUNNING
    started_at: str = field(default_factory=utc_now_iso)
    finished_at: str | None = None
    guardian_decision_ref: str | None = None
    runtime_request_ref: str | None = None
    runtime_result_ref: str | None = None
    error_type: str | None = None
    error_message: str | None = None
    retry_decision: str | None = None
    cost_used: float | None = None
    tokens_used: int | None = None
    audit_log_ref: str | None = None

    def with_state(self, state: TaskQueueState, **changes: Any) -> "TaskAttempt":
        """Return a copy with a new attempt state."""

        return replace(self, state=state, **changes)


@dataclass(frozen=True, slots=True)
class TaskQueueResult:
    """Normalized result for queue operations that change local state."""

    queue_id: str
    workflow_id: str
    mission_id: str
    success: bool
    task: Task | None = None
    attempt: TaskAttempt | None = None
    message: str = ""
    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
