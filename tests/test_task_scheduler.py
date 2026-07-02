from __future__ import annotations

from collections import defaultdict

from vercosa_ai_framework.tasks import (
    Task,
    TaskExecutionOutcome,
    TaskPriority,
    TaskQueue,
    TaskQueueState,
    TaskScheduler,
)


def task(
    task_id: str,
    *,
    priority: int = int(TaskPriority.NORMAL),
    dependencies: tuple[str, ...] = (),
    max_attempts: int = 1,
    created_at: str | None = None,
) -> Task:
    timestamp = created_at or "2026-07-02T00:00:00+00:00"
    return Task(
        task_id=task_id,
        workflow_id="wf-1",
        mission_id="mission-1",
        title=f"Task {task_id}",
        goal=f"Run {task_id}",
        priority=priority,
        dependencies=dependencies,
        max_attempts=max_attempts,
        created_at=timestamp,
        queued_at=timestamp,
        updated_at=timestamp,
    )


def queue_with(*tasks: Task) -> TaskQueue:
    queue = TaskQueue(workflow_id="wf-1", mission_id="mission-1")
    for queued_task in tasks:
        queue.add_task(queued_task)
    return queue


def test_scheduler_selects_by_dependency_priority_and_creation_order():
    queue = queue_with(
        task("task-b", priority=int(TaskPriority.CRITICAL), dependencies=("task-a",)),
        task("task-c", priority=int(TaskPriority.HIGH), created_at="2026-07-02T00:00:02+00:00"),
        task("task-a", priority=int(TaskPriority.NORMAL), created_at="2026-07-02T00:00:01+00:00"),
    )
    scheduler = TaskScheduler()

    result = scheduler.run_until_idle(queue, lambda _task, _attempt: TaskExecutionOutcome())

    assert result.status == "done"
    assert result.executed_task_ids == ("task-c", "task-a", "task-b")
    assert [queued.task_id for queued in queue.list_by_state(TaskQueueState.DONE)] == ["task-b", "task-c", "task-a"]


def test_scheduler_blocks_dependents_when_dependency_fails():
    queue = queue_with(task("task-a"), task("task-b", dependencies=("task-a",)))
    scheduler = TaskScheduler()

    result = scheduler.run_until_idle(
        queue,
        lambda _task, _attempt: TaskExecutionOutcome(
            status=TaskQueueState.FAILED,
            error_message="deterministic failure",
            retryable=False,
        ),
    )

    assert result.status == "failed"
    assert result.executed_task_ids == ("task-a",)
    assert result.failed_task_ids == ("task-a",)
    assert result.blocked_task_ids == ("task-b",)
    assert queue.list_by_state(TaskQueueState.BLOCKED)[0].blocked_by == ("task-a",)


def test_scheduler_retries_until_limit_then_continues_deterministically():
    queue = queue_with(task("task-a", max_attempts=2), task("task-b"))
    scheduler = TaskScheduler()
    calls: dict[str, int] = defaultdict(int)

    def executor(running: Task, _attempt: object) -> TaskExecutionOutcome:
        calls[running.task_id] += 1
        if running.task_id == "task-a" and calls[running.task_id] == 1:
            return TaskExecutionOutcome(status=TaskQueueState.FAILED, error_message="transient")
        return TaskExecutionOutcome()

    result = scheduler.run_until_idle(queue, executor)

    assert result.status == "done"
    assert result.executed_task_ids == ("task-a", "task-a", "task-b")
    assert [attempt.attempt_number for attempt in queue.attempts_for("task-a")] == [1, 2]
    assert queue.list_by_state(TaskQueueState.DONE)[0].task_id == "task-a"


def test_scheduler_marks_skipped_blocked_and_cancelled_without_runtime_side_effects():
    queue = queue_with(task("task-a"), task("task-b"), task("task-c"))
    scheduler = TaskScheduler()

    def executor(running: Task, _attempt: object) -> TaskExecutionOutcome:
        if running.task_id == "task-a":
            return TaskExecutionOutcome(status=TaskQueueState.SKIPPED, error_message="not needed")
        if running.task_id == "task-b":
            return TaskExecutionOutcome(status=TaskQueueState.BLOCKED, error_message="needs approval")
        return TaskExecutionOutcome(status=TaskQueueState.CANCELLED, error_message="workflow stopped")

    result = scheduler.run_until_idle(queue, executor)

    assert result.status == "blocked"
    assert result.skipped_task_ids == ("task-a",)
    assert result.blocked_task_ids == ("task-b",)
    assert result.cancelled_task_ids == ("task-c",)
