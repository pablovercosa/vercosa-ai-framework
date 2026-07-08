Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- docs/documentation/readme-standard.md
- docs/architecture/module-index.md
- docs/alignment/current-state.md
- docs/alignment/architecture-map.md
- docs/alignment/roadmap.md
- docs/roadmap/mission-backlog.md
- docs/operations/safe-runner-usage.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md
- src/vercosa_ai_framework/policy/README.md
- src/vercosa_ai_framework/guardian/README.md
- src/vercosa_ai_framework/context/README.md
- src/vercosa_ai_framework/model_selection/README.md
- src/vercosa_ai_framework/runtime/README.md
- src/vercosa_ai_framework/missions/README.md

Leia também, se existirem após execuções anteriores neste mesmo batch:
- src/vercosa_ai_framework/audit/README.md
- src/vercosa_ai_framework/cli/README.md
- tests/test_audit_event_log_contracts.py
- tests/test_audit_decision_events.py
- tests/test_audit_mission_events.py
- tests/test_cli_operacional_inicial.py
- tests/test_cli_validate.py
- tests/test_cli_doctor.py

Assuma o papel de:
- documentation-agent;
- framework-architect;
- examples-engineer;
- developer-experience-engineer;
- reliability-engineer.

Missão:
Criar exemplos operacionais iniciais do Vercosa AI Framework.

Objetivo:
Criar documentação inicial de exemplos operacionais reais e copiáveis para explicar como os módulos centrais do Vercosa AI Framework se conectam, sem implementar funcionalidades novas, sem executar providers externos e sem prometer comportamento ainda não existente.

Contexto:
- O projeto já possui vários módulos centrais.
- O projeto já possui runner seguro de uma missão.
- O projeto já possui runner seguro em batch.
- O projeto já possui Policy Engine.
- O projeto já possui Guardian Engine.
- O projeto já possui Context Router.
- O projeto já possui Token Budget Manager.
- O projeto já possui Knowledge Hub.
- O projeto já possui Model Selection Engine.
- O projeto já possui Usage/API Limit Guard.
- Missões anteriores deste batch devem criar Audit/Event Log e CLI operacional inicial.
- Agora é necessário começar a documentar exemplos operacionais para facilitar entendimento, continuidade e futura documentação pública.
- Os exemplos devem ser realistas, mas não devem fingir que existe integração que ainda não existe.
- Os exemplos devem deixar claro o que é contrato, MVP, integração inicial ou uso futuro.

Entregáveis obrigatórios:
1. Criar diretório, se ainda não existir:
   - docs/examples/

2. Criar arquivo:
   - docs/examples/README.md

3. Criar pelo menos dois exemplos documentais:
   - docs/examples/mission-batch-operational-flow.md
   - docs/examples/policy-context-guardian-flow.md

4. Criar terceiro exemplo se fizer sentido após ler o estado do projeto:
   - docs/examples/cli-diagnostics-flow.md
   - ou docs/examples/audit-event-flow.md

5. Atualizar README.md somente se houver seção adequada.

6. Atualizar docs/architecture/module-index.md somente se necessário.

7. Atualizar docs/roadmap/mission-backlog.md somente se necessário.

8. Não alterar código Python.

9. Não alterar scripts shell.

10. Não adicionar dependências.

Requisitos do arquivo docs/examples/README.md:
1. Estar em português do Brasil.

2. Explicar o propósito dos exemplos.

3. Explicar que exemplos podem misturar:
   - comportamento implementado;
   - contratos existentes;
   - fluxo operacional atual;
   - próximos passos documentados.

4. Diferenciar claramente:
   - exemplo executável;
   - exemplo conceitual;
   - exemplo de arquitetura;
   - exemplo futuro.

5. Listar os exemplos criados com links relativos.

6. Explicar que os exemplos não substituem:
   - README principal;
   - docs de arquitetura;
   - specs;
   - testes;
   - playbooks operacionais.

7. Explicar que exemplos devem ser mantidos em português do Brasil.

8. Explicar que exemplos não devem prometer integração ainda não implementada.

Requisitos do exemplo docs/examples/mission-batch-operational-flow.md:
1. Explicar o fluxo operacional de missões.

2. Incluir o caminho:
   - missions/queue
   - missions/running
   - missions/done
   - missions/failed

3. Explicar runner seguro de uma missão.

4. Explicar runner seguro em batch.

5. Explicar batch de 3.

6. Explicar batch de 10.

7. Explicar quando usar batch de 10.

8. Explicar quando não usar batch de 10.

9. Incluir comandos operacionais em blocos Markdown normais no arquivo final, se fizer sentido.

10. Explicar que push automático é opt-in.

11. Explicar que validação pós-batch é obrigatória.

12. Apontar para:
   - docs/operations/batch-execution-playbook.md
   - docs/operations/post-batch-validation-checklist.md

13. Não alterar scripts.

14. Não prometer automação além do que já existe.

Requisitos do exemplo docs/examples/policy-context-guardian-flow.md:
1. Explicar o fluxo conceitual implementado até aqui:
   - Policy Engine
   - ResolvedPolicySet
   - Context Router
   - ContextPackage
   - Guardian Engine

2. Explicar que o Policy Engine resolve políticas declarativas.

3. Explicar que o Context Router consome políticas resolvidas, mas não resolve políticas.

4. Explicar que o Guardian Engine avalia risco operacional.

5. Explicar que o Guardian pode considerar ContextPackage e políticas resolvidas.

6. Explicar o papel do Token Budget Manager.

7. Explicar limites atuais:
   - sem RAG semântico;
   - sem embeddings;
   - sem pgvector;
   - sem provider externo;
   - sem chamada de LLM nesse fluxo de teste.

8. Incluir exemplo conceitual de entrada e saída, se fizer sentido.

9. Marcar claramente o que é comportamento implementado e o que é evolução futura.

10. Não criar código Python novo.

11. Não prometer DSL completa de políticas.

12. Não prometer enforcement completo ainda não implementado.

Requisitos do terceiro exemplo, se criado:
1. Se escolher CLI, explicar:
   - status;
   - validate;
   - doctor;
   - limites atuais;
   - diferença entre CLI e scripts shell.

2. Se escolher Audit/Event Log, explicar:
   - eventos estruturados;
   - eventos em memória;
   - diferença entre log textual e evento auditável;
   - ausência de persistência externa;
   - próximos passos.

3. O terceiro exemplo deve estar em português do Brasil.

4. O terceiro exemplo não deve prometer comportamento ainda não implementado.

Requisitos gerais de documentação:
1. Tudo deve estar em português do Brasil.

2. Usar links relativos corretos.

3. Manter o README principal enxuto.

4. Evitar duplicação excessiva com docs existentes.

5. Reutilizar termos arquiteturais já adotados:
   - Policy Engine;
   - Guardian Engine;
   - Context Router;
   - Token Budget Manager;
   - Knowledge Hub;
   - Model Selection Engine;
   - Audit/Event Log;
   - CLI operacional;
   - Mission Runner.

6. Marcar claramente quando algo for:
   - implementado;
   - MVP;
   - integração inicial;
   - futuro;
   - fora do escopo.

7. Não prometer funcionalidade ainda não implementada.

8. Não transformar exemplos em roadmap completo.

9. Não substituir specs por exemplos.

10. Não substituir testes por exemplos.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não implementar novas funcionalidades.
- Não adicionar dependências.
- Não acessar rede.
- Não acessar banco.
- Não chamar OpenAI.
- Não chamar Gemini.
- Não chamar Ollama.
- Não chamar Claude.
- Não chamar OpenCode.
- Não acessar MCPs.
- Não executar providers.
- Não executar missões.
- Não fazer git push.
- Não usar sudo.
- Não alterar configs globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- docs/examples/README.md existe.
- docs/examples/mission-batch-operational-flow.md existe.
- docs/examples/policy-context-guardian-flow.md existe.
- Pelo menos dois exemplos operacionais foram criados.
- Um terceiro exemplo foi criado se fizer sentido após leitura do projeto.
- Exemplos usam português do Brasil.
- Exemplos possuem links relativos corretos.
- Exemplos diferenciam comportamento implementado de comportamento futuro.
- Exemplos não prometem recursos inexistentes.
- README.md é atualizado somente se necessário.
- docs/architecture/module-index.md é atualizado somente se necessário.
- Nenhum código Python é alterado.
- Nenhum script shell é alterado.
- Nenhuma dependência é adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
