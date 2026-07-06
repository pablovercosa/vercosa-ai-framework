import socket

from vercosa_ai_framework.context import (
    ContextCitation,
    ContextItem,
    ContextItemType,
    ContextOmissionReason,
    ContextPackage,
    ContextRedaction,
    ContextRiskLevel,
    ContextSource,
    ContextSourceType,
    TokenBudgetDecision,
    TokenEstimate,
)
from vercosa_ai_framework.guardian import GuardianAction, GuardianEngine


def test_safe_context_package_returns_allow() -> None:
    package = _safe_package()

    decision = GuardianEngine().evaluate_context_package(package)

    assert decision.decision == GuardianAction.ALLOW
    assert decision.metadata["context_package_id"] == package.context_package_id
    assert "context_package.deterministic_checks" in decision.matched_policies


def test_item_without_traceable_citation_generates_warning_or_approval() -> None:
    source = ContextSource(source_id="src-1", source_type=ContextSourceType.SPEC, trust_level="high", content_hash="hash-src")
    item = ContextItem(context_item_id="item-1", source_ref="src-1", content="Trecho sem citacao.", item_type=ContextItemType.EXCERPT)
    package = _package(items=(item,), sources=(source,))

    decision = GuardianEngine().evaluate_context_package(package)

    assert decision.decision in {GuardianAction.WARN, GuardianAction.REQUIRE_APPROVAL}
    assert "context.traceability.item_citation_missing" in decision.matched_policies


def test_unknown_source_generates_warning() -> None:
    citation = ContextCitation(citation_id="cite-1", source_ref="src-unknown", path="docs/origem.md")
    source = ContextSource(source_id="src-unknown", source_type=ContextSourceType.UNKNOWN, trust_level="unknown", uri="docs/origem.md")
    item = ContextItem(context_item_id="item-1", source_ref="src-unknown", content="Trecho.", citations=(citation,))
    package = _package(items=(item,), sources=(source,), citations=(citation,))

    decision = GuardianEngine().evaluate_context_package(package)

    assert decision.decision == GuardianAction.WARN
    assert "context.source.unknown_or_low_trust" in decision.matched_policies


def test_inconsistent_budget_generates_guardian_decision() -> None:
    package = _safe_package(
        token_estimate=TokenEstimate(estimated_tokens=120),
        metadata={"available_context_tokens": 100, "used_context_tokens": 90},
        model_requirements={"estimated_context_tokens": 110, "minimum_context_window": 130},
    )

    decision = GuardianEngine().evaluate_context_package(package)

    assert decision.decision == GuardianAction.BLOCK
    assert "context.budget.exceeded" in decision.matched_policies
    assert "context.budget.inconsistent_used_tokens" in decision.matched_policies


def test_pending_or_suspicious_redaction_is_detected() -> None:
    redaction = ContextRedaction(
        redaction_id="redaction-1",
        redaction_type="secret",
        target_ref="item-1",
        reason="pending review",
        replacement="[REDACTED]",
    )
    package = _safe_package(redactions=(redaction,))

    decision = GuardianEngine().evaluate_context_package(package)

    assert decision.decision == GuardianAction.REQUIRE_APPROVAL
    assert "context.redaction.pending_or_suspicious" in decision.matched_policies
    assert "redaction-1" in decision.redactions_applied


def test_critical_omission_reason_is_detected() -> None:
    omission = TokenBudgetDecision(
        item_ref="omitted-1",
        included=False,
        token_estimate=TokenEstimate(estimated_tokens=10),
        tokens_before=0,
        tokens_after=0,
        available_context_tokens=100,
        omission_reason=ContextOmissionReason.PROMPT_INJECTION_RISK,
        reason="prompt_injection_risk",
    )
    package = _package(omission_reasons=(omission,))

    decision = GuardianEngine().evaluate_context_package(package)

    assert decision.decision == GuardianAction.BLOCK
    assert "context.omission.prompt_injection_risk" in decision.matched_policies


def test_sensitive_context_item_is_detected() -> None:
    citation = ContextCitation(citation_id="cite-1", source_ref="src-1", path="docs/sensivel.md")
    source = ContextSource(source_id="src-1", source_type=ContextSourceType.CANONICAL_DOCUMENT, trust_level="high", uri="docs/sensivel.md")
    item = ContextItem(
        context_item_id="item-sensitive",
        source_ref="src-1",
        content="Conteudo sensivel.",
        citations=(citation,),
        sensitivity="confidential",
        risk_level=ContextRiskLevel.HIGH,
    )
    package = _package(items=(item,), sources=(source,), citations=(citation,))

    decision = GuardianEngine().evaluate_context_package(package)

    assert decision.decision == GuardianAction.REQUIRE_APPROVAL
    assert "context.item.sensitive" in decision.matched_policies


def test_context_package_evaluation_is_deterministic_for_decision_fields() -> None:
    engine = GuardianEngine()
    package = _safe_package(warnings=("context_item_without_citation:item-1",))

    first = engine.evaluate_context_package(package)
    second = engine.evaluate_context_package(package)

    assert first.decision == second.decision
    assert first.risk_level == second.risk_level
    assert first.matched_policies == second.matched_policies
    assert first.reasons == second.reasons
    assert first.violations == second.violations


def test_context_package_evaluation_does_not_require_external_calls(monkeypatch) -> None:
    def fail_socket(*args, **kwargs):  # noqa: ANN001, ANN002, ANN003
        raise AssertionError("network access is not allowed")

    monkeypatch.setattr(socket, "socket", fail_socket)

    decision = GuardianEngine().evaluate_context_package(_safe_package())

    assert decision.decision == GuardianAction.ALLOW


def _safe_package(**overrides) -> ContextPackage:
    citation = ContextCitation(citation_id="cite-1", source_ref="src-1", path="specs/framework/0014.md", content_hash="hash-src")
    source = ContextSource(
        source_id="src-1",
        source_type=ContextSourceType.SPEC,
        domain="specs",
        uri="specs/framework/0014.md",
        content_hash="hash-src",
        trust_level="high",
    )
    item = ContextItem(
        context_item_id="item-1",
        source_ref="src-1",
        content="Context Router monta ContextPackage rastreavel.",
        citations=(citation,),
        trust_level="high",
        is_untrusted_data=False,
    )
    defaults = {
        "items": (item,),
        "sources": (source,),
        "citations": (citation,),
        "token_estimate": TokenEstimate(estimated_tokens=12),
        "output_token_reservation": 20,
        "model_requirements": {"estimated_context_tokens": 12, "minimum_context_window": 32},
        "content_hash": "hash-package",
        "metadata": {"available_context_tokens": 100, "used_context_tokens": 12},
    }
    defaults.update(overrides)
    return _package(**defaults)


def _package(**overrides) -> ContextPackage:
    defaults = {
        "context_package_id": "pkg-1",
        "request_id": "req-1",
        "request_goal": "Avaliar pacote de contexto",
        "scope": "unit-test",
        "content_hash": "hash-package",
        "token_estimate": TokenEstimate(estimated_tokens=0),
        "model_requirements": {"estimated_context_tokens": 0, "minimum_context_window": 0},
        "metadata": {"available_context_tokens": 100, "used_context_tokens": 0},
    }
    defaults.update(overrides)
    return ContextPackage(**defaults)
