# ADR 0002: Usar AgentTaskExecutor Como Ponte Desacoplada

Estado: Aceita.

## Contexto

A missão 0105 validou Task Scheduler -> AgentTaskExecutor -> Agent Orchestrator -> Capability Resolver, preservando a independência da Task Queue em relação a agentes e capabilities.

## Decisão

Usar `AgentTaskExecutor` como ponte explícita e injetável entre Task Scheduler e Agent Orchestrator.

O Agent Orchestrator seleciona `AgentProfile`, cria execução normalizada e pode resolver Capabilities antes do runtime quando configurado. A Task Queue permanece responsável por estado, tentativas e retries.

## Evidências

- Código: `src/vercosa_ai_framework/agents/task_executor.py`.
- Código: `src/vercosa_ai_framework/agents/orchestrator.py`.
- Código: `src/vercosa_ai_framework/tasks/scheduler.py`.
- Teste: `tests/test_task_agent_capability_integration.py`.

## Consequências

- Task Queue não importa `agents`, `capabilities`, `skills`, `tools` ou `providers`.
- Agent Orchestrator não controla retry operacional da fila.
- Falhas de agente retornam como resultado de task para decisão da Task Queue.

## Decisões Ainda Pendentes

- Catálogo real de Agent Profiles.
- Política final de delegação para subagents.
- Contrato persistente de Agent Assignment.
