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
- docs/examples/mission-batch-operational-flow.md
- scripts/vaf-run-next-safe.sh
- scripts/vaf-run-batch-safe.sh
- scripts/vaf-status.sh
- scripts/vaf-worker.sh
- scripts/vaf-run-one-mission.sh
- tests/test_worker_scripts.py

Assuma o papel de:
- operations-engineer;
- reliability-engineer;
- documentation-agent;
- framework-architect;
- process-governance-agent.

Missão:
Padronizar execução em batch como fluxo operacional do projeto.

Objetivo:
Atualizar a documentação operacional e o README para registrar que a execução em batch passa a ser o fluxo operacional padrão do Vercosa AI Framework quando o bloco de missões estiver bem especificado, revisado e seguro, mantendo a execução individual para missões críticas, sensíveis ou de alto risco.

Contexto:
- O projeto já possui runner seguro de uma missão.
- O projeto já possui runner seguro em batch.
- O batch de 3 missões foi testado, validado e publicado.
- O primeiro bloco de 10 missões foi concluído após retomada de limite externo de API.
- O batch de 10 executou missões reais de integração, auditoria, CLI e documentação.
- O projeto agora pode adotar execução em batch como padrão operacional, desde que mantenha governança.
- O batch não deve significar execução cega.
- O batch não deve substituir missões completas em Markdown.
- O batch não deve eliminar revisão.
- O batch não deve eliminar testes.
- O batch não deve eliminar compileall.
- O batch não deve eliminar commits separados.
- A execução individual continua necessária para mudanças sensíveis, arquiteturais, arriscadas ou incertas.
- Erros de usage limit, quota, rate limit ou 429 devem suspender o batch.

Entregáveis obrigatórios:
1. Atualizar:
   - README.md
   - docs/operations/batch-execution-playbook.md
   - docs/operations/post-batch-validation-checklist.md
   - docs/operations/safe-runner-usage.md
   - docs/roadmap/mission-backlog.md

2. Atualizar, se necessário:
   - docs/alignment/roadmap.md
   - docs/alignment/current-state.md
   - docs/examples/mission-batch-operational-flow.md

3. Não alterar código Python.

4. Não alterar scripts shell.

5. Não adicionar dependências.

Requisitos funcionais/documentais:
1. Registrar que o fluxo operacional padrão passa a ser execução em batch quando as condições de segurança forem atendidas.

2. Registrar que a execução individual continua existindo e deve ser usada para:
   - mudanças arquiteturais profundas;
   - alterações em scripts críticos;
   - alterações no Guardian Engine com impacto amplo;
   - alterações no Policy Engine com impacto amplo;
   - alterações no Context Router com impacto amplo;
   - alterações em providers ou runtimes;
   - missões com dependências incertas;
   - missões com critérios de aceite fracos;
   - recuperação após falha;
   - investigação de erro;
   - limite de API ou quota recém-ocorrido.

3. Registrar que o batch padrão deve usar:
   - missões completas em Markdown;
   - uma missão por arquivo;
   - referências obrigatórias;
   - escopo claro;
   - restrições claras;
   - critérios de aceite claros;
   - commits separados;
   - parada na primeira falha;
   - validação após execução;
   - push manual por padrão.

4. Registrar que o batch padrão recomendado é:
   - VAF_BATCH_SIZE=10 para blocos normais já revisados;
   - VAF_BATCH_SIZE=3 para testes, retomadas, blocos pequenos ou recuperação;
   - execução individual para missões sensíveis.

5. Registrar que VAF_AUTO_PUSH continua opt-in e não deve ser padrão.

6. Registrar que push manual continua sendo a prática recomendada após validação.

7. Registrar que o batch deve ser suspenso se ocorrer:
   - usage limit;
   - quota exceeded;
   - insufficient quota;
   - rate limit;
   - erro 429;
   - falha em pytest;
   - falha em compileall;
   - missão em failed;
   - missão presa em running;
   - Git sujo;
   - dúvida sobre a entrega;
   - alteração fora do escopo.

8. Registrar que, se o batch for interrompido por limite externo de API:
   - não é bug interno do projeto;
   - não se deve insistir em retries;
   - deve-se parar;
   - verificar estado de missions/queue, missions/running, missions/done e missions/failed;
   - devolver missão presa em running para queue quando seguro;
   - continuar depois que a quota estiver disponível.

9. Atualizar o playbook para deixar claro o novo padrão:
   - batch é fluxo normal;
   - execução individual é fluxo especial para risco alto;
   - batch de 3 é fluxo de validação ou retomada;
   - batch de 10 é fluxo operacional padrão quando seguro.

10. Atualizar o checklist pós-batch para refletir que ele é obrigatório antes de push.

11. Atualizar safe-runner-usage para explicar a relação entre:
   - vaf-run-next-safe.sh;
   - vaf-run-batch-safe.sh;
   - fluxo padrão;
   - fluxo sensível.

12. Atualizar mission-backlog para refletir que batch virou padrão operacional.

13. Atualizar README com uma seção curta sobre fluxo operacional padrão, sem transformar README em manual longo.

14. Atualizar exemplos operacionais se estiverem desatualizados.

15. Não alterar scripts nesta missão.

16. Não implementar nova lógica de batch nesta missão.

17. Não alterar VAF_BATCH_SIZE.

18. Não aumentar limite máximo de batch além de 10.

19. Não alterar comportamento de push automático.

20. Não executar missões nesta missão.

21. Não chamar providers.

22. Não acessar rede.

23. Não acessar banco.

Requisitos de documentação:
1. Tudo deve estar em português do Brasil.

2. Usar linguagem direta e operacional.

3. Diferenciar claramente:
   - padrão operacional;
   - exceção;
   - recuperação;
   - investigação.

4. Não dizer que batch é obrigatório para todos os casos.

5. Não dizer que execução individual está obsoleta.

6. Não dizer que batch elimina revisão.

7. Não dizer que batch elimina validação.

8. Não prometer automação que ainda não existe.

9. Manter links relativos corretos.

10. Evitar duplicação excessiva entre README, playbook e checklist.

11. README deve ser sintético.

12. Playbook deve ser detalhado.

13. Checklist deve ser prático.

14. Backlog deve refletir a decisão.

15. Exemplos devem continuar coerentes.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não implementar novas funcionalidades.
- Não adicionar dependências.
- Não aumentar limite máximo do batch.
- Não alterar push automático.
- Não alterar fluxo Git.
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
- README.md menciona o fluxo operacional padrão em batch.
- docs/operations/batch-execution-playbook.md registra batch como fluxo padrão quando seguro.
- docs/operations/post-batch-validation-checklist.md registra validação obrigatória antes de push.
- docs/operations/safe-runner-usage.md diferencia runner individual e runner em batch.
- docs/roadmap/mission-backlog.md reflete que batch virou padrão operacional.
- Documentação deixa claro que execução individual continua válida para missões sensíveis.
- Documentação deixa claro que batch deve parar na primeira falha.
- Documentação deixa claro que VAF_AUTO_PUSH não é padrão.
- Documentação deixa claro que usage limit/quota/rate limit suspende batch.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
