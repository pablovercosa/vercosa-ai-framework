from __future__ import annotations

from collections.abc import Iterable

from vercosa_ai_framework.guardian import (
    GuardianAction,
    GuardianDecision,
    GuardianEvaluationContext,
    GuardianMode,
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
from vercosa_ai_framework.workflows import (
    TaskDependency,
    TaskStatus,
    Workflow,
    WorkflowEngine,
    WorkflowStatus,
    WorkflowTask,
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
        return self.execute_task(request)

    def execute_task(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        self.requests.append(request)
        if self.results:
            result = self.results.pop(0)
            return RuntimeExecutionResult(
                mission_id=result.mission_id,
                runtime_id=result.runtime_id,
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
            errors=("no fake runtime result configured",),
        )

    def collect_logs(self, mission_id: str, task_id: str | None = None) -> tuple[str, ...]:
        return (f"log:{mission_id}:{task_id}",)

    def stop_execution(self, mission_id: str, task_id: str | None = None) -> RuntimeExecutionResult:
        return RuntimeExecutionResult(mission_id=mission_id, runtime_id="fake", status=RuntimeStatus.STOPPED)

    def validate_artifacts(
        self, mission_id: str, expected_artifacts: Iterable[str]
    ) -> tuple[str, ...]:
        return tuple(expected_artifacts)


class FakeGuardian:
    def __init__(self, blocked_task_ids: Iterable[str] = ()) -> None:
        self.blocked_task_ids = set(blocked_task_ids)
        self.contexts: list[GuardianEvaluationContext] = []

    def evaluate(self, context: GuardianEvaluationContext) -> GuardianDecision:
        self.contexts.append(context)
        task_id = str(context.metadata.get("task_id", ""))
        if task_id in self.blocked_task_ids:
            return GuardianDecision(
                mission_id=context.mission_id,
                evaluation_id=context.evaluation_id or task_id,
                decision=GuardianAction.BLOCK,
                guardian_mode=context.guardian_mode,
                reasons=("blocked by fake guardian",),
                blocked_items=(task_id,),
            )
        return GuardianDecision(
            mission_id=context.mission_id,
            evaluation_id=context.evaluation_id or task_id,
            decision=GuardianAction.ALLOW,
            guardian_mode=context.guardian_mode,
        )


def runtime_result(mission_id: str, status: RuntimeStatus, **kwargs: object) -> RuntimeExecutionResult:
    return RuntimeExecutionResult(mission_id=mission_id, runtime_id="fake", status=status, **kwargs)


def workflow_with_tasks(*tasks: WorkflowTask) -> Workflow:
    return Workflow(
        workflow_id="wf-1",
        mission_id="mission-1",
        title="Workflow Engine MVP",
        goal="Execute governed tasks sequentially",
        spec_refs=("specs/framework/0006-workflow-engine.md",),
        tasks=tasks,
    )


def task(task_id: str, *, dependencies: tuple[TaskDependency, ...] = ()) -> WorkflowTask:
    return WorkflowTask(
        task_id=task_id,
        workflow_id="wf-1",
        mission_id="mission-1",
        title=f"Task {task_id}",
        goal=f"Run {task_id}",
        acceptance_criteria=("runtime returned done",),
        dependencies=dependencies,
    )


def test_engine_executes_tasks_sequentially_respecting_dependencies():
    first = task("task-a")
    second = task(
        "task-b",
        dependencies=(TaskDependency("requires_completion", "task-a"),),
    )
    workflow = workflow_with_tasks(second, first)
    runtime = FakeRuntimeAdapter(
        [
            runtime_result("mission-1", RuntimeStatus.DONE, artifacts=("a.md",)),
            runtime_result("mission-1", RuntimeStatus.DONE, artifacts=("b.md",)),
        ]
    )
    guardian = FakeGuardian()
    engine = WorkflowEngine(runtime, guardian, workspace="/workspace")

    result = engine.execute(workflow)

    assert result.status == WorkflowStatus.DONE
    assert result.closure_recommendation == "conclude"
    assert [request.task_id for request in runtime.requests] == ["task-a", "task-b"]
    assert [context.metadata["task_id"] for context in guardian.contexts] == ["task-a", "task-b"]
    assert [task_result.status for task_result in result.task_results] == [TaskStatus.DONE, TaskStatus.DONE]
    assert result.artifacts == ("a.md", "b.md")
    assert engine.last_workflow is not None
    assert [task.status for task in engine.last_workflow.tasks] == [TaskStatus.DONE, TaskStatus.DONE]


def test_engine_fails_workflow_when_required_task_fails():
    workflow = workflow_with_tasks(task("task-a"), task("task-b"))
    runtime = FakeRuntimeAdapter(
        [runtime_result("mission-1", RuntimeStatus.FAILED, errors=("runtime failed",))]
    )
    engine = WorkflowEngine(runtime, FakeGuardian())

    result = engine.execute(workflow)

    assert result.status == WorkflowStatus.FAILED
    assert result.errors == ("runtime failed",)
    assert [request.task_id for request in runtime.requests] == ["task-a"]
    assert [task_result.status for task_result in result.task_results] == [TaskStatus.FAILED]


def test_engine_skips_task_when_required_dependency_failed():
    failed_dependency = WorkflowTask(
        task_id="task-a",
        workflow_id="wf-1",
        mission_id="mission-1",
        title="Optional setup",
        goal="May fail without failing workflow",
        acceptance_criteria=("runtime attempted",),
        validation_policy={"required": False},
    )
    dependent = task(
        "task-b",
        dependencies=(TaskDependency("requires_completion", "task-a"),),
    )
    workflow = workflow_with_tasks(failed_dependency, dependent)
    runtime = FakeRuntimeAdapter(
        [runtime_result("mission-1", RuntimeStatus.FAILED, errors=("optional failed",))]
    )
    engine = WorkflowEngine(runtime, FakeGuardian())

    result = engine.execute(workflow)

    assert result.status == WorkflowStatus.DONE
    assert [request.task_id for request in runtime.requests] == ["task-a"]
    assert [task_result.status for task_result in result.task_results] == [TaskStatus.FAILED, TaskStatus.SKIPPED]
    assert result.task_results[1].errors == ("dependency failed",)


def test_engine_evaluates_guardian_before_runtime_and_blocks_task():
    workflow = workflow_with_tasks(task("task-a"), task("task-b"))
    runtime = FakeRuntimeAdapter([runtime_result("mission-1", RuntimeStatus.DONE)])
    guardian = FakeGuardian(blocked_task_ids=("task-a",))
    engine = WorkflowEngine(runtime, guardian, guardian_mode=GuardianMode.STRICT)

    result = engine.execute(workflow)

    assert result.status == WorkflowStatus.FAILED
    assert result.errors == ("guardian blocked task: blocked by fake guardian",)
    assert runtime.requests == []
    assert len(guardian.contexts) == 1
    assert guardian.contexts[0].guardian_mode == GuardianMode.STRICT
    assert guardian.contexts[0].metadata["task_id"] == "task-a"


def test_engine_rejects_unresolvable_dependencies_without_runtime_execution():
    workflow = workflow_with_tasks(
        task(
            "task-a",
            dependencies=(TaskDependency("requires_completion", "missing-task"),),
        )
    )
    runtime = FakeRuntimeAdapter([runtime_result("mission-1", RuntimeStatus.DONE)])
    guardian = FakeGuardian()
    engine = WorkflowEngine(runtime, guardian)

    result = engine.execute(workflow)

    assert result.status == WorkflowStatus.FAILED
    assert result.errors == ("unresolvable dependency: task task-a requires missing-task",)
    assert runtime.requests == []
    assert guardian.contexts == []
