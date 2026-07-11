# Fluxo Mínimo Mission, Workflow E Task

Links principais: [README principal](../../README.md) | [Exemplos operacionais](README.md) | [Arquitetura da integração](../architecture/mission-workflow-task-integration.md)

## Objetivo

Mostrar o uso local mínimo da integração Mission Runner -> Workflow Engine -> Task Queue sem rede, banco, provider real, OpenCode real, Agent Orchestrator, capabilities, skills ou tools.

## Status

Status: `MVP`.

Este exemplo é executável em teste por fakes locais equivalentes aos de `tests/test_mission_workflow_task_integration.py`.

## Fluxo

```text
Mission
↓
InMemoryWorkflowProvider
↓
QueueBackedWorkflowExecutor
↓
WorkflowEngine.execute_with_queue()
↓
TaskQueue + TaskScheduler
↓
RuntimeAdapter.execute_task() fake
↓
WorkflowResult
↓
MissionResult
```

## Exemplo Conceitual

```python
from vercosa_ai_framework.missions import (
    DirectoryMissionQueue,
    InMemoryWorkflowProvider,
    Mission,
    MissionRunner,
    QueueBackedWorkflowExecutor,
)
from vercosa_ai_framework.workflows import TaskDependency, Workflow, WorkflowEngine, WorkflowTask

mission = Mission(title="Exemplo", goal="Executar duas tasks locais")

first = WorkflowTask(
    task_id="task-a",
    workflow_id="wf-local",
    mission_id=mission.mission_id,
    title="Primeira task",
    goal="Produzir artefato A",
)

second = WorkflowTask(
    task_id="task-b",
    workflow_id="wf-local",
    mission_id=mission.mission_id,
    title="Segunda task",
    goal="Produzir artefato B",
    dependencies=(TaskDependency("requires_completion", "task-a"),),
)

workflow = Workflow(
    workflow_id="wf-local",
    mission_id=mission.mission_id,
    title="Workflow local",
    goal=mission.goal,
    tasks=(first, second),
)

queue = DirectoryMissionQueue("/tmp/vaf-missions")
queue.enqueue(mission)

engine = WorkflowEngine(runtime=fake_runtime, guardian=fake_guardian)
runner = MissionRunner(
    queue,
    fake_runtime,
    workflow_provider=InMemoryWorkflowProvider({mission.mission_id: workflow}),
    workflow_executor=QueueBackedWorkflowExecutor(engine),
)

result = runner.run(mission.mission_id)
```

`fake_runtime` deve implementar `RuntimeAdapter` e retornar resultados determinísticos em `execute_task()`. `fake_guardian` deve implementar `evaluate()` e retornar decisões locais, sem chamar provider real.

## Limites

Este exemplo não demonstra Agent Orchestrator, Capability Resolver, SkillExecutor, ToolExecutor, Provider Gateway, providers reais, persistência externa, banco, rede ou OpenCode real.
