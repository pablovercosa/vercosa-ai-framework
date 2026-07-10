# Checklist De Instalação Limpa

Links principais: [README principal](../../README.md) | [Instalação local](local-installation.md) | [Prontidão para alfa pública](../release/public-alpha-readiness.md) | [Registro de validação limpa](../release/clean-install-validation.md)

## Objetivo

Este documento define um checklist manual para validar uma instalação limpa do Vercosa AI Framework em ambiente novo antes de uma futura release alfa.

Instalação limpa significa usar um ambiente novo, sem reaproveitar ambiente virtual, cache local, artefatos antigos, diretórios de trabalho já modificados ou checkout usado em desenvolvimento diário.

Este checklist deve ser executado antes de uma release alfa. Uma execução real foi registrada em [clean-install-validation.md](../release/clean-install-validation.md) em 2026-07-10 com resultado `REPROVADO`; portanto, uma nova execução aprovada ainda é necessária antes de qualquer release alfa.

## Limites

- Este checklist não substitui `pytest`.
- Este checklist não substitui `python3 -m compileall src`.
- Este checklist não cria release.
- Este checklist não cria tag.
- Este checklist não publica pacote.
- Este checklist não promete estabilidade.
- Este checklist não valida produção.
- Este checklist não exige Docker, banco de dados, provider externo, OpenCode, Ollama, PostgreSQL ou pgvector para a validação local básica.

## Pré-Requisitos

- Git.
- Python 3 compatível com o projeto. No estado atual, `pyproject.toml` declara `requires-python = ">=3.11"`.
- Shell compatível com os scripts existentes.
- Acesso ao repositório.
- Permissão local para criar e ativar ambiente virtual.
- `pytest` disponível após instalar as dependências necessárias.
- Permissões locais para executar scripts do repositório.

## Verificação Inicial Do Ambiente

Execute em um diretório fora de checkouts antigos do projeto:

```bash
python3 --version
git --version
pwd
```

Se já existir um checkout local que será usado por engano, pare e escolha um diretório temporário ou limpo.

## Clonar Em Diretório Limpo

Use um diretório temporário ou limpo. Exemplo com HTTPS público:

```bash
mkdir -p /tmp/vaf-clean-install
cd /tmp/vaf-clean-install
git clone https://github.com/pablovercosa/vercosa-ai-framework.git
cd vercosa-ai-framework
git status --short
```

Também é aceitável usar SSH quando a chave já estiver autorizada:

```bash
git clone git@github.com:pablovercosa/vercosa-ai-framework.git
cd vercosa-ai-framework
git status --short
```

O resultado esperado de `git status --short` em clone recém-criado é saída vazia.

## Criar E Ativar Ambiente Virtual

Crie o ambiente virtual dentro do checkout limpo:

```bash
python3 -m venv .venv
source .venv/bin/activate
python --version
python -m pip --version
```

Confirme que `python` e `pip` apontam para o ambiente virtual recém-criado antes de continuar.

## Instalar Dependências Suportadas Pelo Projeto

O estado atual possui `pyproject.toml` com empacotamento local e extra de desenvolvimento. Para instalar o checkout limpo em modo editável com dependências de desenvolvimento:

```bash
python -m pip install -e ".[dev]"
```

Essa instalação é local ao ambiente virtual ativo. Ela não significa que exista pacote publicado no PyPI.

Em validações sem rede, esse comando depende de o build backend e as dependências de desenvolvimento já estarem disponíveis localmente. Na execução de 2026-07-10, `python -m pip install --no-index -e ".[dev]"` falhou por ausência local de `hatchling>=1.25`.

Não use `pip install vercosa-ai-framework` como validação deste checklist enquanto não houver pacote publicado e documentado.

Se em algum momento o projeto deixar de possuir `pyproject.toml`, `setup.py` ou arquivo equivalente de empacotamento, a limitação deve ser registrada antes de continuar, porque não haverá comando local de instalação suportado por este checklist.

## Validar Estrutura Básica

Execute na raiz do checkout limpo:

```bash
ls
test -d src
test -d tests
test -d scripts
test -f README.md
git status --short
```

Falha em qualquer comando indica reprovação até diagnóstico. `git status --short` deve continuar vazio neste ponto.

## Validar Documentação Mínima

Confirme a presença dos documentos mínimos:

```bash
test -f README.md
test -f CONTRIBUTING.md
test -f CHANGELOG.md
test -f SECURITY.md
test -f CODE_OF_CONDUCT.md
test -f docs/getting-started/local-installation.md
test -f docs/release/public-alpha-readiness.md
test -f docs/release/versioning-policy.md
test -f docs/release/alpha-version-plan.md
```

O arquivo `LICENSE` ainda é pendência documentada no estado atual. Se a release alfa exigir licença publicada, essa pendência deve ser resolvida antes da publicação.

## Validar Scripts Operacionais

Execute:

```bash
./scripts/vaf-status.sh
```

Se o script não tiver permissão de execução, a instalação limpa deve ser reprovada até que a causa seja entendida. Não altere scripts como parte da validação sem registrar a ação.

## Validar Testes

Execute:

```bash
pytest
```

Falha em teste reprova a instalação limpa até diagnóstico e correção.

## Validar Compilação

Execute:

```bash
python3 -m compileall src
```

Falha de compilação reprova a instalação limpa até diagnóstico e correção.

## Validar CLI

Use a forma conservadora suportada pelo checkout atual, sem depender de entrypoint global:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --help
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main status
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions --state queue
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main batch-summary
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor
```

`missions` é uma verificação opcional de leitura para confirmar quais arquivos `.md` estão em `queue`, `running`, `done` e `failed`. Ele não cria diretórios, não move arquivos, não executa missões e não substitui `./scripts/vaf-status.sh`.

`batch-summary` é uma verificação opcional de leitura para conferir resumo pós-batch local, último log quando existir e lembretes de validação manual. Ele não executa `pytest`, não executa `python3 -m compileall src`, não executa Git, não chama scripts shell, não executa missões e não substitui o checklist pós-batch.

Se o pacote foi instalado no ambiente virtual com `python -m pip install -e ".[dev]"`, os console scripts locais também podem ser verificados dentro do ambiente virtual:

```bash
vaf --help
vercosa --help
```

Esses atalhos não devem ser tratados como entrypoints globais do sistema. Para diagnóstico reproduzível de checkout, prefira a forma explícita com `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main`.

## Validar Ausência De Segredos E Alterações Locais

Faça uma revisão conservadora antes de aprovar:

```bash
git status --short
git log --oneline --decorate -1
```

`git status --short` deve estar vazio. Se houver arquivos modificados, novos ou removidos depois da validação, registre a causa e reprove até entender o estado.

Não publique logs contendo tokens, credenciais, caminhos privados sensíveis, prompts privados ou dados de ambiente não sanitizados.

## Critérios De Aprovação

- Clone limpo criado em diretório temporário ou limpo.
- Ambiente virtual criado e ativado sem reaproveitar `.venv` antigo.
- Comandos básicos de ambiente funcionam.
- `./scripts/vaf-status.sh` executa sem erro.
- `pytest` passa.
- `python3 -m compileall src` passa.
- CLI responde pela forma `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main`.
- Documentação mínima existe.
- Nenhum segredo foi exposto nos registros da validação.
- Nenhuma alteração local inesperada existe após a validação.

## Critérios De Reprovação

- Dependência ausente sem documentação.
- Teste falhando.
- `python3 -m compileall src` falhando.
- CLI não inicia.
- Scripts sem permissão de execução.
- Documentação mínima ausente.
- Comandos documentados não existem.
- Necessidade de passos manuais não documentados.
- Git sujo após a validação sem causa registrada.
- Instalação depende de PyPI, Docker, CI, banco ou provider externo não documentado como requisito real.

## Problemas Comuns

Ambiente virtual não ativado:

```bash
source .venv/bin/activate
python -m pip --version
```

`python` apontando para versão errada:

```bash
python3 --version
python --version
```

`pytest` não instalado:

```bash
python -m pip install -e ".[dev]"
pytest
```

Scripts sem permissão de execução:

```bash
ls -l scripts/vaf-status.sh scripts/vaf-run-next-safe.sh scripts/vaf-run-batch-safe.sh
```

Documentação prometendo comando inexistente:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --help
```

Git sujo após validação:

```bash
git status --short
```

Diretório antigo reutilizado sem limpeza:

```bash
pwd
git status --short
```

Se houver dúvida sobre a origem do diretório, descarte a validação e reinicie em clone novo.

## Registro Do Resultado

Este checklist define o procedimento. O resultado de cada execução real deve ser registrado em [docs/release/clean-install-validation.md](../release/clean-install-validation.md), sem preencher dados inventados e sem declarar aprovação quando a validação não tiver sido executada. O resultado atual registrado é `REPROVADO`.
