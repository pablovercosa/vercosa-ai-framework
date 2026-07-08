# Vercosa AI Framework

O Vercosa AI Framework é um framework open source de Harness Engineering para agentes de IA, desenvolvimento orientado por especificações e execução governada de software.

O projeto não trata o modelo de IA como o sistema inteiro. O modelo é apenas uma peça substituível dentro de uma camada operacional que organiza missões, runners, contexto, orçamento de tokens, políticas, guardrails, auditoria, seleção de modelos, providers, runtimes, validações e CLI operacional.

## Objetivo

Permitir que pessoas e agentes executem trabalho de engenharia de software de forma rastreável, segura e reproduzível, mantendo Specs, missões, workflows, tasks, agentes, capabilities, skills, tools, policies, Knowledge Hub, validações e adapters substituíveis sob uma arquitetura coerente.

## Prompt Engineering, Agent Framework E Harness Engineering

- Prompt Engineering foca em instruções, exemplos e formato de entrada para melhorar a resposta de um modelo.
- Agent Framework foca em agentes, ferramentas, memória, planejamento e execução automatizada de tarefas.
- Harness Engineering foca na camada operacional ao redor dos agentes e modelos: execução governada, limites, políticas, auditoria, validação, rastreabilidade, orquestração, adaptação de runtimes e integração segura com providers.

O VAF se posiciona como Harness Engineering: ele organiza o ambiente em que agentes de IA trabalham, em vez de depender apenas de prompts ou de um agente monolítico.

## O Que O Framework É

- Um framework Specification First para desenvolvimento assistido por IA.
- Uma arquitetura AI Native para execução governada, rastreabilidade, segurança operacional, evolução por missões, separação de responsabilidades, testes e documentação progressiva.
- Um harness model agnostic, provider agnostic, runtime agnostic e storage agnostic como direção arquitetural.
- Um conjunto de contratos e MVPs em Python para Mission Runner, Workflow Engine, Task Queue, Agent Orchestrator, Policy Engine, Guardian Engine, Usage/API Limit Guard, Audit/Event Log, Context Router, Token Budget Manager, Knowledge Hub, Model Selection Engine, Runtime Adapter, Provider Gateway, CLI operacional e adapters iniciais.

## O Que O Framework Não É

- Não é um IDE.
- Não é um MCP server.
- Não é um único agente.
- Não é apenas um wrapper de OpenCode, Claude Code, Codex CLI, Cursor ou outro runtime.
- Não é dependente de PostgreSQL, pgvector, Ollama, ARM64, systemd ou SSH.
- Não é uma coleção de prompts sem Specs, validação e governança.

## Estado Atual

Status: MVP operacional inicial com fundação arquitetural e contratos em evolução.

As Specs em `specs/framework/` descrevem a arquitetura desejada. O código em `src/vercosa_ai_framework/` implementa MVPs determinísticos e integrações iniciais, mas o fluxo completo Mission -> Workflow -> Task -> Agent -> Capability -> Skill -> Tool -> Provider ainda não está integrado de ponta a ponta.

Implementado em estado MVP ou contrato inicial:

- Mission Runner local, fila em diretórios e integração opcional com eventos auditáveis em Python.
- Runner seguro de uma missão e runner seguro em batch por scripts operacionais.
- Policy Engine declarativo e Guardian Engine determinístico.
- Usage/API Limit Guard para classificar sinais textuais de limite externo em logs já recebidos.
- Context Router, Token Budget Manager e `ContextPackage` determinísticos.
- Knowledge Hub com ingestão Markdown, store em memória, busca textual e adaptação para candidatos de contexto.
- Model Selection Engine com catálogo em memória, políticas resolvidas opcionais e requisitos opcionais de orçamento de tokens.
- Runtime Adapter inicial para OpenCode.
- Provider Gateway, Tools, Skills, Capabilities e Agent Orchestrator como cadeia MVP de contratos.
- Audit/Event Log em memória com helpers opcionais para decisões e ciclo de vida de missão.
- CLI operacional inicial com `status`, `validate` e `doctor`.

Ainda são futuros ou lacunas:

- RAG semântico.
- Embeddings.
- pgvector como adapter real.
- Semantic Index.
- Múltiplos providers reais.
- Persistência externa de eventos.
- Internacionalização dos READMEs.

Esses recursos não devem ser interpretados como implementados no estado atual.

## Runtime Inicial

OpenCode é o runtime e laboratório inicial. Ele permanece atrás de adapter em `runtime/` e não define o núcleo do framework. O VAF deve poder suportar outros runtimes e interfaces no futuro sem transformar nenhum deles no centro arquitetural.

## Arquitetura Resumida

Fluxo conceitual principal:

```text
Mission Runner
↓
Workflow Engine
↓
Task Queue
↓
Agent Orchestrator
↓
Capabilities
↓
Skills
↓
Tools
↓
Provider Gateway
↓
Runtime Adapter / Providers / MCPs / APIs
```

Eixo de governança:

- Policy Engine resolve políticas declarativas.
- Guardian Engine avalia ações concretas, riscos e pacotes de contexto.
- Usage/API Limit Guard classifica sinais textuais de limite externo.
- Audit/Event Log registra eventos estruturados quando um `EventLog` é fornecido.

Eixo de contexto e memória:

- Knowledge Hub organiza documentos textuais e busca textual MVP.
- Context Router monta `ContextPackage` a partir de candidatos explícitos.
- Token Budget Manager estima orçamento de tokens de forma determinística.
- `ContextPackage` preserva itens selecionados, omissões, citações, warnings, refs de política e requisitos mínimos para seleção de modelo.

Eixo operacional:

- Runner seguro de uma missão: `scripts/vaf-run-next-safe.sh`.
- Runner seguro em batch: `scripts/vaf-run-batch-safe.sh`.
- CLI operacional: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main status|validate|doctor`.
- Playbooks e checklists documentam execução, validação e revisão pós-batch.

## Fluxo Operacional Padrão

O fluxo operacional padrão do projeto é executar missões em batch quando o bloco em `missions/queue/` estiver bem especificado, revisado e seguro. O batch continua usando missões completas em Markdown, uma missão por arquivo, escopo claro, restrições explícitas, critérios de aceite verificáveis, commits separados, parada na primeira falha, validação pós-batch e push manual por padrão.

Use `VAF_BATCH_SIZE=10` para blocos normais já revisados. Use `VAF_BATCH_SIZE=3` para testes, retomadas, blocos pequenos ou recuperação. Use `./scripts/vaf-run-next-safe.sh` para missões sensíveis, arquiteturais, incertas, de alto risco, investigação de erro ou recuperação após falha.

`VAF_AUTO_PUSH=1` continua sendo opt-in. A prática recomendada é validar o batch com o checklist operacional e fazer push manual somente depois de revisar estado das missões, testes, `compileall`, Git e commits.

## Mapa De Módulos

O mapa navegável oficial está em [docs/architecture/module-index.md](docs/architecture/module-index.md).

Módulos principais:

- [cli](src/vercosa_ai_framework/cli/README.md)
- [core](src/vercosa_ai_framework/core/README.md)
- [missions](src/vercosa_ai_framework/missions/README.md)
- [workflows](src/vercosa_ai_framework/workflows/README.md)
- [tasks](src/vercosa_ai_framework/tasks/README.md)
- [agents](src/vercosa_ai_framework/agents/README.md)
- [capabilities](src/vercosa_ai_framework/capabilities/README.md)
- [policy](src/vercosa_ai_framework/policy/README.md)
- [guardian](src/vercosa_ai_framework/guardian/README.md)
- [audit](src/vercosa_ai_framework/audit/README.md)
- [context](src/vercosa_ai_framework/context/README.md)
- [model_selection](src/vercosa_ai_framework/model_selection/README.md)
- [knowledge](src/vercosa_ai_framework/knowledge/README.md)
- [canonicalizer](src/vercosa_ai_framework/canonicalizer/README.md)
- [skills](src/vercosa_ai_framework/skills/README.md)
- [tools](src/vercosa_ai_framework/tools/README.md)
- [providers](src/vercosa_ai_framework/providers/README.md)
- [runtime](src/vercosa_ai_framework/runtime/README.md)
- [persistence](src/vercosa_ai_framework/persistence/README.md)

## Estrutura Do Repositório

- `AGENTS.md`: contexto central para agentes e regras de colaboração.
- `specs/framework/`: Specs do framework.
- `docs/`: documentação técnica, alinhamento, arquitetura, operações e exemplos.
- `src/vercosa_ai_framework/`: contratos e MVPs do framework.
- `knowledge/`: visão, princípios, arquitetura de referência e ADRs.
- `.opencode/`: integração inicial com OpenCode como laboratório/runtime.

## Operação Local

Scripts operacionais:

- `./scripts/vaf-run-next-safe.sh`: executa uma missão com validações antes e depois.
- `./scripts/vaf-run-batch-safe.sh`: executa um batch sequencial seguro e para na primeira falha.
- `./scripts/vaf-status.sh`: mostra estado operacional dos diretórios de missão.

CLI inicial:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main status
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor
```

A CLI não substitui `pytest`, `python3 -m compileall src`, os scripts seguros ou revisão humana quando a política exigir.

## Documentação Relevante

- [Índice de módulos](docs/architecture/module-index.md)
- [Backlog estratégico de missões](docs/roadmap/mission-backlog.md)
- [Playbook de execução em batch](docs/operations/batch-execution-playbook.md)
- [Checklist de validação pós-batch](docs/operations/post-batch-validation-checklist.md)
- [Exemplos operacionais](docs/examples/README.md)
- [Estado atual](docs/alignment/current-state.md)
- [Roadmap](docs/alignment/roadmap.md)
- [Padrão de README](docs/documentation/readme-standard.md)
- [Padrão de idioma e commits](docs/documentation/language-and-commit-standard.md)
- [Política de atualização de documentação](docs/documentation/documentation-update-policy.md)

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

## Princípios

- Specification First
- AI Native
- Provider Agnostic
- Local First
- Extensible by Design
- Security by Design
- Token Efficiency
- Governance by Design

## Idioma E Commits

O idioma oficial da documentação do projeto é português do Brasil. Termos técnicos e nomes arquiteturais consolidados podem permanecer em inglês quando fizerem parte da API, arquitetura ou vocabulário do framework.

Mensagens de commit futuras devem usar português do Brasil. O histórico Git já publicado não deve ser reescrito apenas para traduzir mensagens antigas.

## Regras De Trabalho

- Nenhum código deve ser implementado sem Spec aprovada.
- Documentação deve refletir o estado real do código e das Specs.
- Recursos futuros devem ser marcados como futuros, lacunas ou próximos passos.
- Agentes não devem chamar providers, MCPs, APIs, bancos ou filesystem diretamente; agentes solicitam capabilities.
- Links de documentação devem ser relativos.
- Mudanças arquiteturais materiais devem gerar ADR, Spec update ou pergunta registrada.
