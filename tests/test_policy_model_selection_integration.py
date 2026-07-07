from __future__ import annotations

import sys

from vercosa_ai_framework.model_selection import ModelProfile, ModelSelectionPolicy, ModelSelector, select_model
from vercosa_ai_framework.policy import (
    DeterministicPolicyEngine,
    PolicyConflict,
    PolicyEffect,
    PolicyRule,
    PolicyScope,
    PolicySeverity,
    PolicySource,
    ResolvedPolicySet,
)


def _models() -> tuple[ModelProfile, ...]:
    return (
        ModelProfile(
            id="local-small",
            provider="local-provider",
            runtime="local",
            quality_tier="standard",
            reasoning_tier="light",
            memory_tier="short",
            context_window=8_000,
            local=True,
            free=True,
            paid=False,
            small=True,
        ),
        ModelProfile(
            id="local-strong",
            provider="local-provider",
            runtime="local",
            quality_tier="high",
            reasoning_tier="high",
            memory_tier="long",
            context_window=32_000,
            local=True,
            free=True,
            paid=False,
        ),
        ModelProfile(
            id="remote-strong",
            provider="remote-provider",
            runtime="api",
            quality_tier="high",
            reasoning_tier="high",
            memory_tier="long",
            context_window=32_000,
            local=False,
            free=True,
            paid=False,
        ),
    )


def _policy() -> ModelSelectionPolicy:
    return ModelSelectionPolicy(
        complexity="low",
        quality="standard",
        reasoning="light",
        memory="short",
        cost_profile="strict_free",
        prefer_local=True,
    )


def _resolved_rule(effect: PolicyEffect, *, rule_id: str | None = None, key: str = "model") -> ResolvedPolicySet:
    rule = PolicyRule(
        rule_id=rule_id or f"model.{effect.value}",
        key=key,
        effect=effect,
        scope=PolicyScope.MODEL,
        source=PolicySource.PROJECT_SPEC,
        severity=PolicySeverity.HIGH,
        priority=10,
        value="local-small",
    )
    return ResolvedPolicySet(resolved_rules=(rule,))


def test_model_selection_without_resolved_policy_set_keeps_current_behavior():
    decision = select_model(_models(), _policy())

    assert decision.selected_model.id == "local-small"
    assert decision.policy_sources == ("framework_defaults",)


def test_allow_policy_does_not_force_model_choice():
    resolved = _resolved_rule(PolicyEffect.ALLOW, rule_id="model.allow.remote")

    decision = select_model(_models(), _policy(), resolved_policy_set=resolved)

    assert decision.selected_model.id == "local-small"
    assert "model.allow.remote" in decision.policy_sources


def test_warn_policy_is_reflected_in_security_notes():
    resolved = _resolved_rule(PolicyEffect.WARN, rule_id="model.warn.review")

    decision = select_model(_models(), _policy(), resolved_policy_set=resolved)

    assert decision.selected_model.id == "local-small"
    assert any("model.warn.review" in note for note in decision.security_notes)


def test_require_approval_policy_is_traceable_in_decision():
    resolved = _resolved_rule(PolicyEffect.REQUIRE_APPROVAL, rule_id="model.approval.required")

    decision = select_model(_models(), _policy(), resolved_policy_set=resolved)

    assert decision.requires_user_approval is True
    assert decision.requires_review is True
    assert any("model.approval.required" in note for note in decision.security_notes)


def test_deny_policy_excludes_model_when_rule_has_clear_target():
    resolved = _resolved_rule(PolicyEffect.DENY, rule_id="model.deny.local-small")

    decision = select_model(_models(), _policy(), resolved_policy_set=resolved)
    selected_ids = (decision.selected_model.id, *(model.id for model in decision.fallback_chain))

    assert decision.selected_model.id == "local-strong"
    assert "local-small" not in selected_ids
    assert any("model.deny.local-small" in note for note in decision.security_notes)


def test_policy_conflict_is_considered_deterministically():
    conflict = PolicyConflict(
        key="model",
        scope=PolicyScope.MODEL,
        winning_rule_id="model.prefer.local",
        losing_rule_ids=("model.prefer.remote",),
        reason="preferencias divergentes de modelo",
        severity=PolicySeverity.HIGH,
        conflict_id="conflict.model.preference",
    )
    resolved = ResolvedPolicySet(resolved_rules=(), conflicts=(conflict,))
    selector = ModelSelector(_models())

    first = selector.select(_policy(), resolved_policy_set=resolved)
    second = selector.select(_policy(), resolved_policy_set=resolved)

    assert first.selected_model.id == second.selected_model.id == "local-small"
    assert first.requires_user_approval is True
    assert second.requires_user_approval is True
    assert first.security_notes == second.security_notes
    assert "conflict.model.preference" in first.policy_sources


def test_selection_is_repeatable_with_same_resolved_policy_set():
    resolved = _resolved_rule(PolicyEffect.WARN, rule_id="model.warn.repeatable")
    selector = ModelSelector(_models())

    first = selector.select(_policy(), resolved_policy_set=resolved)
    second = selector.select(_policy(), resolved_policy_set=resolved)

    assert first.selected_model == second.selected_model
    assert first.fallback_chain == second.fallback_chain
    assert first.policy_sources == second.policy_sources
    assert first.security_notes == second.security_notes


def test_policy_model_selection_integration_does_not_import_external_clients_or_guardian():
    forbidden_modules = {
        "requests",
        "httpx",
        "psycopg",
        "psycopg2",
        "openai",
        "google.generativeai",
        "anthropic",
        "ollama",
        "vercosa_ai_framework.guardian",
    }
    sys.modules.pop("vercosa_ai_framework.guardian", None)
    before = set(sys.modules)

    select_model(_models(), _policy(), resolved_policy_set=_resolved_rule(PolicyEffect.WARN))

    imported_after_selection = set(sys.modules) - before
    assert not forbidden_modules.intersection(imported_after_selection)


def test_policy_engine_does_not_import_model_selection_for_resolution():
    for module_name in tuple(sys.modules):
        if module_name.startswith("vercosa_ai_framework.model_selection"):
            sys.modules.pop(module_name, None)
    before = set(sys.modules)

    DeterministicPolicyEngine().resolve([])

    imported_after_resolution = set(sys.modules) - before
    assert not any(
        module_name.startswith("vercosa_ai_framework.model_selection")
        for module_name in imported_after_resolution
    )
