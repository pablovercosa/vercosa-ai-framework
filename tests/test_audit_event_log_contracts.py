from __future__ import annotations

import socket
import sys
from dataclasses import FrozenInstanceError

import pytest

from vercosa_ai_framework.audit import (
    AuditEvent,
    EventCategory,
    EventLog,
    EventResult,
    EventSeverity,
    InMemoryEventLog,
)


FIXED_TIMESTAMP = "2026-07-07T00:00:00+00:00"


def test_event_creation_with_minimum_fields() -> None:
    event = AuditEvent(category=EventCategory.SYSTEM, name="system.ready", created_at=FIXED_TIMESTAMP)

    assert event.category is EventCategory.SYSTEM
    assert event.name == "system.ready"
    assert event.severity is EventSeverity.INFO
    assert event.result is EventResult.SUCCESS
    assert event.source == "framework"
    assert event.created_at == FIXED_TIMESTAMP


def test_event_creation_with_metadata() -> None:
    event = AuditEvent(
        category=EventCategory.POLICY,
        name="policy.resolved",
        result=EventResult.WARNING,
        metadata={"policy_refs": ("policy.warn",), "conflicts": 1},
        created_at=FIXED_TIMESTAMP,
    )

    assert event.metadata["policy_refs"] == ("policy.warn",)
    assert event.metadata["conflicts"] == 1


def test_event_id_is_filled_and_deterministic_for_same_data() -> None:
    first = AuditEvent(
        category=EventCategory.GUARDIAN,
        name="guardian.decision",
        severity=EventSeverity.WARNING,
        result=EventResult.REQUIRES_APPROVAL,
        message="Aprovação requerida.",
        source="guardian",
        metadata={"decision": "require_approval"},
        created_at=FIXED_TIMESTAMP,
    )
    second = AuditEvent(
        category=EventCategory.GUARDIAN,
        name="guardian.decision",
        severity=EventSeverity.WARNING,
        result=EventResult.REQUIRES_APPROVAL,
        message="Aprovação requerida.",
        source="guardian",
        metadata={"decision": "require_approval"},
        created_at=FIXED_TIMESTAMP,
    )

    assert first.event_id
    assert first.event_id == second.event_id


def test_created_at_can_be_controlled_or_left_unset() -> None:
    controlled = AuditEvent(category=EventCategory.MISSION, name="mission.started", created_at=FIXED_TIMESTAMP)
    unset = AuditEvent(category=EventCategory.MISSION, name="mission.started")

    assert controlled.created_at == FIXED_TIMESTAMP
    assert unset.created_at is None


def test_event_log_protocol_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        EventLog()


def test_record_event_in_memory_log() -> None:
    event = AuditEvent(category=EventCategory.RUNTIME, name="runtime.plan", created_at=FIXED_TIMESTAMP)
    event_log = InMemoryEventLog()

    recorded = event_log.record(event)

    assert recorded == event
    assert event_log.list_events() == (event,)


def test_listing_preserves_deterministic_insertion_order() -> None:
    first = AuditEvent(category=EventCategory.MISSION, name="mission.started", created_at=FIXED_TIMESTAMP)
    second = AuditEvent(category=EventCategory.MISSION, name="mission.finished", created_at=FIXED_TIMESTAMP)
    event_log = InMemoryEventLog()

    event_log.record(first)
    event_log.record(second)

    assert event_log.list_events() == (first, second)


def test_filter_by_category() -> None:
    policy = AuditEvent(category=EventCategory.POLICY, name="policy.resolved", created_at=FIXED_TIMESTAMP)
    context = AuditEvent(category=EventCategory.CONTEXT, name="context.package", created_at=FIXED_TIMESTAMP)
    event_log = InMemoryEventLog([policy, context])

    assert event_log.filter_by_category(EventCategory.POLICY) == (policy,)


def test_filter_by_severity() -> None:
    warning = AuditEvent(
        category=EventCategory.USAGE_LIMIT,
        name="usage_limit.detected",
        severity=EventSeverity.WARNING,
        created_at=FIXED_TIMESTAMP,
    )
    info = AuditEvent(category=EventCategory.SYSTEM, name="system.ready", created_at=FIXED_TIMESTAMP)
    event_log = InMemoryEventLog([warning, info])

    assert event_log.filter_by_severity(EventSeverity.WARNING) == (warning,)


def test_filter_by_result() -> None:
    blocked = AuditEvent(
        category=EventCategory.GUARDIAN,
        name="guardian.blocked",
        result=EventResult.BLOCKED,
        created_at=FIXED_TIMESTAMP,
    )
    success = AuditEvent(category=EventCategory.MODEL_SELECTION, name="model.selected", created_at=FIXED_TIMESTAMP)
    event_log = InMemoryEventLog([blocked, success])

    assert event_log.filter_by_result(EventResult.BLOCKED) == (blocked,)


def test_returned_events_do_not_allow_internal_state_mutation() -> None:
    event = AuditEvent(category=EventCategory.PROVIDER, name="provider.skipped", created_at=FIXED_TIMESTAMP)
    event_log = InMemoryEventLog([event])
    returned = event_log.list_events()

    with pytest.raises(AttributeError):
        returned.append(event)  # type: ignore[attr-defined]
    with pytest.raises(FrozenInstanceError):
        event.name = "mutated"  # type: ignore[misc]
    with pytest.raises(TypeError):
        event.metadata["mutated"] = True  # type: ignore[index]

    assert event_log.list_events() == (event,)


def test_clear_events() -> None:
    event_log = InMemoryEventLog(
        [AuditEvent(category=EventCategory.SYSTEM, name="system.ready", created_at=FIXED_TIMESTAMP)]
    )

    event_log.clear()

    assert event_log.list_events() == ()


def test_no_external_call_is_made(monkeypatch) -> None:
    def fail_socket(*args, **kwargs):  # noqa: ANN001, ANN002, ANN003
        raise AssertionError("network access is not allowed")

    monkeypatch.setattr(socket, "socket", fail_socket)
    event_log = InMemoryEventLog()
    event_log.record(AuditEvent(category=EventCategory.SYSTEM, name="system.local", created_at=FIXED_TIMESTAMP))

    assert event_log.list_events()[0].name == "system.local"


def test_no_new_external_dependency_is_required() -> None:
    forbidden_modules = {
        "requests",
        "httpx",
        "psycopg",
        "psycopg2",
        "openai",
        "google.generativeai",
        "anthropic",
        "ollama",
        "opentelemetry",
    }
    before = set(sys.modules)

    event_log = InMemoryEventLog()
    event_log.record(AuditEvent(category=EventCategory.SYSTEM, name="system.local", created_at=FIXED_TIMESTAMP))

    imported_after_record = set(sys.modules) - before
    assert not forbidden_modules.intersection(imported_after_record)
