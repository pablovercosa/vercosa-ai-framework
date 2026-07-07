"""Provider-neutral types for model selection.

The MVP keeps these contracts as plain Python dataclasses so adapters can fill
them from any runtime without coupling the engine to a provider API.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class ModelProfile:
    """Normalized metadata for a selectable model."""

    id: str
    provider: str
    runtime: str = "unknown"
    available: bool = True
    pricing_class: str = "free"
    quality_tier: str = "standard"
    reasoning_tier: str = "light"
    memory_tier: str = "short"
    context_window: int = 0
    cost_input: float = 0.0
    cost_output: float = 0.0
    local: bool = False
    free: bool = True
    paid: bool = False
    deprecated: bool = False
    small: bool = False
    tool_use: bool = False
    vision: bool = False
    json_mode: bool = False
    structured_output: bool = False
    embedding: bool = False

    @property
    def estimated_unit_cost(self) -> float:
        """Return a simple comparable cost estimate for ranking candidates."""
        return self.cost_input + self.cost_output


@dataclass(frozen=True, slots=True)
class TokenBudgetRequirements:
    """Provider-neutral token budget requirements consumed by model selection."""

    minimum_context_window: int = 0
    estimated_context_tokens: int = 0
    reserved_output_tokens: int = 0
    available_context_tokens: int = 0

    def __post_init__(self) -> None:
        for field_name in (
            "minimum_context_window",
            "estimated_context_tokens",
            "reserved_output_tokens",
            "available_context_tokens",
        ):
            if getattr(self, field_name) < 0:
                msg = f"{field_name} must be greater than or equal to zero"
                raise ValueError(msg)

    @classmethod
    def from_mapping(cls, values: dict[str, Any]) -> "TokenBudgetRequirements":
        """Build requirements from a plain mapping, ignoring unknown future fields."""
        supported = {field for field in cls.__dataclass_fields__}
        return cls(**{key: value for key, value in values.items() if key in supported})

    @property
    def required_context_window(self) -> int:
        """Return the minimum declared context window needed by a candidate."""
        derived_total = self.estimated_context_tokens + self.reserved_output_tokens
        return max(self.minimum_context_window, derived_total)

    @property
    def is_empty(self) -> bool:
        """Return whether no budget signal was provided."""
        return self.required_context_window == 0 and self.available_context_tokens == 0


@dataclass(frozen=True, slots=True)
class SelectionDecision:
    """Auditable result produced by the model selection engine."""

    selected_model: ModelProfile
    small_model: ModelProfile | None
    fallback_chain: tuple[ModelProfile, ...] = field(default_factory=tuple)
    reason: str = ""
    policy_sources: tuple[str, ...] = ("framework_defaults",)
    estimated_cost: float | None = None
    quality_expectation: str = "standard"
    requires_review: bool = False
    requires_user_approval: bool = False
    security_notes: tuple[str, ...] = field(default_factory=tuple)
    token_budget_requirements: TokenBudgetRequirements | None = None
    token_budget_compatibility: dict[str, bool] = field(default_factory=dict)
    token_budget_warnings: tuple[str, ...] = field(default_factory=tuple)

    @property
    def selected_provider(self) -> str:
        """Provider for the selected model."""
        return self.selected_model.provider

    @property
    def selected_runtime(self) -> str:
        """Runtime for the selected model."""
        return self.selected_model.runtime


class ModelSelectionError(ValueError):
    """Raised when no safe model selection can be produced."""
