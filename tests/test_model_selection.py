import pytest

from vercosa_ai_framework.model_selection import (
    ModelProfile,
    ModelSelectionError,
    ModelSelectionPolicy,
    ModelSelector,
    select_model,
)


def model_catalog():
    return [
        ModelProfile(
            id="local-small",
            provider="ollama",
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
            provider="ollama",
            runtime="local",
            quality_tier="high",
            reasoning_tier="high",
            memory_tier="long",
            context_window=32_000,
            local=True,
            free=True,
            paid=False,
            cost_input=0.0,
            cost_output=0.0,
        ),
        ModelProfile(
            id="paid-frontier",
            provider="frontier-provider",
            runtime="api",
            pricing_class="paid",
            quality_tier="maximum",
            reasoning_tier="high",
            memory_tier="long",
            context_window=128_000,
            cost_input=0.01,
            cost_output=0.03,
            local=False,
            free=False,
            paid=True,
        ),
    ]


def test_selects_local_small_model_for_simple_free_task():
    decision = select_model(
        model_catalog(),
        ModelSelectionPolicy(
            task_role="router",
            complexity="low",
            quality="standard",
            cost_profile="strict_free",
            reasoning="light",
            memory="short",
            allow_paid=False,
            prefer_local=True,
        ),
    )

    assert decision.selected_model.id == "local-small"
    assert decision.small_model is not None
    assert decision.small_model.id == "local-small"
    assert all(not model.paid for model in decision.fallback_chain)
    assert any("strict_free" in note for note in decision.security_notes)


def test_selects_stronger_local_model_when_quality_requires_high():
    decision = ModelSelector(model_catalog()).select(
        ModelSelectionPolicy(
            task_role="developer",
            complexity="high",
            quality="high",
            cost_profile="balanced",
            reasoning="high",
            memory="long",
            allow_paid=False,
            prefer_local=True,
        )
    )

    assert decision.selected_model.id == "local-strong"
    assert decision.requires_review is True
    assert [model.id for model in decision.fallback_chain] == []


def test_premium_policy_can_select_paid_maximum_model():
    decision = select_model(
        model_catalog(),
        {
            "task_role": "architect",
            "complexity": "critical",
            "quality": "maximum",
            "cost_profile": "premium",
            "reasoning": "high",
            "memory": "long",
            "allow_paid": True,
            "prefer_local": False,
            "context_size": 64_000,
        },
    )

    assert decision.selected_model.id == "paid-frontier"
    assert decision.selected_provider == "frontier-provider"
    assert decision.selected_runtime == "api"
    assert decision.fallback_chain == ()
    assert decision.requires_review is True


def test_paid_model_is_blocked_without_policy_permission():
    with pytest.raises(ModelSelectionError, match="no compatible model"):
        select_model(
            model_catalog(),
            ModelSelectionPolicy(
                complexity="critical",
                quality="maximum",
                cost_profile="balanced",
                reasoning="high",
                memory="long",
                allow_paid=False,
                prefer_local=False,
                context_size=64_000,
            ),
        )


def test_fallback_can_be_disabled():
    decision = select_model(
        model_catalog(),
        ModelSelectionPolicy(
            complexity="low",
            quality="standard",
            cost_profile="strict_free",
            reasoning="light",
            memory="short",
            fallback=False,
        ),
    )

    assert decision.fallback_chain == ()


def test_empty_catalog_fails_with_explainable_error():
    with pytest.raises(ModelSelectionError, match="no models are registered"):
        select_model([], ModelSelectionPolicy())
