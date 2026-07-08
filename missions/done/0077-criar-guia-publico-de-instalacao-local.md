Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- docs/documentation/readme-standard.md
- docs/architecture/module-index.md
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/roadmap/mission-backlog.md
- docs/operations/safe-runner-usage.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md
- src/vercosa_ai_framework/cli/README.md
- src/vercosa_ai_framework/runtime/README.md
- src/vercosa_ai_framework/missions/README.md
- tests/test_cli_operacional_inicial.py
- tests/test_worker_scripts.py

Assuma o papel de:
- documentation-agent;
- developer-experience-engineer;
- release-preparation-agent;
- technical-editor;
- reliability-engineer.

Missão:
Criar guia público de instalação local.

Objetivo:
Criar um guia inicial de instalação local do Vercosa AI Framework para desenvolvedores, documentando pré-requisitos, clonagem, ambiente Python, instalação em modo desenvolvimento, execução de testes, compileall, uso básico da CLI e validações iniciais, sem prometer release estável e sem alterar código.

Contexto:
- O projeto está caminhando para uma futura alfa pública.
- O README principal deve continuar enxuto.
- O projeto precisa de um guia dedicado para instalação local.
- O guia deve ser factual e refletir o estado atual do projeto.
- O projeto ainda não deve ser apresentado como framework maduro.
- O guia não deve prometer pacote publicado em PyPI se isso ainda não existir.
- O guia não deve prometer instalação global da CLI se isso ainda não existir.
- O guia deve diferenciar instalação para desenvolvimento local de uso final.
- O guia deve estar em português do Brasil.
- A internacionalização dos READMEs continua sendo tarefa futura e não deve ser feita agora.

Entregáveis obrigatórios:
1. Criar documento:
   - docs/getting-started/local-installation.md

2. Criar diretório, se necessário:
   - docs/getting-started/

3. Atualizar:
   - README.md

4. Atualizar, se necessário:
   - docs/roadmap/mission-backlog.md
   - docs/alignment/roadmap.md
   - docs/alignment/current-state.md

5. Não alterar código Python.

6. Não alterar scripts shell.

7. Não adicionar dependências.

Requisitos para docs/getting-started/local-installation.md:
1. O documento deve estar em português do Brasil.

2. O documento deve explicar que o Vercosa AI Framework está em desenvolvimento.

3. O documento deve explicar que a instalação documentada é para desenvolvimento local.

4. O documento deve conter seção de pré-requisitos, incluindo:
   - Git;
   - Python compatível com o projeto;
   - ambiente virtual recomendado;
   - pytest;
   - acesso ao repositório;
   - shell compatível com os scripts existentes quando for usar runners.

5. O documento deve evitar afirmar uma versão exata de Python se o projeto não declarar isso claramente.

6. O documento deve orientar o leitor a verificar a versão de Python com:
   - python3 --version

7. O documento deve documentar clonagem do repositório usando o endereço público ou SSH já usado pelo projeto, sem expor credenciais.

8. O documento deve documentar criação e ativação de ambiente virtual local.

9. O documento deve documentar instalação em modo desenvolvimento, apenas se isso for suportado pelo projeto.

10. Se não houver pyproject.toml, setup.py ou configuração clara de pacote instalável, o documento deve orientar de forma conservadora e marcar instalação empacotada como futura.

11. O documento deve documentar execução de testes:
   - pytest

12. O documento deve documentar validação de compilação:
   - python3 -m compileall src

13. O documento deve documentar validações operacionais básicas:
   - ./scripts/vaf-status.sh
   - python -m vercosa_ai_framework.cli.main --help, ou a forma real compatível com a implementação existente
   - comando de status da CLI, se existir
   - comando validate da CLI, se existir
   - comando doctor da CLI, se existir

14. Não inventar entrypoint global chamado vaf se ele não existir.

15. Não documentar pip install vercosa-ai-framework via PyPI se isso não existir.

16. Não documentar Docker se isso ainda não existir.

17. Não documentar banco de dados como requisito se o projeto ainda não usa banco.

18. Não documentar pgvector como requisito.

19. Não documentar embeddings como requisito.

20. Não documentar RAG semântico como requisito.

21. Explicar que OpenCode é runtime/laboratório atual, mas não requisito para usar contratos Python do framework, salvo quando for executar as missões via fluxo atual.

22. Explicar que alguns scripts operacionais dependem do ambiente local do projeto.

23. Explicar o fluxo mínimo de validação após instalação:
   - entrar no diretório do projeto;
   - verificar status;
   - rodar testes;
   - rodar compileall;
   - rodar CLI de ajuda;
   - não executar batch sem entender o playbook.

24. Incluir seção de problemas comuns, incluindo:
   - pytest não encontrado;
   - ambiente virtual não ativado;
   - comando python aponta para versão errada;
   - scripts sem permissão de execução;
   - limite externo de API se estiver usando runtime com provider;
   - Git com alterações pendentes.

25. Incluir seção de próximos passos, apontando para:
   - README.md;
   - docs/architecture/module-index.md;
   - docs/operations/batch-execution-playbook.md;
   - docs/examples/README.md;
   - docs/roadmap/mission-backlog.md.

26. Incluir blocos de comando Markdown onde forem úteis, com crases corretas.

27. Controlar corretamente blocos Markdown dentro do documento final.

28. Não empobrecer o guia por evitar comandos.

29. Não prometer comportamento ainda não implementado.

Requisitos para README.md:
1. Adicionar link para o guia de instalação local.

2. Manter README enxuto.

3. Não duplicar o guia inteiro.

4. Não prometer instalação global se não existir.

5. Não prometer pacote PyPI se não existir.

6. Não prometer release estável se não existir.

Requisitos para docs/roadmap/mission-backlog.md:
1. Atualizar somente se o backlog mencionar guia de instalação como pendente.

2. Marcar o guia de instalação local como concluído ou em progresso, conforme o conteúdo real.

3. Manter guia de instalação pública completa/release como futuro se ainda faltar.

Requisitos para docs/alignment/roadmap.md:
1. Atualizar somente se fizer sentido registrar avanço rumo à documentação alfa.

2. Não reescrever roadmap inteiro.

Requisitos para docs/alignment/current-state.md:
1. Atualizar somente se estiver desatualizado.

2. Registrar que existe guia inicial de instalação local, se fizer sentido.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não implementar CLI nova.
- Não implementar instalação empacotada.
- Não criar pyproject.toml.
- Não criar setup.py.
- Não publicar pacote.
- Não criar Dockerfile.
- Não criar configuração Docker.
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
- Não alterar configs globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- docs/getting-started/local-installation.md existe.
- O guia explica instalação local para desenvolvimento.
- O guia não promete PyPI se não existir.
- O guia não inventa entrypoint global inexistente.
- O guia documenta testes com pytest.
- O guia documenta compileall.
- O guia documenta validações operacionais básicas.
- O guia aponta para documentos relevantes.
- README.md aponta para o guia.
- Roadmap/backlog foram atualizados somente se necessário.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
