Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- scripts/vaf-run-next-safe.sh
- scripts/vaf-status.sh
- tests/test_worker_scripts.py

Assuma o papel de documentation-architect e test-engineer.

Missão:
Testar o runner seguro com uma missão documental simples.

Objetivo:
Validar o uso de `scripts/vaf-run-next-safe.sh` em uma missão de baixo risco, sem alterar código de produção, confirmando que o fluxo seguro de execução, testes, compileall, auto-commit e documentação funciona como esperado.

Entregáveis obrigatórios:
- criar docs/operations/safe-runner-usage.md;
- atualizar README.md com link para o documento, se ainda não houver;
- atualizar tests/test_worker_scripts.py apenas se necessário para cobrir documentação ou presença do runner;
- não alterar src/.

Requisitos de documentação:
1. Explicar o propósito do runner seguro.
2. Documentar uso básico:
   `./scripts/vaf-run-next-safe.sh`
3. Documentar uso com push automático:
   `VAF_AUTO_PUSH=1 ./scripts/vaf-run-next-safe.sh`
4. Documentar uso com mensagem customizada:
   `VAF_COMMIT_MESSAGE="implementação: exemplo" ./scripts/vaf-run-next-safe.sh`
5. Explicar pré-condições:
   - Git limpo;
   - worker parado;
   - uma missão na fila;
   - branch main;
   - testes devem passar.
6. Explicar que push automático é opt-in.
7. Explicar que o runner executa uma missão por padrão.
8. Explicar que ele aborta em caso de erro.
9. Explicar que ele não substitui revisão humana em mudanças sensíveis.
10. Tudo deve estar em português do Brasil.

Requisitos de teste:
- pytest deve passar;
- python3 -m compileall src deve passar;
- bash -n scripts/vaf-run-next-safe.sh deve passar;
- se alterar tests/test_worker_scripts.py, manter cobertura simples e determinística.

Regra de commit automático:
Se esta missão gerar commit automático, a mensagem deve estar em português do Brasil.
Usar a mensagem fornecida por VAF_COMMIT_MESSAGE quando existir.

Restrições:
- não alterar src/;
- não adicionar dependências;
- não acessar rede;
- não chamar providers externos;
- não chamar LLMs externos;
- não alterar .opencode;
- não alterar node_modules;
- não reescrever histórico Git;
- não fazer force push;
- documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- docs/operations/safe-runner-usage.md existe;
- README.md aponta para o documento ou menciona o runner seguro;
- pytest passa;
- compileall passa;
- bash -n passa;
- auto-commit usa mensagem em português do Brasil.
