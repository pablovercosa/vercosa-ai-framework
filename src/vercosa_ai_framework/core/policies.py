"""Policy primitives for framework governance."""

from __future__ import annotations

from enum import Enum


class PolicyLevel(str, Enum):
    """Generic policy strictness levels used by future policy engines."""

    STANDARD = "standard"
    STRICT = "strict"
    MAXIMUM = "maximum"
