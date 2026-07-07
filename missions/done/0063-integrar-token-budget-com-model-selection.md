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
- docs/roadmap/mission-backlog.md
- src/vercosa_ai_framework/context/
- src/vercosa_ai_framework/context/README.md
- src/vercosa_ai_framework/model_selection/
- src/vercosa_ai_framework/model_selection/README.md
- src/vercosa_ai_framework/policy/
- src/vercosa_ai_framework/policy/README.md
- tests/test_context_contracts.py
- tests/test_context_router_mvp.py
- tests/test_policy_model_selection_integration.py

Assuma o papel de:
- framework-architect;
- python-implementation-agent;
- test-engineer;
- reliability-engineer.

Missão:
Integrar Token Budget Manager com Model Selection de forma inicial e determinística.

Objetivo:
Permitir que o Model Selection Engine considere informações de orçamento de tokens ao selecionar ou ranquear modelos, sem consultar providers externos, sem precificação real e sem alterar a responsabilidade do Context Router.

Contexto:
- O Context Router monta ContextPackage.
- O Token Budget Manager estima orçamento de tokens.
- O Model Selection Engine seleciona modelos conforme critérios do framework.
- O Policy Engine já se integra ao Model Selection na missão anterior, se ela tiver sido executada antes desta no batch.
- Agora o Model Selection deve conseguir considerar orçamento de tokens como entrada opcional.
- O Model Selection não deve calcular todo o contexto.
- O Token Budget Manager não deve selecionar modelos.
- A integração deve ser pequena, local, determinística e testável.

Entregáveis obrigatórios:
1. Atualizar arquivos em:
   - src/vercosa_ai_framework/model_selection/

2. Atualizar arquivos em:
   - src/vercosa_ai_framework/context/

   somente se for necessário para expor contratos de orçamento já existentes de forma limpa.

3. Criar teste:
   - tests/test_token_budget_model_selection_integration.py

4. Atualizar documentação:
   - src/vercosa_ai_framework/model_selection/README.md
   - src/vercosa_ai_framework/context/README.md
   - docs/context-router-token-budget.md
   - docs/architecture/module-index.md

5. Atualizar README.md somente se necessário.

Requisitos funcionais:
1. Inspecionar contratos atuais do Token Budget Manager.

2. Inspecionar contratos atuais do Model Selection Engine.

3. Criar integração opcional em que a seleção de modelo possa receber informações de orçamento de tokens.

4. Não quebrar chamadas existentes do Model Selection.

5. Não fazer o Model Selection montar ContextPackage.

6. Não fazer o Token Budget Manager escolher modelo.

7. Não criar acoplamento circular entre context e model_selection.

8. Reutilizar tipos existentes sempre que possível.

9. Permitir que a decisão de seleção registre se um modelo candidato parece compatível com o orçamento informado.

10. Permitir que a decisão de seleção registre warning quando o orçamento for insuficiente ou apertado, se houver campo adequado.

11. Se houver candidatos de modelo com capacidades de contexto diferentes, permitir filtragem ou ordenação determinística com base no orçamento.

12. Não implementar precificação real por token.

13. Não consultar limites reais de providers.

14. Não consultar billing real.

15. Não chamar LLM.

16. Não chamar provider externo.

17. Não acessar rede.

18. Não acessar banco.

19. Não implementar ranking semântico.

20. Não implementar RAG.

21. Não implementar embeddings.

22. Não adicionar dependências.

Requisitos de testes:
Criar testes cobrindo:
1. Model Selection sem orçamento de tokens mantém comportamento atual.

2. Orçamento suficiente não bloqueia seleção.

3. Orçamento insuficiente gera warning, metadata ou exclusão determinística conforme contrato implementado.

4. Candidatos com janela de contexto menor podem ser desfavorecidos ou excluídos se a regra for clara.

5. Candidatos com janela de contexto suficiente permanecem elegíveis.

6. A seleção permanece determinística com a mesma entrada.

7. Não há chamada externa.

8. Não há dependência de provider real.

9. Não há acoplamento circular evidente.

10. Testes existentes continuam passando.

Requisitos de documentação:
1. Tudo deve estar em português do Brasil.

2. Explicar que Token Budget Manager estima orçamento.

3. Explicar que Model Selection apenas consome informações de orçamento.

4. Explicar que esta integração é inicial.

5. Explicar que não há precificação real.

6. Explicar que não há consulta a provider externo.

7. Explicar que não há billing real.

8. Explicar limites atuais.

9. Explicar próximos passos.

10. Manter links relativos corretos.

11. Não prometer comportamento ainda não implementado.

Restrições:
- Não adicionar dependências.
- Não chamar OpenAI.
- Não chamar Gemini.
- Não chamar Ollama.
- Não chamar Claude.
- Não chamar OpenCode.
- Não acessar MCPs.
- Não acessar rede.
- Não acessar banco.
- Não implementar billing real.
- Não implementar precificação real.
- Não implementar consulta real de limites de contexto de providers.
- Não implementar RAG.
- Não implementar embeddings.
- Não implementar pgvector.
- Não usar sudo.
- Não alterar configs globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- tests/test_token_budget_model_selection_integration.py existe.
- Model Selection aceita informações de orçamento de tokens como entrada opcional ou estrutura equivalente.
- Chamadas existentes do Model Selection continuam compatíveis.
- Token Budget Manager não seleciona modelos.
- Model Selection não monta ContextPackage.
- Não há acoplamento circular.
- Documentação relacionada foi atualizada.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
