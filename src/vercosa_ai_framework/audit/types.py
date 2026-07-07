"""Provider-neutral audit event types for the framework.

The initial Audit/Event Log contracts are deterministic and local. They do not
persist data, call external systems, or integrate with observability providers.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping


class EventCategory(str, Enum):
    """Initial categories for internal framework events."""

    MISSION = "mission"
    POLICY = "policy"
    GUARDIAN = "guardian"
    CONTEXT = "context"
    MODEL_SELECTION = "model_selection"
    RUNTIME = "runtime"
    PROVIDER = "provider"
    USAGE_LIMIT = "usage_limit"
    SYSTEM = "system"


class EventSeverity(str, Enum):
    """Severity attached to an audit event."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class EventResult(str, Enum):
    """Outcome represented by an audit event."""

    SUCCESS = "success"
    SKIPPED = "skipped"
    WARNING = "warning"
    FAILED = "failed"
    BLOCKED = "blocked"
    REQUIRES_APPROVAL = "requires_approval"


def utc_now_iso() -> str:
    """Return a UTC timestamp for events created outside deterministic tests."""

    return datetime.now(timezone.utc).isoformat()


def _normalize_for_hash(value: Any) -> Any:
    """Convert event payload values into JSON-stable primitives."""

    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {str(key): _normalize_for_hash(value[key]) for key in sorted(value, key=str)}
    if isinstance(value, tuple | list):
        return [_normalize_for_hash(item) for item in value]
    if isinstance(value, set | frozenset):
        return [_normalize_for_hash(item) for item in sorted(value, key=repr)]
    return value


def generate_event_id(
    *,
    category: EventCategory,
    name: str,
    severity: EventSeverity,
    result: EventResult,
    message: str,
    source: str,
    metadata: Mapping[str, Any],
    created_at: str | None,
) -> str:
    """Generate a deterministic identifier from normalized event data."""

    payload = {
        "category": category.value,
        "name": name,
        "severity": severity.value,
        "result": result.value,
        "message": message,
        "source": source,
        "metadata": _normalize_for_hash(metadata),
        "created_at": created_at,
    }
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class AuditEvent:
    """Structured internal event emitted by framework components."""

    category: EventCategory
    name: str
    severity: EventSeverity = EventSeverity.INFO
    result: EventResult = EventResult.SUCCESS
    message: str = ""
    source: str = "framework"
    metadata: Mapping[str, Any] = field(default_factory=dict)
    created_at: str | None = None
    event_id: str = ""

    def __post_init__(self) -> None:
        normalized_metadata = MappingProxyType(dict(self.metadata))
        object.__setattr__(self, "metadata", normalized_metadata)
        if not self.event_id:
            object.__setattr__(
                self,
                "event_id",
                generate_event_id(
                    category=self.category,
                    name=self.name,
                    severity=self.severity,
                    result=self.result,
                    message=self.message,
                    source=self.source,
                    metadata=normalized_metadata,
                    created_at=self.created_at,
                ),
            )


__all__ = [
    "AuditEvent",
    "EventCategory",
    "EventResult",
    "EventSeverity",
    "generate_event_id",
    "utc_now_iso",
]
