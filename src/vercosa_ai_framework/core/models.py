"""Core domain models.

This module intentionally contains only provider-neutral primitives.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FrameworkIdentity:
    """Stable identity metadata for the framework core."""

    name: str = "Vercosa AI Framework"
    package: str = "vercosa-ai-framework"
    specification_first: bool = True
    provider_agnostic: bool = True
    local_first: bool = True
