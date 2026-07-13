# Task Queue MVP

The Task Queue MVP implements the operational queue defined by `specs/framework/0007-task-queue.md`.

It is intentionally in-memory and provider agnostic. It does not execute OpenCode, call subprocesses, use `sudo`, read global configuration, or contact external providers.

## Components

- `TaskQueue` stores workflow task state, dependencies, attempts, retry counters, and deterministic selection.
- `TaskScheduler` drains eligible queue items sequentially through an injected Python executor used by tests or future framework boundaries.
- `TaskExecutionOutcome` is the normalized result returned by that executor.
- `AgentTaskExecutor`, definido em `agents/`, pode ser usado como executor injetado para acionar o `AgentOrchestrator` sem criar dependência de `tasks/` para `agents/`.

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

No caminho integrado da missão 0105, a fila preserva referências genéricas como `agent_assignment_ref`, `runtime_result_ref`, `audit_log_ref` e metadados do outcome. Essas referências são rastreabilidade operacional; elas não tornam a Task Queue responsável por selecionar agente, resolver capability ou executar runtime.

## Uso No Fluxo Integrado

No caminho integrado da missão 0104, `WorkflowEngine.execute_with_queue()` materializa `WorkflowTask` em `Task` e entrega a fila ao `TaskScheduler`.

Nesse fluxo:

- `TaskScheduler` é o único loop operacional de tasks;
- `TaskQueue` controla dependências, tentativas e retries;
- o executor injetado chama o runtime por uma fronteira acima da fila;
- `tasks/` não importa `workflows/`, `missions/`, runtime, providers, agentes, capabilities, skills ou tools.

No caminho integrado da missão 0105, o executor injetado pode ser a ponte `AgentTaskExecutor`, que converte `AgentExecutionResult` em `TaskExecutionOutcome`. Retry continua pertencendo à Task Queue e ao scheduler.

Documento arquitetural: [Integração Mission Runner, Workflow Engine e Task Queue](architecture/mission-workflow-task-integration.md).

Documento complementar: [Integração Task, Agent e Capability](architecture/task-agent-capability-integration.md).
