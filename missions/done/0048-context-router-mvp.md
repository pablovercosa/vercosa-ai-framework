Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- docs/documentation/readme-standard.md
- docs/architecture/module-index.md
- docs/context-router-token-budget.md
- knowledge/decisions/2026-07-04-policy-engine-vs-guardian-engine.md
- knowledge/decisions/2026-07-04-context-router-token-budget-memory-architecture.md
- specs/framework/0014-context-router-token-budget-memory.md
- src/vercosa_ai_framework/context/
- src/vercosa_ai_framework/context/README.md
- tests/test_context_contracts.py

Assuma o papel de python-implementation-agent e framework-architect.

Missão:
Implementar o MVP determinístico do Context Router e do Token Budget Manager.

Objetivo:
Expandir os contratos criados na missão 0046 para um MVP funcional, determinístico, sem LLM, sem provider externo, sem embeddings, sem pgvector e sem RAG real.

Entregáveis obrigatórios:
- atualizar src/vercosa_ai_framework/context/router.py
- atualizar src/vercosa_ai_framework/context/budget.py
- atualizar src/vercosa_ai_framework/context/types.py apenas se necessário
- atualizar src/vercosa_ai_framework/context/__init__.py se necessário
- criar ou atualizar tests/test_context_router_mvp.py
- atualizar tests/test_context_contracts.py se necessário
- atualizar docs/context-router-token-budget.md
- atualizar src/vercosa_ai_framework/context/README.md
- atualizar docs/architecture/module-index.md apenas se necessário

Requisitos funcionais:
1. O Context Router MVP deve aceitar uma ContextRequest e uma lista explícita de candidatos ContextItem.
2. Deve produzir um ContextPackage determinístico.
3. Deve preservar citations de itens selecionados.
4. Deve deduplicar itens por:
   - id do item, quando existir;
   - content_hash, quando existir;
   - conteúdo, como fallback.
5. Deve respeitar orçamento de tokens fornecido pelo TokenBudgetManager.
6. Deve omitir itens que excedam orçamento com ContextOmissionReason.TOKEN_BUDGET_EXCEEDED ou equivalente já definido.
7. Deve registrar motivos de omissão no ContextPackage.
8. Deve ordenar candidatos de forma determinística.
9. Deve aceitar prioridade/rank quando já existir no tipo.
10. Deve tratar itens sem citação como permitidos apenas se o tipo de item não exigir citação, mantendo warning quando apropriado.
11. Deve expor comportamento simples e testável, sem acoplamento com filesystem, banco, provider ou runtime.
12. Deve manter compatibilidade com os testes existentes.

Requisitos do Token Budget Manager MVP:
1. Estimar tokens de forma determinística e simples.
2. Calcular orçamento disponível para contexto após reserva de output.
3. Avaliar se um item cabe no orçamento restante.
4. Produzir decisão ou resultado contendo:
   - tokens estimados;
   - tokens reservados para output;
   - tokens disponíveis para contexto;
   - tokens usados;
   - tokens restantes;
   - itens aceitos;
   - itens omitidos, se aplicável.
5. Não chamar API externa.
6. Não usar dependência nova.

Requisitos de testes:
Criar testes cobrindo:
- roteamento com lista vazia de candidatos;
- seleção de item único;
- preservação de citação;
- deduplicação por hash;
- deduplicação por conteúdo;
- omissão por orçamento insuficiente;
- reserva de tokens de output;
- ordenação determinística;
- pacote final contendo omission reasons;
- comportamento repetível com mesma entrada;
- ausência de chamadas externas;
- compatibilidade com testes de contratos existentes.

Requisitos de documentação:
- documentação em português do Brasil;
- explicar claramente que ainda não há RAG real;
- explicar que ainda não há embeddings;
- explicar que ainda não há pgvector;
- explicar que o MVP trabalha com candidatos explícitos;
- atualizar README do módulo context com uso mínimo;
- manter links relativos corretos;
- não prometer memória infinita;
- documentar limitações e próximos passos.

Restrições:
- não implementar Semantic Index;
- não implementar embeddings;
- não implementar pgvector;
- não implementar PostgreSQL;
- não implementar RAG real;
- não adicionar dependências;
- não chamar Gemini, OpenAI, Ollama, Claude, OpenCode ou qualquer runtime;
- não executar providers externos;
- não acessar MCPs;
- não usar sudo;
- não alterar configs globais;
- não alterar módulos fora de context salvo documentação relacionada estritamente necessária;
- não prometer comportamento ainda não implementado;
- manter storage agnostic, provider agnostic, runtime agnostic e model agnostic;
- documentação e textos explicativos devem estar em português do Brasil.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar;
- git status deve mostrar apenas arquivos relacionados à missão antes do commit;
- documentação relacionada deve estar atualizada;
- não deve haver dependência externa nova;
- não deve haver chamada de rede.
