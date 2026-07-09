Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
- CHANGELOG.md
- docs/getting-started/local-installation.md
- docs/getting-started/clean-install-checklist.md
- docs/release/public-alpha-readiness.md
- docs/release/versioning-policy.md
- docs/release/alpha-version-plan.md
- docs/architecture/module-index.md
- docs/architecture/post-integration-architecture-review.md
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/roadmap/mission-backlog.md
- docs/operations/safe-runner-usage.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md
- src/vercosa_ai_framework/cli/README.md
- src/vercosa_ai_framework/cli/main.py
- src/vercosa_ai_framework/missions/README.md
- tests/test_cli_operacional_inicial.py
- tests/test_cli_validate.py
- tests/test_cli_doctor.py

Leia também, se existirem:
- tests/test_cli_missions.py
- tests/test_cli_list_missions.py
- tests/test_cli_batch_summary.py
- scripts/vaf-run-batch-safe.sh
- scripts/vaf-status.sh
- logs/

Assuma o papel de:
- cli-engineer;
- test-engineer;
- operations-engineer;
- developer-experience-engineer;
- documentation-agent.

Missão:
Criar comando CLI para resumo pós-batch.

Objetivo:
Adicionar à CLI operacional um comando de resumo pós-batch, permitindo visualizar um diagnóstico local, seguro e não destrutivo do estado após execução de batch, com foco em contagens de missões, último log, estado de Git quando possível de forma segura, e lembretes de validação manual, sem substituir os scripts shell e sem executar testes automaticamente.

Contexto:
- A CLI operacional já existe.
- Os comandos status, validate e doctor já existem.
- A missão 0088 deve adicionar comando para listar missões.
- O runner seguro em batch já existe.
- O batch é fluxo operacional padrão quando seguro.
- O checklist pós-batch já existe.
- Atualmente o resumo pós-batch principal vem do script ./scripts/vaf-run-batch-safe.sh.
- A CLI deve complementar o fluxo operacional, não substituir scripts.
- O comando novo deve ser somente leitura.
- O comando não deve executar missões.
- O comando não deve mover arquivos.
- O comando não deve executar pytest.
- O comando não deve executar compileall.
- O comando não deve fazer push.
- O comando não deve chamar providers.
- O comando não deve acessar rede.
- O comando não deve depender de banco de dados.
- O comando deve ter testes.
- A documentação deve ser atualizada.

Entregáveis obrigatórios:
1. Atualizar a CLI em:
   - src/vercosa_ai_framework/cli/main.py

2. Criar ou atualizar testes:
   - tests/test_cli_batch_summary.py
   - ou arquivo de teste existente da CLI, se for mais coerente

3. Atualizar:
   - src/vercosa_ai_framework/cli/README.md
   - README.md
   - docs/getting-started/local-installation.md
   - docs/getting-started/clean-install-checklist.md
   - docs/operations/post-batch-validation-checklist.md
   - docs/operations/batch-execution-playbook.md
   - docs/operations/safe-runner-usage.md
   - docs/roadmap/mission-backlog.md
   - CHANGELOG.md

4. Atualizar, se necessário:
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md
   - docs/release/public-alpha-readiness.md

5. Não alterar scripts shell.

6. Não adicionar dependências.

Requisitos funcionais:
1. Adicionar comando de CLI para resumo pós-batch.

2. Nome recomendado do comando:
   - batch-summary

3. Se a CLI atual exigir outro padrão de nomes, usar nome coerente com a implementação existente e documentar.

4. Exemplo conceitual esperado:
   - python3 -m vercosa_ai_framework.cli.main batch-summary

5. Não inventar entrypoint global se ele não existir.

6. A saída deve incluir, quando possível:
   - contagem de missions/queue;
   - contagem de missions/running;
   - contagem de missions/done;
   - contagem de missions/failed;
   - último arquivo de log encontrado;
   - indicação de worker não verificado pela CLI, se a CLI não conseguir verificar com segurança;
   - lembrete para rodar pytest;
   - lembrete para rodar python3 -m compileall src;
   - lembrete para verificar git status --short;
   - lembrete para fazer push somente após validação.

7. O comando deve ser seguro e somente leitura.

8. O comando deve funcionar a partir da raiz do projeto.

9. O comando deve usar diretórios locais do projeto.

10. O comando deve tratar diretórios vazios.

11. O comando deve tratar diretórios ausentes sem traceback não tratado.

12. O comando deve listar o último log de forma determinística, preferencialmente por modificação ou nome, conforme for mais simples e testável.

13. A saída deve ser estável o suficiente para testes.

14. O comando não deve executar:
   - pytest;
   - compileall;
   - git push;
   - git add;
   - git commit;
   - scripts shell;
   - missões;
   - OpenCode;
   - providers;
   - modelos.

15. O comando não deve alterar:
   - missions/queue;
   - missions/running;
   - missions/done;
   - missions/failed;
   - logs;
   - arquivos de documentação;
   - estado Git.

16. O comando não deve prometer que validação foi feita.

17. O comando deve deixar claro que é diagnóstico auxiliar.

18. O comando não substitui:
   - ./scripts/vaf-status.sh;
   - docs/operations/post-batch-validation-checklist.md;
   - pytest;
   - python3 -m compileall src;
   - revisão dos logs;
   - revisão dos commits.

19. Se houver falha em missions/failed, a saída deve indicar atenção.

20. Se houver arquivo em missions/running, a saída deve indicar atenção.

21. Se queue não estiver vazia, a saída deve indicar que ainda há missões pendentes.

22. Se queue=0, running=0 e failed=0, a saída pode indicar estado operacional aparentemente limpo, mas sem afirmar validação completa.

Requisitos de implementação:
1. Manter implementação simples.

2. Usar apenas biblioteca padrão.

3. Não adicionar dependências.

4. Reutilizar padrões existentes da CLI.

5. Preservar compatibilidade dos comandos existentes:
   - status;
   - validate;
   - doctor;
   - missions, se já tiver sido implementado pela missão 0088.

6. Não quebrar testes existentes.

7. Evitar acoplamento com scripts shell.

8. Não implementar execução de batch pela CLI nesta missão.

9. Não implementar auto-push.

10. Não implementar JSON output nesta missão, salvo se já existir padrão e for trivial.

11. Não implementar interface interativa.

12. Não implementar TUI.

13. Não implementar análise profunda dos logs.

14. Não implementar leitura completa do conteúdo dos logs.

15. Não implementar parsing complexo do resumo do batch.

16. Não implementar consulta ao remoto Git.

17. Não acessar rede.

18. Não alterar contratos de outros módulos sem necessidade.

Requisitos de testes:
1. Criar testes para o novo comando.

2. Testar cenário com:
   - queue vazio;
   - running vazio;
   - done com arquivos;
   - failed vazio;
   - logs com pelo menos um arquivo.

3. Testar cenário com failed contendo arquivo.

4. Testar cenário com running contendo arquivo.

5. Testar cenário com queue contendo arquivo.

6. Testar cenário sem logs.

7. Testar diretórios ausentes, se o comportamento for definido.

8. Testar que o comando não altera arquivos.

9. Testar que a saída contém lembretes de validação.

10. Não depender da fila real do projeto para testes.

11. Usar diretório temporário nos testes.

12. Não depender de rede.

13. Não depender de banco.

14. Não chamar providers.

15. Não chamar OpenCode.

16. Garantir que pytest passe.

Requisitos de documentação:
1. Atualizar src/vercosa_ai_framework/cli/README.md com:
   - propósito do comando batch-summary;
   - forma real de execução;
   - exemplos;
   - limites;
   - diferença entre batch-summary, vaf-status.sh e checklist pós-batch.

2. Atualizar README.md de forma breve, se houver seção da CLI.

3. Atualizar docs/getting-started/local-installation.md para incluir o comando como validação opcional.

4. Atualizar docs/getting-started/clean-install-checklist.md para incluir o comando na validação da CLI.

5. Atualizar docs/operations/post-batch-validation-checklist.md para mencionar batch-summary como diagnóstico complementar.

6. Atualizar docs/operations/batch-execution-playbook.md para mencionar uso opcional após batch.

7. Atualizar docs/operations/safe-runner-usage.md para mencionar que o comando não executa missões.

8. Atualizar docs/roadmap/mission-backlog.md para marcar comando de resumo pós-batch como concluído ou em progresso conforme esta missão.

9. Atualizar CHANGELOG.md na seção Não publicado.

10. Documentação deve estar em português do Brasil.

11. Não prometer comandos futuros como implementados.

12. Não inventar entrypoint global.

13. Usar links relativos corretos.

Restrições:
- Não alterar scripts shell.
- Não executar missões.
- Não implementar comando de execução pela CLI.
- Não implementar comando de batch pela CLI.
- Não implementar comando de mover missões.
- Não implementar comando de criar missões.
- Não implementar comando de excluir missões.
- Não executar pytest dentro do comando.
- Não executar compileall dentro do comando.
- Não executar git push dentro do comando.
- Não executar git commit dentro do comando.
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
- Não fazer git push.
- Não usar sudo.
- Não alterar configs globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação, testes e mensagens devem estar em português do Brasil quando aplicável.

Critérios de aceite:
- A CLI possui comando de resumo pós-batch.
- O comando mostra contagens de queue, running, done e failed.
- O comando mostra o último log quando houver.
- O comando indica atenção quando há running ou failed.
- O comando lembra que pytest e compileall devem ser executados manualmente.
- O comando não altera arquivos.
- O comando não executa missões.
- O comando não chama rede, banco, provider ou runtime externo.
- Comandos existentes da CLI continuam funcionando.
- Testes cobrem o novo comando.
- src/vercosa_ai_framework/cli/README.md documenta o comando.
- README.md foi atualizado se necessário.
- docs/getting-started/local-installation.md foi atualizado.
- docs/getting-started/clean-install-checklist.md foi atualizado.
- docs/operations/post-batch-validation-checklist.md foi atualizado.
- docs/operations/batch-execution-playbook.md foi atualizado.
- CHANGELOG.md registra a mudança.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
