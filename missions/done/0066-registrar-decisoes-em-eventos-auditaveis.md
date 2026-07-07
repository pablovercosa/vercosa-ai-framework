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
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/guardian/README.md
- src/vercosa_ai_framework/context/
- src/vercosa_ai_framework/context/README.md
- tests/test_policy_engine_contracts.py
- tests/test_policy_guardian_integration.py
- tests/test_policy_context_router_integration.py
- tests/test_guardian_context_package_checks.py
- tests/test_context_router_mvp.py

Leia também, se existirem após execuções anteriores neste mesmo batch:
- src/vercosa_ai_framework/audit/
- src/vercosa_ai_framework/audit/README.md
- tests/test_audit_event_log_contracts.py

Assuma o papel de:
- framework-architect;
- python-implementation-agent;
- audit-architect;
- reliability-engineer;
- test-engineer.

Missão:
Registrar decisões de Policy, Guardian e Context em eventos auditáveis.

Objetivo:
Criar integração inicial e determinística entre o Audit/Event Log e decisões relevantes do Policy Engine, Guardian Engine e Context Router, permitindo registrar eventos estruturados sem persistência externa, sem banco de dados e sem alterar agressivamente o comportamento dos módulos existentes.

Contexto:
- A missão anterior do batch deve criar o módulo Audit/Event Log inicial.
- O Audit/Event Log deve começar a servir como trilha estruturada de decisões.
- Policy Engine resolve políticas declarativas.
- Guardian Engine avalia riscos operacionais.
- Context Router monta ContextPackage.
- Já existem integrações entre Policy Engine, Guardian Engine e Context Router.
- Agora precisamos registrar eventos auditáveis de decisões centrais, mas de forma inicial, opcional e segura.
- O objetivo não é criar observabilidade completa.
- O objetivo não é persistir logs em arquivo ou banco.
- O objetivo não é reescrever a arquitetura dos módulos.

Entregáveis obrigatórios:
1. Atualizar, se necessário:
   - src/vercosa_ai_framework/audit/

2. Criar arquivo de integração ou helpers, se coerente:
   - src/vercosa_ai_framework/audit/integrations.py
   - ou nome equivalente dentro do módulo audit

3. Atualizar, de forma mínima e segura, se necessário:
   - src/vercosa_ai_framework/policy/
   - src/vercosa_ai_framework/guardian/
   - src/vercosa_ai_framework/context/

4. Criar testes:
   - tests/test_audit_decision_events.py

5. Atualizar documentação:
   - src/vercosa_ai_framework/audit/README.md
   - src/vercosa_ai_framework/policy/README.md
   - src/vercosa_ai_framework/guardian/README.md
   - src/vercosa_ai_framework/context/README.md
   - docs/architecture/module-index.md, somente se necessário
   - README.md, somente se necessário

Requisitos funcionais:
1. Inspecionar o módulo audit criado na missão anterior antes de implementar.

2. Inspecionar contratos atuais de Policy Engine, Guardian Engine e Context Router.

3. Criar forma determinística de transformar decisões/resultados desses módulos em eventos auditáveis.

4. A integração deve ser opcional.

5. Nenhuma chamada existente deve quebrar.

6. Nenhum módulo deve passar a depender obrigatoriamente de um event log.

7. O Audit/Event Log pode expor helpers para criar eventos a partir de:
   - resultado de resolução de política;
   - decisão do Guardian;
   - montagem de ContextPackage;
   - warning de contexto;
   - omissão de item de contexto;
   - conflito de política;
   - sinal de require_approval.

8. Preferir helpers/factories de eventos antes de alterar profundamente os módulos.

9. Se for seguro, permitir que funções existentes aceitem parâmetro opcional de event_log.

10. Se não for seguro alterar assinaturas, criar apenas helpers auditáveis e documentar integração futura.

11. Eventos de Policy devem registrar, quando disponível:
   - quantidade de políticas consideradas;
   - quantidade de políticas resolvidas;
   - conflitos;
   - resultado geral;
   - severidade adequada;
   - metadata sem dados sensíveis desnecessários.

12. Eventos de Guardian devem registrar, quando disponível:
   - decisão operacional;
   - warnings;
   - bloqueios;
   - require_approval;
   - origem da avaliação;
   - metadata mínima.

13. Eventos de Context Router devem registrar, quando disponível:
   - quantidade de candidatos;
   - quantidade de itens selecionados;
   - quantidade de itens omitidos;
   - uso estimado de tokens;
   - warnings;
   - omission reasons;
   - metadata mínima.

14. Não registrar conteúdo integral sensível por padrão.

15. Não registrar prompts completos por padrão.

16. Não registrar secrets.

17. Não registrar credenciais.

18. Não registrar tokens de API.

19. Não implementar persistência externa.

20. Não acessar banco.

21. Não acessar rede.

22. Não chamar LLM.

23. Não chamar provider externo.

24. Não adicionar dependências.

Requisitos de testes:
Criar testes cobrindo:
1. Criação de evento auditável para resultado de Policy Engine.

2. Criação de evento auditável para decisão do Guardian.

3. Criação de evento auditável para ContextPackage ou resultado do Context Router.

4. Evento de Policy inclui categoria policy.

5. Evento de Guardian inclui categoria guardian.

6. Evento de Context inclui categoria context.

7. Eventos usam severidade coerente.

8. Eventos usam resultado coerente.

9. Metadata é preservada quando segura.

10. Conteúdo sensível bruto não é obrigatório no evento.

11. Helpers são determinísticos para a mesma entrada.

12. A integração é opcional.

13. Chamadas existentes dos módulos continuam funcionando.

14. Nenhuma persistência externa é usada.

15. Nenhuma dependência nova é exigida.

16. Testes existentes continuam passando.

Requisitos de documentação:
1. Tudo deve estar em português do Brasil.

2. Explicar que o Audit/Event Log agora possui integração inicial com decisões centrais.

3. Explicar que a integração é opcional.

4. Explicar que não há persistência externa.

5. Explicar que não há observabilidade externa.

6. Explicar que os eventos devem registrar metadados úteis sem capturar conteúdo sensível por padrão.

7. Explicar a diferença entre:
   - log textual operacional;
   - evento auditável estruturado;
   - persistência futura.

8. Explicar como eventos podem representar:
   - políticas resolvidas;
   - conflitos de política;
   - decisões do Guardian;
   - montagem de contexto;
   - omissões de contexto;
   - warnings;
   - require_approval.

9. Explicar limites atuais.

10. Explicar próximos passos possíveis:
   - registrar eventos no Mission Runner;
   - registrar eventos no Worker;
   - persistência futura;
   - exportação futura;
   - integração futura com Provider Gateway.

11. Não prometer comportamento ainda não implementado.

12. Manter links relativos corretos.

Restrições:
- Não adicionar dependências.
- Não acessar rede.
- Não acessar banco.
- Não implementar persistência real.
- Não implementar SQLite.
- Não implementar PostgreSQL.
- Não implementar OpenTelemetry.
- Não implementar dashboard.
- Não alterar scripts shell.
- Não alterar worker.
- Não alterar runner seguro.
- Não alterar runner em batch.
- Não chamar OpenAI.
- Não chamar Gemini.
- Não chamar Ollama.
- Não chamar Claude.
- Não chamar OpenCode.
- Não acessar MCPs.
- Não usar sudo.
- Não alterar configs globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- tests/test_audit_decision_events.py existe.
- Eventos auditáveis podem ser criados para Policy Engine.
- Eventos auditáveis podem ser criados para Guardian Engine.
- Eventos auditáveis podem ser criados para Context Router ou ContextPackage.
- A integração é opcional.
- Chamadas existentes continuam compatíveis.
- Eventos não exigem persistência externa.
- Eventos não exigem provider externo.
- Eventos não registram conteúdo sensível bruto por padrão.
- Documentação relacionada foi atualizada.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
