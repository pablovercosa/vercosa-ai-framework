# Integração Mission Runner, Workflow Engine E Task Queue

Links principais: [README principal](../../README.md) | [Índice de módulos](module-index.md) | [Mission Runner](../mission-runner.md) | [Workflow Engine](../workflow-engine.md) | [Task Queue](../task-queue.md) | [Spec 0004](../../specs/framework/0004-mission-runner.md) | [Spec 0006](../../specs/framework/0006-workflow-engine.md) | [Spec 0007](../../specs/framework/0007-task-queue.md)

## Objetivo

Documentar o fluxo mínimo integrado implementado pela missão 0104 entre Mission Runner, Workflow Engine, Task Queue e Task Scheduler.

## Status

Status: `MVP`.

O fluxo `Mission Runner -> Workflow Engine -> Task Queue -> Task Scheduler -> RuntimeAdapter.execute_task()` está implementado e validado por `tests/test_mission_workflow_task_integration.py`.

## Fluxo Integrado

```text
Mission
↓
MissionRunner
↓
MissionWorkflowProvider.resolve()
↓
QueueBackedWorkflowExecutor
↓
WorkflowEngine.execute_with_queue()
↓
WorkflowTask -> Task
↓
TaskQueue
↓
TaskScheduler
↓
executor injetado
↓
RuntimeAdapter.execute_task()
↓
TaskExecutionOutcome
↓
WorkflowResult
↓
MissionResult
```

## Responsabilidades

`MissionRunner` continua responsável por estado global da missão, ciclo, Guardian de missão, validação final, auto-commit opcional e estado terminal da missão.

`WorkflowEngine.execute_with_queue()` continua responsável por semântica de workflow, avaliação Guardian por task, materialização de tasks operacionais, execução via scheduler e reconstrução do `WorkflowResult`.

`TaskQueue` continua responsável por estado operacional, dependências, elegibilidade, tentativas e retries finitos.

`TaskScheduler` é o único loop operacional de tasks no caminho integrado e usa apenas executor injetado.

## Contratos Injetáveis

`MissionWorkflowProvider` resolve uma `Mission` normalizada para um `Workflow` local e determinístico.

`MissionWorkflowExecutor` executa o `Workflow` e retorna `WorkflowResult` sem alterar diretamente estado de missão.

`QueueBackedWorkflowExecutor` adapta `WorkflowEngine.execute_with_queue()` ao contrato usado pelo Mission Runner.

`InMemoryWorkflowProvider` é uma implementação local usada por testes e exemplos. Ela não acessa rede, banco, provider ou catálogo persistente.

## Mapeamento WorkflowTask Para Task

| Campo em `WorkflowTask` | Campo em `Task` | Observação |
| --- | --- | --- |
| `mission_id` | `mission_id` | Preservado. |
| `workflow_id` | `workflow_id` | Preservado. |
| `task_id` | `task_id` | Preservado. |
| `title` | `title` | Preservado. |
| `goal` | `goal` | Preservado. |
| `task_type` | `task_type` | Preservado. |
| `priority` | `priority` | Preservado como inteiro de ordenação. |
| `risk_level` | `risk_level` | Preservado. |
| `required_capabilities` | `required_capabilities` | Preservado como metadado operacional, sem resolver capabilities. |
| dependências obrigatórias | `dependencies` | Apenas dependências obrigatórias afetam elegibilidade da fila. |
| dependências opcionais | `metadata.optional_dependencies` | Preservadas sem bloquear execução. |
| `retry_policy.max_attempts` | `max_attempts` | Default documentado: `1`. Valor inválido falha antes da execução. |
| `execution_limits` | `metadata.execution_limits` | Preservado e usado no request de runtime pelo engine. |
| `acceptance_criteria` | `metadata.acceptance_criteria` | Preservado. |
| `inputs` | `metadata.inputs` | Preservado. |
| `expected_outputs` | `metadata.expected_outputs` | Preservado. |
| `model_policy` | `metadata.model_policy` | Preservado; não seleciona modelo nesta integração. |
| `validation_policy` | `metadata.validation_policy` | Preservado. |
| `artifacts` | `artifact_refs` | Preservado e consolidado ao retornar para workflow. |
| `audit_log_ref` | `audit_log_ref` e metadata | Preservado. |

## Mapeamento De Estados

| `TaskStatus` de Workflow | `TaskQueueState` | Observação |
| --- | --- | --- |
| `pending` | `queued` | Default antes da elegibilidade. |
| `ready` | `queued` | A fila decide elegibilidade real. |
| `running` | `running` | Preservado. |
| `blocked` | `blocked` | Preservado. |
| `validating` | `running` | Não há estado equivalente na Queue; divergência fica em metadata. |
| `done` | `done` | Preservado. |
| `failed` | `failed` | Preservado. |
| `skipped` | `skipped` | Preservado. |
| `cancelled` | `cancelled` | Preservado. |

No retorno, `queued` vira `ready` no `WorkflowTask`, porque a fila não distingue `pending` de `ready` internamente.

## Compatibilidade Legada

Quando `MissionRunner` não recebe `workflow_provider` e `workflow_executor`, o caminho legado permanece ativo e chama `RuntimeAdapter.execute_mission()`.

Quando apenas uma das duas integrações é configurada, a missão falha claramente com `workflow integration requires provider and executor`.

## Limites

Esta integração não implementa Mission Orchestrator completo, Agent Orchestrator, capabilities, skills, tools, Provider Gateway, providers reais, rede, banco, persistência externa, paralelismo ou RAG.

O caminho legado `WorkflowEngine.execute()` permanece para compatibilidade, mas o caminho integrado validado usa `execute_with_queue()` e `TaskScheduler` como único loop de tasks.

## Evidência

Evidência principal: `tests/test_mission_workflow_task_integration.py`.

O teste cobre fluxo bem-sucedido com duas tasks dependentes, falha de task obrigatória com retry e dependente bloqueada, compatibilidade legada do Mission Runner e fronteiras do módulo `tasks`.
