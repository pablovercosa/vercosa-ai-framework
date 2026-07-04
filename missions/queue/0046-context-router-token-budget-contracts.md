Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/alignment/current-state.md
- docs/alignment/architecture-map.md
- docs/alignment/roadmap.md
- docs/alignment/alignment-review-2026-07-03.md
- docs/architecture/module-index.md
- docs/documentation/readme-standard.md
- knowledge/decisions/2026-07-04-policy-engine-vs-guardian-engine.md
- knowledge/decisions/2026-07-04-context-router-token-budget-memory-architecture.md
- specs/framework/0014-context-router-token-budget-memory.md
- src/vercosa_ai_framework/knowledge/
- src/vercosa_ai_framework/canonicalizer/
- src/vercosa_ai_framework/persistence/
- src/vercosa_ai_framework/model_selection/
- src/vercosa_ai_framework/guardian/

Assuma o papel de framework-architect e python-implementation-agent.

Missão:
Implementar os contratos iniciais do Context Router e do Token Budget Manager.

Objetivo:
Criar apenas tipos, portas e estruturas determinísticas iniciais para contexto, memória e orçamento de tokens, seguindo a Spec 0014.

Entregáveis obrigatórios:
- src/vercosa_ai_framework/context/__init__.py
- src/vercosa_ai_framework/context/types.py
- src/vercosa_ai_framework/context/router.py
- src/vercosa_ai_framework/context/budget.py
- tests/test_context_contracts.py
- docs/context-router-token-budget.md
- src/vercosa_ai_framework/context/README.md

Requisitos de implementação:
1. Criar pacote `context`.
2. Criar enums/tipos conceituais para:
   - ContextSourceType
   - ContextItemType
   - ContextOmissionReason
   - ContextRiskLevel
   - MemoryLayerType
3. Criar dataclasses ou estruturas equivalentes para:
   - ContextSource
   - ContextCitation
   - ContextRedaction
   - ContextItem
   - ContextPackage
   - ContextRequest
   - TokenBudget
   - TokenEstimate
   - TokenBudgetDecision
   - MemoryLayer
4. Criar porta/contrato abstrato de ContextRouter.
5. Criar implementação simples determinística `DeterministicContextRouter` ou equivalente.
6. Criar porta/contrato abstrato de TokenBudgetManager.
7. Criar implementação simples determinística `SimpleTokenBudgetManager` ou equivalente.
8. O roteador inicial deve:
   - receber uma ContextRequest;
   - aceitar candidatos explícitos de contexto;
   - deduplicar por hash/id quando possível;
   - respeitar limite básico de tokens estimados;
   - registrar omission reasons;
   - preservar citations;
   - produzir ContextPackage;
   - não chamar LLM;
   - não chamar provider externo;
   - não fazer embeddings;
   - não fazer RAG real;
   - não acessar banco;
   - não acessar filesystem salvo se já houver padrão interno seguro.
9. O TokenBudgetManager inicial deve:
   - estimar tokens de forma simples e determinística;
   - aceitar orçamento máximo;
   - reservar tokens de saída;
   - calcular tokens disponíveis para contexto;
   - indicar se um item cabe ou deve ser omitido;
   - nunca chamar API externa.
10. Criar testes cobrindo:
   - criação de ContextSource;
   - criação de ContextCitation;
   - criação de ContextItem;
   - criação de ContextPackage;
   - deduplicação simples;
   - limite de orçamento;
   - omission reason por token_budget_exceeded;
   - preservação de citations;
   - cálculo de output reservation;
   - comportamento determinístico.
11. Criar documentação clara e linkada:
   - docs/context-router-token-budget.md
   - src/vercosa_ai_framework/context/README.md
12. Atualizar README.md principal e docs/architecture/module-index.md se necessário para incluir o novo módulo `context/`.

Restrições:
- não implementar Semantic Index;
- não implementar embeddings;
- não implementar pgvector;
- não implementar PostgreSQL;
- não implementar RAG;
- não adicionar dependências;
- não chamar Gemini, OpenAI, Ollama, Claude, OpenCode ou qualquer runtime;
- não alterar configs globais;
- não usar sudo;
- não criar execução automática de providers;
- não prometer memória infinita;
- não alterar módulos existentes desnecessariamente;
- manter storage agnostic, provider agnostic, runtime agnostic e model agnostic.

Critérios de aceite:
- `pytest` deve passar;
- `python3 -m compileall src` deve passar;
- o novo módulo deve ter README.md seguindo docs/documentation/readme-standard.md;
- docs devem explicar claramente que esta missão cria contratos/MVP determinístico, não RAG funcional;
- o código deve ser simples, legível e sem dependência externa.
