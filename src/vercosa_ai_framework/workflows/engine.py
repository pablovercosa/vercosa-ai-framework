"""Sequential Workflow Engine MVP.

The engine coordinates governed task execution through abstract boundaries. It
does not execute commands, call OpenCode directly, choose models, or bypass the
Guardian Engine.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Protocol

from vercosa_ai_framework.guardian import (
    GuardianAction,
    GuardianDecision,
    GuardianEvaluationContext,
    GuardianMode,
)
from vercosa_ai_framework.runtime import (
    RuntimeAdapter,
    RuntimeExecutionRequest,
    RuntimeExecutionResult,
    RuntimeStatus,
)
from vercosa_ai_framework.workflows.types import (
    TaskResult,
    TaskStatus,
    Workflow,
    WorkflowResult,
    WorkflowStatus,
    WorkflowTask,
    utc_now_iso,
)


class WorkflowEngineError(RuntimeError):
    """Raised when a workflow plan cannot be executed safely."""


class GuardianEvaluator(Protocol):
    """Testable Guardian Engine boundary used by the Workflow Engine."""

    def evaluate(self, context: GuardianEvaluationContext) -> GuardianDecision:
        """Evaluate a workflow or task policy context."""


class WorkflowEngine:
    """Execute workflow tasks sequentially through a Runtime Adapter."""

    def __init__(
        self,
        runtime: RuntimeAdapter,
        guardian: GuardianEvaluator,
        *,
        workspace: str = ".",
        guardian_mode: GuardianMode | str = GuardianMode.STANDARD,
        engine_id: str = "workflow-engine",
    ) -> None:
        self.runtime = runtime
        self.guardian = guardian
        self.workspace = workspace
        self.guardian_mode = GuardianMode(guardian_mode)
        self.engine_id = engine_id
        self.audit_log: list[str] = []
        self.last_workflow: Workflow | None = None

    def execute(self, workflow: Workflow) -> WorkflowResult:
        """Run eligible tasks one at a time until the workflow closes."""

        if workflow.execution_mode != "sequential":
            return self._workflow_result(
                workflow.with_status(WorkflowStatus.FAILED, finished_at=utc_now_iso()),
                errors=(f"unsupported execution mode: {workflow.execution_mode}",),
                closure_recommendation="fail",
            )

        working = workflow.with_status(WorkflowStatus.RUNNING, started_at=workflow.started_at or utc_now_iso())
        task_map = {task.task_id: task for task in working.tasks}
        task_results: list[TaskResult] = []
        failed_tasks: set[str] = set()
        failed_required: set[str] = set()

        self._log(working, "workflow started")
        dependency_error = self._dependency_error(working)
        if dependency_error is not None:
            failed = working.with_status(WorkflowStatus.FAILED, finished_at=utc_now_iso())
            self.last_workflow = failed
            return self._workflow_result(failed, errors=(dependency_error,), closure_recommendation="fail")

        for task in self._ordered_tasks(working):
            current = task_map[task.task_id]
            failed_dependencies = self._failed_dependencies(current, failed_tasks)
            if failed_dependencies:
                skipped = current.with_status(
                    TaskStatus.SKIPPED,
                    blocked_by=failed_dependencies,
                    finished_at=utc_now_iso(),
                    last_error="dependency failed",
                )
                task_map[skipped.task_id] = skipped
                task_results.append(self._task_result(skipped, errors=("dependency failed",)))
                self._log(working, f"task skipped task_id={skipped.task_id} reason=dependency_failed")
                continue

            ready = current.with_status(TaskStatus.READY, blocked_by=())
            task_map[ready.task_id] = ready
            self._log(working, f"task ready task_id={ready.task_id}")

            guardian_decision = self._evaluate_task(working, ready)
            if guardian_decision.decision == GuardianAction.REQUIRE_APPROVAL:
                blocked = ready.with_status(
                    TaskStatus.BLOCKED,
                    last_error=self._guardian_reason(guardian_decision),
                    finished_at=utc_now_iso(),
                )
                task_map[blocked.task_id] = blocked
                paused = self._workflow_with_tasks(working, task_map).with_status(
                    WorkflowStatus.PAUSED,
                    finished_at=utc_now_iso(),
                )
                result = self._task_result(blocked, warnings=self._guardian_warnings(guardian_decision), requires_review=True)
                task_results.append(result)
                self.last_workflow = paused
                return self._workflow_result(
                    paused,
                    task_results=tuple(task_results),
                    warnings=result.warnings,
                    errors=(f"guardian approval required: {blocked.last_error}",),
                    closure_recommendation="review",
                    requires_review=True,
                )

            if guardian_decision.decision == GuardianAction.BLOCK:
                failed = ready.with_status(
                    TaskStatus.FAILED,
                    last_error=self._guardian_reason(guardian_decision),
                    finished_at=utc_now_iso(),
                )
                task_map[failed.task_id] = failed
                task_result = self._task_result(failed, errors=(f"guardian blocked task: {failed.last_error}",))
                task_results.append(task_result)
                failed_tasks.add(failed.task_id)
                if self._task_required(failed):
                    failed_required.add(failed.task_id)
                    final = self._workflow_with_tasks(working, task_map).with_status(
                        WorkflowStatus.FAILED,
                        finished_at=utc_now_iso(),
                    )
                    self.last_workflow = final
                    return self._workflow_result(
                        final,
                        task_results=tuple(task_results),
                        errors=task_result.errors,
                        closure_recommendation="fail",
                    )
                continue

            runtime_result = self._execute_task(working, ready)
            completed_task = self._task_from_runtime(ready, runtime_result)
            task_map[completed_task.task_id] = completed_task
            task_result = self._task_result_from_runtime(completed_task, runtime_result, guardian_decision)
            task_results.append(task_result)
            self._log(working, f"task finished task_id={completed_task.task_id} status={completed_task.status.value}")

            if completed_task.status == TaskStatus.FAILED and self._task_required(completed_task):
                failed_tasks.add(completed_task.task_id)
                failed_required.add(completed_task.task_id)
                final = self._workflow_with_tasks(working, task_map).with_status(
                    WorkflowStatus.FAILED,
                    finished_at=utc_now_iso(),
                )
                self.last_workflow = final
                return self._workflow_result(
                    final,
                    task_results=tuple(task_results),
                    errors=task_result.errors or (completed_task.last_error or "required task failed",),
                    closure_recommendation="fail",
                )
            if completed_task.status == TaskStatus.FAILED:
                failed_tasks.add(completed_task.task_id)

        final_status = WorkflowStatus.FAILED if failed_required else WorkflowStatus.DONE
        recommendation = "fail" if failed_required else "conclude"
        final_workflow = self._workflow_with_tasks(working, task_map).with_status(final_status, finished_at=utc_now_iso())
        self.last_workflow = final_workflow
        self._log(final_workflow, f"workflow finished status={final_status.value}")
        return self._workflow_result(
            final_workflow,
            task_results=tuple(task_results),
            closure_recommendation=recommendation,
        )

    def _evaluate_task(self, workflow: Workflow, task: WorkflowTask) -> GuardianDecision:
        context = GuardianEvaluationContext(
            mission_id=workflow.mission_id,
            evaluation_type="workflow_task_pre_execution",
            evaluation_id=f"{workflow.workflow_id}:{task.task_id}",
            guardian_mode=self.guardian_mode,
            mission_goal=workflow.goal,
            spec_refs=workflow.spec_refs,
            guardian_refs=workflow.guardian_refs,
            workspace=self.workspace,
            requested_action=f"{task.title}\n{task.goal}",
            planned_command=self._planned_command(task),
            target_paths=self._target_paths(task),
            budget_policy=dict(workflow.budget_policy),
            execution_limits={**workflow.execution_limits, **task.execution_limits},
            metadata={
                "workflow_id": workflow.workflow_id,
                "task_id": task.task_id,
                "task_type": task.task_type,
                "risk_level": task.risk_level,
                "acceptance_criteria": task.acceptance_criteria,
                "required": self._task_required(task),
            },
        )
        decision = self.guardian.evaluate(context)
        self._log(workflow, f"guardian decision={decision.decision.value} task_id={task.task_id}")
        return decision

    def _execute_task(self, workflow: Workflow, task: WorkflowTask) -> RuntimeExecutionResult:
        running = task.with_status(TaskStatus.RUNNING, started_at=utc_now_iso(), attempt_count=task.attempt_count + 1)
        request = RuntimeExecutionRequest(
            mission_id=workflow.mission_id,
            workspace=self.workspace,
            workflow_id=workflow.workflow_id,
            task_id=running.task_id,
            context={
                "workflow_title": workflow.title,
                "workflow_goal": workflow.goal,
                "task_title": running.title,
                "task_goal": running.goal,
                "task_type": running.task_type,
                "inputs": running.inputs,
                "expected_outputs": running.expected_outputs,
                "acceptance_criteria": running.acceptance_criteria,
                "model_policy": running.model_policy,
            },
            execution_limits=dict(running.execution_limits),
            logging_policy={"sanitize_secrets": True},
            approval_policy=dict(running.validation_policy),
        )
        self._log(workflow, f"task started task_id={running.task_id}")
        return self.runtime.execute_task(request)

    def _ordered_tasks(self, workflow: Workflow) -> tuple[WorkflowTask, ...]:
        ordered: list[WorkflowTask] = []
        remaining = {task.task_id: task for task in workflow.tasks}
        completed: set[str] = set()

        while remaining:
            ready = [
                task
                for task in remaining.values()
                if all(
                    not dependency.required
                    or dependency.target_ref in completed
                    or dependency.target_ref not in remaining
                    for dependency in task.dependencies
                )
            ]
            if not ready:
                raise WorkflowEngineError("cyclic task dependency detected")
            ready.sort(key=lambda task: (task.priority, task.created_at, task.task_id))
            task = ready[0]
            ordered.append(task)
            completed.add(task.task_id)
            del remaining[task.task_id]
        return tuple(ordered)

    def _dependency_error(self, workflow: Workflow) -> str | None:
        task_ids = {task.task_id for task in workflow.tasks}
        for task in workflow.tasks:
            for dependency in task.dependencies:
                if dependency.required and dependency.target_ref not in task_ids:
                    return f"unresolvable dependency: task {task.task_id} requires {dependency.target_ref}"
        try:
            self._ordered_tasks(workflow)
        except WorkflowEngineError as exc:
            return str(exc)
        return None

    def _failed_dependencies(self, task: WorkflowTask, failed_tasks: set[str]) -> tuple[str, ...]:
        return tuple(
            dependency.target_ref
            for dependency in task.dependencies
            if dependency.required and dependency.target_ref in failed_tasks
        )

    def _task_from_runtime(self, task: WorkflowTask, result: RuntimeExecutionResult) -> WorkflowTask:
        if result.status == RuntimeStatus.DONE:
            return task.with_status(
                TaskStatus.DONE,
                artifacts=tuple(dict.fromkeys((*task.artifacts, *result.artifacts, *result.changed_files))),
                finished_at=utc_now_iso(),
                last_error=None,
                audit_log_ref=result.audit_log_ref,
            )
        return task.with_status(
            TaskStatus.FAILED,
            finished_at=utc_now_iso(),
            last_error=self._runtime_error(result),
            audit_log_ref=result.audit_log_ref,
        )

    def _task_result_from_runtime(
        self,
        task: WorkflowTask,
        runtime_result: RuntimeExecutionResult,
        guardian_decision: GuardianDecision,
    ) -> TaskResult:
        warnings = (*self._guardian_warnings(guardian_decision), *runtime_result.warnings)
        return self._task_result(
            task,
            summary=f"runtime status={runtime_result.status.value}",
            artifacts=tuple(dict.fromkeys((*runtime_result.artifacts, *runtime_result.changed_files))),
            validation_results=runtime_result.validation_results,
            warnings=warnings,
            errors=runtime_result.errors if task.status == TaskStatus.FAILED else (),
            requires_review=runtime_result.requires_review,
            audit_log_ref=runtime_result.audit_log_ref,
        )

    def _task_result(
        self,
        task: WorkflowTask,
        *,
        summary: str = "",
        artifacts: tuple[str, ...] = (),
        validation_results: tuple[str, ...] = (),
        warnings: tuple[str, ...] = (),
        errors: tuple[str, ...] = (),
        requires_review: bool = False,
        audit_log_ref: str | None = None,
    ) -> TaskResult:
        return TaskResult(
            task_id=task.task_id,
            workflow_id=task.workflow_id,
            mission_id=task.mission_id,
            status=task.status,
            summary=summary,
            artifacts=artifacts or task.artifacts,
            validation_results=validation_results,
            warnings=warnings,
            errors=errors,
            requires_review=requires_review,
            audit_log_ref=audit_log_ref or task.audit_log_ref,
        )

    def _workflow_result(
        self,
        workflow: Workflow,
        *,
        task_results: tuple[TaskResult, ...] = (),
        warnings: tuple[str, ...] = (),
        errors: tuple[str, ...] = (),
        closure_recommendation: str = "review",
        requires_review: bool = False,
    ) -> WorkflowResult:
        return WorkflowResult(
            workflow_id=workflow.workflow_id,
            mission_id=workflow.mission_id,
            status=workflow.status,
            summary=f"workflow status={workflow.status.value}",
            task_results=task_results,
            artifacts=tuple(dict.fromkeys(artifact for result in task_results for artifact in result.artifacts)),
            validation_results=tuple(
                validation for result in task_results for validation in result.validation_results
            ),
            warnings=warnings or tuple(warning for result in task_results for warning in result.warnings),
            errors=errors or tuple(error for result in task_results for error in result.errors),
            closure_recommendation=closure_recommendation,
            requires_review=requires_review,
            audit_log_ref=f"memory://workflow/{workflow.workflow_id}",
        )

    def _workflow_with_tasks(self, workflow: Workflow, task_map: dict[str, WorkflowTask]) -> Workflow:
        return replace(workflow, tasks=tuple(task_map[task.task_id] for task in workflow.tasks))

    def _task_required(self, task: WorkflowTask) -> bool:
        return bool(task.validation_policy.get("required", True))

    def _planned_command(self, task: WorkflowTask) -> str | None:
        value = task.inputs.get("planned_command")
        if value is None:
            return None
        return str(value)

    def _target_paths(self, task: WorkflowTask) -> tuple[str, ...]:
        target_paths = task.inputs.get("target_paths", ())
        if isinstance(target_paths, str):
            target_paths = (target_paths,)
        return tuple(str(path) for path in (*target_paths, *task.expected_outputs, *task.artifacts))

    def _runtime_error(self, result: RuntimeExecutionResult) -> str:
        if result.errors:
            return "; ".join(result.errors)
        return f"runtime returned status={result.status.value}"

    def _guardian_reason(self, decision: GuardianDecision) -> str:
        if decision.reasons:
            return "; ".join(decision.reasons)
        if decision.blocked_items:
            return "; ".join(decision.blocked_items)
        return decision.decision.value

    def _guardian_warnings(self, decision: GuardianDecision) -> tuple[str, ...]:
        if decision.decision == GuardianAction.WARN:
            return decision.warnings or decision.reasons
        return ()

    def _log(self, workflow: Workflow, message: str) -> None:
        self.audit_log.append(f"workflow={workflow.workflow_id} mission={workflow.mission_id} {message}")


__all__ = ["GuardianEvaluator", "WorkflowEngine", "WorkflowEngineError"]
