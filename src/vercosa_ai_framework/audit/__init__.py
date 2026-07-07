"""Audit/Event Log contracts for Vercosa AI Framework."""

from .event_log import EventLog, InMemoryEventLog
from .integrations import (
    context_package_event,
    guardian_decision_event,
    policy_resolution_event,
    record_context_package_event,
    record_guardian_decision_event,
    record_policy_resolution_event,
)
from .types import AuditEvent, EventCategory, EventResult, EventSeverity, generate_event_id, utc_now_iso

__all__ = [
    "AuditEvent",
    "EventCategory",
    "EventLog",
    "EventResult",
    "EventSeverity",
    "InMemoryEventLog",
    "context_package_event",
    "generate_event_id",
    "guardian_decision_event",
    "policy_resolution_event",
    "record_context_package_event",
    "record_guardian_decision_event",
    "record_policy_resolution_event",
    "utc_now_iso",
]
