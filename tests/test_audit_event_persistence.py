from __future__ import annotations

import json
import socket
import sys

import pytest

from vercosa_ai_framework.audit import (
    AuditEvent,
    EventCategory,
    EventResult,
    EventSeverity,
    InMemoryEventLog,
    JsonlAuditEventLog,
    serialize_audit_event_jsonl,
)


FIXED_TIMESTAMP = "2026-07-07T00:00:00+00:00"


def test_jsonl_event_log_creates_file_on_first_append(tmp_path) -> None:
    path = tmp_path / "audit-events.jsonl"
    event_log = JsonlAuditEventLog(path)
    event = _event(name="system.ready")

    recorded = event_log.record(event)

    assert recorded == event
    assert path.exists()
    assert event_log.list_events() == (event,)


def test_jsonl_event_log_appends_one_event_per_valid_json_line(tmp_path) -> None:
    path = tmp_path / "audit-events.jsonl"
    event_log = JsonlAuditEventLog(path)

    first = _event(name="mission.started", category=EventCategory.MISSION)
    second = _event(name="mission.completed", category=EventCategory.MISSION)

    event_log.record(first)
    event_log.record(second)

    lines = path.read_text(encoding="utf-8").splitlines()
    decoded = [json.loads(line) for line in lines]

    assert len(lines) == 2
    assert decoded[0]["name"] == "mission.started"
    assert decoded[1]["name"] == "mission.completed"
    assert event_log.list_events() == (first, second)


def test_jsonl_event_log_preserves_main_fields(tmp_path) -> None:
    path = tmp_path / "audit-events.jsonl"
    event = _event(
        name="guardian.decision",
        category=EventCategory.GUARDIAN,
        severity=EventSeverity.WARNING,
        result=EventResult.REQUIRES_APPROVAL,
        message="Aprovação requerida.",
        source="guardian",
        metadata={"mission_id": "m-1"},
    )

    JsonlAuditEventLog(path).record(event)

    decoded = json.loads(path.read_text(encoding="utf-8").strip())
    assert decoded == {
        "event_id": event.event_id,
        "category": "guardian",
        "name": "guardian.decision",
        "severity": "warning",
        "result": "requires_approval",
        "message": "Aprovação requerida.",
        "source": "guardian",
        "metadata": {"mission_id": "m-1"},
        "created_at": FIXED_TIMESTAMP,
    }


def test_jsonl_event_log_handles_empty_metadata(tmp_path) -> None:
    path = tmp_path / "audit-events.jsonl"
    JsonlAuditEventLog(path).record(_event(name="system.empty", metadata={}))

    decoded = json.loads(path.read_text(encoding="utf-8").strip())

    assert decoded["metadata"] == {}


def test_jsonl_event_log_handles_simple_metadata(tmp_path) -> None:
    path = tmp_path / "audit-events.jsonl"
    metadata = {
        "string": "valor",
        "number": 3,
        "float": 1.5,
        "flag": True,
        "items": ["a", 2, False, None],
        "nested": {"b": 2, "a": 1},
        "nothing": None,
    }

    JsonlAuditEventLog(path).record(_event(name="system.metadata", metadata=metadata))

    decoded = json.loads(path.read_text(encoding="utf-8").strip())

    assert decoded["metadata"] == {
        "string": "valor",
        "number": 3,
        "float": 1.5,
        "flag": True,
        "items": ["a", 2, False, None],
        "nested": {"a": 1, "b": 2},
        "nothing": None,
    }


def test_jsonl_serialization_is_stable_for_same_event() -> None:
    event = _event(name="system.stable", metadata={"b": 2, "a": 1})

    assert serialize_audit_event_jsonl(event) == serialize_audit_event_jsonl(event)
    assert serialize_audit_event_jsonl(event).startswith('{"category":"system","created_at"')


def test_jsonl_event_log_requires_explicit_parent_creation(tmp_path) -> None:
    path = tmp_path / "missing" / "audit-events.jsonl"

    with pytest.raises(FileNotFoundError, match="create_parent_dirs=True"):
        JsonlAuditEventLog(path)

    event_log = JsonlAuditEventLog(path, create_parent_dirs=True)
    event_log.record(_event(name="system.parent-created"))

    assert path.exists()


def test_jsonl_event_log_rejects_directory_path(tmp_path) -> None:
    with pytest.raises(IsADirectoryError):
        JsonlAuditEventLog(tmp_path)


def test_jsonl_event_log_fails_clearly_for_non_serializable_metadata(tmp_path) -> None:
    path = tmp_path / "audit-events.jsonl"
    event = AuditEvent(
        category=EventCategory.SYSTEM,
        name="system.bad-metadata",
        metadata={"bad": object()},
        created_at=FIXED_TIMESTAMP,
        event_id="manual-event-id",
    )

    with pytest.raises(TypeError, match="metadata nao serializavel"):
        JsonlAuditEventLog(path).record(event)

    assert not path.exists()


def test_in_memory_event_log_continues_working() -> None:
    event = _event(name="system.memory")
    event_log = InMemoryEventLog()

    event_log.record(event)

    assert event_log.list_events() == (event,)


def test_jsonl_event_log_does_not_use_network(monkeypatch, tmp_path) -> None:
    def fail_socket(*args, **kwargs):  # noqa: ANN001, ANN002, ANN003
        raise AssertionError("network access is not allowed")

    monkeypatch.setattr(socket, "socket", fail_socket)

    path = tmp_path / "audit-events.jsonl"
    JsonlAuditEventLog(path).record(_event(name="system.local"))

    assert path.exists()


def test_jsonl_event_log_requires_no_database_or_external_dependency(tmp_path) -> None:
    forbidden_modules = {
        "requests",
        "httpx",
        "psycopg",
        "psycopg2",
        "sqlite3",
        "openai",
        "google.generativeai",
        "anthropic",
        "ollama",
        "opentelemetry",
    }
    before = set(sys.modules)

    path = tmp_path / "audit-events.jsonl"
    JsonlAuditEventLog(path).record(_event(name="system.no-db"))

    imported_after_record = set(sys.modules) - before
    assert not forbidden_modules.intersection(imported_after_record)


def _event(
    *,
    name: str,
    category: EventCategory = EventCategory.SYSTEM,
    severity: EventSeverity = EventSeverity.INFO,
    result: EventResult = EventResult.SUCCESS,
    message: str = "Evento auditavel local.",
    source: str = "framework",
    metadata=None,  # noqa: ANN001
) -> AuditEvent:
    return AuditEvent(
        category=category,
        name=name,
        severity=severity,
        result=result,
        message=message,
        source=source,
        metadata={} if metadata is None else metadata,
        created_at=FIXED_TIMESTAMP,
    )
