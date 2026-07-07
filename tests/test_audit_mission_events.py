from __future__ import annotations

import socket
import sys
from collections.abc import Iterable

from vercosa_ai_framework.audit import (
    EventCategory,
    EventResult,
    EventSeverity,
    InMemoryEventLog,
    batch_completed_event,
    batch_interrupted_event,
    batch_started_event,
    mission_completed_event,
    mission_failed_event,
    mission_queued_event,
    mission_skipped_event,
    mission_started_event,
    record_mission_event,
)
from vercosa_ai_framework.missions import DirectoryMissionQueue, Mission, MissionRunner
from vercosa_ai_framework.runtime import (
    RuntimeAdapter,
    RuntimeExecutionPlan,
    RuntimeExecutionRequest,
    RuntimeExecutionResult,
    RuntimeInfo,
    RuntimeStatus,
)


SAFE_METADATA = {
    "mission_id": "m-1",
    "mission_name": "Documentar auditoria",
    "mission_path": "missions/queue/m-1.md",
    "batch_size": 3,
    "executed_count": 2,
    "queue_count": 1,
    "done_count": 2,
    "failed_count": 0,
    "commit_hash": "abc123",
}


def test_mission_queued_event_creation() -> None:
    event = mission_queued_event(metadata=SAFE_METADATA)

    assert event.category is EventCategory.MISSION
    assert event.name == "mission.queued"
    assert event.severity is EventSeverity.INFO
    assert event.result is EventResult.SUCCESS
    assert event.metadata["mission_name"] == "Documentar auditoria"


def test_mission_started_event_creation() -> None:
    event = mission_started_event(metadata=SAFE_METADATA)

    assert event.category is EventCategory.MISSION
    assert event.name == "mission.started"
    assert event.severity is EventSeverity.INFO
    assert event.result is EventResult.SUCCESS


def test_mission_completed_event_creation() -> None:
    event = mission_completed_event(metadata=SAFE_METADATA)

    assert event.category is EventCategory.MISSION
    assert event.name == "mission.completed"
    assert event.severity is EventSeverity.INFO
    assert event.result is EventResult.SUCCESS
    assert event.metadata["commit_hash"] == "abc123"


def test_mission_failed_event_creation() -> None:
    event = mission_failed_event(metadata=SAFE_METADATA)

    assert event.category is EventCategory.MISSION
    assert event.name == "mission.failed"
    assert event.severity is EventSeverity.ERROR
    assert event.result is EventResult.FAILED


def test_mission_skipped_event_creation() -> None:
    event = mission_skipped_event(metadata=SAFE_METADATA)

    assert event.category is EventCategory.MISSION
    assert event.name == "mission.skipped"
    assert event.severity is EventSeverity.WARNING
    assert event.result is EventResult.SKIPPED


def test_batch_started_event_creation() -> None:
    event = batch_started_event(metadata=SAFE_METADATA)

    assert event.category is EventCategory.MISSION
    assert event.name == "mission.batch.started"
    assert event.severity is EventSeverity.INFO
    assert event.result is EventResult.SUCCESS
    assert event.metadata["batch_size"] == 3


def test_batch_completed_event_creation() -> None:
    event = batch_completed_event(metadata=SAFE_METADATA)

    assert event.category is EventCategory.MISSION
    assert event.name == "mission.batch.completed"
    assert event.severity is EventSeverity.INFO
    assert event.result is EventResult.SUCCESS
    assert event.metadata["executed_count"] == 2


def test_batch_interrupted_event_creation() -> None:
    event = batch_interrupted_event(metadata=SAFE_METADATA)

    assert event.category is EventCategory.MISSION
    assert event.name == "mission.batch.interrupted"
    assert event.severity is EventSeverity.WARNING
    assert event.result is EventResult.FAILED


def test_mission_event_metadata_preserves_only_safe_fields() -> None:
    event = mission_queued_event(
        metadata={
            **SAFE_METADATA,
            "mission_content": "conteudo integral da missão",
            "prompt": "prompt completo",
            "secret": "segredo",
            "api_token": "token",
            "credential": "credencial",
        }
    )

    assert event.metadata["mission_path"] == "missions/queue/m-1.md"
    assert "mission_content" not in event.metadata
    assert "prompt" not in event.metadata
    assert "secret" not in event.metadata
    assert "api_token" not in event.metadata
    assert "credential" not in event.metadata
    assert "conteudo integral da missão" not in repr(event.metadata)
    assert "prompt completo" not in repr(event.metadata)


def test_mission_event_helpers_are_deterministic_for_same_input() -> None:
    assert mission_queued_event(metadata=SAFE_METADATA) == mission_queued_event(metadata=SAFE_METADATA)
    assert mission_started_event(metadata=SAFE_METADATA) == mission_started_event(metadata=SAFE_METADATA)
    assert mission_completed_event(metadata=SAFE_METADATA) == mission_completed_event(metadata=SAFE_METADATA)
    assert mission_failed_event(metadata=SAFE_METADATA) == mission_failed_event(metadata=SAFE_METADATA)
    assert batch_started_event(metadata=SAFE_METADATA) == batch_started_event(metadata=SAFE_METADATA)
    assert batch_completed_event(metadata=SAFE_METADATA) == batch_completed_event(metadata=SAFE_METADATA)
    assert batch_interrupted_event(metadata=SAFE_METADATA) == batch_interrupted_event(metadata=SAFE_METADATA)


def test_record_mission_event_is_optional() -> None:
    event_log = InMemoryEventLog()
    event = mission_started_event(metadata=SAFE_METADATA)

    unrecorded = record_mission_event(event)
    assert unrecorded == event
    assert event_log.list_events() == ()

    recorded = record_mission_event(event, event_log=event_log)
    assert recorded == event
    assert event_log.list_events() == (event,)


def test_mission_runner_records_events_only_when_event_log_is_provided(tmp_path) -> None:
    event_log = InMemoryEventLog()
    queue = DirectoryMissionQueue(tmp_path)
    mission = Mission(mission_id="mission-runner-audit", title="Missão segura", goal="Executar dry-run local")
    runner = MissionRunner(queue, _SuccessfulRuntime(), event_log=event_log)

    runner.register(mission)
    result = runner.run(mission.mission_id)

    assert result.status.value == "done"
    assert [event.name for event in event_log.list_events()] == [
        "mission.queued",
        "mission.started",
        "mission.completed",
    ]
    assert event_log.list_events()[0].metadata["mission_name"] == "Missão segura"
    assert "Executar dry-run local" not in repr(event_log.list_events())


def test_mission_runner_without_event_log_keeps_optional_integration(tmp_path) -> None:
    queue = DirectoryMissionQueue(tmp_path)
    mission = Mission(mission_id="mission-runner-no-audit", title="Sem audit log", goal="Executar local")
    runner = MissionRunner(queue, _SuccessfulRuntime())

    runner.register(mission)
    result = runner.run(mission.mission_id)

    assert result.status.value == "done"
    assert runner.audit_log == [
        "mission=mission-runner-no-audit mission queued",
        "mission=mission-runner-no-audit mission started",
        "mission=mission-runner-no-audit cycle 1 started",
        "mission=mission-runner-no-audit cycle 1 runtime status=done",
        "mission=mission-runner-no-audit result status=done",
    ]


def test_mission_events_do_not_use_network(monkeypatch) -> None:
    def fail_socket(*args, **kwargs):  # noqa: ANN001, ANN002, ANN003
        raise AssertionError("network access is not allowed")

    monkeypatch.setattr(socket, "socket", fail_socket)

    event = batch_completed_event(metadata=SAFE_METADATA)

    assert event.category is EventCategory.MISSION


def test_mission_events_require_no_new_external_dependency() -> None:
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

    mission_queued_event(metadata=SAFE_METADATA)

    imported_after_event = set(sys.modules) - before
    assert not forbidden_modules.intersection(imported_after_event)


class _SuccessfulRuntime(RuntimeAdapter):
    def detect_runtime(self, workspace: str) -> RuntimeInfo:
        return RuntimeInfo(runtime_id="test", runtime_name="Test", available=True)

    def list_models(self) -> tuple[object, ...]:
        return ()

    def prepare_execution(self, request: RuntimeExecutionRequest) -> RuntimeExecutionPlan:
        return RuntimeExecutionPlan(mission_id=request.mission_id, workspace=request.workspace)

    def execute_mission(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        return RuntimeExecutionResult(
            mission_id=request.mission_id,
            runtime_id="test",
            status=RuntimeStatus.DONE,
            metadata={"summary": "ok"},
        )

    def execute_task(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        return self.execute_mission(request)

    def collect_logs(self, mission_id: str, task_id: str | None = None) -> tuple[str, ...]:
        return ()

    def stop_execution(self, mission_id: str, task_id: str | None = None) -> RuntimeExecutionResult:
        return RuntimeExecutionResult(mission_id=mission_id, runtime_id="test", status=RuntimeStatus.STOPPED)

    def validate_artifacts(self, mission_id: str, expected_artifacts: Iterable[str]) -> tuple[str, ...]:
        return tuple(expected_artifacts)
