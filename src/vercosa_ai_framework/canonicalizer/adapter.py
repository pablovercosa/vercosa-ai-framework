"""Canonicalizer Adapter abstract contract."""

from __future__ import annotations

from abc import ABC, abstractmethod

from collections.abc import Iterable

from vercosa_ai_framework.canonicalizer.types import (
    CanonicalSourceType,
    CanonicalizationRequest,
    CanonicalizationResult,
)


class CanonicalizerAdapter(ABC):
    """Abstract boundary for provider-agnostic canonicalization adapters."""

    @abstractmethod
    def supported_source_types(self) -> tuple[CanonicalSourceType, ...]:
        """Return source types supported by this adapter."""

    @abstractmethod
    def can_handle(self, request: CanonicalizationRequest) -> bool:
        """Return whether this adapter can handle the request without side effects."""

    @abstractmethod
    def canonicalize(self, request: CanonicalizationRequest) -> CanonicalizationResult:
        """Canonicalize a governed request into a CanonicalizationResult."""

    def supports_any(self, source_types: Iterable[CanonicalSourceType]) -> bool:
        """Return whether any requested source type is supported."""

        supported = set(self.supported_source_types())
        return any(source_type in supported for source_type in source_types)


__all__ = ["CanonicalizerAdapter"]
