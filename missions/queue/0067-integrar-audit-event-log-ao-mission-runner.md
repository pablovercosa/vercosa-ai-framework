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
- src/vercosa_ai_framework/missions/
- src/vercosa_ai_framework/missions/README.md
- src/vercosa_ai_framework/runtime/
- src/vercosa_ai_framework/runtime/README.md
- scripts/vaf-run-one-mission.sh
- scripts/vaf-worker.sh
- scripts/vaf-run-next-safe.sh
- scripts/vaf-run-batch-safe.sh
- tests/test_worker_scripts.py

Leia também, se existirem após execuções anteriores neste mesmo batch:
- src/vercosa_ai_framework/audit/
- src/vercosa_ai_framework/audit/README.md
- tests/test_audit_event_log_contracts.py
- tests/test_audit_decision_events.py

Assuma o papel de:
- framework-architect;
- python-implementation-agent;
- audit-architect;
- reliability-engineer;
- test-engineer.

Missão:
Integrar Audit/Event Log ao Mission Runner de forma inicial e opcional.

Objetivo:
Permitir que o Mission Runner ou contratos equivalentes de missão possam registrar eventos auditáveis básicos de ciclo de vida de missão, sem alterar agressivamente os scripts shell existentes, sem persistência externa e sem quebrar o fluxo operacional atual.

Contexto:
- O projeto executa missões por arquivos Markdown em missions/queue.
- O fluxo operacional move missões por queue, running, done e failed.
- O runner seguro de uma missão e o runner seguro em batch já existem.
- O Audit/Event Log inicial deve ter sido criado em missão anterior deste batch.
- Eventos auditáveis de decisões centrais devem ter sido criados em missão anterior deste batch.
- Agora é necessário iniciar a rastreabilidade do ciclo de vida de missões.
- O objetivo não é substituir logs textuais.
- O objetivo não é alterar profundamente scripts shell.
- O objetivo não é implementar persistência externa.
- O objetivo é criar base Python para eventos auditáveis de missão e documentar a relação com os scripts operacionais.

Entregáveis obrigatórios:
1. Atualizar, se necessário:
   - src/vercosa_ai_framework/missions/

2. Atualizar, se necessário:
   - src/vercosa_ai_framework/audit/

3. Criar testes:
   - tests/test_audit_mission_events.py

4. Atualizar documentação:
   - src/vercosa_ai_framework/missions/README.md
   - src/vercosa_ai_framework/audit/README.md
   - docs/architecture/module-index.md, somente se necessário
   - docs/operations/safe-runner-usage.md, somente se necessário
   - docs/operations/batch-execution-playbook.md, somente se necessário
   - README.md, somente se necessário

5. Não alterar scripts shell, salvo se houver uma integração extremamente pequena, segura e bem testável.

Requisitos funcionais:
1. Inspecionar o módulo missions existente antes de implementar.

2. Inspecionar o módulo audit criado em missão anterior antes de implementar.

3. Criar forma determinística de representar eventos de ciclo de vida de missão.

4. Eventos de missão devem cobrir, no mínimo, quando aplicável:
   - missão enfileirada;
   - missão iniciada;
   - missão concluída;
   - missão falhou;
   - missão ignorada;
   - batch iniciado;
   - batch concluído;
   - batch interrompido.

5. Não é obrigatório que os scripts shell passem a emitir esses eventos nesta missão.

6. Se a integração direta com scripts for arriscada, criar apenas helpers Python e documentar que integração operacional completa é futura.

7. Criar helpers ou factories de eventos para missões, por exemplo:
   - evento_missao_enfileirada;
   - evento_missao_iniciada;
   - evento_missao_concluida;
   - evento_missao_falhou;
   - evento_batch_iniciado;
   - evento_batch_concluido;
   - evento_batch_interrompido.

8. Os nomes reais podem seguir padrão em inglês se o código existente usar inglês, mas documentação deve estar em português do Brasil.

9. Eventos devem usar categoria mission.

10. Eventos devem usar severity e result coerentes:
   - conclusão bem-sucedida como success;
   - falha como failed ou error;
   - interrupção como warning ou failed conforme contrato existente;
   - batch saudável como success.

11. Metadata deve conter apenas dados seguros, como:
   - mission_name;
   - mission_path;
   - batch_size;
   - executed_count;
   - queue_count;
   - done_count;
   - failed_count;
   - commit_hash quando disponível.

12. Não registrar conteúdo integral da missão por padrão.

13. Não registrar prompts completos por padrão.

14. Não registrar secrets.

15. Não registrar credenciais.

16. Não registrar tokens de API.

17. Não implementar persistência em arquivo.

18. Não implementar banco de dados.

19. Não implementar leitura automática dos diretórios reais de missions, salvo se já houver contrato adequado.

20. Não alterar fluxo queue, running, done e failed nesta missão.

21. Não quebrar scripts existentes.

22. Não chamar LLM.

23. Não chamar provider externo.

24. Não acessar rede.

25. Não adicionar dependências.

Requisitos de testes:
Criar testes cobrindo:
1. Criação de evento de missão enfileirada.

2. Criação de evento de missão iniciada.

3. Criação de evento de missão concluída.

4. Criação de evento de missão com falha.

5. Criação de evento de batch iniciado.

6. Criação de evento de batch concluído.

7. Criação de evento de batch interrompido.

8. Eventos de missão usam categoria mission.

9. Eventos usam severity coerente.

10. Eventos usam result coerente.

11. Metadata segura é preservada.

12. Conteúdo integral da missão não é exigido no evento.

13. Helpers são determinísticos para a mesma entrada.

14. Integração é opcional.

15. Nenhuma persistência externa é usada.

16. Nenhuma dependência nova é exigida.

17. Scripts existentes continuam passando nos testes.

18. Testes existentes continuam passando.

Requisitos de documentação:
1. Tudo deve estar em português do Brasil.

2. Explicar o papel de eventos auditáveis no ciclo de vida de missões.

3. Explicar diferença entre:
   - logs textuais dos scripts;
   - eventos auditáveis estruturados;
   - persistência futura.

4. Explicar que esta missão não substitui os scripts shell.

5. Explicar que esta missão não altera o fluxo operacional queue, running, done e failed.

6. Explicar que a integração completa dos scripts com audit log pode ser futura.

7. Explicar quais eventos de missão já podem ser representados.

8. Explicar cuidados de segurança:
   - não registrar conteúdo integral da missão por padrão;
   - não registrar secrets;
   - não registrar credenciais;
   - não registrar tokens.

9. Explicar limites atuais.

10. Explicar próximos passos possíveis:
   - registrar eventos reais durante execução do runner;
   - registrar eventos reais durante batch;
   - persistir eventos em arquivo controlado;
   - exportar eventos;
   - relacionar eventos com commits.

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
- Não alterar fluxo operacional das missões.
- Não alterar scripts shell salvo ajuste mínimo, seguro e justificado.
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
- tests/test_audit_mission_events.py existe.
- Eventos auditáveis de missão podem ser criados.
- Eventos auditáveis de batch podem ser criados.
- Eventos usam categoria mission.
- Eventos usam severity e result coerentes.
- Metadata segura é preservada.
- Conteúdo integral da missão não é obrigatório no evento.
- Integração é opcional.
- Scripts existentes continuam compatíveis.
- Nenhuma persistência externa foi adicionada.
- Nenhuma dependência foi adicionada.
- Documentação relacionada foi atualizada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
