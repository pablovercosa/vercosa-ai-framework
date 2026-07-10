Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
- CHANGELOG.md
- SECURITY.md
- CODE_OF_CONDUCT.md
- pyproject.toml
- docs/release/public-alpha-readiness.md
- docs/release/versioning-policy.md
- docs/release/alpha-version-plan.md
- docs/release/release-policy.md
- docs/release/pre-release-checklist.md
- docs/release/release-notes-alpha.md
- docs/getting-started/local-installation.md
- docs/getting-started/clean-install-checklist.md
- docs/architecture/module-index.md
- docs/architecture/post-integration-architecture-review.md
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/roadmap/mission-backlog.md
- src/vercosa_ai_framework/cli/README.md
- src/vercosa_ai_framework/cli/main.py
- tests/

Leia também, se existirem:
- .github/workflows/ci.yml
- tests/test_cli_docs_links.py
- tests/test_markdown_links.py
- src/vercosa_ai_framework/docs/
- src/vercosa_ai_framework/cli/
- docs/

Assuma o papel de:
- documentation-quality-engineer;
- cli-engineer;
- test-engineer;
- release-preparation-agent;
- developer-experience-engineer.

Missão:
Criar validador local de links Markdown.

Objetivo:
Adicionar uma validação local, segura e sem rede para verificar links relativos em arquivos Markdown do projeto, ajudando a preparar a documentação pública alfa sem depender de serviços externos, sem validar URLs remotas e sem alterar scripts shell.

Contexto:
- O projeto possui documentação pública crescente.
- O projeto já possui README, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, CHANGELOG e múltiplos documentos em docs/.
- O projeto está se aproximando de uma futura alfa.
- O risco de links relativos quebrados aumentou.
- O CI mínimo deve validar o básico do projeto.
- A validação de links deve ser local, determinística e sem rede.
- URLs externas não devem ser acessadas.
- Âncoras Markdown podem ser tratadas de forma conservadora.
- Esta missão deve criar uma validação pequena, testável e útil.
- Esta missão não deve criar dependências externas.
- Esta missão não deve alterar scripts shell.
- Esta missão não deve criar release.
- Esta missão não deve criar tag.

Entregáveis obrigatórios:
1. Criar ou atualizar código Python para validação local de links Markdown, preferencialmente dentro de:
   - src/vercosa_ai_framework/cli/main.py
   - ou módulo pequeno apropriado em src/vercosa_ai_framework/

2. Criar ou atualizar testes:
   - tests/test_cli_docs_links.py
   - ou tests/test_markdown_links.py
   - ou arquivo de teste coerente com a estrutura existente.

3. Atualizar:
   - src/vercosa_ai_framework/cli/README.md
   - README.md
   - CONTRIBUTING.md
   - docs/release/pre-release-checklist.md
   - docs/release/public-alpha-readiness.md
   - docs/getting-started/clean-install-checklist.md
   - docs/roadmap/mission-backlog.md
   - CHANGELOG.md

4. Atualizar, se necessário:
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md
   - docs/alignment/open-questions.md
   - .github/workflows/ci.yml

5. Não alterar scripts shell.

6. Não adicionar dependências.

7. Não acessar rede.

Requisitos funcionais:
1. Criar uma validação local de links Markdown.

2. A validação deve localizar arquivos Markdown relevantes, incluindo:
   - README.md;
   - CONTRIBUTING.md;
   - CHANGELOG.md;
   - SECURITY.md;
   - CODE_OF_CONDUCT.md;
   - docs/**/*.md;
   - src/vercosa_ai_framework/**/README.md.

3. A validação deve verificar links relativos para arquivos locais.

4. A validação deve identificar links para arquivos inexistentes.

5. A validação deve ignorar links externos, como:
   - https://
   - http://
   - mailto:
   - tel:

6. A validação não deve acessar links externos.

7. A validação não deve fazer requisições HTTP.

8. A validação deve ignorar imagens remotas.

9. A validação deve tratar links com âncoras, como:
   - docs/arquivo.md#secao
   - README.md#instalacao

10. Para links com âncora, a validação mínima obrigatória é verificar se o arquivo existe.

11. A validação de existência da âncora é opcional nesta missão.

12. Se validação de âncora for implementada, deve ser simples, testada e conservadora.

13. A validação deve tratar links relativos com:
   - ./arquivo.md
   - ../arquivo.md
   - docs/arquivo.md
   - pasta/arquivo.md#ancora

14. A validação deve tratar links com espaços codificados de forma básica, se isso for simples.

15. A validação deve ignorar links vazios ou âncoras internas puras, como:
   - #secao

16. A validação deve ignorar blocos de código quando possível.

17. Se ignorar blocos de código for complexo, documentar limitação e testar o comportamento escolhido.

18. A validação deve ser determinística.

19. A saída deve listar arquivos com links quebrados de forma clara.

20. Quando não houver links quebrados, a saída deve indicar sucesso.

21. O comando deve retornar código de saída 0 em sucesso.

22. O comando deve retornar código de saída diferente de 0 quando houver links relativos quebrados.

23. O comando não deve modificar arquivos.

24. O comando não deve criar arquivos.

25. O comando não deve depender de Git.

26. O comando não deve depender de banco.

27. O comando não deve chamar providers.

28. O comando não deve executar missões.

29. O comando não deve executar batch.

30. O comando não deve executar pytest.

31. O comando não deve executar compileall.

Requisitos de CLI:
1. Adicionar comando na CLI operacional.

2. Nome recomendado:
   - docs-links

3. Exemplo conceitual:
   - python3 -m vercosa_ai_framework.cli.main docs-links

4. Se a missão 0092 tiver criado entrypoint local vaf, documentar alternativa:
   - vaf docs-links

5. Não inventar entrypoint global se ele não existir.

6. O comando deve aceitar diretório base opcional se isso for coerente com os comandos existentes.

7. Se aceitar diretório base opcional, usar nome simples, como:
   - --base-dir

8. Se não aceitar diretório base opcional, deve funcionar a partir da raiz do projeto.

9. O comando deve ser seguro e somente leitura.

10. O comando deve integrar-se ao padrão de saída da CLI existente.

11. O comando não deve substituir validate ou doctor.

12. O comando pode ser mencionado como validação complementar de documentação.

13. Preservar comandos existentes:
   - status;
   - validate;
   - doctor;
   - missions;
   - batch-summary.

Requisitos de implementação:
1. Usar somente biblioteca padrão.

2. Não adicionar dependências.

3. Manter implementação pequena e testável.

4. Separar lógica de validação em função testável, se fizer sentido.

5. Evitar regex excessivamente frágil.

6. Validar links Markdown inline básicos:
   - [texto](destino)

7. Validar links de imagem básicos:
   - ![alt](destino)

8. Não implementar parser Markdown completo.

9. Documentar limitação se o parser for simples.

10. Evitar falso positivo em URLs externas.

11. Evitar falso positivo em âncoras internas.

12. Evitar falso positivo em links dentro de blocos de código quando possível.

13. Não ler arquivos binários.

14. Não atravessar diretórios desnecessários, como:
   - .git;
   - .venv;
   - __pycache__;
   - logs;
   - runtime;
   - dist;
   - build;
   - .pytest_cache.

15. Não validar arquivos em missions/done como documentação pública obrigatória, salvo se decidir explicitamente; preferir focar documentação pública.

16. Não validar logs.

17. Não validar arquivos temporários.

18. Manter saída em português do Brasil.

Requisitos de testes:
1. Criar testes unitários para links válidos.

2. Criar testes unitários para link relativo quebrado.

3. Criar testes para link externo ignorado.

4. Criar testes para âncora interna pura ignorada.

5. Criar testes para link com âncora em arquivo existente.

6. Criar testes para múltiplos arquivos Markdown.

7. Criar testes para diretórios ignorados.

8. Criar testes para código de saída do comando, se o padrão da CLI permitir.

9. Usar tmp_path ou diretório temporário.

10. Não depender da documentação real do projeto nos testes unitários.

11. Não acessar rede.

12. Não chamar providers.

13. Não executar missões.

14. Garantir que pytest passe.

Requisitos de CI:
1. Atualizar .github/workflows/ci.yml somente se ele existir após a missão 0093.

2. Se atualizado, adicionar etapa para rodar:
   - python -m vercosa_ai_framework.cli.main docs-links

3. Se entrypoint vaf existir, ainda preferir python -m para CI por ser mais explícito.

4. A etapa deve rodar depois da instalação local e antes ou depois dos testes, conforme fizer sentido.

5. Não usar rede.

6. Não usar secrets.

7. Não adicionar deploy.

8. Não publicar pacote.

Requisitos de documentação:
1. Atualizar src/vercosa_ai_framework/cli/README.md com:
   - propósito do docs-links;
   - forma real de execução;
   - escopo;
   - limites;
   - exemplos;
   - diferença entre docs-links, validate e doctor.

2. Atualizar README.md de forma breve, se houver seção de qualidade ou CLI.

3. Atualizar CONTRIBUTING.md para orientar contribuidores a rodar docs-links quando alterarem documentação.

4. Atualizar docs/release/pre-release-checklist.md para incluir validação de links Markdown antes de tag.

5. Atualizar docs/release/public-alpha-readiness.md para registrar validador local de links.

6. Atualizar docs/getting-started/clean-install-checklist.md para incluir validação de links como etapa opcional ou recomendada.

7. Atualizar docs/roadmap/mission-backlog.md para marcar validador de links como concluído ou em progresso conforme esta missão.

8. Atualizar CHANGELOG.md na seção Não publicado.

9. Não prometer validação de links externos.

10. Não prometer parser Markdown completo.

11. Não prometer validação perfeita de âncoras.

12. Tudo deve estar em português do Brasil.

13. Usar links relativos corretos.

Restrições:
- Não alterar scripts shell.
- Não adicionar dependências.
- Não criar CI de release.
- Não criar tag.
- Não criar release.
- Não publicar pacote.
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
- Não fazer git push.
- Não usar sudo.
- Não alterar configurações globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação, testes e mensagens devem estar em português do Brasil quando aplicável.

Critérios de aceite:
- A CLI possui comando docs-links ou equivalente documentado.
- O comando valida links relativos em Markdown.
- O comando ignora links externos sem acessar rede.
- O comando detecta links relativos quebrados.
- O comando não altera arquivos.
- O comando retorna sucesso quando não há links quebrados.
- O comando retorna falha quando há links quebrados.
- Testes cobrem links válidos, links quebrados, links externos e âncoras.
- CI inclui docs-links se .github/workflows/ci.yml existir.
- src/vercosa_ai_framework/cli/README.md documenta o comando.
- README.md foi atualizado se necessário.
- CONTRIBUTING.md menciona a validação para mudanças documentais.
- docs/release/pre-release-checklist.md inclui validação de links.
- CHANGELOG.md registra a mudança.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
