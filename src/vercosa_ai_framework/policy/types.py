"""Policy Engine contract types.

These types model declarative policy resolution only. They do not evaluate
concrete actions, call Guardian Engine, access external systems, or execute
providers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class PolicyScope(str, Enum):
    """Initial scopes where declarative policies can apply."""

    GLOBAL = "global"
    PROJECT = "project"
    MISSION = "mission"
    WORKFLOW = "workflow"
    TASK = "task"
    AGENT = "agent"
    CAPABILITY = "capability"
    SKILL = "skill"
    TOOL = "tool"
    PROVIDER = "provider"
    MODEL = "model"
    CONTEXT = "context"
    RUNTIME = "runtime"
    ENVIRONMENT = "environment"


class PolicySource(str, Enum):
    """Known origins for policy declarations."""

    GUARDIAN_SPEC = "guardian_spec"
    FRAMEWORK_SPEC = "framework_spec"
    PROJECT_SPEC = "project_spec"
    ADR = "adr"
    MISSION = "mission"
    USER = "user"
    ENVIRONMENT = "environment"
    RUNTIME = "runtime"
    PROVIDER = "provider"
    FRAMEWORK_DEFAULT = "framework_default"


class PolicyEffect(str, Enum):
    """Declarative effects resolved before operational enforcement."""

    ALLOW = "allow"
    DENY = "deny"
    WARN = "warn"
    REQUIRE_APPROVAL = "require_approval"
    SET_LIMIT = "set_limit"
    PREFER = "prefer"


class PolicySeverity(str, Enum):
    """Severity attached to a declarative policy rule or conflict."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


def utc_now_iso() -> str:
    """Return an auditable UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True, slots=True)
class PolicyRule:
    """Single declarative policy rule.

    ``key`` is the normalized policy dimension, such as ``network`` or
    ``max_tokens_per_task``. Rules with the same scope and key compete by
    priority in the deterministic MVP resolver.
    """

    rule_id: str
    key: str
    effect: PolicyEffect
    scope: PolicyScope = PolicyScope.GLOBAL
    source: PolicySource = PolicySource.FRAMEWORK_DEFAULT
    severity: PolicySeverity = PolicySeverity.MEDIUM
    priority: int = 0
    value: Any | None = None
    description: str = ""
    target_refs: tuple[str, ...] = field(default_factory=tuple)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def conflict_key(self) -> tuple[str, str]:
        """Return the deterministic key used for basic conflict detection."""

        return (self.scope.value, self.key)

    @property
    def effect_signature(self) -> tuple[str, str]:
        """Return a comparable representation of the declared outcome."""

        return (self.effect.value, repr(self.value))


@dataclass(frozen=True, slots=True)
class PolicySet:
    """Named collection of declarative policy rules."""

    policy_set_id: str
    name: str
    source: PolicySource
    scope: PolicyScope = PolicyScope.GLOBAL
    priority: int = 0
    rules: tuple[PolicyRule, ...] = field(default_factory=tuple)
    version: str = "0.1"
    description: str = ""
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class PolicyConflict:
    """Basic conflict detected between declarative policy rules."""

    key: str
    scope: PolicyScope
    winning_rule_id: str
    losing_rule_ids: tuple[str, ...]
    reason: str
    severity: PolicySeverity = PolicySeverity.MEDIUM
    conflict_id: str = field(default_factory=lambda: str(uuid4()))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ResolvedPolicySet:
    """Effective declarative policies after deterministic resolution."""

    resolved_rules: tuple[PolicyRule, ...]
    source_policy_set_ids: tuple[str, ...] = field(default_factory=tuple)
    conflicts: tuple[PolicyConflict, ...] = field(default_factory=tuple)
    effective_values: dict[str, Any] = field(default_factory=dict)
    resolution_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def matched_policy_refs(self) -> tuple[str, ...]:
        """Return rule identifiers included in the effective policy set."""

        return tuple(rule.rule_id for rule in self.resolved_rules)


@dataclass(frozen=True, slots=True)
class PolicyEvaluationContext:
    """Context used to scope policy resolution without operational enforcement."""

    mission_id: str | None = None
    workflow_id: str | None = None
    task_id: str | None = None
    agent_id: str | None = None
    capability_id: str | None = None
    target_scope: PolicyScope | None = None
    requested_scopes: tuple[PolicyScope, ...] = field(default_factory=tuple)
    requested_keys: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class PolicyResolutionResult:
    """Auditable result returned by a Policy Engine implementation."""

    resolved_policy_set: ResolvedPolicySet
    context: PolicyEvaluationContext = field(default_factory=PolicyEvaluationContext)
    ordered_policy_set_ids: tuple[str, ...] = field(default_factory=tuple)
    conflicts: tuple[PolicyConflict, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)


class PolicyEngine(ABC):
    """Port for declarative policy resolution."""

    @abstractmethod
    def resolve(
        self,
        policy_sets: tuple[PolicySet, ...] | list[PolicySet],
        context: PolicyEvaluationContext | None = None,
    ) -> PolicyResolutionResult:
        """Resolve declarative policies into an effective policy set."""


__all__ = [
    "PolicyConflict",
    "PolicyEffect",
    "PolicyEngine",
    "PolicyEvaluationContext",
    "PolicyResolutionResult",
    "PolicyRule",
    "PolicyScope",
    "PolicySet",
    "PolicySeverity",
    "PolicySource",
    "ResolvedPolicySet",
]
