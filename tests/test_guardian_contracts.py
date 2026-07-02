from __future__ import annotations

from dataclasses import asdict

import pytest

from vercosa_ai_framework.guardian import (
    GuardianAction,
    GuardianDecision,
    GuardianEvaluationContext,
    GuardianMode,
    GuardianPolicy,
    GuardianRiskLevel,
    GuardianSeverity,
    GuardianViolation,
    StaticGuardianPolicy,
)


def test_guardian_actions_match_spec_0005_decisions():
    assert {action.value for action in GuardianAction} == {
        "allow",
        "warn",
        "block",
        "require_approval",
    }


def test_guardian_policy_is_abstract():
    with pytest.raises(TypeError):
        GuardianPolicy()


def test_guardian_decision_captures_violations_and_explainability_fields():
    violation = GuardianViolation(
        policy_id="security.no_sudo",
        severity=GuardianSeverity.CRITICAL,
        action=GuardianAction.BLOCK,
        message="sudo is blocked by default",
        target_refs=("planned_command",),
        evidence_refs=("specs/framework/0005-guardian-engine.md",),
        redactions_applied=("command_args",),
    )
    decision = GuardianDecision(
        mission_id="m-1",
        evaluation_id="e-1",
        decision=GuardianAction.BLOCK,
        risk_level=GuardianRiskLevel.CRITICAL,
        guardian_mode=GuardianMode.STANDARD,
        matched_policies=("security.no_sudo",),
        violations=(violation,),
        reasons=("execution privilegiada nao autorizada",),
        blocked_items=("sudo apt update",),
        safe_alternatives=("Use um adapter autorizado sem sudo.",),
    )

    assert decision.blocked is True
    assert decision.allowed is False
    assert decision.requires_approval is False
    assert decision.violations[0].severity == GuardianSeverity.CRITICAL
    assert asdict(decision)["decision"] == GuardianAction.BLOCK


def test_static_policy_returns_testable_decision_without_runtime_execution():
    policy = StaticGuardianPolicy(
        policy_id="quality.requires_validation",
        title="Require validation evidence",
        default_action=GuardianAction.REQUIRE_APPROVAL,
        severity=GuardianSeverity.HIGH,
        reason="high risk work requires explicit approval",
    )
    context = GuardianEvaluationContext(
        mission_id="m-2",
        evaluation_id="e-2",
        evaluation_type="mission_start",
        mission_goal="Implementar contrato inicial",
        spec_refs=("specs/framework/0005-guardian-engine.md",),
        guardian_refs=("Security by Design",),
    )

    decision = policy.evaluate(context)

    assert decision.mission_id == "m-2"
    assert decision.evaluation_id == "e-2"
    assert decision.decision == GuardianAction.REQUIRE_APPROVAL
    assert decision.requires_approval is True
    assert decision.matched_policies == ("quality.requires_validation",)
    assert decision.reasons == ("high risk work requires explicit approval",)
