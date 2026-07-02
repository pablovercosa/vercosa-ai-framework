from vercosa_ai_framework.missions import (
    DirectoryMissionQueue,
    Mission,
    MissionQueueError,
    MissionStatus,
)

import pytest


def test_directory_mission_queue_persists_and_orders_missions(tmp_path):
    queue = DirectoryMissionQueue(tmp_path)
    later = queue.enqueue(Mission(title="Later", goal="Run later", priority=20))
    first = queue.enqueue(Mission(title="First", goal="Run first", priority=10))

    assert queue.get(first.mission_id).status == MissionStatus.QUEUED
    assert [mission.mission_id for mission in queue.list(MissionStatus.QUEUED)] == [
        first.mission_id,
        later.mission_id,
    ]
    assert queue.next().mission_id == first.mission_id


def test_directory_mission_queue_controls_lifecycle(tmp_path):
    queue = DirectoryMissionQueue(tmp_path)
    mission = queue.enqueue(Mission(title="Implement", goal="Create contracts"))

    running = queue.start(mission.mission_id, locked_by="test-runner")
    done = queue.complete(mission.mission_id)

    assert running.status == MissionStatus.RUNNING
    assert running.locked_by == "test-runner"
    assert running.attempt_count == 1
    assert done.status == MissionStatus.DONE
    assert done.locked_by is None
    assert done.finished_at is not None


def test_directory_mission_queue_rejects_invalid_transition(tmp_path):
    queue = DirectoryMissionQueue(tmp_path)
    mission = queue.enqueue(Mission(title="Invalid", goal="Invalid transition"))

    with pytest.raises(MissionQueueError, match="expected one of"):
        queue.complete(mission.mission_id)


def test_directory_mission_queue_can_fail_cancel_and_requeue(tmp_path):
    queue = DirectoryMissionQueue(tmp_path)
    failed_source = queue.enqueue(
        Mission(title="Retry", goal="Retry failed mission", max_attempts=2)
    )
    queue.start(failed_source.mission_id)
    failed = queue.fail(failed_source.mission_id, "validation failed")
    requeued = queue.requeue(failed_source.mission_id)

    cancellable = queue.enqueue(Mission(title="Cancel", goal="Cancel safely"))
    cancelled = queue.cancel(cancellable.mission_id, "user cancelled")

    assert failed.status == MissionStatus.FAILED
    assert failed.last_error == "validation failed"
    assert requeued.status == MissionStatus.QUEUED
    assert requeued.last_error is None
    assert cancelled.status == MissionStatus.CANCELLED
    assert cancelled.last_error == "user cancelled"


def test_directory_mission_queue_blocks_retry_after_limit(tmp_path):
    queue = DirectoryMissionQueue(tmp_path)
    mission = queue.enqueue(Mission(title="No retry", goal="Fail once", max_attempts=1))
    queue.start(mission.mission_id)
    queue.fail(mission.mission_id, "failed")

    with pytest.raises(MissionQueueError, match="retry limit"):
        queue.requeue(mission.mission_id)
