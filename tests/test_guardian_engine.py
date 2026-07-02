from __future__ import annotations

from vercosa_ai_framework.guardian import GuardianAction, GuardianEngine, GuardianEvaluationContext, GuardianMode, GuardianRiskLevel


def test_allows_clear_low_risk_mission_with_spec_deliverables_and_acceptance_criteria():
    engine = GuardianEngine()
    decision = engine.evaluate(
        GuardianEvaluationContext(
            mission_id="m-allow",
            evaluation_id="e-allow",
            evaluation_type="mission_pre_execution",
            guardian_mode=GuardianMode.STANDARD,
            mission_goal="Implementar MVP documentado. Entregaveis: engine e testes. Criterios de aceite: pytest passa.",
            spec_refs=("specs/framework/0005-guardian-engine.md",),
        )
    )

    assert decision.decision == GuardianAction.ALLOW
    assert decision.allowed is True
    assert decision.evaluation_id == "e-allow"


def test_blocks_empty_mission_before_execution():
    decision = GuardianEngine().validate_mission_text("   ")

    assert decision.decision == GuardianAction.BLOCK
    assert "mission.requires_goal" in decision.matched_policies


def test_requires_spec_for_implementation_mission_in_standard_mode():
    decision = GuardianEngine().validate_mission_text(
        "Implementar novo modulo. Entregaveis: codigo. Criterios de aceite: testes passam.",
        guardian_mode=GuardianMode.STANDARD,
    )

    assert decision.decision == GuardianAction.REQUIRE_APPROVAL
    assert "mission.requires_spec" in decision.matched_policies


def test_blocks_dangerous_commands():
    commands = ("rm -rf /", "mkfs.ext4 /dev/sda", "dd if=/dev/zero of=/dev/sda", "shutdown now", "reboot")
    engine = GuardianEngine()

    for command in commands:
        decision = engine.evaluate(
            GuardianEvaluationContext(
                mission_id=f"m-{command}",
                evaluation_type="command_pre_execution",
                mission_goal="Entregaveis: avaliacao. Criterios de aceite: bloquear comando.",
                planned_command=command,
                spec_refs=("specs/framework/0005-guardian-engine.md",),
            )
        )
        assert decision.decision == GuardianAction.BLOCK
        assert decision.risk_level == GuardianRiskLevel.CRITICAL


def test_detects_probable_secrets_without_returning_secret_value():
    secret = "api_key=super-secret-token-123456"
    decision = GuardianEngine().validate_mission_text(
        f"Validar configuracao com {secret}. Entregaveis: relatorio. Criterios de aceite: bloquear.",
        spec_refs=("specs/framework/0005-guardian-engine.md",),
    )

    assert decision.decision == GuardianAction.BLOCK
    assert "security.secret.assignment" in decision.matched_policies
    assert "secret_value" in decision.redactions_applied
    assert secret not in " ".join(decision.reasons + decision.blocked_items + decision.warnings)


def test_sudo_policy_depends_on_mode():
    engine = GuardianEngine()

    strict = engine.evaluate(_command_context("sudo apt update", GuardianMode.STRICT))
    standard = engine.evaluate(_command_context("sudo apt update", GuardianMode.STANDARD))
    permissive = engine.evaluate(_command_context("sudo apt update", GuardianMode.PERMISSIVE))

    assert strict.decision == GuardianAction.BLOCK
    assert standard.decision == GuardianAction.REQUIRE_APPROVAL
    assert permissive.decision == GuardianAction.WARN


def test_global_config_policy_depends_on_mode():
    engine = GuardianEngine()

    strict = engine.evaluate(_command_context("git config --global user.email test@example.com", GuardianMode.STRICT))
    standard = engine.evaluate(_command_context("git config --global user.email test@example.com", GuardianMode.STANDARD))
    permissive = engine.evaluate(_command_context("git config --global user.email test@example.com", GuardianMode.PERMISSIVE))

    assert strict.decision == GuardianAction.BLOCK
    assert standard.decision == GuardianAction.REQUIRE_APPROVAL
    assert permissive.decision == GuardianAction.WARN


def test_most_restrictive_decision_wins():
    decision = GuardianEngine().evaluate(
        GuardianEvaluationContext(
            mission_id="m-restrictive",
            evaluation_type="command_pre_execution",
            guardian_mode=GuardianMode.PERMISSIVE,
            mission_goal="Entregaveis: avaliacao. Criterios de aceite: bloquear comando.",
            planned_command="sudo rm -rf /",
            spec_refs=("specs/framework/0005-guardian-engine.md",),
        )
    )

    assert decision.decision == GuardianAction.BLOCK
    assert "security.sudo" in decision.matched_policies
    assert "security.block.rm_root" in decision.matched_policies


def _command_context(command: str, mode: GuardianMode) -> GuardianEvaluationContext:
    return GuardianEvaluationContext(
        mission_id=f"m-{mode.value}",
        evaluation_type="command_pre_execution",
        guardian_mode=mode,
        mission_goal="Entregaveis: avaliacao. Criterios de aceite: decisao estruturada.",
        planned_command=command,
        target_paths=(command,),
        spec_refs=("specs/framework/0005-guardian-engine.md",),
    )
