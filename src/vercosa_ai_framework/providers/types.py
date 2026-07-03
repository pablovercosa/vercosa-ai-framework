"""Provider Gateway contract types.

These initial contracts are descriptive only. They do not execute providers,
call MCPs or APIs, access filesystems or databases, invoke CLIs, or use
subprocesses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class ProviderKind(str, Enum):
    """Supported initial provider kinds for Provider Gateway contracts."""

    MCP = "mcp"
    API = "api"
    CLI = "cli"
    FILESYSTEM = "filesystem"
    DATABASE = "database"
    LOCAL_SERVICE = "local_service"
    MOCK = "mock"


def utc_now_iso() -> str:
    """Return an auditable UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True, slots=True)
class ProviderProfile:
    """Declarative profile for a provider available through the gateway."""

    name: str
    version: str
    description: str
    kind: ProviderKind
    adapter_ref: str
    provider_id: str = field(default_factory=lambda: str(uuid4()))
    supported_operations: tuple[str, ...] = field(default_factory=tuple)
    supported_domains: tuple[str, ...] = field(default_factory=tuple)
    effects: tuple[str, ...] = field(default_factory=tuple)
    required_permissions: tuple[str, ...] = field(default_factory=tuple)
    network_policy: str = "none"
    data_sensitivity_allowed: tuple[str, ...] = ("public",)
    secret_refs: tuple[str, ...] = field(default_factory=tuple)
    default_timeout: float | None = None
    retry_policy: dict[str, Any] = field(default_factory=dict)
    fallback_providers: tuple[str, ...] = field(default_factory=tuple)
    cost_policy: dict[str, Any] = field(default_factory=dict)
    rate_limit_policy: dict[str, Any] = field(default_factory=dict)
    locality: str = "local"
    availability: dict[str, Any] = field(default_factory=dict)
    tags: tuple[str, ...] = field(default_factory=tuple)
    enabled: bool = True
    dangerous: bool = False
    experimental: bool = False
    deprecated: bool = False
    blocked: bool = False
    guardian_policy_refs: tuple[str, ...] = field(default_factory=tuple)
    audit_log_ref: str | None = None
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def has_tags(self, tags: tuple[str, ...]) -> bool:
        """Return whether all requested tags are present in the profile."""

        profile_tags = set(self.tags)
        return all(tag in profile_tags for tag in tags)

    def supports_domain(self, domain: str) -> bool:
        """Return whether the provider declares support for a domain."""

        return domain in set(self.supported_domains)

    def supports_operation(self, operation: str) -> bool:
        """Return whether the provider declares support for an operation."""

        return operation in set(self.supported_operations)


@dataclass(frozen=True, slots=True)
class ProviderRequest:
    """Normalized request emitted by a Tool for Provider Gateway handling."""

    operation: str
    mission_id: str
    workflow_id: str
    task_id: str
    tool_id: str
    inputs: dict[str, Any] = field(default_factory=dict)
    provider_ref: str | None = None
    provider_kind: ProviderKind | None = None
    tool_execution_request_id: str | None = None
    attempt_id: str | None = None
    agent_assignment_id: str | None = None
    skill_id: str | None = None
    input_schema_ref: str | None = None
    expected_output_schema_ref: str | None = None
    granted_permissions: tuple[str, ...] = field(default_factory=tuple)
    allowed_effects: tuple[str, ...] = field(default_factory=tuple)
    allowed_paths: tuple[str, ...] = field(default_factory=tuple)
    data_sensitivity: str = "public"
    network_policy: dict[str, Any] = field(default_factory=dict)
    budget_policy: dict[str, Any] = field(default_factory=dict)
    timeout: float | None = None
    retry_policy: dict[str, Any] = field(default_factory=dict)
    fallback_allowed: bool = False
    dry_run: bool = True
    guardian_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    provider_request_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ProviderResult:
    """Normalized result returned from Provider Gateway to a Tool."""

    provider_request_id: str
    provider_id: str
    adapter_ref: str
    operation: str
    success: bool
    status: str
    provider_result_id: str = field(default_factory=lambda: str(uuid4()))
    outputs: dict[str, Any] = field(default_factory=dict)
    normalized_output_schema_ref: str | None = None
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    artifact_refs: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
    blocked_reason: str | None = None
    fallback_from: str | None = None
    fallback_to: str | None = None
    retry_count: int = 0
    timeout_applied: float | None = None
    cost_used: float | None = None
    rate_limit_state: dict[str, Any] = field(default_factory=dict)
    guardian_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    redactions_applied: tuple[str, ...] = field(default_factory=tuple)
    audit_log_ref: str | None = None
    started_at: str | None = None
    finished_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)


__all__ = ["ProviderKind", "ProviderProfile", "ProviderRequest", "ProviderResult"]
