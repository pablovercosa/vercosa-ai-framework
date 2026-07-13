# Integração De Governança Da Execução 0107

Links principais: [README principal](../../README.md) | [Índice de módulos](module-index.md) | [Agent Orchestrator](../agent-orchestrator.md) | [Exemplo mínimo](../examples/minimal-execution-governance-0107.md)

## Objetivo

Documentar a integração mínima e local entre Policy Engine, Guardian Engine, Context Router, Token Budget Manager, Model Selection Engine e Audit/Event Log no fluxo de execução de Agent Assignment.

## Fluxo Validado

```text
Mission Runner
-> Workflow Engine
-> Task Queue
-> Agent Orchestrator
-> AgentExecutionGovernance
-> Policy Engine
-> Context Router
-> Token Budget Manager
-> Guardian Engine para ContextPackage
-> Model Selection Engine
-> Capability Resolver
-> Capability Executor
-> Skill Executor
-> Tool Executor
-> Provider Gateway em dry-run
-> Runtime Adapter fake ou injetado
-> Guardian Engine para validação
-> Audit/Event Log
-> AgentExecutionResult
-> TaskExecutionOutcome
-> WorkflowResult
```

## Responsabilidades

- `AgentExecutionGovernance` prepara a execução de forma explícita e injetável antes do runtime.
- `Policy Engine` resolve `PolicySet` explícitos em um único `ResolvedPolicySet` efetivo.
- `Context Router` recebe apenas candidatos explícitos, aplica orçamento e produz `ContextPackage`.
- `Guardian Engine` avalia planejamento, contexto e validação final.
- `Model Selection Engine` recebe `ResolvedPolicySet` e requisitos derivados do `ContextPackage`.
- `Audit/Event Log` registra decisões estruturadas em ordem de inserção quando injetado.
- `AgentOrchestrator` coordena o fluxo sem montar contexto, resolver políticas ou escrever JSONL diretamente.

## Não Responsabilidades

- Não faz RAG, busca vetorial, crawling, banco, rede, MCP, provider real ou subprocesso.
- Não ativa `JsonlAuditEventLog` globalmente.
- Não muda a responsabilidade da Task Queue.
- Não transforma Policy Engine em enforcement operacional.
- Não transforma Context Router em seletor de modelo.

## Entradas

- `Task` e `TaskAttempt` do fluxo local.
- `AgentProfile` selecionado pelo `AgentOrchestrator`.
- `PolicySet` explícitos por dependência, configuração do pipeline ou `Task.metadata`/`Task.metadata["inputs"]`.
- `ContextItem` e `ContextSource` explícitos por `Task.metadata`/`Task.metadata["inputs"]`.
- `TokenBudget` derivado de metadados explícitos, limites do agente ou default conservador.
- Catálogo de modelos em memória injetado no `ModelSelector`.
- `EventLog` opcional em memória ou outro port compatível.

## Saídas

- `AgentExecutionGovernanceResult` com `PolicyResolutionResult`, `ResolvedPolicySet`, `ContextRequest`, `ContextPackage`, decisões Guardian, decisão de modelo, warnings, erros, aprovações e refs de auditoria.
- `AgentExecutionRequest` com referências principais, sem duplicar conteúdo sensível em metadados auditáveis.
- `RuntimeExecutionRequest` com `ContextPackage` por referência no contexto de execução e `SelectionDecision` normalizada.
- `AgentExecutionResult` e `TaskExecutionOutcome` com `policy_resolution_id`, `context_package_id`, `selected_model_id`, `guardian_decision_refs` e `audit_event_refs`.

## Ordem De Auditoria

Quando os eventos existem, a ordem validada é:

1. `policy.resolution`
2. `context.package`
3. `guardian.decision` para contexto
4. `model_selection.decision`
5. `agent_execution.governance_started`
6. `agent_execution.runtime_result`
7. `guardian.decision` para validação quando registrado pelo chamador
8. `agent_execution.final_result`

Bloqueios de preparação registram `agent_execution.governance_blocked` antes de capabilities e runtime.

## Status

Status: `MVP`.

O fluxo está validado com fakes locais e dry-run para Provider Gateway. Provider real, rede, banco, MCP, API externa, RAG e persistência externa continuam fora do estado implementado.
