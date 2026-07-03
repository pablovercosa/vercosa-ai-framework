from __future__ import annotations

import json

import pytest

from vercosa_ai_framework.persistence import EntityRef, FilesystemRepository, PersistedRecord, QueryFilter


def make_record(record_id: str, *, status: str = "queued", metadata: dict[str, object] | None = None) -> PersistedRecord[dict[str, object]]:
    return PersistedRecord(
        record_id=record_id,
        record_type="mission",
        entity_ref=EntityRef(entity_type="mission", entity_id=f"entity-{record_id}"),
        payload={"status": status, "priority": 1},
        metadata=metadata or {},
        created_at="2026-07-03T00:00:00+00:00",
        updated_at="2026-07-03T00:00:00+00:00",
    )


def test_filesystem_repository_saves_gets_lists_and_deletes_records(tmp_path):
    repository = FilesystemRepository(tmp_path, namespace="framework", collection="missions")
    first = make_record("record-1", status="queued", metadata={"mission_id": "mission-1"})
    second = make_record("record-2", status="done", metadata={"mission_id": "mission-2"})

    assert repository.save(second).success is True
    assert repository.save(first).success is True

    assert repository.get(first.ref()).payload == {"priority": 1, "status": "queued"}
    assert [record.record_id for record in repository.list()] == ["record-1", "record-2"]
    assert repository.list(QueryFilter(metadata={"mission_id": "mission-2"})) == (repository.get(second.ref()),)

    deleted = repository.delete(first.ref())

    assert deleted.success is True
    assert repository.get(first.ref()) is None
    assert [record.record_id for record in repository.list()] == ["record-2"]


def test_filesystem_repository_uses_configurable_namespace_and_collection(tmp_path):
    repository = FilesystemRepository(tmp_path, namespace="project-a", collection="tasks")
    record = PersistedRecord(
        record_id="task-1",
        record_type="task",
        entity_ref=EntityRef(entity_type="task", entity_id="task-1"),
        payload={"state": "ready"},
        created_at="2026-07-03T00:00:00+00:00",
        updated_at="2026-07-03T00:00:00+00:00",
    )

    repository.save(record)

    assert (tmp_path / "project-a" / "tasks" / "task-1.json").exists()


def test_filesystem_repository_serializes_json_deterministically(tmp_path):
    repository = FilesystemRepository(tmp_path, namespace="framework", collection="records")
    record = PersistedRecord(
        record_id="record-json",
        record_type="mission",
        entity_ref=EntityRef(entity_type="mission", entity_id="mission-json"),
        payload={"z": 1, "a": {"b": 2}},
        metadata={"z": "last", "a": "first"},
        created_at="2026-07-03T00:00:00+00:00",
        updated_at="2026-07-03T00:00:00+00:00",
    )

    repository.save(record)
    path = tmp_path / "framework" / "records" / "record-json.json"
    first_write = path.read_text(encoding="utf-8")
    repository.save(record)

    assert path.read_text(encoding="utf-8") == first_write
    assert list(json.loads(first_write)) == sorted(json.loads(first_write))
    assert '"schema_version": "1"' in first_write


def test_filesystem_repository_redacts_payload_when_secret_warning_is_set(tmp_path):
    repository = FilesystemRepository(tmp_path, namespace="framework", collection="guarded")
    record = PersistedRecord(
        record_id="secret-record",
        record_type="guardian_decision",
        entity_ref=EntityRef(entity_type="guardian_decision", entity_id="decision-1"),
        payload={"api_key": "sk-live-secret", "nested": {"token": "plain-token"}, "count": 1},
        metadata={"secret_warning": True, "raw_secret_hint": "plain-token"},
        created_at="2026-07-03T00:00:00+00:00",
        updated_at="2026-07-03T00:00:00+00:00",
    )

    saved = repository.save(record)
    raw = (tmp_path / "framework" / "guarded" / "secret-record.json").read_text(encoding="utf-8")

    assert saved.success is True
    assert "sk-live-secret" not in raw
    assert "plain-token" not in raw
    assert repository.get(record.ref()).payload == {"api_key": "[REDACTED]", "count": 1, "nested": {"token": "[REDACTED]"}}
    assert "secret_warning_payload_redaction" in repository.get(record.ref()).redactions_applied


def test_filesystem_repository_rejects_unsafe_path_components(tmp_path):
    with pytest.raises(ValueError, match="namespace"):
        FilesystemRepository(tmp_path, namespace="../escape", collection="records")

    repository = FilesystemRepository(tmp_path, namespace="safe", collection="records")
    result = repository.save(make_record("../escape"))

    assert result.success is False
    assert not (tmp_path / "escape.json").exists()
