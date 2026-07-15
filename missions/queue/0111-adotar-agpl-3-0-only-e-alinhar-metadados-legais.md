---
id: "0111"
title: "Adotar AGPL-3.0-only e alinhar metadados legais"
base_contract: "v1"
roles:
  - open-source-license-reviewer
  - python-packaging-engineer
  - legal-documentation-reviewer
  - release-readiness-auditor
  - test-engineer
agents:
  - framework-architect
network: allow
database: deny
providers: deny
git_push: deny
git_tag: deny
release: deny
package_publish: deny
sudo: deny
destructive_commands: deny
---

# Objetivo

Adotar formalmente a GNU Affero General Public License versão 3 como licença
do Vercosa AI Framework, usando exclusivamente a expressão SPDX:

`AGPL-3.0-only`

Criar o arquivo `LICENSE` com o texto oficial e inalterado da GNU, alinhar os
metadados de empacotamento Python, atualizar a documentação legal e remover a
licença ausente como bloqueio factual de prontidão alfa.

A missão não autoriza tag, release, publicação de pacote ou declaração de que
todos os gates da alfa foram aprovados.

# Decisão Do Mantenedor

O mantenedor decidiu explicitamente adotar:

- licença: GNU Affero General Public License v3.0 only;
- identificador SPDX: `AGPL-3.0-only`;
- política de versão da licença: somente versão 3, sem cláusula automática
  `or-later`.

Essa decisão substitui a pendência anteriormente registrada entre licenças
permissivas e copyleft.

Não reabrir a escolha entre MIT, Apache-2.0, GPL ou AGPL nesta missão.

# Estado De Partida

Antes desta missão:

- não existe arquivo `LICENSE` na raiz;
- `docs/legal/license-notes.md` registra a licença como pendente;
- `docs/legal/README.md` registra que não há licença final;
- `pyproject.toml` não possui `license`;
- `pyproject.toml` não possui `license-files`;
- o build backend é `setuptools.build_meta`;
- `build-system.requires` usa `setuptools>=61`;
- `alpha-readiness` considera `LICENSE` um arquivo obrigatório;
- a reavaliação 0110 classificou o projeto como `NÃO PRONTO`;
- a ausência de `LICENSE` foi o bloqueio persistente principal da 0110;
- testes, compilação e CI estavam aprovados ao final do ciclo 0101-0110.

Os diagnósticos históricos anteriores devem permanecer factuais para os
commits que avaliaram.

# Acesso À Rede

O acesso à rede está autorizado exclusivamente para consultar fontes oficiais
necessárias à licença e aos metadados de empacotamento.

Fontes permitidas:

- `https://www.gnu.org/licenses/agpl-3.0.txt`
- `https://www.gnu.org/licenses/agpl-3.0.html`
- `https://spdx.org/licenses/AGPL-3.0-only.html`
- `https://packaging.python.org/`
- `https://setuptools.pypa.io/`

Não utilizar:

- blogs;
- respostas de fóruns;
- textos copiados de repositórios de terceiros;
- geradores de licença não oficiais;
- traduções como substituição do texto jurídico oficial;
- resumos produzidos por IA como conteúdo de `LICENSE`.

Caso o texto oficial da GNU não possa ser obtido ou verificado, interromper a
missão de forma segura. Não sintetizar nem reconstruir o texto de memória.

# Texto Oficial Da Licença

Criar na raiz:

- `LICENSE`

O arquivo deve conter o texto integral oficial disponível em:

`https://www.gnu.org/licenses/agpl-3.0.txt`

Requisitos:

- preservar o texto oficial;
- preservar o idioma original;
- não traduzir;
- não resumir;
- não adaptar cláusulas;
- não substituir AGPL por GPL;
- não adicionar comentários dentro do texto;
- não adicionar cabeçalho personalizado antes do texto;
- não adicionar rodapé depois do texto;
- não inserir Markdown;
- não inserir URL como substituição do conteúdo;
- manter terminação de linha textual válida.

Verificar, no mínimo, que o arquivo contém:

- `GNU AFFERO GENERAL PUBLIC LICENSE`;
- `Version 3, 19 November 2007`;
- a seção sobre interação remota por rede;
- os termos finais de aplicação da licença.

O arquivo deve ser tratado como artefato jurídico canônico. Explicações em
linguagem simples devem ficar na documentação, não dentro de `LICENSE`.

# Metadados De Empacotamento

Atualizar `pyproject.toml`.

Em `[build-system]`, alterar o requisito para:

`setuptools>=77.0.3`

Em `[project]`, adicionar:

`license = "AGPL-3.0-only"`

`license-files = ["LICENSE"]`

Preservar:

- nome do pacote;
- versão `0.1.0a1`;
- entrypoint `vaf`;
- layout `src`;
- dependências runtime vazias;
- extra de desenvolvimento;
- configuração atual do pytest.

Não adicionar classificador de licença legado quando a expressão SPDX moderna
já estiver declarada.

Não criar configuração de publicação.

Não adicionar token, repositório PyPI, workflow de release ou credencial.

# Testes De Empacotamento

Atualizar apenas quando necessário:

- `tests/test_python_packaging.py`

Adicionar verificações para garantir que:

- o build backend continua sendo `setuptools.build_meta`;
- `setuptools>=77.0.3` está declarado;
- `project.license` é exatamente `AGPL-3.0-only`;
- `project.license-files` é exatamente `["LICENSE"]`;
- o arquivo `LICENSE` existe;
- o texto identifica GNU Affero General Public License;
- o texto identifica versão 3;
- o texto contém a cláusula de interação remota por rede;
- o entrypoint e os demais metadados existentes continuam preservados.

Não testar uma tradução ou resumo da licença.

Não fixar teste a espaços ou quebras de linha irrelevantes.

# Validação Do Artefato De Distribuição

Construir localmente uma wheel temporária apenas para inspeção.

A construção:

- deve usar diretório temporário;
- não deve publicar nada;
- não deve criar arquivo permanente em `dist/`;
- não deve deixar wheel, sdist ou diretório de build no repositório;
- deve verificar que `LICENSE` está incluído nos metadados da distribuição;
- deve verificar que a expressão de licença aparece nos metadados gerados;
- deve remover os artefatos temporários ao final.

Uma construção local de teste não representa autorização para publicar pacote.

Caso uma dependência de build precise ser obtida, limitar o acesso à
infraestrutura oficial do ecossistema Python necessária ao build.

Não executar upload.

# Documentação Legal

Atualizar:

- `docs/legal/README.md`;
- `docs/legal/license-notes.md`.

`docs/legal/license-notes.md` deve deixar de tratar a licença como pendente e
registrar:

- decisão por `AGPL-3.0-only`;
- data da adoção;
- motivo declarado pelo mantenedor: preservar reciprocidade do código aberto;
- diferença resumida entre uso, modificação, distribuição e serviço por rede;
- obrigação de fornecer código-fonte correspondente nos casos cobertos;
- preservação dos avisos e da licença;
- inexistência de autorização para relicenciamento unilateral;
- uso comercial permitido sob os termos da licença;
- ausência de garantia;
- limite entre resumo informativo e texto jurídico vinculante;
- link relativo para `../../LICENSE`;
- recomendação de análise jurídica para integrações complexas.

A explicação deve ser conservadora.

Não afirmar que toda modificação privada precisa ser publicada.

Não afirmar que qualquer programa que apenas se comunique com o VAF se torna
automaticamente AGPL.

Não criar aconselhamento jurídico individualizado.

# Contribuições

Revisar e atualizar:

- `CONTRIBUTING.md`

Registrar de forma objetiva que:

- contribuições aceitas passam a integrar o projeto sob
  `AGPL-3.0-only`;
- o contribuidor deve possuir direito de submeter o código;
- o contribuidor não deve inserir código incompatível ou sem autorização;
- dependências e trechos de terceiros devem ter licença identificada;
- esta missão não cria CLA;
- esta missão não exige transferência de copyright ao mantenedor.

Não inventar processo jurídico ainda inexistente.

# README E Estado Público

Atualizar minimamente:

- `README.md`;
- `docs/release/public-alpha-readiness.md`;
- `docs/release/release-notes-alpha.md`;
- `docs/alignment/implementation-status.md`;
- `docs/alignment/current-state.md`;
- `docs/alignment/open-questions.md`;
- `docs/alignment/roadmap.md`;
- `docs/roadmap/mission-backlog.md`;
- `CHANGELOG.md`.

No README, criar ou atualizar uma seção curta de licença contendo:

- nome GNU Affero General Public License v3.0 only;
- expressão `AGPL-3.0-only`;
- link para `LICENSE`;
- resumo não jurídico da reciprocidade;
- aviso de que o texto do `LICENSE` prevalece.

Nos documentos vivos:

- remover a afirmação de que a licença ainda não foi escolhida;
- remover `LICENSE` ausente como bloqueio atual;
- registrar a licença como adotada;
- preservar outros bloqueios e ressalvas;
- não declarar automaticamente a alfa pronta;
- não autorizar tag ou release;
- não duplicar extensamente o texto jurídico;
- manter `implementation-status.md` como fonte factual canônica.

Atualizar as release notes preliminares para informar a licença planejada da
futura alfa, sem declarar release publicada.

# Preservação Histórica

Não reescrever as conclusões históricas de:

- `docs/release/clean-install-validation.md`;
- `docs/release/alpha-readiness-diagnostic.md`;
- `docs/release/pre-tag-checklist-execution.md`;
- `docs/release/alpha-readiness-reassessment-0110.md`;
- auditorias anteriores.

Esses documentos devem continuar registrando que `LICENSE` estava ausente nos
commits e datas avaliados.

Quando necessário para navegação, pode ser adicionada uma nota posterior curta,
claramente identificada como posterior, sem alterar:

- classificação original;
- data;
- commit avaliado;
- evidências originais;
- conclusão histórica.

Preferir não alterar relatórios históricos quando os documentos vivos já forem
suficientes.

# Alpha Readiness

Executar:

`PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main alpha-readiness`

Durante a execução, `running=1` pode corresponder à própria missão 0111.

Distinguir:

- bloqueio persistente por licença;
- estado transitório da missão em execução;
- demais ressalvas de release.

Após a criação válida de `LICENSE`, o diagnóstico não deve continuar relatando:

`Arquivo obrigatorio ausente: LICENSE`

A missão não deve forçar artificialmente classificação `PRONTO`.

O resultado final após a movimentação para `done` será revalidado pelo
mantenedor.

# Entregáveis

Entregáveis obrigatórios:

- `LICENSE`;
- `pyproject.toml` atualizado;
- testes de metadados de licença;
- documentação legal atualizada;
- README alinhado;
- documentação viva de prontidão alinhada;
- changelog atualizado.

Entregáveis opcionais somente quando necessários:

- notas posteriores curtas em documentos históricos;
- pequenos ajustes de links relativos.

# Arquivos Permitidos

A missão pode alterar somente:

- `LICENSE`;
- `pyproject.toml`;
- `tests/test_python_packaging.py`;
- `README.md`;
- `CONTRIBUTING.md`;
- `CHANGELOG.md`;
- `docs/legal/README.md`;
- `docs/legal/license-notes.md`;
- `docs/release/public-alpha-readiness.md`;
- `docs/release/release-notes-alpha.md`;
- `docs/alignment/implementation-status.md`;
- `docs/alignment/current-state.md`;
- `docs/alignment/open-questions.md`;
- `docs/alignment/roadmap.md`;
- `docs/roadmap/mission-backlog.md`;
- notas posteriores estritamente necessárias nos relatórios históricos
  explicitamente relacionados à licença;
- movimentação final da própria missão realizada pelo runner.

Não alterar todos esses arquivos automaticamente. Alterar somente os que
realmente contiverem estado desatualizado ou precisarem de alinhamento.

# Limites

Esta missão não deve:

- alterar módulos em `src/`;
- alterar scripts shell;
- alterar `.github/workflows/`;
- alterar Specs;
- alterar ADRs;
- alterar `AGENTS.md`;
- alterar o contrato base;
- alterar templates de missão;
- criar `NOTICE` sem necessidade demonstrada;
- criar CLA;
- transferir copyright;
- escolher `AGPL-3.0-or-later`;
- trocar a licença decidida;
- traduzir o texto jurídico;
- publicar pacote;
- criar tag;
- criar GitHub Release;
- fazer push;
- criar missão 0112;
- executar outra missão;
- mover manualmente o próprio arquivo para `missions/done`.

# Validações Obrigatórias

Executar e registrar:

- verificação do texto oficial do `LICENSE`;
- validação de `pyproject.toml` com `tomllib`;
- testes de empacotamento direcionados;
- `pytest`;
- `python3 -m compileall src`;
- `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main docs-links`;
- `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main alpha-readiness`;
- construção temporária da wheel;
- inspeção da wheel para confirmar inclusão de `LICENSE`;
- inspeção dos metadados gerados;
- `git diff --check`;
- revisão completa do diff;
- confirmação de ausência de artefatos de build no worktree.

Resultados não zero causados exclusivamente pela própria missão em
`missions/running` devem ser registrados como transitórios.

Falhas de teste, empacotamento, texto de licença, links ou metadados não devem
ser mascaradas.

# Critérios Específicos De Aceite

A missão será aceita somente se:

- `LICENSE` existir na raiz;
- `LICENSE` contiver o texto oficial integral da AGPLv3;
- o texto jurídico não tiver sido traduzido ou adaptado;
- a expressão SPDX for exatamente `AGPL-3.0-only`;
- `pyproject.toml` declarar `license`;
- `pyproject.toml` declarar `license-files`;
- `setuptools>=77.0.3` estiver declarado;
- a wheel temporária incluir `LICENSE`;
- os metadados da distribuição indicarem a licença correta;
- os testes de empacotamento cobrirem a decisão;
- a documentação legal não continuar dizendo que a licença está pendente;
- o README apontar para `LICENSE`;
- contribuições estiverem alinhadas à licença;
- relatórios históricos preservarem suas conclusões originais;
- `alpha-readiness` não relatar `LICENSE` ausente;
- outros bloqueios não forem ocultados;
- nenhuma tag for criada;
- nenhuma release for publicada;
- nenhum pacote for publicado;
- nenhuma missão 0112 for criada;
- `pytest` passar;
- `compileall` passar;
- `docs-links` passar;
- `git diff --check` passar;
- o worktree não contiver artefatos temporários;
- a implementação produzir um único commit próprio.

# Próximo Passo

Após conclusão, revisão, push manual e CI aprovado da 0111, uma missão futura
poderá reexecutar a validação de instalação limpa.

Essa missão futura não deve ser criada nesta execução.

# Referência Operacional

O contrato base está em `missions/base/EXECUTION_CONTRACT.md` e é composto
obrigatoriamente pelo runner.

A movimentação final de `missions/running` para `missions/done` é
responsabilidade exclusiva do runner seguro.
