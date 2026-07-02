"""Provider-neutral Workflow Engine contract types.

These contracts represent workflow plans and task results only. They do not
execute agents, call runtimes, choose concrete models, or contact providers.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class WorkflowStatus(str, Enum):
    """Allowed workflow states from Spec 0006."""

    DRAFT = "draft"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    REPLANNING = "replanning"
    DONE = "done"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskStatus(str, Enum):
    """Allowed task states from Spec 0006."""

    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    BLOCKED = "blocked"
    VALIDATING = "validating"
    DONE = "done"
    FAILED = "failed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"


def utc_now_iso() -> str:
    """Return an auditable UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True, slots=True)
class TaskDependency:
    """Traceable dependency between workflow tasks or artifacts."""

    dependency_type: str
    target_ref: str
    reason: str = ""
    required: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class WorkflowTask:
    """Small, traceable, validable unit of planned workflow work."""

    title: str
    goal: str
    workflow_id: str
    mission_id: str
    task_id: str = field(default_factory=lambda: str(uuid4()))
    task_type: str = "generic"
    status: TaskStatus = TaskStatus.PENDING
    inputs: dict[str, Any] = field(default_factory=dict)
    expected_outputs: tuple[str, ...] = field(default_factory=tuple)
    acceptance_criteria: tuple[str, ...] = field(default_factory=tuple)
    dependencies: tuple[TaskDependency, ...] = field(default_factory=tuple)
    blocked_by: tuple[str, ...] = field(default_factory=tuple)
    priority: int = 100
    risk_level: str = "low"
    required_capabilities: tuple[str, ...] = field(default_factory=tuple)
    model_policy: dict[str, Any] = field(default_factory=dict)
    execution_limits: dict[str, Any] = field(default_factory=dict)
    retry_policy: dict[str, Any] = field(default_factory=lambda: {"max_attempts": 1})
    validation_policy: dict[str, Any] = field(default_factory=dict)
    assigned_agent_ref: str | None = None
    artifacts: tuple[str, ...] = field(default_factory=tuple)
    attempt_count: int = 0
    last_error: str | None = None
    audit_log_ref: str | None = None
    created_at: str = field(default_factory=utc_now_iso)
    started_at: str | None = None
    finished_at: str | None = None

    def with_status(self, status: TaskStatus, **changes: Any) -> "WorkflowTask":
        """Return a copy with a new status and additional field changes."""

        return replace(self, status=status, **changes)


@dataclass(frozen=True, slots=True)
class Workflow:
    """Auditable workflow plan derived from a mission."""

    mission_id: str
    title: str
    goal: str
    workflow_id: str = field(default_factory=lambda: str(uuid4()))
    status: WorkflowStatus = WorkflowStatus.DRAFT
    spec_refs: tuple[str, ...] = field(default_factory=tuple)
    guardian_refs: tuple[str, ...] = field(default_factory=tuple)
    policy_refs: tuple[str, ...] = field(default_factory=tuple)
    tasks: tuple[WorkflowTask, ...] = field(default_factory=tuple)
    dependency_graph: dict[str, tuple[str, ...]] = field(default_factory=dict)
    execution_mode: str = "sequential"
    execution_limits: dict[str, Any] = field(default_factory=lambda: {"max_parallel_tasks": 1})
    budget_policy: dict[str, Any] = field(default_factory=dict)
    validation_policy: dict[str, Any] = field(default_factory=dict)
    retry_policy: dict[str, Any] = field(default_factory=lambda: {"max_replans": 0})
    created_at: str = field(default_factory=utc_now_iso)
    started_at: str | None = None
    finished_at: str | None = None
    audit_log_ref: str | None = None

    def with_status(self, status: WorkflowStatus, **changes: Any) -> "Workflow":
        """Return a copy with a new status and additional field changes."""

        return replace(self, status=status, **changes)


@dataclass(frozen=True, slots=True)
class TaskResult:
    """Final or partial result returned for a workflow task."""

    task_id: str
    workflow_id: str
    mission_id: str
    status: TaskStatus
    summary: str = ""
    artifacts: tuple[str, ...] = field(default_factory=tuple)
    validation_results: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
    requires_review: bool = False
    audit_log_ref: str | None = None


@dataclass(frozen=True, slots=True)
class WorkflowResult:
    """Final or partial result for a workflow execution cycle."""

    workflow_id: str
    mission_id: str
    status: WorkflowStatus
    summary: str = ""
    task_results: tuple[TaskResult, ...] = field(default_factory=tuple)
    artifacts: tuple[str, ...] = field(default_factory=tuple)
    validation_results: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
    closure_recommendation: str = "review"
    requires_review: bool = False
    audit_log_ref: str | None = None
