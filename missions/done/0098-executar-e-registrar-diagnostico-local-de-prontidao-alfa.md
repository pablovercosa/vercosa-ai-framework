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
- docs/release/alpha-readiness-diagnostic.md
- docs/release/pre-tag-diagnostic.md
- tests/test_cli_alpha_readiness.py
- tests/test_cli_docs_links.py
- tests/test_cli_batch_summary.py
- tests/test_cli_missions.py

Assuma o papel de:
- release-preparation-agent;
- diagnostic-engineer;
- documentation-quality-engineer;
- test-engineer;
- risk-reviewer;
- consistency-reviewer.

Missão:
Executar e registrar diagnóstico local de prontidão alfa.

Objetivo:
Executar um diagnóstico local completo e factual da prontidão alfa do Vercosa AI Framework, usando os comandos locais já implementados, registrar os resultados em documento próprio de release e atualizar a documentação de prontidão, sem criar tag, sem publicar release, sem publicar pacote e sem ocultar ressalvas ou bloqueios.

Contexto:
- O projeto caminha para a futura versão 0.1.0-alpha.1.
- A missão 0091 executou validação de instalação limpa.
- A missão 0092 criou empacotamento Python mínimo.
- A missão 0093 criou CI mínimo.
- A missão 0094 criou política de release e checklist pré-tag.
- A missão 0095 criou release notes alfa preliminares.
- A missão 0096 criou validador local de links Markdown.
- A missão 0097 criou comando CLI de prontidão alfa.
- Esta missão deve executar os diagnósticos locais disponíveis e registrar os resultados.
- Esta missão não é release.
- Esta missão não cria tag.
- Esta missão não publica pacote.
- Esta missão não substitui autorização humana.
- Esta missão deve ser honesta: se houver ressalvas, registrar ressalvas; se houver bloqueios, registrar bloqueios.
- A missão pode corrigir apenas problemas documentais pequenos e inequívocos encontrados durante o diagnóstico, como links relativos quebrados.
- A missão não deve alterar código Python.
- A missão não deve alterar scripts shell.
- A missão não deve alterar workflow de CI, salvo ajuste documental inevitável e justificado.

Entregáveis obrigatórios:
1. Criar documento:
   - docs/release/alpha-readiness-diagnostic.md

2. Atualizar:
   - docs/release/public-alpha-readiness.md
   - docs/release/pre-release-checklist.md
   - docs/release/alpha-version-plan.md
   - docs/release/release-notes-alpha.md
   - docs/roadmap/mission-backlog.md
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md
   - CHANGELOG.md

3. Atualizar, se necessário:
   - README.md
   - CONTRIBUTING.md
   - docs/alignment/open-questions.md
   - docs/getting-started/clean-install-checklist.md

4. Corrigir links Markdown quebrados somente se forem simples, documentais e inequívocos.

5. Não alterar código Python.

6. Não alterar scripts shell.

7. Não criar tag.

8. Não criar release.

9. Não publicar pacote.

10. Não adicionar dependências.

Procedimento obrigatório:
1. Registrar dados do ambiente:
   - data e hora da execução;
   - branch atual;
   - commit testado;
   - sistema operacional;
   - arquitetura;
   - versão do Python;
   - versão do Git.

2. Não registrar:
   - tokens;
   - secrets;
   - credenciais;
   - variáveis de ambiente completas;
   - conteúdo de chaves SSH;
   - endereços sensíveis desnecessários.

3. Executar e registrar, no mínimo:
   - ./scripts/vaf-status.sh
   - git status --short
   - git log --oneline --decorate -10
   - python3 -m vercosa_ai_framework.cli.main --help
   - python3 -m vercosa_ai_framework.cli.main validate
   - python3 -m vercosa_ai_framework.cli.main doctor
   - python3 -m vercosa_ai_framework.cli.main missions
   - python3 -m vercosa_ai_framework.cli.main batch-summary
   - python3 -m vercosa_ai_framework.cli.main docs-links
   - python3 -m vercosa_ai_framework.cli.main alpha-readiness
   - pytest
   - python3 -m compileall src

4. Se o entrypoint vaf existir e estiver disponível no ambiente, pode executar também:
   - vaf --help
   - vaf validate
   - vaf doctor
   - vaf docs-links
   - vaf alpha-readiness

5. Não exigir entrypoint vaf se ele não estiver instalado no ambiente atual.

6. Não executar:
   - scripts/vaf-run-batch-safe.sh;
   - scripts/vaf-run-next-safe.sh;
   - scripts/vaf-run-one-mission.sh;
   - qualquer missão;
   - git tag;
   - git push;
   - git push --tags;
   - gh release;
   - twine;
   - build de pacote;
   - publicação de pacote.

7. Não acessar rede.

8. Não acessar banco.

9. Não chamar providers.

10. Não chamar OpenCode.

11. Não executar MCPs.

12. Não usar sudo.

13. Registrar resultado factual de cada comando:
   - passou;
   - falhou;
   - não disponível;
   - não aplicável.

14. Para comandos que falharem, registrar resumo curto e sanitizado.

15. Não colar logs extensos.

16. Não esconder falhas.

17. Se docs-links encontrar links quebrados simples e inequívocos:
   - corrigir os links;
   - registrar que houve correção documental;
   - executar docs-links novamente;
   - registrar novo resultado.

18. Se alpha-readiness classificar como PRONTO COM RESSALVAS:
   - registrar as ressalvas;
   - não declarar release pronta sem ressalvas.

19. Se alpha-readiness classificar como NÃO PRONTO:
   - registrar bloqueios;
   - não prosseguir para qualquer simulação de release.

20. Se pytest falhar:
   - registrar falha;
   - não ocultar;
   - não alterar código para corrigir nesta missão.

21. Se compileall falhar:
   - registrar falha;
   - não ocultar;
   - não alterar código para corrigir nesta missão.

22. Se git status ficar sujo após comandos de diagnóstico por geração inesperada de arquivos:
   - registrar;
   - limpar somente arquivos claramente temporários e não rastreados;
   - não apagar arquivos rastreados;
   - não usar git reset --hard;
   - não usar git clean -fdx.

Requisitos para docs/release/alpha-readiness-diagnostic.md:
1. O documento deve estar em português do Brasil.

2. O título deve indicar diagnóstico local de prontidão alfa.

3. Deve declarar explicitamente:
   - não é release;
   - não cria tag;
   - não publica pacote;
   - não substitui revisão humana;
   - é um diagnóstico local.

4. Deve registrar:
   - data;
   - branch;
   - commit;
   - sistema operacional;
   - arquitetura;
   - versão do Python;
   - versão do Git.

5. Deve registrar o estado das missões:
   - queue;
   - running;
   - done;
   - failed;
   - worker.

6. Deve registrar o estado Git:
   - branch;
   - último commit;
   - git status limpo ou não.

7. Deve registrar resultados dos comandos de CLI:
   - help;
   - validate;
   - doctor;
   - missions;
   - batch-summary;
   - docs-links;
   - alpha-readiness.

8. Deve registrar resultado dos testes:
   - pytest;
   - quantidade de testes aprovados, se disponível;
   - falhas, se houver.

9. Deve registrar resultado do compileall.

10. Deve registrar resultado da validação de links Markdown.

11. Deve registrar resultado do comando alpha-readiness.

12. Deve classificar o diagnóstico como:
   - PRONTO;
   - PRONTO COM RESSALVAS;
   - NÃO PRONTO.

13. A classificação deve ser conservadora.

14. Não classificar como PRONTO se:
   - pytest falhar;
   - compileall falhar;
   - docs-links falhar após correções possíveis;
   - alpha-readiness retornar NÃO PRONTO;
   - running > 0;
   - failed > 0;
   - git status estiver sujo sem justificativa;
   - documentos obrigatórios estiverem ausentes;
   - política de release estiver ausente;
   - SECURITY.md estiver ausente;
   - CHANGELOG.md estiver ausente.

15. PRONTO COM RESSALVAS pode ser usado quando:
   - alpha-readiness retornar ressalvas não bloqueantes;
   - release notes ainda forem preliminares;
   - release ainda depender de revisão humana;
   - checklist pré-tag ainda não foi executado formalmente como autorização;
   - CI precisa ser confirmado no GitHub após push.

16. Deve incluir seção de bloqueios.

17. Deve incluir seção de ressalvas.

18. Deve incluir seção de recomendações para próximas missões.

19. Recomendações possíveis:
   - executar checklist pré-tag formal;
   - revisar release notes finais;
   - confirmar CI remoto após push;
   - criar missão específica para tag alfa;
   - criar missão específica para publicação de release;
   - decidir sobre PyPI;
   - internacionalizar READMEs.

20. Não deve incluir logs longos.

21. Não deve incluir secrets.

22. Não deve incluir caminhos sensíveis desnecessários.

23. Deve usar links relativos para documentos de release.

Requisitos para docs/release/public-alpha-readiness.md:
1. Registrar que o diagnóstico local de prontidão alfa foi executado.

2. Registrar classificação real:
   - PRONTO;
   - PRONTO COM RESSALVAS;
   - NÃO PRONTO.

3. Linkar para docs/release/alpha-readiness-diagnostic.md.

4. Não declarar release publicada.

5. Não declarar tag criada.

6. Manter pendente:
   - autorização explícita;
   - execução final do checklist pré-tag, se ainda não feita como gate formal;
   - criação de tag;
   - publicação de release;
   - publicação de pacote, se aplicável;
   - internacionalização dos READMEs.

Requisitos para docs/release/pre-release-checklist.md:
1. Incluir o diagnóstico local de prontidão alfa como evidência recomendada antes da tag.

2. Apontar para docs/release/alpha-readiness-diagnostic.md.

3. Manter checklist como gate manual, não automático.

4. Não incluir comandos de publicação.

Requisitos para docs/release/alpha-version-plan.md:
1. Registrar que o diagnóstico local foi executado.

2. Linkar para o relatório.

3. Manter versão como planejada, não publicada.

4. Não declarar tag criada.

Requisitos para docs/release/release-notes-alpha.md:
1. Atualizar somente se o diagnóstico alterar o estado real.

2. Manter release notes como preliminares.

3. Não declarar release publicada.

4. Não declarar data de release.

Requisitos para docs/roadmap/mission-backlog.md:
1. Marcar diagnóstico local de prontidão alfa como concluído ou em progresso conforme esta missão.

2. Manter como futuras:
   - executar checklist pré-tag formal;
   - revisar release notes finais;
   - confirmar CI remoto após push;
   - criar tag alfa;
   - publicar release alfa;
   - internacionalizar READMEs;
   - decidir sobre PyPI.

3. Não criar missões novas na fila.

Requisitos para docs/alignment/current-state.md:
1. Registrar que existe relatório de diagnóstico local de prontidão alfa.

2. Registrar classificação real.

3. Não declarar release publicada.

Requisitos para docs/alignment/roadmap.md:
1. Atualizar roadmap conforme resultado real.

2. Não declarar release feita.

3. Manter próximos passos conservadores.

Requisitos para docs/alignment/open-questions.md:
1. Atualizar somente se o diagnóstico gerar perguntas concretas.

2. Possíveis perguntas:
   - CI remoto já foi confirmado após push?
   - tag alfa será criada imediatamente após checklist pré-tag?
   - release terá pacote PyPI ou apenas código-fonte?
   - quando internacionalizar READMEs?

Requisitos para CHANGELOG.md:
1. Atualizar seção Não publicado.

2. Registrar criação do diagnóstico local de prontidão alfa.

3. Se links Markdown forem corrigidos, registrar correções documentais.

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
- docs/release/alpha-readiness-diagnostic.md existe.
- O diagnóstico foi realmente executado.
- O relatório registra ambiente, commit e branch.
- O relatório registra estado das missões.
- O relatório registra estado Git.
- O relatório registra resultados de validate, doctor, missions, batch-summary, docs-links e alpha-readiness.
- O relatório registra resultado de pytest.
- O relatório registra resultado de compileall.
- O relatório classifica prontidão de forma conservadora.
- docs/release/public-alpha-readiness.md aponta para o diagnóstico.
- docs/release/pre-release-checklist.md inclui o diagnóstico como evidência.
- docs/release/alpha-version-plan.md foi atualizado.
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
