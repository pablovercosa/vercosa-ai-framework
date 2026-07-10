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
- docs/release/clean-install-validation.md
- docs/getting-started/local-installation.md
- docs/getting-started/clean-install-checklist.md
- docs/roadmap/mission-backlog.md
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/architecture/module-index.md
- docs/architecture/post-integration-architecture-review.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md
- .github/workflows/ci.yml

Leia também, se existirem:
- docs/release/release-policy.md
- docs/release/pre-release-checklist.md
- docs/release/release-notes.md
- docs/release/release-process.md
- .github/workflows/release.yml

Assuma o papel de:
- release-manager;
- release-preparation-agent;
- open-source-maintainer;
- documentation-agent;
- risk-reviewer;
- consistency-reviewer.

Missão:
Criar política de release e checklist pré-tag.

Objetivo:
Criar uma política inicial de release e um checklist pré-tag para o Vercosa AI Framework, definindo critérios mínimos, etapas manuais, validações obrigatórias, riscos e bloqueios antes de uma futura tag alfa, sem criar tag, sem publicar release, sem publicar pacote e sem automatizar deploy.

Contexto:
- O projeto caminha para uma futura versão alfa.
- A versão planejada foi documentada como alfa, mas ainda não foi publicada.
- O projeto já possui CHANGELOG.md.
- O projeto já possui documentação de prontidão para alfa pública.
- O projeto já possui empacotamento Python mínimo, se a missão 0092 tiver sido executada.
- O projeto já possui CI mínimo, se a missão 0093 tiver sido executada.
- Ainda falta uma política clara para decidir quando criar tag e release.
- Esta missão deve preparar o processo, não executar release.
- O release deve continuar manual e explícito nesta fase.
- O projeto não deve publicar pacote automaticamente.
- O projeto não deve criar tag automaticamente.
- O projeto não deve declarar alfa publicada nesta missão.

Entregáveis obrigatórios:
1. Criar documento:
   - docs/release/release-policy.md

2. Criar documento:
   - docs/release/pre-release-checklist.md

3. Atualizar:
   - README.md
   - CONTRIBUTING.md
   - CHANGELOG.md
   - docs/release/public-alpha-readiness.md
   - docs/release/versioning-policy.md
   - docs/release/alpha-version-plan.md
   - docs/roadmap/mission-backlog.md
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md

4. Atualizar, se necessário:
   - docs/alignment/open-questions.md
   - docs/getting-started/clean-install-checklist.md
   - docs/release/clean-install-validation.md

5. Não alterar código Python.

6. Não alterar scripts shell.

7. Não alterar workflow de CI, salvo correção documental inevitável de referência.

8. Não criar tag.

9. Não criar release.

10. Não publicar pacote.

11. Não adicionar dependências.

Requisitos para docs/release/release-policy.md:
1. O documento deve estar em português do Brasil.

2. Explicar que a política é inicial.

3. Explicar que o projeto ainda não possui release estável.

4. Explicar que a primeira release prevista é uma alfa.

5. Explicar que release alfa não significa estabilidade de produção.

6. Diferenciar claramente:
   - versão planejada;
   - tag Git;
   - release GitHub;
   - pacote publicado;
   - changelog;
   - release notes;
   - branch main;
   - produção.

7. Registrar que, nesta fase, release é um processo manual e explícito.

8. Registrar que nenhuma tag deve ser criada sem autorização explícita.

9. Registrar que nenhuma release deve ser publicada sem autorização explícita.

10. Registrar que nenhum pacote deve ser publicado sem missão específica.

11. Registrar que VAF_AUTO_PUSH não equivale a release.

12. Registrar que git push comum não equivale a release.

13. Registrar critérios mínimos para uma release alfa:
   - queue=0;
   - running=0;
   - failed=0;
   - git status limpo;
   - origin/main sincronizado;
   - pytest passando;
   - python3 -m compileall src passando;
   - CI mínimo passando;
   - validação de instalação limpa executada e aprovada ou aprovada com ressalvas aceitáveis;
   - CHANGELOG.md atualizado;
   - documentação pública mínima presente;
   - SECURITY.md presente;
   - CODE_OF_CONDUCT.md presente;
   - templates de issue e pull request presentes;
   - licença definida ou pendência documentada de forma aceitável;
   - versão planejada documentada;
   - riscos conhecidos documentados.

14. Registrar bloqueios para release:
   - testes falhando;
   - compileall falhando;
   - failed > 0;
   - missão presa em running;
   - git sujo;
   - CI falhando;
   - documentação prometendo recurso inexistente;
   - ausência de SECURITY.md;
   - ausência de CHANGELOG.md;
   - ausência de política de uso;
   - problema de licença não resolvido;
   - instalação limpa reprovada;
   - secrets expostos;
   - tag/release sem aprovação explícita.

15. Definir etapas manuais recomendadas:
   - revisar status das missões;
   - validar git;
   - rodar pytest;
   - rodar compileall;
   - rodar comandos principais da CLI;
   - revisar CHANGELOG.md;
   - revisar documentação de release;
   - revisar SECURITY.md e política de uso;
   - confirmar CI;
   - confirmar versão;
   - obter autorização explícita;
   - criar tag em missão própria;
   - publicar release em missão própria, se aprovado.

16. Explicar convenção de tag planejada:
   - v0.1.0-alpha.1

17. Deixar claro que a tag não deve ser criada nesta missão.

18. Explicar que release notes finais devem ser criadas ou revisadas em missão específica antes da publicação.

19. Explicar que publicação em PyPI é futura e depende de decisão própria.

20. Explicar que internacionalização dos READMEs continua futura.

21. Não prometer estabilidade.

22. Não prometer suporte formal.

23. Não prometer compatibilidade de API.

24. Não prometer SLA.

25. Usar links relativos para:
   - CHANGELOG.md
   - docs/release/alpha-version-plan.md
   - docs/release/public-alpha-readiness.md
   - docs/release/pre-release-checklist.md
   - docs/release/clean-install-validation.md
   - SECURITY.md
   - CONTRIBUTING.md

Requisitos para docs/release/pre-release-checklist.md:
1. O documento deve estar em português do Brasil.

2. Deve ser um checklist operacional pré-tag.

3. Deve deixar claro que executar o checklist não cria release.

4. Deve deixar claro que o checklist é pré-condição, não autorização automática.

5. Deve conter seção de estado Git:
   - branch main;
   - git status --short limpo;
   - HEAD sincronizado com origin/main;
   - último commit revisado;
   - sem alterações locais.

6. Deve conter seção de missões:
   - queue=0;
   - running=0;
   - failed=0;
   - done consistente;
   - worker stopped;
   - logs revisados quando aplicável.

7. Deve conter seção de testes:
   - pytest;
   - python3 -m compileall src;
   - comandos principais da CLI;
   - CI GitHub Actions.

8. Deve conter seção de documentação:
   - README.md;
   - CONTRIBUTING.md;
   - CHANGELOG.md;
   - SECURITY.md;
   - CODE_OF_CONDUCT.md;
   - LICENSE;
   - docs/legal/usage-policy.md;
   - docs/release/versioning-policy.md;
   - docs/release/alpha-version-plan.md;
   - docs/release/public-alpha-readiness.md;
   - docs/release/clean-install-validation.md.

9. Deve conter seção de segurança:
   - sem secrets;
   - sem tokens;
   - sem credenciais;
   - logs sanitizados;
   - SECURITY.md atualizado;
   - vulnerabilidades conhecidas avaliadas;
   - política de uso atualizada.

10. Deve conter seção de empacotamento:
   - pyproject.toml existe;
   - instalação local em modo desenvolvimento documentada;
   - versão coerente com plano alfa;
   - sem publicação de pacote.

11. Deve conter seção de validação de instalação limpa:
   - checklist criado;
   - execução registrada;
   - resultado classificado;
   - ressalvas avaliadas;
   - bloqueios resolvidos ou aceitos explicitamente.

12. Deve conter seção de autorização:
   - autorização explícita para tag;
   - autorização explícita para release;
   - autorização explícita para publicação de pacote, se um dia houver.

13. Deve conter seção de comandos sugeridos, sem executá-los automaticamente.

14. Os comandos sugeridos devem incluir:
   - ./scripts/vaf-status.sh
   - git status --short
   - git log --oneline --decorate -10
   - pytest
   - python3 -m compileall src
   - python3 -m vercosa_ai_framework.cli.main --help
   - python3 -m vercosa_ai_framework.cli.main validate
   - python3 -m vercosa_ai_framework.cli.main doctor
   - python3 -m vercosa_ai_framework.cli.main missions
   - python3 -m vercosa_ai_framework.cli.main batch-summary

15. Incluir observação para usar o entrypoint vaf somente se instalado e documentado após a missão de empacotamento.

16. Não criar comandos de tag reais como etapa automática.

17. Se mencionar comando de tag futuro, deixar claro que é apenas para missão específica autorizada.

18. Não incluir git push --tags como comando operacional desta missão.

19. Não incluir gh release create como comando operacional desta missão.

20. Não incluir twine upload.

21. Não incluir publicação PyPI.

Requisitos para README.md:
1. Adicionar link curto para:
   - docs/release/release-policy.md
   - docs/release/pre-release-checklist.md

2. Manter README enxuto.

3. Não declarar release publicada.

4. Não declarar produção pronta.

Requisitos para CONTRIBUTING.md:
1. Adicionar referência curta à política de release.

2. Explicar que contribuições que afetem comportamento público devem considerar CHANGELOG.md.

3. Explicar que criação de tag e release exige missão e autorização explícita.

4. Não transformar CONTRIBUTING.md em manual completo de release.

Requisitos para CHANGELOG.md:
1. Atualizar seção Não publicado.

2. Registrar criação da política de release e checklist pré-tag.

3. Não criar versão publicada.

4. Não criar data de release.

Requisitos para docs/release/public-alpha-readiness.md:
1. Marcar política de release como criada.

2. Marcar checklist pré-tag como criado.

3. Manter pendente:
   - execução do checklist pré-tag;
   - autorização explícita;
   - criação de tag;
   - publicação de release;
   - internacionalização dos READMEs.

4. Não declarar alfa pública como publicada.

Requisitos para docs/release/versioning-policy.md:
1. Apontar para a política de release.

2. Diferenciar versionamento de publicação de release.

3. Não alterar versão planejada sem justificativa.

Requisitos para docs/release/alpha-version-plan.md:
1. Apontar para política de release e checklist pré-tag.

2. Manter status como planejado, não publicado.

3. Não declarar tag criada.

Requisitos para docs/roadmap/mission-backlog.md:
1. Marcar política de release e checklist pré-tag como concluídos ou em progresso conforme esta missão.

2. Manter como futuras:
   - executar checklist pré-tag;
   - revisar release notes alfa;
   - criar tag alfa;
   - publicar release alfa;
   - internacionalizar READMEs.

3. Não criar missões novas na fila.

Requisitos para docs/alignment/current-state.md:
1. Registrar que existe política inicial de release.

2. Registrar que existe checklist pré-tag.

3. Deixar claro que nenhuma release foi publicada.

Requisitos para docs/alignment/roadmap.md:
1. Atualizar roadmap para refletir preparação de release.

2. Não declarar release alfa feita.

3. Manter próximos passos conservadores.

Requisitos para docs/alignment/open-questions.md:
1. Atualizar somente se houver perguntas concretas.

2. Perguntas possíveis:
   - quando executar checklist pré-tag;
   - se a alfa terá pacote PyPI ou apenas código-fonte;
   - quando internacionalizar READMEs;
   - quando criar release notes finais.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não criar tag.
- Não criar release.
- Não publicar pacote.
- Não criar workflow de release.
- Não criar deploy.
- Não criar PyPI config.
- Não executar gh release.
- Não executar git tag.
- Não executar git push --tags.
- Não executar twine.
- Não criar README.en.md.
- Não criar README.es.md.
- Não internacionalizar READMEs.
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
- Não executar missões.
- Não fazer git push.
- Não usar sudo.
- Não alterar configurações globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- docs/release/release-policy.md existe.
- docs/release/pre-release-checklist.md existe.
- A política diferencia versão planejada, tag, release e pacote.
- O checklist pré-tag define validações mínimas.
- A documentação deixa claro que nenhuma tag foi criada.
- A documentação deixa claro que nenhuma release foi publicada.
- README.md aponta para os documentos de release.
- CONTRIBUTING.md menciona a política de release.
- CHANGELOG.md registra a mudança sem criar versão publicada.
- docs/release/public-alpha-readiness.md registra política e checklist como criados.
- docs/release/alpha-version-plan.md aponta para política e checklist.
- docs/roadmap/mission-backlog.md foi atualizado se necessário.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- Nenhuma tag foi criada.
- Nenhuma release foi criada.
- Nenhum pacote foi publicado.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
