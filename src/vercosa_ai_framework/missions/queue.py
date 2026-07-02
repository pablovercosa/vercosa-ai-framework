"""Local file-backed Mission Queue MVP."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from vercosa_ai_framework.missions.types import Mission, MissionStatus, utc_now_iso


class MissionQueueError(ValueError):
    """Raised when a mission queue operation violates state rules."""


class DirectoryMissionQueue:
    """Simple audit-friendly queue persisted as one JSON file per mission."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def enqueue(self, mission: Mission) -> Mission:
        """Persist a mission in queued state."""

        if self._path(mission.mission_id).exists():
            msg = f"mission already exists: {mission.mission_id}"
            raise MissionQueueError(msg)
        queued = mission.with_status(MissionStatus.QUEUED, queued_at=mission.queued_at or utc_now_iso())
        self._save(queued)
        return queued

    def get(self, mission_id: str) -> Mission:
        """Load a mission by id."""

        path = self._path(mission_id)
        if not path.exists():
            msg = f"mission not found: {mission_id}"
            raise MissionQueueError(msg)
        return self._load(path)

    def list(self, status: MissionStatus | None = None) -> tuple[Mission, ...]:
        """List missions, optionally filtered by state."""

        missions = [self._load(path) for path in sorted(self.root.glob("*.json"))]
        if status is not None:
            missions = [mission for mission in missions if mission.status == status]
        return tuple(sorted(missions, key=lambda mission: (mission.priority, mission.queued_at or "")))

    def next(self) -> Mission | None:
        """Return the next queued mission without locking it."""

        queued = self.list(MissionStatus.QUEUED)
        return queued[0] if queued else None

    def start(self, mission_id: str, locked_by: str | None = None) -> Mission:
        """Move a queued mission to running and lock it for execution."""

        mission = self.get(mission_id)
        self._require_status(mission, {MissionStatus.QUEUED})
        running = mission.with_status(
            MissionStatus.RUNNING,
            started_at=utc_now_iso(),
            attempt_count=mission.attempt_count + 1,
            locked_by=locked_by,
        )
        self._save(running)
        return running

    def complete(self, mission_id: str) -> Mission:
        """Mark a running mission as done."""

        mission = self.get(mission_id)
        self._require_status(mission, {MissionStatus.RUNNING})
        done = mission.with_status(MissionStatus.DONE, finished_at=utc_now_iso(), locked_by=None)
        self._save(done)
        return done

    def fail(self, mission_id: str, error: str) -> Mission:
        """Mark a running mission as failed while preserving error context."""

        mission = self.get(mission_id)
        self._require_status(mission, {MissionStatus.RUNNING})
        failed = mission.with_status(
            MissionStatus.FAILED,
            finished_at=utc_now_iso(),
            locked_by=None,
            last_error=error,
        )
        self._save(failed)
        return failed

    def cancel(self, mission_id: str, reason: str | None = None) -> Mission:
        """Cancel a queued or running mission."""

        mission = self.get(mission_id)
        self._require_status(mission, {MissionStatus.QUEUED, MissionStatus.RUNNING})
        cancelled = mission.with_status(
            MissionStatus.CANCELLED,
            finished_at=utc_now_iso(),
            locked_by=None,
            last_error=reason,
        )
        self._save(cancelled)
        return cancelled

    def requeue(self, mission_id: str) -> Mission:
        """Requeue a failed or cancelled mission when retry limits allow it."""

        mission = self.get(mission_id)
        self._require_status(mission, {MissionStatus.FAILED, MissionStatus.CANCELLED})
        if mission.attempt_count >= mission.max_attempts:
            msg = f"mission retry limit reached: {mission_id}"
            raise MissionQueueError(msg)
        queued = mission.with_status(
            MissionStatus.QUEUED,
            queued_at=utc_now_iso(),
            started_at=None,
            finished_at=None,
            locked_by=None,
            last_error=None,
        )
        self._save(queued)
        return queued

    def _path(self, mission_id: str) -> Path:
        return self.root / f"{mission_id}.json"

    def _save(self, mission: Mission) -> None:
        data = asdict(mission)
        data["status"] = mission.status.value
        path = self._path(mission.mission_id)
        temporary = path.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
        temporary.replace(path)

    def _load(self, path: Path) -> Mission:
        data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        data["status"] = MissionStatus(data["status"])
        for key in ("spec_refs", "guardian_refs", "acceptance_criteria"):
            data[key] = tuple(data.get(key, ()))
        return Mission(**data)

    def _require_status(self, mission: Mission, allowed: set[MissionStatus]) -> None:
        if mission.status not in allowed:
            expected = ", ".join(status.value for status in sorted(allowed, key=lambda item: item.value))
            msg = f"mission {mission.mission_id} is {mission.status.value}; expected one of: {expected}"
            raise MissionQueueError(msg)
