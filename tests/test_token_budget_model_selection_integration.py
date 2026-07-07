from __future__ import annotations

import sys

from vercosa_ai_framework.model_selection import (
    ModelProfile,
    ModelSelectionPolicy,
    ModelSelector,
    TokenBudgetRequirements,
    select_model,
)


def _models() -> tuple[ModelProfile, ...]:
    return (
        ModelProfile(
            id="local-small-window",
            provider="local-provider",
            runtime="local",
            quality_tier="standard",
            reasoning_tier="light",
            memory_tier="short",
            context_window=4_000,
            local=True,
            free=True,
            small=True,
        ),
        ModelProfile(
            id="local-medium-window",
            provider="local-provider",
            runtime="local",
            quality_tier="standard",
            reasoning_tier="light",
            memory_tier="short",
            context_window=8_000,
            local=True,
            free=True,
        ),
        ModelProfile(
            id="local-large-window",
            provider="local-provider",
            runtime="local",
            quality_tier="standard",
            reasoning_tier="light",
            memory_tier="long",
            context_window=32_000,
            local=True,
            free=True,
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


def test_selection_without_token_budget_keeps_current_behavior() -> None:
    decision = select_model(_models(), _policy())

    assert decision.selected_model.id == "local-small-window"
    assert decision.token_budget_requirements is None
    assert decision.token_budget_compatibility == {}
    assert decision.token_budget_warnings == ()


def test_sufficient_token_budget_does_not_block_selection() -> None:
    requirements = TokenBudgetRequirements(minimum_context_window=3_000, estimated_context_tokens=2_000, reserved_output_tokens=1_000)

    decision = select_model(_models(), _policy(), token_budget_requirements=requirements)

    assert decision.selected_model.id == "local-small-window"
    assert decision.token_budget_compatibility["local-small-window"] is True
    assert decision.token_budget_compatibility["local-medium-window"] is True
    assert decision.token_budget_compatibility["local-large-window"] is True


def test_insufficient_token_budget_excludes_small_context_window_and_records_warning() -> None:
    requirements = TokenBudgetRequirements(minimum_context_window=6_000)

    decision = select_model(_models(), _policy(), token_budget_requirements=requirements)
    selected_ids = (decision.selected_model.id, *(model.id for model in decision.fallback_chain))

    assert decision.selected_model.id == "local-medium-window"
    assert "local-small-window" not in selected_ids
    assert decision.token_budget_compatibility["local-small-window"] is False
    assert any("token_budget_insufficient:local-small-window" in warning for warning in decision.token_budget_warnings)


def test_candidates_with_sufficient_context_window_remain_eligible() -> None:
    requirements = TokenBudgetRequirements(estimated_context_tokens=5_000, reserved_output_tokens=1_000)

    decision = select_model(_models(), _policy(), token_budget_requirements=requirements)
    eligible_ids = (decision.selected_model.id, *(model.id for model in decision.fallback_chain))

    assert "local-medium-window" in eligible_ids
    assert "local-large-window" in eligible_ids


def test_token_budget_requirements_accept_context_package_model_requirements_mapping() -> None:
    model_requirements = {
        "minimum_context_window": 6_000,
        "estimated_context_tokens": 5_000,
        "reserved_output_tokens": 1_000,
        "ignored_future_field": "ignored",
    }

    decision = select_model(_models(), _policy(), token_budget_requirements=model_requirements)

    assert decision.token_budget_requirements is not None
    assert decision.token_budget_requirements.required_context_window == 6_000
    assert decision.selected_model.id == "local-medium-window"


def test_tight_token_budget_records_warning_without_external_lookup() -> None:
    requirements = TokenBudgetRequirements(minimum_context_window=7_500)

    decision = select_model(_models(), _policy(), token_budget_requirements=requirements)

    assert decision.selected_model.id == "local-medium-window"
    assert any("token_budget_tight:local-medium-window" in warning for warning in decision.token_budget_warnings)
    assert decision.token_budget_warnings == tuple(note for note in decision.security_notes if note.startswith("token_budget_"))


def test_selection_with_token_budget_is_deterministic() -> None:
    requirements = TokenBudgetRequirements(minimum_context_window=6_000)
    selector = ModelSelector(_models())

    first = selector.select(_policy(), token_budget_requirements=requirements)
    second = selector.select(_policy(), token_budget_requirements=requirements)

    assert first.selected_model == second.selected_model
    assert first.fallback_chain == second.fallback_chain
    assert first.token_budget_compatibility == second.token_budget_compatibility
    assert first.token_budget_warnings == second.token_budget_warnings


def test_token_budget_model_selection_does_not_import_external_clients_or_context() -> None:
    forbidden_modules = {
        "requests",
        "httpx",
        "psycopg",
        "psycopg2",
        "openai",
        "google.generativeai",
        "anthropic",
        "ollama",
        "vercosa_ai_framework.context",
        "vercosa_ai_framework.guardian",
    }
    for module_name in tuple(sys.modules):
        if module_name.startswith("vercosa_ai_framework.context") or module_name.startswith("vercosa_ai_framework.guardian"):
            sys.modules.pop(module_name, None)
    before = set(sys.modules)

    select_model(_models(), _policy(), token_budget_requirements=TokenBudgetRequirements(minimum_context_window=6_000))

    imported_after_selection = set(sys.modules) - before
    assert not forbidden_modules.intersection(imported_after_selection)


def test_context_module_does_not_import_model_selection_for_budget_estimation() -> None:
    for module_name in tuple(sys.modules):
        if module_name.startswith("vercosa_ai_framework.model_selection"):
            sys.modules.pop(module_name, None)
    before = set(sys.modules)

    from vercosa_ai_framework.context import ContextItem, SimpleTokenBudgetManager, TokenBudget

    SimpleTokenBudgetManager().decide_item(
        ContextItem(context_item_id="item", source_ref="source", content="conteudo"),
        TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
    )

    imported_after_budget = set(sys.modules) - before
    assert not any(module_name.startswith("vercosa_ai_framework.model_selection") for module_name in imported_after_budget)
