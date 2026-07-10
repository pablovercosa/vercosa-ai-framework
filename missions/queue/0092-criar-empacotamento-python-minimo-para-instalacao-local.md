Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
- CHANGELOG.md
- SECURITY.md
- docs/getting-started/local-installation.md
- docs/getting-started/clean-install-checklist.md
- docs/release/clean-install-validation.md
- docs/release/public-alpha-readiness.md
- docs/release/versioning-policy.md
- docs/release/alpha-version-plan.md
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/roadmap/mission-backlog.md
- docs/architecture/module-index.md
- src/vercosa_ai_framework/cli/README.md
- src/vercosa_ai_framework/cli/main.py
- tests/test_cli_operacional_inicial.py
- tests/test_cli_validate.py
- tests/test_cli_doctor.py
- tests/test_cli_missions.py
- tests/test_cli_batch_summary.py

Leia também, se existirem:
- pyproject.toml
- setup.py
- setup.cfg
- requirements.txt
- requirements-dev.txt
- MANIFEST.in
- VERSION

Assuma o papel de:
- packaging-engineer;
- release-preparation-agent;
- python-project-maintainer;
- developer-experience-engineer;
- test-engineer;
- documentation-agent.

Missão:
Criar empacotamento Python mínimo para instalação local.

Objetivo:
Criar uma configuração mínima e conservadora de empacotamento Python para permitir instalação local em modo desenvolvimento do Vercosa AI Framework, preparando o projeto para futura alfa, sem publicar pacote, sem criar release, sem adicionar dependências externas desnecessárias e sem prometer PyPI.

Contexto:
- A missão 0091 executa e registra a validação de instalação limpa.
- Se a validação apontar ausência de empacotamento formal como ressalva, esta missão deve resolver essa lacuna.
- O projeto usa estrutura src/vercosa_ai_framework.
- A CLI operacional já existe.
- O projeto precisa permitir uma experiência local mais previsível para desenvolvedores.
- O objetivo é empacotamento mínimo, não release pública.
- Esta missão não deve publicar em PyPI.
- Esta missão não deve criar tag.
- Esta missão não deve criar release.
- Esta missão não deve criar CI.
- Esta missão não deve adicionar dependências de runtime sem necessidade.
- Esta missão não deve reestruturar o projeto.

Entregáveis obrigatórios:
1. Criar ou atualizar:
   - pyproject.toml

2. Atualizar, se necessário:
   - README.md
   - docs/getting-started/local-installation.md
   - docs/getting-started/clean-install-checklist.md
   - docs/release/clean-install-validation.md
   - docs/release/public-alpha-readiness.md
   - docs/release/alpha-version-plan.md
   - docs/release/versioning-policy.md
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md
   - docs/alignment/open-questions.md
   - docs/roadmap/mission-backlog.md
   - src/vercosa_ai_framework/cli/README.md
   - CHANGELOG.md

3. Criar ou atualizar testes somente se necessário para cobrir o empacotamento ou entrypoint.

4. Não alterar scripts shell.

5. Não publicar pacote.

6. Não criar tag.

7. Não criar release.

Requisitos para pyproject.toml:
1. Criar pyproject.toml se ele ainda não existir.

2. Se pyproject.toml já existir, atualizar de forma mínima e conservadora.

3. Usar backend de build padrão e simples.

4. Preferir setuptools como backend se não houver decisão existente diferente.

5. Declarar nome do projeto de forma coerente:
   - vercosa-ai-framework

6. Declarar pacote Python correspondente:
   - vercosa_ai_framework

7. Declarar versão de desenvolvimento ou alfa planejada de forma conservadora.

8. Não declarar a versão planejada como release publicada.

9. Se definir version no pyproject.toml, usar a versão planejada documentada:
   - 0.1.0a1
   ou outra forma PEP 440 equivalente à alfa planejada.

10. Não criar inconsistência com docs/release/alpha-version-plan.md.

11. Declarar descrição curta coerente com Harness Engineering.

12. Declarar README.md como readme do pacote.

13. Declarar licença de forma compatível com o arquivo LICENSE existente.

14. Não inventar metadados falsos.

15. Não expor e-mail privado se não houver decisão explícita.

16. Não adicionar classifiers excessivos.

17. Não declarar produção estável.

18. Usar classifier de desenvolvimento compatível com estágio alfa, se fizer sentido.

19. Declarar requires-python somente se houver segurança sobre versão mínima suportada.

20. Se não houver segurança, escolher versão mínima conservadora compatível com o ambiente e registrar a decisão documentalmente.

21. Não adicionar dependências de runtime se o projeto não precisa delas.

22. Não adicionar dependências de desenvolvimento pesadas.

23. Se pytest já é necessário para desenvolvimento, pode ser documentado como dependência opcional de desenvolvimento apenas se isso for coerente.

24. Não depender de rede para funcionamento do pacote instalado localmente, exceto para instalação futura de dependências em ambientes novos.

25. Configurar descoberta de pacotes em src.

26. Não incluir missions, logs, docs ou tests como pacote importável.

27. Não empacotar arquivos privados ou runtime sensível.

28. Não incluir logs.

29. Não incluir secrets.

30. Não incluir arquivos temporários.

31. Se criar entrypoint de console, usar nome conservador e documentado.

32. Nome recomendado de entrypoint, se implementado:
   - vaf

33. O entrypoint deve apontar para a CLI existente.

34. Criar entrypoint somente se for simples, seguro e testável.

35. Se criar entrypoint, documentar que ele é local após instalação em modo desenvolvimento.

36. Não prometer instalação global fora do ambiente virtual.

37. Não alterar comportamento da CLI existente.

38. Não quebrar a execução via:
   - python3 -m vercosa_ai_framework.cli.main

Requisitos de implementação:
1. Manter a alteração mínima.

2. Não reestruturar diretórios.

3. Não mover pacotes.

4. Não renomear módulos.

5. Não alterar scripts shell.

6. Não adicionar dependências externas sem justificativa clara.

7. Não criar setup.py se pyproject.toml for suficiente.

8. Não criar package.json.

9. Não criar Dockerfile.

10. Não criar workflow de CI.

11. Não alterar código Python salvo se for estritamente necessário para entrypoint de CLI.

12. Se alterar código Python para suportar entrypoint, manter mudança mínima e testada.

13. Preservar todos os comandos existentes da CLI.

14. Preservar testes existentes.

15. Não alterar contratos públicos desnecessariamente.

Requisitos de testes:
1. Rodar pytest.

2. Rodar python3 -m compileall src.

3. Se criar entrypoint, criar teste que valide que o entrypoint aponta para função existente ou que a CLI continua invocável.

4. Não depender de instalação de pacote em ambiente externo nos testes unitários.

5. Se testar metadados do pyproject.toml, usar biblioteca padrão quando possível.

6. Não acessar rede.

7. Não publicar pacote.

8. Não criar build de distribuição como requisito obrigatório, salvo se for simples e sem rede.

9. Não chamar providers.

10. Não chamar OpenCode.

Requisitos de documentação:
1. Atualizar docs/getting-started/local-installation.md para documentar instalação local em modo desenvolvimento.

2. Se pyproject.toml for criado, documentar comando local adequado, como:
   - python3 -m pip install -e .

3. Se houver dependências opcionais de desenvolvimento, documentar a forma real definida.

4. Não documentar pip install vercosa-ai-framework via PyPI.

5. Não declarar pacote publicado.

6. Não declarar release alfa publicada.

7. Atualizar docs/getting-started/clean-install-checklist.md com o novo caminho de instalação.

8. Atualizar docs/release/clean-install-validation.md se a validação da 0091 tiver registrado ressalva sobre ausência de empacotamento.

9. Atualizar docs/release/public-alpha-readiness.md para refletir que empacotamento local mínimo existe.

10. Atualizar docs/release/alpha-version-plan.md para refletir que pyproject.toml prepara, mas não publica, a versão alfa.

11. Atualizar docs/release/versioning-policy.md se houver decisão sobre PEP 440.

12. Atualizar docs/alignment/current-state.md para registrar empacotamento local mínimo.

13. Atualizar docs/alignment/open-questions.md para remover ou ajustar pergunta sobre adoção de pyproject.toml, se existir.

14. Atualizar docs/roadmap/mission-backlog.md para marcar empacotamento local mínimo como concluído ou em progresso.

15. Atualizar CHANGELOG.md na seção Não publicado.

16. Atualizar README.md de forma breve, se houver seção de instalação.

17. Atualizar src/vercosa_ai_framework/cli/README.md se entrypoint de console for criado.

18. Tudo deve estar em português do Brasil.

19. Não prometer PyPI.

20. Não prometer estabilidade.

21. Não prometer produção.

22. Não prometer compatibilidade de API.

23. Usar links relativos corretos.

Restrições:
- Não publicar pacote.
- Não criar release.
- Não criar tag.
- Não criar GitHub Actions.
- Não criar CI.
- Não criar Dockerfile.
- Não adicionar dependências desnecessárias.
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
- Documentação, testes e mensagens devem estar em português do Brasil quando aplicável.

Critérios de aceite:
- pyproject.toml existe.
- O empacotamento usa src/vercosa_ai_framework corretamente.
- O pacote pode ser instalado localmente em modo desenvolvimento conforme documentação.
- O projeto não promete PyPI.
- O projeto não declara release publicada.
- A versão documentada é coerente com a alfa planejada.
- README.md e guia de instalação foram atualizados se necessário.
- Checklist de instalação limpa foi atualizado.
- Documentação de release foi atualizada se necessário.
- CHANGELOG.md registra a mudança.
- Nenhum script shell foi alterado.
- Nenhuma dependência desnecessária foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
