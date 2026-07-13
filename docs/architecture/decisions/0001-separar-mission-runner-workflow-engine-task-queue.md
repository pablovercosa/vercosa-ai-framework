# ADR 0001: Separar Mission Runner, Workflow Engine e Task Queue

Estado: Aceita.

## Contexto

As missões 0104 a 0107 validaram um fluxo mínimo em que Mission Runner, Workflow Engine e Task Queue cooperam por contratos injetáveis, sem fundir responsabilidades.

## Decisão

Manter Mission Runner, Workflow Engine e Task Queue como camadas separadas.

O Mission Runner controla o ciclo de vida da Mission e agrega `WorkflowResult` em `MissionResult` quando recebe integração explícita. O Workflow Engine constrói e acompanha o Workflow. A Task Queue, por meio do `TaskScheduler`, controla execução operacional de Tasks, estados, dependências, tentativas e retries.

## Evidências

- Código: `src/vercosa_ai_framework/missions/runner.py`.
- Código: `src/vercosa_ai_framework/missions/workflow_integration.py`.
- Código: `src/vercosa_ai_framework/workflows/engine.py`.
- Código: `src/vercosa_ai_framework/tasks/scheduler.py`.
- Teste: `tests/test_mission_workflow_task_integration.py`.

## Consequências

- Mission Runner não deve absorver permanentemente Workflow Engine.
- Task Queue não deve conhecer Agent, Capability, Skill, Tool, Provider, Runtime ou Mission Runner.
- Retries permanecem responsabilidade da Task Queue.

## Decisões Ainda Pendentes

- Mission Orchestrator como módulo separado.
- Remoção futura do caminho legado `WorkflowEngine.execute()`.
- Contrato persistente final de Workflow, Task Queue e tentativas.
