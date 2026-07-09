Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
- CHANGELOG.md
- SECURITY.md
- docs/security/vulnerability-reporting.md
- docs/legal/usage-policy.md
- docs/architecture/audit-event-architecture.md
- docs/architecture/post-integration-architecture-review.md
- docs/architecture/module-index.md
- docs/alignment/current-state.md
- docs/alignment/architecture-map.md
- docs/alignment/roadmap.md
- docs/roadmap/mission-backlog.md
- docs/operations/safe-runner-usage.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md
- src/vercosa_ai_framework/audit/README.md
- src/vercosa_ai_framework/audit/types.py
- src/vercosa_ai_framework/audit/event_log.py
- src/vercosa_ai_framework/audit/integrations.py
- tests/test_audit_event_log_contracts.py
- tests/test_audit_decision_events.py
- tests/test_audit_mission_events.py

Leia também, se existirem:
- src/vercosa_ai_framework/audit/persistence.py
- src/vercosa_ai_framework/audit/jsonl.py
- tests/test_audit_event_persistence.py
- tests/test_audit_jsonl_event_log.py
- docs/audit/
- audit/
- var/
- runtime/

Assuma o papel de:
- audit-engineer;
- security-reviewer;
- test-engineer;
- framework-architect;
- documentation-agent.

Missão:
Persistir eventos auditáveis em arquivo local controlado.

Objetivo:
Adicionar uma persistência local simples, explícita e segura para eventos auditáveis, usando arquivo JSONL controlado, sem banco de dados, sem rede, sem dependências externas e sem transformar a persistência em comportamento obrigatório global.

Contexto:
- O módulo audit já possui contratos de eventos auditáveis.
- O Audit/Event Log inicial existe.
- Integrações auditáveis já existem para decisões centrais e Mission Runner.
- A documentação arquitetural já identifica persistência externa como futura.
- Esta missão deve implementar apenas uma persistência local controlada em arquivo.
- O objetivo é permitir testes, rastreabilidade local e preparação para relatórios futuros.
- Esta missão não deve implementar banco de dados.
- Esta missão não deve implementar SQLite.
- Esta missão não deve implementar PostgreSQL.
- Esta missão não deve implementar OpenTelemetry.
- Esta missão não deve implementar dashboard.
- Esta missão não deve implementar exportador remoto.
- Esta missão não deve alterar scripts shell.
- Esta missão não deve ativar gravação global automática sem decisão explícita.

Entregáveis obrigatórios:
1. Criar ou atualizar módulo de persistência em:
   - src/vercosa_ai_framework/audit/

2. Criar testes para persistência local, preferencialmente:
   - tests/test_audit_event_persistence.py

3. Atualizar:
   - src/vercosa_ai_framework/audit/README.md
   - docs/architecture/audit-event-architecture.md
   - docs/architecture/module-index.md
   - docs/alignment/current-state.md
   - docs/alignment/architecture-map.md
   - docs/roadmap/mission-backlog.md
   - CHANGELOG.md

4. Atualizar, se necessário:
   - README.md
   - docs/alignment/roadmap.md
   - docs/operations/post-batch-validation-checklist.md
   - docs/release/public-alpha-readiness.md

5. Não alterar scripts shell.

6. Não adicionar dependências.

Requisitos funcionais:
1. Implementar persistência local de eventos auditáveis em arquivo JSONL.

2. A persistência deve ser explícita e opt-in.

3. Não deve substituir a implementação em memória existente.

4. Não deve tornar escrita em disco obrigatória para todos os usos do Audit/Event Log.

5. Deve ser possível instanciar um log auditável persistente apontando para um caminho de arquivo local.

6. Cada evento persistido deve ocupar uma linha JSON válida.

7. O arquivo deve ser append-only na operação normal.

8. A implementação deve criar diretório pai somente quando isso for seguro e explícito.

9. A implementação deve usar codificação UTF-8.

10. A implementação deve preservar os campos principais do evento:
   - event_id;
   - category;
   - name;
   - severity;
   - result;
   - message;
   - source;
   - metadata;
   - created_at.

11. A serialização deve ser determinística o suficiente para testes.

12. A implementação deve lidar corretamente com metadata vazia.

13. A implementação deve lidar com metadata simples contendo:
   - strings;
   - números;
   - booleanos;
   - listas simples;
   - dicionários simples;
   - null, se aplicável.

14. Se metadata contiver valores não serializáveis, a implementação deve falhar de forma clara ou normalizar de forma segura e documentada.

15. Não registrar secrets por conta própria.

16. Não adicionar coleta automática de variáveis de ambiente.

17. Não capturar prompts completos por padrão.

18. Não capturar tokens de API.

19. Não capturar credenciais.

20. Não capturar conteúdo sensível bruto por padrão.

21. Não implementar redaction complexa nesta missão, salvo se já houver função simples existente.

22. Se houver validação simples de chaves sensíveis, manter conservadora e testada.

23. A persistência deve ser local e síncrona.

24. Não implementar fila assíncrona.

25. Não implementar rotação de arquivo.

26. Não implementar retenção.

27. Não implementar compressão.

28. Não implementar criptografia.

29. Não implementar envio remoto.

30. Não implementar integração com banco.

31. Não implementar integração com logs operacionais existentes.

32. Não alterar comportamento de batch.

33. Não alterar comportamento dos scripts.

Requisitos de implementação:
1. Usar somente biblioteca padrão.

2. Preferir nomes claros, como:
   - JsonlAuditEventLog
   - AuditEventJsonlWriter
   - FileAuditEventLog

3. Escolher o nome mais coerente com o código existente.

4. Se já houver classe base ou protocolo de Event Log, seguir o contrato existente.

5. Se não houver contrato formal, manter a integração mínima e compatível com a implementação atual.

6. Preservar compatibilidade com testes existentes.

7. Não quebrar o Audit/Event Log em memória.

8. Não modificar tipos públicos sem necessidade.

9. Não alterar categorias, severidades ou resultados existentes sem necessidade.

10. Não adicionar dependências.

11. Não acoplar persistência local a Mission Runner nesta missão, salvo se já houver ponto claro e seguro de integração opcional.

12. Não alterar providers.

13. Não alterar runtimes.

14. Não alterar Policy Engine.

15. Não alterar Guardian Engine.

16. Não alterar Context Router.

17. Manter responsabilidade dentro do módulo audit.

18. Se criar arquivo novo, exportar no __init__.py somente se esse padrão já existir no projeto.

19. Evitar APIs grandes.

20. Manter implementação pequena, testável e explícita.

Requisitos de segurança:
1. Documentar que o arquivo JSONL pode conter metadados sensíveis se o chamador passar metadados sensíveis.

2. Orientar que chamadores não devem enviar:
   - secrets;
   - tokens;
   - credenciais;
   - chaves de API;
   - prompts completos;
   - dados pessoais sensíveis;
   - logs brutos não sanitizados.

3. Não implementar coleta automática de dados.

4. Não gravar variáveis de ambiente.

5. Não gravar estado Git automaticamente.

6. Não gravar conteúdo de arquivos automaticamente.

7. Não gravar conteúdo de missões automaticamente além do que já estiver no evento recebido.

8. Não usar caminho fixo global perigoso.

9. Não gravar em diretórios fora do projeto salvo caminho explicitamente fornecido.

10. Tratar erros de escrita com exceção clara.

Requisitos de testes:
1. Criar testes unitários para persistência JSONL.

2. Usar diretório temporário nos testes.

3. Testar criação do arquivo.

4. Testar append de um evento.

5. Testar append de múltiplos eventos.

6. Testar que cada linha é JSON válido.

7. Testar que campos principais são preservados.

8. Testar metadata vazia.

9. Testar metadata simples.

10. Testar ordenação ou estabilidade da serialização quando aplicável.

11. Testar diretório pai inexistente, conforme comportamento definido.

12. Testar erro de caminho inválido se for prático e portável.

13. Testar que o log em memória existente continua funcionando.

14. Testar que a persistência não chama rede.

15. Testar que a persistência não depende de banco.

16. Não depender de arquivos reais do diretório logs.

17. Não depender da fila real de missões.

18. Não depender de data/hora instável sem controle.

19. Garantir que pytest passe.

Requisitos de documentação:
1. Atualizar src/vercosa_ai_framework/audit/README.md com:
   - persistência local JSONL;
   - uso explícito;
   - limites;
   - cuidados com dados sensíveis;
   - diferença entre log em memória e log em arquivo;
   - o que ainda é futuro.

2. Atualizar docs/architecture/audit-event-architecture.md com:
   - persistência local controlada;
   - JSONL;
   - limites atuais;
   - ainda sem banco;
   - ainda sem OpenTelemetry;
   - ainda sem dashboard;
   - ainda sem retenção/rotação.

3. Atualizar docs/architecture/module-index.md para refletir a evolução do módulo audit.

4. Atualizar docs/alignment/current-state.md para registrar persistência local de eventos auditáveis como implementada.

5. Atualizar docs/alignment/architecture-map.md para diferenciar:
   - Audit/Event Log em memória;
   - persistência local JSONL;
   - persistência externa futura.

6. Atualizar docs/roadmap/mission-backlog.md para marcar persistência local controlada como concluída ou em progresso.

7. Manter como futuras:
   - retenção;
   - rotação;
   - redaction avançada;
   - persistência externa;
   - banco;
   - OpenTelemetry;
   - dashboard;
   - exportador remoto;
   - relatórios pós-batch baseados em eventos.

8. Atualizar CHANGELOG.md na seção Não publicado.

9. Atualizar README.md somente se houver seção adequada para auditoria/governança.

10. Não prometer persistência externa como implementada.

11. Não prometer banco como implementado.

12. Não prometer dashboard.

13. Não prometer segurança absoluta.

14. Tudo deve estar em português do Brasil.

15. Usar links relativos corretos.

Restrições:
- Não alterar scripts shell.
- Não implementar banco de dados.
- Não implementar SQLite.
- Não implementar PostgreSQL.
- Não implementar pgvector.
- Não implementar OpenTelemetry.
- Não implementar dashboard.
- Não implementar exportador remoto.
- Não implementar API HTTP.
- Não implementar retenção.
- Não implementar rotação.
- Não implementar compressão.
- Não implementar criptografia.
- Não implementar redaction complexa.
- Não alterar fluxo de batch.
- Não ativar persistência global obrigatória.
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
- Documentação, testes e mensagens devem estar em português do Brasil quando aplicável.

Critérios de aceite:
- Existe persistência local JSONL para eventos auditáveis.
- A persistência é explícita e opt-in.
- O log em memória existente continua funcionando.
- Cada evento persistido é uma linha JSON válida.
- Campos principais do evento são preservados.
- Testes cobrem persistência local.
- Testes usam diretório temporário.
- Nenhuma dependência foi adicionada.
- Nenhum script shell foi alterado.
- Não há banco de dados.
- Não há rede.
- Não há integração remota.
- Documentação do módulo audit foi atualizada.
- Documentação arquitetural foi atualizada.
- CHANGELOG.md registra a mudança.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
