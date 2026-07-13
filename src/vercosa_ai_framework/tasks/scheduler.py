"""Deterministic in-memory scheduler for the Task Queue MVP."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from vercosa_ai_framework.tasks.queue import TaskQueue, TaskQueueError
from vercosa_ai_framework.tasks.types import Task, TaskAttempt, TaskQueueState


@dataclass(frozen=True, slots=True)
class TaskExecutionOutcome:
    """Normalized outcome returned by a testable task executor."""

    status: TaskQueueState = TaskQueueState.DONE
    artifact_refs: tuple[str, ...] = field(default_factory=tuple)
    error_message: str = ""
    retryable: bool = True
    next_attempt_at: str | None = None
    agent_assignment_ref: str | None = None
    runtime_result_ref: str | None = None
    audit_log_ref: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)


TaskExecutor = Callable[[Task, TaskAttempt], TaskExecutionOutcome]


@dataclass(frozen=True, slots=True)
class TaskSchedulerResult:
    """Summary of one deterministic scheduler drain cycle."""

    queue_id: str
    workflow_id: str
    mission_id: str
    status: str
    executed_task_ids: tuple[str, ...] = field(default_factory=tuple)
    done_task_ids: tuple[str, ...] = field(default_factory=tuple)
    failed_task_ids: tuple[str, ...] = field(default_factory=tuple)
    blocked_task_ids: tuple[str, ...] = field(default_factory=tuple)
    skipped_task_ids: tuple[str, ...] = field(default_factory=tuple)
    cancelled_task_ids: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)


class TaskScheduler:
    """Run queued tasks sequentially through an injected in-memory executor.

    The scheduler is deliberately runtime agnostic. It only advances Task Queue
    state and never invokes OpenCode, subprocesses, global config, sudo, tools,
    providers, or operating-system specific behavior.
    """

    def run_until_idle(
        self,
        queue: TaskQueue,
        executor: TaskExecutor,
        *,
        now: str | None = None,
        max_steps: int | None = None,
    ) -> TaskSchedulerResult:
        """Drain eligible tasks until no deterministic progress remains."""

        if max_steps is not None and max_steps < 1:
            raise TaskQueueError("max_steps must be at least 1")

        executed_task_ids: list[str] = []
        errors: list[str] = []
        steps = 0

        while max_steps is None or steps < max_steps:
            queue.block_tasks_with_failed_dependencies()
            started = queue.start_next_attempt(now=now)
            if not started.success or started.task is None or started.attempt is None:
                break

            steps += 1
            task = started.task
            attempt = started.attempt
            executed_task_ids.append(task.task_id)

            try:
                outcome = executor(task, attempt)
            except Exception as exc:  # pragma: no cover - defensive boundary normalization
                outcome = TaskExecutionOutcome(status=TaskQueueState.FAILED, error_message=str(exc), retryable=False)

            self._apply_outcome(queue, task.task_id, outcome, errors)

        queue.block_tasks_with_failed_dependencies()
        tasks = queue.list_tasks()
        failed = tuple(task.task_id for task in tasks if task.state == TaskQueueState.FAILED)
        blocked = tuple(task.task_id for task in tasks if task.state == TaskQueueState.BLOCKED)
        skipped = tuple(task.task_id for task in tasks if task.state == TaskQueueState.SKIPPED)
        cancelled = tuple(task.task_id for task in tasks if task.state == TaskQueueState.CANCELLED)
        done = tuple(task.task_id for task in tasks if task.state == TaskQueueState.DONE)

        return TaskSchedulerResult(
            queue_id=queue.queue_id,
            workflow_id=queue.workflow_id,
            mission_id=queue.mission_id,
            status=self._status(queue),
            executed_task_ids=tuple(executed_task_ids),
            done_task_ids=done,
            failed_task_ids=failed,
            blocked_task_ids=blocked,
            skipped_task_ids=skipped,
            cancelled_task_ids=cancelled,
            errors=tuple(errors),
        )

    def _apply_outcome(
        self,
        queue: TaskQueue,
        task_id: str,
        outcome: TaskExecutionOutcome,
        errors: list[str],
    ) -> None:
        status = TaskQueueState(outcome.status)
        if status == TaskQueueState.DONE:
            queue.complete_task(
                task_id,
                artifact_refs=outcome.artifact_refs,
                agent_assignment_ref=outcome.agent_assignment_ref,
                runtime_result_ref=outcome.runtime_result_ref,
                audit_log_ref=outcome.audit_log_ref,
                metadata=outcome.metadata,
            )
            return
        if status == TaskQueueState.FAILED:
            queue.fail_task(
                task_id,
                error_message=outcome.error_message,
                agent_assignment_ref=outcome.agent_assignment_ref,
                runtime_result_ref=outcome.runtime_result_ref,
                audit_log_ref=outcome.audit_log_ref,
                metadata=outcome.metadata,
            )
            if outcome.retryable and queue.retry_remaining(task_id):
                queue.requeue_failed(task_id, next_attempt_at=outcome.next_attempt_at)
            else:
                errors.append(outcome.error_message or f"task failed: {task_id}")
            return
        if status == TaskQueueState.BLOCKED:
            queue.block_task(task_id, reason=outcome.error_message or "blocked by scheduler outcome")
            return
        if status == TaskQueueState.SKIPPED:
            queue.skip_task(task_id, reason=outcome.error_message or "skipped by scheduler outcome")
            return
        if status == TaskQueueState.CANCELLED:
            queue.cancel_task(task_id, reason=outcome.error_message or "cancelled by scheduler outcome")
            return
        raise TaskQueueError(f"unsupported scheduler outcome status: {status.value}")

    def _status(self, queue: TaskQueue) -> str:
        tasks = queue.list_tasks()
        if any(task.state == TaskQueueState.RUNNING for task in tasks):
            return "running"
        if any(task.state == TaskQueueState.FAILED for task in tasks):
            return "failed"
        if any(task.state == TaskQueueState.BLOCKED for task in tasks):
            return "blocked"
        if any(task.state == TaskQueueState.QUEUED for task in tasks):
            return "idle"
        return "done"


__all__ = ["TaskExecutionOutcome", "TaskExecutor", "TaskScheduler", "TaskSchedulerResult"]
