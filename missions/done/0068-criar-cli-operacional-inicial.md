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
- scripts/vaf-status.sh
- scripts/vaf-run-next-safe.sh
- scripts/vaf-run-batch-safe.sh
- scripts/vaf-worker.sh
- scripts/vaf-run-one-mission.sh
- src/vercosa_ai_framework/missions/
- src/vercosa_ai_framework/missions/README.md
- src/vercosa_ai_framework/runtime/
- src/vercosa_ai_framework/runtime/README.md
- tests/test_worker_scripts.py

Leia também, se existirem após execuções anteriores neste mesmo batch:
- src/vercosa_ai_framework/audit/
- src/vercosa_ai_framework/audit/README.md
- tests/test_audit_event_log_contracts.py
- tests/test_audit_mission_events.py

Assuma o papel de:
- framework-architect;
- python-implementation-agent;
- cli-engineer;
- reliability-engineer;
- test-engineer;
- documentation-agent.

Missão:
Criar CLI operacional inicial do Vercosa AI Framework.

Objetivo:
Criar uma interface CLI Python inicial, local, determinística e sem dependências externas para consultar informações básicas do projeto, especialmente estado de missões, versão operacional mínima e caminhos relevantes, sem substituir os scripts shell existentes.

Contexto:
- O projeto já possui scripts shell operacionais.
- O usuário opera o framework principalmente por comandos no terminal.
- O runner seguro de uma missão existe.
- O runner seguro em batch existe.
- Os scripts shell continuam sendo a base operacional atual.
- A CLI Python deve começar pequena, como camada de conveniência.
- A CLI não deve alterar o fluxo de missões nesta fase.
- A CLI não deve substituir vaf-status.sh.
- A CLI não deve executar missões nesta fase.
- A CLI deve ser útil para leitura e diagnóstico básico.
- A CLI deve ser implementada apenas com biblioteca padrão do Python.
- A CLI deve ser testável sem acessar rede, banco ou provider externo.

Entregáveis obrigatórios:
1. Criar módulo, se ainda não existir:
   - src/vercosa_ai_framework/cli/

2. Criar arquivos:
   - src/vercosa_ai_framework/cli/__init__.py
   - src/vercosa_ai_framework/cli/main.py
   - src/vercosa_ai_framework/cli/README.md

3. Criar teste:
   - tests/test_cli_operacional_inicial.py

4. Atualizar documentação:
   - README.md, somente se houver seção adequada
   - docs/architecture/module-index.md
   - docs/operations/safe-runner-usage.md, somente se necessário
   - docs/operations/batch-execution-playbook.md, somente se necessário

5. Não alterar scripts shell, salvo documentação cruzada.

6. Não adicionar dependências.

Requisitos funcionais:
1. Inspecionar estrutura atual do pacote src/vercosa_ai_framework antes de implementar.

2. Criar uma função principal invocável em Python, por exemplo main.

3. A CLI deve funcionar com biblioteca padrão.

4. A CLI deve aceitar pelo menos um comando de ajuda.

5. A CLI deve aceitar um comando de status básico, por exemplo:
   - status
   - ou mission-status
   - ou comando equivalente definido de forma clara.

6. O status básico deve ser calculado localmente a partir dos diretórios de missão, quando possível:
   - missions/queue
   - missions/running
   - missions/done
   - missions/failed

7. O status básico deve retornar ou imprimir:
   - quantidade de missões em queue
   - quantidade de missões em running
   - quantidade de missões em done
   - quantidade de missões em failed

8. A CLI deve permitir informar caminho raiz do projeto, quando viável, para facilitar testes.

9. A CLI deve ter comportamento determinístico.

10. A CLI deve ser testável sem executar shell scripts.

11. A CLI não deve chamar vaf-status.sh diretamente nesta missão.

12. A CLI não deve executar missões.

13. A CLI não deve fazer git push.

14. A CLI não deve alterar arquivos.

15. A CLI não deve mover missões entre diretórios.

16. A CLI não deve acessar rede.

17. A CLI não deve acessar banco.

18. A CLI não deve chamar LLM.

19. A CLI não deve chamar provider externo.

20. A CLI não deve depender de OpenCode.

21. A CLI deve tratar diretórios ausentes de forma previsível.

22. A CLI deve retornar código de saída adequado para sucesso e erro de argumentos.

23. O design deve permitir expansão futura para comandos como:
   - run-next
   - run-batch
   - validate
   - audit
   - policy
   - context
   - doctor

24. Não implementar esses comandos futuros nesta missão, apenas documentar como próximos passos.

Requisitos de testes:
Criar testes cobrindo:
1. O módulo cli pode ser importado.

2. A função principal existe.

3. O comando de ajuda retorna sucesso ou texto esperado.

4. O comando de status conta corretamente arquivos em queue, running, done e failed usando diretório temporário.

5. Diretórios de missão ausentes são tratados de forma previsível.

6. Argumento inválido retorna erro controlado.

7. A CLI não executa scripts shell.

8. A CLI não acessa rede.

9. A CLI não exige dependência externa.

10. Testes existentes continuam passando.

Requisitos de documentação:
1. Tudo deve estar em português do Brasil.

2. Explicar que a CLI inicial é uma camada de conveniência.

3. Explicar que a CLI não substitui os scripts shell.

4. Explicar que a CLI não executa missões nesta fase.

5. Explicar que a CLI inicial é somente local e determinística.

6. Explicar comandos implementados.

7. Explicar exemplos de uso, sem blocos cercados por crases dentro da missão.

8. Explicar próximos comandos possíveis, sem prometer que já existem.

9. Explicar limites atuais.

10. Manter links relativos corretos.

11. Não prometer comportamento ainda não implementado.

Restrições:
- Não adicionar dependências.
- Não alterar scripts shell.
- Não executar missões.
- Não implementar run-next na CLI.
- Não implementar run-batch na CLI.
- Não implementar push na CLI.
- Não alterar fluxo queue, running, done e failed.
- Não acessar rede.
- Não acessar banco.
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
- src/vercosa_ai_framework/cli/__init__.py existe.
- src/vercosa_ai_framework/cli/main.py existe.
- src/vercosa_ai_framework/cli/README.md existe.
- tests/test_cli_operacional_inicial.py existe.
- CLI pode ser importada.
- CLI possui comando de ajuda.
- CLI possui comando de status básico ou equivalente.
- Status básico conta missões por diretório.
- CLI não executa scripts shell.
- CLI não altera arquivos.
- CLI não acessa rede.
- Nenhuma dependência foi adicionada.
- Documentação relacionada foi atualizada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
