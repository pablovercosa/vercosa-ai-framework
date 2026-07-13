"""Audit/Event Log contracts for Vercosa AI Framework."""

from .event_log import EventLog, InMemoryEventLog
from .integrations import (
    agent_execution_event,
    context_package_event,
    guardian_decision_event,
    model_selection_event,
    policy_resolution_event,
    record_context_package_event,
    record_guardian_decision_event,
    record_policy_resolution_event,
)
from .jsonl import AuditEventJsonlWriter, JsonlAuditEventLog, audit_event_to_json_dict, serialize_audit_event_jsonl
from .mission_events import (
    batch_completed_event,
    batch_interrupted_event,
    batch_started_event,
    mission_completed_event,
    mission_failed_event,
    mission_queued_event,
    mission_skipped_event,
    mission_started_event,
    record_mission_event,
)
from .types import AuditEvent, EventCategory, EventResult, EventSeverity, generate_event_id, utc_now_iso

__all__ = [
    "AuditEvent",
    "AuditEventJsonlWriter",
    "EventCategory",
    "EventLog",
    "EventResult",
    "EventSeverity",
    "InMemoryEventLog",
    "JsonlAuditEventLog",
    "agent_execution_event",
    "audit_event_to_json_dict",
    "batch_completed_event",
    "batch_interrupted_event",
    "batch_started_event",
    "context_package_event",
    "generate_event_id",
    "guardian_decision_event",
    "mission_completed_event",
    "mission_failed_event",
    "mission_queued_event",
    "mission_skipped_event",
    "mission_started_event",
    "model_selection_event",
    "policy_resolution_event",
    "record_context_package_event",
    "record_guardian_decision_event",
    "record_mission_event",
    "record_policy_resolution_event",
    "serialize_audit_event_jsonl",
    "utc_now_iso",
]
