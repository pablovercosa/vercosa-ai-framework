Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- scripts/vaf-run-one-mission.sh
- scripts/vaf-worker.sh
- scripts/vaf-start-background.sh
- scripts/vaf-stop-background.sh
- scripts/vaf-status.sh
- tests/test_worker_scripts.py

Assuma o papel de shell-maintenance-agent, test-engineer e framework-architect.

Missão:
Criar um runner seguro de missão.

Objetivo:
Criar um script de alto nível para executar a próxima missão da fila com mínima intervenção manual, validando o estado do Git, executando o worker, rodando testes, compilando o pacote e, opcionalmente, fazendo push automático de forma segura.

Nome esperado do script:
- scripts/vaf-run-next-safe.sh

Comando desejado:
- ./scripts/vaf-run-next-safe.sh

Com push opcional:
- VAF_AUTO_PUSH=1 ./scripts/vaf-run-next-safe.sh

Com mensagem de commit customizada:
- VAF_COMMIT_MESSAGE="implementação: exemplo" ./scripts/vaf-run-next-safe.sh

Entregáveis obrigatórios:
- criar scripts/vaf-run-next-safe.sh;
- tornar o script executável;
- atualizar README.md com uso do novo script;
- atualizar tests/test_worker_scripts.py ou criar teste específico para o novo script;
- atualizar documentação relacionada, se necessário.

Requisitos funcionais do script:
1. Usar bash com `set -euo pipefail`.
2. Determinar automaticamente a raiz do repositório.
3. Entrar na raiz do repositório antes de executar comandos.
4. Verificar se o Git está limpo antes de iniciar.
5. Se houver alterações pendentes antes da execução, abortar com mensagem clara.
6. Verificar se não há worker em execução antes de iniciar.
7. Executar apenas 1 ciclo de missão por padrão.
8. Usar:
   - VAF_MAX_CYCLES=1 por padrão;
   - VAF_AUTO_APPROVE=1 por padrão;
   - VAF_AUTO_COMMIT=1 por padrão.
9. Preservar VAF_COMMIT_MESSAGE quando fornecida.
10. Se VAF_COMMIT_MESSAGE não for fornecida, permitir que o worker use o padrão pt-BR já implementado.
11. Executar o worker em foreground, ou outro modo seguro que permita aguardar a conclusão.
12. Após a missão, rodar:
   - pytest;
   - python3 -m compileall src.
13. Verificar status final do worker usando scripts existentes quando apropriado.
14. Verificar que:
   - queue/running não ficaram inconsistentes;
   - failed continua 0, ou abortar se houver falha;
   - git status está limpo quando VAF_AUTO_COMMIT=1.
15. Se VAF_AUTO_COMMIT=0, aceitar alterações pendentes, mas informar claramente que commit manual é necessário.
16. Não fazer push por padrão.
17. Fazer push somente se VAF_AUTO_PUSH=1.
18. Antes do push automático, exigir:
   - branch atual seja main;
   - git status limpo;
   - pytest tenha passado;
   - compileall tenha passado;
   - worker parado;
   - failed = 0;
   - remoto origin configurado.
19. Se qualquer validação falhar, não fazer push.
20. Ao final, imprimir resumo com:
   - último commit;
   - status das missões;
   - resultado dos testes;
   - se houve push ou não.

Requisitos de segurança:
- VAF_AUTO_PUSH deve ser opt-in, nunca padrão.
- Não usar sudo.
- Não alterar configurações globais.
- Não fazer force push.
- Não apagar logs.
- Não apagar missões.
- Não executar mais de uma missão por padrão.
- Não mascarar falhas.
- Não continuar após erro de teste.
- Não continuar após erro de compileall.
- Não fazer push se houver alterações locais.
- Não fazer push se a branch não for main, salvo se uma variável explícita futura for implementada; não implementar essa exceção agora.

Requisitos de teste:
- Validar sintaxe com bash -n.
- Adicionar teste que confirme que scripts/vaf-run-next-safe.sh existe.
- Adicionar teste que confirme que o script é executável.
- Adicionar teste textual simples confirmando presença de proteções importantes:
  - `set -euo pipefail`;
  - `VAF_AUTO_PUSH`;
  - `VAF_AUTO_COMMIT`;
  - `pytest`;
  - `compileall`;
  - `git push`;
  - checagem de git status.
- Manter testes existentes passando.

Requisitos de documentação:
- Tudo em português do Brasil.
- Documentar uso básico:
  `./scripts/vaf-run-next-safe.sh`
- Documentar uso com push:
  `VAF_AUTO_PUSH=1 ./scripts/vaf-run-next-safe.sh`
- Documentar uso com mensagem customizada:
  `VAF_COMMIT_MESSAGE="implementação: exemplo" ./scripts/vaf-run-next-safe.sh`
- Explicar que push automático é opcional.
- Explicar que o script aborta se o Git não estiver limpo.
- Explicar que o script executa apenas uma missão por padrão.
- Não prometer execução assíncrona externa.
- Não prometer que o ChatGPT executa comandos no servidor.

Regra de commit automático:
Se esta missão gerar commit automático, a mensagem deve estar em português do Brasil.
Não usar o prefixo `mission:`.
Usar a mensagem fornecida por VAF_COMMIT_MESSAGE quando existir.

Restrições:
- não alterar src/;
- não adicionar dependências;
- não acessar rede, exceto `git push` quando VAF_AUTO_PUSH=1 no script criado;
- não chamar providers externos;
- não chamar LLMs externos;
- não alterar .opencode;
- não alterar node_modules;
- não reescrever histórico Git;
- não fazer force push;
- documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- scripts/vaf-run-next-safe.sh existe;
- scripts/vaf-run-next-safe.sh é executável;
- bash -n passa nos scripts relevantes;
- pytest passa;
- python3 -m compileall src passa;
- README.md documenta o novo runner seguro;
- auto-commit desta missão usa mensagem em português do Brasil.
