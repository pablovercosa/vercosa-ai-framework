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
- docs/release/clean-install-validation.md
- docs/getting-started/local-installation.md
- docs/getting-started/clean-install-checklist.md
- docs/architecture/module-index.md
- docs/architecture/post-integration-architecture-review.md
- docs/architecture/audit-event-architecture.md
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/roadmap/mission-backlog.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md

Leia também, se existirem:
- docs/release/release-notes.md
- docs/release/release-notes-alpha.md
- docs/release/v0.1.0-alpha.1.md
- .github/workflows/ci.yml

Assuma o papel de:
- release-preparation-agent;
- release-notes-writer;
- open-source-maintainer;
- documentation-agent;
- consistency-reviewer.

Missão:
Criar release notes alfa preliminares.

Objetivo:
Criar notas preliminares para a futura release alfa do Vercosa AI Framework, consolidando o que já foi implementado, o que ainda é limitação conhecida, como validar a instalação e quais cuidados o usuário deve ter, sem publicar release, sem criar tag, sem declarar a alfa como publicada e sem prometer estabilidade.

Contexto:
- O projeto possui versão alfa planejada.
- A política de versionamento foi documentada.
- A política de release e o checklist pré-tag foram criados.
- O projeto possui CHANGELOG.md, mas release notes são um artefato mais direcionado à futura publicação.
- A release alfa ainda não foi criada.
- A tag ainda não foi criada.
- O pacote ainda não foi publicado.
- Esta missão deve preparar notas preliminares, não executar release.
- As notas devem ser públicas, claras e conservadoras.
- A documentação deve diferenciar estado implementado de planos futuros.
- A documentação não deve declarar que a alfa já está disponível.

Entregáveis obrigatórios:
1. Criar documento:
   - docs/release/release-notes-alpha.md

2. Atualizar:
   - README.md
   - CHANGELOG.md
   - docs/release/public-alpha-readiness.md
   - docs/release/alpha-version-plan.md
   - docs/release/release-policy.md
   - docs/release/pre-release-checklist.md
   - docs/roadmap/mission-backlog.md
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md

3. Atualizar, se necessário:
   - docs/alignment/open-questions.md
   - CONTRIBUTING.md

4. Não alterar código Python.

5. Não alterar scripts shell.

6. Não alterar workflow de CI.

7. Não criar tag.

8. Não criar release.

9. Não publicar pacote.

10. Não adicionar dependências.

Requisitos para docs/release/release-notes-alpha.md:
1. O documento deve estar em português do Brasil.

2. O título deve deixar claro que são notas preliminares da futura alfa.

3. A versão planejada deve ser indicada de forma conservadora:
   - 0.1.0-alpha.1

4. A tag futura planejada deve ser indicada de forma conservadora:
   - v0.1.0-alpha.1

5. O documento deve declarar explicitamente:
   - a release ainda não foi publicada;
   - a tag ainda não foi criada;
   - o pacote ainda não foi publicado;
   - a versão é planejada;
   - o documento é preparatório.

6. O documento deve conter uma seção de resumo.

7. O resumo deve explicar que o VAF é um framework de Harness Engineering para agentes de IA.

8. O documento deve conter seção "O que está incluído nesta alfa planejada".

9. Essa seção deve mencionar, de forma factual:
   - fundação modular do framework;
   - evolução por missões;
   - Mission Runner;
   - runner seguro de uma missão;
   - runner seguro em batch;
   - batch como fluxo operacional padrão quando seguro;
   - Policy Engine;
   - Guardian Engine;
   - Context Router;
   - Token Budget Manager;
   - Knowledge Hub;
   - Model Selection Engine;
   - Provider Gateway;
   - Runtime Adapter;
   - Usage/API Limit Guard;
   - Audit/Event Log;
   - persistência local JSONL de eventos auditáveis, se a missão 0090 já tiver sido executada;
   - CLI operacional;
   - comandos status, validate, doctor, missions e batch-summary, se existirem;
   - documentação pública inicial;
   - guia de instalação local;
   - guia de contribuição;
   - SECURITY.md;
   - CODE_OF_CONDUCT.md;
   - templates de issue e pull request;
   - CHANGELOG.md;
   - CI mínimo, se a missão 0093 tiver sido executada;
   - empacotamento Python mínimo, se a missão 0092 tiver sido executada.

10. O documento deve conter seção "Limitações conhecidas".

11. Limitações conhecidas devem incluir, quando aplicável:
   - projeto em desenvolvimento;
   - não pronto para produção;
   - APIs internas ainda podem mudar;
   - sem garantia de compatibilidade;
   - sem RAG semântico;
   - sem embeddings;
   - sem pgvector;
   - sem Semantic Index;
   - sem múltiplos providers reais em produção;
   - sem múltiplos runtimes reais em produção;
   - sem dashboard;
   - sem persistência externa de eventos;
   - sem política madura de vulnerabilidades;
   - internacionalização dos READMEs ainda futura;
   - release ainda não publicada.

12. O documento deve conter seção "Como testar localmente".

13. Essa seção deve apontar para:
   - docs/getting-started/local-installation.md
   - docs/getting-started/clean-install-checklist.md
   - docs/release/clean-install-validation.md

14. Incluir comandos de validação local em bloco Markdown, como:
   - pytest
   - python3 -m compileall src
   - python3 -m vercosa_ai_framework.cli.main --help
   - python3 -m vercosa_ai_framework.cli.main validate
   - python3 -m vercosa_ai_framework.cli.main doctor
   - python3 -m vercosa_ai_framework.cli.main missions
   - python3 -m vercosa_ai_framework.cli.main batch-summary

15. Se entrypoint vaf existir após a missão 0092, pode mencioná-lo como alternativa instalada localmente.

16. Não inventar entrypoint se ele não existir.

17. O documento deve conter seção "Segurança e uso responsável".

18. Essa seção deve apontar para:
   - SECURITY.md
   - docs/legal/usage-policy.md
   - docs/security/vulnerability-reporting.md

19. O documento deve conter seção "Antes da publicação".

20. Essa seção deve listar pendências antes da release real:
   - executar checklist pré-tag;
   - confirmar CI passando;
   - revisar CHANGELOG.md;
   - revisar release notes;
   - confirmar instalação limpa;
   - confirmar licença;
   - obter autorização explícita para tag;
   - obter autorização explícita para release;
   - decidir se haverá pacote ou somente código-fonte.

21. O documento deve conter seção "Links úteis".

22. Links úteis devem incluir:
   - README.md;
   - CHANGELOG.md;
   - docs/release/versioning-policy.md;
   - docs/release/alpha-version-plan.md;
   - docs/release/release-policy.md;
   - docs/release/pre-release-checklist.md;
   - docs/release/public-alpha-readiness.md;
   - CONTRIBUTING.md;
   - SECURITY.md.

23. O documento não deve criar release notes finais definitivas.

24. O documento não deve declarar data de release.

25. O documento não deve declarar que a alfa foi publicada.

26. O documento não deve prometer estabilidade.

27. O documento não deve prometer suporte formal.

28. O documento não deve prometer SLA.

29. O documento não deve prometer compatibilidade de API.

30. O documento não deve prometer publicação em PyPI.

Requisitos para README.md:
1. Adicionar link curto para docs/release/release-notes-alpha.md.

2. O texto deve deixar claro que são notas preliminares.

3. Não declarar release publicada.

4. Não transformar README em release notes.

5. Manter README enxuto.

Requisitos para CHANGELOG.md:
1. Atualizar seção Não publicado.

2. Registrar criação das release notes alfa preliminares.

3. Não criar seção versionada publicada.

4. Não criar data de release.

5. Não mover o conteúdo para 0.1.0-alpha.1 como publicado.

Requisitos para docs/release/public-alpha-readiness.md:
1. Marcar release notes alfa preliminares como criadas.

2. Manter pendente:
   - revisão final das release notes;
   - execução do checklist pré-tag;
   - criação de tag;
   - publicação da release;
   - internacionalização dos READMEs.

3. Não declarar alfa publicada.

Requisitos para docs/release/alpha-version-plan.md:
1. Apontar para as release notes alfa preliminares.

2. Manter status como planejado, não publicado.

3. Não declarar tag criada.

4. Não declarar release criada.

Requisitos para docs/release/release-policy.md:
1. Apontar para as release notes preliminares como artefato preparatório.

2. Deixar claro que release notes precisam ser revisadas antes da publicação real.

3. Não alterar o processo para publicar automaticamente.

Requisitos para docs/release/pre-release-checklist.md:
1. Incluir revisão das release notes alfa preliminares como item obrigatório antes de tag.

2. Não incluir comando de publicação.

Requisitos para docs/roadmap/mission-backlog.md:
1. Marcar release notes alfa preliminares como concluídas ou em progresso conforme esta missão.

2. Manter como futuras:
   - revisão final pré-release;
   - executar checklist pré-tag;
   - criar tag alfa;
   - publicar release alfa;
   - internacionalizar READMEs.

3. Não criar missões novas na fila.

Requisitos para docs/alignment/current-state.md:
1. Registrar que existem release notes alfa preliminares.

2. Deixar claro que release não foi publicada.

Requisitos para docs/alignment/roadmap.md:
1. Atualizar roadmap para refletir preparação das release notes.

2. Não declarar release feita.

Requisitos para docs/alignment/open-questions.md:
1. Atualizar somente se houver perguntas concretas.

2. Perguntas possíveis:
   - release alfa terá pacote PyPI ou apenas código-fonte;
   - quando revisar release notes finais;
   - quando internacionalizar READMEs.

Requisitos gerais:
1. Tudo deve estar em português do Brasil.

2. Usar linguagem pública, clara e conservadora.

3. Diferenciar:
   - release notes preliminares;
   - release notes finais;
   - versão planejada;
   - tag;
   - release publicada;
   - pacote publicado.

4. Não prometer maturidade inexistente.

5. Não criar tag.

6. Não publicar release.

7. Não publicar pacote.

8. Não alterar código.

9. Não alterar scripts.

10. Não adicionar dependências.

11. Usar links relativos corretos.

12. Usar blocos Markdown quando úteis.

13. Controlar corretamente a quantidade de crases nos blocos Markdown.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não alterar workflow de CI.
- Não criar tag.
- Não criar release.
- Não publicar pacote.
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
- docs/release/release-notes-alpha.md existe.
- O documento se declara preliminar.
- O documento informa que a release não foi publicada.
- O documento informa que a tag não foi criada.
- O documento resume o que está incluído na alfa planejada.
- O documento lista limitações conhecidas.
- O documento aponta para instalação, segurança, release policy e changelog.
- README.md aponta para as release notes preliminares.
- CHANGELOG.md registra a criação das release notes preliminares sem criar versão publicada.
- docs/release/public-alpha-readiness.md registra release notes preliminares como criadas.
- docs/release/alpha-version-plan.md aponta para as release notes.
- docs/release/pre-release-checklist.md inclui revisão das release notes.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhum workflow de CI foi alterado.
- Nenhuma tag foi criada.
- Nenhuma release foi criada.
- Nenhum pacote foi publicado.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
