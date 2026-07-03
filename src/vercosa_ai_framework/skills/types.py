"""Provider-neutral Skill contract types.

Skills describe reusable procedures that implement capabilities. These contracts
do not execute tools, call providers, access MCPs, or use subprocesses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def utc_now_iso() -> str:
    """Return an auditable UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True, slots=True)
class SkillProfile:
    """Static contract for a reusable framework skill."""

    name: str
    version: str
    description: str
    implemented_capabilities: tuple[str, ...]
    domain: str
    skill_id: str = field(default_factory=lambda: str(uuid4()))
    input_contract_ref: str | None = None
    output_contract_ref: str | None = None
    required_tools: tuple[str, ...] = field(default_factory=tuple)
    optional_tools: tuple[str, ...] = field(default_factory=tuple)
    fallback_skills: tuple[str, ...] = field(default_factory=tuple)
    risk_level: str = "low"
    permission_requirements: tuple[str, ...] = field(default_factory=tuple)
    execution_limits: dict[str, Any] = field(default_factory=dict)
    validation_requirements: tuple[str, ...] = field(default_factory=tuple)
    trusted_context_requirements: tuple[str, ...] = field(default_factory=tuple)
    audit_log_ref: str | None = None
    tags: tuple[str, ...] = field(default_factory=tuple)
    priority: int = 100
    experimental: bool = False
    deprecated: bool = False
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def implements_capability(self, capability: str) -> bool:
        """Return whether this skill declares support for a capability."""

        return capability in self.implemented_capabilities

    def has_tags(self, tags: tuple[str, ...]) -> bool:
        """Return whether all requested tags are present in the profile."""

        profile_tags = set(self.tags)
        return all(tag in profile_tags for tag in tags)


@dataclass(frozen=True, slots=True)
class SkillExecutionRequest:
    """Normalized request to execute a skill through an authorized boundary."""

    skill: str
    capability: str
    mission_id: str
    workflow_id: str
    task_id: str
    agent_assignment_id: str
    inputs: dict[str, Any] = field(default_factory=dict)
    context_refs: tuple[str, ...] = field(default_factory=tuple)
    granted_permissions: tuple[str, ...] = field(default_factory=tuple)
    allowed_tools: tuple[str, ...] = field(default_factory=tuple)
    limits: dict[str, Any] = field(default_factory=dict)
    guardian_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    request_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class SkillExecutionResult:
    """Normalized skill result without provider or MCP coupling."""

    skill: str
    capability: str
    mission_id: str
    workflow_id: str
    task_id: str
    success: bool
    outputs: dict[str, Any] = field(default_factory=dict)
    tool_result_refs: tuple[str, ...] = field(default_factory=tuple)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
    audit_log_ref: str | None = None
    finished_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)


__all__ = ["SkillExecutionRequest", "SkillExecutionResult", "SkillProfile"]
