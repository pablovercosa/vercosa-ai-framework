"""Local JSONL persistence for audit events.

This module is explicit and opt-in. It does not configure a global event log,
does not collect data by itself, and does not access network, databases or
external providers.
"""

from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Any, Mapping

from .types import AuditEvent, EventCategory, EventResult, EventSeverity


class AuditEventJsonlWriter:
    """Synchronous UTF-8 append-only writer for one audit JSONL file."""

    def __init__(self, path: str | Path, *, create_parent_dirs: bool = False) -> None:
        self.path = Path(path)
        parent = self.path.parent
        if parent and not parent.exists():
            if not create_parent_dirs:
                raise FileNotFoundError(
                    f"Diretorio pai inexistente para audit JSONL: {parent}. "
                    "Use create_parent_dirs=True para cria-lo explicitamente."
                )
            parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists() and self.path.is_dir():
            raise IsADirectoryError(f"Caminho de audit JSONL aponta para diretorio: {self.path}")

    def append(self, event: AuditEvent) -> None:
        """Append one event as a single valid JSON line."""

        line = serialize_audit_event_jsonl(event)
        try:
            with self.path.open("a", encoding="utf-8") as file:
                file.write(line)
                file.write("\n")
        except OSError as exc:
            raise OSError(f"Falha ao persistir evento auditavel em JSONL: {self.path}") from exc

    def truncate(self) -> None:
        """Explicitly clear the file; normal writes remain append-only."""

        try:
            with self.path.open("w", encoding="utf-8"):
                pass
        except OSError as exc:
            raise OSError(f"Falha ao limpar arquivo JSONL de eventos auditaveis: {self.path}") from exc


class JsonlAuditEventLog:
    """Opt-in local JSONL event log compatible with the EventLog protocol."""

    def __init__(
        self,
        path: str | Path,
        *,
        create_parent_dirs: bool = False,
        events: tuple[AuditEvent, ...] | list[AuditEvent] | None = None,
    ) -> None:
        self._events: list[AuditEvent] = list(events or ())
        self._writer = AuditEventJsonlWriter(path, create_parent_dirs=create_parent_dirs)

    @property
    def path(self) -> Path:
        """Return the local JSONL file path configured by the caller."""

        return self._writer.path

    def record(self, event: AuditEvent) -> AuditEvent:
        """Persist an event and keep an in-process snapshot for filtering."""

        self._writer.append(event)
        self._events.append(event)
        return event

    def list_events(self) -> tuple[AuditEvent, ...]:
        """Return events recorded by this instance in insertion order."""

        return tuple(self._events)

    def filter_by_category(self, category: EventCategory) -> tuple[AuditEvent, ...]:
        """Return events recorded by this instance that match a category."""

        return tuple(event for event in self._events if event.category is category)

    def filter_by_severity(self, severity: EventSeverity) -> tuple[AuditEvent, ...]:
        """Return events recorded by this instance that match a severity."""

        return tuple(event for event in self._events if event.severity is severity)

    def filter_by_result(self, result: EventResult) -> tuple[AuditEvent, ...]:
        """Return events recorded by this instance that match a result."""

        return tuple(event for event in self._events if event.result is result)

    def clear(self) -> None:
        """Explicitly clear the in-process snapshot and truncate the JSONL file."""

        self._writer.truncate()
        self._events.clear()


def audit_event_to_json_dict(event: AuditEvent) -> dict[str, Any]:
    """Convert an AuditEvent to the stable JSON object stored in JSONL."""

    return {
        "event_id": event.event_id,
        "category": event.category.value,
        "name": event.name,
        "severity": event.severity.value,
        "result": event.result.value,
        "message": event.message,
        "source": event.source,
        "metadata": _json_value(event.metadata),
        "created_at": event.created_at,
    }


def serialize_audit_event_jsonl(event: AuditEvent) -> str:
    """Serialize one event as deterministic JSON suitable for one JSONL line."""

    try:
        return json.dumps(
            audit_event_to_json_dict(event),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except TypeError as exc:
        raise TypeError("Evento auditavel contem metadata nao serializavel em JSON") from exc


def _json_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, str | int | float | bool) or value is None:
        return value
    if isinstance(value, tuple | list):
        return [_json_value(item) for item in value]
    if isinstance(value, Mapping):
        return {str(key): _json_value(value[key]) for key in sorted(value, key=str)}
    return value


__all__ = [
    "AuditEventJsonlWriter",
    "JsonlAuditEventLog",
    "audit_event_to_json_dict",
    "serialize_audit_event_jsonl",
]
