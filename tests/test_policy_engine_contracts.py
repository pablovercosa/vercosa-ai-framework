from __future__ import annotations

import sys

import pytest

from vercosa_ai_framework.policy import (
    DeterministicPolicyEngine,
    PolicyEffect,
    PolicyEngine,
    PolicyEvaluationContext,
    PolicyRule,
    PolicyScope,
    PolicySet,
    PolicySeverity,
    PolicySource,
    ResolvedPolicySet,
)


def test_policy_rule_creation():
    rule = PolicyRule(
        rule_id="context.max_tokens",
        key="max_tokens",
        effect=PolicyEffect.SET_LIMIT,
        scope=PolicyScope.CONTEXT,
        source=PolicySource.FRAMEWORK_SPEC,
        severity=PolicySeverity.HIGH,
        priority=10,
        value=4096,
    )

    assert rule.rule_id == "context.max_tokens"
    assert rule.conflict_key == ("context", "max_tokens")
    assert rule.effect_signature == ("set_limit", "4096")


def test_policy_set_creation():
    rule = PolicyRule(rule_id="network.none", key="network", effect=PolicyEffect.DENY)
    policy_set = PolicySet(
        policy_set_id="framework-defaults",
        name="Defaults do framework",
        source=PolicySource.FRAMEWORK_DEFAULT,
        rules=(rule,),
    )

    assert policy_set.rules == (rule,)
    assert policy_set.enabled is True


def test_policy_engine_port_is_abstract():
    with pytest.raises(TypeError):
        PolicyEngine()


def test_empty_policy_list_resolution():
    result = DeterministicPolicyEngine().resolve([])

    assert isinstance(result.resolved_policy_set, ResolvedPolicySet)
    assert result.resolved_policy_set.resolved_rules == ()
    assert result.ordered_policy_set_ids == ()
    assert result.conflicts == ()


def test_simple_policy_resolution_produces_resolved_policy_set():
    rule = PolicyRule(rule_id="network.local_only", key="network", effect=PolicyEffect.DENY, value="external")
    policy_set = PolicySet(
        policy_set_id="security",
        name="Seguranca",
        source=PolicySource.GUARDIAN_SPEC,
        rules=(rule,),
    )

    result = DeterministicPolicyEngine().resolve([policy_set])

    assert result.resolved_policy_set.resolved_rules == (rule,)
    assert result.resolved_policy_set.matched_policy_refs == ("network.local_only",)
    assert result.resolved_policy_set.effective_values == {"global.network": "external"}


def test_deterministic_ordering_by_priority():
    low = PolicyRule(rule_id="model.free", key="model", effect=PolicyEffect.PREFER, priority=1, value="free")
    high = PolicyRule(rule_id="model.local", key="model", effect=PolicyEffect.PREFER, priority=20, value="local")
    policy_set = PolicySet(
        policy_set_id="models",
        name="Modelos",
        source=PolicySource.FRAMEWORK_SPEC,
        rules=(low, high),
    )

    result = DeterministicPolicyEngine().resolve([policy_set])

    assert result.resolved_policy_set.resolved_rules == (high,)
    assert result.resolved_policy_set.effective_values["global.model"] == "local"


def test_basic_conflict_detection():
    allow_network = PolicyRule(
        rule_id="network.allow",
        key="network",
        effect=PolicyEffect.ALLOW,
        priority=1,
        value="external",
    )
    deny_network = PolicyRule(
        rule_id="network.deny",
        key="network",
        effect=PolicyEffect.DENY,
        severity=PolicySeverity.CRITICAL,
        priority=10,
        value="external",
    )
    policy_set = PolicySet(
        policy_set_id="network-policies",
        name="Politicas de rede",
        source=PolicySource.PROJECT_SPEC,
        rules=(allow_network, deny_network),
    )

    result = DeterministicPolicyEngine().resolve([policy_set])

    assert result.resolved_policy_set.resolved_rules == (deny_network,)
    assert len(result.conflicts) == 1
    assert result.conflicts[0].winning_rule_id == "network.deny"
    assert result.conflicts[0].losing_rule_ids == ("network.allow",)
    assert result.conflicts[0].severity == PolicySeverity.CRITICAL


def test_context_filters_scope_and_key():
    context_rule = PolicyRule(
        rule_id="context.max_tokens",
        key="max_tokens",
        effect=PolicyEffect.SET_LIMIT,
        scope=PolicyScope.CONTEXT,
        value=2048,
    )
    model_rule = PolicyRule(
        rule_id="model.local",
        key="model",
        effect=PolicyEffect.PREFER,
        scope=PolicyScope.MODEL,
        value="local",
    )
    policy_set = PolicySet(
        policy_set_id="mixed",
        name="Politicas mistas",
        source=PolicySource.FRAMEWORK_SPEC,
        rules=(context_rule, model_rule),
    )

    result = DeterministicPolicyEngine().resolve(
        [policy_set],
        PolicyEvaluationContext(target_scope=PolicyScope.CONTEXT, requested_keys=("max_tokens",)),
    )

    assert result.resolved_policy_set.resolved_rules == (context_rule,)


def test_resolution_is_repeatable_with_same_input():
    rules = (
        PolicyRule(rule_id="tokens.task", key="max_tokens", effect=PolicyEffect.SET_LIMIT, priority=5, value=2000),
        PolicyRule(rule_id="tokens.mission", key="max_tokens", effect=PolicyEffect.SET_LIMIT, priority=10, value=8000),
    )
    policy_set = PolicySet(
        policy_set_id="tokens",
        name="Tokens",
        source=PolicySource.FRAMEWORK_SPEC,
        rules=rules,
    )
    engine = DeterministicPolicyEngine()

    first = engine.resolve([policy_set])
    second = engine.resolve([policy_set])

    assert first.ordered_policy_set_ids == second.ordered_policy_set_ids
    assert first.resolved_policy_set.resolved_rules == second.resolved_policy_set.resolved_rules
    assert first.resolved_policy_set.effective_values == second.resolved_policy_set.effective_values
    assert [(conflict.winning_rule_id, conflict.losing_rule_ids) for conflict in first.conflicts] == [
        (conflict.winning_rule_id, conflict.losing_rule_ids) for conflict in second.conflicts
    ]


def test_policy_engine_does_not_import_or_depend_on_guardian_for_resolution():
    sys.modules.pop("vercosa_ai_framework.guardian", None)
    before = set(sys.modules)

    result = DeterministicPolicyEngine().resolve([])

    imported_after_resolution = set(sys.modules) - before
    assert result.resolved_policy_set.resolved_rules == ()
    assert "vercosa_ai_framework.guardian" not in imported_after_resolution


def test_policy_engine_uses_no_external_clients():
    forbidden_modules = (
        "requests",
        "httpx",
        "psycopg",
        "psycopg2",
        "openai",
        "google.generativeai",
        "anthropic",
        "ollama",
    )
    before = set(sys.modules)


    DeterministicPolicyEngine().resolve([])

    imported_after_resolution = set(sys.modules) - before
    assert not set(forbidden_modules).intersection(imported_after_resolution)
