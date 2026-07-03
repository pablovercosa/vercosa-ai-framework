"""Filesystem-backed persistence adapter for JSON records."""

from __future__ import annotations

import json
import re
import tempfile
from dataclasses import asdict, is_dataclass
from enum import Enum
from hashlib import sha256
from pathlib import Path
from typing import Any, Generic

from vercosa_ai_framework.persistence.repository import Repository
from vercosa_ai_framework.persistence.types import EntityRef, PayloadT, PersistedRecord, PersistenceResult, QueryFilter


_SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
_REDACTED = "[REDACTED]"


class FilesystemRepository(Generic[PayloadT], Repository[PayloadT]):
    """Persist records as deterministic JSON files under a local directory."""

    def __init__(self, root_dir: str | Path, *, namespace: str = "default", collection: str = "records") -> None:
        self.root_dir = Path(root_dir).expanduser().resolve()
        self.namespace = _validate_name(namespace, "namespace")
        self.collection = _validate_name(collection, "collection")
        self.collection_dir = (self.root_dir / self.namespace / self.collection).resolve()
        if not self.collection_dir.is_relative_to(self.root_dir):
            raise ValueError("collection directory must stay inside root_dir")
        self.collection_dir.mkdir(parents=True, exist_ok=True)

    def save(self, record: PersistedRecord[PayloadT]) -> PersistenceResult[PayloadT]:
        """Persist or update one record as a JSON file."""

        try:
            stored_record = _record_for_storage(record)
            data = _record_to_data(stored_record)
            stored_record = _with_content_hash(stored_record, _content_hash(data))
            data = _record_to_data(stored_record)
            path = self._path_for_record_id(stored_record.record_id)
            _atomic_write_json(path, data)
            return PersistenceResult(success=True, operation="save", ref=stored_record.ref(), record=stored_record)
        except (OSError, TypeError, ValueError) as exc:
            return PersistenceResult(success=False, operation="save", ref=record.ref(), errors=(str(exc),))

    def get(self, ref: EntityRef) -> PersistedRecord[PayloadT] | None:
        """Return a persisted record by record ID or entity reference."""

        if ref.record_id is not None:
            path = self._path_for_record_id(ref.record_id)
            if not path.exists():
                return None
            return _record_from_data(_read_json(path))

        for record in self.list(QueryFilter(entity_type=ref.entity_type, entity_id=ref.entity_id)):
            return record
        return None

    def list(self, query_filter: QueryFilter | None = None) -> tuple[PersistedRecord[PayloadT], ...]:
        """Return records in deterministic order, optionally filtered."""

        records = tuple(
            sorted(
                (_record_from_data(_read_json(path)) for path in self.collection_dir.glob("*.json")),
                key=lambda item: (item.record_type, item.entity_type, item.entity_id, item.record_id),
            )
        )
        if query_filter is None:
            return records

        filtered = tuple(record for record in records if _matches_filter(record, query_filter))
        start = query_filter.offset
        end = None if query_filter.limit is None else start + query_filter.limit
        return filtered[start:end]

    def delete(self, ref: EntityRef) -> PersistenceResult[PayloadT]:
        """Delete a record by record ID or entity reference."""

        record = self.get(ref)
        if record is None:
            return PersistenceResult(success=False, operation="delete", ref=ref, errors=("record not found",))
        path = self._path_for_record_id(record.record_id)
        try:
            path.unlink()
        except FileNotFoundError:
            return PersistenceResult(success=False, operation="delete", ref=record.ref(), errors=("record not found",))
        except OSError as exc:
            return PersistenceResult(success=False, operation="delete", ref=record.ref(), errors=(str(exc),))
        return PersistenceResult(success=True, operation="delete", ref=record.ref(), record=record)

    def _path_for_record_id(self, record_id: str) -> Path:
        safe_record_id = _validate_name(record_id, "record_id")
        path = (self.collection_dir / f"{safe_record_id}.json").resolve()
        if not path.is_relative_to(self.collection_dir):
            raise ValueError("record path must stay inside collection directory")
        return path


def _validate_name(value: str, field_name: str) -> str:
    if not _SAFE_NAME.fullmatch(value):
        raise ValueError(f"{field_name} must be a safe filesystem name")
    return value


def _record_for_storage(record: PersistedRecord[PayloadT]) -> PersistedRecord[PayloadT]:
    if not record.metadata.get("secret_warning"):
        return record

    redactions = tuple(dict.fromkeys((*record.redactions_applied, "secret_warning_payload_redaction")))
    return PersistedRecord(
        record_type=record.record_type,
        entity_ref=record.entity_ref,
        payload=_redact(record.payload),
        record_id=record.record_id,
        schema_version=record.schema_version,
        parent_refs=record.parent_refs,
        content_hash=record.content_hash,
        created_at=record.created_at,
        updated_at=record.updated_at,
        created_by=record.created_by,
        updated_by=record.updated_by,
        sensitivity=record.sensitivity,
        redactions_applied=redactions,
        guardian_decision_refs=record.guardian_decision_refs,
        audit_log_refs=record.audit_log_refs,
        metadata={**_redact(record.metadata), "secret_warning": True},
    )


def _with_content_hash(record: PersistedRecord[PayloadT], content_hash: str) -> PersistedRecord[PayloadT]:
    return PersistedRecord(
        record_type=record.record_type,
        entity_ref=record.entity_ref,
        payload=record.payload,
        record_id=record.record_id,
        schema_version=record.schema_version,
        parent_refs=record.parent_refs,
        content_hash=content_hash,
        created_at=record.created_at,
        updated_at=record.updated_at,
        created_by=record.created_by,
        updated_by=record.updated_by,
        sensitivity=record.sensitivity,
        redactions_applied=record.redactions_applied,
        guardian_decision_refs=record.guardian_decision_refs,
        audit_log_refs=record.audit_log_refs,
        metadata=record.metadata,
    )


def _redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _redact(item) for key, item in value.items()}
    if isinstance(value, list | tuple | set):
        return [_redact(item) for item in value]
    if value is None or isinstance(value, bool | int | float):
        return value
    return _REDACTED


def _record_to_data(record: PersistedRecord[Any]) -> dict[str, Any]:
    return {
        "audit_log_refs": list(record.audit_log_refs),
        "content_hash": record.content_hash,
        "created_at": record.created_at,
        "created_by": record.created_by,
        "entity_ref": _entity_ref_to_data(record.entity_ref),
        "guardian_decision_refs": list(record.guardian_decision_refs),
        "metadata": _json_value(record.metadata),
        "parent_refs": [_entity_ref_to_data(ref) for ref in record.parent_refs],
        "payload": _json_value(record.payload),
        "record_id": record.record_id,
        "record_type": record.record_type,
        "redactions_applied": list(record.redactions_applied),
        "schema_version": record.schema_version,
        "sensitivity": record.sensitivity,
        "updated_at": record.updated_at,
        "updated_by": record.updated_by,
    }


def _entity_ref_to_data(ref: EntityRef) -> dict[str, Any]:
    return {
        "content_hash": ref.content_hash,
        "entity_id": ref.entity_id,
        "entity_type": ref.entity_type,
        "record_id": ref.record_id,
        "schema_version": ref.schema_version,
    }


def _record_from_data(data: dict[str, Any]) -> PersistedRecord[PayloadT]:
    return PersistedRecord(
        record_type=str(data["record_type"]),
        entity_ref=_entity_ref_from_data(data["entity_ref"]),
        payload=data["payload"],
        record_id=str(data["record_id"]),
        schema_version=str(data["schema_version"]),
        parent_refs=tuple(_entity_ref_from_data(item) for item in data.get("parent_refs", ())),
        content_hash=data.get("content_hash"),
        created_at=str(data["created_at"]),
        updated_at=str(data["updated_at"]),
        created_by=data.get("created_by"),
        updated_by=data.get("updated_by"),
        sensitivity=str(data.get("sensitivity", "public")),
        redactions_applied=tuple(str(item) for item in data.get("redactions_applied", ())),
        guardian_decision_refs=tuple(str(item) for item in data.get("guardian_decision_refs", ())),
        audit_log_refs=tuple(str(item) for item in data.get("audit_log_refs", ())),
        metadata=dict(data.get("metadata", {})),
    )


def _entity_ref_from_data(data: dict[str, Any]) -> EntityRef:
    return EntityRef(
        entity_type=str(data["entity_type"]),
        entity_id=str(data["entity_id"]),
        record_id=data.get("record_id"),
        schema_version=str(data.get("schema_version", "1")),
        content_hash=data.get("content_hash"),
    )


def _json_value(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return _json_value(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(key): _json_value(value[key]) for key in sorted(value, key=str)}
    if isinstance(value, set):
        return [_json_value(item) for item in sorted(value, key=str)]
    if isinstance(value, tuple | list):
        return [_json_value(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    return value


def _content_hash(data: dict[str, Any]) -> str:
    canonical = {key: value for key, value in data.items() if key != "content_hash"}
    return sha256(_json_dumps(canonical).encode("utf-8")).hexdigest()


def _json_dumps(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def _atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as temp_file:
        temp_file.write(_json_dumps(data))
        temp_path = Path(temp_file.name)
    temp_path.replace(path)


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError("persisted record JSON must be an object")
    return data


def _matches_filter(record: PersistedRecord[Any], query_filter: QueryFilter) -> bool:
    if query_filter.record_type is not None and record.record_type != query_filter.record_type:
        return False
    if query_filter.entity_type is not None and record.entity_type != query_filter.entity_type:
        return False
    if query_filter.entity_id is not None and record.entity_id != query_filter.entity_id:
        return False
    if query_filter.schema_version is not None and record.schema_version != query_filter.schema_version:
        return False
    if query_filter.sensitivity is not None and record.sensitivity != query_filter.sensitivity:
        return False
    if query_filter.parent_ref is not None and query_filter.parent_ref not in record.parent_refs:
        return False
    for key, expected in query_filter.metadata.items():
        if record.metadata.get(key) != expected:
            return False
    return True


__all__ = ["FilesystemRepository"]
