"""Optional audit helpers for central framework decisions.

The helpers in this module turn already-produced Policy, Guardian and Context
results into structured audit events. They do not call those engines, persist
events, access external systems, or require callers to provide an EventLog.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Mapping

from vercosa_ai_framework.audit.event_log import EventLog
from vercosa_ai_framework.audit.types import AuditEvent, EventCategory, EventResult, EventSeverity
from vercosa_ai_framework.context.types import ContextPackage
from vercosa_ai_framework.guardian.types import GuardianAction, GuardianDecision
from vercosa_ai_framework.model_selection.types import SelectionDecision
from vercosa_ai_framework.policy.types import PolicyEffect, PolicyResolutionResult, PolicySeverity


_SENSITIVE_METADATA_MARKERS = (
    "api_key",
    "apikey",
    "authorization",
    "command",
    "content",
    "credential",
    "password",
    "prompt",
    "raw",
    "secret",
    "text",
    "token",
)


def policy_resolution_event(
    result: PolicyResolutionResult,
    *,
    considered_policy_count: int | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> AuditEvent:
    """Create a structured audit event for a Policy Engine result."""

    resolved = result.resolved_policy_set
    conflicts = result.conflicts or resolved.conflicts
    require_approval_refs = tuple(
        rule.rule_id for rule in resolved.resolved_rules if rule.effect is PolicyEffect.REQUIRE_APPROVAL
    )
    warning_policy_refs = tuple(rule.rule_id for rule in resolved.resolved_rules if rule.effect is PolicyEffect.WARN)
    denied_refs = tuple(rule.rule_id for rule in resolved.resolved_rules if rule.effect is PolicyEffect.DENY)
    has_warnings = bool(result.warnings or resolved.warnings or warning_policy_refs)
    severity = _policy_event_severity(conflicts, has_warnings, bool(require_approval_refs))
    event_result = _policy_event_result(conflicts, has_warnings, bool(require_approval_refs))
    event_metadata = _safe_metadata(metadata)
    event_metadata.update(
        {
            "policy_sets_considered": considered_policy_count
            if considered_policy_count is not None
            else len(result.ordered_policy_set_ids),
            "policy_sets_ordered": len(result.ordered_policy_set_ids),
            "policies_resolved": len(resolved.resolved_rules),
            "conflicts_count": len(conflicts),
            "warnings_count": len(result.warnings or resolved.warnings),
            "resolution_id": resolved.resolution_id,
            "matched_policy_refs": resolved.matched_policy_refs,
            "conflict_refs": tuple(conflict.conflict_id for conflict in conflicts),
            "warning_policy_refs": warning_policy_refs,
            "require_approval_refs": require_approval_refs,
            "denied_policy_refs": denied_refs,
        }
    )
    return AuditEvent(
        category=EventCategory.POLICY,
        name="policy.resolution",
        severity=severity,
        result=event_result,
        message="Resultado de resolução de políticas registrado de forma estruturada.",
        source="policy",
        metadata=event_metadata,
    )


def record_policy_resolution_event(
    result: PolicyResolutionResult,
    *,
    event_log: EventLog | None = None,
    considered_policy_count: int | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> AuditEvent:
    """Create a Policy event and record it only when an EventLog is provided."""

    event = policy_resolution_event(result, considered_policy_count=considered_policy_count, metadata=metadata)
    return event_log.record(event) if event_log is not None else event


def guardian_decision_event(
    decision: GuardianDecision,
    *,
    origin: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> AuditEvent:
    """Create a structured audit event for a Guardian decision."""

    event_metadata = _safe_metadata(metadata)
    event_metadata.update(
        {
            "decision": decision.decision.value,
            "evaluation_id": decision.evaluation_id,
            "mission_id": decision.mission_id,
            "risk_level": decision.risk_level.value,
            "guardian_mode": decision.guardian_mode.value,
            "origin": origin,
            "matched_policy_refs": decision.matched_policies,
            "violations_count": len(decision.violations),
            "warning_count": len(decision.warnings),
            "blocked_items_count": len(decision.blocked_items),
            "approval_requirements_count": len(decision.approval_requirements),
            "requires_approval": decision.requires_approval,
            "blocked": decision.blocked,
            "violation_policy_refs": tuple(violation.policy_id for violation in decision.violations),
            "blocked_item_refs": decision.blocked_items,
            "redactions_applied_count": len(decision.redactions_applied),
        }
    )
    return AuditEvent(
        category=EventCategory.GUARDIAN,
        name="guardian.decision",
        severity=_guardian_event_severity(decision.decision),
        result=_guardian_event_result(decision.decision),
        message="Decisão do Guardian registrada de forma estruturada.",
        source="guardian",
        metadata=event_metadata,
    )


def record_guardian_decision_event(
    decision: GuardianDecision,
    *,
    event_log: EventLog | None = None,
    origin: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> AuditEvent:
    """Create a Guardian event and record it only when an EventLog is provided."""

    event = guardian_decision_event(decision, origin=origin, metadata=metadata)
    return event_log.record(event) if event_log is not None else event


def context_package_event(
    package: ContextPackage,
    *,
    candidate_count: int | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> AuditEvent:
    """Create a structured audit event for a ContextPackage."""

    omitted_by_reason: dict[str, int] = {}
    for omission in package.omission_reasons:
        reason = omission.omission_reason.value if omission.omission_reason is not None else "unknown"
        omitted_by_reason[reason] = omitted_by_reason.get(reason, 0) + 1

    requires_approval = bool(package.metadata.get("requires_approval"))
    severity = _context_event_severity(package, requires_approval)
    event_result = _context_event_result(package, requires_approval)
    event_metadata = _safe_metadata(metadata)
    event_metadata.update(
        {
            "context_package_id": package.context_package_id,
            "request_id": package.request_id,
            "candidate_count": candidate_count,
            "selected_items_count": len(package.items),
            "selected_source_count": len(package.sources),
            "omitted_items_count": len(package.omission_reasons),
            "warnings_count": len(package.warnings),
            "estimated_context_tokens": package.token_estimate.estimated_tokens,
            "reserved_output_tokens": package.output_token_reservation,
            "omission_reasons": dict(sorted(omitted_by_reason.items())),
            "omitted_item_refs": tuple(omission.item_ref for omission in package.omission_reasons),
            "policy_refs": package.policy_refs,
            "guardian_decision_refs": package.guardian_decision_refs,
            "requires_approval": requires_approval,
            "approval_policy_refs": _tuple_from_metadata(package.metadata.get("approval_policy_refs")),
            "blocked_policy_refs": _tuple_from_metadata(package.metadata.get("blocked_policy_refs")),
            "used_context_tokens": package.metadata.get("used_context_tokens"),
            "available_context_tokens": package.metadata.get("available_context_tokens"),
            "remaining_context_tokens": package.metadata.get("remaining_context_tokens"),
        }
    )
    return AuditEvent(
        category=EventCategory.CONTEXT,
        name="context.package",
        severity=severity,
        result=event_result,
        message="Montagem de ContextPackage registrada de forma estruturada.",
        source="context",
        metadata=event_metadata,
    )


def record_context_package_event(
    package: ContextPackage,
    *,
    event_log: EventLog | None = None,
    candidate_count: int | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> AuditEvent:
    """Create a Context event and record it only when an EventLog is provided."""

    event = context_package_event(package, candidate_count=candidate_count, metadata=metadata)
    return event_log.record(event) if event_log is not None else event


def model_selection_event(
    decision: SelectionDecision,
    *,
    metadata: Mapping[str, Any] | None = None,
) -> AuditEvent:
    """Create a structured audit event for a Model Selection decision."""

    event_metadata = _safe_metadata(metadata)
    requirements = decision.token_budget_requirements
    event_metadata.update(
        {
            "selected_model_id": decision.selected_model.id,
            "selected_provider": decision.selected_provider,
            "selected_runtime": decision.selected_runtime,
            "small_model_id": decision.small_model.id if decision.small_model else None,
            "fallback_model_ids": tuple(model.id for model in decision.fallback_chain),
            "estimated_cost": decision.estimated_cost,
            "quality_expectation": decision.quality_expectation,
            "policy_sources": decision.policy_sources,
            "requires_review": decision.requires_review,
            "requires_user_approval": decision.requires_user_approval,
            "minimum_context_window": requirements.minimum_context_window if requirements else None,
            "estimated_context_tokens": requirements.estimated_context_tokens if requirements else None,
            "reserved_output_tokens": requirements.reserved_output_tokens if requirements else None,
            "available_context_tokens": requirements.available_context_tokens if requirements else None,
            "token_budget_compatibility": dict(sorted(decision.token_budget_compatibility.items())),
            "warning_count": len(decision.security_notes) + len(decision.token_budget_warnings),
        }
    )
    result = EventResult.REQUIRES_APPROVAL if decision.requires_user_approval else EventResult.SUCCESS
    severity = EventSeverity.WARNING if decision.requires_review or decision.requires_user_approval else EventSeverity.INFO
    return AuditEvent(
        category=EventCategory.MODEL_SELECTION,
        name="model_selection.decision",
        severity=severity,
        result=result,
        message="Decisão de Model Selection registrada de forma estruturada.",
        source="model_selection",
        metadata=event_metadata,
    )


def agent_execution_event(
    name: str,
    *,
    result: str = "success",
    metadata: Mapping[str, Any] | None = None,
) -> AuditEvent:
    """Create a sanitized Agent Assignment execution audit event."""

    result_map = {
        "success": EventResult.SUCCESS,
        "failed": EventResult.FAILED,
        "blocked": EventResult.BLOCKED,
        "requires_approval": EventResult.REQUIRES_APPROVAL,
        "warning": EventResult.WARNING,
    }
    event_result = result_map.get(result, EventResult.SUCCESS)
    severity = EventSeverity.ERROR if event_result in {EventResult.FAILED, EventResult.BLOCKED} else EventSeverity.INFO
    if event_result in {EventResult.REQUIRES_APPROVAL, EventResult.WARNING}:
        severity = EventSeverity.WARNING
    return AuditEvent(
        category=EventCategory.RUNTIME,
        name=f"agent_execution.{name}",
        severity=severity,
        result=event_result,
        message="Evento de execução de Agent Assignment registrado de forma estruturada.",
        source="agents",
        metadata=_safe_metadata(metadata),
    )


def _policy_event_severity(conflicts: tuple[Any, ...], has_warnings: bool, requires_approval: bool) -> EventSeverity:
    if any(conflict.severity is PolicySeverity.CRITICAL for conflict in conflicts):
        return EventSeverity.ERROR
    if conflicts or has_warnings or requires_approval:
        return EventSeverity.WARNING
    return EventSeverity.INFO


def _policy_event_result(conflicts: tuple[Any, ...], has_warnings: bool, requires_approval: bool) -> EventResult:
    if requires_approval:
        return EventResult.REQUIRES_APPROVAL
    if conflicts or has_warnings:
        return EventResult.WARNING
    return EventResult.SUCCESS


def _guardian_event_severity(decision: GuardianAction) -> EventSeverity:
    if decision is GuardianAction.BLOCK:
        return EventSeverity.ERROR
    if decision in {GuardianAction.WARN, GuardianAction.REQUIRE_APPROVAL}:
        return EventSeverity.WARNING
    return EventSeverity.INFO


def _guardian_event_result(decision: GuardianAction) -> EventResult:
    if decision is GuardianAction.BLOCK:
        return EventResult.BLOCKED
    if decision is GuardianAction.REQUIRE_APPROVAL:
        return EventResult.REQUIRES_APPROVAL
    if decision is GuardianAction.WARN:
        return EventResult.WARNING
    return EventResult.SUCCESS


def _context_event_severity(package: ContextPackage, requires_approval: bool) -> EventSeverity:
    if requires_approval or package.warnings or package.omission_reasons:
        return EventSeverity.WARNING
    return EventSeverity.INFO


def _context_event_result(package: ContextPackage, requires_approval: bool) -> EventResult:
    if requires_approval:
        return EventResult.REQUIRES_APPROVAL
    if package.warnings or package.omission_reasons:
        return EventResult.WARNING
    return EventResult.SUCCESS


def _safe_metadata(metadata: Mapping[str, Any] | None) -> dict[str, Any]:
    if not metadata:
        return {}
    return {str(key): _safe_metadata_value(value) for key, value in metadata.items() if _safe_metadata_key(str(key))}


def _safe_metadata_key(key: str) -> bool:
    normalized = key.lower().replace("-", "_")
    return not any(marker in normalized for marker in _SENSITIVE_METADATA_MARKERS)


def _safe_metadata_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, str | int | float | bool) or value is None:
        return value
    if isinstance(value, tuple | list):
        return tuple(_safe_metadata_value(item) for item in value)
    if isinstance(value, set | frozenset):
        return tuple(_safe_metadata_value(item) for item in sorted(value, key=repr))
    if isinstance(value, Mapping):
        return _safe_metadata(value)
    return repr(value)


def _tuple_from_metadata(value: Any) -> tuple[Any, ...]:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    return (value,)


__all__ = [
    "context_package_event",
    "agent_execution_event",
    "guardian_decision_event",
    "model_selection_event",
    "policy_resolution_event",
    "record_context_package_event",
    "record_guardian_decision_event",
    "record_policy_resolution_event",
]
