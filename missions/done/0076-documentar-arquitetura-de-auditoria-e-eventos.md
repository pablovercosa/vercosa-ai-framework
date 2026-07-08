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
- docs/examples/README.md
- src/vercosa_ai_framework/audit/README.md
- src/vercosa_ai_framework/audit/types.py
- src/vercosa_ai_framework/audit/event_log.py
- src/vercosa_ai_framework/audit/integrations.py
- src/vercosa_ai_framework/policy/README.md
- src/vercosa_ai_framework/guardian/README.md
- src/vercosa_ai_framework/context/README.md
- src/vercosa_ai_framework/missions/README.md
- tests/test_audit_event_log_contracts.py
- tests/test_audit_decision_events.py
- tests/test_audit_mission_events.py

Assuma o papel de:
- documentation-agent;
- audit-architect;
- framework-architect;
- technical-editor;
- security-reviewer.

Missão:
Documentar arquitetura de auditoria e eventos.

Objetivo:
Criar documentação arquitetural dedicada para o Audit/Event Log do Vercosa AI Framework, explicando seu papel, contratos, categorias, severidades, resultados, eventos auditáveis, integrações atuais, limites de segurança e próximos passos, sem alterar código e sem implementar persistência externa.

Contexto:
- O módulo audit já existe.
- O Audit/Event Log inicial foi criado com contratos e implementação em memória.
- Eventos auditáveis de decisões centrais foram adicionados.
- Eventos auditáveis de missão foram adicionados.
- O README do módulo audit existe, mas o projeto precisa de uma documentação arquitetural mais completa.
- O Audit/Event Log é peça central para rastreabilidade, governança, debugging, segurança operacional e futura explicabilidade.
- A documentação deve diferenciar evento auditável estruturado de log textual operacional.
- A documentação deve deixar claro que ainda não há persistência externa.
- A documentação deve deixar claro que ainda não há banco de dados.
- A documentação deve deixar claro que ainda não há OpenTelemetry.
- A documentação deve deixar claro que eventos não devem registrar conteúdo sensível bruto por padrão.

Entregáveis obrigatórios:
1. Criar documento:
   - docs/architecture/audit-event-architecture.md

2. Atualizar:
   - docs/architecture/module-index.md
   - src/vercosa_ai_framework/audit/README.md

3. Atualizar, se necessário:
   - README.md
   - docs/alignment/architecture-map.md
   - docs/alignment/current-state.md
   - docs/examples/README.md

4. Não alterar código Python.

5. Não alterar scripts shell.

6. Não adicionar dependências.

Requisitos para docs/architecture/audit-event-architecture.md:
1. O documento deve estar em português do Brasil.

2. Explicar o propósito do Audit/Event Log no Vercosa AI Framework.

3. Explicar por que auditoria é necessária em um framework de Harness Engineering.

4. Explicar a diferença entre:
   - log textual operacional;
   - evento auditável estruturado;
   - telemetria externa futura;
   - persistência futura.

5. Explicar que o Audit/Event Log atual é uma fundação inicial, não uma plataforma completa de observabilidade.

6. Documentar categorias de eventos existentes ou previstas no contrato, incluindo:
   - mission;
   - policy;
   - guardian;
   - context;
   - model_selection;
   - runtime;
   - provider;
   - usage_limit;
   - system.

7. Documentar severidades existentes ou previstas no contrato, incluindo:
   - debug;
   - info;
   - warning;
   - error;
   - critical.

8. Documentar resultados existentes ou previstos no contrato, incluindo:
   - success;
   - skipped;
   - warning;
   - failed;
   - blocked;
   - requires_approval.

9. Explicar os campos principais de um evento auditável, como:
   - event_id;
   - category;
   - name;
   - severity;
   - result;
   - message;
   - source;
   - metadata;
   - created_at.

10. Explicar que event_id e created_at devem ser testáveis e previsíveis conforme contrato implementado.

11. Explicar o papel da implementação em memória.

12. Explicar que a implementação em memória serve para:
   - testes;
   - contratos;
   - composição futura;
   - integração inicial;
   - evitar dependências externas nesta fase.

13. Explicar integrações atuais ou helpers existentes para:
   - Policy Engine;
   - Guardian Engine;
   - Context Router;
   - ContextPackage;
   - Mission Runner;
   - batch;
   - Usage/API Limit Guard, se aplicável ao estado atual.

14. Explicar que a integração é opcional quando esse for o caso.

15. Explicar que módulos não devem depender obrigatoriamente do Event Log para funcionar, salvo decisão futura explícita.

16. Explicar cuidados de segurança:
   - não registrar secrets;
   - não registrar credenciais;
   - não registrar tokens de API;
   - não registrar prompts completos por padrão;
   - não registrar conteúdo integral sensível por padrão;
   - preferir metadata mínima;
   - preservar rastreabilidade sem vazar dados.

17. Explicar exemplos de eventos de alto nível, em texto claro:
   - política resolvida;
   - conflito de política;
   - decisão do Guardian;
   - ContextPackage montado;
   - item de contexto omitido;
   - missão iniciada;
   - missão concluída;
   - missão falhou;
   - batch interrompido por quota.

18. Incluir exemplos em blocos Markdown normais quando isso tornar o documento mais claro.

19. Controlar corretamente a quantidade de crases nos blocos Markdown gerados.

20. Não empobrecer a documentação por evitar blocos de comando quando eles forem úteis.

21. Explicar limites atuais:
   - sem persistência externa;
   - sem banco;
   - sem SQLite;
   - sem PostgreSQL;
   - sem OpenTelemetry;
   - sem dashboard;
   - sem exportador;
   - sem correlação completa com Git;
   - sem retenção configurável.

22. Explicar próximos passos possíveis:
   - persistência local controlada;
   - exportação em JSONL;
   - integração com Mission Runner real;
   - integração com Provider Gateway;
   - correlação com commits;
   - relatórios pós-batch;
   - política de retenção;
   - redaction de metadata;
   - auditoria de uso de tools/providers.

23. Não prometer esses próximos passos como implementados.

24. Manter links relativos corretos para:
   - src/vercosa_ai_framework/audit/README.md
   - docs/architecture/module-index.md
   - docs/alignment/architecture-map.md
   - docs/examples/README.md

Requisitos para src/vercosa_ai_framework/audit/README.md:
1. Atualizar para apontar para docs/architecture/audit-event-architecture.md.

2. Manter o README do módulo como visão de módulo, não documentação arquitetural longa.

3. Explicar brevemente os arquivos do módulo:
   - types.py;
   - event_log.py;
   - integrations.py, se existir.

4. Explicar o que está implementado.

5. Explicar o que ainda é futuro.

6. Não prometer persistência externa.

Requisitos para docs/architecture/module-index.md:
1. Garantir que o módulo audit esteja descrito de forma coerente.

2. Adicionar link para docs/architecture/audit-event-architecture.md.

3. Não duplicar o documento inteiro dentro do índice.

Requisitos para README.md:
1. Atualizar somente se houver seção adequada de auditoria, governança ou módulos.

2. Se atualizar, mencionar Audit/Event Log de forma breve e apontar para o documento arquitetural.

3. Não transformar README em documentação longa de auditoria.

Requisitos para docs/alignment/architecture-map.md:
1. Atualizar somente se o mapa não representar Audit/Event Log de forma coerente.

2. Mostrar relação do Audit/Event Log com:
   - Policy Engine;
   - Guardian Engine;
   - Context Router;
   - Mission Runner;
   - Model Selection;
   - Usage/API Limit Guard.

3. Não redesenhar toda a arquitetura sem necessidade.

Requisitos para docs/examples/README.md:
1. Atualizar somente se existir exemplo de audit/event flow ou se for útil apontar para a arquitetura.

2. Não criar exemplo novo nesta missão, salvo se for pequeno e estritamente documental.

Requisitos gerais:
1. Tudo deve estar em português do Brasil.

2. Usar linguagem técnica clara.

3. Diferenciar implementado, MVP, integração inicial, futuro e fora do escopo.

4. Não prometer recursos futuros como implementados.

5. Usar blocos de comando ou JSON nos documentos finais quando úteis, com crases corretas.

6. Não alterar código.

7. Não alterar scripts.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não implementar persistência externa.
- Não implementar JSONL.
- Não implementar banco.
- Não implementar SQLite.
- Não implementar PostgreSQL.
- Não implementar OpenTelemetry.
- Não implementar dashboard.
- Não implementar exportador.
- Não adicionar dependências.
- Não executar missões.
- Não acessar rede.
- Não acessar banco.
- Não chamar OpenAI.
- Não chamar Gemini.
- Não chamar Ollama.
- Não chamar Claude.
- Não chamar OpenCode.
- Não acessar MCPs.
- Não fazer git push.
- Não usar sudo.
- Não alterar configs globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- docs/architecture/audit-event-architecture.md existe.
- O documento explica propósito, categorias, severidades e resultados.
- O documento diferencia log textual, evento estruturado, persistência futura e telemetria futura.
- O documento explica integrações atuais de auditoria.
- O documento registra limites atuais sem prometer recursos futuros.
- O documento inclui cuidados de segurança contra vazamento de dados sensíveis.
- src/vercosa_ai_framework/audit/README.md aponta para o documento arquitetural.
- docs/architecture/module-index.md aponta para o documento arquitetural.
- README.md foi atualizado somente se necessário.
- docs/alignment/architecture-map.md foi atualizado somente se necessário.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
