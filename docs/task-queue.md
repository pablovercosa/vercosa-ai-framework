# Task Queue MVP

The Task Queue MVP implements the operational queue defined by `specs/framework/0007-task-queue.md`.

It is intentionally in-memory and provider agnostic. It does not execute OpenCode, call subprocesses, use `sudo`, read global configuration, or contact external providers.

## Components

- `TaskQueue` stores workflow task state, dependencies, attempts, retry counters, and deterministic selection.
- `TaskScheduler` drains eligible queue items sequentially through an injected Python executor used by tests or future framework boundaries.
- `TaskExecutionOutcome` is the normalized result returned by that executor.

## Deterministic Selection

The next executable task is selected by:

1. Rejecting selection when any task is already `running`.
2. Filtering tasks in `queued` state.
3. Requiring all dependencies to be `done`.
4. Requiring `next_attempt_at` to be due.
5. Sorting by priority ascending, dependency depth, `created_at` ascending, and `task_id` lexicographic order.

Lower numeric priority means higher priority.

## States

Queue items can be marked as `queued`, `running`, `done`, `failed`, `skipped`, `blocked`, or `cancelled`.

The scheduler applies outcomes as follows:

- `done`: completes the running task and stores artifact refs.
- `failed`: records the failure and requeues only if retry budget remains.
- `blocked`: blocks the task with a reason.
- `skipped`: skips the task with a reason.
- `cancelled`: cancels the task with a reason.

When a dependency is `failed`, queued dependents are marked `blocked` with `blocked_by` pointing to the failed dependency.

## Retries

Retries are finite. `max_attempts` defaults to `1`. A failed task may return to `queued` only while `attempt_count < max_attempts`.

The scheduler preserves every `TaskAttempt` and never retries indefinitely.

## Boundaries

This MVP is not a runtime adapter and not an agent orchestrator. Future execution layers must call the queue through explicit framework contracts and return normalized outcomes without exposing the queue to provider-specific details.
