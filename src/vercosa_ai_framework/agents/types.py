"""Provider-neutral Agent Orchestrator contract types.

These contracts describe agent profiles, requests, and normalized results only.
They do not execute OpenCode, call providers, invoke MCPs, resolve tools, or use
subprocesses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


def utc_now_iso() -> str:
    """Return an auditable UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


class AgentRole(str, Enum):
    """Framework-level agent roles independent from any concrete runtime."""

    GENERAL = "general"
    ARCHITECT = "architect"
    IMPLEMENTATION_ARCHITECT = "implementation_architect"
    DEVELOPER = "developer"
    REVIEWER = "reviewer"
    SECURITY_REVIEWER = "security_reviewer"
    TESTER = "tester"
    DOCUMENTATION = "documentation"


class AgentMode(str, Enum):
    """Allowed execution modes for agent assignments."""

    PRIMARY = "primary"
    SUBAGENT = "subagent"
    REVIEW = "review"
    VALIDATION = "validation"


class AgentState(str, Enum):
    """Agent Assignment state machine states from Spec 0008."""

    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    REFLECTING = "reflecting"
    VALIDATING = "validating"
    REPLANNING = "replanning"
    DONE = "done"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class AgentProfile:
    """Static profile used by the Agent Orchestrator to select an agent."""

    role: AgentRole
    domain: str
    supported_task_types: tuple[str, ...]
    supported_capabilities: tuple[str, ...]
    agent_profile_id: str = field(default_factory=lambda: str(uuid4()))
    modes: tuple[AgentMode, ...] = (AgentMode.PRIMARY,)
    tags: tuple[str, ...] = field(default_factory=tuple)
    complexity_range: tuple[str, ...] = ("low", "medium")
    risk_range: tuple[str, ...] = ("low", "medium")
    default_model_policy: dict[str, Any] = field(default_factory=dict)
    default_execution_limits: dict[str, Any] = field(default_factory=dict)
    allowed_delegations: tuple[AgentRole, ...] = field(default_factory=tuple)
    validation_requirements: tuple[str, ...] = field(default_factory=tuple)
    security_profile: dict[str, Any] = field(default_factory=dict)
    runtime_constraints: dict[str, Any] = field(default_factory=dict)
    audit_log_ref: str | None = None
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def supports_capabilities(self, required_capabilities: tuple[str, ...]) -> bool:
        """Return whether all required capabilities are declared by the profile."""

        supported = set(self.supported_capabilities)
        return all(capability in supported for capability in required_capabilities)

    def has_tags(self, tags: tuple[str, ...]) -> bool:
        """Return whether all requested tags are present in the profile."""

        profile_tags = set(self.tags)
        return all(tag in profile_tags for tag in tags)


@dataclass(frozen=True, slots=True)
class AgentCapabilityRequest:
    """Abstract capability request emitted by an agent boundary."""

    capability: str
    mission_id: str
    workflow_id: str
    task_id: str
    agent_assignment_id: str
    inputs: dict[str, Any] = field(default_factory=dict)
    context_refs: tuple[str, ...] = field(default_factory=tuple)
    risk_level: str = "low"
    limits: dict[str, Any] = field(default_factory=dict)
    guardian_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    request_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AgentExecutionRequest:
    """Normalized request for a runtime adapter to execute an agent assignment."""

    mission_id: str
    workflow_id: str
    task_id: str
    attempt_id: str
    agent_assignment_id: str
    agent_profile: AgentProfile
    required_capabilities: tuple[str, ...]
    task_type: str = "generic"
    mode: AgentMode = AgentMode.PRIMARY
    state: AgentState = AgentState.IDLE
    model_selection_decision_ref: str | None = None
    guardian_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    context_refs: tuple[str, ...] = field(default_factory=tuple)
    expected_outputs: tuple[str, ...] = field(default_factory=tuple)
    acceptance_criteria: tuple[str, ...] = field(default_factory=tuple)
    execution_limits: dict[str, Any] = field(default_factory=dict)
    logging_policy: dict[str, Any] = field(default_factory=dict)
    security_policy: dict[str, Any] = field(default_factory=dict)
    approval_policy: dict[str, Any] = field(default_factory=dict)
    allowed_paths: tuple[str, ...] = field(default_factory=tuple)
    denied_paths: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AgentExecutionResult:
    """Normalized result for an agent assignment without runtime coupling."""

    mission_id: str
    workflow_id: str
    task_id: str
    attempt_id: str
    agent_assignment_id: str
    agent_profile_id: str
    state: AgentState
    success: bool
    artifact_refs: tuple[str, ...] = field(default_factory=tuple)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    validation_results: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
    cost_used: float | None = None
    tokens_used: int | None = None
    cycle_count: int = 0
    runtime_result_ref: str | None = None
    audit_log_ref: str | None = None
    finished_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)


__all__ = [
    "AgentCapabilityRequest",
    "AgentExecutionRequest",
    "AgentExecutionResult",
    "AgentMode",
    "AgentProfile",
    "AgentRole",
    "AgentState",
]
