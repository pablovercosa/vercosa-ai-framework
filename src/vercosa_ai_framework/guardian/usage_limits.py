"""Deterministic Usage/API Limit Guard contracts and detection.

The guard only classifies text already produced by providers or runtimes. It
does not inspect billing, call external providers, access networks, or retry.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class UsageLimitType(str, Enum):
    """Normalized categories for usage, quota, billing, and rate limit signals."""

    RATE_LIMIT = "rate_limit"
    QUOTA_EXCEEDED = "quota_exceeded"
    BILLING_LIMIT = "billing_limit"
    UNKNOWN_USAGE_LIMIT = "unknown_usage_limit"
    NOT_USAGE_LIMIT = "not_usage_limit"


class UsageLimitSeverity(str, Enum):
    """Operational severity for a detected usage limit signal."""

    NONE = "none"
    TEMPORARY = "temporary"
    BLOCKING = "blocking"
    REQUIRES_REVIEW = "requires_review"


class UsageLimitAction(str, Enum):
    """Recommended operational action after classification."""

    STOP_WORKER = "stop_worker"
    RETRY_LATER = "retry_later"
    INSPECT_PROVIDER_LIMITS = "inspect_provider_limits"
    MANUAL_REVIEW = "manual_review"


@dataclass(frozen=True, slots=True)
class UsageLimitDetection:
    """Structured result emitted by the Usage/API Limit Guard."""

    limit_type: UsageLimitType
    severity: UsageLimitSeverity
    origin: str
    original_message: str
    recommended_action: UsageLimitAction
    should_stop_worker: bool
    can_retry_later: bool
    provider: str | None = None
    runtime: str | None = None
    matched_patterns: tuple[str, ...] = field(default_factory=tuple)
    recommended_actions: tuple[UsageLimitAction, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_usage_limit(self) -> bool:
        """Return whether the input was classified as a usage/API limit."""

        return self.limit_type is not UsageLimitType.NOT_USAGE_LIMIT


_PATTERNS: tuple[tuple[UsageLimitType, re.Pattern[str], str], ...] = (
    (UsageLimitType.BILLING_LIMIT, re.compile(r"\bbilling\s+hard\s+limit\b", re.I), "billing hard limit"),
    (UsageLimitType.QUOTA_EXCEEDED, re.compile(r"\bquota\s+exceeded\b", re.I), "quota exceeded"),
    (UsageLimitType.QUOTA_EXCEEDED, re.compile(r"\binsufficient\s+quota\b", re.I), "insufficient quota"),
    (UsageLimitType.QUOTA_EXCEEDED, re.compile(r"\bdaily\s+limit\b", re.I), "daily limit"),
    (UsageLimitType.RATE_LIMIT, re.compile(r"\brate\s+limit(?:ed)?\b", re.I), "rate limit"),
    (UsageLimitType.RATE_LIMIT, re.compile(r"\btoo\s+many\s+requests\b", re.I), "too many requests"),
    (UsageLimitType.RATE_LIMIT, re.compile(r"\brequests\s+per\s+minute\b", re.I), "requests per minute"),
    (UsageLimitType.RATE_LIMIT, re.compile(r"\btokens\s+per\s+minute\b", re.I), "tokens per minute"),
    (UsageLimitType.RATE_LIMIT, re.compile(r"(?:^|\D)429(?:\D|$)", re.I), "429"),
    (UsageLimitType.UNKNOWN_USAGE_LIMIT, re.compile(r"\busage\s+limit\s+has\s+been\s+reached\b", re.I), "usage limit has been reached"),
    (UsageLimitType.UNKNOWN_USAGE_LIMIT, re.compile(r"\busage\s+limit\b", re.I), "usage limit"),
)


def detect_usage_limit(
    message: str,
    *,
    origin: str = "unknown",
    provider: str | None = None,
    runtime: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> UsageLimitDetection:
    """Classify textual usage/API limit signals without external calls."""

    matches_by_type: dict[UsageLimitType, list[str]] = {}
    for limit_type, pattern, label in _PATTERNS:
        if pattern.search(message):
            matches_by_type.setdefault(limit_type, []).append(label)

    limit_type = _highest_priority_type(matches_by_type)
    matched_patterns = _specific_patterns(matches_by_type.get(limit_type, ()))
    severity, recommended_action, should_stop_worker, can_retry_later, recommended_actions = _operational_guidance(limit_type)

    return UsageLimitDetection(
        limit_type=limit_type,
        severity=severity,
        origin=origin,
        provider=provider,
        runtime=runtime,
        original_message=message,
        recommended_action=recommended_action,
        should_stop_worker=should_stop_worker,
        can_retry_later=can_retry_later,
        matched_patterns=matched_patterns,
        recommended_actions=recommended_actions,
        metadata=metadata or {},
    )


def _highest_priority_type(matches_by_type: dict[UsageLimitType, list[str]]) -> UsageLimitType:
    for limit_type in (
        UsageLimitType.BILLING_LIMIT,
        UsageLimitType.QUOTA_EXCEEDED,
        UsageLimitType.RATE_LIMIT,
        UsageLimitType.UNKNOWN_USAGE_LIMIT,
    ):
        if limit_type in matches_by_type:
            return limit_type
    return UsageLimitType.NOT_USAGE_LIMIT


def _specific_patterns(patterns: list[str]) -> tuple[str, ...]:
    if "usage limit has been reached" in patterns:
        patterns = [pattern for pattern in patterns if pattern != "usage limit"]
    return tuple(dict.fromkeys(patterns))


def _operational_guidance(
    limit_type: UsageLimitType,
) -> tuple[UsageLimitSeverity, UsageLimitAction, bool, bool, tuple[UsageLimitAction, ...]]:
    if limit_type is UsageLimitType.RATE_LIMIT:
        return (
            UsageLimitSeverity.TEMPORARY,
            UsageLimitAction.RETRY_LATER,
            True,
            True,
            (UsageLimitAction.STOP_WORKER, UsageLimitAction.RETRY_LATER),
        )
    if limit_type is UsageLimitType.QUOTA_EXCEEDED:
        return (
            UsageLimitSeverity.BLOCKING,
            UsageLimitAction.STOP_WORKER,
            True,
            True,
            (UsageLimitAction.STOP_WORKER, UsageLimitAction.INSPECT_PROVIDER_LIMITS, UsageLimitAction.RETRY_LATER),
        )
    if limit_type is UsageLimitType.BILLING_LIMIT:
        return (
            UsageLimitSeverity.REQUIRES_REVIEW,
            UsageLimitAction.MANUAL_REVIEW,
            True,
            False,
            (UsageLimitAction.STOP_WORKER, UsageLimitAction.INSPECT_PROVIDER_LIMITS, UsageLimitAction.MANUAL_REVIEW),
        )
    if limit_type is UsageLimitType.UNKNOWN_USAGE_LIMIT:
        return (
            UsageLimitSeverity.REQUIRES_REVIEW,
            UsageLimitAction.MANUAL_REVIEW,
            True,
            True,
            (UsageLimitAction.STOP_WORKER, UsageLimitAction.INSPECT_PROVIDER_LIMITS, UsageLimitAction.MANUAL_REVIEW),
        )
    return (
        UsageLimitSeverity.NONE,
        UsageLimitAction.MANUAL_REVIEW,
        False,
        False,
        (),
    )


__all__ = [
    "UsageLimitAction",
    "UsageLimitDetection",
    "UsageLimitSeverity",
    "UsageLimitType",
    "detect_usage_limit",
]
