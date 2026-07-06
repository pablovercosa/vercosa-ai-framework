# Índice De Módulos

Links principais: [README principal](../../README.md) | [Mapa de arquitetura](../alignment/architecture-map.md) | [Padrão de README](../documentation/readme-standard.md) | [Política de documentação](../documentation/documentation-update-policy.md)

## Objetivo

Mapear os módulos do Vercosa AI Framework, suas responsabilidades, status, Specs e relações arquiteturais.

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
Guardian / Policy
↓
Skills
↓
Tools
↓
Provider Gateway
↓
Providers / MCPs / APIs / Runtimes
```

## Mapa Navegável

| Camada | Módulo | README | Status | Spec | Docs |
| --- | --- | --- | --- | --- | --- |
| Fundacional | `core/` | [core](../../src/vercosa_ai_framework/core/README.md) | MVP | [0001](../../specs/framework/0001-framework-foundation.md) | [Mapa de arquitetura](../alignment/architecture-map.md) |
| Missões | `missions/` | [missions](../../src/vercosa_ai_framework/missions/README.md) | MVP | [0004](../../specs/framework/0004-mission-runner.md) | [Mission Runner](../mission-runner.md) |
| Workflows | `workflows/` | [workflows](../../src/vercosa_ai_framework/workflows/README.md) | MVP | [0006](../../specs/framework/0006-workflow-engine.md) | [Workflow Engine](../workflow-engine.md) |
| Tarefas | `tasks/` | [tasks](../../src/vercosa_ai_framework/tasks/README.md) | MVP | [0007](../../specs/framework/0007-task-queue.md) | [Task Queue](../task-queue.md) |
| Agentes | `agents/` | [agents](../../src/vercosa_ai_framework/agents/README.md) | MVP | [0008](../../specs/framework/0008-agent-orchestrator.md) | [Agent Orchestrator](../agent-orchestrator.md) |
| Capabilities | `capabilities/` | [capabilities](../../src/vercosa_ai_framework/capabilities/README.md) | MVP | [0009](../../specs/framework/0009-capabilities-skills-tools.md) | [Capabilities, Skills, Tools](../capabilities-skills-tools.md) |
| Governança | `guardian/` | [guardian](../../src/vercosa_ai_framework/guardian/README.md) | MVP | [0005](../../specs/framework/0005-guardian-engine.md) | [Guardian Engine](../guardian-engine.md) |
| Skills | `skills/` | [skills](../../src/vercosa_ai_framework/skills/README.md) | MVP | [0009](../../specs/framework/0009-capabilities-skills-tools.md) | [Capabilities, Skills, Tools](../capabilities-skills-tools.md) |
| Tools | `tools/` | [tools](../../src/vercosa_ai_framework/tools/README.md) | MVP | [0009](../../specs/framework/0009-capabilities-skills-tools.md) | [Capabilities, Skills, Tools](../capabilities-skills-tools.md) |
| Providers | `providers/` | [providers](../../src/vercosa_ai_framework/providers/README.md) | MVP | [0010](../../specs/framework/0010-provider-gateway.md) | [Provider Gateway](../provider-gateway.md) |
| Runtime | `runtime/` | [runtime](../../src/vercosa_ai_framework/runtime/README.md) | MVP | [0003](../../specs/framework/0003-opencode-runtime-adapter.md) | [OpenCode Runtime Adapter](../opencode-runtime-adapter.md) |
| Modelos | `model_selection/` | [model_selection](../../src/vercosa_ai_framework/model_selection/README.md) | MVP | [0002](../../specs/framework/0002-model-selection-engine.md) | [Mapa de arquitetura](../alignment/architecture-map.md) |
| Contexto | `context/` | [context](../../src/vercosa_ai_framework/context/README.md) | MVP | [0014](../../specs/framework/0014-context-router-token-budget-memory.md) | [Context Router e Token Budget](../context-router-token-budget.md) |
| Conhecimento | `knowledge/` | [knowledge](../../src/vercosa_ai_framework/knowledge/README.md) | MVP | [0011](../../specs/framework/0011-knowledge-hub.md) | [Knowledge Hub](../knowledge-hub.md) |
| Canonicalização | `canonicalizer/` | [canonicalizer](../../src/vercosa_ai_framework/canonicalizer/README.md) | MVP | [0012](../../specs/framework/0012-canonicalizer.md) | [Canonicalizer](../canonicalizer.md) |
| Persistência | `persistence/` | [persistence](../../src/vercosa_ai_framework/persistence/README.md) | MVP | [0013](../../specs/framework/0013-persistence-layer.md) | [Persistence Layer](../persistence-layer.md) |

## Relações Principais

- `missions/` controla ciclo operacional de missões e deve delegar planejamento para `workflows/` quando a ponte estiver consolidada.
- `workflows/` define plano e execução sequencial MVP; `tasks/` concentra estado, elegibilidade e tentativas de tasks.
- `agents/` seleciona perfis e prepara execução, mas não chama tools, providers, MCPs ou bancos diretamente.
- `capabilities/`, `skills/`, `tools/` e `providers/` formam a cadeia de resolução de intenção até infraestrutura concreta.
- `guardian/` é transversal e avalia riscos, permissões, bloqueios e Context Packages já montados antes de ações sensíveis ou entrega governada.
- `model_selection/` é transversal e deve decidir modelos por política, não por hardcode.
- `context/` monta pacotes de contexto e aplica orçamento de tokens sem buscar, indexar, persistir, chamar providers diretamente ou decidir enforcement operacional.
- `knowledge/` organiza documentos, busca textual MVP e fornece adaptador determinístico para candidatos do Context Router; `canonicalizer/` prepara documentos canônicos antes de ingestão.
- `persistence/` oferece portas e adapters para durabilidade sem fixar storage específico.
- `runtime/` isola execução concreta em runtimes como OpenCode.

## Lacunas Registradas

As principais lacunas arquiteturais já estão listadas em [Perguntas em aberto](../alignment/open-questions.md), especialmente:

- fronteira entre Guardian Engine e Policy Engine;
- fronteira entre Mission Runner e Mission Orchestrator;
- integração completa Mission -> Workflow -> Task -> Agent -> Capability -> Skill -> Tool -> Provider;
- Context Router integrado aos fluxos de missão, agente, modelo, Guardian e recuperação governada completa do Knowledge Hub;
- Semantic Index e persistência final.
