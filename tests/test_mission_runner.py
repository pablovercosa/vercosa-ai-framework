from __future__ import annotations

from collections.abc import Iterable

from vercosa_ai_framework.model_selection import ModelProfile
from vercosa_ai_framework.missions import (
    AutoCommitResult,
    DirectoryMissionQueue,
    Mission,
    MissionResult,
    MissionRunner,
    MissionStatus,
)
from vercosa_ai_framework.runtime import (
    RuntimeAdapter,
    RuntimeExecutionPlan,
    RuntimeExecutionRequest,
    RuntimeExecutionResult,
    RuntimeInfo,
    RuntimeStatus,
)


class FakeRuntimeAdapter(RuntimeAdapter):
    def __init__(
        self,
        results: Iterable[RuntimeExecutionResult],
        *,
        validated_artifacts: Iterable[str] = (),
    ) -> None:
        self.results = list(results)
        self.requests: list[RuntimeExecutionRequest] = []
        self.validated_artifacts = tuple(validated_artifacts)
        self.validation_calls: list[tuple[str, tuple[str, ...]]] = []

    def detect_runtime(self, workspace: str) -> RuntimeInfo:
        return RuntimeInfo(runtime_id="fake", runtime_name="Fake", available=True)

    def list_models(self) -> tuple[ModelProfile, ...]:
        return ()

    def prepare_execution(self, request: RuntimeExecutionRequest) -> RuntimeExecutionPlan:
        return RuntimeExecutionPlan(mission_id=request.mission_id, workspace=request.workspace)

    def execute_mission(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        self.requests.append(request)
        if self.results:
            return self.results.pop(0)
        return RuntimeExecutionResult(
            mission_id=request.mission_id,
            runtime_id="fake",
            status=RuntimeStatus.FAILED,
            errors=("no fake runtime result configured",),
        )

    def execute_task(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        return self.execute_mission(request)

    def collect_logs(self, mission_id: str, task_id: str | None = None) -> tuple[str, ...]:
        return (f"log:{mission_id}",)

    def stop_execution(self, mission_id: str, task_id: str | None = None) -> RuntimeExecutionResult:
        return RuntimeExecutionResult(mission_id=mission_id, runtime_id="fake", status=RuntimeStatus.STOPPED)

    def validate_artifacts(
        self, mission_id: str, expected_artifacts: Iterable[str]
    ) -> tuple[str, ...]:
        expected = tuple(expected_artifacts)
        self.validation_calls.append((mission_id, expected))
        return self.validated_artifacts


class RecordingCommitter:
    def __init__(self, result: AutoCommitResult | None = None) -> None:
        self.result = result or AutoCommitResult(committed=True, commit_ref="abc123")
        self.calls: list[tuple[Mission, MissionResult]] = []

    def commit(self, mission: Mission, result: MissionResult) -> AutoCommitResult:
        self.calls.append((mission, result))
        return self.result


def runtime_result(mission_id: str, status: RuntimeStatus, **kwargs: object) -> RuntimeExecutionResult:
    return RuntimeExecutionResult(mission_id=mission_id, runtime_id="fake", status=status, **kwargs)


def test_runner_executes_next_queued_mission_to_done(tmp_path):
    queue = DirectoryMissionQueue(tmp_path)
    mission = queue.enqueue(Mission(title="Docs", goal="Write docs"))
    runtime = FakeRuntimeAdapter([runtime_result(mission.mission_id, RuntimeStatus.DONE)])
    runner = MissionRunner(queue, runtime)

    result = runner.run_next()

    stored = queue.get(mission.mission_id)
    assert result is not None
    assert result.status == MissionStatus.DONE
    assert stored.status == MissionStatus.DONE
    assert stored.cycle_count == 1
    assert runtime.requests[0].mission_id == mission.mission_id
    assert runtime.requests[0].context["mission_goal"] == "Write docs"
    assert runner.results[mission.mission_id].status == MissionStatus.DONE


def test_runner_marks_mission_failed_when_runtime_fails(tmp_path):
    queue = DirectoryMissionQueue(tmp_path)
    mission = queue.enqueue(Mission(title="Fail", goal="Fail safely"))
    runtime = FakeRuntimeAdapter(
        [runtime_result(mission.mission_id, RuntimeStatus.FAILED, errors=("runtime failed",))]
    )
    runner = MissionRunner(queue, runtime)

    result = runner.run(mission.mission_id)

    stored = queue.get(mission.mission_id)
    assert result.status == MissionStatus.FAILED
    assert result.errors == ("runtime failed",)
    assert stored.status == MissionStatus.FAILED
    assert stored.last_error == "runtime failed"


def test_runner_stops_at_cycle_limit(tmp_path):
    queue = DirectoryMissionQueue(tmp_path)
    mission = queue.enqueue(
        Mission(title="Loop", goal="Stop looping", execution_limits={"max_cycles": 2})
    )
    runtime = FakeRuntimeAdapter(
        [
            runtime_result(mission.mission_id, RuntimeStatus.RUNNING),
            runtime_result(mission.mission_id, RuntimeStatus.RUNNING),
        ]
    )
    runner = MissionRunner(queue, runtime)

    result = runner.run(mission.mission_id)

    stored = queue.get(mission.mission_id)
    assert result.status == MissionStatus.FAILED
    assert result.errors == ("max cycle limit reached: 2",)
    assert stored.status == MissionStatus.FAILED
    assert stored.cycle_count == 2
    assert len(runtime.requests) == 2


def test_runner_validates_expected_artifacts_before_done(tmp_path):
    queue = DirectoryMissionQueue(tmp_path)
    mission = queue.enqueue(
        Mission(
            title="Artifact",
            goal="Produce artifact",
            validation_policy={"expected_artifacts": ("docs/mission-runner.md",)},
        )
    )
    runtime = FakeRuntimeAdapter(
        [runtime_result(mission.mission_id, RuntimeStatus.DONE)],
        validated_artifacts=("docs/mission-runner.md",),
    )
    runner = MissionRunner(queue, runtime)

    result = runner.run(mission.mission_id)

    assert result.status == MissionStatus.DONE
    assert runtime.validation_calls == [(mission.mission_id, ("docs/mission-runner.md",))]
    assert result.validation_results == ("validated artifacts: 1",)


def test_runner_fails_when_expected_artifact_is_missing(tmp_path):
    queue = DirectoryMissionQueue(tmp_path)
    mission = queue.enqueue(
        Mission(
            title="Missing",
            goal="Validate missing artifact",
            validation_policy={"expected_artifacts": ("missing.md",)},
        )
    )
    runtime = FakeRuntimeAdapter([runtime_result(mission.mission_id, RuntimeStatus.DONE)])
    runner = MissionRunner(queue, runtime)

    result = runner.run(mission.mission_id)

    assert result.status == MissionStatus.FAILED
    assert result.errors == ("missing expected artifacts: missing.md",)
    assert queue.get(mission.mission_id).status == MissionStatus.FAILED


def test_runner_uses_injected_auto_committer_after_validation(tmp_path):
    queue = DirectoryMissionQueue(tmp_path)
    mission = queue.enqueue(
        Mission(
            title="Commit",
            goal="Commit safely",
            commit_policy={"auto_commit": "after_validation"},
        )
    )
    runtime = FakeRuntimeAdapter([runtime_result(mission.mission_id, RuntimeStatus.DONE)])
    committer = RecordingCommitter()
    runner = MissionRunner(queue, runtime, auto_committer=committer)

    result = runner.run(mission.mission_id)

    assert result.status == MissionStatus.DONE
    assert "commit=abc123" in result.summary
    assert len(committer.calls) == 1
    assert committer.calls[0][0].mission_id == mission.mission_id


def test_runner_does_not_execute_git_when_auto_commit_has_no_interface(tmp_path):
    queue = DirectoryMissionQueue(tmp_path)
    mission = queue.enqueue(
        Mission(
            title="No committer",
            goal="Fail safely",
            commit_policy={"auto_commit": "after_validation"},
        )
    )
    runtime = FakeRuntimeAdapter([runtime_result(mission.mission_id, RuntimeStatus.DONE)])
    runner = MissionRunner(queue, runtime)

    result = runner.run(mission.mission_id)

    assert result.status == MissionStatus.FAILED
    assert result.errors == ("auto_commit requested but no committer configured",)
    assert queue.get(mission.mission_id).status == MissionStatus.FAILED
