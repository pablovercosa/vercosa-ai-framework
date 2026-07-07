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
- docs/operations/safe-runner-usage.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md
- src/vercosa_ai_framework/guardian/usage_limits.py
- src/vercosa_ai_framework/guardian/README.md
- src/vercosa_ai_framework/runtime/
- src/vercosa_ai_framework/runtime/README.md
- src/vercosa_ai_framework/providers/
- src/vercosa_ai_framework/providers/README.md
- scripts/vaf-run-one-mission.sh
- scripts/vaf-worker.sh
- scripts/vaf-run-next-safe.sh
- scripts/vaf-run-batch-safe.sh
- scripts/vaf-status.sh
- tests/test_usage_limit_guard.py
- tests/test_worker_scripts.py

Assuma o papel de:
- reliability-engineer;
- shell-maintenance-agent;
- python-implementation-agent;
- test-engineer;
- framework-architect.

Missão:
Integrar Usage/API Limit Guard ao fluxo operacional do worker de forma inicial e segura.

Objetivo:
Permitir que sinais de limite de uso, quota, rate limit, erro 429 ou crédito insuficiente detectados pelo Usage/API Limit Guard sejam refletidos no fluxo operacional do worker ou dos runners seguros, sem retry infinito, sem classificação errada como bug interno e sem integração com billing real.

Contexto:
- O Usage/API Limit Guard inicial já existe em src/vercosa_ai_framework/guardian/usage_limits.py.
- Ele detecta mensagens de limite de uso de forma determinística.
- O projeto já enfrentou erro real de limite de API em missões anteriores.
- O worker e os runners seguros devem conseguir sinalizar esse tipo de falha com clareza.
- O objetivo desta missão não é consultar API externa nem billing real.
- O objetivo também não é alterar agressivamente o fluxo de execução.
- A integração deve ser mínima, segura e testável.
- O worker não deve entrar em loop quando houver sinal claro de quota/rate limit.
- Falhas de limite externo devem ser distinguíveis de falhas de implementação.

Entregáveis obrigatórios:
1. Atualizar, se necessário:
   - src/vercosa_ai_framework/guardian/usage_limits.py

2. Criar ou atualizar um utilitário operacional pequeno, se necessário, em local coerente com a arquitetura existente.

3. Atualizar scripts apenas se for seguro e necessário:
   - scripts/vaf-run-one-mission.sh
   - scripts/vaf-worker.sh
   - scripts/vaf-run-next-safe.sh
   - scripts/vaf-run-batch-safe.sh

4. Criar ou atualizar testes:
   - tests/test_usage_limit_guard.py
   - tests/test_worker_scripts.py
   - ou novo teste específico para integração operacional.

5. Atualizar documentação:
   - src/vercosa_ai_framework/guardian/README.md
   - docs/operations/safe-runner-usage.md
   - docs/operations/batch-execution-playbook.md
   - docs/operations/post-batch-validation-checklist.md
   - docs/architecture/module-index.md, somente se necessário.

6. Atualizar README.md somente se necessário.

Requisitos funcionais:
1. Inspecionar o Usage/API Limit Guard existente antes de alterar qualquer coisa.

2. Inspecionar scripts do worker e runners seguros antes de alterar qualquer coisa.

3. Identificar qual é o ponto mais seguro para detectar mensagens de erro de limite:
   - no log da missão;
   - no retorno do runner;
   - em utilitário Python;
   - em verificação pós-falha do shell.

4. Criar integração mínima para reconhecer sinais de limite de uso quando uma missão falhar por mensagem conhecida.

5. A integração deve preservar a mensagem original.

6. A integração deve classificar o erro como limitação externa quando aplicável.

7. A integração deve recomendar parada segura do worker quando o erro indicar:
   - usage limit has been reached;
   - quota exceeded;
   - insufficient quota;
   - billing hard limit;
   - rate limit persistente;
   - erro 429 associado a limite.

8. A integração não deve mascarar falhas normais de teste, sintaxe, código ou documentação.

9. A integração deve ser case-insensitive.

10. A integração deve ser determinística.

11. A integração deve registrar mensagem clara no log ou saída operacional quando encontrar limite externo.

12. Se alterar scripts shell, manter a mudança pequena e defensiva.

13. Se criar comando auxiliar Python, manter sem dependências externas.

14. Não consultar OpenAI, Gemini, Ollama, Claude ou qualquer provider.

15. Não acessar rede.

16. Não acessar banco.

17. Não implementar billing real.

18. Não implementar leitura de dashboard externo.

19. Não implementar retry automático avançado.

20. Não transformar Usage/API Limit Guard em Guardian Engine completo.

21. Não alterar sem necessidade o comportamento de missões bem-sucedidas.

22. Não quebrar o runner seguro de uma missão.

23. Não quebrar o runner seguro em batch.

24. Não quebrar testes existentes.

Requisitos de testes:
Criar ou atualizar testes cobrindo:
1. Detecção já existente continua funcionando.

2. Mensagem de uso excedido gera recomendação de parada ou retry futuro conforme contrato.

3. Mensagem de quota excedida gera classificação adequada.

4. Mensagem de erro 429 associada a rate limit gera classificação adequada.

5. Mensagem de erro comum de teste não é classificada como limite de uso.

6. Mensagem de erro de sintaxe não é classificada como limite de uso.

7. Scripts mencionam ou integram o guard apenas no ponto pretendido.

8. Runner seguro em batch continua mencionando parada na primeira falha.

9. A integração não exige rede.

10. A integração não exige dependência nova.

11. Testes existentes continuam passando.

Requisitos de documentação:
1. Tudo deve estar em português do Brasil.

2. Explicar que o Usage/API Limit Guard é determinístico.

3. Explicar que ele não consulta billing real.

4. Explicar que ele não chama provider externo.

5. Explicar que ele ajuda a distinguir falha externa de limite de uso de bug interno.

6. Explicar como o worker ou runner sinaliza esse tipo de falha.

7. Explicar que a ação segura é parar e investigar limites do provider.

8. Explicar que batch de 10 deve ser suspenso se houver erro de quota/rate limit.

9. Explicar próximos passos possíveis:
   - event log;
   - classificação estruturada de falhas;
   - integração futura com Provider Gateway;
   - backoff configurável futuro.

10. Não prometer consulta automática de billing.

11. Não prometer retry inteligente ainda não implementado.

12. Manter links relativos corretos.

Restrições:
- Não adicionar dependências.
- Não chamar OpenAI.
- Não chamar Gemini.
- Não chamar Ollama.
- Não chamar Claude.
- Não chamar OpenCode diretamente.
- Não acessar MCPs.
- Não acessar rede.
- Não acessar banco.
- Não implementar billing real.
- Não implementar retry automático avançado.
- Não implementar backoff distribuído.
- Não alterar configs globais.
- Não usar sudo.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- Usage/API Limit Guard continua com testes passando.
- Existe integração operacional mínima ou documentação clara caso a integração direta não seja segura.
- Falhas de quota/rate limit podem ser reconhecidas no fluxo operacional.
- Falhas comuns não são mascaradas como limite de uso.
- Runner seguro de uma missão continua funcionando.
- Runner seguro em batch continua funcionando.
- Documentação operacional foi atualizada.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
