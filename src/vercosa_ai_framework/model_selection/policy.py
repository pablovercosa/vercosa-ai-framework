"""Policy primitives for the Model Selection Engine MVP."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


COMPLEXITY_TIERS = {"low": 0, "medium": 1, "high": 2, "critical": 3}
QUALITY_TIERS = {"draft": 0, "standard": 1, "high": 2, "maximum": 3}
REASONING_TIERS = {"none": 0, "light": 1, "medium": 2, "high": 3, "adaptive": -1}
MEMORY_TIERS = {"none": 0, "short": 1, "long": 2, "adaptive": -1}
COST_PROFILES = {"economy", "balanced", "premium", "strict_free"}


@dataclass(frozen=True, slots=True)
class ModelSelectionPolicy:
    """Normalized intent and constraints for selecting models."""

    task_role: str = "developer"
    complexity: str = "medium"
    quality: str = "standard"
    cost_profile: str = "balanced"
    reasoning: str = "adaptive"
    memory: str = "adaptive"
    allow_paid: bool = False
    prefer_local: bool = True
    context_size: int = 0
    fallback: bool = True

    def __post_init__(self) -> None:
        _require("complexity", self.complexity, COMPLEXITY_TIERS)
        _require("quality", self.quality, QUALITY_TIERS)
        _require("cost_profile", self.cost_profile, COST_PROFILES)
        _require("reasoning", self.reasoning, REASONING_TIERS)
        _require("memory", self.memory, MEMORY_TIERS)
        if self.context_size < 0:
            msg = "context_size must be greater than or equal to zero"
            raise ValueError(msg)

    @classmethod
    def from_mapping(cls, values: dict[str, Any]) -> "ModelSelectionPolicy":
        """Build a policy from a plain mapping, ignoring unknown future fields."""
        supported = {field for field in cls.__dataclass_fields__}
        return cls(**{key: value for key, value in values.items() if key in supported})

    @property
    def quality_rank(self) -> int:
        return QUALITY_TIERS[self.quality]

    @property
    def complexity_rank(self) -> int:
        return COMPLEXITY_TIERS[self.complexity]

    @property
    def reasoning_rank(self) -> int:
        if self.reasoning != "adaptive":
            return REASONING_TIERS[self.reasoning]
        return min(self.complexity_rank + 1, REASONING_TIERS["high"])

    @property
    def memory_rank(self) -> int:
        if self.memory != "adaptive":
            return MEMORY_TIERS[self.memory]
        return MEMORY_TIERS["long"] if self.complexity_rank >= 2 else MEMORY_TIERS["short"]

    @property
    def requires_review(self) -> bool:
        return self.complexity in {"high", "critical"} or self.quality == "maximum"


def _require(name: str, value: str, allowed: set[str] | dict[str, int]) -> None:
    if value not in allowed:
        expected = ", ".join(sorted(allowed))
        msg = f"unsupported {name!s}: {value!r}; expected one of: {expected}"
        raise ValueError(msg)
