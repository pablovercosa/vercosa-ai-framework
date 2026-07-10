# Registro De Validação De Instalação Limpa

Links principais: [README principal](../../README.md) | [Checklist de instalação limpa](../getting-started/clean-install-checklist.md) | [Instalação local](../getting-started/local-installation.md) | [Prontidão para alfa pública](public-alpha-readiness.md) | [Política de release](release-policy.md) | [Checklist pré-tag](pre-release-checklist.md)

## Objetivo

Este documento registra o resultado factual de uma validação manual de instalação limpa do Vercosa AI Framework executada em cópia temporária local do repositório.

O checklist operacional está em [docs/getting-started/clean-install-checklist.md](../getting-started/clean-install-checklist.md). A execução registrada abaixo não aprova release, não cria tag, não publica alfa, não publica pacote e não corrige automaticamente problemas encontrados.

O resultado deste registro deve ser revisado antes de executar o [checklist pré-tag](pre-release-checklist.md). O estado atual permanece `REPROVADO` até nova validação aprovada ou decisão explícita de exceção com risco aceito.

## Regras De Registro

- Não registre validação falsa.
- Não preencha dados inventados.
- Não declare aprovação sem execução real.
- Não oculte falhas encontradas durante a validação.
- Não publique saídas com tokens, credenciais, prompts privados ou dados sensíveis.
- Diferencie falha de instalação, falha de teste, falha documental e pendência de release.

## Validação De Instalação Limpa - 2026-07-10

Status da validação: `REPROVADO`.

Data e hora da execução: `2026-07-10T13:05:56Z`.

Branch de origem testada: `main`.

Commit testado: `365ea328399495434d3727fcf212f8aaf4ae25f4`.

Sistema operacional: `Linux 7.0.0-1007-oracle #7-Ubuntu SMP PREEMPT Fri Jun 19 02:38:12 UTC 2026 aarch64 GNU/Linux`.

Arquitetura: `aarch64`.

Python do sistema: `Python 3.14.4`.

Git: `git version 2.53.0`.

Estratégia de clone local: clone local com `git clone --no-hardlinks` a partir do repositório atual, seguido de checkout explícito do commit testado em `HEAD` destacado. Não foram usados `git fetch`, `git pull`, consulta a `origin`, rede, `sudo`, providers, banco, OpenCode, Ollama, LLMs ou MCPs.

Estratégia de diretório temporário: diretório criado com `mktemp -d`, com remoção automática por `trap` ao final da execução.

Estratégia de ambiente virtual: `.venv` novo criado dentro da cópia temporária com `python3 -m venv .venv`.

Python no ambiente virtual: `Python 3.14.4`.

pip no ambiente virtual: `pip 25.1.1`.

Mecanismo de instalação encontrado: `pyproject.toml` com build backend `hatchling.build`, `requires-python = ">=3.11"`, dependências runtime vazias, extra de desenvolvimento `pytest>=8.0` e console scripts `vaf` e `vercosa`.

## Comandos Executados

Comandos e verificações executados de forma resumida:

```bash
mktemp -d
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git clone --no-hardlinks <repo-local> <tmp>/repo
git checkout --detach 365ea328399495434d3727fcf212f8aaf4ae25f4
git status --short
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
test -f README.md
test -d src
test -d tests
test -d scripts
test -d docs
test -f README.md
test -f CONTRIBUTING.md
test -f CHANGELOG.md
test -f SECURITY.md
test -f CODE_OF_CONDUCT.md
test -f docs/getting-started/local-installation.md
test -f docs/getting-started/clean-install-checklist.md
test -f docs/release/public-alpha-readiness.md
test -f docs/release/versioning-policy.md
test -f docs/release/alpha-version-plan.md
test -f docs/legal/usage-policy.md
test -f docs/architecture/module-index.md
python3 -m venv .venv
python --version
python -m pip --version
python -m pip install --no-index -e ".[dev]"
./scripts/vaf-status.sh
PYTHONPATH=src python -m vercosa_ai_framework.cli.main --help
PYTHONPATH=src python -m vercosa_ai_framework.cli.main status
PYTHONPATH=src python -m vercosa_ai_framework.cli.main validate
PYTHONPATH=src python -m vercosa_ai_framework.cli.main doctor
PYTHONPATH=src python -m vercosa_ai_framework.cli.main missions
PYTHONPATH=src python -m vercosa_ai_framework.cli.main batch-summary
PYTHONPATH=src pytest
PYTHONPATH=src python -m compileall src
git status --short
```

## Resultado Da Estrutura Mínima

Estrutura obrigatória encontrada na cópia limpa:

| Item | Resultado |
| --- | --- |
| `README.md` | presente |
| `src/` | presente |
| `tests/` | presente |
| `scripts/` | presente |
| `docs/` | presente |

Documentação pública mínima:

| Item | Resultado |
| --- | --- |
| `README.md` | presente |
| `CONTRIBUTING.md` | presente |
| `CHANGELOG.md` | presente |
| `SECURITY.md` | presente |
| `CODE_OF_CONDUCT.md` | presente |
| `LICENSE` | ausente, já documentado como pendência |
| `docs/getting-started/local-installation.md` | presente |
| `docs/getting-started/clean-install-checklist.md` | presente |
| `docs/release/public-alpha-readiness.md` | presente |
| `docs/release/versioning-policy.md` | presente |
| `docs/release/alpha-version-plan.md` | presente |
| `docs/legal/usage-policy.md` | presente |
| `docs/architecture/module-index.md` | presente |

Permissões dos scripts operacionais relevantes:

```text
scripts/vaf-run-batch-safe.sh: executável
scripts/vaf-run-next-safe.sh: executável
scripts/vaf-status.sh: executável
```

## Resultado Da Instalação Local Offline

Resultado: falhou.

Comando executado:

```bash
python -m pip install --no-index -e ".[dev]"
```

Saída resumida:

```text
ERROR: Could not find a version that satisfies the requirement hatchling>=1.25 (from versions: none)
ERROR: No matching distribution found for hatchling>=1.25
```

Interpretação: o projeto possui empacotamento local em `pyproject.toml`, mas a instalação editável offline depende do build backend `hatchling>=1.25`. Como o ambiente temporário não possuía esse backend disponível localmente e a validação não podia consultar rede ou PyPI, a instalação local editável não foi concluída.

Console scripts: `vaf` e `vercosa` não ficaram disponíveis no ambiente virtual porque a instalação local falhou.

Fallback utilizado: uso via `PYTHONPATH=src` para validar a CLI e execução de `pytest` disponível pelo ambiente do servidor. Esse fallback é evidência complementar e não equivale a instalação isolada completamente aprovada.

## Resultado Da CLI

Forma validada: `PYTHONPATH=src python -m vercosa_ai_framework.cli.main` dentro do ambiente virtual temporário.

| Comando | Resultado |
| --- | --- |
| `--help` | passou |
| `status` | passou |
| `validate` | falhou |
| `doctor` | falhou |
| `missions` | passou |
| `batch-summary` | passou |

Falha resumida de `validate` e `doctor`:

```text
problema[mission_subdir_missing]: Diretorio obrigatorio ausente: missions/running
problema[mission_subdir_missing]: Diretorio obrigatorio ausente: missions/failed
```

Interpretação: a cópia limpa do commit testado não contém os diretórios vazios `missions/running` e `missions/failed`, porque diretórios vazios não são versionados pelo Git. A CLI considera esses diretórios obrigatórios para uma estrutura saudável.

## Resultado Do Script Operacional

`./scripts/vaf-status.sh` retornou código de sucesso, mas a saída exibiu estado do repositório principal, não da cópia temporária. A causa observada no script é o uso de caminho absoluto para o checkout principal.

Interpretação: o script é executável, mas não valida corretamente uma cópia limpa temporária quando invocado fora do checkout principal. Esta missão não alterou scripts shell; o achado deve ser tratado em missão futura.

## Resultado Do Pytest

Resultado: passou como evidência complementar, com ressalva.

Saída resumida:

```text
416 passed
```

Ressalva: a instalação editável offline falhou antes de instalar o extra `dev`; portanto, a disponibilidade de `pytest` durante a execução veio do ambiente já existente do servidor, mesmo com o ambiente virtual ativo. Essa evidência valida a suíte no clone, mas não comprova uma instalação de desenvolvimento completamente isolada.

## Resultado Do Compileall

Resultado: passou.

Comando executado no ambiente temporário:

```bash
PYTHONPATH=src python -m compileall src
```

Saída resumida:

```text
compileall concluiu sem erro
```

## Resultado Do Git Status Na Cópia Limpa

Antes da validação: `git status --short` sem saída.

Depois da validação: `git status --short` sem saída.

Não houve alteração inesperada relevante no clone temporário após testes e `compileall`.

## Problemas Encontrados

- A instalação editável offline falhou porque `hatchling>=1.25` não estava disponível localmente e a validação não podia acessar PyPI.
- `validate` e `doctor` falharam porque `missions/running` e `missions/failed` não existem no clone limpo do commit testado.
- `./scripts/vaf-status.sh` usa caminho absoluto para o checkout principal e, por isso, não representa corretamente a cópia temporária limpa.
- `LICENSE` permanece ausente, embora a pendência já esteja documentada.
- Os console scripts `vaf` e `vercosa` não puderam ser validados porque a instalação local falhou.

## Ressalvas

- A CLI funciona parcialmente via `PYTHONPATH=src`, mas a experiência de instalação limpa não está aprovada.
- `pytest` passou como evidência complementar, não como prova de ambiente de desenvolvimento isolado instalado a partir do projeto.
- No commit validado, o pacote declarava `license = { text = "MIT" }` em `pyproject.toml`, enquanto a documentação pública afirmava que `LICENSE` final permanecia pendente. Essa inconsistência foi tratada posteriormente no empacotamento local mínimo, mas a licença final continua pendente antes da alfa.

## Conclusão

Conclusão: a validação limpa foi executada de forma real em cópia temporária local, sem rede e sem publicar artefatos, mas o commit testado não atende aos critérios mínimos para aprovação de instalação limpa.

Nota posterior: missão de empacotamento local mínimo ajustou `pyproject.toml` para `setuptools`, versão PEP 440 `0.1.0a1`, pacote em `src/vercosa_ai_framework` e entrypoint local `vaf`. Este registro histórico permanece `REPROVADO` porque descreve o commit validado; uma nova execução do checklist ainda é necessária antes de qualquer tag, release ou pacote.

Resultado final: `REPROVADO`.

Recomendações objetivas para missões futuras:

- Garantir que diretórios operacionais vazios obrigatórios existam em clones limpos, por exemplo com arquivos sentinela documentados, sem alterar o contrato por acidente.
- Corrigir `scripts/vaf-status.sh` para operar sobre o checkout atual ou aceitar raiz do projeto, sem caminho absoluto para o ambiente do mantenedor.
- Definir estratégia de instalação offline ou documentar explicitamente que `python -m pip install -e ".[dev]"` exige build backend e dependências previamente disponíveis localmente ou acesso controlado a índice remoto.
- Resolver a inconsistência entre licença pendente na documentação e metadado `MIT` em `pyproject.toml`.
- Reexecutar a validação limpa antes de qualquer tag ou release alfa.
