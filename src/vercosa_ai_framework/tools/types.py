"""Tool contract types.

Tools describe concrete integration mechanisms for skills. These initial
contracts are descriptive only and do not execute providers, MCPs, APIs,
filesystem operations, commands, or subprocesses.
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
class ToolProfile:
    """Static contract for a concrete tool available to skills."""

    name: str
    version: str
    description: str
    provider_type: str
    operation_type: str
    domain: str
    tool_id: str = field(default_factory=lambda: str(uuid4()))
    provider_ref: str | None = None
    mcp_ref: str | None = None
    effects: tuple[str, ...] = field(default_factory=tuple)
    required_permissions: tuple[str, ...] = field(default_factory=tuple)
    input_schema_ref: str | None = None
    output_schema_ref: str | None = None
    timeout: float | None = None
    retry_policy: dict[str, Any] = field(default_factory=dict)
    fallback_tools: tuple[str, ...] = field(default_factory=tuple)
    network_policy: str = "none"
    data_sensitivity: str = "public"
    audit_log_ref: str | None = None
    tags: tuple[str, ...] = field(default_factory=tuple)
    available: bool = True
    dangerous: bool = False
    experimental: bool = False
    deprecated: bool = False
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def has_tags(self, tags: tuple[str, ...]) -> bool:
        """Return whether all requested tags are present in the profile."""

        profile_tags = set(self.tags)
        return all(tag in profile_tags for tag in tags)

    def has_effects(self, effects: tuple[str, ...]) -> bool:
        """Return whether all requested effects are declared by the tool."""

        tool_effects = set(self.effects)
        return all(effect in tool_effects for effect in effects)


@dataclass(frozen=True, slots=True)
class ToolExecutionRequest:
    """Normalized request to execute a tool through an authorized skill boundary."""

    tool: str
    skill: str
    mission_id: str
    workflow_id: str
    task_id: str
    inputs: dict[str, Any] = field(default_factory=dict)
    granted_permissions: tuple[str, ...] = field(default_factory=tuple)
    allowed_effects: tuple[str, ...] = field(default_factory=tuple)
    dry_run: bool = True
    limits: dict[str, Any] = field(default_factory=dict)
    guardian_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    request_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ToolExecutionResult:
    """Normalized tool result without exposing external implementation details."""

    tool: str
    skill: str
    mission_id: str
    workflow_id: str
    task_id: str
    success: bool
    outputs: dict[str, Any] = field(default_factory=dict)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
    cost_used: float | None = None
    audit_log_ref: str | None = None
    finished_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)


__all__ = ["ToolExecutionRequest", "ToolExecutionResult", "ToolProfile"]
