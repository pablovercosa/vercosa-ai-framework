# Estado Atual

Links principais: [README principal](../../README.md) | [Checklist canônico de implementação](implementation-status.md) | [Mapa de arquitetura](architecture-map.md) | [Roadmap](roadmap.md) | [Perguntas em aberto](open-questions.md) | [Revisão pós-integrações](../architecture/post-integration-architecture-review.md)

## Objetivo

Registrar uma fotografia narrativa e resumida do estado atual do Vercosa AI Framework após as integrações mínimas concluídas até a missão 0107, a revisão de Specs/ADRs da missão 0108 e a consolidação documental da missão 0109.

Este documento não é checklist operacional. O checklist factual canônico de itens planejados, implementados, integrados, validados, parciais, adiados, fora de escopo e em revisão fica em [implementation-status.md](implementation-status.md).

## Classificação Geral

Status: MVP operacional inicial com fundação arquitetural e contratos em evolução.

A classificação de alinhamento registrada pela auditoria 0101 permanece `ALINHADO COM RESSALVAS`. A auditoria está em [docs/audits/objective-and-scope-alignment-audit.md](../audits/objective-and-scope-alignment-audit.md).

## O Que O Framework É

O Vercosa AI Framework é um framework open source de Harness Engineering para agentes de IA, desenvolvimento de software orientado por especificações e execução governada assistida por IA.

Seu objetivo central é organizar a camada operacional ao redor de modelos e agentes em torno de missões, Specs, workflows, políticas, agentes, capabilities, contexto, orçamento de tokens, conhecimento, validação, auditoria e adapters agnósticos de provider, runtime e storage.

## O Que O Framework Não É

O framework não é um IDE, MCP server, agente único, wrapper de OpenCode, coleção de prompts ou produto dependente de PostgreSQL, pgvector, Ollama, ARM64, systemd ou SSH.

OpenCode é atualmente runtime e laboratório inicial. Ele não é o centro arquitetural.

## Estado Resumido Do Repositório

O repositório possui uma base operacional local para executar missões controladas, validar batches seguros, diagnosticar estado básico pela CLI, registrar eventos auditáveis opcionais e documentar arquitetura, operação, release e governança.

Os módulos Python existem como contratos, MVPs ou integrações iniciais. A lista navegável de módulos, status, Specs e relações arquiteturais fica em [docs/architecture/module-index.md](../architecture/module-index.md).

As Specs normativas ficam em [specs/framework](../../specs/framework/). Decisões arquiteturais aceitas ficam em [docs/architecture/decisions](../architecture/decisions/). Perguntas ainda abertas ficam em [open-questions.md](open-questions.md).

## Capacidades Principais No Checkpoint Atual

Resumo narrativo:

- operação local por missões, runners seguros e batch governado;
- CLI diagnóstica e comandos de leitura local;
- contratos e MVPs dos motores centrais do framework;
- integrações mínimas locais entre Mission Runner, Workflow Engine, Task Queue, Agent Orchestrator, Capability Resolver, Skills, Tools, Provider Gateway em dry-run, Policy, Context, Token Budget, Guardian, Model Selection e Audit/Event Log;
- documentação operacional, arquitetura, release, segurança, contribuição e histórico inicial.

Detalhes factuais e evidências por código/teste ficam exclusivamente em [implementation-status.md](implementation-status.md).

## Limitações Principais

O estado atual ainda não valida provider real, rede, banco, MCP, API externa, RAG, PostgreSQL, pgvector, Semantic Index, múltiplos runtimes reais, observabilidade externa, release alfa publicada, tag, pacote publicado ou prontidão de produção.

A documentação de release preserva registros históricos importantes:

- validação de instalação limpa em 2026-07-10: `REPROVADO` em [clean-install-validation.md](../release/clean-install-validation.md);
- diagnóstico local de prontidão alfa em 2026-07-11: `NÃO PRONTO` em [alpha-readiness-diagnostic.md](../release/alpha-readiness-diagnostic.md);
- checklist pré-tag local em 2026-07-11: `REPROVADO` em [pre-tag-checklist-execution.md](../release/pre-tag-checklist-execution.md).
- reavaliação de prontidão alfa em 2026-07-15: `NÃO PRONTO` em [alpha-readiness-reassessment-0110.md](../release/alpha-readiness-reassessment-0110.md), apesar dos avanços de integração mínima, testes locais, compileall, documentação canônica e CI informado para a missão 0109.

Esses registros são históricos e não devem ser reescritos para parecer atuais. O estado factual vivo fica em [implementation-status.md](implementation-status.md).

## Estado De Versionamento E Release

A versão alfa inicial planejada é `0.1.0-alpha.1`, com tag futura planejada `v0.1.0-alpha.1`.

Esse estado é apenas documental:

- não há release alfa publicada;
- não há tag Git criada para alfa;
- não há GitHub Release publicada;
- não há pacote PyPI publicado;
- não há garantia de estabilidade de produção;
- não há promessa de compatibilidade de API.

Antes de qualquer publicação, ainda são necessárias validações aplicáveis, resolução ou aceitação explícita de bloqueios, confirmação de CI remoto quando houver push, decisão explícita de tag/release e revisão das pendências de licença, instalação limpa e distribuição.

## Responsabilidade Documental

Este documento resume o checkpoint atual. Ele não deve manter catálogo completo de módulos, integrações, testes, lacunas ou pendências.

Fontes relacionadas:

- checklist factual: [implementation-status.md](implementation-status.md);
- topologia e fronteiras: [architecture-map.md](architecture-map.md);
- direção estratégica: [roadmap.md](roadmap.md);
- backlog estratégico: [docs/roadmap/mission-backlog.md](../roadmap/mission-backlog.md);
- histórico de missões: [docs/history/mission-milestones.md](../history/mission-milestones.md);
- histórico de mudanças: [CHANGELOG.md](../../CHANGELOG.md);
- auditorias datadas: [docs/audits](../audits/);
- evidências de release: [docs/release](../release/).

## Recomendação De Alinhamento

Antes de novas implementações, manter o vocabulário arquitetural explícito, preservar Specification First, evitar acoplamento a providers ou infraestrutura específica e escolher próximos blocos a partir do roadmap e do backlog estratégico, sem tratar documentação como prova de implementação.
