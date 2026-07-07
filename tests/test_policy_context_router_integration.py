from __future__ import annotations

import socket
import sys

from vercosa_ai_framework.context import (
    ContextCitation,
    ContextItem,
    ContextItemType,
    ContextOmissionReason,
    ContextRequest,
    ContextSource,
    ContextSourceType,
    DeterministicContextRouter,
    TokenBudget,
)
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


def _source() -> ContextSource:
    return ContextSource(source_id="src-1", source_type=ContextSourceType.SPEC, trust_level="high")


def _citation() -> ContextCitation:
    return ContextCitation(citation_id="cite-1", source_ref="src-1", path="specs/framework/0014.md")


def _item(item_id: str = "item-1", content: str = "conteudo citavel") -> ContextItem:
    return ContextItem(context_item_id=item_id, source_ref="src-1", content=content, citations=(_citation(),))


def _request(resolved_policy_set: ResolvedPolicySet | None = None, item: ContextItem | None = None) -> ContextRequest:
    return ContextRequest(
        request_id="req-policy-context",
        request_goal="montar contexto governado",
        token_budget=TokenBudget(max_input_tokens=80, reserved_output_tokens=10),
        candidate_sources=(_source(),),
        candidate_items=(item or _item(),),
        resolved_policy_set=resolved_policy_set,
    )


def _resolved_rule(
    effect: PolicyEffect,
    *,
    rule_id: str | None = None,
    target_refs: tuple[str, ...] = (),
    value: object | None = None,
    severity: PolicySeverity = PolicySeverity.MEDIUM,
) -> ResolvedPolicySet:
    rule = PolicyRule(
        rule_id=rule_id or f"context.{effect.value}",
        key="context_item",
        effect=effect,
        scope=PolicyScope.CONTEXT,
        source=PolicySource.PROJECT_SPEC,
        severity=severity,
        priority=10,
        value=value,
        target_refs=target_refs,
    )
    return ResolvedPolicySet(resolved_rules=(rule,))


def test_context_router_without_resolved_policy_set_keeps_current_behavior() -> None:
    package = DeterministicContextRouter().route(_request())

    assert [item.context_item_id for item in package.items] == ["item-1"]
    assert package.policy_refs == ()
    assert package.warnings == ()
    assert package.metadata["requires_approval"] is False


def test_allow_policy_does_not_block_or_change_selected_context() -> None:
    baseline = DeterministicContextRouter().route(_request())
    resolved = _resolved_rule(PolicyEffect.ALLOW, rule_id="context.allow")

    package = DeterministicContextRouter().route(_request(resolved))

    assert package.items == baseline.items
    assert package.omission_reasons == baseline.omission_reasons
    assert package.policy_refs == ("context.allow",)
    assert package.warnings == ()


def test_warn_policy_is_reflected_as_warning_and_policy_ref() -> None:
    resolved = _resolved_rule(PolicyEffect.WARN, rule_id="context.warn")

    package = DeterministicContextRouter().route(_request(resolved))

    assert [item.context_item_id for item in package.items] == ["item-1"]
    assert "context.warn" in package.policy_refs
    assert "policy_warn:context.warn" in package.warnings


def test_require_approval_policy_is_traceable_without_refactor() -> None:
    resolved = _resolved_rule(PolicyEffect.REQUIRE_APPROVAL, rule_id="context.review")

    package = DeterministicContextRouter().route(_request(resolved))

    assert package.metadata["requires_approval"] is True
    assert package.metadata["approval_policy_refs"] == ("context.review",)
    assert "policy_requires_approval:context.review" in package.warnings


def test_targeted_deny_policy_omits_matching_item() -> None:
    resolved = _resolved_rule(PolicyEffect.DENY, rule_id="context.deny.item", target_refs=("item-1",))

    package = DeterministicContextRouter().route(_request(resolved))

    assert package.items == ()
    assert package.omission_reasons[0].item_ref == "item-1"
    assert package.omission_reasons[0].omission_reason is ContextOmissionReason.POLICY_DENIED
    assert package.omission_reasons[0].reason == "policy_denied:context.deny.item"


def test_untargeted_deny_policy_is_signaled_without_ambiguous_omission() -> None:
    resolved = _resolved_rule(PolicyEffect.DENY, rule_id="context.deny.ambiguous")

    package = DeterministicContextRouter().route(_request(resolved))

    assert [item.context_item_id for item in package.items] == ["item-1"]
    assert package.omission_reasons == ()
    assert package.metadata["blocked_policy_refs"] == ("context.deny.ambiguous",)


def test_policy_conflict_is_considered_deterministically() -> None:
    conflict = PolicyConflict(
        key="context_item",
        scope=PolicyScope.CONTEXT,
        winning_rule_id="context.local",
        losing_rule_ids=("context.remote",),
        reason="politicas divergentes para contexto",
        severity=PolicySeverity.HIGH,
        conflict_id="conflict.context",
    )
    resolved = ResolvedPolicySet(resolved_rules=(), conflicts=(conflict,))

    package = DeterministicContextRouter().route(_request(resolved))

    assert "conflict.context" in package.policy_refs
    assert "policy_conflict_requires_approval:conflict.context" in package.warnings
    assert package.metadata["requires_approval"] is True


def test_token_budget_still_works_with_resolved_policy_set() -> None:
    item = _item(content="x" * 300)
    resolved = _resolved_rule(PolicyEffect.WARN, rule_id="context.warn.budget")

    package = DeterministicContextRouter().route(_request(resolved, item))

    assert package.items == ()
    assert package.omission_reasons[0].omission_reason is ContextOmissionReason.TOKEN_BUDGET_EXCEEDED
    assert "policy_warn:context.warn.budget" in package.warnings


def test_citations_are_preserved_with_resolved_policy_set() -> None:
    resolved = _resolved_rule(PolicyEffect.WARN, rule_id="context.warn.citation")

    package = DeterministicContextRouter().route(_request(resolved))

    assert package.items[0].citations == (_citation(),)
    assert package.citations == (_citation(),)


def test_existing_omission_reasons_are_preserved_with_policy_warnings() -> None:
    item = ContextItem(
        context_item_id="evidence",
        source_ref="src-1",
        content="evidencia sem citacao",
        item_type=ContextItemType.EVIDENCE,
    )
    resolved = _resolved_rule(PolicyEffect.WARN, rule_id="context.warn.omission")

    package = DeterministicContextRouter().route(_request(resolved, item))

    assert package.omission_reasons[0].omission_reason is ContextOmissionReason.MISSING_CITATION
    assert "policy_warn:context.warn.omission" in package.warnings


def test_policy_context_router_integration_is_repeatable() -> None:
    resolved = _resolved_rule(PolicyEffect.REQUIRE_APPROVAL, rule_id="context.review.repeat")
    request = _request(resolved)
    router = DeterministicContextRouter()

    assert router.route(request) == router.route(request)


def test_policy_resolution_can_feed_context_router_without_context_calling_policy_engine() -> None:
    rule = PolicyRule(
        rule_id="context.warn.engine",
        key="traceability",
        effect=PolicyEffect.WARN,
        scope=PolicyScope.CONTEXT,
    )
    result = DeterministicPolicyEngine().resolve(
        [PolicySet(policy_set_id="context", name="Contexto", source=PolicySource.PROJECT_SPEC, rules=(rule,))]
    )

    package = DeterministicContextRouter().route(_request(result.resolved_policy_set))

    assert package.policy_refs == ("context.warn.engine",)
    assert "policy_warn:context.warn.engine" in package.warnings


def test_integration_does_not_call_network(monkeypatch) -> None:
    def fail_socket(*args, **kwargs):  # noqa: ANN001, ANN002, ANN003
        raise AssertionError("network access is not allowed")

    monkeypatch.setattr(socket, "socket", fail_socket)
    resolved = _resolved_rule(PolicyEffect.WARN, rule_id="context.warn.no-network")

    package = DeterministicContextRouter().route(_request(resolved))

    assert package.metadata["router"] == "deterministic"


def test_policy_module_does_not_import_context_router() -> None:
    sys.modules.pop("vercosa_ai_framework.context", None)
    before = set(sys.modules)

    DeterministicPolicyEngine().resolve([])

    imported_after_resolution = set(sys.modules) - before
    assert "vercosa_ai_framework.context" not in imported_after_resolution
