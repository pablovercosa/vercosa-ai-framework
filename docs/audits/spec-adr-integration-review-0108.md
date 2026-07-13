# Auditoria 0108: Revisão De Specs E ADRs Da Integração Mínima

Links principais: [README principal](../../README.md) | [Status de implementação](../alignment/implementation-status.md) | [Perguntas em aberto](../alignment/open-questions.md) | [Índice de módulos](../architecture/module-index.md) | [Decisões arquiteturais](../architecture/decisions/README.md)

## Objetivo

Auditar Specs e decisões arquiteturais afetadas pelas integrações mínimas concluídas nas missões 0104, 0105, 0106 e 0107.

Esta auditoria é documental e arquitetural. Ela não cria comportamento de runtime, não altera código, não altera testes e não valida provider real, rede, banco, MCP, API externa, PostgreSQL, pgvector, RAG ou release.

## Escopo Revisado

Specs revisadas:

- `specs/framework/0001-framework-foundation.md`
- `specs/framework/0002-model-selection-engine.md`
- `specs/framework/0004-mission-runner.md`
- `specs/framework/0005-guardian-engine.md`
- `specs/framework/0006-workflow-engine.md`
- `specs/framework/0007-task-queue.md`
- `specs/framework/0008-agent-orchestrator.md`
- `specs/framework/0009-capabilities-skills-tools.md`
- `specs/framework/0010-provider-gateway.md`
- `specs/framework/0014-context-router-token-budget-memory.md`

Evidências principais de integração:

- `tests/test_mission_workflow_task_integration.py`
- `tests/test_task_agent_capability_integration.py`
- `tests/test_capability_skill_tool_provider_dry_run.py`
- `tests/test_agent_execution_governance_0107.py`

## Matriz De Auditoria

| Documento normativo | Responsabilidade declarada | Implementação correspondente | Evidência por teste | Estado | Divergência encontrada | Ação adotada | Decisão ainda pendente |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `0001-framework-foundation.md` | Fundação Specification First, provider agnostic, local first e execução por missões | Integração mínima local entre módulos centrais por contratos injetáveis | `tests/test_mission_workflow_task_integration.py`, `tests/test_task_agent_capability_integration.py`, `tests/test_capability_skill_tool_provider_dry_run.py`, `tests/test_agent_execution_governance_0107.py` | Validado no fluxo mínimo | Spec conceitual não diferenciava claramente o recorte validado 0104-0107 | Adicionada seção de estado implementado e validado em 0108 | Fluxo público completo, providers reais, RAG, PostgreSQL, pgvector, múltiplos runtimes reais e release |
| `0002-model-selection-engine.md` | Selecionar modelo por política, contexto, custo, qualidade e segurança sem hardcode | `src/vercosa_ai_framework/model_selection/` com catálogo em memória injetado e `ModelSelectionPolicy` | `tests/test_model_selection.py`, `tests/test_policy_model_selection_integration.py`, `tests/test_token_budget_model_selection_integration.py`, `tests/test_agent_execution_governance_0107.py` | Integrado e validado no caminho 0107 | Spec descrevia descoberta/fallback mais ampla do que o MVP atual | Registrado que não chama provider nem runtime e que fallback externo real não foi validado | Model Registry persistente, descoberta real de modelos, billing e fallback externo |
| `0004-mission-runner.md` | Controlar ciclo de Mission sem substituir Workflow Engine | `MissionRunner`, `InMemoryWorkflowProvider`, `QueueBackedWorkflowExecutor` | `tests/test_mission_workflow_task_integration.py` | Validado | Integração com Workflow ainda aparecia como futura em parte do texto | Registrado caminho injetável validado e que Mission Runner não absorve Workflow Engine | Mission Orchestrator separado e fronteira final Mission Runner/Orchestrator |
| `0005-guardian-engine.md` | Enforcement operacional por decisões `allow`, `warn`, `block`, `require_approval` | `GuardianEngine`, avaliação de ContextPackage e consumo de políticas resolvidas | `tests/test_guardian_engine.py`, `tests/test_guardian_context_package_checks.py`, `tests/test_policy_guardian_integration.py`, `tests/test_agent_execution_governance_0107.py` | Integrado e validado no caminho 0107 | Fronteira com Policy Engine precisava ficar explícita no estado implementado | Registrada separação Policy resolve, Guardian aplica enforcement | Formato definitivo de aprovação humana e políticas versionadas |
| `0006-workflow-engine.md` | Transformar Mission em Workflow/Tasks e acompanhar resultado | `WorkflowEngine.execute_with_queue()` e `task_mapping.py` | `tests/test_mission_workflow_task_integration.py`, `tests/test_task_agent_capability_integration.py`, `tests/test_agent_execution_governance_0107.py` | Validado no caminho mínimo | Caminho legado `execute()` precisava ser classificado | Registrado `execute_with_queue()` como caminho integrado mínimo e `execute()` como compatibilidade transitória | Remoção/depreciação futura do caminho legado |
| `0007-task-queue.md` | Controlar Tasks, dependências, tentativas, retries e execução sequencial | `TaskQueue` e `TaskScheduler` com executor injetado | `tests/test_task_scheduler.py`, `tests/test_mission_workflow_task_integration.py`, `tests/test_task_agent_capability_integration.py`, `tests/test_capability_skill_tool_provider_dry_run.py` | Validado | Spec não registrava o scheduler como loop operacional validado | Registrado TaskScheduler como loop operacional e Task Queue sem conhecimento de camadas superiores | Persistência final, recovery após crash e paralelismo futuro |
| `0008-agent-orchestrator.md` | Selecionar Agent Profile e coordenar execução sem acessar provider/MCP/API/banco diretamente | `AgentOrchestrator`, `AgentTaskExecutor`, `AgentExecutionGovernance` | `tests/test_task_agent_capability_integration.py`, `tests/test_capability_skill_tool_provider_dry_run.py`, `tests/test_agent_execution_governance_0107.py` | Integrado e validado | Dependências opcionais e comportamento legado precisavam ficar claros | Registrado AgentTaskExecutor como ponte e Execution Governance como dependência explícita opcional | Catálogo real de agents e política de subagents |
| `0009-capabilities-skills-tools.md` | Separar Capability, Skill e Tool com rastreabilidade e governança | `CapabilityResolver`, `ResolvedCapabilityExecutor`, `SkillExecutor`, `ToolExecutor` | `tests/test_capability_resolution.py`, `tests/test_skill_executor.py`, `tests/test_tool_executor.py`, `tests/test_tool_executor_provider_gateway.py`, `tests/test_capability_skill_tool_provider_dry_run.py` | Integrado e validado em dry-run | Separação entre resolução e execução precisava ser normativa no estado atual | Registrado que resolver não executa Skill e que ToolExecutor chama ProviderGateway | Catálogos aprovados e política de fallback de tools |
| `0010-provider-gateway.md` | Isolar Tools de providers concretos e suportar dry-run rastreável | `ProviderGateway`, `ProviderRegistry`, `ProviderProfile` | `tests/test_provider_gateway.py`, `tests/test_tool_executor_provider_gateway.py`, `tests/test_capability_skill_tool_provider_dry_run.py`, `tests/test_agent_execution_governance_0107.py` | Validado em dry-run | Spec poderia ser lida como validação de provider real | Registrado que dry-run usa Gateway real, mas não chama adapter concreto | Providers reais, rede, MCP, bancos, APIs externas e fallback externo real |
| `0014-context-router-token-budget-memory.md` | Montar ContextPackage, aplicar Token Budget e preparar requisitos para Model Selection sem RAG | `DeterministicContextRouter`, `TokenBudgetManager`, `ContextPackage` | `tests/test_context_router_mvp.py`, `tests/test_context_contracts.py`, `tests/test_policy_context_router_integration.py`, `tests/test_token_budget_model_selection_integration.py`, `tests/test_agent_execution_governance_0107.py` | Integrado e validado no caminho 0107 | Spec conceitual precisava registrar MVP implementado sem busca vetorial/memória global | Registrado candidatos explícitos, omissão determinística e ausência de RAG/memória global | Semantic Index, pgvector, PostgreSQL, RAG e modelo definitivo de memória |
| `docs/architecture/decisions/0001-0007` | Registrar decisões arquiteturais comprovadas | ADRs documentais em `docs/architecture/decisions/` | Testes listados nas ADRs | Implementado documentalmente | Não havia diretório `docs/architecture/decisions/` para a revisão 0108; ADRs históricas existem fora do escopo permitido da missão | Criado registro documental em `docs/architecture/decisions/` sem mover decisões históricas | Consolidar política canônica de localização de ADRs em missão futura, se necessário |
| `docs/alignment/implementation-status.md` | Fonte canônica factual de estado | Checklist atualizado com fluxo 0107 validado | Testes 0104-0107 | Atualizado | Linha anterior dizia que Policy/Context/Token/Model/Audit ainda faltavam na integração global | Atualizado para registrar validação mínima 0107 e limites explícitos | Fluxo público completo de produto |
| `docs/alignment/open-questions.md` | Registrar decisões abertas | Perguntas mantidas para Mission Orchestrator, legado, providers, RAG, persistência e aprovação | Não aplicável como teste | Atualizado | Havia notas dizendo que 0108 ainda deveria revisar decisões já auditadas nesta missão | Atualizadas notas de decisões encaminhadas e mantidas perguntas abertas | Todas as decisões explicitamente marcadas como pendentes |

## ADRs Criadas

- `docs/architecture/decisions/0001-separar-mission-runner-workflow-engine-task-queue.md`: aceita.
- `docs/architecture/decisions/0002-agent-task-executor-como-ponte-desacoplada.md`: aceita.
- `docs/architecture/decisions/0003-separar-resolucao-e-execucao-de-capability.md`: aceita.
- `docs/architecture/decisions/0004-provider-gateway-dry-run-sem-adapter-concreto.md`: aceita.
- `docs/architecture/decisions/0005-policy-guardian-governanca-injetavel.md`: aceita.
- `docs/architecture/decisions/0006-contextpackage-model-selection-audit-observador.md`: aceita.
- `docs/architecture/decisions/0007-compatibilidade-legada-por-configuracao-explicita.md`: provisória.

## Decisões Mantidas Em Aberto

- Mission Orchestrator como módulo separado.
- Remoção do `WorkflowEngine.execute()` legado.
- Catálogo real de Agents, Capabilities, Skills e Tools.
- Providers reais.
- Múltiplos runtimes reais.
- Formato definitivo de aprovação humana.
- Persistência externa de auditoria.
- PostgreSQL.
- pgvector.
- RAG.
- Modelo definitivo de memória.
- Consumidor principal do produto.
- Tag ou release alfa.

## Conclusão

As Specs revisadas agora diferenciam arquitetura pretendida, comportamento implementado, fluxo integrado validado, compatibilidade legada, limitações atuais e decisões pendentes.

O estado validado continua sendo MVP local, determinístico, injetável e sem provider real. O checklist canônico permanece `docs/alignment/implementation-status.md`.
