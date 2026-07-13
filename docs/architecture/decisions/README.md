# Decisões Arquiteturais

Links principais: [README principal](../../../README.md) | [Índice de módulos](../module-index.md) | [Revisão pós-integrações](../post-integration-architecture-review.md) | [Status de implementação](../../alignment/implementation-status.md) | [Perguntas em aberto](../../alignment/open-questions.md)

## Objetivo

Registrar decisões arquiteturais aceitas, provisórias, substituídas, rejeitadas ou em avaliação para o Vercosa AI Framework.

## Responsabilidades

- Documentar decisões já apoiadas por Specs, código e testes.
- Diferenciar decisão aceita de decisão pendente.
- Apontar para evidências executáveis quando uma decisão depender de implementação.
- Evitar tratar documentação como prova de implementação.

## Não Responsabilidades

- Criar implementação.
- Autorizar provider real, rede, banco, MCP, RAG, release, tag ou pacote.
- Substituir Specs, checklist canônico de implementação ou perguntas em aberto.

## Padrão

Cada ADR deve usar número estável, título claro, estado, contexto, decisão, consequências, evidências e decisões ainda pendentes.

Estados permitidos nesta pasta:

- Aceita.
- Provisória.
- Substituída.
- Rejeitada.
- Em avaliação.

## Decisões Da Revisão 0108

- [ADR 0001: Separar Mission Runner, Workflow Engine e Task Queue](0001-separar-mission-runner-workflow-engine-task-queue.md)
- [ADR 0002: Usar AgentTaskExecutor como ponte desacoplada](0002-agent-task-executor-como-ponte-desacoplada.md)
- [ADR 0003: Separar resolução e execução de Capability](0003-separar-resolucao-e-execucao-de-capability.md)
- [ADR 0004: Usar Provider Gateway em dry-run sem adapter concreto](0004-provider-gateway-dry-run-sem-adapter-concreto.md)
- [ADR 0005: Separar Policy Engine, Guardian Engine e governança injetável](0005-policy-guardian-governanca-injetavel.md)
- [ADR 0006: Propagar ContextPackage para Model Selection e Audit/Event Log observador](0006-contextpackage-model-selection-audit-observador.md)
- [ADR 0007: Manter compatibilidade legada por configuração explícita](0007-compatibilidade-legada-por-configuracao-explicita.md)

## Status

MVP documental. Esta pasta registra decisões arquiteturais sem criar novo comportamento de runtime.
