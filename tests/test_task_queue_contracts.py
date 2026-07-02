from __future__ import annotations

from dataclasses import asdict

import pytest

from vercosa_ai_framework.tasks import (
    Task,
    TaskAttempt,
    TaskPriority,
    TaskQueue,
    TaskQueueError,
    TaskQueueResult,
    TaskQueueState,
)


def task(
    task_id: str,
    *,
    priority: int = int(TaskPriority.NORMAL),
    dependencies: tuple[str, ...] = (),
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
        created_at=timestamp,
        queued_at=timestamp,
        updated_at=timestamp,
    )


def test_task_queue_states_match_spec_0007():
    assert {state.value for state in TaskQueueState} == {
        "queued",
        "running",
        "done",
        "failed",
        "blocked",
        "skipped",
        "cancelled",
    }


def test_task_contract_captures_traceability_priority_and_dependencies():
    queued_task = task(
        "task-impl",
        priority=int(TaskPriority.HIGH),
        dependencies=("task-plan",),
    )

    assert queued_task.state == TaskQueueState.QUEUED
    assert queued_task.priority == 50
    assert queued_task.dependencies == ("task-plan",)
    assert queued_task.max_attempts == 1
    assert asdict(queued_task)["workflow_id"] == "wf-1"


def test_queue_adds_and_lists_tasks_by_state_without_runtime_execution():
    queue = TaskQueue(workflow_id="wf-1", mission_id="mission-1")

    result = queue.add_task(task("task-a"))

    assert isinstance(result, TaskQueueResult)
    assert result.success is True
    assert [queued.task_id for queued in queue.list_by_state(TaskQueueState.QUEUED)] == ["task-a"]
    assert "opencode" not in asdict(result)


def test_next_executable_respects_required_dependencies_before_priority():
    queue = TaskQueue(workflow_id="wf-1", mission_id="mission-1")
    queue.add_task(task("task-b", priority=int(TaskPriority.CRITICAL), dependencies=("task-a",)))
    queue.add_task(task("task-a", priority=int(TaskPriority.NORMAL)))

    assert queue.next_executable().task_id == "task-a"

    started = queue.start_next_attempt()
    assert started.success is True
    assert isinstance(started.attempt, TaskAttempt)
    queue.complete_task("task-a")

    assert queue.next_executable().task_id == "task-b"


def test_queue_orders_eligible_tasks_deterministically():
    queue = TaskQueue(workflow_id="wf-1", mission_id="mission-1")
    queue.add_task(task("task-z", priority=int(TaskPriority.NORMAL)))
    queue.add_task(task("task-a", priority=int(TaskPriority.NORMAL)))
    queue.add_task(task("task-fast", priority=int(TaskPriority.HIGH)))

    assert [queued.task_id for queued in queue.list_by_state("queued")] == ["task-fast", "task-a", "task-z"]
    assert queue.next_executable().task_id == "task-fast"


def test_queue_does_not_select_task_while_another_is_running():
    queue = TaskQueue(workflow_id="wf-1", mission_id="mission-1")
    queue.add_task(task("task-a"))
    queue.add_task(task("task-b"))

    queue.start_next_attempt()

    assert queue.next_executable() is None


def test_retry_is_finite_and_preserves_attempts():
    queue = TaskQueue(workflow_id="wf-1", mission_id="mission-1")
    queue.add_task(task("task-a").with_state(TaskQueueState.QUEUED, max_attempts=2))

    first = queue.start_next_attempt()
    queue.fail_task("task-a", error_message="transient failure")
    queue.requeue_failed("task-a")
    second = queue.start_next_attempt()

    assert first.attempt.attempt_number == 1
    assert second.attempt.attempt_number == 2
    assert [attempt.attempt_number for attempt in queue.attempts_for("task-a")] == [1, 2]

    queue.fail_task("task-a", error_message="still failing")
    with pytest.raises(TaskQueueError, match="attempt limit exceeded"):
        queue.requeue_failed("task-a")


def test_queue_rejects_wrong_workflow_and_unsupported_parallelism():
    with pytest.raises(TaskQueueError, match="only sequential"):
        TaskQueue(workflow_id="wf-1", mission_id="mission-1", max_parallel_tasks=2)

    queue = TaskQueue(workflow_id="wf-1", mission_id="mission-1")
    wrong_workflow = Task(
        task_id="task-a",
        workflow_id="wf-other",
        mission_id="mission-1",
        title="Wrong workflow",
        goal="Must not be accepted",
    )

    with pytest.raises(TaskQueueError, match="workflow_id"):
        queue.add_task(wrong_workflow)
