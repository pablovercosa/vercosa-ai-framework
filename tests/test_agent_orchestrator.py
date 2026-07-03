from __future__ import annotations

from collections.abc import Iterable

import pytest

from vercosa_ai_framework.agents import (
    AgentExecutionRequest,
    AgentOrchestrator,
    AgentProfile,
    AgentRegistry,
    AgentRole,
    AgentState,
    NoCompatibleAgentError,
)
from vercosa_ai_framework.model_selection import ModelProfile
from vercosa_ai_framework.runtime import (
    RuntimeAdapter,
    RuntimeExecutionPlan,
    RuntimeExecutionRequest,
    RuntimeExecutionResult,
    RuntimeInfo,
    RuntimeStatus,
)
from vercosa_ai_framework.tasks import Task, TaskAttempt


class FakeRuntimeAdapter(RuntimeAdapter):
    def __init__(self, result_status: RuntimeStatus = RuntimeStatus.DONE) -> None:
        self.result_status = result_status
        self.requests: list[RuntimeExecutionRequest] = []

    def detect_runtime(self, workspace: str) -> RuntimeInfo:
        return RuntimeInfo(runtime_id="fake", runtime_name="Fake", available=True)

    def list_models(self) -> tuple[ModelProfile, ...]:
        return ()

    def prepare_execution(self, request: RuntimeExecutionRequest) -> RuntimeExecutionPlan:
        return RuntimeExecutionPlan(mission_id=request.mission_id, workspace=request.workspace)

    def execute_mission(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        return self.execute_task(request)

    def execute_task(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        self.requests.append(request)
        return RuntimeExecutionResult(
            mission_id=request.mission_id,
            runtime_id="fake",
            status=self.result_status,
            workflow_id=request.workflow_id,
            task_id=request.task_id,
            artifacts=("docs/agent-orchestrator.md",),
            validation_results=("pytest",),
            errors=() if self.result_status == RuntimeStatus.DONE else ("runtime failed",),
            audit_log_ref="memory://fake/task-1",
        )

    def collect_logs(self, mission_id: str, task_id: str | None = None) -> tuple[str, ...]:
        return ()

    def stop_execution(self, mission_id: str, task_id: str | None = None) -> RuntimeExecutionResult:
        return RuntimeExecutionResult(mission_id=mission_id, runtime_id="fake", status=RuntimeStatus.STOPPED)

    def validate_artifacts(self, mission_id: str, expected_artifacts: Iterable[str]) -> tuple[str, ...]:
        return tuple(expected_artifacts)


def profile() -> AgentProfile:
    return AgentProfile(
        agent_profile_id="implementation-architect-framework",
        role=AgentRole.IMPLEMENTATION_ARCHITECT,
        domain="framework",
        supported_task_types=("implementation",),
        supported_capabilities=("ReadContext", "SearchCode", "RunValidation"),
        tags=("python", "contracts"),
        complexity_range=("low", "medium", "high"),
        risk_range=("low", "medium", "high"),
        default_execution_limits={"max_cycles": 2},
    )


def task(**metadata_overrides: object) -> Task:
    metadata = {
        "role": "implementation_architect",
        "domain": "framework",
        "tags": ("python", "contracts"),
        "complexity": "medium",
        "expected_outputs": ("AgentExecutionResult",),
        "acceptance_criteria": ("pytest passes",),
        "execution_limits": {"max_cycles": 3},
        "allowed_paths": ("src/vercosa_ai_framework/agents/",),
    }
    metadata.update(metadata_overrides)
    return Task(
        title="Implement Agent Orchestrator MVP",
        goal="Implementar MVP do Agent Orchestrator. Entregaveis: codigo, testes e docs. Criterios de aceite: pytest passa.",
        workflow_id="wf-1",
        mission_id="mission-1",
        task_id="task-1",
        task_type="implementation",
        risk_level="medium",
        required_capabilities=("ReadContext", "RunValidation"),
        context_refs=("specs/framework/0008-agent-orchestrator.md",),
        metadata=metadata,
    )


def test_orchestrator_selects_agent_builds_request_executes_runtime_and_returns_result():
    runtime = FakeRuntimeAdapter()
    orchestrator = AgentOrchestrator(
        registry=AgentRegistry((profile(),)),
        runtime_adapter=runtime,
        workspace="/workspace",
    )
    attempt = TaskAttempt(task_id="task-1", workflow_id="wf-1", mission_id="mission-1", attempt_number=1)

    result = orchestrator.execute_task(task(), attempt)

    assert result.success is True
    assert result.state == AgentState.DONE
    assert result.agent_profile_id == "implementation-architect-framework"
    assert result.artifact_refs == ("docs/agent-orchestrator.md",)
    assert result.validation_results == ("pytest",)
    assert result.metadata["state_transitions"] == (
        "idle->planning",
        "planning->executing",
        "executing->validating",
        "validating->done",
    )

    assert len(runtime.requests) == 1
    runtime_request = runtime.requests[0]
    agent_request = runtime_request.context["agent_execution_request"]
    assert isinstance(agent_request, AgentExecutionRequest)
    assert agent_request.required_capabilities == ("ReadContext", "RunValidation")
    assert runtime_request.permissions["mcp_direct_access"] is False
    assert runtime_request.selection_decision is None


def test_orchestrator_selects_model_when_catalog_and_policy_are_provided():
    runtime = FakeRuntimeAdapter()
    orchestrator = AgentOrchestrator(
        registry=AgentRegistry((profile(),)),
        runtime_adapter=runtime,
        model_catalog=(
            ModelProfile(
                id="local-strong",
                provider="ollama",
                runtime="local",
                quality_tier="high",
                reasoning_tier="high",
                memory_tier="long",
                context_window=32_000,
                local=True,
                free=True,
            ),
        ),
    )

    result = orchestrator.execute_task(
        task(
            model_policy={
                "quality": "high",
                "reasoning": "high",
                "memory": "long",
                "allow_paid": False,
                "prefer_local": True,
            }
        )
    )

    assert result.success is True
    assert runtime.requests[0].selection_decision is not None
    assert runtime.requests[0].selection_decision.selected_model.id == "local-strong"
    assert result.metadata["selected_model"] == "local-strong"


def test_orchestrator_fails_before_runtime_when_guardian_blocks():
    runtime = FakeRuntimeAdapter()
    orchestrator = AgentOrchestrator(
        registry=AgentRegistry((profile(),)),
        runtime_adapter=runtime,
    )

    blocked_task = task()
    blocked_task = blocked_task.with_state(
        blocked_task.state,
        goal="Implementar com api_key=super-secret-token-123456. Entregaveis: bloquear. Criterios de aceite: bloquear.",
    )
    result = orchestrator.execute_task(blocked_task)

    assert result.success is False
    assert result.state == AgentState.FAILED
    assert runtime.requests == []
    assert result.metadata["state_transitions"] == ("idle->planning", "planning->failed")


def test_orchestrator_raises_when_no_agent_is_compatible():
    orchestrator = AgentOrchestrator(
        registry=AgentRegistry((profile(),)),
        runtime_adapter=FakeRuntimeAdapter(),
    )

    unsupported = task(domain="unknown")

    with pytest.raises(NoCompatibleAgentError, match="no compatible agent profile"):
        orchestrator.execute_task(unsupported)


def test_orchestrator_maps_runtime_failure_to_failed_agent_result():
    orchestrator = AgentOrchestrator(
        registry=AgentRegistry((profile(),)),
        runtime_adapter=FakeRuntimeAdapter(RuntimeStatus.FAILED),
    )

    result = orchestrator.execute_task(task())

    assert result.success is False
    assert result.state == AgentState.FAILED
    assert result.errors == ("runtime failed",)
    assert result.metadata["state_transitions"][-1] == "validating->failed"
