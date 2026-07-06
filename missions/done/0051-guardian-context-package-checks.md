Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- docs/architecture/module-index.md
- specs/framework/0005-guardian-engine.md
- specs/framework/0014-context-router-token-budget-memory.md
- knowledge/decisions/2026-07-04-policy-engine-vs-guardian-engine.md
- knowledge/decisions/2026-07-04-context-router-token-budget-memory-architecture.md
- docs/context-router-token-budget.md
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/guardian/README.md
- src/vercosa_ai_framework/context/
- src/vercosa_ai_framework/context/README.md
- tests/test_context_contracts.py
- tests/test_context_router_mvp.py
- tests/test_context_knowledge_integration.py

Assuma o papel de python-implementation-agent, security-architect e framework-architect.

Missão:
Adicionar verificações iniciais do Guardian Engine para ContextPackage.

Objetivo:
Permitir que o Guardian Engine avalie riscos básicos de um ContextPackage produzido pelo Context Router, sem chamar LLM, sem provider externo, sem rede, sem RAG semântico e sem alterar o fluxo principal de execução.

Contexto:
- O Context Router monta ContextPackage.
- O Token Budget Manager controla limites de tokens.
- O Knowledge Hub já pode fornecer candidatos de contexto por integração determinística.
- O Guardian Engine deve avaliar riscos operacionais e de segurança.
- O Policy Engine ainda não existe como camada separada completa.
- Nesta fase, o Guardian pode fazer validações determinísticas simples sobre ContextPackage.

Entregáveis obrigatórios:
- atualizar src/vercosa_ai_framework/guardian/ se necessário;
- atualizar src/vercosa_ai_framework/context/ apenas se necessário;
- criar tests/test_guardian_context_package_checks.py;
- atualizar src/vercosa_ai_framework/guardian/README.md;
- atualizar src/vercosa_ai_framework/context/README.md se necessário;
- atualizar docs/context-router-token-budget.md;
- atualizar docs/architecture/module-index.md se necessário.

Requisitos funcionais:
1. Inspecionar os tipos existentes do Guardian Engine antes de implementar.
2. Inspecionar os tipos existentes do ContextPackage antes de implementar.
3. Criar verificações determinísticas para ContextPackage.
4. As verificações devem detectar, quando aplicável:
   - item sem citação ou referência rastreável;
   - fonte desconhecida ou pouco confiável;
   - pacote com warnings relevantes;
   - pacote com redactions pendentes ou suspeitas;
   - orçamento de tokens excedido ou inconsistente;
   - ausência de hash ou rastreabilidade quando o tipo exigir;
   - conteúdo marcado como sensível, se já houver tipo/campo para isso;
   - omission reasons críticos.
5. As verificações devem retornar decisões compatíveis com o Guardian Engine existente.
6. Se já houver enum de decisão como allow/warn/block/require_approval, reutilizar.
7. Se não houver tipo adequado, criar extensão mínima e compatível.
8. Não criar Policy Engine nesta missão.
9. Não misturar responsabilidades: Context Router monta contexto; Guardian avalia risco.
10. Não bloquear tudo por padrão; usar decisão proporcional:
    - allow para pacote seguro;
    - warn para risco moderado;
    - require_approval para risco que exige revisão humana;
    - block apenas para risco claro e determinístico.
11. Manter comportamento determinístico e testável.

Requisitos de testes:
Criar testes cobrindo:
- ContextPackage seguro retorna allow ou decisão equivalente;
- item sem citação/referência gera warn ou require_approval;
- fonte desconhecida gera warning;
- orçamento inconsistente gera warn, require_approval ou block conforme severidade;
- redaction pendente/suspeita é detectada;
- pacote com omission reason crítico é detectado;
- comportamento determinístico;
- ausência de chamada externa;
- compatibilidade com testes existentes.

Requisitos de documentação:
- tudo em português do Brasil;
- explicar que as verificações são determinísticas;
- explicar que o Guardian não escolhe contexto;
- explicar que o Guardian não faz RAG;
- explicar que o Guardian não chama LLM;
- explicar limites atuais;
- atualizar próximos passos;
- manter links relativos corretos;
- não prometer comportamento ainda não implementado.

Regra de commit automático:
Se esta missão gerar commit automático, a mensagem deve estar em português do Brasil.
Não usar o prefixo `mission:`.
Usar a mensagem fornecida por VAF_COMMIT_MESSAGE quando existir.

Restrições:
- não adicionar dependências;
- não implementar Policy Engine completo;
- não implementar embeddings;
- não implementar pgvector;
- não implementar PostgreSQL;
- não implementar RAG semântico;
- não chamar Gemini, OpenAI, Ollama, Claude, OpenCode ou qualquer runtime;
- não executar providers externos;
- não acessar MCPs;
- não usar sudo;
- não alterar configs globais;
- não reescrever histórico Git;
- não fazer force push;
- não alterar APIs públicas sem necessidade;
- não prometer comportamento ainda não implementado;
- manter storage agnostic, provider agnostic, runtime agnostic e model agnostic;
- documentação e textos explicativos devem estar em português do Brasil.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar;
- documentação relacionada deve estar atualizada;
- não deve haver dependência externa nova;
- não deve haver chamada de rede;
- auto-commit deve usar mensagem em português do Brasil.
