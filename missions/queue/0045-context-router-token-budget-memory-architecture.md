Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/alignment/current-state.md
- docs/alignment/architecture-map.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/alignment/alignment-review-2026-07-03.md
- docs/alignment/sdd-lifecycle.md
- docs/architecture/module-index.md
- docs/documentation/readme-standard.md
- knowledge/decisions/2026-07-04-policy-engine-vs-guardian-engine.md
- specs/framework/0002-model-selection-engine.md
- specs/framework/0005-guardian-engine.md
- specs/framework/0008-agent-orchestrator.md
- specs/framework/0011-knowledge-hub.md
- specs/framework/0012-canonicalizer.md
- specs/framework/0013-persistence-layer.md
- src/vercosa_ai_framework/knowledge/
- src/vercosa_ai_framework/canonicalizer/
- src/vercosa_ai_framework/persistence/
- src/vercosa_ai_framework/model_selection/
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/agents/

Assuma o papel de framework-architect.

Missão:
Criar uma ADR/Spec conceitual para Context Router, Token Budget Manager e arquitetura de memória do Vercosa AI Framework.

Entregáveis obrigatórios:
- knowledge/decisions/2026-07-04-context-router-token-budget-memory-architecture.md
- specs/framework/0014-context-router-token-budget-memory.md

Objetivo:
Definir a arquitetura de contexto, memória e otimização de tokens antes de qualquer implementação funcional de Context Router, Token Budget Manager, Semantic Index, embeddings, pgvector ou RAG.

A ADR deve conter:
1. Título.
2. Status da decisão.
3. Contexto.
4. Problema.
5. Decisão.
6. Justificativa.
7. Definição de Context Router.
8. Definição de Token Budget Manager.
9. Definição de Context Package.
10. Definição de Memory Architecture.
11. Diferença entre memória infinita, memória persistente, memória semântica, Knowledge Hub, Semantic Index e Context Router.
12. Responsabilidades do Context Router.
13. Responsabilidades que NÃO pertencem ao Context Router.
14. Responsabilidades do Token Budget Manager.
15. Responsabilidades que NÃO pertencem ao Token Budget Manager.
16. Relação com Policy Engine.
17. Relação com Guardian Engine.
18. Relação com Knowledge Hub.
19. Relação com Canonicalizer.
20. Relação com Persistence Layer.
21. Relação com Model Selection Engine.
22. Relação com Agent Orchestrator, Capabilities, Skills, Tools e Providers.
23. Relação com SDD: Spec, Plan, Tasks, Implement, Validate e Commit.
24. Estratégia de token efficiency.
25. Estratégia de redaction e contexto sensível.
26. Estratégia de citações e rastreabilidade.
27. Estratégia de cache, hash e reutilização de contexto.
28. Estratégia futura para Semantic Index, embeddings e pgvector.
29. O que não deve ser implementado ainda.
30. Consequências positivas.
31. Consequências negativas.
32. Riscos.
33. Checklist para próximas missões.

A Spec 0014 deve conter:
1. Visão geral.
2. Objetivos.
3. Não objetivos.
4. Componentes:
   - Context Router
   - Token Budget Manager
   - Context Package
   - Context Source
   - Context Item
   - Context Citation
   - Context Redaction
   - Context Omission Reason
   - Context Policy Reference
   - Memory Layer
5. Fluxo esperado:
   Mission/Task/Agent Request
   -> Policy Engine
   -> Context Router
   -> Knowledge Hub / Canonicalizer / Persistence / future Semantic Index
   -> Token Budget Manager
   -> Guardian Engine
   -> Model Selection Engine
   -> Runtime Adapter.
6. Contratos conceituais.
7. Estados e decisões.
8. Regras de segurança.
9. Regras de token efficiency.
10. Regras de rastreabilidade.
11. Regras de storage agnostic.
12. Regras para não acoplar a pgvector, PostgreSQL, Ollama, OpenCode, Claude Code, LangGraph, AutoGen, MetaGPT, ECC ou Hermes.
13. Critérios de aceitação para futura implementação.
14. Testes esperados para futura implementação.
15. Pendências.

Direção arquitetural esperada:
- Não prometer "memória infinita".
- Definir memória como arquitetura em camadas.
- Context Router seleciona, compõe e justifica contexto.
- Token Budget Manager estima, reserva e limita orçamento de tokens.
- Knowledge Hub armazena e recupera conhecimento canônico.
- Canonicalizer converte fontes para forma canônica.
- Persistence Layer persiste artefatos, decisões e pacotes.
- Semantic Index é futuro adapter/índice derivado, não requisito obrigatório.
- pgvector é adapter futuro opcional, não default.
- Guardian avalia risco operacional do pacote de contexto.
- Policy Engine resolve políticas declarativas antes da seleção/entrega de contexto.
- Model Selection usa requisitos de contexto/tokens para selecionar modelo compatível.
- Context Package deve conter itens, fontes, citações, estimativas de tokens, redactions, omitted context reasons e policy refs.

Regras:
- não implementar código;
- não alterar src/;
- não alterar testes;
- não alterar configs globais;
- não usar sudo;
- não criar novas features executáveis;
- não adicionar dependências;
- não prometer comportamento já implementado se for apenas arquitetura futura;
- se encontrar inconsistências, registrar apenas dentro dos entregáveis desta missão.
