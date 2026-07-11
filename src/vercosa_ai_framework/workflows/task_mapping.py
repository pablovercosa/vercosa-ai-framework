"""Explicit WorkflowTask to Task Queue mapping utilities."""

from __future__ import annotations

from dataclasses import replace

from vercosa_ai_framework.tasks import Task, TaskQueueState
from vercosa_ai_framework.workflows.types import TaskResult, TaskStatus, WorkflowTask


class WorkflowTaskMappingError(ValueError):
    """Raised when a workflow task cannot be materialized safely."""


WORKFLOW_TO_QUEUE_STATE: dict[TaskStatus, TaskQueueState] = {
    TaskStatus.PENDING: TaskQueueState.QUEUED,
    TaskStatus.READY: TaskQueueState.QUEUED,
    TaskStatus.RUNNING: TaskQueueState.RUNNING,
    TaskStatus.BLOCKED: TaskQueueState.BLOCKED,
    TaskStatus.VALIDATING: TaskQueueState.RUNNING,
    TaskStatus.DONE: TaskQueueState.DONE,
    TaskStatus.FAILED: TaskQueueState.FAILED,
    TaskStatus.SKIPPED: TaskQueueState.SKIPPED,
    TaskStatus.CANCELLED: TaskQueueState.CANCELLED,
}

QUEUE_TO_WORKFLOW_STATUS: dict[TaskQueueState, TaskStatus] = {
    TaskQueueState.QUEUED: TaskStatus.READY,
    TaskQueueState.RUNNING: TaskStatus.RUNNING,
    TaskQueueState.DONE: TaskStatus.DONE,
    TaskQueueState.FAILED: TaskStatus.FAILED,
    TaskQueueState.BLOCKED: TaskStatus.BLOCKED,
    TaskQueueState.SKIPPED: TaskStatus.SKIPPED,
    TaskQueueState.CANCELLED: TaskStatus.CANCELLED,
}


def workflow_task_to_task(workflow_task: WorkflowTask) -> Task:
    """Materialize a WorkflowTask as an operational Task without mutation."""

    if not workflow_task.task_id:
        raise WorkflowTaskMappingError("workflow task requires task_id")
    if not workflow_task.workflow_id:
        raise WorkflowTaskMappingError(f"workflow task requires workflow_id: {workflow_task.task_id}")
    if not workflow_task.mission_id:
        raise WorkflowTaskMappingError(f"workflow task requires mission_id: {workflow_task.task_id}")

    max_attempts = _max_attempts(workflow_task)
    required_dependencies = tuple(
        dependency.target_ref for dependency in workflow_task.dependencies if dependency.required
    )
    optional_dependencies = tuple(
        dependency.target_ref for dependency in workflow_task.dependencies if not dependency.required
    )
    state = WORKFLOW_TO_QUEUE_STATE[TaskStatus(workflow_task.status)]
    warnings = ()
    if workflow_task.status == TaskStatus.VALIDATING:
        warnings = ("workflow status validating mapped to queue state running",)

    return Task(
        task_id=workflow_task.task_id,
        title=workflow_task.title,
        goal=workflow_task.goal,
        workflow_id=workflow_task.workflow_id,
        mission_id=workflow_task.mission_id,
        state=state,
        priority=workflow_task.priority,
        dependencies=required_dependencies,
        blocked_by=workflow_task.blocked_by,
        task_type=workflow_task.task_type,
        risk_level=workflow_task.risk_level,
        required_capabilities=workflow_task.required_capabilities,
        artifact_refs=workflow_task.artifacts,
        attempt_count=workflow_task.attempt_count,
        max_attempts=max_attempts,
        last_error=workflow_task.last_error,
        metadata={
            "workflow_task_status": workflow_task.status.value,
            "inputs": dict(workflow_task.inputs),
            "expected_outputs": workflow_task.expected_outputs,
            "acceptance_criteria": workflow_task.acceptance_criteria,
            "optional_dependencies": optional_dependencies,
            "dependency_details": tuple(
                {
                    "dependency_type": dependency.dependency_type,
                    "target_ref": dependency.target_ref,
                    "reason": dependency.reason,
                    "required": dependency.required,
                    "metadata": dict(dependency.metadata),
                }
                for dependency in workflow_task.dependencies
            ),
            "model_policy": dict(workflow_task.model_policy),
            "execution_limits": dict(workflow_task.execution_limits),
            "retry_policy": dict(workflow_task.retry_policy),
            "validation_policy": dict(workflow_task.validation_policy),
            "assigned_agent_ref": workflow_task.assigned_agent_ref,
            "audit_log_ref": workflow_task.audit_log_ref,
            "mapping_warnings": warnings,
        },
        created_at=workflow_task.created_at,
        started_at=workflow_task.started_at,
        finished_at=workflow_task.finished_at,
        audit_log_ref=workflow_task.audit_log_ref,
    )


def task_to_workflow_task(task: Task, source: WorkflowTask) -> WorkflowTask:
    """Map an operational Task back into a WorkflowTask copy."""

    return replace(
        source,
        status=QUEUE_TO_WORKFLOW_STATUS[TaskQueueState(task.state)],
        blocked_by=task.blocked_by,
        artifacts=tuple(dict.fromkeys((*source.artifacts, *task.artifact_refs))),
        attempt_count=task.attempt_count,
        last_error=task.last_error,
        started_at=task.started_at or source.started_at,
        finished_at=task.finished_at or source.finished_at,
        audit_log_ref=task.audit_log_ref or source.audit_log_ref,
    )


def task_result_from_task(task: Task, source: WorkflowTask, *, errors: tuple[str, ...] = ()) -> TaskResult:
    """Create a Workflow TaskResult from final queue state."""

    status = QUEUE_TO_WORKFLOW_STATUS[TaskQueueState(task.state)]
    task_errors = errors
    if not task_errors and status in {TaskStatus.FAILED, TaskStatus.BLOCKED, TaskStatus.CANCELLED} and task.last_error:
        task_errors = (task.last_error,)
    return TaskResult(
        task_id=task.task_id,
        workflow_id=task.workflow_id,
        mission_id=task.mission_id,
        status=status,
        summary=f"queue state={task.state.value} attempts={task.attempt_count}",
        artifacts=tuple(dict.fromkeys((*source.artifacts, *task.artifact_refs))),
        errors=task_errors,
        requires_review=status == TaskStatus.BLOCKED,
        audit_log_ref=task.audit_log_ref or source.audit_log_ref,
    )


def _max_attempts(workflow_task: WorkflowTask) -> int:
    raw_value = workflow_task.retry_policy.get("max_attempts", 1)
    try:
        max_attempts = int(raw_value)
    except (TypeError, ValueError) as exc:
        raise WorkflowTaskMappingError(
            f"invalid max_attempts for workflow task {workflow_task.task_id}: {raw_value!r}"
        ) from exc
    if max_attempts < 1:
        raise WorkflowTaskMappingError(
            f"max_attempts must be at least 1 for workflow task {workflow_task.task_id}"
        )
    return max_attempts


__all__ = [
    "QUEUE_TO_WORKFLOW_STATUS",
    "WORKFLOW_TO_QUEUE_STATE",
    "WorkflowTaskMappingError",
    "task_result_from_task",
    "task_to_workflow_task",
    "workflow_task_to_task",
]
