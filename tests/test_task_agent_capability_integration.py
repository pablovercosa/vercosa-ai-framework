from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import pytest

from vercosa_ai_framework.agents import AgentOrchestrator, AgentProfile, AgentRegistry, AgentRole, AgentTaskExecutor
from vercosa_ai_framework.capabilities import CapabilityProfile, CapabilityRegistry, CapabilityResolver
from vercosa_ai_framework.missions import DirectoryMissionQueue, InMemoryWorkflowProvider, Mission, MissionRunner, MissionStatus, QueueBackedWorkflowExecutor
from vercosa_ai_framework.model_selection import ModelProfile
from vercosa_ai_framework.runtime import RuntimeAdapter, RuntimeExecutionPlan, RuntimeExecutionRequest, RuntimeExecutionResult, RuntimeInfo, RuntimeStatus
from vercosa_ai_framework.skills import SkillProfile, SkillRegistry
from vercosa_ai_framework.tasks import Task, TaskQueue, TaskQueueState, TaskScheduler
from vercosa_ai_framework.workflows import Workflow, WorkflowEngine, WorkflowStatus, WorkflowTask


class FakeRuntimeAdapter(RuntimeAdapter):
    def __init__(self, statuses: tuple[RuntimeStatus, ...] = (RuntimeStatus.DONE,)) -> None:
        self.statuses = list(statuses)
        self.requests: list[RuntimeExecutionRequest] = []

    def detect_runtime(self, workspace: str) -> RuntimeInfo:
        return RuntimeInfo(runtime_id="fake", runtime_name="Fake", available=True)

    def list_models(self) -> tuple[ModelProfile, ...]:
        return ()

    def prepare_execution(self, request: RuntimeExecutionRequest) -> RuntimeExecutionPlan:
        return RuntimeExecutionPlan(mission_id=request.mission_id, workspace=request.workspace)

    def execute_mission(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        return RuntimeExecutionResult(mission_id=request.mission_id, runtime_id="fake", status=RuntimeStatus.DONE)

    def execute_task(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        self.requests.append(request)
        status = self.statuses.pop(0) if self.statuses else RuntimeStatus.DONE
        return RuntimeExecutionResult(
            mission_id=request.mission_id,
            runtime_id="fake",
            status=status,
            workflow_id=request.workflow_id,
            task_id=request.task_id,
            artifacts=(f"artifact-{len(self.requests)}.md",) if status == RuntimeStatus.DONE else (),
            errors=() if status == RuntimeStatus.DONE else ("runtime failed",),
            audit_log_ref=f"memory://runtime/{len(self.requests)}",
        )

    def collect_logs(self, mission_id: str, task_id: str | None = None) -> tuple[str, ...]:
        return ()

    def stop_execution(self, mission_id: str, task_id: str | None = None) -> RuntimeExecutionResult:
        return RuntimeExecutionResult(mission_id=mission_id, runtime_id="fake", status=RuntimeStatus.STOPPED)

    def validate_artifacts(self, mission_id: str, expected_artifacts: Iterable[str]) -> tuple[str, ...]:
        return tuple(expected_artifacts)


def agent_profile(*, capabilities: tuple[str, ...] = ("ReadContext",)) -> AgentProfile:
    return AgentProfile(
        agent_profile_id="agent-framework",
        role=AgentRole.IMPLEMENTATION_ARCHITECT,
        domain="framework",
        supported_task_types=("integration-test",),
        supported_capabilities=capabilities,
        complexity_range=("low", "medium", "high"),
        risk_range=("low", "medium", "high"),
    )


def capability(name: str = "ReadContext", *, permissions: tuple[str, ...] = ("read_workspace",)) -> CapabilityProfile:
    return CapabilityProfile(
        capability_id=f"cap-{name}",
        name=name,
        version="1.0",
        description="Resolve contexto por contrato declarativo.",
        intent="Ler contexto permitido por referencia.",
        domain="framework",
        required_permissions=permissions,
    )


def skill(name: str = "ReadContext") -> SkillProfile:
    return SkillProfile(
        skill_id=f"skill-{name}",
        name=f"declarative-{name}",
        version="1.0",
        description="Skill declarativa sem tools para testes.",
        implemented_capabilities=(name,),
        domain="framework",
        required_tools=(),
        permission_requirements=("read_workspace",),
    )


def resolver(*, capabilities: tuple[CapabilityProfile, ...] | None = None) -> CapabilityResolver:
    profiles = capabilities if capabilities is not None else (capability(),)
    return CapabilityResolver(CapabilityRegistry(profiles), SkillRegistry(tuple(skill(profile.name) for profile in profiles)))


def task(*, required_capabilities: tuple[str, ...] = ("ReadContext",), max_attempts: int = 1, retryable: bool = False) -> Task:
    return Task(
        title="Executar task por agente",
        goal="Executar fluxo local minimo.",
        workflow_id="wf-0105",
        mission_id="mission-0105",
        task_id="task-0105",
        task_type="integration-test",
        risk_level="low",
        required_capabilities=required_capabilities,
        context_refs=("specs/framework/0009-capabilities-skills-tools.md",),
        max_attempts=max_attempts,
        metadata={
            "granted_permissions": ("read_workspace",),
            "capability_inputs": {"ReadContext": {"ref": "docs/task-queue.md"}},
            "retry_policy": {"retryable_agent_failures": retryable},
        },
    )


def executor(runtime: FakeRuntimeAdapter, *, profile: AgentProfile | None = None, capability_resolver: CapabilityResolver | None = None) -> AgentTaskExecutor:
    orchestrator = AgentOrchestrator(
        registry=AgentRegistry((profile or agent_profile(),)),
        runtime_adapter=runtime,
        capability_resolver=capability_resolver or resolver(),
        require_capability_resolution=True,
    )
    return AgentTaskExecutor(orchestrator)


def run_task(task_to_run: Task, task_executor: AgentTaskExecutor) -> tuple[TaskQueue, object]:
    queue = TaskQueue(workflow_id=task_to_run.workflow_id, mission_id=task_to_run.mission_id)
    queue.add_task(task_to_run)
    result = TaskScheduler().run_until_idle(queue, task_executor)
    return queue, result


def test_task_scheduler_agent_orchestrator_capability_resolver_success_path():
    runtime = FakeRuntimeAdapter()

    queue, scheduler_result = run_task(task(), executor(runtime))

    finished = queue.list_tasks()[0]
    attempt = queue.attempts_for(finished.task_id)[0]
    runtime_request = runtime.requests[0]
    agent_request = runtime_request.context["agent_execution_request"]
    resolution = agent_request.metadata["capability_resolutions"][0]

    assert scheduler_result.status == "done"
    assert finished.state == TaskQueueState.DONE
    assert finished.agent_assignment_ref == agent_request.agent_assignment_id
    assert attempt.agent_assignment_ref == agent_request.agent_assignment_id
    assert resolution["capability"] == "ReadContext"
    assert resolution["skill_id"] == "skill-ReadContext"
    assert resolution["declarative_resolution_only"] is True
    assert resolution["request_id"]
    assert runtime_request.context["capability_resolutions"] == agent_request.metadata["capability_resolutions"]
    assert len(runtime.requests) == 1


def test_missing_capability_blocks_runtime_and_fails_task_queue():
    runtime = FakeRuntimeAdapter()

    queue, scheduler_result = run_task(
        task(required_capabilities=("MissingCapability",)),
        executor(runtime, profile=agent_profile(capabilities=("MissingCapability",))),
    )

    finished = queue.list_tasks()[0]
    assert finished.state == TaskQueueState.FAILED
    assert "unknown capability" in (finished.last_error or "")
    assert runtime.requests == []
    assert scheduler_result.errors


def test_missing_permission_blocks_resolution_before_runtime():
    runtime = FakeRuntimeAdapter()
    unsafe_task = task().with_state(TaskQueueState.QUEUED, metadata={"granted_permissions": ()})

    queue, _ = run_task(unsafe_task, executor(runtime))

    finished = queue.list_tasks()[0]
    assert finished.state == TaskQueueState.FAILED
    assert "permissions" in (finished.last_error or "")
    assert runtime.requests == []


def test_incompatible_agent_blocks_before_capability_resolver_and_runtime():
    runtime = FakeRuntimeAdapter()
    queue, _ = run_task(task(), executor(runtime, profile=agent_profile(capabilities=("OtherCapability",))))

    finished = queue.list_tasks()[0]
    assert finished.state == TaskQueueState.FAILED
    assert "no compatible agent profile" in (finished.last_error or "")
    assert runtime.requests == []


def test_retry_creates_new_attempt_and_new_agent_assignment_without_orchestrator_controlling_retry():
    runtime = FakeRuntimeAdapter((RuntimeStatus.FAILED, RuntimeStatus.DONE))

    queue, scheduler_result = run_task(task(max_attempts=2, retryable=True), executor(runtime))

    attempts = queue.attempts_for("task-0105")
    assignments = tuple(attempt.agent_assignment_ref for attempt in attempts)

    assert scheduler_result.status == "done"
    assert len(attempts) == 2
    assert attempts[0].attempt_id != attempts[1].attempt_id
    assert assignments[0] != assignments[1]
    assert len(runtime.requests) == 2
    assert queue.list_tasks()[0].state == TaskQueueState.DONE


def test_mission_workflow_task_agent_capability_incremental_flow(tmp_path):
    mission = Mission(title="0105", goal="Executar fluxo integrado completo minimo")
    workflow_task = WorkflowTask(
        task_id="task-0105",
        workflow_id="wf-0105",
        mission_id=mission.mission_id,
        title="Task integrada",
        goal="Executar via Agent Orchestrator e Capability Resolver",
        task_type="integration-test",
        required_capabilities=("ReadContext",),
        inputs={
            "granted_permissions": ("read_workspace",),
            "capability_inputs": {"ReadContext": {"ref": "docs/examples/minimal-task-agent-capability-flow.md"}},
        },
        expected_outputs=("artifact-1.md",),
        validation_policy={"required": True},
    )
    workflow = Workflow(
        workflow_id="wf-0105",
        mission_id=mission.mission_id,
        title="Workflow integrado 0105",
        goal=mission.goal,
        execution_limits={"max_parallel_tasks": 1},
        tasks=(workflow_task,),
    )
    runtime = FakeRuntimeAdapter()
    workflow_engine = WorkflowEngine(
        runtime,
        guardian=AgentOrchestrator(registry=AgentRegistry(()), runtime_adapter=runtime).guardian_engine,
        workspace=str(tmp_path),
        queue_task_executor=executor(runtime),
    )
    mission_queue = DirectoryMissionQueue(tmp_path)
    mission_queue.enqueue(mission)
    runner = MissionRunner(
        mission_queue,
        runtime,
        workflow_provider=InMemoryWorkflowProvider({mission.mission_id: workflow}),
        workflow_executor=QueueBackedWorkflowExecutor(workflow_engine),
    )

    result = runner.run(mission.mission_id)

    assert result.status == MissionStatus.DONE
    assert workflow_engine.last_workflow is not None
    assert workflow_engine.last_workflow.status == WorkflowStatus.DONE
    assert runtime.requests[0].context["capability_resolutions"][0]["skill_id"] == "skill-ReadContext"
    assert result.artifacts == ("artifact-1.md",)


def test_static_boundaries_do_not_cross_forbidden_execution_layers():
    tasks_dir = Path("src/vercosa_ai_framework/tasks")
    for path in tasks_dir.glob("*.py"):
        content = path.read_text(encoding="utf-8")
        assert "vercosa_ai_framework.agents" not in content
        assert "vercosa_ai_framework.capabilities" not in content

    orchestrator = Path("src/vercosa_ai_framework/agents/orchestrator.py").read_text(encoding="utf-8")
    resolver_source = Path("src/vercosa_ai_framework/capabilities/resolver.py").read_text(encoding="utf-8")
    assert "SkillExecutor" not in orchestrator
    assert "ToolExecutor" not in orchestrator
    assert "ProviderGateway" not in orchestrator
    assert ".execute(" not in resolver_source
