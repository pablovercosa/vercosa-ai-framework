from __future__ import annotations

from collections.abc import Iterable

import pytest

from vercosa_ai_framework.model_selection import ModelProfile
from vercosa_ai_framework.runtime import (
    RuntimeAdapter,
    RuntimeCapability,
    RuntimeExecutionPlan,
    RuntimeExecutionRequest,
    RuntimeExecutionResult,
    RuntimeInfo,
    RuntimeStatus,
)


def test_runtime_adapter_is_abstract():
    with pytest.raises(TypeError):
        RuntimeAdapter()


def test_runtime_contracts_are_provider_neutral_dataclasses():
    capability = RuntimeCapability("file_write", limitations=("workspace_only",))
    info = RuntimeInfo(
        runtime_id="local-test",
        runtime_name="Local Test Runtime",
        available=True,
        capabilities=(capability,),
    )
    request = RuntimeExecutionRequest(mission_id="m-1", workspace="/workspace")
    plan = RuntimeExecutionPlan(
        mission_id=request.mission_id,
        workspace=request.workspace,
        permissions_granted={"write_files": False},
    )
    result = RuntimeExecutionResult(
        mission_id="m-1",
        runtime_id="local-test",
        status=RuntimeStatus.DONE,
        artifacts=("artifact.md",),
    )

    assert info.capabilities[0].name == "file_write"
    assert plan.permissions_granted["write_files"] is False
    assert result.status == RuntimeStatus.DONE
    assert result.artifacts == ("artifact.md",)


class FakeRuntimeAdapter(RuntimeAdapter):
    def detect_runtime(self, workspace: str) -> RuntimeInfo:
        return RuntimeInfo(runtime_id="fake", runtime_name="Fake", available=True)

    def list_models(self) -> tuple[ModelProfile, ...]:
        return ()

    def prepare_execution(self, request: RuntimeExecutionRequest) -> RuntimeExecutionPlan:
        return RuntimeExecutionPlan(mission_id=request.mission_id, workspace=request.workspace)

    def execute_mission(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        return RuntimeExecutionResult(
            mission_id=request.mission_id,
            runtime_id="fake",
            status=RuntimeStatus.DONE,
        )

    def execute_task(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        return RuntimeExecutionResult(
            mission_id=request.mission_id,
            runtime_id="fake",
            status=RuntimeStatus.DONE,
            task_id=request.task_id,
        )

    def collect_logs(self, mission_id: str, task_id: str | None = None) -> tuple[str, ...]:
        return (f"log:{mission_id}",)

    def stop_execution(self, mission_id: str, task_id: str | None = None) -> RuntimeExecutionResult:
        return RuntimeExecutionResult(
            mission_id=mission_id,
            runtime_id="fake",
            status=RuntimeStatus.STOPPED,
            task_id=task_id,
        )

    def validate_artifacts(
        self, mission_id: str, expected_artifacts: Iterable[str]
    ) -> tuple[str, ...]:
        return tuple(expected_artifacts)


def test_concrete_runtime_adapter_can_implement_contract():
    adapter = FakeRuntimeAdapter()
    request = RuntimeExecutionRequest(mission_id="m-2", workspace="/workspace", task_id="t-1")

    assert adapter.detect_runtime("/workspace").available is True
    assert adapter.prepare_execution(request).mission_id == "m-2"
    assert adapter.execute_task(request).task_id == "t-1"
    assert adapter.collect_logs("m-2") == ("log:m-2",)
    assert adapter.stop_execution("m-2").status == RuntimeStatus.STOPPED
    assert adapter.validate_artifacts("m-2", ["a.md"]) == ("a.md",)
