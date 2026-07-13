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

Esse fluxo é local, determinístico e validado por testes. Na missão 0105 ele resolvia capabilities de forma declarativa. A missão 0106 adicionou execução opcional por `capability_executor` em dry-run governado, documentada em [Capabilities, Skills e Tools](../capabilities-skills-tools.md).

## Responsabilidades

- `TaskQueue` mantém estado, dependências, tentativas e retry finito.
- `TaskScheduler` continua sendo o único loop operacional de tasks.
- `AgentTaskExecutor` é a ponte explícita entre o executor injetado do scheduler e o `AgentOrchestrator`.
- `AgentOrchestrator` seleciona `AgentProfile`, cria `agent_assignment_id`, resolve capabilities obrigatórias quando configurado, executa capabilities por contrato injetável quando exigido e chama somente `RuntimeAdapter` após sucesso.
- `CapabilityResolver` valida capability, permissões, Guardian opcional e skill declarativa compatível.

## Não Responsabilidades

- A Task Queue não seleciona agente.
- O scheduler não conhece registries de agentes ou capabilities.
- O Agent Orchestrator não controla retry de task.
- O Capability Resolver não executa Skill nem Tool.
- O Agent Orchestrator não importa nem constrói SkillExecutor, ToolExecutor, ProviderGateway, adapters concretos, MCPs, APIs ou clientes de rede.
- O Runtime Adapter não é Provider Gateway.

## Rastreabilidade

O fluxo preserva referências por `mission_id`, `workflow_id`, `task_id`, `attempt_id`, `agent_assignment_id`, capability request, capability resolvida, skill selecionada, execução de capability quando configurada, resultado de runtime e outcome da task.

## Estado

Status: `MVP`.

Validado por `tests/test_task_agent_capability_integration.py` como integração mínima 0105. O dry-run Capability -> Skill -> Tool -> Provider Gateway foi adicionado em 0106 e é validado por `tests/test_capability_skill_tool_provider_dry_run.py`, sem provider real, rede, banco, MCP ou API externa.
