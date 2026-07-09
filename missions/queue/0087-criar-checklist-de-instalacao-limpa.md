Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
- CHANGELOG.md
- SECURITY.md
- CODE_OF_CONDUCT.md
- LICENSE
- docs/getting-started/local-installation.md
- docs/release/public-alpha-readiness.md
- docs/release/versioning-policy.md
- docs/release/alpha-version-plan.md
- docs/roadmap/mission-backlog.md
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/architecture/module-index.md
- docs/architecture/post-integration-architecture-review.md
- docs/operations/safe-runner-usage.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md
- src/vercosa_ai_framework/cli/README.md
- tests/test_cli_operacional_inicial.py
- tests/test_cli_validate.py
- tests/test_cli_doctor.py
- tests/test_worker_scripts.py

Leia também, se existirem:
- pyproject.toml
- setup.py
- setup.cfg
- requirements.txt
- requirements-dev.txt
- tox.ini
- noxfile.py
- Makefile
- docs/getting-started/clean-install-checklist.md
- docs/release/clean-install-validation.md

Assuma o papel de:
- release-preparation-agent;
- developer-experience-engineer;
- documentation-agent;
- reliability-engineer;
- installation-reviewer.

Missão:
Criar checklist de instalação limpa.

Objetivo:
Criar um checklist documental para validar instalação limpa do Vercosa AI Framework em ambiente novo, preparando o projeto para futura alfa pública, sem executar a instalação nesta missão, sem alterar código e sem criar automações novas.

Contexto:
- O projeto caminha para uma futura alfa pública.
- O projeto já possui guia de instalação local.
- O projeto já possui documentação de prontidão para alfa pública.
- O projeto já possui estratégia de versionamento e versão alfa planejada.
- Antes de publicar uma alfa, será necessário validar instalação em ambiente limpo.
- Esta missão deve criar o checklist e o procedimento documental, não executar a validação.
- O checklist deve ser conservador e refletir o estado real do projeto.
- O projeto ainda não deve prometer instalação via PyPI se isso não existir.
- O projeto ainda não deve prometer Docker se isso não existir.
- O projeto ainda não deve prometer CI se isso não existir.
- O projeto ainda não deve prometer suporte a produção.
- Esta missão não deve alterar código.
- Esta missão não deve alterar scripts.
- Esta missão não deve adicionar dependências.

Entregáveis obrigatórios:
1. Criar documento:
   - docs/getting-started/clean-install-checklist.md

2. Criar documento:
   - docs/release/clean-install-validation.md

3. Atualizar:
   - docs/getting-started/local-installation.md
   - docs/release/public-alpha-readiness.md
   - docs/release/alpha-version-plan.md
   - docs/roadmap/mission-backlog.md
   - README.md

4. Atualizar, se necessário:
   - CONTRIBUTING.md
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md
   - docs/alignment/open-questions.md

5. Não alterar código Python.

6. Não alterar scripts shell.

7. Não adicionar dependências.

Requisitos para docs/getting-started/clean-install-checklist.md:
1. O documento deve estar em português do Brasil.

2. Explicar que o checklist é para validação manual de instalação limpa.

3. Explicar que instalação limpa significa ambiente novo, sem reaproveitar venv, cache local, artefatos antigos ou diretórios de trabalho já modificados.

4. Explicar que o checklist deve ser executado antes de uma release alfa.

5. Explicar que o checklist não substitui pytest nem compileall.

6. Explicar que o checklist não cria release.

7. Explicar que o checklist não cria tag.

8. Explicar pré-requisitos:
   - Git;
   - Python 3 compatível;
   - shell compatível;
   - acesso ao repositório;
   - ambiente virtual;
   - pytest disponível após instalação das dependências necessárias;
   - permissões locais para executar scripts.

9. Evitar fixar versão exata de Python se o projeto ainda não declarar uma versão mínima formal.

10. Incluir etapa para verificar:
   - python3 --version
   - git --version
   - pwd
   - git status --short

11. Incluir etapa para clonar o repositório em diretório temporário ou limpo.

12. Incluir etapa para criar e ativar ambiente virtual.

13. Incluir etapa para instalar dependências conforme o projeto realmente suporta.

14. Se não houver requirements.txt, pyproject.toml ou setup.py, documentar essa limitação claramente.

15. Não inventar comando pip install -e . se o projeto não suportar empacotamento.

16. Não inventar comando pip install vercosa-ai-framework se não houver pacote publicado.

17. Incluir etapa para validar estrutura básica:
   - ls
   - test -d src
   - test -d tests
   - test -d scripts
   - test -f README.md

18. Incluir etapa para validar scripts operacionais:
   - ./scripts/vaf-status.sh

19. Incluir etapa para validar testes:
   - pytest

20. Incluir etapa para validar compilação:
   - python3 -m compileall src

21. Incluir etapa para validar CLI usando a forma real suportada pelo projeto.

22. Não inventar entrypoint global se ele não existir.

23. Incluir etapa para validar documentação mínima:
   - README.md
   - CONTRIBUTING.md
   - CHANGELOG.md
   - SECURITY.md
   - CODE_OF_CONDUCT.md
   - docs/getting-started/local-installation.md
   - docs/release/public-alpha-readiness.md
   - docs/release/versioning-policy.md
   - docs/release/alpha-version-plan.md

24. Incluir seção de critérios de aprovação:
   - clone limpo;
   - ambiente virtual criado;
   - comandos básicos funcionam;
   - status operacional sem erro;
   - pytest passa;
   - compileall passa;
   - CLI responde;
   - documentação mínima existe;
   - nenhum segredo exposto;
   - nenhuma alteração local inesperada após validação.

25. Incluir seção de critérios de reprovação:
   - dependência ausente sem documentação;
   - teste falhando;
   - compileall falhando;
   - CLI não inicia;
   - scripts sem permissão;
   - documentação mínima ausente;
   - comandos documentados não existem;
   - necessidade de passos manuais não documentados.

26. Incluir seção de problemas comuns:
   - ambiente virtual não ativado;
   - python apontando para versão errada;
   - pytest não instalado;
   - scripts sem permissão de execução;
   - documentação prometendo comando inexistente;
   - Git sujo após validação;
   - diretório antigo reutilizado sem limpeza.

27. Usar blocos de comando Markdown quando úteis.

28. Controlar corretamente a quantidade de crases nos blocos Markdown.

29. Não prometer estabilidade.

30. Não declarar que a validação foi executada.

Requisitos para docs/release/clean-install-validation.md:
1. O documento deve estar em português do Brasil.

2. Explicar como registrar o resultado futuro de uma validação de instalação limpa.

3. Deixar claro que, nesta missão, o documento é preparatório.

4. Criar modelo de registro de validação futura contendo:
   - data;
   - commit testado;
   - branch;
   - sistema operacional;
   - versão do Python;
   - ambiente virtual;
   - comandos executados;
   - resultado de pytest;
   - resultado de compileall;
   - resultado da CLI;
   - problemas encontrados;
   - soluções aplicadas;
   - conclusão;
   - aprovado ou reprovado.

5. Incluir checklist de evidências mínimas, como:
   - saída de git status --short;
   - saída resumida de pytest;
   - saída resumida de compileall;
   - último commit;
   - observações.

6. Não registrar validação falsa.

7. Não preencher dados inventados.

8. Não declarar instalação limpa como concluída.

9. Explicar que o documento será preenchido ou atualizado em missão futura de execução real da validação.

Requisitos para docs/getting-started/local-installation.md:
1. Adicionar link para o checklist de instalação limpa.

2. Diferenciar guia de instalação local de checklist de validação limpa.

3. Corrigir comandos se algum estiver incoerente com o estado real.

4. Não duplicar o checklist inteiro.

Requisitos para docs/release/public-alpha-readiness.md:
1. Atualizar checklist para indicar que o checklist de instalação limpa foi criado.

2. Manter a execução real do checklist como pendente.

3. Manter pendente:
   - execução de instalação limpa;
   - decisão explícita de release;
   - criação de tag;
   - publicação de release;
   - CI público, se ainda não existir;
   - internacionalização dos READMEs.

4. Não declarar alfa pública como publicada.

Requisitos para docs/release/alpha-version-plan.md:
1. Atualizar pendências para incluir execução do checklist de instalação limpa.

2. Diferenciar checklist criado de checklist executado.

3. Não declarar versão alfa publicada.

Requisitos para docs/roadmap/mission-backlog.md:
1. Marcar criação do checklist de instalação limpa como concluída ou em progresso conforme esta missão.

2. Manter como futura:
   - executar instalação limpa real;
   - registrar resultado da instalação limpa;
   - revisão final pré-release;
   - tag alfa;
   - release alfa;
   - CI público;
   - internacionalização dos READMEs.

3. Não criar missões novas na fila.

Requisitos para README.md:
1. Adicionar link curto para o checklist de instalação limpa se houver seção de instalação ou release.

2. Manter README enxuto.

3. Não declarar que instalação limpa foi executada.

4. Não declarar alfa publicada.

Requisitos para CONTRIBUTING.md:
1. Atualizar somente se fizer sentido mencionar checklist de instalação limpa antes de PRs/release.

2. Não transformar CONTRIBUTING.md em guia de instalação.

Requisitos para docs/alignment/current-state.md:
1. Atualizar somente se necessário.

2. Se atualizar, registrar que existe checklist documental de instalação limpa.

3. Deixar claro que a execução real ainda é futura, se for o caso.

Requisitos para docs/alignment/roadmap.md:
1. Atualizar somente se necessário.

2. Manter execução real do checklist como próximo passo.

Requisitos para docs/alignment/open-questions.md:
1. Atualizar somente se houver perguntas relevantes.

2. Perguntas possíveis:
   - qual ambiente será usado para validação limpa;
   - qual versão mínima de Python será formalizada;
   - haverá CI para repetir instalação limpa;
   - haverá container apenas para validação futura.

Requisitos gerais:
1. Tudo deve estar em português do Brasil.

2. Usar linguagem operacional e verificável.

3. Diferenciar:
   - guia de instalação;
   - checklist de instalação limpa;
   - execução real do checklist;
   - release alfa.

4. Não declarar validação executada.

5. Não inventar comandos que o projeto não suporta.

6. Não prometer PyPI.

7. Não prometer Docker.

8. Não prometer CI.

9. Não alterar código.

10. Não alterar scripts.

11. Não adicionar dependências.

12. Usar links relativos corretos.

13. Usar blocos Markdown quando úteis.

14. Controlar corretamente a quantidade de crases nos blocos Markdown.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não executar instalação limpa nesta missão.
- Não criar ambiente virtual nesta missão.
- Não alterar requirements.
- Não criar pyproject.toml.
- Não criar setup.py.
- Não publicar pacote.
- Não criar Dockerfile.
- Não criar CI.
- Não criar GitHub Actions.
- Não criar release.
- Não criar tag.
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
- Não alterar configs globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- docs/getting-started/clean-install-checklist.md existe.
- docs/release/clean-install-validation.md existe.
- O checklist diferencia criação documental de execução real.
- O checklist não inventa PyPI, Docker ou CI.
- O checklist inclui pytest e compileall.
- O checklist inclui validação da CLI de forma compatível com o estado real.
- docs/release/public-alpha-readiness.md marca checklist criado e execução real pendente.
- docs/release/alpha-version-plan.md menciona execução do checklist como pendência.
- README.md aponta para o checklist se apropriado.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
