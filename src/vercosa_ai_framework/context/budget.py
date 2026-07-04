"""Token Budget Manager contracts and deterministic MVP implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod

from vercosa_ai_framework.context.types import (
    ContextItem,
    ContextOmissionReason,
    TokenBudget,
    TokenBudgetDecision,
    TokenBudgetResult,
    TokenEstimate,
)


class TokenBudgetManager(ABC):
    """Abstract boundary for token estimation and budget decisions."""

    @abstractmethod
    def estimate_text(self, text: str) -> TokenEstimate:
        """Estimate token usage for plain text without calling external APIs."""

    @abstractmethod
    def estimate_item(self, item: ContextItem) -> TokenEstimate:
        """Estimate token usage for one context item."""

    @abstractmethod
    def available_context_tokens(self, budget: TokenBudget) -> int:
        """Return the input budget left after output and fixed reservations."""

    @abstractmethod
    def decide_item(
        self,
        item: ContextItem,
        budget: TokenBudget,
        used_context_tokens: int = 0,
    ) -> TokenBudgetDecision:
        """Return whether an item fits in the remaining context budget."""

    def evaluate_items(
        self,
        items: tuple[ContextItem, ...],
        budget: TokenBudget,
        used_context_tokens: int = 0,
    ) -> TokenBudgetResult:
        """Evaluate a deterministic sequence of items against the budget."""

        accepted: list[str] = []
        omitted: list[TokenBudgetDecision] = []
        used_tokens = used_context_tokens

        for item in items:
            decision = self.decide_item(item, budget, used_tokens)
            if decision.included:
                accepted.append(item.context_item_id)
                used_tokens = decision.tokens_after
            else:
                omitted.append(decision)

        return TokenBudgetResult(
            token_estimate=TokenEstimate(
                estimated_tokens=used_tokens,
                estimation_method="sum_item_estimates",
                confidence="low",
                content_chars=sum(len(item.content) for item in items if item.context_item_id in accepted),
            ),
            reserved_output_tokens=budget.reserved_output_tokens,
            available_context_tokens=self.available_context_tokens(budget),
            used_context_tokens=used_tokens,
            remaining_context_tokens=max(0, self.available_context_tokens(budget) - used_tokens),
            accepted_items=tuple(accepted),
            omitted_items=tuple(omitted),
        )


class SimpleTokenBudgetManager(TokenBudgetManager):
    """Deterministic token estimator based on a conservative char heuristic."""

    def __init__(self, chars_per_token: int = 4) -> None:
        if chars_per_token <= 0:
            raise ValueError("chars_per_token must be positive")
        self.chars_per_token = chars_per_token

    def estimate_text(self, text: str) -> TokenEstimate:
        content_chars = len(text)
        estimated_tokens = 0 if content_chars == 0 else (content_chars + self.chars_per_token - 1) // self.chars_per_token
        return TokenEstimate(
            estimated_tokens=estimated_tokens,
            estimation_method=f"chars_div_{self.chars_per_token}_ceil",
            confidence="low",
            content_chars=content_chars,
        )

    def estimate_item(self, item: ContextItem) -> TokenEstimate:
        if item.token_estimate is not None:
            return item.token_estimate
        return self.estimate_text(item.content or item.content_ref or "")

    def available_context_tokens(self, budget: TokenBudget) -> int:
        return budget.available_context_tokens

    def decide_item(
        self,
        item: ContextItem,
        budget: TokenBudget,
        used_context_tokens: int = 0,
    ) -> TokenBudgetDecision:
        estimate = self.estimate_item(item)
        available = self.available_context_tokens(budget)
        tokens_after = used_context_tokens + estimate.estimated_tokens
        included = tokens_after <= available
        return TokenBudgetDecision(
            item_ref=item.context_item_id,
            included=included,
            token_estimate=estimate,
            tokens_before=used_context_tokens,
            tokens_after=tokens_after if included else used_context_tokens,
            available_context_tokens=available,
            omission_reason=None if included else ContextOmissionReason.TOKEN_BUDGET_EXCEEDED,
            reason="fits_token_budget" if included else "token_budget_exceeded",
        )


__all__ = ["SimpleTokenBudgetManager", "TokenBudgetManager"]
