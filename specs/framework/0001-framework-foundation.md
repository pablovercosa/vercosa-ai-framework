# Spec 0001 — Fundação do Vercosa AI Framework

## Status

Aprovada conceitualmente.

## Objetivo

Criar a fundação arquitetural do Vercosa AI Framework como um framework open source de desenvolvimento de software orientado por especificações e assistido por IA.

## Escopo

Esta Spec cobre:

- princípios do framework;
- arquitetura de alto nível;
- Guardian Specs;
- uso inicial do OpenCode;
- Knowledge Hub;
- Specification Providers;
- Canonicalizer;
- AI Orchestrator;
- Model Selection Engine;
- agentes;
- skills;
- MCPs;
- políticas;
- loops;
- execução por missões.

## Decisões já aprovadas

1. O projeto se chamará Vercosa AI Framework.
2. O framework será Specification First.
3. O framework será AI Native.
4. O framework será Provider Agnostic.
5. O framework será Local First.
6. O framework será Extensible by Design.
7. O OpenCode será o runtime inicial, mas não o núcleo.
8. Agentes não conhecerão MCPs diretamente.
9. O framework usará capabilities entre agentes e tools.
10. Specs podem vir de múltiplos providers.
11. Binários devem ser convertidos para Markdown canônico.
12. Guardian Specs governam todos os projetos.
13. Prompts devem ser substituídos por missões, workflows e loops sempre que possível.
14. Modelo de IA deve ser escolhido por política, não hardcoded.
15. O ambiente atual do usuário usa PostgreSQL + pgvector + Ollama, mas isso deve ser adapter.

## Critérios de aceite

- Existe AGENTS.md com contexto central.
- Existem documentos de visão.
- Existem princípios.
- Existe arquitetura central.
- Existem Guardian Specs iniciais.
- Existe estrutura de diretórios.
- OpenCode consegue ler este projeto e trabalhar com base nesses arquivos.

## Estado implementado e validado em 0108

As missões 0104 a 0107 validaram uma integração mínima local, determinística e injetável entre Mission Runner, Workflow Engine, Task Queue, Agent Orchestrator, Policy Engine, Context Router, Token Budget Manager, Guardian Engine, Model Selection, Capabilities, Skills, Tools, Provider Gateway em dry-run, Runtime Adapter e Audit/Event Log.

Evidências principais:

- `tests/test_mission_workflow_task_integration.py` valida Mission Runner -> Workflow Engine -> Task Queue com executor injetado e preserva caminho legado sem workflow.
- `tests/test_task_agent_capability_integration.py` valida Task Scheduler -> AgentTaskExecutor -> Agent Orchestrator -> Capability Resolver antes do runtime.
- `tests/test_capability_skill_tool_provider_dry_run.py` valida Capability -> Skill -> Tool -> Provider Gateway em `dry_run=True`, sem chamada a adapter concreto.
- `tests/test_agent_execution_governance_0107.py` valida o fluxo governado com Policy Engine, Context Router, Token Budget Manager, Guardian Engine, Model Selection e Audit/Event Log.

Esse estado não valida provider real, rede, banco, MCP, PostgreSQL, pgvector, RAG, memória global automática, múltiplos runtimes reais ou release alfa. Esses itens permanecem planejados ou pendentes conforme `docs/alignment/implementation-status.md` e `docs/alignment/open-questions.md`.
