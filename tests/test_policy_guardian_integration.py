from __future__ import annotations

import sys

from vercosa_ai_framework.guardian import GuardianAction, GuardianEngine, GuardianEvaluationContext
from vercosa_ai_framework.policy import (
    DeterministicPolicyEngine,
    PolicyConflict,
    PolicyEffect,
    PolicyRule,
    PolicyScope,
    PolicySet,
    PolicySeverity,
    PolicySource,
    ResolvedPolicySet,
)


MISSION_TEXT = "Atualizar documentacao com entregaveis e criterios de aceite definidos."


def _context(resolved_policy_set: ResolvedPolicySet | None = None) -> GuardianEvaluationContext:
    return GuardianEvaluationContext(
        mission_id="mission-policy-guardian",
        evaluation_id="evaluation-policy-guardian",
        evaluation_type="mission_pre_execution",
        mission_goal=MISSION_TEXT,
        resolved_policy_set=resolved_policy_set,
        metadata={"deliverables": "documentacao", "acceptance_criteria": "pytest"},
    )


def _resolved_rule(effect: PolicyEffect, *, severity: PolicySeverity = PolicySeverity.MEDIUM) -> ResolvedPolicySet:
    rule = PolicyRule(
        rule_id=f"policy.{effect.value}",
        key="network",
        effect=effect,
        scope=PolicyScope.TOOL,
        source=PolicySource.PROJECT_SPEC,
        severity=severity,
        priority=10,
        value="external",
    )
    return ResolvedPolicySet(resolved_rules=(rule,))


def test_guardian_without_resolved_policy_set_keeps_current_behavior():
    decision = GuardianEngine().evaluate(_context())

    assert decision.decision == GuardianAction.ALLOW
    assert decision.matched_policies == ("guardian.mvp",)


def test_resolved_allow_policy_does_not_block():
    decision = GuardianEngine().evaluate(_context(_resolved_rule(PolicyEffect.ALLOW)))

    assert decision.decision == GuardianAction.ALLOW
    assert decision.blocked is False


def test_resolved_warn_policy_elevates_to_warn():
    decision = GuardianEngine().evaluate(_context(_resolved_rule(PolicyEffect.WARN)))

    assert decision.decision == GuardianAction.WARN
    assert "policy.warn" in decision.matched_policies


def test_resolved_require_approval_policy_elevates_to_require_approval():
    decision = GuardianEngine().evaluate(_context(_resolved_rule(PolicyEffect.REQUIRE_APPROVAL)))

    assert decision.decision == GuardianAction.REQUIRE_APPROVAL
    assert decision.requires_approval is True


def test_resolved_deny_policy_elevates_to_block():
    decision = GuardianEngine().evaluate(_context(_resolved_rule(PolicyEffect.DENY, severity=PolicySeverity.CRITICAL)))

    assert decision.decision == GuardianAction.BLOCK
    assert decision.blocked is True


def test_policy_engine_conflicts_are_considered_by_guardian():
    allow = PolicyRule(rule_id="network.allow", key="network", effect=PolicyEffect.ALLOW, priority=1)
    deny = PolicyRule(
        rule_id="network.deny",
        key="network",
        effect=PolicyEffect.DENY,
        severity=PolicySeverity.CRITICAL,
        priority=10,
    )
    result = DeterministicPolicyEngine().resolve(
        [
            PolicySet(
                policy_set_id="network",
                name="Politicas de rede",
                source=PolicySource.PROJECT_SPEC,
                rules=(allow, deny),
            )
        ]
    )

    decision = GuardianEngine().evaluate(_context(result.resolved_policy_set))

    assert result.conflicts
    assert decision.decision == GuardianAction.BLOCK
    assert any("conflito de politica resolvida" in reason for reason in decision.reasons)


def test_low_severity_policy_conflict_generates_warning():
    conflict = PolicyConflict(
        key="model",
        scope=PolicyScope.MODEL,
        winning_rule_id="model.local",
        losing_rule_ids=("model.free",),
        reason="preferencias divergentes",
        severity=PolicySeverity.LOW,
        conflict_id="conflict.model",
    )
    resolved = ResolvedPolicySet(resolved_rules=(), conflicts=(conflict,))

    decision = GuardianEngine().evaluate(_context(resolved))


    assert decision.decision == GuardianAction.WARN
    assert "conflict.model" in decision.matched_policies


def test_policy_guardian_integration_is_deterministic():
    context = _context(_resolved_rule(PolicyEffect.REQUIRE_APPROVAL, severity=PolicySeverity.HIGH))
    first = GuardianEngine().evaluate(context)
    second = GuardianEngine().evaluate(context)

    assert first.evaluation_id == second.evaluation_id
    assert first.decision == second.decision
    assert first.risk_level == second.risk_level
    assert first.matched_policies == second.matched_policies
    assert first.reasons == second.reasons
    assert first.required_actions == second.required_actions


def test_policy_guardian_integration_does_not_import_external_clients():
    forbidden_modules = {
        "requests",
        "httpx",
        "psycopg",
        "psycopg2",
        "openai",
        "google.generativeai",
        "anthropic",
        "ollama",
    }
    before = set(sys.modules)

    GuardianEngine().evaluate(_context(_resolved_rule(PolicyEffect.WARN)))

    imported_after_evaluation = set(sys.modules) - before
    assert not forbidden_modules.intersection(imported_after_evaluation)


def test_policy_engine_still_does_not_depend_on_guardian():
    sys.modules.pop("vercosa_ai_framework.guardian", None)
    before = set(sys.modules)

    DeterministicPolicyEngine().resolve([])

    imported_after_resolution = set(sys.modules) - before
    assert "vercosa_ai_framework.guardian" not in imported_after_resolution
