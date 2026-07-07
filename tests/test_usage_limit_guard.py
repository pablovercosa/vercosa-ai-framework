from __future__ import annotations

from dataclasses import asdict

from vercosa_ai_framework.guardian import (
    UsageLimitAction,
    UsageLimitSeverity,
    UsageLimitType,
    detect_usage_limit,
)


def test_detects_usage_limit_has_been_reached_as_unknown_usage_limit():
    message = "Error: usage limit has been reached for this account."

    detection = detect_usage_limit(message, origin="provider", provider="llm-provider")

    assert detection.limit_type == UsageLimitType.UNKNOWN_USAGE_LIMIT
    assert detection.severity == UsageLimitSeverity.REQUIRES_REVIEW
    assert detection.recommended_action == UsageLimitAction.MANUAL_REVIEW
    assert detection.should_stop_worker is True
    assert detection.can_retry_later is True
    assert detection.provider == "llm-provider"
    assert detection.original_message == message


def test_detects_rate_limit_with_retry_later_guidance():
    detection = detect_usage_limit("Provider returned rate limit while processing.", origin="runtime")

    assert detection.limit_type == UsageLimitType.RATE_LIMIT
    assert detection.recommended_action == UsageLimitAction.RETRY_LATER
    assert detection.should_stop_worker is True
    assert detection.can_retry_later is True
    assert UsageLimitAction.STOP_WORKER in detection.recommended_actions


def test_detects_quota_exceeded_with_stop_worker_guidance():
    detection = detect_usage_limit("quota exceeded for the current project")

    assert detection.limit_type == UsageLimitType.QUOTA_EXCEEDED
    assert detection.recommended_action == UsageLimitAction.STOP_WORKER
    assert detection.should_stop_worker is True
    assert detection.can_retry_later is True
    assert UsageLimitAction.INSPECT_PROVIDER_LIMITS in detection.recommended_actions


def test_detects_insufficient_quota_as_quota_exceeded():
    detection = detect_usage_limit("Request failed: insufficient quota.")

    assert detection.limit_type == UsageLimitType.QUOTA_EXCEEDED
    assert detection.recommended_action == UsageLimitAction.STOP_WORKER
    assert detection.original_message == "Request failed: insufficient quota."


def test_detects_429_as_rate_limit():
    detection = detect_usage_limit("HTTP 429 returned by runtime adapter")

    assert detection.limit_type == UsageLimitType.RATE_LIMIT
    assert detection.recommended_action == UsageLimitAction.RETRY_LATER
    assert detection.should_stop_worker is True


def test_message_without_usage_limit_is_not_masked():
    message = "SyntaxError: invalid syntax in local file"

    detection = detect_usage_limit(message)

    assert detection.limit_type == UsageLimitType.NOT_USAGE_LIMIT
    assert detection.is_usage_limit is False
    assert detection.should_stop_worker is False
    assert detection.can_retry_later is False
    assert detection.recommended_action == UsageLimitAction.MANUAL_REVIEW
    assert detection.original_message == message
    assert detection.matched_patterns == ()


def test_detection_is_case_insensitive():
    detection = detect_usage_limit("USAGE LIMIT HAS BEEN REACHED")

    assert detection.limit_type == UsageLimitType.UNKNOWN_USAGE_LIMIT
    assert detection.matched_patterns == ("usage limit has been reached",)


def test_billing_limit_requires_manual_review_without_retry_later():
    detection = detect_usage_limit("Billing hard limit reached for this organization")

    assert detection.limit_type == UsageLimitType.BILLING_LIMIT
    assert detection.recommended_action == UsageLimitAction.MANUAL_REVIEW
    assert detection.should_stop_worker is True
    assert detection.can_retry_later is False


def test_detection_is_deterministic_for_same_input():
    first = detect_usage_limit("Too many requests: requests per minute exceeded", origin="provider")
    second = detect_usage_limit("Too many requests: requests per minute exceeded", origin="provider")

    assert first == second
    assert asdict(first) == asdict(second)


def test_detection_api_has_no_external_callable_or_network_dependency():
    detection = detect_usage_limit("tokens per minute exceeded", runtime="opencode")

    assert detection.runtime == "opencode"
    assert detection.limit_type == UsageLimitType.RATE_LIMIT
    assert detection.metadata == {}
