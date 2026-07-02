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
