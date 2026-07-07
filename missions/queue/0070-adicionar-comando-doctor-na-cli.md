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

Leia também, se existirem após execuções anteriores neste mesmo batch:
- src/vercosa_ai_framework/cli/
- src/vercosa_ai_framework/cli/README.md
- src/vercosa_ai_framework/cli/main.py
- tests/test_cli_operacional_inicial.py
- tests/test_cli_validate.py

Assuma o papel de:
- cli-engineer;
- reliability-engineer;
- python-implementation-agent;
- test-engineer;
- documentation-agent.

Missão:
Adicionar comando doctor à CLI operacional.

Objetivo:
Adicionar um comando doctor à CLI do Vercosa AI Framework para executar um diagnóstico local, determinístico e não destrutivo do projeto, combinando verificações estruturais já existentes com mensagens operacionais mais úteis, sem executar missões, sem rodar scripts shell, sem acessar rede e sem alterar arquivos.

Contexto:
- A missão 0068 deve criar a CLI operacional inicial.
- A missão 0069 deve adicionar o comando validate.
- O comando validate faz validações estruturais básicas.
- O comando doctor deve ser uma camada de diagnóstico mais amigável, construída sobre validações locais.
- O doctor deve ajudar o usuário a entender se o projeto parece pronto para:
  - iniciar uma missão;
  - iniciar um batch;
  - investigar falhas;
  - revisar estado pós-batch.
- O doctor não deve substituir scripts shell.
- O doctor não deve executar pytest.
- O doctor não deve executar compileall.
- O doctor não deve executar git.
- O doctor não deve acessar rede.
- O doctor deve ser implementado apenas com biblioteca padrão do Python.

Entregáveis obrigatórios:
1. Atualizar:
   - src/vercosa_ai_framework/cli/main.py
   - src/vercosa_ai_framework/cli/README.md

2. Atualizar, se necessário:
   - src/vercosa_ai_framework/cli/__init__.py

3. Criar ou atualizar testes:
   - tests/test_cli_validate.py
   - ou tests/test_cli_operacional_inicial.py
   - ou criar tests/test_cli_doctor.py se ficar mais organizado

4. Atualizar documentação:
   - README.md, somente se houver seção adequada
   - docs/operations/post-batch-validation-checklist.md, somente se necessário
   - docs/operations/batch-execution-playbook.md, somente se necessário
   - docs/architecture/module-index.md, somente se necessário

5. Não alterar scripts shell.

6. Não adicionar dependências.

Requisitos funcionais:
1. Inspecionar a CLI existente antes de alterar.

2. Inspecionar o comando validate criado na missão anterior antes de implementar doctor.

3. Adicionar comando doctor ou equivalente claro.

4. O comando doctor deve aceitar caminho raiz do projeto, quando viável, para facilitar testes.

5. O comando doctor deve executar verificações locais e não destrutivas.

6. O comando doctor deve verificar, no mínimo:
   - diretório raiz existe;
   - README.md existe;
   - src/vercosa_ai_framework existe;
   - diretório missions existe;
   - diretórios missions/queue, missions/running, missions/done e missions/failed existem;
   - contagem de arquivos em queue;
   - contagem de arquivos em running;
   - contagem de arquivos em done;
   - contagem de arquivos em failed;
   - se running está vazio;
   - se failed está vazio;
   - se docs/operations/post-batch-validation-checklist.md existe, quando aplicável;
   - se docs/roadmap/mission-backlog.md existe, quando aplicável.

7. O comando doctor deve produzir resultado claro, com status geral como:
   - ok;
   - warning;
   - error.

8. O comando doctor deve retornar código de saída:
   - 0 quando o diagnóstico estiver saudável;
   - diferente de 0 quando houver erro estrutural relevante.

9. Warnings podem ser reportados sem necessariamente retornar erro, desde que documentado.

10. O comando doctor deve reaproveitar lógica do validate quando fizer sentido, sem duplicação excessiva.

11. O comando doctor não deve alterar arquivos.

12. O comando doctor não deve mover missões.

13. O comando doctor não deve executar missões.

14. O comando doctor não deve chamar scripts shell.

15. O comando doctor não deve chamar git.

16. O comando doctor não deve executar pytest.

17. O comando doctor não deve executar compileall.

18. O comando doctor não deve acessar rede.

19. O comando doctor não deve acessar banco.

20. O comando doctor não deve chamar LLM.

21. O comando doctor não deve chamar provider externo.

22. O comando doctor deve ser determinístico.

23. O comando doctor deve ser testável com diretório temporário.

24. O design deve permitir diagnósticos futuros, como:
   - Git limpo;
   - branch main;
   - pytest;
   - compileall;
   - logs recentes;
   - audit log;
   - provider health;
   - limites de API.

25. Não implementar esses diagnósticos futuros nesta missão.

Requisitos de testes:
Criar testes cobrindo:
1. O comando doctor existe.

2. Doctor retorna sucesso para estrutura mínima saudável.

3. Doctor retorna erro controlado quando missions não existe.

4. Doctor retorna erro controlado quando src/vercosa_ai_framework não existe.

5. Doctor reporta problema quando failed contém arquivos.

6. Doctor reporta problema quando running contém arquivos.

7. Doctor reporta contagens de queue, running, done e failed.

8. Doctor trata ausência de documentos opcionais como warning ou informação, conforme regra implementada.

9. Doctor não altera arquivos.

10. Doctor não executa scripts shell.

11. Doctor não chama git.

12. Doctor não executa pytest.

13. Doctor não executa compileall.

14. Doctor não acessa rede.

15. Doctor não exige dependências externas.

16. Comando validate continua funcionando.

17. Comando status continua funcionando.

18. Testes existentes continuam passando.

Requisitos de documentação:
1. Tudo deve estar em português do Brasil.

2. Explicar o comando doctor.

3. Explicar diferença entre status, validate e doctor.

4. Explicar que doctor é diagnóstico local e não destrutivo.

5. Explicar que doctor não substitui pytest.

6. Explicar que doctor não substitui python3 -m compileall src.

7. Explicar que doctor não substitui vaf-status.sh.

8. Explicar que doctor não executa missões.

9. Explicar exemplos de uso em texto simples.

10. Explicar limites atuais.

11. Explicar próximos passos possíveis.

12. Manter links relativos corretos.

13. Não prometer comportamento ainda não implementado.

Restrições:
- Não adicionar dependências.
- Não alterar scripts shell.
- Não executar missões.
- Não implementar run-next na CLI.
- Não implementar run-batch na CLI.
- Não implementar push na CLI.
- Não executar git.
- Não executar pytest dentro da CLI.
- Não executar compileall dentro da CLI.
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
- CLI possui comando doctor.
- Doctor executa diagnóstico local não destrutivo.
- Doctor verifica estrutura básica do projeto.
- Doctor verifica diretórios de missão.
- Doctor reporta contagens de queue, running, done e failed.
- Doctor sinaliza failed maior que 0.
- Doctor sinaliza running não vazio.
- Doctor é testável com diretório temporário.
- Doctor não altera arquivos.
- Doctor não executa scripts shell.
- Doctor não acessa rede.
- Documentação da CLI foi atualizada.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
