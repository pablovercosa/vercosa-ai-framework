Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
- CHANGELOG.md
- SECURITY.md
- CODE_OF_CONDUCT.md
- LICENSE
- pyproject.toml
- .github/workflows/ci.yml
- docs/release/public-alpha-readiness.md
- docs/release/versioning-policy.md
- docs/release/alpha-version-plan.md
- docs/release/release-policy.md
- docs/release/pre-release-checklist.md
- docs/release/release-notes-alpha.md
- docs/release/clean-install-validation.md
- docs/release/alpha-readiness-diagnostic.md
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
- docs/release/pre-tag-checklist-execution.md
- docs/release/final-alpha-review.md
- docs/release/tag-plan.md
- docs/release/release-notes-final.md

Assuma o papel de:
- release-manager;
- release-preparation-agent;
- risk-reviewer;
- diagnostic-engineer;
- documentation-agent;
- consistency-reviewer.

Missão:
Executar e registrar checklist pré-tag alfa local.

Objetivo:
Executar formalmente o checklist pré-tag alfa em modo local, registrar evidências, pendências, ressalvas e bloqueios em documento próprio, atualizar os documentos de release e deixar claro se o projeto está apto ou não a avançar para uma missão futura de criação de tag, sem criar tag, sem publicar release, sem publicar pacote e sem fazer push.

Contexto:
- O projeto caminha para a futura versão 0.1.0-alpha.1.
- A política de release já foi criada.
- O checklist pré-tag já foi criado.
- As release notes alfa preliminares já foram criadas.
- O diagnóstico local de prontidão alfa já foi criado.
- Esta missão deve executar o checklist pré-tag local como gate documental.
- Esta missão ainda não cria tag.
- Esta missão ainda não publica release.
- Esta missão ainda não publica pacote.
- Esta missão não substitui autorização explícita do usuário.
- Esta missão não deve declarar que a alfa foi publicada.
- Como o batch ainda não terá sido enviado ao GitHub durante a execução desta missão, a confirmação do CI remoto pode permanecer como pendência pós-push.
- A missão deve ser honesta e conservadora.
- Se houver bloqueios, registrar bloqueios.
- Se houver ressalvas, registrar ressalvas.
- Correções permitidas são apenas documentais, pequenas e inequívocas.

Entregáveis obrigatórios:
1. Criar documento:
   - docs/release/pre-tag-checklist-execution.md

2. Atualizar:
   - docs/release/public-alpha-readiness.md
   - docs/release/alpha-version-plan.md
   - docs/release/release-policy.md
   - docs/release/pre-release-checklist.md
   - docs/release/release-notes-alpha.md
   - docs/release/alpha-readiness-diagnostic.md
   - docs/roadmap/mission-backlog.md
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md
   - CHANGELOG.md

3. Atualizar, se necessário:
   - README.md
   - CONTRIBUTING.md
   - docs/alignment/open-questions.md
   - docs/getting-started/clean-install-checklist.md

4. Corrigir apenas links ou inconsistências documentais pequenas e inequívocas.

5. Não alterar código Python.

6. Não alterar scripts shell.

7. Não alterar workflow de CI.

8. Não criar tag.

9. Não criar release.

10. Não publicar pacote.

11. Não adicionar dependências.

Procedimento obrigatório:
1. Registrar dados do ambiente:
   - data e hora da execução;
   - branch atual;
   - commit testado;
   - sistema operacional;
   - arquitetura;
   - versão do Python;
   - versão do Git.

2. Registrar estado Git:
   - branch;
   - último commit;
   - git status --short;
   - relação local com origin/main, se disponível sem acessar rede.

3. Não executar git fetch.

4. Não executar git pull.

5. Não acessar rede.

6. Não confirmar CI remoto via GitHub nesta missão.

7. Registrar CI remoto como:
   - pendente de confirmação após push;
   - não aplicável nesta execução local;
   - ou já conhecido apenas se houver evidência local disponível sem rede.

8. Executar e registrar:
   - ./scripts/vaf-status.sh
   - git status --short
   - git log --oneline --decorate -10
   - python3 -m vercosa_ai_framework.cli.main validate
   - python3 -m vercosa_ai_framework.cli.main doctor
   - python3 -m vercosa_ai_framework.cli.main missions
   - python3 -m vercosa_ai_framework.cli.main batch-summary
   - python3 -m vercosa_ai_framework.cli.main docs-links
   - python3 -m vercosa_ai_framework.cli.main alpha-readiness
   - pytest
   - python3 -m compileall src

9. Se entrypoint vaf existir e estiver disponível, pode executar também:
   - vaf validate
   - vaf doctor
   - vaf docs-links
   - vaf alpha-readiness

10. Não exigir entrypoint vaf se ele não estiver disponível no ambiente atual.

11. Verificar existência dos documentos mínimos:
   - README.md;
   - CONTRIBUTING.md;
   - CHANGELOG.md;
   - SECURITY.md;
   - CODE_OF_CONDUCT.md;
   - LICENSE;
   - pyproject.toml;
   - .github/workflows/ci.yml;
   - docs/legal/usage-policy.md;
   - docs/release/versioning-policy.md;
   - docs/release/alpha-version-plan.md;
   - docs/release/release-policy.md;
   - docs/release/pre-release-checklist.md;
   - docs/release/release-notes-alpha.md;
   - docs/release/public-alpha-readiness.md;
   - docs/release/clean-install-validation.md;
   - docs/release/alpha-readiness-diagnostic.md.

12. Verificar estado das missões:
   - queue;
   - running;
   - done;
   - failed;
   - worker.

13. Considerar como bloqueio:
   - running > 0;
   - failed > 0;
   - pytest falhando;
   - compileall falhando;
   - docs-links falhando após correções documentais simples;
   - alpha-readiness retornando NÃO PRONTO;
   - arquivos obrigatórios ausentes;
   - SECURITY.md ausente;
   - CHANGELOG.md ausente;
   - política de release ausente;
   - release notes alfa ausentes;
   - pyproject.toml ausente;
   - git status sujo sem justificativa;
   - secrets detectados em documentação pública.

14. Considerar como ressalva possível:
   - queue > 0 durante preparação em batch;
   - CI remoto ainda não confirmado por falta de push;
   - release notes ainda preliminares;
   - tag ainda não autorizada;
   - release ainda não autorizada;
   - pacote PyPI ainda não decidido;
   - internacionalização dos READMEs ainda futura;
   - validação de instalação limpa aprovada com ressalvas.

15. Não tratar como bloqueio automático o fato de haver missões 0099 e 0100 na fila durante o próprio ciclo, desde que isso seja explicado como preparação em andamento.

16. Não ocultar ressalvas.

17. Não transformar ressalvas em aprovação plena.

18. Não transformar checklist local em autorização automática para tag.

19. Não executar:
   - git tag;
   - git push;
   - git push --tags;
   - gh release;
   - twine;
   - build de pacote;
   - publicação de pacote;
   - scripts de batch;
   - missões.

20. Não usar sudo.

21. Não acessar banco.

22. Não chamar providers.

23. Não registrar secrets.

Requisitos para docs/release/pre-tag-checklist-execution.md:
1. O documento deve estar em português do Brasil.

2. O título deve indicar execução local do checklist pré-tag alfa.

3. Deve declarar explicitamente:
   - não é autorização para tag;
   - não cria tag;
   - não publica release;
   - não publica pacote;
   - não substitui autorização humana;
   - não confirma CI remoto se ainda não houve push.

4. Deve registrar:
   - data;
   - branch;
   - commit;
   - sistema operacional;
   - arquitetura;
   - versão do Python;
   - versão do Git.

5. Deve registrar estado das missões:
   - queue;
   - running;
   - done;
   - failed;
   - worker.

6. Deve registrar estado Git:
   - branch;
   - último commit;
   - git status;
   - observação sobre origin/main, se disponível sem rede.

7. Deve registrar resultados:
   - validate;
   - doctor;
   - missions;
   - batch-summary;
   - docs-links;
   - alpha-readiness;
   - pytest;
   - compileall.

8. Deve registrar documentos verificados.

9. Deve registrar status de CI:
   - workflow local existe;
   - CI remoto pendente de confirmação após push, se aplicável.

10. Deve registrar status de release notes:
   - preliminares;
   - ainda pendentes de revisão final antes da publicação.

11. Deve registrar status de tag:
   - não criada.

12. Deve registrar status de release:
   - não publicada.

13. Deve registrar status de pacote:
   - não publicado.

14. Deve registrar bloqueios.

15. Deve registrar ressalvas.

16. Deve registrar recomendações.

17. Deve classificar o checklist local como:
   - APROVADO;
   - APROVADO COM RESSALVAS;
   - REPROVADO.

18. A classificação deve ser conservadora.

19. Não classificar como APROVADO pleno se CI remoto ainda estiver pendente.

20. Não classificar como APROVADO pleno se release notes ainda forem preliminares.

21. APROVADO COM RESSALVAS pode ser usado quando todos os gates locais passam, mas permanecem pendências normais pré-publicação:
   - confirmação do CI remoto após push;
   - autorização explícita para tag;
   - revisão final de release notes;
   - decisão sobre pacote;
   - internacionalização futura.

22. REPROVADO deve ser usado quando houver bloqueio real local.

23. O documento deve incluir próximos passos recomendados:
   - concluir missão 0100;
   - rodar batch;
   - validar testes finais;
   - fazer push;
   - confirmar CI remoto;
   - revisar evidências;
   - pedir autorização explícita para missão de tag, se aplicável.

24. Não incluir logs extensos.

25. Não incluir tokens.

26. Não incluir credenciais.

27. Usar links relativos para documentos de release.

Requisitos para docs/release/public-alpha-readiness.md:
1. Registrar execução local do checklist pré-tag.

2. Linkar para:
   - docs/release/pre-tag-checklist-execution.md

3. Registrar classificação real:
   - APROVADO;
   - APROVADO COM RESSALVAS;
   - REPROVADO.

4. Não declarar alfa publicada.

5. Não declarar tag criada.

6. Manter pendente:
   - push do bloco atual, se aplicável;
   - confirmação do CI remoto;
   - autorização explícita para tag;
   - criação de tag;
   - publicação de release;
   - publicação de pacote, se aplicável;
   - internacionalização dos READMEs.

Requisitos para docs/release/alpha-version-plan.md:
1. Registrar que checklist pré-tag local foi executado.

2. Apontar para o relatório.

3. Manter versão como planejada, não publicada.

4. Não declarar tag criada.

5. Não declarar release publicada.

Requisitos para docs/release/release-policy.md:
1. Apontar para o relatório de execução local do checklist.

2. Reforçar que a execução local não substitui autorização explícita.

3. Reforçar que CI remoto deve ser confirmado após push quando aplicável.

Requisitos para docs/release/pre-release-checklist.md:
1. Marcar que existe modelo de checklist e execução local registrada.

2. Apontar para docs/release/pre-tag-checklist-execution.md.

3. Manter checklist como processo reutilizável.

4. Não transformar o documento em relatório único.

Requisitos para docs/release/release-notes-alpha.md:
1. Atualizar status caso o checklist pré-tag local tenha sido executado.

2. Manter release notes como preliminares.

3. Não declarar data de release.

4. Não declarar release publicada.

Requisitos para docs/release/alpha-readiness-diagnostic.md:
1. Apontar para o relatório de checklist pré-tag local como etapa posterior.

2. Não alterar resultados históricos de forma enganosa.

Requisitos para docs/roadmap/mission-backlog.md:
1. Marcar execução local do checklist pré-tag como concluída ou em progresso conforme esta missão.

2. Manter futuras:
   - consolidação final do candidato alfa;
   - confirmação do CI remoto após push;
   - autorização explícita para tag;
   - criação da tag alfa;
   - publicação da release alfa;
   - internacionalização dos READMEs;
   - decisão sobre PyPI.

3. Não criar missões novas na fila.

Requisitos para docs/alignment/current-state.md:
1. Registrar que o checklist pré-tag local foi executado.

2. Registrar classificação real.

3. Deixar claro que release não foi publicada.

4. Deixar claro que tag não foi criada.

Requisitos para docs/alignment/roadmap.md:
1. Atualizar roadmap conforme resultado real do checklist.

2. Manter próximos passos conservadores.

3. Não declarar release feita.

Requisitos para docs/alignment/open-questions.md:
1. Atualizar somente se houver perguntas concretas.

2. Possíveis perguntas:
   - quando confirmar CI remoto após push;
   - se a próxima etapa será missão de tag;
   - se haverá pacote PyPI;
   - quando revisar release notes finais;
   - quando internacionalizar READMEs.

Requisitos para CHANGELOG.md:
1. Atualizar seção Não publicado.

2. Registrar execução local do checklist pré-tag alfa.

3. Registrar correções documentais, se houver.

4. Não criar versão publicada.

5. Não criar data de release.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não alterar workflow de CI.
- Não criar tag.
- Não criar release.
- Não publicar pacote.
- Não executar git tag.
- Não executar git push.
- Não executar git push --tags.
- Não executar gh release.
- Não executar twine.
- Não executar build de pacote.
- Não executar missões.
- Não executar batch.
- Não acessar rede.
- Não acessar banco.
- Não chamar OpenAI.
- Não chamar Gemini.
- Não chamar Ollama.
- Não chamar Claude.
- Não chamar OpenCode.
- Não acessar MCPs.
- Não executar providers.
- Não usar sudo.
- Não alterar configurações globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- docs/release/pre-tag-checklist-execution.md existe.
- O checklist pré-tag local foi realmente executado.
- O relatório registra ambiente, branch e commit.
- O relatório registra estado das missões.
- O relatório registra estado Git.
- O relatório registra resultados de validate, doctor, missions, batch-summary, docs-links e alpha-readiness.
- O relatório registra resultado de pytest.
- O relatório registra resultado de compileall.
- O relatório registra CI remoto como pendente quando aplicável.
- O relatório classifica o checklist local como APROVADO, APROVADO COM RESSALVAS ou REPROVADO.
- docs/release/public-alpha-readiness.md aponta para o relatório.
- docs/release/alpha-version-plan.md foi atualizado.
- docs/release/release-policy.md foi atualizado.
- docs/release/pre-release-checklist.md foi atualizado.
- CHANGELOG.md registra a mudança.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhum workflow de CI foi alterado.
- Nenhuma tag foi criada.
- Nenhuma release foi criada.
- Nenhum pacote foi publicado.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
