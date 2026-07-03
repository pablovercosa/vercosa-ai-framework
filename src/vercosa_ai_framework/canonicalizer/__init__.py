"""Canonicalizer public contracts."""

from vercosa_ai_framework.canonicalizer.adapter import CanonicalizerAdapter
from vercosa_ai_framework.canonicalizer.types import (
    CanonicalDocument,
    CanonicalMetadata,
    CanonicalSource,
    CanonicalSourceType,
    CanonicalizationRequest,
    CanonicalizationResult,
    CanonicalizationStatus,
    canonical_content_hash,
)

__all__ = [
    "CanonicalDocument",
    "CanonicalMetadata",
    "CanonicalSource",
    "CanonicalSourceType",
    "CanonicalizationRequest",
    "CanonicalizationResult",
    "CanonicalizationStatus",
    "CanonicalizerAdapter",
    "canonical_content_hash",
]
