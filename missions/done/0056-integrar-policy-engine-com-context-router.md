Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- docs/architecture/module-index.md
- docs/context-router-token-budget.md
- docs/alignment/current-state.md
- docs/alignment/architecture-map.md
- docs/alignment/roadmap.md
- specs/framework/0014-context-router-token-budget-memory.md
- knowledge/decisions/2026-07-04-policy-engine-vs-guardian-engine.md
- knowledge/decisions/2026-07-04-context-router-token-budget-memory-architecture.md
- src/vercosa_ai_framework/policy/
- src/vercosa_ai_framework/policy/README.md
- src/vercosa_ai_framework/context/
- src/vercosa_ai_framework/context/README.md
- src/vercosa_ai_framework/guardian/
- tests/test_policy_engine_contracts.py
- tests/test_policy_guardian_integration.py
- tests/test_context_contracts.py
- tests/test_context_router_mvp.py
- tests/test_context_knowledge_integration.py

Assuma o papel de framework-architect, python-implementation-agent e test-engineer.

Missão:
Integrar Policy Engine com Context Router de forma inicial e determinística.

Objetivo:
Permitir que o Context Router considere um ResolvedPolicySet produzido pelo Policy Engine ao montar um ContextPackage, sem implementar RAG semântico, embeddings, pgvector, banco de dados, provider externo ou chamada de LLM.

Contexto:
- O Policy Engine resolve políticas declarativas.
- O Context Router monta ContextPackage a partir de candidatos explícitos.
- O Token Budget Manager controla orçamento de tokens.
- O Guardian Engine já pode considerar políticas resolvidas e avaliar ContextPackage.
- Nesta missão, o Context Router deve apenas considerar políticas resolvidas de forma simples, determinística e opcional.
- O Policy Engine não deve chamar o Context Router.
- O Context Router não deve resolver políticas; ele deve apenas receber políticas já resolvidas como entrada opcional.

Entregáveis obrigatórios:
- atualizar src/vercosa_ai_framework/context/ se necessário;
- atualizar src/vercosa_ai_framework/policy/ se necessário;
- criar tests/test_policy_context_router_integration.py;
- atualizar src/vercosa_ai_framework/context/README.md;
- atualizar src/vercosa_ai_framework/policy/README.md;
- atualizar docs/context-router-token-budget.md;
- atualizar docs/architecture/module-index.md se necessário;
- atualizar README.md se necessário.

Requisitos funcionais:
1. Inspecionar os contratos existentes do Policy Engine.
2. Inspecionar os contratos existentes do Context Router.
3. Criar integração opcional em que ContextRequest, ContextRouter ou estrutura equivalente possa receber um ResolvedPolicySet ou referência compatível.
4. Não quebrar chamadas existentes do Context Router.
5. Manter compatibilidade com testes existentes.
6. Reutilizar tipos existentes sempre que possível.
7. Não criar acoplamento circular.
8. Não fazer o Policy Engine chamar Context Router.
9. Não fazer o Context Router resolver políticas.
10. O Context Router pode considerar políticas resolvidas para:
    - gerar warnings;
    - registrar policy refs;
    - omitir itens quando houver política determinística de bloqueio;
    - exigir rastreabilidade quando política indicar;
    - respeitar restrições simples relacionadas a contexto, se já houver campos adequados.
11. Políticas com efeito allow não devem, por si só, alterar o pacote de contexto.
12. Políticas com efeito warn podem gerar warning no ContextPackage ou estrutura equivalente.
13. Políticas com efeito require_approval podem marcar o pacote como exigindo revisão, se houver campo apropriado; se não houver, registrar warning/metadata sem criar grande refatoração.
14. Políticas com efeito deny/block podem omitir item ou gerar sinalização de bloqueio, somente se a regra for clara e determinística.
15. Conflitos de política podem gerar warning ou require_approval, conforme tipos existentes.
16. Manter comportamento determinístico.
17. Não implementar DSL.
18. Não implementar parser de política.
19. Não implementar busca semântica.
20. Não chamar LLM.
21. Não chamar provider externo.
22. Não acessar rede.
23. Não acessar banco.

Requisitos de testes:
Criar testes cobrindo:
- Context Router sem ResolvedPolicySet mantém comportamento atual;
- política allow não bloqueia nem altera indevidamente o pacote;
- política warn é refletida em warning/metadata/policy refs;
- política require_approval é refletida de forma rastreável;
- política block/deny causa omissão ou sinalização quando aplicável;
- conflito de política é considerado de forma determinística;
- orçamento de tokens continua funcionando;
- citations continuam preservadas;
- omission reasons continuam preservadas;
- comportamento repetível com mesma entrada;
- ausência de chamada externa;
- sem acoplamento circular evidente;
- testes existentes continuam passando.

Requisitos de documentação:
- tudo em português do Brasil;
- explicar que Policy Engine resolve políticas;
- explicar que Context Router apenas consome políticas resolvidas;
- explicar que a integração é inicial;
- explicar que não há DSL;
- explicar que não há RAG semântico;
- explicar que não há embeddings;
- explicar que não há pgvector;
- explicar que não há provider externo;
- explicar limites atuais e próximos passos;
- manter links relativos corretos;
- não prometer comportamento ainda não implementado.

Regra de commit automático:
Se esta missão gerar commit automático, a mensagem deve estar em português do Brasil.
Usar a mensagem fornecida por VAF_COMMIT_MESSAGE quando existir.

Restrições:
- não adicionar dependências;
- não implementar Policy Engine completo;
- não alterar arquitetura para acoplamento forte;
- não implementar RAG;
- não implementar embeddings;
- não implementar pgvector;
- não chamar Gemini, OpenAI, Ollama, Claude, OpenCode ou qualquer runtime;
- não acessar MCPs;
- não usar sudo;
- não alterar configs globais;
- não reescrever histórico Git;
- não fazer force push;
- documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- testes novos existem e passam;
- pytest passa;
- python3 -m compileall src passa;
- documentação relacionada é atualizada;
- auto-commit usa mensagem em português do Brasil.
