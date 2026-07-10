Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
- CHANGELOG.md
- SECURITY.md
- CODE_OF_CONDUCT.md
- LICENSE
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
- docs/architecture/post-integration-architecture-review.md
- docs/operations/safe-runner-usage.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md
- src/vercosa_ai_framework/cli/README.md
- tests/test_cli_operacional_inicial.py
- tests/test_cli_validate.py
- tests/test_cli_doctor.py

Leia também, se existirem:
- pyproject.toml
- setup.py
- setup.cfg
- requirements.txt
- requirements-dev.txt
- tox.ini
- Makefile
- tests/test_cli_missions.py
- tests/test_cli_list_missions.py
- tests/test_cli_batch_summary.py

Assuma o papel de:
- installation-validation-engineer;
- release-preparation-agent;
- reliability-engineer;
- test-engineer;
- documentation-agent.

Missão:
Executar e registrar validação de instalação limpa.

Objetivo:
Executar uma validação real e controlada do Vercosa AI Framework em uma cópia local limpa e temporária do repositório, registrar o resultado factual em docs/release/clean-install-validation.md e atualizar a documentação de prontidão para alfa, sem acessar rede, sem publicar release, sem criar tag e sem corrigir silenciosamente problemas encontrados.

Contexto:
- A missão 0087 criou o checklist documental de instalação limpa.
- O checklist ainda não foi executado formalmente.
- O projeto possui versão alfa planejada, mas nenhuma versão alfa foi publicada.
- O projeto precisa validar se um clone limpo consegue reproduzir o ambiente documentado.
- A validação deve usar uma cópia temporária local do repositório.
- A validação não deve depender do diretório de trabalho atual como ambiente de teste.
- A validação não deve acessar GitHub nem qualquer outra rede.
- A validação pode encontrar limitações reais.
- O resultado pode ser:
  - APROVADO;
  - APROVADO COM RESSALVAS;
  - REPROVADO.
- A missão será considerada concluída se a execução for real, o resultado for registrado honestamente e as evidências forem suficientes, mesmo que o resultado técnico seja APROVADO COM RESSALVAS ou REPROVADO.
- Problemas encontrados não devem ser escondidos.
- Correções de código não pertencem a esta missão.
- Correções estruturais relevantes devem ser registradas como pendências futuras.
- Correções pequenas exclusivamente documentais podem ser feitas quando um comando documentado estiver claramente incorreto.

Entregáveis obrigatórios:
1. Executar a validação de instalação limpa em diretório temporário local.

2. Atualizar com o resultado real:
   - docs/release/clean-install-validation.md

3. Atualizar:
   - docs/release/public-alpha-readiness.md
   - docs/release/alpha-version-plan.md
   - docs/roadmap/mission-backlog.md
   - docs/alignment/current-state.md

4. Atualizar, se necessário:
   - docs/getting-started/local-installation.md
   - docs/getting-started/clean-install-checklist.md
   - docs/alignment/roadmap.md
   - docs/alignment/open-questions.md
   - CHANGELOG.md
   - README.md

5. Não alterar código Python.

6. Não alterar scripts shell.

7. Não adicionar dependências.

8. Não criar tag.

9. Não criar release.

10. Não fazer push.

Procedimento obrigatório de validação:
1. Identificar e registrar:
   - branch atual;
   - commit testado;
   - sistema operacional;
   - arquitetura;
   - versão do Python;
   - versão do Git;
   - data e hora da execução.

2. Não registrar:
   - tokens;
   - credenciais;
   - secrets;
   - variáveis de ambiente sensíveis;
   - endereços privados desnecessários;
   - conteúdo de chaves SSH.

3. Criar diretório temporário usando mecanismo seguro, preferencialmente:
   - mktemp -d

4. Configurar limpeza automática do diretório temporário com trap quando possível.

5. Criar uma cópia local limpa do repositório sem acessar rede.

6. Usar clonagem local a partir do repositório atual, preferencialmente com:
   - git clone --no-hardlinks

7. A cópia deve apontar para o commit selecionado para validação.

8. Não usar git pull.

9. Não usar git fetch.

10. Não consultar origin.

11. Verificar na cópia limpa:
   - git status --short;
   - git rev-parse --abbrev-ref HEAD;
   - git rev-parse HEAD;
   - existência de README.md;
   - existência de src/;
   - existência de tests/;
   - existência de scripts/;
   - existência de docs/.

12. Criar ambiente virtual novo dentro da cópia temporária ou em diretório temporário associado:
   - python3 -m venv .venv

13. Se python3 -m venv não estiver disponível:
   - registrar o bloqueio;
   - não usar sudo;
   - não instalar pacotes do sistema;
   - continuar as validações que ainda forem possíveis;
   - classificar o resultado adequadamente.

14. Ativar o ambiente virtual quando ele for criado com sucesso.

15. Registrar:
   - caminho lógico do ambiente virtual, sem expor dados desnecessários;
   - versão do Python dentro do ambiente virtual;
   - versão do pip, se disponível.

16. Inspecionar o mecanismo real de instalação do projeto:
   - pyproject.toml;
   - setup.py;
   - setup.cfg;
   - requirements.txt;
   - requirements-dev.txt;
   - ou ausência desses arquivos.

17. Não inventar suporte a empacotamento.

18. Não executar pip install vercosa-ai-framework.

19. Não consultar PyPI.

20. Não instalar dependências pela internet.

21. Se houver empacotamento local compatível, tentar instalação local sem rede de forma conservadora.

22. Se uma instalação local exigir dependências indisponíveis offline:
   - registrar a limitação;
   - não contornar usando rede;
   - não afirmar que a instalação foi aprovada integralmente.

23. Se o projeto não tiver empacotamento formal:
   - registrar essa condição;
   - validar o uso suportado por PYTHONPATH=src quando aplicável;
   - classificar isso como ressalva ou condição documentada, conforme o estado real do projeto.

24. Não criar pyproject.toml.

25. Não criar setup.py.

26. Não criar requirements.txt.

27. Não alterar arquivos de empacotamento.

Validações obrigatórias na cópia limpa:
1. Verificar estrutura mínima do projeto.

2. Verificar permissões de execução dos scripts operacionais relevantes.

3. Executar, quando suportado:
   - ./scripts/vaf-status.sh

4. Executar a CLI usando a forma real suportada pelo projeto.

5. Validar pelo menos:
   - ajuda da CLI;
   - status;
   - validate;
   - doctor;
   - missions;
   - batch-summary.

6. Não inventar entrypoint global.

7. Se algum comando não existir ou tiver outro nome:
   - registrar o resultado real;
   - corrigir somente documentação claramente desatualizada;
   - não criar o comando nesta missão.

8. Executar:
   - pytest

9. Executar:
   - python3 -m compileall src

10. Preferir executar pytest e compileall usando o ambiente temporário criado.

11. Se pytest não estiver disponível no ambiente virtual e não puder ser instalado sem rede:
   - registrar a limitação;
   - pode ser usada uma segunda execução com o ambiente Python já disponível no servidor apenas como evidência complementar;
   - deixar explícito que essa execução complementar não equivale a instalação completamente isolada.

12. Não ocultar uso de fallback.

13. Registrar quantidade de testes aprovados quando disponível.

14. Registrar falhas de testes de forma resumida e sanitizada.

15. Registrar resultado de compileall.

16. Verificar após os testes:
   - git status --short na cópia temporária.

17. A validação deve identificar se testes ou comandos geraram alterações inesperadas no clone.

18. Não modificar o repositório principal durante a validação, além dos documentos entregáveis da missão.

Validação documental obrigatória:
1. Verificar a existência dos documentos públicos mínimos:
   - README.md;
   - CONTRIBUTING.md;
   - CHANGELOG.md;
   - SECURITY.md;
   - CODE_OF_CONDUCT.md;
   - LICENSE ou pendência claramente documentada;
   - docs/getting-started/local-installation.md;
   - docs/getting-started/clean-install-checklist.md;
   - docs/release/public-alpha-readiness.md;
   - docs/release/versioning-policy.md;
   - docs/release/alpha-version-plan.md;
   - docs/legal/usage-policy.md;
   - docs/architecture/module-index.md.

2. Verificar se os comandos principais do guia de instalação existem de fato.

3. Verificar se a documentação não promete:
   - PyPI inexistente;
   - Docker inexistente;
   - CI inexistente;
   - release alfa inexistente;
   - estabilidade de produção inexistente.

4. Corrigir apenas divergências documentais inequívocas.

5. Não ampliar o escopo para uma reescrita geral dos documentos.

Requisitos para docs/release/clean-install-validation.md:
1. Substituir o modelo preparatório ou adicionar uma seção de execução real.

2. Registrar:
   - status da validação;
   - data;
   - branch;
   - commit testado;
   - sistema operacional;
   - arquitetura;
   - versão do Python;
   - versão do Git;
   - estratégia de clone local;
   - estratégia de ambiente virtual;
   - mecanismo de instalação encontrado;
   - comandos executados;
   - resultado da CLI;
   - resultado do pytest;
   - resultado do compileall;
   - resultado do git status na cópia limpa;
   - problemas encontrados;
   - ressalvas;
   - conclusão.

3. Usar uma classificação explícita:
   - APROVADO;
   - APROVADO COM RESSALVAS;
   - REPROVADO.

4. Não registrar APROVADO se:
   - pytest falhar;
   - compileall falhar;
   - CLI principal não iniciar;
   - passos obrigatórios dependerem de comandos não documentados;
   - instalação exigir rede sem isso estar documentado;
   - houver alteração inesperada relevante no clone.

5. APROVADO COM RESSALVAS pode ser usado quando:
   - o projeto funciona via PYTHONPATH=src, mas ainda não possui empacotamento formal;
   - pytest depende do ambiente global por ausência de dependências instaláveis offline;
   - existe limitação documental claramente registrada;
   - a funcionalidade central funciona, mas a experiência de instalação ainda precisa de melhoria.

6. REPROVADO deve ser usado quando:
   - o projeto não puder ser validado minimamente;
   - testes falharem;
   - compileall falhar;
   - CLI não funcionar;
   - documentação essencial estiver incompatível com a realidade;
   - houver bloqueio estrutural relevante.

7. Não preencher informações inventadas.

8. Não incluir logs extensos.

9. Resumir evidências relevantes.

10. Não expor caminhos sensíveis desnecessários.

11. Registrar claramente qualquer fallback utilizado.

12. Incluir recomendações objetivas para missões futuras quando houver ressalvas ou reprovação.

Requisitos para docs/release/public-alpha-readiness.md:
1. Marcar a execução da instalação limpa como:
   - concluída e aprovada;
   - concluída com ressalvas;
   - ou concluída e reprovada.

2. Não marcar a alfa como pronta se houver bloqueios relevantes.

3. Manter separadas:
   - criação do checklist;
   - execução do checklist;
   - aprovação para release;
   - criação de tag;
   - publicação de release.

4. Não declarar release publicada.

Requisitos para docs/release/alpha-version-plan.md:
1. Atualizar o estado da validação de instalação limpa.

2. Registrar ressalvas ou bloqueios reais.

3. Não criar tag.

4. Não alterar a versão planejada sem justificativa explícita.

5. Não declarar a versão como publicada.

Requisitos para docs/roadmap/mission-backlog.md:
1. Marcar a execução da instalação limpa conforme o resultado real.

2. Criar pendências estratégicas apenas quando forem sustentadas por achados reais.

3. Não criar arquivos em missions/queue.

4. Não transformar automaticamente cada observação em uma nova missão.

5. Manter como futuras, quando aplicável:
   - correção de empacotamento;
   - formalização de versão mínima do Python;
   - CI;
   - revisão final pré-release;
   - tag alfa;
   - release alfa;
   - internacionalização dos READMEs.

Requisitos para docs/alignment/current-state.md:
1. Registrar que a validação de instalação limpa foi executada.

2. Registrar a classificação real.

3. Registrar limitações relevantes.

4. Não afirmar prontidão maior que a evidência disponível.

Requisitos para docs/alignment/roadmap.md:
1. Atualizar somente se o resultado mudar o planejamento da alfa.

2. Manter próximos passos coerentes com o resultado.

Requisitos para docs/alignment/open-questions.md:
1. Atualizar somente se a validação gerar perguntas concretas.

2. Exemplos:
   - qual versão mínima de Python deve ser formalizada;
   - o projeto deve adotar pyproject.toml;
   - como instalar dependências de desenvolvimento sem rede;
   - quando criar CI de instalação limpa;
   - se a alfa será distribuída apenas como código-fonte.

Requisitos para CHANGELOG.md:
1. Atualizar somente se a validação gerar uma mudança documental pública relevante.

2. Não registrar validação como release.

3. Não criar seção versionada.

Requisitos de segurança:
1. Não acessar rede.

2. Não executar curl ou wget.

3. Não executar git fetch ou git pull.

4. Não instalar pacotes de fontes remotas.

5. Não usar sudo.

6. Não registrar variáveis de ambiente completas.

7. Não registrar conteúdo de arquivos de credenciais.

8. Não registrar tokens.

9. Não registrar chaves SSH.

10. Não executar providers.

11. Não chamar modelos.

12. Não executar missões dentro da cópia temporária.

13. Não executar batch dentro da cópia temporária.

14. Não fazer push.

15. Remover o diretório temporário ao final quando seguro.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não adicionar dependências.
- Não criar arquivos de empacotamento.
- Não criar CI.
- Não criar GitHub Actions.
- Não criar Dockerfile.
- Não criar container.
- Não criar tag.
- Não criar release.
- Não publicar pacote.
- Não acessar rede.
- Não acessar banco.
- Não chamar OpenAI.
- Não chamar Gemini.
- Não chamar Ollama.
- Não chamar Claude.
- Não chamar OpenCode como parte da validação interna.
- Não acessar MCPs.
- Não executar providers.
- Não executar missões na cópia temporária.
- Não fazer git push.
- Não usar sudo.
- Não alterar configurações globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- A validação foi realmente executada em cópia local temporária.
- A validação não acessou rede.
- O commit testado foi registrado.
- O ambiente utilizado foi registrado.
- O mecanismo real de instalação foi identificado.
- A CLI foi validada conforme os comandos realmente existentes.
- pytest foi executado ou a impossibilidade foi registrada com precisão.
- compileall foi executado.
- O estado do clone após a validação foi verificado.
- docs/release/clean-install-validation.md contém resultado real.
- O resultado está classificado como APROVADO, APROVADO COM RESSALVAS ou REPROVADO.
- Ressalvas e bloqueios não foram ocultados.
- docs/release/public-alpha-readiness.md foi atualizado conforme o resultado.
- docs/release/alpha-version-plan.md foi atualizado conforme o resultado.
- docs/roadmap/mission-backlog.md foi atualizado conforme o resultado.
- docs/alignment/current-state.md foi atualizado conforme o resultado.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- Nenhuma tag foi criada.
- Nenhuma release foi criada.
- pytest do repositório principal passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.
