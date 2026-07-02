"""Provider-neutral runtime contract types.

These types describe the boundary between the framework core and any concrete
execution runtime. They intentionally do not mention OpenCode so the core can
support other runtimes through adapters.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from vercosa_ai_framework.model_selection import SelectionDecision


class RuntimeStatus(str, Enum):
    """Normalized lifecycle states reported by runtime adapters."""

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    PREPARED = "prepared"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    STOPPED = "stopped"


@dataclass(frozen=True, slots=True)
class RuntimeCapability:
    """Capability detected or declared by a runtime."""

    name: str
    available: bool = True
    limitations: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RuntimeInfo:
    """Normalized runtime detection result."""

    runtime_id: str
    runtime_name: str
    available: bool
    runtime_version: str | None = None
    capabilities: tuple[RuntimeCapability, ...] = field(default_factory=tuple)
    limitations: tuple[str, ...] = field(default_factory=tuple)
    security_warnings: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class RuntimeExecutionRequest:
    """Governed request passed into a Runtime Adapter."""

    mission_id: str
    workspace: str
    workflow_id: str | None = None
    task_id: str | None = None
    context: dict[str, Any] = field(default_factory=dict)
    permissions: dict[str, Any] = field(default_factory=dict)
    execution_limits: dict[str, Any] = field(default_factory=dict)
    selection_decision: SelectionDecision | None = None
    logging_policy: dict[str, Any] = field(default_factory=dict)
    approval_policy: dict[str, Any] = field(default_factory=dict)
    plugin_policy: dict[str, Any] = field(default_factory=dict)
    fallback_policy: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RuntimeExecutionPlan:
    """Prepared execution details after policy constraints are applied."""

    mission_id: str
    workspace: str
    workflow_id: str | None = None
    task_id: str | None = None
    selected_provider: str | None = None
    selected_model: str | None = None
    context_included: tuple[str, ...] = field(default_factory=tuple)
    permissions_granted: dict[str, Any] = field(default_factory=dict)
    plugins_allowed: tuple[str, ...] = field(default_factory=tuple)
    limits_applied: dict[str, Any] = field(default_factory=dict)
    approvals_required: tuple[str, ...] = field(default_factory=tuple)
    blocked_reasons: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class RuntimeExecutionResult:
    """Normalized result emitted by a Runtime Adapter."""

    mission_id: str
    runtime_id: str
    status: RuntimeStatus
    workflow_id: str | None = None
    task_id: str | None = None
    selected_provider: str | None = None
    selected_model: str | None = None
    small_model_used: bool = False
    fallback_used: bool = False
    artifacts: tuple[str, ...] = field(default_factory=tuple)
    changed_files: tuple[str, ...] = field(default_factory=tuple)
    commands_executed: tuple[str, ...] = field(default_factory=tuple)
    tests_executed: tuple[str, ...] = field(default_factory=tuple)
    validation_results: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
    requires_review: bool = False
    audit_log_ref: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
