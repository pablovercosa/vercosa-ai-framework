Leia obrigatoriamente:
- AGENTS.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- scripts/vaf-run-one-mission.sh
- scripts/vaf-worker.sh
- scripts/vaf-start-background.sh
- scripts/vaf-status.sh
- README.md

Assuma o papel de shell-maintenance-agent e framework-architect.

Missão:
Ajustar o auto-commit do worker para português do Brasil.

Objetivo:
Corrigir o mecanismo de auto-commit para que commits automáticos não usem mais o prefixo inglês `mission:` e passem a respeitar o padrão pt-BR definido na documentação.

Contexto:
O comando abaixo mostrou que o auto-commit está hardcoded:

`scripts/vaf-run-one-mission.sh:52: git commit -m "mission: ${NAME}"`

O projeto agora definiu português do Brasil como idioma oficial para documentação e mensagens de commit futuras.

Entregáveis obrigatórios:
- atualizar scripts/vaf-run-one-mission.sh;
- atualizar scripts/vaf-start-background.sh se necessário para propagar VAF_COMMIT_MESSAGE;
- atualizar scripts/vaf-worker.sh se necessário para registrar VAF_COMMIT_MESSAGE no log;
- atualizar documentação relacionada, se necessário;
- criar ou atualizar teste/script simples de validação se já houver padrão para scripts;
- atualizar README.md ou docs apenas se a forma de uso do worker mudar.

Requisitos funcionais:
1. Substituir o prefixo automático `mission:` por `missão:`.
2. Permitir mensagem customizada via variável de ambiente `VAF_COMMIT_MESSAGE`.
3. Se `VAF_COMMIT_MESSAGE` estiver definida e não vazia, o auto-commit deve usar essa mensagem.
4. Se `VAF_COMMIT_MESSAGE` não estiver definida, o auto-commit deve usar:
   `missão: ${NAME}`
5. Preservar o comportamento existente de `VAF_AUTO_COMMIT=1`.
6. Não quebrar `VAF_AUTO_APPROVE`.
7. Não alterar o fluxo de fila/running/done/failed.
8. Não alterar a lógica de execução do OpenCode.
9. Não reescrever histórico Git.
10. Não fazer force push.
11. Não alterar configurações globais.
12. Não usar sudo.

Comportamento esperado:
- Com:
  `VAF_AUTO_COMMIT=1`
  a mensagem padrão deve ser:
  `missão: nome-da-missao`

- Com:
  `VAF_AUTO_COMMIT=1 VAF_COMMIT_MESSAGE="implementação: exemplo"`
  a mensagem deve ser:
  `implementação: exemplo`

Requisitos de documentação:
- documentação em português do Brasil;
- se documentar variável nova, explicar:
  - VAF_AUTO_COMMIT;
  - VAF_COMMIT_MESSAGE;
  - comportamento padrão;
  - exemplo de uso;
- não prometer comportamento não implementado.

Requisitos de teste/validação:
- `bash -n scripts/vaf-run-one-mission.sh` deve passar;
- `bash -n scripts/vaf-worker.sh` deve passar;
- `bash -n scripts/vaf-start-background.sh` deve passar;
- `pytest` deve passar;
- `python3 -m compileall src` deve passar;
- usar grep para confirmar que não há mais `git commit -m "mission:` nos scripts do projeto.

Restrições:
- não implementar nova funcionalidade de framework;
- não alterar src/ salvo necessidade extrema;
- não adicionar dependências;
- não acessar rede;
- não chamar providers externos;
- não chamar LLMs externos;
- não alterar .opencode;
- não alterar node_modules;
- não fazer commit automático nesta missão;
- documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- scripts passam em `bash -n`;
- pytest passa;
- compileall passa;
- auto-commit usa pt-BR por padrão;
- VAF_COMMIT_MESSAGE é suportada;
- git status mostra apenas arquivos relacionados à missão antes do commit manual.
