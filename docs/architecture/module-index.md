# Índice De Módulos

Links principais: [README principal](../../README.md) | [Mapa de arquitetura](../alignment/architecture-map.md) | [Revisão pós-integrações](post-integration-architecture-review.md) | [Padrão de README](../documentation/readme-standard.md) | [Política de documentação](../documentation/documentation-update-policy.md)

## Objetivo

Mapear os módulos do Vercosa AI Framework, suas responsabilidades, status, Specs e relações arquiteturais dentro da camada de Harness Engineering para agentes de IA.

## Cadeia Arquitetural

```text
Mission
↓
Mission Runner / Mission Orchestrator
↓
Workflow Engine
↓
Task Queue
↓
Agent Orchestrator
↓
Agents / Subagents
↓
Capabilities
↓
Policy / Guardian
↓
Skills
↓
Tools
↓
Provider Gateway
↓
Providers / MCPs / APIs / Runtimes
```

Essa cadeia descreve o harness operacional ao redor de modelos e agentes: camadas superiores expressam intenção e governança; camadas inferiores fornecem execução substituível por adapters.

A revisão arquitetural consolidada após as integrações até a missão 0080 está em [Revisão arquitetural pós-integrações](post-integration-architecture-review.md). Este índice permanece como mapa navegável e não duplica a revisão completa.

## Mapa Navegável

| Camada | Módulo | README | Status | Spec | Docs |
| --- | --- | --- | --- | --- | --- |
| Interface operacional | `cli/` | [cli](../../src/vercosa_ai_framework/cli/README.md) | MVP | [0004](../../specs/framework/0004-mission-runner.md) | [CLI](../cli.md) |
| Fundacional | `core/` | [core](../../src/vercosa_ai_framework/core/README.md) | MVP | [0001](../../specs/framework/0001-framework-foundation.md) | [Mapa de arquitetura](../alignment/architecture-map.md) |
| Missões | `missions/` | [missions](../../src/vercosa_ai_framework/missions/README.md) | MVP | [0004](../../specs/framework/0004-mission-runner.md) | [Mission Runner](../mission-runner.md), [Integração Mission/Workflow/Task](mission-workflow-task-integration.md) |
| Workflows | `workflows/` | [workflows](../../src/vercosa_ai_framework/workflows/README.md) | MVP | [0006](../../specs/framework/0006-workflow-engine.md) | [Workflow Engine](../workflow-engine.md), [Integração Mission/Workflow/Task](mission-workflow-task-integration.md) |
| Tarefas | `tasks/` | [tasks](../../src/vercosa_ai_framework/tasks/README.md) | MVP | [0007](../../specs/framework/0007-task-queue.md) | [Task Queue](../task-queue.md), [Integração Mission/Workflow/Task](mission-workflow-task-integration.md), [Integração Task/Agent/Capability](task-agent-capability-integration.md) |
| Agentes | `agents/` | [agents](../../src/vercosa_ai_framework/agents/README.md) | MVP | [0008](../../specs/framework/0008-agent-orchestrator.md) | [Agent Orchestrator](../agent-orchestrator.md), [Integração Task/Agent/Capability](task-agent-capability-integration.md) |
| Capabilities | `capabilities/` | [capabilities](../../src/vercosa_ai_framework/capabilities/README.md) | MVP | [0009](../../specs/framework/0009-capabilities-skills-tools.md) | [Capabilities, Skills, Tools](../capabilities-skills-tools.md), [Integração Task/Agent/Capability](task-agent-capability-integration.md) |
| Governança | `policy/` | [policy](../../src/vercosa_ai_framework/policy/README.md) | MVP | [0005](../../specs/framework/0005-guardian-engine.md) | [ADR Policy/Guardian](../../knowledge/decisions/2026-07-04-policy-engine-vs-guardian-engine.md) |
| Governança | `guardian/` | [guardian](../../src/vercosa_ai_framework/guardian/README.md) | MVP | [0005](../../specs/framework/0005-guardian-engine.md) | [Guardian Engine](../guardian-engine.md) |
| Governança e rastreabilidade | `audit/` | [audit](../../src/vercosa_ai_framework/audit/README.md) | contracts | [0001](../../specs/framework/0001-framework-foundation.md) | [Arquitetura de Audit/Event Log](audit-event-architecture.md) |
| Skills | `skills/` | [skills](../../src/vercosa_ai_framework/skills/README.md) | MVP | [0009](../../specs/framework/0009-capabilities-skills-tools.md) | [Capabilities, Skills, Tools](../capabilities-skills-tools.md) |
| Tools | `tools/` | [tools](../../src/vercosa_ai_framework/tools/README.md) | MVP | [0009](../../specs/framework/0009-capabilities-skills-tools.md) | [Capabilities, Skills, Tools](../capabilities-skills-tools.md) |
| Providers | `providers/` | [providers](../../src/vercosa_ai_framework/providers/README.md) | MVP | [0010](../../specs/framework/0010-provider-gateway.md) | [Provider Gateway](../provider-gateway.md) |
| Runtime | `runtime/` | [runtime](../../src/vercosa_ai_framework/runtime/README.md) | MVP | [0003](../../specs/framework/0003-opencode-runtime-adapter.md) | [OpenCode Runtime Adapter](../opencode-runtime-adapter.md) |
| Modelos | `model_selection/` | [model_selection](../../src/vercosa_ai_framework/model_selection/README.md) | MVP | [0002](../../specs/framework/0002-model-selection-engine.md) | [Context Router e Token Budget](../context-router-token-budget.md) |
| Contexto | `context/` | [context](../../src/vercosa_ai_framework/context/README.md) | MVP | [0014](../../specs/framework/0014-context-router-token-budget-memory.md) | [Context Router e Token Budget](../context-router-token-budget.md) |
| Conhecimento | `knowledge/` | [knowledge](../../src/vercosa_ai_framework/knowledge/README.md) | MVP | [0011](../../specs/framework/0011-knowledge-hub.md) | [Knowledge Hub](../knowledge-hub.md) |
| Canonicalização | `canonicalizer/` | [canonicalizer](../../src/vercosa_ai_framework/canonicalizer/README.md) | MVP | [0012](../../specs/framework/0012-canonicalizer.md) | [Canonicalizer](../canonicalizer.md) |
| Persistência | `persistence/` | [persistence](../../src/vercosa_ai_framework/persistence/README.md) | MVP | [0013](../../specs/framework/0013-persistence-layer.md) | [Persistence Layer](../persistence-layer.md) |

## Relações Principais

- `missions/` controla ciclo operacional de missões, compõe contexto de execução por contrato base e pode delegar para `workflows/` por `MissionWorkflowProvider` e `MissionWorkflowExecutor` injetados.
- `workflows/` define plano e execução sequencial MVP; no caminho integrado, `execute_with_queue()` usa `tasks/` como substrato de estado, elegibilidade, tentativas e retries.
- `agents/` seleciona perfis, prepara execução e pode resolver capabilities obrigatórias de forma declarativa antes do runtime quando configurado explicitamente, mas não chama tools, providers, MCPs ou bancos diretamente.
- `capabilities/`, `skills/`, `tools/` e `providers/` formam a cadeia de resolução de intenção até infraestrutura concreta; no fluxo 0105 somente a resolução Capability -> Skill declarativa foi integrada.
- `policy/` resolve políticas declarativas, precedência e conflitos básicos sem enforcement operacional; `guardian/`, `context/` e `model_selection/` podem consumir `ResolvedPolicySet` opcional já resolvido, sem chamar o Policy Engine por conta própria.
- `audit/` define contratos iniciais, implementação em memória, persistência local JSONL opt-in e helpers opcionais para eventos de decisões Policy, Guardian e Context, além de eventos básicos de ciclo de vida de missão e batch; a integração com `MissionRunner` Python é opcional e não altera scripts shell, persistência externa, banco ou fluxo operacional de diretórios. A arquitetura dedicada está em [Arquitetura de Audit/Event Log](audit-event-architecture.md).
- `model_selection/` é transversal e decide modelos por política, catálogo local e requisitos opcionais de orçamento de tokens, não por hardcode; pode considerar políticas resolvidas opcionais para warnings, aprovação e exclusões determinísticas sem chamar providers, billing real, Context Router ou Guardian Engine.
- `context/` monta pacotes de contexto, aplica orçamento de tokens, expõe `model_requirements` mínimos e considera políticas resolvidas opcionais sem buscar, indexar, persistir, chamar providers diretamente, resolver políticas, selecionar modelos ou decidir enforcement operacional amplo.
- `knowledge/` organiza documentos, busca textual MVP e fornece adaptador determinístico para candidatos do Context Router; `canonicalizer/` prepara documentos canônicos antes de ingestão.
- `persistence/` oferece portas e adapters para durabilidade sem fixar storage específico.
- `runtime/` isola execução concreta em runtimes como OpenCode; OpenCode é adapter/laboratório atual, não núcleo do framework.
- `cli/` oferece consulta local básica de estado operacional, listagem de missões por estado, resumo pós-batch auxiliar, validação estrutural local, diagnóstico local com `doctor`, validação local de links Markdown com `docs-links` e diagnóstico de prontidão alfa com `alpha-readiness`, sem substituir scripts shell, `pytest`, `compileall`, checklist pré-tag nem executar missões nesta fase.

## Lacunas Registradas

As principais lacunas arquiteturais já estão listadas em [Perguntas em aberto](../alignment/open-questions.md), especialmente:

- integração orquestrada entre Policy Engine, Context Router, Guardian Engine, Model Selection e Audit/Event Log nos fluxos completos, além das pontes iniciais via `ResolvedPolicySet` opcional, requisitos opcionais de orçamento de tokens e helpers de eventos;
- fronteira entre Mission Runner e Mission Orchestrator;
- integração completa a partir de Capability -> Skill -> Tool -> Provider, após a ponte mínima Task Queue -> Agent Orchestrator -> Capability Resolver;
- Context Router integrado aos fluxos de missão, agente, modelo, Guardian e recuperação governada completa do Knowledge Hub;
- integração automática de persistência local de eventos auditáveis nos fluxos operacionais;
- Semantic Index, embeddings, pgvector e RAG semântico.
