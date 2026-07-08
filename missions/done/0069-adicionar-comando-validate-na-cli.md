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
- tests/test_worker_scripts.py

Leia também, se existirem após execuções anteriores neste mesmo batch:
- src/vercosa_ai_framework/cli/
- src/vercosa_ai_framework/cli/README.md
- tests/test_cli_operacional_inicial.py
- src/vercosa_ai_framework/audit/
- src/vercosa_ai_framework/audit/README.md

Assuma o papel de:
- cli-engineer;
- reliability-engineer;
- python-implementation-agent;
- test-engineer;
- documentation-agent.

Missão:
Adicionar comando validate à CLI operacional inicial.

Objetivo:
Adicionar um comando local e determinístico de validação à CLI do Vercosa AI Framework, capaz de verificar condições básicas do projeto sem executar missões, sem rodar scripts shell, sem acessar rede e sem alterar arquivos.

Contexto:
- A missão anterior deste batch deve criar uma CLI operacional inicial.
- A CLI inicial deve fornecer comando de ajuda e status básico.
- Agora a CLI deve ganhar um comando validate, ainda pequeno, seguro e local.
- O comando validate deve ajudar a verificar se o estado do projeto está adequado para iniciar uma missão, iniciar um batch ou fazer revisão pós-batch.
- A CLI não deve substituir os scripts shell.
- A CLI não deve executar pytest nesta missão.
- A CLI não deve executar compileall nesta missão.
- A CLI não deve executar git nesta missão.
- A CLI deve apenas validar estrutura local e estado dos diretórios de missão usando Python e biblioteca padrão.

Entregáveis obrigatórios:
1. Atualizar:
   - src/vercosa_ai_framework/cli/main.py
   - src/vercosa_ai_framework/cli/README.md

2. Atualizar, se necessário:
   - src/vercosa_ai_framework/cli/__init__.py

3. Criar ou atualizar teste:
   - tests/test_cli_operacional_inicial.py
   - ou criar tests/test_cli_validate.py se ficar mais organizado

4. Atualizar documentação:
   - README.md, somente se houver seção adequada
   - docs/operations/post-batch-validation-checklist.md, somente se necessário
   - docs/operations/batch-execution-playbook.md, somente se necessário
   - docs/architecture/module-index.md, somente se necessário

5. Não alterar scripts shell.

6. Não adicionar dependências.

Requisitos funcionais:
1. Inspecionar a CLI criada na missão anterior antes de alterar.

2. Adicionar comando validate ou equivalente claro.

3. O comando validate deve aceitar caminho raiz do projeto, quando viável, para facilitar testes.

4. O comando validate deve verificar, no mínimo:
   - se o diretório raiz existe;
   - se existe diretório missions;
   - se existem os diretórios missions/queue, missions/running, missions/done e missions/failed;
   - se não há missão presa em running quando esperado;
   - se a contagem de failed é 0, ou se failed maior que 0 é reportado como problema;
   - se a estrutura básica de src/vercosa_ai_framework existe;
   - se README.md existe.

5. O comando validate deve retornar sucesso quando a estrutura estiver saudável.

6. O comando validate deve retornar erro controlado quando a estrutura estiver inválida.

7. O comando validate deve imprimir mensagens compreensíveis em português do Brasil ou retornar estrutura testável que permita mensagens claras.

8. O comando validate não deve alterar arquivos.

9. O comando validate não deve mover missões.

10. O comando validate não deve executar missões.

11. O comando validate não deve chamar scripts shell.

12. O comando validate não deve chamar git.

13. O comando validate não deve executar pytest.

14. O comando validate não deve executar compileall.

15. O comando validate não deve acessar rede.

16. O comando validate não deve acessar banco.

17. O comando validate não deve chamar LLM.

18. O comando validate não deve chamar provider externo.

19. O comando validate deve ser determinístico.

20. O comando validate deve ser testável com diretório temporário.

21. O design deve permitir validações futuras, como:
   - Git limpo;
   - branch main;
   - pytest;
   - compileall;
   - logs recentes;
   - audit log;
   - políticas;
   - contexto;
   - providers.

22. Não implementar essas validações futuras nesta missão.

Requisitos de testes:
Criar testes cobrindo:
1. O comando validate existe.

2. Validate retorna sucesso para estrutura mínima válida.

3. Validate retorna erro controlado quando missions não existe.

4. Validate retorna erro controlado quando algum subdiretório obrigatório de missions não existe.

5. Validate reporta problema quando failed contém arquivos.

6. Validate reporta problema quando running contém arquivos, se essa for a regra escolhida.

7. Validate verifica existência de README.md.

8. Validate verifica existência de src/vercosa_ai_framework.

9. Validate não altera arquivos.

10. Validate não executa scripts shell.

11. Validate não acessa rede.

12. Validate não exige dependências externas.

13. Comando de status da CLI continua funcionando.

14. Testes existentes continuam passando.

Requisitos de documentação:
1. Tudo deve estar em português do Brasil.

2. Explicar o comando validate.

3. Explicar que validate é uma validação estrutural local.

4. Explicar que validate não substitui pytest.

5. Explicar que validate não substitui python3 -m compileall src.

6. Explicar que validate não substitui vaf-status.sh.

7. Explicar que validate não executa missões.

8. Explicar exemplos de uso em texto simples.

9. Explicar limites atuais.

10. Explicar próximos passos possíveis.

11. Manter links relativos corretos.

12. Não prometer comportamento ainda não implementado.

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
- CLI possui comando validate.
- Validate verifica estrutura mínima do projeto.
- Validate verifica diretórios de missão.
- Validate sinaliza failed maior que 0.
- Validate sinaliza running não vazio, se aplicável.
- Validate é testável com diretório temporário.
- Validate não altera arquivos.
- Validate não executa scripts shell.
- Validate não acessa rede.
- Documentação da CLI foi atualizada.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
