Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- docs/architecture/module-index.md
- docs/alignment/current-state.md
- docs/alignment/architecture-map.md
- docs/alignment/roadmap.md
- docs/roadmap/mission-backlog.md
- src/vercosa_ai_framework/policy/
- src/vercosa_ai_framework/policy/README.md
- src/vercosa_ai_framework/model_selection/
- src/vercosa_ai_framework/model_selection/README.md
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/guardian/README.md
- tests/test_policy_engine_contracts.py
- tests/test_policy_guardian_integration.py

Assuma o papel de:
- framework-architect;
- python-implementation-agent;
- test-engineer;
- policy-architect.

Missão:
Integrar Policy Engine com Model Selection de forma inicial e determinística.

Objetivo:
Permitir que o Model Selection Engine considere políticas resolvidas pelo Policy Engine ao selecionar ou ranquear modelos, mantendo a separação de responsabilidades e sem chamar providers externos.

Contexto:
- O Policy Engine resolve políticas declarativas.
- O Model Selection Engine seleciona modelos conforme critérios do framework.
- O Guardian Engine avalia riscos operacionais.
- O Policy Engine já se integra ao Guardian Engine.
- O Policy Engine já se integra ao Context Router.
- Agora o Model Selection deve ser capaz de receber políticas resolvidas como entrada opcional.
- O Model Selection não deve resolver políticas.
- O Policy Engine não deve chamar o Model Selection.
- A integração deve ser determinística, local, testável e pequena.

Entregáveis obrigatórios:
1. Atualizar arquivos em:
   - src/vercosa_ai_framework/model_selection/

2. Atualizar arquivos em:
   - src/vercosa_ai_framework/policy/

   somente se for necessário para manter contratos coerentes.

3. Criar teste:
   - tests/test_policy_model_selection_integration.py

4. Atualizar documentação:
   - src/vercosa_ai_framework/model_selection/README.md
   - src/vercosa_ai_framework/policy/README.md
   - docs/architecture/module-index.md

5. Atualizar README.md somente se necessário.

Requisitos funcionais:
1. Inspecionar os contratos atuais do Model Selection Engine.

2. Inspecionar os contratos atuais do Policy Engine.

3. Criar integração opcional em que o Model Selection possa receber um ResolvedPolicySet ou estrutura equivalente já produzida pelo Policy Engine.

4. Não fazer o Model Selection resolver políticas.

5. Não fazer o Policy Engine selecionar modelos.

6. Não criar acoplamento circular.

7. Reutilizar tipos existentes sempre que possível.

8. Preservar compatibilidade com chamadas existentes do Model Selection.

9. Políticas com efeito allow não devem, por si só, forçar escolha de modelo.

10. Políticas com efeito warn podem gerar warning ou metadata na decisão de seleção.

11. Políticas com efeito require_approval podem sinalizar que a escolha exige revisão ou aprovação, se houver campo adequado; se não houver, registrar warning ou metadata de forma mínima.

12. Políticas com efeito deny ou block podem excluir candidatos de modelo somente se a regra for clara e determinística.

13. Conflitos de política podem gerar warning ou require_approval conforme contratos existentes.

14. A seleção deve continuar determinística.

15. A seleção deve continuar sem provider externo.

16. A seleção deve continuar sem chamada de LLM.

17. Não implementar precificação real.

18. Não consultar billing real.

19. Não consultar limites reais de API.

20. Não implementar roteamento avançado de modelos nesta missão.

21. Não implementar ranking semântico.

22. Não adicionar dependências.

Requisitos de testes:
Criar testes cobrindo:
1. Model Selection sem ResolvedPolicySet mantém comportamento atual.

2. Política allow não altera indevidamente a seleção.

3. Política warn é refletida em warning ou metadata.

4. Política require_approval é refletida de forma rastreável.

5. Política deny ou block pode excluir modelo quando houver regra clara.

6. Conflito de política é considerado de forma determinística.

7. Seleção permanece repetível com a mesma entrada.

8. Não há chamada externa.

9. Não há dependência de Guardian Engine para seleção.

10. Não há acoplamento circular evidente.

11. Testes existentes continuam passando.

Requisitos de documentação:
1. Tudo deve estar em português do Brasil.

2. Explicar que o Policy Engine resolve políticas.

3. Explicar que o Model Selection apenas consome políticas resolvidas.

4. Explicar que esta integração é inicial.

5. Explicar que não há precificação real nesta missão.

6. Explicar que não há chamada a provider externo.

7. Explicar que não há consulta a billing real.

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
- Não implementar rate limit real.
- Não implementar seleção baseada em preço real.
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
- tests/test_policy_model_selection_integration.py existe.
- Model Selection aceita políticas resolvidas como entrada opcional ou estrutura equivalente.
- Chamadas existentes do Model Selection continuam compatíveis.
- Policy Engine não chama Model Selection.
- Model Selection não resolve políticas.
- Não há acoplamento circular.
- Documentação relacionada foi atualizada.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
