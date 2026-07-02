"""Guardian Engine policy contracts."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from vercosa_ai_framework.guardian.types import (
    GuardianAction,
    GuardianDecision,
    GuardianMode,
    GuardianSeverity,
)


@dataclass(frozen=True, slots=True)
class GuardianEvaluationContext:
    """Minimal input context for a Guardian policy evaluation."""

    mission_id: str
    evaluation_type: str
    mission_goal: str = ""
    evaluation_id: str | None = None
    guardian_mode: GuardianMode = GuardianMode.STANDARD
    spec_refs: tuple[str, ...] = field(default_factory=tuple)
    guardian_refs: tuple[str, ...] = field(default_factory=tuple)
    workspace: str = "."
    requested_action: str | None = None
    planned_command: str | None = None
    target_paths: tuple[str, ...] = field(default_factory=tuple)
    data_sensitivity: str | None = None
    network_policy: dict[str, Any] = field(default_factory=dict)
    provider_policy: dict[str, Any] = field(default_factory=dict)
    budget_policy: dict[str, Any] = field(default_factory=dict)
    execution_limits: dict[str, Any] = field(default_factory=dict)
    current_cycle: int | None = None
    risk_overrides: tuple[str, ...] = field(default_factory=tuple)
    prior_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)


class GuardianPolicy(ABC):
    """Abstract policy boundary for Guardian Engine implementations."""

    policy_id: str
    title: str
    default_action: GuardianAction
    severity: GuardianSeverity

    @abstractmethod
    def evaluate(self, context: GuardianEvaluationContext) -> GuardianDecision:
        """Evaluate context and return a structured decision without side effects."""


@dataclass(frozen=True, slots=True)
class StaticGuardianPolicy(GuardianPolicy):
    """Testable policy implementation that always returns its configured action."""

    policy_id: str
    title: str
    default_action: GuardianAction = GuardianAction.ALLOW
    severity: GuardianSeverity = GuardianSeverity.LOW
    reason: str = ""

    def evaluate(self, context: GuardianEvaluationContext) -> GuardianDecision:
        """Return a deterministic decision for contract tests and adapters."""

        reasons = (self.reason,) if self.reason else ()
        return GuardianDecision(
            mission_id=context.mission_id,
            evaluation_id=context.evaluation_id or context.mission_id,
            decision=self.default_action,
            guardian_mode=context.guardian_mode,
            matched_policies=(self.policy_id,),
            reasons=reasons,
        )


__all__ = [
    "GuardianEvaluationContext",
    "GuardianPolicy",
    "StaticGuardianPolicy",
]
