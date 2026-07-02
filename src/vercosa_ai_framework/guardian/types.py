"""Guardian Engine contract types.

These types represent policy decisions only. They do not execute commands,
inspect external systems, or call concrete runtimes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class GuardianAction(str, Enum):
    """Actions a Guardian policy decision can emit."""

    ALLOW = "allow"
    WARN = "warn"
    BLOCK = "block"
    REQUIRE_APPROVAL = "require_approval"


class GuardianSeverity(str, Enum):
    """Severity assigned to a policy match or violation."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class GuardianMode(str, Enum):
    """Operational policy mode from Spec 0005."""

    PERMISSIVE = "permissive"
    STANDARD = "standard"
    STRICT = "strict"


class GuardianRiskLevel(str, Enum):
    """Aggregated mission or action risk level from Spec 0005."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


def utc_now_iso() -> str:
    """Return an auditable UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True, slots=True)
class GuardianViolation:
    """Policy violation or relevant policy match found during evaluation."""

    policy_id: str
    severity: GuardianSeverity
    message: str
    action: GuardianAction = GuardianAction.WARN
    target_refs: tuple[str, ...] = field(default_factory=tuple)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    redactions_applied: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class GuardianDecision:
    """Structured, auditable Guardian Engine evaluation result."""

    mission_id: str
    decision: GuardianAction
    evaluation_id: str = field(default_factory=lambda: str(uuid4()))
    risk_level: GuardianRiskLevel = GuardianRiskLevel.LOW
    guardian_mode: GuardianMode = GuardianMode.STANDARD
    matched_policies: tuple[str, ...] = field(default_factory=tuple)
    violations: tuple[GuardianViolation, ...] = field(default_factory=tuple)
    reasons: tuple[str, ...] = field(default_factory=tuple)
    required_actions: tuple[str, ...] = field(default_factory=tuple)
    approval_requirements: tuple[str, ...] = field(default_factory=tuple)
    blocked_items: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    safe_alternatives: tuple[str, ...] = field(default_factory=tuple)
    limits_applied: dict[str, Any] = field(default_factory=dict)
    redactions_applied: tuple[str, ...] = field(default_factory=tuple)
    created_at: str = field(default_factory=utc_now_iso)
    expires_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def allowed(self) -> bool:
        """Return whether the evaluated action can proceed without a hard stop."""

        return self.decision in {GuardianAction.ALLOW, GuardianAction.WARN}

    @property
    def requires_approval(self) -> bool:
        """Return whether explicit approval is required before proceeding."""

        return self.decision == GuardianAction.REQUIRE_APPROVAL

    @property
    def blocked(self) -> bool:
        """Return whether the evaluated action is blocked."""

        return self.decision == GuardianAction.BLOCK
