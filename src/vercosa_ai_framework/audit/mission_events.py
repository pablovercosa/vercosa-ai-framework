"""Optional audit helpers for mission lifecycle events.

The helpers in this module create structured Mission Runner and batch events.
They do not inspect mission directories, persist events, call runtimes, or require
callers to provide an EventLog.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Mapping

from vercosa_ai_framework.audit.event_log import EventLog
from vercosa_ai_framework.audit.types import AuditEvent, EventCategory, EventResult, EventSeverity


_SAFE_METADATA_KEYS = {
    "mission_id",
    "mission_name",
    "mission_path",
    "batch_size",
    "executed_count",
    "queue_count",
    "done_count",
    "failed_count",
    "commit_hash",
}


def mission_queued_event(*, metadata: Mapping[str, Any] | None = None) -> AuditEvent:
    """Create an event representing a mission entering the queue."""

    return _mission_event(
        name="mission.queued",
        result=EventResult.SUCCESS,
        severity=EventSeverity.INFO,
        message="Missão enfileirada registrada de forma estruturada.",
        metadata=metadata,
    )


def mission_started_event(*, metadata: Mapping[str, Any] | None = None) -> AuditEvent:
    """Create an event representing a mission execution start."""

    return _mission_event(
        name="mission.started",
        result=EventResult.SUCCESS,
        severity=EventSeverity.INFO,
        message="Início de missão registrado de forma estruturada.",
        metadata=metadata,
    )


def mission_completed_event(*, metadata: Mapping[str, Any] | None = None) -> AuditEvent:
    """Create an event representing a successful mission completion."""

    return _mission_event(
        name="mission.completed",
        result=EventResult.SUCCESS,
        severity=EventSeverity.INFO,
        message="Conclusão de missão registrada de forma estruturada.",
        metadata=metadata,
    )


def mission_failed_event(*, metadata: Mapping[str, Any] | None = None) -> AuditEvent:
    """Create an event representing a failed mission."""

    return _mission_event(
        name="mission.failed",
        result=EventResult.FAILED,
        severity=EventSeverity.ERROR,
        message="Falha de missão registrada de forma estruturada.",
        metadata=metadata,
    )


def mission_skipped_event(*, metadata: Mapping[str, Any] | None = None) -> AuditEvent:
    """Create an event representing a skipped mission."""

    return _mission_event(
        name="mission.skipped",
        result=EventResult.SKIPPED,
        severity=EventSeverity.WARNING,
        message="Missão ignorada registrada de forma estruturada.",
        metadata=metadata,
    )


def batch_started_event(*, metadata: Mapping[str, Any] | None = None) -> AuditEvent:
    """Create an event representing a batch execution start."""

    return _mission_event(
        name="mission.batch.started",
        result=EventResult.SUCCESS,
        severity=EventSeverity.INFO,
        message="Início de batch de missões registrado de forma estruturada.",
        metadata=metadata,
    )


def batch_completed_event(*, metadata: Mapping[str, Any] | None = None) -> AuditEvent:
    """Create an event representing a successful batch completion."""

    return _mission_event(
        name="mission.batch.completed",
        result=EventResult.SUCCESS,
        severity=EventSeverity.INFO,
        message="Conclusão de batch de missões registrada de forma estruturada.",
        metadata=metadata,
    )


def batch_interrupted_event(*, metadata: Mapping[str, Any] | None = None) -> AuditEvent:
    """Create an event representing an interrupted batch execution."""

    return _mission_event(
        name="mission.batch.interrupted",
        result=EventResult.FAILED,
        severity=EventSeverity.WARNING,
        message="Interrupção de batch de missões registrada de forma estruturada.",
        metadata=metadata,
    )


def record_mission_event(event: AuditEvent, *, event_log: EventLog | None = None) -> AuditEvent:
    """Record a mission event only when an EventLog is explicitly provided."""

    return event_log.record(event) if event_log is not None else event


def _mission_event(
    *,
    name: str,
    result: EventResult,
    severity: EventSeverity,
    message: str,
    metadata: Mapping[str, Any] | None,
) -> AuditEvent:
    return AuditEvent(
        category=EventCategory.MISSION,
        name=name,
        severity=severity,
        result=result,
        message=message,
        source="missions",
        metadata=_safe_mission_metadata(metadata),
    )


def _safe_mission_metadata(metadata: Mapping[str, Any] | None) -> dict[str, Any]:
    if not metadata:
        return {}
    return {str(key): _safe_metadata_value(value) for key, value in metadata.items() if str(key) in _SAFE_METADATA_KEYS}


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
        return _safe_mission_metadata(value)
    return repr(value)


__all__ = [
    "batch_completed_event",
    "batch_interrupted_event",
    "batch_started_event",
    "mission_completed_event",
    "mission_failed_event",
    "mission_queued_event",
    "mission_skipped_event",
    "mission_started_event",
    "record_mission_event",
]
