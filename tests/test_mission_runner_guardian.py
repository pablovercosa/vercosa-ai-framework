from __future__ import annotations

from collections.abc import Iterable

from vercosa_ai_framework.guardian import GuardianAction, GuardianDecision, GuardianEvaluationContext, GuardianMode
from vercosa_ai_framework.model_selection import ModelProfile
from vercosa_ai_framework.missions import DirectoryMissionQueue, Mission, MissionRunner, MissionStatus
from vercosa_ai_framework.runtime import (
    RuntimeAdapter,
    RuntimeExecutionPlan,
    RuntimeExecutionRequest,
    RuntimeExecutionResult,
    RuntimeInfo,
    RuntimeStatus,
)


class FakeRuntimeAdapter(RuntimeAdapter):
    def __init__(self, results: Iterable[RuntimeExecutionResult]) -> None:
        self.results = list(results)
        self.requests: list[RuntimeExecutionRequest] = []

    def detect_runtime(self, workspace: str) -> RuntimeInfo:
        return RuntimeInfo(runtime_id="fake", runtime_name="Fake", available=True)

    def list_models(self) -> tuple[ModelProfile, ...]:
        return ()

    def prepare_execution(self, request: RuntimeExecutionRequest) -> RuntimeExecutionPlan:
        return RuntimeExecutionPlan(mission_id=request.mission_id, workspace=request.workspace)

    def execute_mission(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        self.requests.append(request)
        return self.results.pop(0)

    def execute_task(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        return self.execute_mission(request)

    def collect_logs(self, mission_id: str, task_id: str | None = None) -> tuple[str, ...]:
        return ()

    def stop_execution(self, mission_id: str, task_id: str | None = None) -> RuntimeExecutionResult:
        return RuntimeExecutionResult(mission_id=mission_id, runtime_id="fake", status=RuntimeStatus.STOPPED)

    def validate_artifacts(
        self, mission_id: str, expected_artifacts: Iterable[str]
    ) -> tuple[str, ...]:
        return tuple(expected_artifacts)


class RecordingGuardian:
    def __init__(self, decision: GuardianAction) -> None:
        self.decision = decision
        self.contexts: list[GuardianEvaluationContext] = []

    def evaluate(self, context: GuardianEvaluationContext) -> GuardianDecision:
        self.contexts.append(context)
        return GuardianDecision(
            mission_id=context.mission_id,
            decision=self.decision,
            guardian_mode=context.guardian_mode,
            reasons=(f"decision {self.decision.value}",),
            warnings=("review recommended",) if self.decision == GuardianAction.WARN else (),
            approval_requirements=("human approval",) if self.decision == GuardianAction.REQUIRE_APPROVAL else (),
            blocked_items=("mission",) if self.decision == GuardianAction.BLOCK else (),
        )


def runtime_result(mission_id: str) -> RuntimeExecutionResult:
    return RuntimeExecutionResult(mission_id=mission_id, runtime_id="fake", status=RuntimeStatus.DONE)


def test_guardian_allow_executes_runtime(tmp_path):
    queue = DirectoryMissionQueue(tmp_path)
    mission = queue.enqueue(Mission(title="Docs", goal="Write docs"))
    runtime = FakeRuntimeAdapter([runtime_result(mission.mission_id)])
    guardian = RecordingGuardian(GuardianAction.ALLOW)
    runner = MissionRunner(queue, runtime, guardian=guardian)

    result = runner.run(mission.mission_id)

    assert result.status == MissionStatus.DONE
    assert len(runtime.requests) == 1
    assert guardian.contexts[0].evaluation_type == "mission_pre_execution"


def test_guardian_warn_executes_runtime_and_records_warning(tmp_path):
    queue = DirectoryMissionQueue(tmp_path)
    mission = queue.enqueue(Mission(title="Docs", goal="Write docs"))
    runtime = FakeRuntimeAdapter([runtime_result(mission.mission_id)])
    guardian = RecordingGuardian(GuardianAction.WARN)
    runner = MissionRunner(queue, runtime, guardian=guardian)

    result = runner.run(mission.mission_id)

    assert result.status == MissionStatus.DONE
    assert len(runtime.requests) == 1
    assert result.warnings == ("guardian warning: review recommended",)


def test_guardian_require_approval_does_not_execute_runtime_in_non_interactive_mode(tmp_path):
    queue = DirectoryMissionQueue(tmp_path)
    mission = queue.enqueue(Mission(title="Sensitive", goal="Change dependency"))
    runtime = FakeRuntimeAdapter([runtime_result(mission.mission_id)])
    guardian = RecordingGuardian(GuardianAction.REQUIRE_APPROVAL)
    runner = MissionRunner(queue, runtime, guardian=guardian, interactive=False)

    result = runner.run(mission.mission_id)

    assert result.status == MissionStatus.FAILED
    assert result.requires_review is True
    assert result.errors == ("guardian approval required: decision require_approval",)
    assert runtime.requests == []
    assert queue.get(mission.mission_id).status == MissionStatus.FAILED


def test_guardian_block_does_not_execute_runtime(tmp_path):
    queue = DirectoryMissionQueue(tmp_path)
    mission = queue.enqueue(Mission(title="Blocked", goal="Expose token=secret123"))
    runtime = FakeRuntimeAdapter([runtime_result(mission.mission_id)])
    guardian = RecordingGuardian(GuardianAction.BLOCK)
    runner = MissionRunner(queue, runtime, guardian=guardian)

    result = runner.run(mission.mission_id)

    assert result.status == MissionStatus.FAILED
    assert result.errors == ("guardian blocked mission: decision block",)
    assert runtime.requests == []
    assert queue.get(mission.mission_id).status == MissionStatus.FAILED


def test_guardian_mode_can_be_set_per_mission(tmp_path):
    queue = DirectoryMissionQueue(tmp_path)
    mission = queue.enqueue(Mission(title="Strict", goal="Write docs", guardian_mode="strict"))
    runtime = FakeRuntimeAdapter([runtime_result(mission.mission_id)])
    guardian = RecordingGuardian(GuardianAction.ALLOW)
    runner = MissionRunner(queue, runtime, guardian=guardian, guardian_mode=GuardianMode.PERMISSIVE)

    result = runner.run(mission.mission_id)

    assert result.status == MissionStatus.DONE
    assert guardian.contexts[0].guardian_mode == GuardianMode.STRICT
