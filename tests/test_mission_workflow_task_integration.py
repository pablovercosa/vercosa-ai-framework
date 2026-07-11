from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from vercosa_ai_framework.guardian import GuardianAction, GuardianDecision, GuardianEvaluationContext
from vercosa_ai_framework.missions import (
    DirectoryMissionQueue,
    InMemoryWorkflowProvider,
    Mission,
    MissionRunner,
    MissionStatus,
    QueueBackedWorkflowExecutor,
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
from vercosa_ai_framework.workflows import TaskDependency, Workflow, WorkflowEngine, WorkflowStatus, WorkflowTask


class FakeRuntimeAdapter(RuntimeAdapter):
    def __init__(self, task_results: Iterable[RuntimeExecutionResult]) -> None:
        self.task_results = list(task_results)
        self.mission_requests: list[RuntimeExecutionRequest] = []
        self.task_requests: list[RuntimeExecutionRequest] = []

    def detect_runtime(self, workspace: str) -> RuntimeInfo:
        return RuntimeInfo(runtime_id="fake", runtime_name="Fake", available=True)

    def list_models(self) -> tuple[ModelProfile, ...]:
        return ()

    def prepare_execution(self, request: RuntimeExecutionRequest) -> RuntimeExecutionPlan:
        return RuntimeExecutionPlan(mission_id=request.mission_id, workspace=request.workspace)

    def execute_mission(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        self.mission_requests.append(request)
        return RuntimeExecutionResult(mission_id=request.mission_id, runtime_id="fake", status=RuntimeStatus.DONE)

    def execute_task(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        self.task_requests.append(request)
        if self.task_results:
            result = self.task_results.pop(0)
            return RuntimeExecutionResult(
                mission_id=request.mission_id,
                runtime_id="fake",
                status=result.status,
                workflow_id=request.workflow_id,
                task_id=request.task_id,
                artifacts=result.artifacts,
                changed_files=result.changed_files,
                validation_results=result.validation_results,
                warnings=result.warnings,
                errors=result.errors,
                requires_review=result.requires_review,
                audit_log_ref=result.audit_log_ref,
            )
        return RuntimeExecutionResult(
            mission_id=request.mission_id,
            runtime_id="fake",
            status=RuntimeStatus.FAILED,
            workflow_id=request.workflow_id,
            task_id=request.task_id,
            errors=("no task result configured",),
        )

    def collect_logs(self, mission_id: str, task_id: str | None = None) -> tuple[str, ...]:
        return (f"log:{mission_id}:{task_id}",)

    def stop_execution(self, mission_id: str, task_id: str | None = None) -> RuntimeExecutionResult:
        return RuntimeExecutionResult(mission_id=mission_id, runtime_id="fake", status=RuntimeStatus.STOPPED)

    def validate_artifacts(self, mission_id: str, expected_artifacts: Iterable[str]) -> tuple[str, ...]:
        return tuple(expected_artifacts)


class AllowGuardian:
    def __init__(self) -> None:
        self.contexts: list[GuardianEvaluationContext] = []

    def evaluate(self, context: GuardianEvaluationContext) -> GuardianDecision:
        self.contexts.append(context)
        return GuardianDecision(
            mission_id=context.mission_id,
            evaluation_id=context.evaluation_id or context.mission_id,
            decision=GuardianAction.ALLOW,
            guardian_mode=context.guardian_mode,
        )


def runtime_result(status: RuntimeStatus, **kwargs: object) -> RuntimeExecutionResult:
    return RuntimeExecutionResult(mission_id="unused", runtime_id="fake", status=status, **kwargs)


def workflow_for(mission: Mission, *tasks: WorkflowTask) -> Workflow:
    return Workflow(
        workflow_id="wf-0104",
        mission_id=mission.mission_id,
        title="Fluxo integrado mínimo",
        goal=mission.goal,
        execution_limits={"max_parallel_tasks": 1},
        tasks=tasks,
    )


def workflow_task(
    mission: Mission,
    task_id: str,
    *,
    dependencies: tuple[TaskDependency, ...] = (),
    max_attempts: int = 1,
) -> WorkflowTask:
    return WorkflowTask(
        task_id=task_id,
        workflow_id="wf-0104",
        mission_id=mission.mission_id,
        title=f"Task {task_id}",
        goal=f"Executar {task_id}",
        task_type="integration-test",
        priority=50 if task_id == "task-a" else 100,
        risk_level="low",
        required_capabilities=("local-execution",),
        dependencies=dependencies,
        acceptance_criteria=("runtime retornou done",),
        expected_outputs=(f"{task_id}.md",),
        inputs={"target_paths": (f"docs/{task_id}.md",)},
        model_policy={"model": "auto"},
        validation_policy={"required": True},
        execution_limits={"timeout_seconds": 30},
        retry_policy={"max_attempts": max_attempts},
    )


def integrated_runner(
    tmp_path: Path,
    mission: Mission,
    workflow: Workflow,
    runtime: FakeRuntimeAdapter,
    guardian: AllowGuardian | None = None,
) -> tuple[DirectoryMissionQueue, WorkflowEngine, MissionRunner]:
    queue = DirectoryMissionQueue(tmp_path)
    queue.enqueue(mission)
    engine = WorkflowEngine(runtime, guardian or AllowGuardian(), workspace=str(tmp_path))
    runner = MissionRunner(
        queue,
        runtime,
        workflow_provider=InMemoryWorkflowProvider({mission.mission_id: workflow}),
        workflow_executor=QueueBackedWorkflowExecutor(engine),
    )
    return queue, engine, runner


def test_integrated_flow_runs_two_dependent_tasks_once_and_finishes_mission(tmp_path):
    mission = Mission(title="Integrar", goal="Executar fluxo integrado")
    first = workflow_task(mission, "task-a")
    second = workflow_task(mission, "task-b", dependencies=(TaskDependency("requires_completion", "task-a"),))
    workflow = workflow_for(mission, second, first)
    runtime = FakeRuntimeAdapter(
        [
            runtime_result(RuntimeStatus.DONE, artifacts=("a.md",)),
            runtime_result(RuntimeStatus.DONE, artifacts=("b.md",)),
        ]
    )
    queue, engine, runner = integrated_runner(tmp_path, mission, workflow, runtime)

    result = runner.run(mission.mission_id)

    assert result.status == MissionStatus.DONE
    assert queue.get(mission.mission_id).status == MissionStatus.DONE
    assert queue.get(mission.mission_id).cycle_count == 1
    assert runtime.mission_requests == []
    assert [request.task_id for request in runtime.task_requests] == ["task-a", "task-b"]
    assert result.artifacts == ("a.md", "b.md")
    assert engine.last_workflow is not None
    assert engine.last_workflow.status == WorkflowStatus.DONE
    assert {task.task_id: task.attempt_count for task in engine.last_workflow.tasks} == {"task-a": 1, "task-b": 1}


def test_integrated_flow_retries_required_task_and_blocks_dependent(tmp_path):
    mission = Mission(title="Falhar", goal="Preservar falha integrada")
    first = workflow_task(mission, "task-a", max_attempts=2)
    second = workflow_task(mission, "task-b", dependencies=(TaskDependency("requires_completion", "task-a"),))
    workflow = workflow_for(mission, first, second)
    runtime = FakeRuntimeAdapter(
        [
            runtime_result(RuntimeStatus.FAILED, errors=("falha transitória",)),
            runtime_result(RuntimeStatus.FAILED, errors=("falha final",)),
        ]
    )
    queue, engine, runner = integrated_runner(tmp_path, mission, workflow, runtime)

    result = runner.run(mission.mission_id)

    assert result.status == MissionStatus.FAILED
    assert queue.get(mission.mission_id).status == MissionStatus.FAILED
    assert [request.task_id for request in runtime.task_requests] == ["task-a", "task-a"]
    assert "falha final" in result.errors
    assert engine.last_workflow is not None
    assert [(task.task_id, task.status.value, task.attempt_count) for task in engine.last_workflow.tasks] == [
        ("task-a", "failed", 2),
        ("task-b", "blocked", 0),
    ]


def test_runner_without_workflow_integration_preserves_legacy_runtime_path(tmp_path):
    queue = DirectoryMissionQueue(tmp_path)
    mission = queue.enqueue(Mission(title="Legado", goal="Executar caminho legado"))
    runtime = FakeRuntimeAdapter([])
    runner = MissionRunner(queue, runtime)

    result = runner.run(mission.mission_id)

    assert result.status == MissionStatus.DONE
    assert len(runtime.mission_requests) == 1
    assert runtime.task_requests == []


def test_task_queue_boundaries_do_not_import_upper_or_runtime_layers():
    tasks_dir = Path("src/vercosa_ai_framework/tasks")
    forbidden = (
        "vercosa_ai_framework.workflows",
        "vercosa_ai_framework.missions",
        "vercosa_ai_framework.runtime",
        "vercosa_ai_framework.providers",
        "vercosa_ai_framework.agents",
        "vercosa_ai_framework.capabilities",
        "vercosa_ai_framework.skills",
        "vercosa_ai_framework.tools",
    )

    for path in tasks_dir.glob("*.py"):
        content = path.read_text(encoding="utf-8")
        assert not any(import_ref in content for import_ref in forbidden), path
