"""Context Router contracts and deterministic MVP implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod

from dataclasses import replace

from vercosa_ai_framework.context.budget import SimpleTokenBudgetManager, TokenBudgetManager
from vercosa_ai_framework.context.types import (
    ContextCitation,
    ContextItem,
    ContextItemType,
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
from vercosa_ai_framework.policy.types import PolicyConflict, PolicyEffect, PolicyRule, PolicySeverity, ResolvedPolicySet


class ContextRouter(ABC):
    """Abstract boundary for building governed context packages."""

    @abstractmethod
    def route(self, request: ContextRequest, candidates: tuple[ContextItem, ...] | None = None) -> ContextPackage:
        """Produce a context package from explicit candidates."""


class DeterministicContextRouter(ContextRouter):
    """Simple router that deduplicates explicit candidates and applies budget."""

    def __init__(self, budget_manager: TokenBudgetManager | None = None) -> None:
        self.budget_manager = budget_manager or SimpleTokenBudgetManager()

    def route(self, request: ContextRequest, candidates: tuple[ContextItem, ...] | None = None) -> ContextPackage:
        selected_items: list[ContextItem] = []
        omitted: list[TokenBudgetDecision] = []
        seen_item_ids: set[str] = set()
        seen_hashes: set[str] = set()
        seen_contents: set[str] = set()
        warnings: list[str] = []
        used_tokens = 0
        resolved_policy_set = request.resolved_policy_set
        policy_refs = _policy_refs(request.policy_refs, resolved_policy_set)
        denied_rules = _context_denied_rules(resolved_policy_set)
        approval_policy_refs = _approval_policy_refs(resolved_policy_set)
        blocked_policy_refs = _untargeted_denied_policy_refs(denied_rules)
        if resolved_policy_set is not None:
            warnings.extend(_policy_warnings(resolved_policy_set))

        explicit_candidates = request.candidate_items if candidates is None else candidates

        for item in sorted(explicit_candidates, key=_candidate_sort_key):
            denied_rule = _matching_denied_rule(item, denied_rules)
            if denied_rule is not None:
                omitted.append(_omitted_policy_denied(item, request.token_budget, used_tokens, self.budget_manager.estimate_item(item), denied_rule))
                continue

            if _is_duplicate(item, seen_item_ids, seen_hashes, seen_contents):
                omitted.append(_omitted_duplicate(item, request.token_budget, used_tokens, self.budget_manager.estimate_item(item)))
                continue

            _remember_item(item, seen_item_ids, seen_hashes, seen_contents)

            if not item.citations:
                if _requires_citation(item) or (request.citation_required and not _allows_missing_citation(item)):
                    omitted.append(_omitted_missing_citation(item, request.token_budget, used_tokens, self.budget_manager.estimate_item(item)))
                    continue
                if not _allows_missing_citation(item):
                    warnings.append(f"context_item_without_citation:{item.context_item_id}")

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
        budget_result = self.budget_manager.evaluate_items(tuple(selected_items), request.token_budget)

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
            policy_refs=policy_refs,
            guardian_decision_refs=request.guardian_decision_refs,
            model_requirements={
                "minimum_context_window": used_tokens + request.token_budget.reserved_output_tokens,
                "estimated_context_tokens": used_tokens,
                "reserved_output_tokens": request.token_budget.reserved_output_tokens,
            },
            content_hash=content_hash,
            cache_key=stable_id("context_cache", request.request_id, content_hash, policy_refs),
            warnings=tuple(warnings),
            metadata={
                "router": "deterministic",
                "omitted_count": len(omitted),
                "available_context_tokens": request.token_budget.available_context_tokens,
                "used_context_tokens": used_tokens,
                "remaining_context_tokens": max(0, request.token_budget.available_context_tokens - used_tokens),
                "accepted_items": tuple(item.context_item_id for item in selected_items),
                "budget_result": budget_result,
                "policy_resolution_id": resolved_policy_set.resolution_id if resolved_policy_set is not None else None,
                "requires_approval": bool(approval_policy_refs),
                "approval_policy_refs": approval_policy_refs,
                "blocked_policy_refs": blocked_policy_refs,
            },
        )


def _policy_refs(existing_refs: tuple[str, ...], resolved_policy_set: ResolvedPolicySet | None) -> tuple[str, ...]:
    refs = list(existing_refs)
    if resolved_policy_set is not None:
        refs.extend(rule.rule_id for rule in resolved_policy_set.resolved_rules)
        refs.extend(conflict.conflict_id for conflict in resolved_policy_set.conflicts)
    return tuple(dict.fromkeys(refs))


def _policy_warnings(resolved_policy_set: ResolvedPolicySet) -> tuple[str, ...]:
    warnings: list[str] = []
    warnings.extend(f"policy_warning:{warning}" for warning in resolved_policy_set.warnings)
    for rule in resolved_policy_set.resolved_rules:
        if rule.effect is PolicyEffect.WARN:
            warnings.append(f"policy_warn:{rule.rule_id}")
        elif rule.effect is PolicyEffect.REQUIRE_APPROVAL:
            warnings.append(f"policy_requires_approval:{rule.rule_id}")
    for conflict in resolved_policy_set.conflicts:
        warnings.append(_conflict_warning(conflict))
    return tuple(dict.fromkeys(warnings))


def _conflict_warning(conflict: PolicyConflict) -> str:
    if conflict.severity in {PolicySeverity.HIGH, PolicySeverity.CRITICAL}:
        return f"policy_conflict_requires_approval:{conflict.conflict_id}"
    return f"policy_conflict_warn:{conflict.conflict_id}"


def _approval_policy_refs(resolved_policy_set: ResolvedPolicySet | None) -> tuple[str, ...]:
    if resolved_policy_set is None:
        return ()
    refs = [rule.rule_id for rule in resolved_policy_set.resolved_rules if rule.effect is PolicyEffect.REQUIRE_APPROVAL]
    refs.extend(
        conflict.conflict_id
        for conflict in resolved_policy_set.conflicts
        if conflict.severity in {PolicySeverity.HIGH, PolicySeverity.CRITICAL}
    )
    return tuple(dict.fromkeys(refs))


def _context_denied_rules(resolved_policy_set: ResolvedPolicySet | None) -> tuple[PolicyRule, ...]:
    if resolved_policy_set is None:
        return ()
    return tuple(rule for rule in resolved_policy_set.resolved_rules if rule.effect is PolicyEffect.DENY and rule.scope.value in {"global", "context"})


def _untargeted_denied_policy_refs(denied_rules: tuple[PolicyRule, ...]) -> tuple[str, ...]:
    return tuple(rule.rule_id for rule in denied_rules if not _has_deterministic_context_target(rule))


def _matching_denied_rule(item: ContextItem, denied_rules: tuple[PolicyRule, ...]) -> PolicyRule | None:
    for rule in denied_rules:
        if _rule_targets_item(rule, item):
            return rule
    return None


def _rule_targets_item(rule: PolicyRule, item: ContextItem) -> bool:
    targets = set(rule.target_refs)
    if item.context_item_id in targets or item.source_ref in targets:
        return True
    if isinstance(rule.value, str) and rule.value in {item.context_item_id, item.source_ref, item.item_type.value, item.sensitivity}:
        return True
    return False


def _has_deterministic_context_target(rule: PolicyRule) -> bool:
    return bool(rule.target_refs) or isinstance(rule.value, str)


def _omitted_policy_denied(
    item: ContextItem,
    budget,
    used_tokens: int,
    estimate: TokenEstimate,
    rule: PolicyRule,
) -> TokenBudgetDecision:
    return TokenBudgetDecision(
        item_ref=item.context_item_id,
        included=False,
        token_estimate=estimate,
        tokens_before=used_tokens,
        tokens_after=used_tokens,
        available_context_tokens=budget.available_context_tokens,
        omission_reason=ContextOmissionReason.POLICY_DENIED,
        reason=f"policy_denied:{rule.rule_id}",
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


def _omitted_missing_citation(
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
        omission_reason=ContextOmissionReason.MISSING_CITATION,
        reason="missing_required_citation",
    )


def _candidate_sort_key(item: ContextItem) -> tuple[int, int, str, str, str]:
    priority = item.metadata.get("priority", 0)
    if not isinstance(priority, int):
        priority = 0
    return (item.rank, priority, item.source_ref, item.context_item_id, item.content_hash or stable_content_hash(item.content))


def _is_duplicate(
    item: ContextItem,
    seen_item_ids: set[str],
    seen_hashes: set[str],
    seen_contents: set[str],
) -> bool:
    return (
        bool(item.context_item_id and item.context_item_id in seen_item_ids)
        or bool(item.content_hash and item.content_hash in seen_hashes)
        or bool(item.content and item.content in seen_contents)
    )


def _remember_item(
    item: ContextItem,
    seen_item_ids: set[str],
    seen_hashes: set[str],
    seen_contents: set[str],
) -> None:
    if item.context_item_id:
        seen_item_ids.add(item.context_item_id)
    if item.content_hash:
        seen_hashes.add(item.content_hash)
    if item.content:
        seen_contents.add(item.content)


def _requires_citation(item: ContextItem) -> bool:
    return item.item_type is ContextItemType.EVIDENCE


def _allows_missing_citation(item: ContextItem) -> bool:
    return item.item_type in {
        ContextItemType.INSTRUCTION,
        ContextItemType.METADATA,
    }


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
