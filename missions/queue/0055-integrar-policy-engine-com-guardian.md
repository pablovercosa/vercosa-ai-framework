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
- src/vercosa_ai_framework/policy/
- src/vercosa_ai_framework/policy/README.md
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/guardian/README.md
- tests/test_policy_engine_contracts.py

Assuma o papel de framework-architect, python-implementation-agent e security-architect.

Missão:
Integrar Policy Engine com Guardian Engine de forma inicial e determinística.

Objetivo:
Criar uma integração mínima entre Policy Engine e Guardian Engine, permitindo que decisões do Guardian considerem um ResolvedPolicySet produzido pelo Policy Engine, sem misturar responsabilidades e sem implementar Policy Engine completo.

Contexto:
- O Policy Engine resolve políticas declarativas.
- O Guardian Engine avalia ações concretas e riscos operacionais.
- A ADR define separação entre Policy Engine e Guardian Engine.
- A integração deve ser pequena, testável e determinística.
- Nesta missão, o Policy Engine não deve virar Guardian, e o Guardian não deve virar Policy Engine.

Entregáveis obrigatórios:
- atualizar src/vercosa_ai_framework/policy/ se necessário;
- atualizar src/vercosa_ai_framework/guardian/ se necessário;
- criar tests/test_policy_guardian_integration.py;
- atualizar src/vercosa_ai_framework/policy/README.md;
- atualizar src/vercosa_ai_framework/guardian/README.md;
- atualizar docs/architecture/module-index.md se necessário;
- atualizar README.md se necessário.

Requisitos funcionais:
1. Inspecionar os contratos existentes do Policy Engine.
2. Inspecionar os contratos existentes do Guardian Engine.
3. Criar uma integração inicial em que o Guardian possa receber ou considerar um ResolvedPolicySet.
4. Reutilizar tipos existentes sempre que possível.
5. Não duplicar enums de decisão se já existirem no Guardian.
6. Não criar acoplamento circular.
7. Não fazer o Policy Engine chamar Guardian.
8. Preferir que o Guardian receba políticas resolvidas como entrada opcional.
9. Criar regras determinísticas simples, por exemplo:
   - uma política com efeito allow não deve bloquear por si só;
   - uma política com efeito warn pode elevar decisão para warn;
   - uma política com efeito require_approval pode elevar decisão para require_approval;
   - uma política com efeito deny/block pode elevar decisão para block, se houver efeito equivalente;
   - conflitos de política podem gerar require_approval ou warning conforme tipos existentes.
10. Manter o Guardian avaliando ações concretas e riscos.
11. Manter o Policy Engine resolvendo políticas declarativas.
12. Não implementar DSL.
13. Não implementar parser de política.
14. Não implementar regras remotas.
15. Não chamar LLM.
16. Não chamar provider externo.
17. Não acessar rede.
18. Não acessar banco.

Requisitos de testes:
Criar testes cobrindo:
- Guardian sem ResolvedPolicySet mantém comportamento atual;
- política resolvida com efeito allow não bloqueia;
- política resolvida com efeito warn gera decisão warn ou equivalente;
- política resolvida com efeito require_approval gera require_approval ou equivalente;
- política resolvida com efeito block/deny gera block ou equivalente, se o tipo existir;
- conflitos resolvidos pelo Policy Engine são considerados;
- comportamento determinístico;
- ausência de chamada externa;
- sem acoplamento circular evidente;
- testes existentes continuam passando.

Requisitos de documentação:
- tudo em português do Brasil;
- explicar que Policy Engine e Guardian Engine continuam separados;
- explicar que a integração é inicial;
- explicar que Policy Engine fornece políticas resolvidas;
- explicar que Guardian avalia risco operacional e pode elevar decisões com base nas políticas;
- explicar limites atuais;
- atualizar próximos passos;
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
