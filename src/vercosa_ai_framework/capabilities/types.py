"""Provider-neutral Capability contract types.

Capabilities describe functional intent only. They do not execute skills, call
tools, access MCPs, contact providers, or use subprocesses.
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
class CapabilityProfile:
    """Static contract for a framework capability."""

    name: str
    version: str
    description: str
    intent: str
    domain: str
    capability_id: str = field(default_factory=lambda: str(uuid4()))
    input_schema_ref: str | None = None
    output_schema_ref: str | None = None
    risk_level: str = "low"
    required_permissions: tuple[str, ...] = field(default_factory=tuple)
    allowed_agent_roles: tuple[str, ...] = field(default_factory=tuple)
    allowed_task_types: tuple[str, ...] = field(default_factory=tuple)
    default_limits: dict[str, Any] = field(default_factory=dict)
    guardian_policy_refs: tuple[str, ...] = field(default_factory=tuple)
    fallback_allowed: bool = False
    audit_log_ref: str | None = None
    tags: tuple[str, ...] = field(default_factory=tuple)
    experimental: bool = False
    deprecated: bool = False
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def has_tags(self, tags: tuple[str, ...]) -> bool:
        """Return whether all requested tags are present in the profile."""

        profile_tags = set(self.tags)
        return all(tag in profile_tags for tag in tags)

    def allows_agent_role(self, role: str) -> bool:
        """Return whether a role is allowed when role constraints are declared."""

        return not self.allowed_agent_roles or role in self.allowed_agent_roles

    def allows_task_type(self, task_type: str) -> bool:
        """Return whether a task type is allowed when task constraints are declared."""

        return not self.allowed_task_types or task_type in self.allowed_task_types


@dataclass(frozen=True, slots=True)
class CapabilityRequest:
    """Traceable abstract request for a capability resolution boundary."""

    capability: str
    mission_id: str
    workflow_id: str
    task_id: str
    agent_assignment_id: str
    inputs: dict[str, Any] = field(default_factory=dict)
    context_refs: tuple[str, ...] = field(default_factory=tuple)
    granted_permissions: tuple[str, ...] = field(default_factory=tuple)
    risk_level: str = "low"
    limits: dict[str, Any] = field(default_factory=dict)
    guardian_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    request_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)


__all__ = ["CapabilityProfile", "CapabilityRequest"]
