# Vercosa AI Framework

Open source framework para desenvolvimento de software orientado por especificações e assistido por IA.

## Objetivo

O Vercosa AI Framework organiza engenharia de software em torno de Specs, missões, workflows, tarefas, agentes, capabilities, skills, tools, policies, Knowledge Hub, validação, auditoria e adapters substituíveis.

## O Que O Framework É

- Um framework Specification First para desenvolvimento assistido por IA.
- Uma arquitetura AI Native com governança, rastreabilidade e validação explícitas.
- Um núcleo provider agnostic para modelos, runtimes, bancos, vetores, IDEs, MCPs e APIs.
- Um conjunto de contratos e MVPs iniciais em Python para missão, workflow, task queue, agentes, Guardian, runtime, knowledge, context routing, token budget, canonicalização, providers e persistência.

## O Que O Framework Não É

- Não é um IDE.
- Não é um MCP server.
- Não é um único agente.
- Não é um wrapper de OpenCode, Claude Code, Codex CLI ou Cursor.
- Não é dependente de PostgreSQL, pgvector, Ollama, ARM64, systemd ou SSH.
- Não é uma coleção de prompts sem Specs, validação e governança.

## Estado Atual

Status: fundação arquitetural com MVPs e contratos iniciais.

As Specs em `specs/framework/` descrevem a arquitetura desejada. O código em `src/vercosa_ai_framework/` implementa partes mínimas e ainda não representa o fluxo completo de ponta a ponta.

## Runtime Inicial

OpenCode é o runtime e laboratório inicial. Ele deve permanecer atrás de adapter em `runtime/` e não define o núcleo do framework.

## Princípios

- Specification First
- AI Native
- Provider Agnostic
- Local First
- Extensible by Design
- Security by Design
- Token Efficiency
- Governance by Design

## Arquitetura Resumida

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

## Mapa De Módulos

O mapa navegável oficial está em [docs/architecture/module-index.md](docs/architecture/module-index.md).

Módulos principais:

- [core](src/vercosa_ai_framework/core/README.md)
- [missions](src/vercosa_ai_framework/missions/README.md)
- [workflows](src/vercosa_ai_framework/workflows/README.md)
- [tasks](src/vercosa_ai_framework/tasks/README.md)
- [agents](src/vercosa_ai_framework/agents/README.md)
- [capabilities](src/vercosa_ai_framework/capabilities/README.md)
- [guardian](src/vercosa_ai_framework/guardian/README.md)
- [skills](src/vercosa_ai_framework/skills/README.md)
- [tools](src/vercosa_ai_framework/tools/README.md)
- [providers](src/vercosa_ai_framework/providers/README.md)
- [runtime](src/vercosa_ai_framework/runtime/README.md)
- [model_selection](src/vercosa_ai_framework/model_selection/README.md)
- [context](src/vercosa_ai_framework/context/README.md)
- [knowledge](src/vercosa_ai_framework/knowledge/README.md)
- [canonicalizer](src/vercosa_ai_framework/canonicalizer/README.md)
- [persistence](src/vercosa_ai_framework/persistence/README.md)

## Estrutura Do Repositório

- `AGENTS.md`: contexto central para agentes e regras de colaboração.
- `specs/framework/`: Specs do framework.
- `docs/`: documentação técnica, alinhamento, arquitetura e guias.
- `docs/documentation/readme-standard.md`: padrão oficial de README.
- `docs/templates/readme-template.md`: template para novos READMEs.
- `src/vercosa_ai_framework/`: contratos e MVPs do framework.
- `knowledge/`: visão, princípios e arquitetura de referência.
- `.opencode/`: integração inicial com OpenCode.

## Specs Principais

- [Spec 0001: Framework Foundation](specs/framework/0001-framework-foundation.md)
- [Spec 0002: Model Selection Engine](specs/framework/0002-model-selection-engine.md)
- [Spec 0003: OpenCode Runtime Adapter](specs/framework/0003-opencode-runtime-adapter.md)
- [Spec 0004: Mission Runner](specs/framework/0004-mission-runner.md)
- [Spec 0005: Guardian Engine](specs/framework/0005-guardian-engine.md)
- [Spec 0006: Workflow Engine](specs/framework/0006-workflow-engine.md)
- [Spec 0007: Task Queue](specs/framework/0007-task-queue.md)
- [Spec 0008: Agent Orchestrator](specs/framework/0008-agent-orchestrator.md)
- [Spec 0009: Capabilities, Skills e Tools](specs/framework/0009-capabilities-skills-tools.md)
- [Spec 0010: Provider Gateway](specs/framework/0010-provider-gateway.md)
- [Spec 0011: Knowledge Hub](specs/framework/0011-knowledge-hub.md)
- [Spec 0012: Canonicalizer](specs/framework/0012-canonicalizer.md)
- [Spec 0013: Persistence Layer](specs/framework/0013-persistence-layer.md)
- [Spec 0014: Context Router, Token Budget Manager e Memory Architecture](specs/framework/0014-context-router-token-budget-memory.md)

## Documentação Técnica

- [Architecture Map](docs/alignment/architecture-map.md)
- [Current State](docs/alignment/current-state.md)
- [Open Questions](docs/alignment/open-questions.md)
- [SDD Lifecycle](docs/alignment/sdd-lifecycle.md)
- [Roadmap](docs/alignment/roadmap.md)
- [README Standard](docs/documentation/readme-standard.md)
- [Context Router And Token Budget](docs/context-router-token-budget.md)

## Regras De Trabalho

- Nenhum código deve ser implementado sem Spec aprovada.
- Documentação deve refletir o estado real do código e das Specs.
- Mudanças arquiteturais materiais devem gerar ADR, Spec update ou pergunta registrada.
- Agentes não devem chamar providers, MCPs, APIs, bancos ou filesystem diretamente.
- Links de documentação devem ser relativos.
