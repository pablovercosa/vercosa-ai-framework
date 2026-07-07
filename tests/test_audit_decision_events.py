from __future__ import annotations

import socket
import sys

from vercosa_ai_framework.audit import (
    EventCategory,
    EventResult,
    EventSeverity,
    InMemoryEventLog,
    context_package_event,
    guardian_decision_event,
    policy_resolution_event,
    record_context_package_event,
    record_guardian_decision_event,
    record_policy_resolution_event,
)
from vercosa_ai_framework.context import (
    ContextCitation,
    ContextItem,
    ContextOmissionReason,
    ContextPackage,
    ContextRequest,
    ContextSource,
    ContextSourceType,
    DeterministicContextRouter,
    TokenBudget,
)
from vercosa_ai_framework.guardian import GuardianAction, GuardianEngine, GuardianEvaluationContext
from vercosa_ai_framework.policy import (
    DeterministicPolicyEngine,
    PolicyEffect,
    PolicyRule,
    PolicyScope,
    PolicySet,
    PolicySeverity,
    PolicySource,
)


def test_policy_resolution_event_has_policy_category_and_counts() -> None:
    result = _policy_result(effect=PolicyEffect.WARN, rule_id="policy.warn")

    event = policy_resolution_event(result, considered_policy_count=1, metadata={"mission_id": "m-1"})

    assert event.category is EventCategory.POLICY
    assert event.name == "policy.resolution"
    assert event.severity is EventSeverity.WARNING
    assert event.result is EventResult.WARNING
    assert event.metadata["policy_sets_considered"] == 1
    assert event.metadata["policies_resolved"] == 1
    assert event.metadata["matched_policy_refs"] == ("policy.warn",)
    assert event.metadata["mission_id"] == "m-1"


def test_policy_resolution_event_marks_require_approval_result() -> None:
    result = _policy_result(effect=PolicyEffect.REQUIRE_APPROVAL, rule_id="policy.approval")

    event = policy_resolution_event(result)

    assert event.severity is EventSeverity.WARNING
    assert event.result is EventResult.REQUIRES_APPROVAL
    assert event.metadata["require_approval_refs"] == ("policy.approval",)


def test_policy_resolution_event_records_conflicts_without_raw_policy_content() -> None:
    allow = PolicyRule(rule_id="network.allow", key="network", effect=PolicyEffect.ALLOW, priority=1, value="external")
    deny = PolicyRule(
        rule_id="network.deny",
        key="network",
        effect=PolicyEffect.DENY,
        severity=PolicySeverity.CRITICAL,
        priority=10,
        value="external",
    )
    result = DeterministicPolicyEngine().resolve(
        [PolicySet(policy_set_id="network", name="Rede", source=PolicySource.PROJECT_SPEC, rules=(allow, deny))]
    )

    event = policy_resolution_event(result, metadata={"prompt": "texto bruto sensivel", "safe_ref": "spec-1"})

    assert event.severity is EventSeverity.ERROR
    assert event.result is EventResult.WARNING
    assert event.metadata["conflicts_count"] == 1
    assert event.metadata["conflict_refs"] == (result.conflicts[0].conflict_id,)
    assert event.metadata["safe_ref"] == "spec-1"
    assert "prompt" not in event.metadata
    assert "texto bruto sensivel" not in repr(event.metadata)


def test_guardian_decision_event_has_guardian_category_and_blocked_result() -> None:
    decision = GuardianEngine().evaluate(
        GuardianEvaluationContext(
            mission_id="m-guardian",
            evaluation_id="eval-guardian",
            evaluation_type="mission_pre_execution",
            mission_goal="Atualizar docs com entregaveis e criterios de aceite.",
            planned_command="rm -rf /",
            metadata={"deliverables": "docs", "acceptance_criteria": "pytest"},
        )
    )

    event = guardian_decision_event(decision, origin="unit-test", metadata={"mission_id": "m-guardian"})

    assert event.category is EventCategory.GUARDIAN
    assert event.severity is EventSeverity.ERROR
    assert event.result is EventResult.BLOCKED
    assert event.metadata["decision"] == GuardianAction.BLOCK.value
    assert event.metadata["origin"] == "unit-test"
    assert event.metadata["blocked"] is True
    assert event.metadata["violations_count"] >= 1


def test_guardian_decision_event_marks_require_approval() -> None:
    decision = GuardianEngine().evaluate(
        GuardianEvaluationContext(
            mission_id="m-approval",
            evaluation_id="eval-approval",
            evaluation_type="mission_pre_execution",
            mission_goal="Atualizar docs com entregaveis e criterios de aceite.",
            planned_command="sudo true",
            metadata={"deliverables": "docs", "acceptance_criteria": "pytest"},
        )
    )

    event = guardian_decision_event(decision)

    assert event.category is EventCategory.GUARDIAN
    assert event.severity is EventSeverity.WARNING
    assert event.result is EventResult.REQUIRES_APPROVAL
    assert event.metadata["requires_approval"] is True


def test_context_package_event_has_context_category_and_package_counts() -> None:
    package = _context_package_with_omission()

    event = context_package_event(package, candidate_count=2, metadata={"mission_id": "m-context"})

    assert event.category is EventCategory.CONTEXT
    assert event.severity is EventSeverity.WARNING
    assert event.result is EventResult.WARNING
    assert event.metadata["candidate_count"] == 2
    assert event.metadata["selected_items_count"] == 1
    assert event.metadata["omitted_items_count"] == 1
    assert event.metadata["estimated_context_tokens"] == package.token_estimate.estimated_tokens
    assert event.metadata["omission_reasons"] == {ContextOmissionReason.DUPLICATE.value: 1}
    assert event.metadata["mission_id"] == "m-context"


def test_context_package_event_marks_require_approval_from_package_metadata() -> None:
    package = ContextPackage(
        context_package_id="pkg-review",
        request_id="req-review",
        request_goal="Montar contexto",
        scope="unit-test",
        metadata={"requires_approval": True, "approval_policy_refs": ("context.review",)},
        warnings=("policy_requires_approval:context.review",),
    )

    event = context_package_event(package)

    assert event.category is EventCategory.CONTEXT
    assert event.severity is EventSeverity.WARNING
    assert event.result is EventResult.REQUIRES_APPROVAL
    assert event.metadata["approval_policy_refs"] == ("context.review",)


def test_context_package_event_does_not_include_raw_context_content() -> None:
    package = _context_package_with_omission()

    event = context_package_event(package, metadata={"raw_content": "segredo bruto", "safe_ref": "pkg-ref"})

    assert event.metadata["safe_ref"] == "pkg-ref"
    assert "raw_content" not in event.metadata
    assert "conteudo citavel" not in repr(event.metadata)
    assert "segredo bruto" not in repr(event.metadata)


def test_decision_event_helpers_are_deterministic_for_same_input() -> None:
    policy_result = _policy_result(effect=PolicyEffect.REQUIRE_APPROVAL, rule_id="policy.repeat")
    guardian_decision = GuardianEngine().evaluate(
        GuardianEvaluationContext(
            mission_id="m-repeat",
            evaluation_id="eval-repeat",
            evaluation_type="mission_pre_execution",
            mission_goal="Atualizar docs com entregaveis e criterios de aceite.",
            metadata={"deliverables": "docs", "acceptance_criteria": "pytest"},
        )
    )
    context_package = _context_package_with_omission()

    assert policy_resolution_event(policy_result) == policy_resolution_event(policy_result)
    assert guardian_decision_event(guardian_decision) == guardian_decision_event(guardian_decision)
    assert context_package_event(context_package, candidate_count=2) == context_package_event(context_package, candidate_count=2)


def test_record_helpers_are_optional_and_record_only_when_log_is_provided() -> None:
    policy_result = _policy_result(effect=PolicyEffect.ALLOW, rule_id="policy.allow")
    guardian_decision = GuardianEngine().evaluate(
        GuardianEvaluationContext(
            mission_id="m-optional",
            evaluation_id="eval-optional",
            evaluation_type="mission_pre_execution",
            mission_goal="Atualizar docs com entregaveis e criterios de aceite.",
            metadata={"deliverables": "docs", "acceptance_criteria": "pytest"},
        )
    )
    context_package = _context_package_with_omission()
    event_log = InMemoryEventLog()

    unrecorded = record_policy_resolution_event(policy_result)
    assert unrecorded.category is EventCategory.POLICY
    assert event_log.list_events() == ()

    record_policy_resolution_event(policy_result, event_log=event_log)
    record_guardian_decision_event(guardian_decision, event_log=event_log)
    record_context_package_event(context_package, event_log=event_log, candidate_count=2)

    assert [event.category for event in event_log.list_events()] == [
        EventCategory.POLICY,
        EventCategory.GUARDIAN,
        EventCategory.CONTEXT,
    ]


def test_existing_module_calls_continue_to_work_without_event_log() -> None:
    policy_result = DeterministicPolicyEngine().resolve([])
    guardian_decision = GuardianEngine().validate_mission_text(
        "Atualizar documentação com entregaveis e criterios de aceite.",
        metadata={"deliverables": "docs", "acceptance_criteria": "pytest"},
    )
    context_package = DeterministicContextRouter().route(
        ContextRequest(request_id="req-existing", request_goal="sem candidatos")
    )

    assert policy_result.resolved_policy_set.resolved_rules == ()
    assert guardian_decision.decision in {GuardianAction.ALLOW, GuardianAction.WARN}
    assert context_package.items == ()


def test_audit_decision_events_do_not_use_network(monkeypatch) -> None:
    def fail_socket(*args, **kwargs):  # noqa: ANN001, ANN002, ANN003
        raise AssertionError("network access is not allowed")

    monkeypatch.setattr(socket, "socket", fail_socket)

    event = policy_resolution_event(_policy_result(effect=PolicyEffect.ALLOW, rule_id="policy.local"))

    assert event.category is EventCategory.POLICY


def test_audit_decision_events_require_no_new_external_dependency() -> None:
    forbidden_modules = {
        "requests",
        "httpx",
        "psycopg",
        "psycopg2",
        "openai",
        "google.generativeai",
        "anthropic",
        "ollama",
        "opentelemetry",
    }
    before = set(sys.modules)

    policy_resolution_event(_policy_result(effect=PolicyEffect.ALLOW, rule_id="policy.no-deps"))

    imported_after_event = set(sys.modules) - before
    assert not forbidden_modules.intersection(imported_after_event)


def _policy_result(*, effect: PolicyEffect, rule_id: str):
    rule = PolicyRule(
        rule_id=rule_id,
        key="audit",
        effect=effect,
        scope=PolicyScope.GLOBAL,
        source=PolicySource.PROJECT_SPEC,
    )
    return DeterministicPolicyEngine().resolve(
        [PolicySet(policy_set_id="policy-set", name="Politicas", source=PolicySource.PROJECT_SPEC, rules=(rule,))]
    )


def _context_package_with_omission():
    source = ContextSource(source_id="src-1", source_type=ContextSourceType.SPEC)
    citation = ContextCitation(citation_id="cite-1", source_ref="src-1", path="specs/framework/0014.md")
    first = ContextItem(context_item_id="item-1", source_ref="src-1", content="conteudo citavel", citations=(citation,))
    duplicate = ContextItem(context_item_id="item-2", source_ref="src-1", content="conteudo citavel", citations=(citation,))
    request = ContextRequest(
        request_id="req-context-audit",
        request_goal="montar contexto",
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
        candidate_sources=(source,),
        candidate_items=(first, duplicate),
    )
    return DeterministicContextRouter().route(request)
