Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
- CHANGELOG.md
- SECURITY.md
- CODE_OF_CONDUCT.md
- LICENSE
- pyproject.toml
- docs/release/public-alpha-readiness.md
- docs/release/versioning-policy.md
- docs/release/alpha-version-plan.md
- docs/release/release-policy.md
- docs/release/pre-release-checklist.md
- docs/release/release-notes-alpha.md
- docs/release/clean-install-validation.md
- docs/getting-started/local-installation.md
- docs/getting-started/clean-install-checklist.md
- docs/architecture/module-index.md
- docs/architecture/post-integration-architecture-review.md
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/roadmap/mission-backlog.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md
- src/vercosa_ai_framework/cli/README.md
- src/vercosa_ai_framework/cli/main.py
- tests/

Leia também, se existirem:
- .github/workflows/ci.yml
- tests/test_cli_alpha_readiness.py
- tests/test_cli_docs_links.py
- tests/test_cli_batch_summary.py
- tests/test_cli_missions.py

Assuma o papel de:
- cli-engineer;
- release-preparation-agent;
- test-engineer;
- documentation-quality-engineer;
- open-source-maintainer.

Missão:
Criar comando CLI de prontidão alfa.

Objetivo:
Adicionar à CLI operacional um comando local, seguro e somente leitura para verificar a prontidão documental e operacional mínima da futura alfa do Vercosa AI Framework, sem criar tag, sem publicar release, sem publicar pacote e sem substituir a revisão humana.

Contexto:
- O projeto caminha para a futura versão 0.1.0-alpha.1.
- O projeto já possui documentação de prontidão pública alfa.
- O projeto já possui política de release e checklist pré-tag.
- O projeto já possui release notes alfa preliminares.
- O projeto já possui CI mínimo, se a missão 0093 tiver sido executada.
- O projeto já possui validador local de links Markdown, se a missão 0096 tiver sido executada.
- O novo comando deve consolidar verificações locais básicas de prontidão.
- O comando não deve executar release.
- O comando não deve criar tag.
- O comando não deve publicar pacote.
- O comando não deve executar missões.
- O comando não deve executar batch.
- O comando não deve chamar providers.
- O comando não deve acessar rede.
- O comando deve ser diagnóstico auxiliar, não autorização automática.

Entregáveis obrigatórios:
1. Atualizar:
   - src/vercosa_ai_framework/cli/main.py

2. Criar ou atualizar testes:
   - tests/test_cli_alpha_readiness.py
   - ou arquivo de teste de CLI já existente, se for mais coerente.

3. Atualizar:
   - src/vercosa_ai_framework/cli/README.md
   - README.md
   - CONTRIBUTING.md
   - docs/release/public-alpha-readiness.md
   - docs/release/pre-release-checklist.md
   - docs/release/release-policy.md
   - docs/release/alpha-version-plan.md
   - docs/getting-started/clean-install-checklist.md
   - docs/roadmap/mission-backlog.md
   - CHANGELOG.md

4. Atualizar, se necessário:
   - .github/workflows/ci.yml
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md
   - docs/alignment/open-questions.md

5. Não alterar scripts shell.

6. Não adicionar dependências.

7. Não criar tag.

8. Não criar release.

9. Não publicar pacote.

Requisitos funcionais:
1. Adicionar comando de CLI para verificar prontidão alfa.

2. Nome recomendado do comando:
   - alpha-readiness

3. Exemplo conceitual:
   - python3 -m vercosa_ai_framework.cli.main alpha-readiness

4. Se entrypoint local vaf existir após empacotamento, documentar alternativa:
   - vaf alpha-readiness

5. Não inventar entrypoint global se ele não existir.

6. O comando deve ser local, seguro e somente leitura.

7. O comando deve verificar a existência dos arquivos mínimos:
   - README.md;
   - CONTRIBUTING.md;
   - CHANGELOG.md;
   - SECURITY.md;
   - CODE_OF_CONDUCT.md;
   - LICENSE;
   - pyproject.toml;
   - docs/release/public-alpha-readiness.md;
   - docs/release/versioning-policy.md;
   - docs/release/alpha-version-plan.md;
   - docs/release/release-policy.md;
   - docs/release/pre-release-checklist.md;
   - docs/release/release-notes-alpha.md;
   - docs/getting-started/local-installation.md;
   - docs/getting-started/clean-install-checklist.md;
   - docs/legal/usage-policy.md;
   - docs/architecture/module-index.md.

8. O comando deve verificar existência dos diretórios principais:
   - src/;
   - tests/;
   - docs/;
   - missions/queue;
   - missions/running;
   - missions/done;
   - missions/failed.

9. O comando deve verificar contagens de missões:
   - queue;
   - running;
   - failed.

10. O comando deve indicar bloqueio quando:
   - running > 0;
   - failed > 0.

11. O comando deve indicar atenção quando:
   - queue > 0.

12. O comando deve verificar se existe workflow de CI:
   - .github/workflows/ci.yml

13. Se o CI não existir, o comando deve indicar pendência, não traceback.

14. O comando deve verificar se release notes alfa preliminares existem.

15. O comando deve verificar se política de release existe.

16. O comando deve verificar se checklist pré-tag existe.

17. O comando deve verificar se CHANGELOG.md existe.

18. O comando deve verificar se SECURITY.md existe.

19. O comando deve verificar se CODE_OF_CONDUCT.md existe.

20. O comando deve verificar se pyproject.toml existe, quando a missão 0092 tiver sido executada.

21. O comando deve emitir uma classificação simples:
   - PRONTO;
   - PRONTO COM RESSALVAS;
   - NÃO PRONTO.

22. A classificação deve ser conservadora.

23. O comando não deve declarar release pronta se houver:
   - failed > 0;
   - running > 0;
   - arquivos obrigatórios ausentes;
   - ausência de pyproject.toml após empacotamento esperado;
   - ausência de CHANGELOG.md;
   - ausência de SECURITY.md;
   - ausência de política de release.

24. O comando pode retornar PRONTO COM RESSALVAS quando:
   - queue > 0;
   - CI ausente mas documentado como futuro;
   - validação de instalação limpa aprovada com ressalvas;
   - release notes existem, mas ainda são preliminares.

25. O comando deve retornar código de saída:
   - 0 para PRONTO;
   - 0 ou 1 para PRONTO COM RESSALVAS, conforme padrão escolhido e documentado;
   - diferente de 0 para NÃO PRONTO.

26. A escolha do código de saída para PRONTO COM RESSALVAS deve ser documentada e testada.

27. O comando deve listar pendências encontradas de forma clara.

28. O comando deve listar ressalvas encontradas de forma clara.

29. O comando deve listar itens aprovados de forma resumida.

30. O comando deve lembrar que:
   - ele não cria tag;
   - ele não publica release;
   - ele não substitui checklist pré-tag;
   - ele não substitui revisão humana;
   - pytest e compileall ainda devem ser executados.

31. O comando não deve executar:
   - pytest;
   - compileall;
   - git tag;
   - git push;
   - git push --tags;
   - gh release;
   - twine;
   - scripts de batch;
   - missões.

32. O comando não deve acessar rede.

33. O comando não deve acessar banco.

34. O comando não deve chamar providers.

35. O comando não deve ler secrets.

36. O comando não deve modificar arquivos.

Requisitos de implementação:
1. Usar somente biblioteca padrão.

2. Não adicionar dependências.

3. Manter implementação pequena e testável.

4. Separar a lógica de verificação em função testável, se fizer sentido.

5. Reutilizar padrões existentes da CLI.

6. Preservar comandos existentes:
   - status;
   - validate;
   - doctor;
   - missions;
   - batch-summary;
   - docs-links, se existir.

7. Não quebrar testes existentes.

8. Não acoplar o comando a scripts shell.

9. Não implementar release.

10. Não implementar tag.

11. Não implementar publicação de pacote.

12. Não implementar consulta ao GitHub.

13. Não implementar consulta ao remoto Git.

14. Não implementar leitura profunda de todos os documentos.

15. Não implementar parser completo de Markdown.

16. Pode verificar presença de palavras-chave mínimas em documentos críticos somente se isso for simples e testado.

17. Evitar complexidade excessiva.

18. Manter mensagens em português do Brasil.

Requisitos de testes:
1. Criar testes unitários para cenário pronto.

2. Criar testes unitários para arquivo obrigatório ausente.

3. Criar testes unitários para failed > 0.

4. Criar testes unitários para running > 0.

5. Criar testes unitários para queue > 0, se classificado como ressalva.

6. Criar testes para ausência de CI, se isso for ressalva ou pendência.

7. Criar testes para código de saída.

8. Criar testes para comando CLI, conforme padrão atual.

9. Usar diretório temporário.

10. Não depender da documentação real do projeto nos testes unitários.

11. Não acessar rede.

12. Não chamar providers.

13. Não executar missões.

14. Garantir que pytest passe.

15. Garantir que compileall passe.

Requisitos de CI:
1. Atualizar .github/workflows/ci.yml somente se existir.

2. Se atualizado, adicionar etapa:
   - python -m vercosa_ai_framework.cli.main alpha-readiness

3. Avaliar se a etapa deve falhar em PRs quando houver queue > 0.

4. Para evitar CI instável, o comando em CI deve ser usado de modo conservador.

5. Se o estado normal do repositório durante desenvolvimento inclui queue não vazia, não transformar queue > 0 em falha obrigatória.

6. Não usar secrets.

7. Não publicar pacote.

8. Não executar release.

Requisitos de documentação:
1. Atualizar src/vercosa_ai_framework/cli/README.md com:
   - propósito do alpha-readiness;
   - forma real de execução;
   - classificação;
   - limites;
   - exemplos;
   - diferença entre alpha-readiness, pre-release-checklist, docs-links, validate e doctor.

2. Atualizar README.md de forma breve.

3. Atualizar CONTRIBUTING.md para orientar uso antes de mudanças de release.

4. Atualizar docs/release/pre-release-checklist.md para incluir alpha-readiness como diagnóstico auxiliar.

5. Atualizar docs/release/release-policy.md para explicar que alpha-readiness não autoriza release sozinho.

6. Atualizar docs/release/public-alpha-readiness.md para registrar o comando.

7. Atualizar docs/release/alpha-version-plan.md para mencionar o comando como verificação auxiliar antes da tag.

8. Atualizar docs/getting-started/clean-install-checklist.md para incluir o comando.

9. Atualizar docs/roadmap/mission-backlog.md para marcar comando de prontidão alfa como concluído ou em progresso.

10. Atualizar CHANGELOG.md na seção Não publicado.

11. Documentação deve estar em português do Brasil.

12. Não prometer release.

13. Não prometer tag.

14. Não prometer publicação.

15. Não prometer validação perfeita.

16. Usar links relativos corretos.

Restrições:
- Não alterar scripts shell.
- Não adicionar dependências.
- Não criar tag.
- Não criar release.
- Não publicar pacote.
- Não executar git tag.
- Não executar git push --tags.
- Não executar gh release.
- Não executar twine.
- Não executar missões.
- Não executar batch.
- Não executar providers.
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
- Não alterar configurações globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação, testes e mensagens devem estar em português do Brasil quando aplicável.

Critérios de aceite:
- A CLI possui comando alpha-readiness ou equivalente documentado.
- O comando verifica arquivos mínimos de release alfa.
- O comando verifica estados de missões.
- O comando classifica prontidão de forma conservadora.
- O comando não altera arquivos.
- O comando não cria tag.
- O comando não publica release.
- O comando não publica pacote.
- O comando não acessa rede.
- Testes cobrem pronto, ressalvas e não pronto.
- src/vercosa_ai_framework/cli/README.md documenta o comando.
- README.md foi atualizado se necessário.
- CONTRIBUTING.md foi atualizado se necessário.
- docs/release/pre-release-checklist.md inclui o comando.
- docs/release/release-policy.md deixa claro que o comando não autoriza release sozinho.
- CHANGELOG.md registra a mudança.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
