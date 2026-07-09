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
- src/vercosa_ai_framework/missions/
- missions/queue/
- missions/running/
- missions/done/
- missions/failed/

Assuma o papel de:
- cli-engineer;
- test-engineer;
- developer-experience-engineer;
- documentation-agent;
- operations-engineer.

Missão:
Criar comando CLI para listar missões.

Objetivo:
Adicionar à CLI operacional um comando para listar missões por estado, permitindo visualizar missões em queue, running, done e failed de forma segura, local, não destrutiva e compatível com o fluxo operacional atual do projeto.

Contexto:
- A CLI operacional já existe.
- Os comandos status, validate e doctor já existem.
- O projeto possui estrutura de missões em:
  - missions/queue/
  - missions/running/
  - missions/done/
  - missions/failed/
- O script ./scripts/vaf-status.sh já mostra contagens gerais.
- O novo comando de CLI deve complementar os scripts existentes, não substituí-los.
- O batch é o fluxo operacional padrão quando seguro.
- A execução individual continua válida para missões sensíveis.
- O comando de listagem deve ser diagnóstico e leitura.
- O comando não deve mover missões.
- O comando não deve executar missões.
- O comando não deve editar arquivos.
- O comando não deve chamar providers.
- O comando não deve acessar rede.
- O comando não deve depender de banco de dados.
- O comando deve ter testes.
- A documentação deve ser atualizada.

Entregáveis obrigatórios:
1. Atualizar a CLI em:
   - src/vercosa_ai_framework/cli/main.py

2. Criar ou atualizar testes:
   - tests/test_cli_missions.py
   - ou tests/test_cli_list_missions.py
   - ou arquivo de teste já existente da CLI, se for mais coerente

3. Atualizar:
   - src/vercosa_ai_framework/cli/README.md
   - README.md
   - docs/getting-started/local-installation.md
   - docs/getting-started/clean-install-checklist.md
   - docs/operations/safe-runner-usage.md
   - docs/operations/batch-execution-playbook.md
   - docs/roadmap/mission-backlog.md
   - CHANGELOG.md

4. Atualizar, se necessário:
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md
   - docs/release/public-alpha-readiness.md

5. Não alterar scripts shell.

6. Não adicionar dependências.

Requisitos funcionais:
1. Adicionar comando de CLI para listar missões.

2. O nome recomendado do comando é:
   - missions

3. Se a estrutura atual da CLI exigir outro padrão, usar nome coerente com a implementação existente, mas documentar claramente.

4. O comando deve listar missões por estado:
   - queue
   - running
   - done
   - failed

5. O comando deve aceitar filtro opcional por estado, se isso for simples e coerente com a CLI existente.

6. Exemplo conceitual esperado:
   - python3 -m vercosa_ai_framework.cli.main missions
   - python3 -m vercosa_ai_framework.cli.main missions --state queue
   - python3 -m vercosa_ai_framework.cli.main missions --state failed

7. Não inventar entrypoint global se ele não existir.

8. Se a CLI atual usa outra forma de execução, respeitar a forma real.

9. A saída deve ser estável o suficiente para testes.

10. A saída deve incluir contagens por estado.

11. A saída deve listar nomes de arquivos de missão de forma ordenada.

12. A ordenação deve ser determinística.

13. Quando não houver missões em um estado, a saída deve indicar zero ou lista vazia de forma clara.

14. O comando deve funcionar mesmo quando diretórios de missões existirem mas estiverem vazios.

15. O comando deve tratar diretórios ausentes de forma segura:
   - não criar diretórios automaticamente, salvo se a CLI atual já faz isso por contrato;
   - reportar ausência de forma clara;
   - não falhar com traceback não tratado.

16. O comando deve permitir execução a partir da raiz do projeto.

17. Se possível e simples, o comando deve aceitar caminho base do projeto via argumento opcional, mas isso não é obrigatório.

18. O comando não deve depender de Git.

19. O comando não deve fazer git status.

20. O comando não deve substituir ./scripts/vaf-status.sh.

21. O comando não deve executar pytest.

22. O comando não deve executar compileall.

23. O comando não deve acessar logs.

24. O comando não deve mover arquivos.

25. O comando não deve alterar conteúdo de missions/.

26. O comando não deve executar missões.

27. O comando não deve fazer push.

28. O comando não deve chamar OpenCode.

29. O comando não deve chamar modelos.

30. O comando não deve acessar rede.

Requisitos de implementação:
1. Manter a implementação simples.

2. Preferir biblioteca padrão.

3. Não adicionar dependências.

4. Reutilizar padrões existentes da CLI.

5. Preservar compatibilidade dos comandos existentes:
   - status;
   - validate;
   - doctor.

6. Não quebrar testes existentes.

7. Evitar acoplamento indevido com scripts shell.

8. Se houver função auxiliar para resolução de caminho do projeto, reutilizar.

9. Se não houver, criar função pequena, testável e local à CLI ou módulo adequado.

10. Não transformar a CLI em framework complexo nesta missão.

11. Não implementar execução de missões pela CLI nesta missão.

12. Não implementar batch pela CLI nesta missão.

13. Não implementar JSON output nesta missão, salvo se já houver padrão existente e for trivial.

14. Não implementar interface interativa.

15. Não implementar TUI.

16. Não implementar paginação.

17. Não implementar filtros avançados.

18. Não implementar busca textual no conteúdo das missões.

19. Não implementar leitura detalhada do Markdown das missões.

20. Não alterar contratos de outros módulos sem necessidade.

Requisitos de testes:
1. Criar testes para o novo comando.

2. Testar listagem com diretórios contendo arquivos em:
   - queue;
   - running;
   - done;
   - failed.

3. Testar ordenação determinística.

4. Testar filtro por estado se implementado.

5. Testar estado vazio.

6. Testar diretório ausente, se o comportamento for definido.

7. Testar que o comando não altera arquivos.

8. Testar que comandos existentes continuam funcionando, se necessário.

9. Não depender da fila real do projeto para testes.

10. Usar diretório temporário nos testes.

11. Não depender de rede.

12. Não depender de banco.

13. Não chamar providers.

14. Não chamar OpenCode.

15. Garantir que pytest passe.

Requisitos de documentação:
1. Atualizar src/vercosa_ai_framework/cli/README.md com:
   - propósito do comando missions;
   - forma real de execução;
   - exemplos;
   - limites;
   - diferença entre missions e vaf-status.sh.

2. Atualizar README.md de forma breve, se houver seção da CLI.

3. Atualizar docs/getting-started/local-installation.md para incluir o comando como validação opcional da CLI.

4. Atualizar docs/getting-started/clean-install-checklist.md para incluir o comando na validação da CLI.

5. Atualizar docs/operations/safe-runner-usage.md para mencionar que o comando ajuda a inspecionar a fila sem executar missões.

6. Atualizar docs/operations/batch-execution-playbook.md para mencionar uso opcional antes e depois de batch.

7. Atualizar docs/roadmap/mission-backlog.md para marcar comando de listar missões como concluído ou em progresso conforme esta missão.

8. Atualizar CHANGELOG.md na seção Não publicado.

9. Documentação deve estar em português do Brasil.

10. Não prometer comandos futuros como implementados.

11. Não inventar entrypoint global.

12. Usar links relativos corretos.

Restrições:
- Não alterar scripts shell.
- Não executar missões.
- Não implementar comando de execução pela CLI.
- Não implementar comando de batch pela CLI.
- Não implementar comando de mover missões.
- Não implementar comando de criar missões.
- Não implementar comando de excluir missões.
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
- A CLI possui comando para listar missões.
- O comando lista queue, running, done e failed.
- O comando mostra contagens por estado.
- O comando ordena nomes de missão de forma determinística.
- O comando não altera arquivos.
- O comando não executa missões.
- O comando não chama rede, banco, provider ou runtime externo.
- Comandos existentes da CLI continuam funcionando.
- Testes cobrem o novo comando.
- src/vercosa_ai_framework/cli/README.md documenta o comando.
- README.md foi atualizado se necessário.
- docs/getting-started/local-installation.md foi atualizado.
- docs/getting-started/clean-install-checklist.md foi atualizado.
- docs/operations/safe-runner-usage.md foi atualizado.
- docs/operations/batch-execution-playbook.md foi atualizado.
- CHANGELOG.md registra a mudança.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
