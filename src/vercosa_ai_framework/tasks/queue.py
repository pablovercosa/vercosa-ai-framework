"""In-memory Task Queue contracts for Workflow Engine orchestration."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from uuid import uuid4

from vercosa_ai_framework.tasks.types import (
    Task,
    TaskAttempt,
    TaskQueueResult,
    TaskQueueState,
    utc_now_iso,
)


class TaskQueueError(RuntimeError):
    """Raised when a Task Queue operation would violate the queue contract."""


class TaskQueue:
    """Deterministic internal queue for workflow tasks.

    The queue only tracks operational state and eligibility. It deliberately does
    not call RuntimeAdapter, OpenCode, agents, tools, APIs, or external services.
    """

    TERMINAL_STATES = {
        TaskQueueState.DONE,
        TaskQueueState.SKIPPED,
        TaskQueueState.CANCELLED,
    }

    def __init__(
        self,
        *,
        workflow_id: str,
        mission_id: str,
        queue_id: str | None = None,
        execution_mode: str = "sequential",
        max_parallel_tasks: int = 1,
    ) -> None:
        if max_parallel_tasks < 1:
            raise TaskQueueError("max_parallel_tasks must be at least 1")
        if execution_mode != "sequential" or max_parallel_tasks != 1:
            raise TaskQueueError("only sequential task queue execution is currently supported")

        self.queue_id = queue_id or str(uuid4())
        self.workflow_id = workflow_id
        self.mission_id = mission_id
        self.execution_mode = execution_mode
        self.max_parallel_tasks = max_parallel_tasks
        self.created_at = utc_now_iso()
        self.updated_at = self.created_at
        self._tasks: dict[str, Task] = {}
        self._attempts: dict[str, tuple[TaskAttempt, ...]] = {}

    def add_task(self, task: Task) -> TaskQueueResult:
        """Add a planned task to the queue without dispatching it."""

        if task.workflow_id != self.workflow_id:
            raise TaskQueueError("task workflow_id does not match queue workflow_id")
        if task.mission_id != self.mission_id:
            raise TaskQueueError("task mission_id does not match queue mission_id")
        if task.task_id in self._tasks:
            raise TaskQueueError(f"task already queued: {task.task_id}")
        if task.max_attempts < 1:
            raise TaskQueueError("task max_attempts must be at least 1")

        queued = task.with_state(TaskQueueState.QUEUED, blocked_by=())
        self._tasks[queued.task_id] = queued
        self._attempts[queued.task_id] = ()
        self.updated_at = utc_now_iso()
        return self._result(True, task=queued, message="task queued")

    def list_by_state(self, state: TaskQueueState | str) -> tuple[Task, ...]:
        """Return tasks in a state using deterministic queue ordering."""

        queue_state = TaskQueueState(state)
        return tuple(task for task in self._ordered_tasks() if task.state == queue_state)

    def list_tasks(self) -> tuple[Task, ...]:
        """Return all tasks using deterministic queue ordering."""

        return tuple(self._ordered_tasks())

    def attempts_for(self, task_id: str) -> tuple[TaskAttempt, ...]:
        """Return preserved attempts for a task."""

        self._require_task(task_id)
        return self._attempts[task_id]

    def next_executable(self, *, now: str | None = None) -> Task | None:
        """Return the next eligible queued task without executing it."""

        if self.list_by_state(TaskQueueState.RUNNING):
            return None

        for task in self._ordered_tasks():
            if task.state != TaskQueueState.QUEUED:
                continue
            if not self._dependencies_satisfied(task):
                continue
            if not self._attempt_due(task, now):
                continue
            return task
        return None

    def start_next_attempt(self, *, now: str | None = None) -> TaskQueueResult:
        """Mark the next eligible task as running and create a local attempt."""

        task = self.next_executable(now=now)
        if task is None:
            return self._result(False, message="no executable task")
        return self.start_attempt(task.task_id)

    def start_attempt(self, task_id: str) -> TaskQueueResult:
        """Mark a queued task as running and record a traceable attempt."""

        task = self._require_task(task_id)
        if task.state != TaskQueueState.QUEUED:
            raise TaskQueueError(f"task is not queued: {task_id}")
        if self.list_by_state(TaskQueueState.RUNNING):
            raise TaskQueueError("sequential queue already has a running task")
        if not self._dependencies_satisfied(task):
            raise TaskQueueError(f"task dependencies are not satisfied: {task_id}")
        if task.attempt_count >= task.max_attempts:
            raise TaskQueueError(f"task attempt limit exceeded: {task_id}")

        attempt = TaskAttempt(
            task_id=task.task_id,
            workflow_id=task.workflow_id,
            mission_id=task.mission_id,
            attempt_number=task.attempt_count + 1,
        )
        running = task.with_state(
            TaskQueueState.RUNNING,
            attempt_count=attempt.attempt_number,
            started_at=attempt.started_at,
            blocked_by=(),
        )
        self._tasks[task_id] = running
        self._attempts[task_id] = (*self._attempts[task_id], attempt)
        self.updated_at = utc_now_iso()
        return self._result(True, task=running, attempt=attempt, message="attempt started")

    def complete_task(self, task_id: str, *, artifact_refs: tuple[str, ...] = ()) -> TaskQueueResult:
        """Mark a running task as done without invoking any runtime."""

        task = self._require_running(task_id)
        finished_at = utc_now_iso()
        done = task.with_state(TaskQueueState.DONE, finished_at=finished_at, artifact_refs=artifact_refs)
        self._tasks[task_id] = done
        self._finish_latest_attempt(task_id, TaskQueueState.DONE, finished_at=finished_at)
        self.updated_at = utc_now_iso()
        return self._result(True, task=done, attempt=self._attempts[task_id][-1], message="task done")

    def fail_task(self, task_id: str, *, error_message: str = "") -> TaskQueueResult:
        """Mark a running task as failed without retrying automatically."""

        task = self._require_running(task_id)
        finished_at = utc_now_iso()
        failed = task.with_state(TaskQueueState.FAILED, finished_at=finished_at, last_error=error_message or None)
        self._tasks[task_id] = failed
        self._finish_latest_attempt(
            task_id,
            TaskQueueState.FAILED,
            finished_at=finished_at,
            error_message=error_message or None,
        )
        self.updated_at = utc_now_iso()
        return self._result(False, task=failed, attempt=self._attempts[task_id][-1], errors=(error_message,) if error_message else ())

    def requeue_failed(self, task_id: str, *, next_attempt_at: str | None = None) -> TaskQueueResult:
        """Requeue a failed task when finite retry budget remains."""

        task = self._require_task(task_id)
        if task.state != TaskQueueState.FAILED:
            raise TaskQueueError(f"task is not failed: {task_id}")
        if task.attempt_count >= task.max_attempts:
            raise TaskQueueError(f"task attempt limit exceeded: {task_id}")

        queued = task.with_state(
            TaskQueueState.QUEUED,
            next_attempt_at=next_attempt_at,
            finished_at=None,
            last_error=None,
        )
        self._tasks[task_id] = queued
        self.updated_at = utc_now_iso()
        return self._result(True, task=queued, message="task requeued")

    def block_task(self, task_id: str, *, reason: str, blocked_by: tuple[str, ...] = ()) -> TaskQueueResult:
        """Block a queued or running task with an auditable reason."""

        task = self._require_task(task_id)
        if task.state not in {TaskQueueState.QUEUED, TaskQueueState.RUNNING, TaskQueueState.FAILED}:
            raise TaskQueueError(f"task cannot be blocked from state {task.state.value}: {task_id}")
        blocked = task.with_state(TaskQueueState.BLOCKED, blocked_by=blocked_by, last_error=reason)
        self._tasks[task_id] = blocked
        self.updated_at = utc_now_iso()
        return self._result(False, task=blocked, message="task blocked", warnings=(reason,))

    def unblock_task(self, task_id: str) -> TaskQueueResult:
        """Move a blocked task back to queued when its blocker is resolved."""

        task = self._require_task(task_id)
        if task.state != TaskQueueState.BLOCKED:
            raise TaskQueueError(f"task is not blocked: {task_id}")
        queued = task.with_state(TaskQueueState.QUEUED, blocked_by=(), last_error=None)
        self._tasks[task_id] = queued
        self.updated_at = utc_now_iso()
        return self._result(True, task=queued, message="task unblocked")

    def _ordered_tasks(self) -> list[Task]:
        return sorted(
            self._tasks.values(),
            key=lambda task: (
                int(task.priority),
                self._dependency_depth(task.task_id, seen=()),
                task.created_at,
                task.task_id,
            ),
        )

    def _dependency_depth(self, task_id: str, *, seen: tuple[str, ...]) -> int:
        if task_id in seen:
            return 0
        task = self._tasks.get(task_id)
        if task is None or not task.dependencies:
            return 0
        return 1 + max(
            (self._dependency_depth(dependency, seen=(*seen, task_id)) for dependency in task.dependencies),
            default=0,
        )

    def _dependencies_satisfied(self, task: Task) -> bool:
        return all(
            dependency in self._tasks and self._tasks[dependency].state == TaskQueueState.DONE
            for dependency in task.dependencies
        )

    def _attempt_due(self, task: Task, now: str | None) -> bool:
        if task.next_attempt_at is None:
            return True
        current = _parse_iso(now or utc_now_iso())
        due_at = _parse_iso(task.next_attempt_at)
        return current >= due_at

    def _require_task(self, task_id: str) -> Task:
        try:
            return self._tasks[task_id]
        except KeyError as exc:
            raise TaskQueueError(f"unknown task: {task_id}") from exc

    def _require_running(self, task_id: str) -> Task:
        task = self._require_task(task_id)
        if task.state != TaskQueueState.RUNNING:
            raise TaskQueueError(f"task is not running: {task_id}")
        return task

    def _finish_latest_attempt(
        self,
        task_id: str,
        state: TaskQueueState,
        *,
        finished_at: str,
        error_message: str | None = None,
    ) -> None:
        attempts = self._attempts[task_id]
        if not attempts:
            raise TaskQueueError(f"task has no active attempt: {task_id}")
        latest = attempts[-1].with_state(state, finished_at=finished_at, error_message=error_message)
        self._attempts[task_id] = (*attempts[:-1], latest)

    def _result(
        self,
        success: bool,
        *,
        task: Task | None = None,
        attempt: TaskAttempt | None = None,
        message: str = "",
        warnings: tuple[str, ...] = (),
        errors: tuple[str, ...] = (),
    ) -> TaskQueueResult:
        return TaskQueueResult(
            queue_id=self.queue_id,
            workflow_id=self.workflow_id,
            mission_id=self.mission_id,
            success=success,
            task=task,
            attempt=attempt,
            message=message,
            warnings=warnings,
            errors=errors,
        )


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
