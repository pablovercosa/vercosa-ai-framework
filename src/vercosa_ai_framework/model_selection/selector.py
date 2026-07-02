"""In-memory Model Selection Engine MVP."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

from vercosa_ai_framework.model_selection.policy import (
    MEMORY_TIERS,
    QUALITY_TIERS,
    REASONING_TIERS,
    ModelSelectionPolicy,
)
from vercosa_ai_framework.model_selection.types import (
    ModelProfile,
    ModelSelectionError,
    SelectionDecision,
)


class InMemoryModelRegistry:
    """Simple provider-agnostic catalog for tests and early adapters."""

    def __init__(self, models: Iterable[ModelProfile] = ()) -> None:
        self._models = tuple(models)

    def list_models(self) -> tuple[ModelProfile, ...]:
        """Return all registered model profiles."""
        return self._models


class ModelSelector:
    """Select primary, small, and fallback models from an in-memory catalog."""

    def __init__(self, models: Iterable[ModelProfile] | InMemoryModelRegistry) -> None:
        if isinstance(models, InMemoryModelRegistry):
            self._registry = models
        else:
            self._registry = InMemoryModelRegistry(models)

    def select(self, policy: ModelSelectionPolicy) -> SelectionDecision:
        """Return a safe model decision that satisfies the given policy."""
        candidates = self._compatible_models(policy)
        selected = self._select_primary(candidates, policy)
        small_model = self._select_small(candidates, policy)
        fallback_chain = self._fallback_chain(candidates, selected, policy)

        reason = self._reason(selected, policy)
        notes = self._security_notes(selected, policy)
        return SelectionDecision(
            selected_model=selected,
            small_model=small_model,
            fallback_chain=fallback_chain,
            reason=reason,
            estimated_cost=selected.estimated_unit_cost,
            quality_expectation=selected.quality_tier,
            requires_review=policy.requires_review or self._is_quality_drop(selected, policy),
            requires_user_approval=selected.paid and not policy.allow_paid,
            security_notes=notes,
        )

    def _compatible_models(self, policy: ModelSelectionPolicy) -> tuple[ModelProfile, ...]:
        models = self._registry.list_models()
        if not models:
            raise ModelSelectionError("no models are registered in the model catalog")

        compatible = [model for model in models if self._is_compatible(model, policy)]
        if not compatible:
            raise ModelSelectionError(
                "no compatible model satisfies availability, cost, context, quality, reasoning, and memory constraints"
            )
        return tuple(compatible)

    def _is_compatible(self, model: ModelProfile, policy: ModelSelectionPolicy) -> bool:
        if not model.available or model.deprecated:
            return False
        if model.paid and (policy.cost_profile == "strict_free" or not policy.allow_paid):
            return False
        if policy.context_size and model.context_window < policy.context_size:
            return False
        if QUALITY_TIERS.get(model.quality_tier, -1) < policy.quality_rank:
            return False
        if REASONING_TIERS.get(model.reasoning_tier, -1) < policy.reasoning_rank:
            return False
        if MEMORY_TIERS.get(model.memory_tier, -1) < policy.memory_rank:
            return False
        return True

    def _select_primary(
        self, candidates: Sequence[ModelProfile], policy: ModelSelectionPolicy
    ) -> ModelProfile:
        ranked = sorted(candidates, key=lambda model: self._rank_key(model, policy))
        return ranked[0]

    def _select_small(
        self, candidates: Sequence[ModelProfile], policy: ModelSelectionPolicy
    ) -> ModelProfile | None:
        small_candidates = [model for model in candidates if model.small]
        if not small_candidates:
            return None
        return sorted(small_candidates, key=lambda model: self._rank_key(model, policy))[0]

    def _fallback_chain(
        self, candidates: Sequence[ModelProfile], selected: ModelProfile, policy: ModelSelectionPolicy
    ) -> tuple[ModelProfile, ...]:
        if not policy.fallback:
            return ()
        fallbacks = [model for model in candidates if model.id != selected.id]
        return tuple(sorted(fallbacks, key=lambda model: self._rank_key(model, policy)))

    def _rank_key(self, model: ModelProfile, policy: ModelSelectionPolicy) -> tuple[float, ...]:
        quality = QUALITY_TIERS.get(model.quality_tier, 0)
        reasoning = REASONING_TIERS.get(model.reasoning_tier, 0)
        cost = model.estimated_unit_cost

        if policy.cost_profile == "premium":
            return (0 if model.local and policy.prefer_local else 1, -quality, -reasoning, cost)
        if policy.prefer_local or policy.cost_profile in {"economy", "strict_free"}:
            return (0 if model.local else 1, 0 if model.free else 1, cost, quality, reasoning)
        return (0 if model.free else 1, cost, -quality, -reasoning)

    def _reason(self, model: ModelProfile, policy: ModelSelectionPolicy) -> str:
        return (
            f"selected {model.id} for role={policy.task_role}, complexity={policy.complexity}, "
            f"quality={policy.quality}, cost_profile={policy.cost_profile}"
        )

    def _security_notes(self, model: ModelProfile, policy: ModelSelectionPolicy) -> tuple[str, ...]:
        notes: list[str] = []
        if not model.local:
            notes.append("selected model is not local; callers must avoid sending secrets or sensitive context")
        if policy.cost_profile == "strict_free":
            notes.append("strict_free policy excluded paid models")
        return tuple(notes)

    def _is_quality_drop(self, model: ModelProfile, policy: ModelSelectionPolicy) -> bool:
        return QUALITY_TIERS.get(model.quality_tier, -1) < policy.quality_rank


def select_model(
    models: Iterable[ModelProfile], policy: ModelSelectionPolicy | dict[str, object] | None = None
) -> SelectionDecision:
    """Convenience function for selecting from a plain in-memory catalog."""
    if policy is None:
        normalized_policy = ModelSelectionPolicy()
    elif isinstance(policy, ModelSelectionPolicy):
        normalized_policy = policy
    else:
        normalized_policy = ModelSelectionPolicy.from_mapping(policy)
    return ModelSelector(models).select(normalized_policy)
