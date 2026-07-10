Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
- CHANGELOG.md
- SECURITY.md
- CODE_OF_CONDUCT.md
- pyproject.toml
- docs/getting-started/local-installation.md
- docs/getting-started/clean-install-checklist.md
- docs/release/clean-install-validation.md
- docs/release/public-alpha-readiness.md
- docs/release/versioning-policy.md
- docs/release/alpha-version-plan.md
- docs/roadmap/mission-backlog.md
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/architecture/module-index.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md
- tests/

Leia também, se existirem:
- .github/workflows/
- .github/workflows/ci.yml
- .github/workflows/python.yml
- .github/dependabot.yml
- requirements.txt
- requirements-dev.txt
- setup.py
- setup.cfg
- tox.ini
- noxfile.py

Assuma o papel de:
- ci-engineer;
- release-preparation-agent;
- python-project-maintainer;
- security-reviewer;
- documentation-agent.

Missão:
Criar CI mínimo com GitHub Actions.

Objetivo:
Criar um workflow mínimo e conservador de CI para o Vercosa AI Framework no GitHub Actions, executando instalação local em modo desenvolvimento, testes com pytest e validação de compileall, sem publicar pacote, sem criar release, sem usar secrets e sem executar providers externos.

Contexto:
- O projeto caminha para uma futura alfa pública.
- O projeto já possui documentação pública inicial.
- O projeto já possui SECURITY.md, CODE_OF_CONDUCT.md, templates de issue e pull request.
- O projeto já possui CHANGELOG.md.
- A missão 0092 deve criar empacotamento Python mínimo com pyproject.toml.
- O projeto precisa de CI público mínimo antes de uma alfa mais segura.
- O CI deve validar o básico, não automatizar release.
- O CI não deve depender de tokens privados.
- O CI não deve executar missões.
- O CI não deve executar batch.
- O CI não deve chamar OpenCode.
- O CI não deve chamar providers de IA.
- O CI não deve acessar banco.
- O CI não deve publicar artefatos sensíveis.
- Esta missão deve criar apenas o workflow e atualizar documentação.

Entregáveis obrigatórios:
1. Criar diretório, se necessário:
   - .github/workflows/

2. Criar arquivo:
   - .github/workflows/ci.yml

3. Atualizar:
   - README.md
   - CONTRIBUTING.md
   - docs/release/public-alpha-readiness.md
   - docs/release/alpha-version-plan.md
   - docs/roadmap/mission-backlog.md
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md
   - CHANGELOG.md

4. Atualizar, se necessário:
   - docs/getting-started/local-installation.md
   - docs/getting-started/clean-install-checklist.md
   - docs/alignment/open-questions.md

5. Não alterar código Python, salvo se houver ajuste mínimo indispensável causado por empacotamento incorreto da missão anterior.

6. Não alterar scripts shell.

7. Não adicionar dependências desnecessárias.

Requisitos para .github/workflows/ci.yml:
1. O workflow deve se chamar de forma clara, como:
   - CI

2. O workflow deve rodar em:
   - pull_request;
   - push para main.

3. O workflow deve usar ambiente Linux padrão do GitHub Actions.

4. O workflow deve usar Python compatível com o projeto.

5. Se pyproject.toml declarar requires-python, escolher versão coerente com ele.

6. Se não houver versão mínima formal, usar versão conservadora compatível com o ambiente atual do projeto e registrar a decisão na documentação.

7. O workflow deve executar checkout do repositório.

8. O workflow deve configurar Python.

9. O workflow deve atualizar pip de forma comum e segura.

10. O workflow deve instalar o projeto em modo desenvolvimento, se pyproject.toml suportar:
   - python -m pip install -e .

11. O workflow deve instalar pytest apenas se necessário e de forma explícita.

12. Se o pyproject.toml possuir extra de desenvolvimento, preferir:
   - python -m pip install -e ".[dev]"
   quando isso for realmente suportado.

13. Não inventar extra dev se ele não existir.

14. Não instalar dependências de IA.

15. Não instalar OpenCode.

16. Não instalar Ollama.

17. Não instalar bancos.

18. Não instalar pgvector.

19. Não instalar Docker.

20. Não usar secrets.

21. Não usar variáveis de ambiente com tokens.

22. Não usar cache com conteúdo sensível.

23. Cache de pip pode ser omitido para manter simplicidade.

24. O workflow deve executar:
   - pytest
   - python -m compileall src

25. O workflow pode executar validação básica da CLI se for seguro e sem rede, por exemplo:
   - python -m vercosa_ai_framework.cli.main --help
   - python -m vercosa_ai_framework.cli.main validate
   - python -m vercosa_ai_framework.cli.main doctor
   - python -m vercosa_ai_framework.cli.main missions
   - python -m vercosa_ai_framework.cli.main batch-summary

26. Só incluir comandos de CLI que existam efetivamente após as missões anteriores.

27. Não executar:
   - scripts/vaf-run-batch-safe.sh;
   - scripts/vaf-run-next-safe.sh;
   - scripts/vaf-run-one-mission.sh;
   - qualquer missão;
   - git push;
   - release;
   - build de pacote para publicação.

28. O workflow deve falhar se pytest falhar.

29. O workflow deve falhar se compileall falhar.

30. O workflow deve permanecer curto e legível.

31. Não criar matriz complexa de múltiplas versões nesta missão, salvo se já houver decisão explícita.

32. Não criar deploy.

33. Não criar release.

34. Não publicar pacote.

35. Não criar artefatos.

36. Não rodar em cron.

37. Não rodar em schedule.

38. Não adicionar permissões amplas.

39. Se declarar permissions, usar permissões mínimas, como:
   - contents: read

40. Usar nomes de steps claros.

Requisitos para README.md:
1. Adicionar referência curta ao CI, se houver seção de qualidade, testes ou status.

2. Se adicionar badge, garantir que o caminho do workflow esteja correto.

3. Não adicionar badge se o repositório, branch ou caminho do workflow não estiverem claros.

4. Não declarar que a alfa está publicada.

5. Não declarar que o CI substitui validação local.

6. Manter README enxuto.

Requisitos para CONTRIBUTING.md:
1. Explicar que PRs devem passar no CI.

2. Explicar que validação local ainda é esperada:
   - pytest;
   - python3 -m compileall src;
   - CLI quando aplicável.

3. Explicar que CI não deve depender de secrets.

4. Explicar que contribuições não devem introduzir dependência de provider externo no CI sem missão específica.

5. Manter o documento enxuto.

Requisitos para docs/release/public-alpha-readiness.md:
1. Marcar CI público mínimo como criado.

2. Manter pendentes itens ainda não concluídos, como:
   - revisão final pré-release;
   - criação de tag;
   - publicação de release;
   - internacionalização dos READMEs;
   - eventual matriz de múltiplas versões de Python, se ainda não existir.

3. Não declarar alfa pública como publicada.

Requisitos para docs/release/alpha-version-plan.md:
1. Registrar que CI mínimo passa a ser critério antes da tag alfa.

2. Não criar tag.

3. Não declarar release publicada.

Requisitos para docs/roadmap/mission-backlog.md:
1. Marcar CI mínimo como concluído ou em progresso conforme esta missão.

2. Manter como futuras:
   - matriz de múltiplas versões de Python, se desejado;
   - CI com lint, se desejado;
   - CI com validação de instalação limpa completa;
   - release alfa;
   - internacionalização dos READMEs.

3. Não criar missões novas na fila.

Requisitos para docs/alignment/current-state.md:
1. Registrar que existe CI mínimo com GitHub Actions.

2. Deixar claro que ele valida testes e compileall.

3. Deixar claro que ele não publica pacote.

4. Deixar claro que ele não executa providers.

Requisitos para docs/alignment/roadmap.md:
1. Atualizar roadmap para refletir avanço de prontidão pública.

2. Não declarar release publicada.

Requisitos para docs/alignment/open-questions.md:
1. Atualizar somente se houver perguntas concretas.

2. Possíveis perguntas:
   - quando adicionar matriz de Python;
   - quando adicionar lint;
   - quando adicionar validação de instalação limpa automatizada;
   - quando automatizar release;
   - se release alfa terá pacote ou apenas código-fonte.

Requisitos para CHANGELOG.md:
1. Atualizar a seção Não publicado.

2. Registrar criação do CI mínimo.

3. Não criar seção versionada.

4. Não declarar release publicada.

Requisitos de segurança:
1. Não usar secrets no workflow.

2. Não declarar permissões de escrita.

3. Não executar comandos destrutivos.

4. Não executar missões.

5. Não executar batch.

6. Não chamar providers.

7. Não acessar banco.

8. Não publicar artefatos.

9. Não publicar pacote.

10. Não fazer deploy.

Restrições:
- Não publicar pacote.
- Não criar release.
- Não criar tag.
- Não executar missões.
- Não alterar scripts shell.
- Não adicionar dependências desnecessárias.
- Não criar Dockerfile.
- Não criar container.
- Não criar workflow de deploy.
- Não criar workflow de release.
- Não criar dependabot nesta missão.
- Não criar README.en.md.
- Não criar README.es.md.
- Não internacionalizar READMEs.
- Não acessar rede durante a execução local desta missão.
- Não acessar banco.
- Não chamar OpenAI.
- Não chamar Gemini.
- Não chamar Ollama.
- Não chamar Claude.
- Não chamar OpenCode.
- Não acessar MCPs.
- Não executar providers.
- Não fazer git push.
- Não usar sudo.
- Não alterar configurações globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- .github/workflows/ci.yml existe.
- O workflow roda em push para main e pull_request.
- O workflow usa permissões mínimas.
- O workflow instala o projeto de forma local coerente com pyproject.toml.
- O workflow executa pytest.
- O workflow executa python -m compileall src.
- O workflow não usa secrets.
- O workflow não publica pacote.
- O workflow não cria release.
- O workflow não executa missões.
- O workflow não chama providers.
- README.md foi atualizado se necessário.
- CONTRIBUTING.md menciona CI.
- docs/release/public-alpha-readiness.md registra CI mínimo como criado.
- docs/release/alpha-version-plan.md registra CI como critério pré-release.
- docs/roadmap/mission-backlog.md foi atualizado se necessário.
- CHANGELOG.md registra a mudança.
- Nenhum script shell foi alterado.
- Nenhuma dependência desnecessária foi adicionada.
- pytest passa localmente.
- python3 -m compileall src passa localmente.
- O commit automático usa mensagem em português do Brasil.
