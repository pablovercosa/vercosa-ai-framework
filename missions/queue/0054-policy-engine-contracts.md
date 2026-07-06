Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- docs/architecture/module-index.md
- docs/alignment/current-state.md
- docs/alignment/architecture-map.md
- docs/alignment/roadmap.md
- specs/framework/0005-guardian-engine.md
- knowledge/decisions/2026-07-04-policy-engine-vs-guardian-engine.md
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/guardian/README.md

Assuma o papel de framework-architect e python-implementation-agent.

Missão:
Criar contratos iniciais do Policy Engine.

Objetivo:
Criar o módulo inicial `policy` com contratos, tipos e documentação para representar a camada declarativa de políticas, separada do Guardian Engine.

Contexto:
- A ADR `2026-07-04-policy-engine-vs-guardian-engine.md` definiu que Policy Engine e Guardian Engine são camadas separadas.
- Policy Engine deve resolver políticas declarativas, precedência e composição.
- Guardian Engine deve avaliar ações concretas e emitir decisões operacionais como allow/warn/block/require_approval.
- Nesta missão, criar apenas contratos iniciais e MVP determinístico simples do Policy Engine.
- Não integrar profundamente com Guardian ainda.

Entregáveis obrigatórios:
- criar src/vercosa_ai_framework/policy/__init__.py;
- criar src/vercosa_ai_framework/policy/types.py;
- criar src/vercosa_ai_framework/policy/engine.py;
- criar src/vercosa_ai_framework/policy/README.md;
- criar tests/test_policy_engine_contracts.py;
- atualizar docs/architecture/module-index.md;
- atualizar README.md se necessário;
- atualizar docs/alignment/current-state.md ou roadmap apenas se necessário.

Requisitos funcionais:
1. Criar tipos determinísticos para políticas declarativas.
2. Incluir conceitos mínimos como:
   - PolicyScope;
   - PolicySource;
   - PolicyEffect;
   - PolicySeverity;
   - PolicyRule;
   - PolicySet;
   - PolicyConflict;
   - ResolvedPolicySet;
   - PolicyEvaluationContext;
   - PolicyResolutionResult.
3. Criar um contrato/porta para PolicyEngine.
4. Criar implementação simples `DeterministicPolicyEngine` ou equivalente.
5. A implementação inicial deve:
   - aceitar uma lista explícita de PolicySet;
   - ordenar policies de forma determinística;
   - aplicar precedência simples por prioridade;
   - detectar conflitos básicos;
   - produzir ResolvedPolicySet;
   - não chamar Guardian Engine;
   - não chamar LLM;
   - não chamar provider externo;
   - não acessar rede;
   - não acessar banco.
6. Não implementar DSL complexa.
7. Não implementar parser externo.
8. Não implementar política dinâmica remota.
9. Não substituir Guardian Engine.
10. Manter compatibilidade arquitetural com futura integração.

Requisitos de testes:
Criar testes cobrindo:
- criação de PolicyRule;
- criação de PolicySet;
- resolução de lista vazia;
- resolução de uma política simples;
- ordenação determinística por prioridade;
- detecção simples de conflito;
- produção de ResolvedPolicySet;
- comportamento repetível com mesma entrada;
- ausência de chamadas externas;
- não dependência do Guardian Engine para resolver políticas.

Requisitos de documentação:
- tudo em português do Brasil;
- explicar diferença entre Policy Engine e Guardian Engine;
- explicar que esta missão cria contratos iniciais;
- explicar que não há DSL completa;
- explicar que não há integração profunda ainda;
- explicar próximos passos;
- manter links relativos corretos;
- não prometer comportamento ainda não implementado.

Regra de commit automático:
Se esta missão gerar commit automático, a mensagem deve estar em português do Brasil.
Usar a mensagem fornecida por VAF_COMMIT_MESSAGE quando existir.

Restrições:
- não adicionar dependências;
- não implementar Policy Engine completo;
- não alterar Guardian Engine salvo documentação ou import estritamente necessário;
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
- módulo policy existe;
- testes novos existem e passam;
- pytest passa;
- python3 -m compileall src passa;
- docs do módulo policy existem;
- índice de módulos atualizado;
- auto-commit usa mensagem em português do Brasil.
