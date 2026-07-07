"""In-memory Audit/Event Log contracts and implementation."""

from __future__ import annotations

from typing import Protocol

from .types import AuditEvent, EventCategory, EventResult, EventSeverity


class EventLog(Protocol):
    """Port for framework event logs."""

    def record(self, event: AuditEvent) -> AuditEvent:
        """Record and return the stored event."""

    def list_events(self) -> tuple[AuditEvent, ...]:
        """Return events in deterministic insertion order."""

    def filter_by_category(self, category: EventCategory) -> tuple[AuditEvent, ...]:
        """Return events that match a category."""

    def filter_by_severity(self, severity: EventSeverity) -> tuple[AuditEvent, ...]:
        """Return events that match a severity."""

    def filter_by_result(self, result: EventResult) -> tuple[AuditEvent, ...]:
        """Return events that match a result."""

    def clear(self) -> None:
        """Remove all events from the log."""


class InMemoryEventLog:
    """Deterministic in-memory event log without external persistence."""

    def __init__(self, events: tuple[AuditEvent, ...] | list[AuditEvent] | None = None) -> None:
        self._events: list[AuditEvent] = list(events or ())

    def record(self, event: AuditEvent) -> AuditEvent:
        """Record an event preserving insertion order."""

        self._events.append(event)
        return event

    def list_events(self) -> tuple[AuditEvent, ...]:
        """Return an immutable snapshot of recorded events."""

        return tuple(self._events)

    def filter_by_category(self, category: EventCategory) -> tuple[AuditEvent, ...]:
        """Return an immutable snapshot filtered by category."""

        return tuple(event for event in self._events if event.category is category)

    def filter_by_severity(self, severity: EventSeverity) -> tuple[AuditEvent, ...]:
        """Return an immutable snapshot filtered by severity."""

        return tuple(event for event in self._events if event.severity is severity)

    def filter_by_result(self, result: EventResult) -> tuple[AuditEvent, ...]:
        """Return an immutable snapshot filtered by result."""

        return tuple(event for event in self._events if event.result is result)

    def clear(self) -> None:
        """Clear the in-memory event list."""

        self._events.clear()


__all__ = ["EventLog", "InMemoryEventLog"]
