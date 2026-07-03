from __future__ import annotations

from dataclasses import asdict

import pytest

from vercosa_ai_framework.persistence import (
    EntityRef,
    PersistedRecord,
    PersistenceResult,
    QueryFilter,
    Repository,
)


def test_entity_ref_is_storage_agnostic_traceability_metadata():
    ref = EntityRef(
        entity_type="mission",
        entity_id="mission-1",
        record_id="record-1",
        schema_version="1",
        content_hash="hash-1",
    )

    assert ref.entity_type == "mission"
    assert ref.entity_id == "mission-1"
    assert ref.record_id == "record-1"
    assert "postgres" not in asdict(ref)


def test_persisted_record_wraps_payload_with_schema_and_audit_metadata():
    entity_ref = EntityRef(entity_type="workflow", entity_id="workflow-1")
    parent_ref = EntityRef(entity_type="mission", entity_id="mission-1")
    record = PersistedRecord(
        record_id="record-workflow-1",
        record_type="workflow",
        schema_version="1",
        entity_ref=entity_ref,
        parent_refs=(parent_ref,),
        payload={"status": "ready"},
        content_hash="hash-workflow-1",
        guardian_decision_refs=("guardian-1",),
        audit_log_refs=("audit-1",),
    )

    assert record.entity_id == "workflow-1"
    assert record.entity_type == "workflow"
    assert record.payload == {"status": "ready"}
    assert record.schema_version == "1"
    assert record.parent_refs == (parent_ref,)
    assert record.ref().record_id == "record-workflow-1"
    assert record.ref().content_hash == "hash-workflow-1"


def test_persistence_result_normalizes_operation_outcome_without_storage_details():
    record = PersistedRecord(
        record_id="record-task-1",
        record_type="task",
        entity_ref=EntityRef(entity_type="task", entity_id="task-1"),
        payload={"state": "queued"},
    )

    result = PersistenceResult(success=True, operation="save", ref=record.ref(), record=record)

    assert result.success is True
    assert result.operation == "save"
    assert result.record == record
    assert result.errors == ()
    assert "filesystem" not in asdict(result)


def test_query_filter_is_simple_and_provider_neutral():
    parent_ref = EntityRef(entity_type="mission", entity_id="mission-1")
    query_filter = QueryFilter(
        record_type="task",
        entity_type="task",
        parent_ref=parent_ref,
        metadata={"workflow_id": "workflow-1"},
        limit=10,
        offset=1,
    )

    assert query_filter.record_type == "task"
    assert query_filter.parent_ref == parent_ref
    assert query_filter.metadata == {"workflow_id": "workflow-1"}
    assert query_filter.limit == 10


def test_query_filter_rejects_negative_pagination_values():
    with pytest.raises(ValueError, match="limit"):
        QueryFilter(limit=-1)

    with pytest.raises(ValueError, match="offset"):
        QueryFilter(offset=-1)


def test_repository_is_abstract_contract():
    with pytest.raises(TypeError):
        Repository()


def test_repository_contract_supports_save_get_list_delete_with_generic_payload():
    class MemoryContractRepository(Repository[dict[str, str]]):
        def __init__(self) -> None:
            self.records: dict[str, PersistedRecord[dict[str, str]]] = {}

        def save(self, record: PersistedRecord[dict[str, str]]) -> PersistenceResult[dict[str, str]]:
            self.records[record.record_id] = record
            return PersistenceResult(success=True, operation="save", ref=record.ref(), record=record)

        def get(self, ref: EntityRef) -> PersistedRecord[dict[str, str]] | None:
            if ref.record_id is not None:
                return self.records.get(ref.record_id)
            for record in self.records.values():
                if record.entity_type == ref.entity_type and record.entity_id == ref.entity_id:
                    return record
            return None

        def list(self, query_filter: QueryFilter | None = None) -> tuple[PersistedRecord[dict[str, str]], ...]:
            records = tuple(sorted(self.records.values(), key=lambda item: item.record_id))
            if query_filter is None:
                return records
            return tuple(
                record
                for record in records
                if (query_filter.record_type is None or record.record_type == query_filter.record_type)
                and (query_filter.entity_type is None or record.entity_type == query_filter.entity_type)
                and (query_filter.entity_id is None or record.entity_id == query_filter.entity_id)
            )

        def delete(self, ref: EntityRef) -> PersistenceResult[dict[str, str]]:
            record = self.get(ref)
            if record is None:
                return PersistenceResult(success=False, operation="delete", ref=ref, errors=("record not found",))
            del self.records[record.record_id]
            return PersistenceResult(success=True, operation="delete", ref=record.ref(), record=record)

    repository = MemoryContractRepository()
    record = PersistedRecord(
        record_id="record-1",
        record_type="mission",
        entity_ref=EntityRef(entity_type="mission", entity_id="mission-1"),
        payload={"status": "queued"},
    )

    saved = repository.save(record)

    assert saved.success is True
    assert repository.get(record.ref()) == record
    assert repository.list(QueryFilter(record_type="mission")) == (record,)
    assert repository.delete(record.ref()).success is True
    assert repository.get(record.ref()) is None
