"""Provider Adapter abstract contracts."""

from __future__ import annotations

from abc import ABC, abstractmethod

from vercosa_ai_framework.providers.types import ProviderProfile, ProviderRequest, ProviderResult


class ProviderAdapter(ABC):
    """Abstract boundary for concrete provider protocol adapters."""

    @abstractmethod
    def execute(self, request: ProviderRequest, profile: ProviderProfile) -> ProviderResult:
        """Execute or simulate a governed provider request."""


__all__ = ["ProviderAdapter"]
