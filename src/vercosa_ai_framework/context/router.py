"""Context Router contracts and deterministic MVP implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod

from dataclasses import replace

from vercosa_ai_framework.context.budget import SimpleTokenBudgetManager, TokenBudgetManager
from vercosa_ai_framework.context.types import (
    ContextCitation,
    ContextItem,
    ContextOmissionReason,
    ContextPackage,
    ContextRedaction,
    ContextRequest,
    ContextSource,
    TokenBudgetDecision,
    TokenEstimate,
    stable_content_hash,
    stable_id,
)


class ContextRouter(ABC):
    """Abstract boundary for building governed context packages."""

    @abstractmethod
    def route(self, request: ContextRequest) -> ContextPackage:
        """Produce a context package from explicit candidates."""


class DeterministicContextRouter(ContextRouter):
    """Simple router that deduplicates explicit candidates and applies budget."""

    def __init__(self, budget_manager: TokenBudgetManager | None = None) -> None:
        self.budget_manager = budget_manager or SimpleTokenBudgetManager()

    def route(self, request: ContextRequest) -> ContextPackage:
        selected_items: list[ContextItem] = []
        omitted: list[TokenBudgetDecision] = []
        seen_keys: set[str] = set()
        used_tokens = 0

        for item in sorted(request.candidate_items, key=lambda candidate: (candidate.rank, candidate.context_item_id)):
            dedupe_key = item.content_hash or item.context_item_id
            if dedupe_key in seen_keys:
                omitted.append(_omitted_duplicate(item, request.token_budget, used_tokens, self.budget_manager.estimate_item(item)))
                continue
            seen_keys.add(dedupe_key)

            decision = self.budget_manager.decide_item(item, request.token_budget, used_tokens)
            if not decision.included:
                omitted.append(decision)
                continue

            estimate = decision.token_estimate
            selected_items.append(replace(item, token_estimate=estimate))
            used_tokens = decision.tokens_after

        selected_source_refs = {item.source_ref for item in selected_items}
        sources = tuple(source for source in request.candidate_sources if source.source_id in selected_source_refs)
        citations = _unique_citations(selected_items)
        redactions = _unique_redactions(selected_items)
        content_hash = _package_content_hash(selected_items)
        package_id = stable_id("context_package", request.request_id, content_hash, used_tokens, request.token_budget.reserved_output_tokens)

        return ContextPackage(
            context_package_id=package_id,
            request_id=request.request_id,
            request_goal=request.request_goal,
            scope=request.scope,
            items=tuple(selected_items),
            sources=sources,
            citations=citations,
            token_estimate=TokenEstimate(
                estimated_tokens=used_tokens,
                estimation_method="sum_item_estimates",
                confidence="low",
                content_chars=sum(len(item.content) for item in selected_items),
            ),
            output_token_reservation=request.token_budget.reserved_output_tokens,
            redactions=redactions,
            omission_reasons=tuple(omitted),
            policy_refs=request.policy_refs,
            guardian_decision_refs=request.guardian_decision_refs,
            model_requirements={
                "minimum_context_window": used_tokens + request.token_budget.reserved_output_tokens,
                "estimated_context_tokens": used_tokens,
                "reserved_output_tokens": request.token_budget.reserved_output_tokens,
            },
            content_hash=content_hash,
            cache_key=stable_id("context_cache", request.request_id, content_hash, tuple(request.policy_refs)),
            warnings=(),
            metadata={"router": "deterministic", "omitted_count": len(omitted)},
        )


def _omitted_duplicate(
    item: ContextItem,
    budget,
    used_tokens: int,
    estimate: TokenEstimate,
) -> TokenBudgetDecision:
    return TokenBudgetDecision(
        item_ref=item.context_item_id,
        included=False,
        token_estimate=estimate,
        tokens_before=used_tokens,
        tokens_after=used_tokens,
        available_context_tokens=budget.available_context_tokens,
        omission_reason=ContextOmissionReason.DUPLICATE,
        reason="duplicate_context_item",
    )


def _unique_citations(items: list[ContextItem]) -> tuple[ContextCitation, ...]:
    citations: list[ContextCitation] = []
    seen: set[str] = set()
    for item in items:
        for citation in item.citations:
            if citation.citation_id in seen:
                continue
            seen.add(citation.citation_id)
            citations.append(citation)
    return tuple(citations)


def _unique_redactions(items: list[ContextItem]) -> tuple[ContextRedaction, ...]:
    redactions: list[ContextRedaction] = []
    seen: set[str] = set()
    for item in items:
        for redaction in item.redactions:
            if redaction.redaction_id in seen:
                continue
            seen.add(redaction.redaction_id)
            redactions.append(redaction)
    return tuple(redactions)


def _package_content_hash(items: list[ContextItem]) -> str:
    content = "\n".join(f"{item.context_item_id}:{item.content_hash or stable_content_hash(item.content)}" for item in items)
    return stable_content_hash(content)


__all__ = ["ContextRouter", "DeterministicContextRouter"]
