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
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/guardian/README.md
- src/vercosa_ai_framework/policy/
- src/vercosa_ai_framework/policy/README.md
- src/vercosa_ai_framework/context/
- src/vercosa_ai_framework/context/README.md
- src/vercosa_ai_framework/model_selection/
- src/vercosa_ai_framework/model_selection/README.md
- src/vercosa_ai_framework/runtime/
- src/vercosa_ai_framework/runtime/README.md
- src/vercosa_ai_framework/missions/
- src/vercosa_ai_framework/missions/README.md
- tests/test_policy_engine_contracts.py
- tests/test_policy_guardian_integration.py
- tests/test_policy_context_router_integration.py
- tests/test_usage_limit_guard.py

Assuma o papel de:
- framework-architect;
- python-implementation-agent;
- reliability-engineer;
- audit-architect;
- test-engineer.

Missão:
Criar Audit/Event Log inicial.

Objetivo:
Criar contratos iniciais e implementação determinística mínima para um Audit/Event Log interno, capaz de representar eventos relevantes do framework sem persistência externa, sem banco de dados e sem integração com observabilidade externa.

Contexto:
- O Vercosa AI Framework já possui módulos centrais como Policy Engine, Guardian Engine, Context Router, Model Selection, Runtime Adapter, Mission Runner e Usage/API Limit Guard.
- As decisões desses módulos precisam ser futuramente auditáveis.
- Ainda não existe uma camada canônica para eventos internos.
- Esta missão deve criar apenas a fundação inicial do Audit/Event Log.
- O objetivo não é implementar observabilidade completa.
- O objetivo não é integrar com banco, OpenTelemetry, arquivos reais de log, serviços externos ou dashboards.
- O objetivo é criar tipos, contratos e uma implementação em memória, determinística, pequena e testável.

Estado arquitetural atual conhecido:
- Policy Engine resolve políticas declarativas.
- Guardian Engine avalia riscos operacionais.
- Context Router monta ContextPackage.
- Model Selection seleciona modelos.
- Usage/API Limit Guard detecta sinais de limite de uso.
- Ainda falta registrar decisões de forma estruturada.
- O Audit/Event Log será base futura para rastreabilidade, debugging, explicabilidade e segurança.

Entregáveis obrigatórios:
1. Criar módulo:
   - src/vercosa_ai_framework/audit/

2. Criar arquivos:
   - src/vercosa_ai_framework/audit/__init__.py
   - src/vercosa_ai_framework/audit/types.py
   - src/vercosa_ai_framework/audit/event_log.py
   - src/vercosa_ai_framework/audit/README.md

3. Criar testes:
   - tests/test_audit_event_log_contracts.py

4. Atualizar documentação:
   - docs/architecture/module-index.md
   - README.md, somente se necessário
   - docs/alignment/current-state.md, somente se necessário
   - docs/roadmap/mission-backlog.md, somente se necessário

Requisitos funcionais:
1. Criar tipos determinísticos para representar eventos internos do framework.

2. Criar enum ou tipo equivalente para categoria de evento, incluindo pelo menos:
   - mission
   - policy
   - guardian
   - context
   - model_selection
   - runtime
   - provider
   - usage_limit
   - system

3. Criar enum ou tipo equivalente para severidade de evento, incluindo pelo menos:
   - debug
   - info
   - warning
   - error
   - critical

4. Criar enum ou tipo equivalente para resultado do evento, incluindo pelo menos:
   - success
   - skipped
   - warning
   - failed
   - blocked
   - requires_approval

5. Criar estrutura de evento, por exemplo AuditEvent ou FrameworkEvent, com campos mínimos:
   - event_id
   - category
   - name
   - severity
   - result
   - message
   - source
   - metadata
   - created_at

6. O event_id deve ser determinístico quando os dados forem iguais, ou ao menos testável e estável dentro da implementação escolhida.

7. created_at pode ser opcional, injetável ou controlável para preservar testes determinísticos.

8. Criar contrato ou protocolo para EventLog.

9. Criar implementação em memória, por exemplo InMemoryEventLog.

10. A implementação em memória deve permitir:
    - registrar evento;
    - listar eventos;
    - filtrar por categoria;
    - filtrar por severidade;
    - filtrar por resultado;
    - limpar eventos, se fizer sentido;
    - retornar cópias ou estruturas imutáveis quando adequado.

11. Não implementar persistência em arquivo nesta missão.

12. Não implementar banco de dados nesta missão.

13. Não implementar SQLite.

14. Não implementar PostgreSQL.

15. Não implementar OpenTelemetry.

16. Não implementar integração com logs do worker nesta missão.

17. Não implementar integração obrigatória com Guardian, Policy, Context Router ou Model Selection nesta missão.

18. Pode documentar integrações futuras, mas não prometer como implementadas.

19. Não chamar LLM.

20. Não chamar provider externo.

21. Não acessar rede.

22. Não adicionar dependências.

Requisitos de testes:
Criar testes cobrindo:
1. Criação de evento com campos mínimos.

2. Criação de evento com metadata.

3. event_id é preenchido.

4. created_at é controlável, opcional ou testável.

5. Registro de evento em InMemoryEventLog.

6. Listagem de eventos preserva ordem determinística de inserção.

7. Filtro por categoria funciona.

8. Filtro por severidade funciona.

9. Filtro por resultado funciona.

10. Eventos retornados não permitem mutação indevida do estado interno, se aplicável ao contrato escolhido.

11. Limpeza de eventos funciona, se implementada.

12. Nenhuma chamada externa é feita.

13. Nenhuma dependência nova é exigida.

14. Testes existentes continuam passando.

Requisitos de documentação:
1. Tudo deve estar em português do Brasil.

2. Explicar o objetivo do Audit/Event Log.

3. Explicar que esta missão cria contratos iniciais e implementação em memória.

4. Explicar que não há persistência externa ainda.

5. Explicar que não há banco de dados ainda.

6. Explicar que não há observabilidade externa ainda.

7. Explicar quais tipos de evento são previstos.

8. Explicar como o Audit/Event Log se relaciona futuramente com:
   - Mission Runner;
   - Policy Engine;
   - Guardian Engine;
   - Context Router;
   - Model Selection;
   - Runtime Adapter;
   - Provider Gateway;
   - Usage/API Limit Guard.

9. Explicar limites atuais.

10. Explicar próximos passos possíveis:
   - registrar decisões de Guardian;
   - registrar políticas resolvidas;
   - registrar montagem de ContextPackage;
   - registrar seleção de modelo;
   - registrar falhas de quota/rate limit;
   - persistência futura;
   - exportação futura.

11. Manter links relativos corretos.

12. Não prometer comportamento ainda não implementado.

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
- src/vercosa_ai_framework/audit/__init__.py existe.
- src/vercosa_ai_framework/audit/types.py existe.
- src/vercosa_ai_framework/audit/event_log.py existe.
- src/vercosa_ai_framework/audit/README.md existe.
- tests/test_audit_event_log_contracts.py existe.
- Existe tipo estruturado para eventos internos.
- Existe implementação em memória do Event Log.
- É possível registrar e listar eventos.
- É possível filtrar eventos por categoria, severidade e resultado.
- Nenhuma persistência externa foi adicionada.
- Nenhuma dependência foi adicionada.
- docs/architecture/module-index.md foi atualizado.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
