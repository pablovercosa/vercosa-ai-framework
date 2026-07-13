# Integração Task, Agent E Capability

Links principais: [README principal](../../README.md) | [Índice de módulos](module-index.md) | [Task Queue](../task-queue.md) | [Agent Orchestrator](../agent-orchestrator.md) | [Capabilities, Skills e Tools](../capabilities-skills-tools.md)

## Objetivo

Documentar o caminho mínimo validado na missão 0105 entre `TaskScheduler`, `AgentOrchestrator` e `CapabilityResolver`.

## Fluxo Validado

```text
Task Queue
↓
Task Scheduler
↓ executor injetado
AgentTaskExecutor
↓
Agent Orchestrator
↓ resolução declarativa obrigatória
Capability Resolver
↓
Runtime Adapter fake ou injetado
↓
AgentExecutionResult
↓
TaskExecutionOutcome
↓
Task Queue
```

Esse fluxo é local, determinístico e validado por testes. Ele não executa Skills, Tools, MCPs, APIs, bancos ou Providers.

## Responsabilidades

- `TaskQueue` mantém estado, dependências, tentativas e retry finito.
- `TaskScheduler` continua sendo o único loop operacional de tasks.
- `AgentTaskExecutor` é a ponte explícita entre o executor injetado do scheduler e o `AgentOrchestrator`.
- `AgentOrchestrator` seleciona `AgentProfile`, cria `agent_assignment_id`, resolve capabilities obrigatórias quando configurado e chama somente `RuntimeAdapter`.
- `CapabilityResolver` valida capability, permissões, Guardian opcional e skill declarativa compatível.

## Não Responsabilidades

- A Task Queue não seleciona agente.
- O scheduler não conhece registries de agentes ou capabilities.
- O Agent Orchestrator não controla retry de task.
- O Capability Resolver não executa Skill nem Tool.
- O Runtime Adapter não é Provider Gateway.

## Rastreabilidade

O fluxo preserva referências por `mission_id`, `workflow_id`, `task_id`, `attempt_id`, `agent_assignment_id`, capability request, capability resolvida, skill selecionada declarativamente, resultado de runtime e outcome da task.

## Estado

Status: `MVP`.

Validado por `tests/test_task_agent_capability_integration.py` como integração mínima. A execução concreta de Capability -> Skill -> Tool -> Provider Gateway continua futura e pertence à missão 0106.
