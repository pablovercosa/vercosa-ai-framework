# Instalação Local Para Desenvolvimento

Links principais: [README principal](../../README.md) | [Checklist de instalação limpa](clean-install-checklist.md) | [Índice de módulos](../architecture/module-index.md) | [Playbook de execução em batch](../operations/batch-execution-playbook.md) | [Exemplos](../examples/README.md) | [Backlog estratégico](../roadmap/mission-backlog.md)

## Objetivo

Orientar a instalação local do Vercosa AI Framework para desenvolvimento, validação inicial e uso básico da CLI no estado atual do projeto.

Este guia é para trabalhar em um checkout local do repositório. Ele não descreve uma release estável, não pressupõe pacote publicado no PyPI e não apresenta o framework como produto maduro.

Para validar uma instalação limpa em ambiente novo antes de uma futura alfa, use o [checklist de instalação limpa](clean-install-checklist.md). Este guia orienta instalação local para desenvolvimento; o checklist de instalação limpa orienta uma validação manual, conservadora e registrável em ambiente novo.

## Estado Atual

O Vercosa AI Framework está em desenvolvimento. O repositório possui contratos e MVPs em Python, scripts operacionais locais e uma CLI operacional inicial, mas ainda há lacunas importantes como release alfa, providers reais obrigatórios, RAG semântico, embeddings, pgvector como adapter real e integração completa ponta a ponta.

OpenCode é o runtime e laboratório atual do projeto. Ele não é requisito para importar e validar os contratos Python do framework, mas pode ser necessário quando o operador for executar missões pelo fluxo operacional atual baseado em runtime e scripts do repositório.

## Pré-Requisitos

Requisitos mínimos para seguir este guia:

- Git.
- Acesso ao repositório público ou acesso SSH autorizado ao repositório.
- Python compatível com o projeto. O `pyproject.toml` declara `requires-python = ">=3.11"`.
- Ambiente virtual local recomendado.
- `pytest`, instalado pelo extra de desenvolvimento ou por outro método controlado no ambiente local.
- Shell compatível com os scripts existentes quando for usar runners e scripts em `scripts/`.

Verifique a versão do Python antes de instalar:

```bash
python3 --version
```

Este guia não exige Docker, banco de dados, PostgreSQL, pgvector, embeddings, Ollama, RAG semântico ou provider externo para validar o checkout, rodar testes, compilar os módulos Python e usar a CLI operacional inicial.

## Clonar O Repositório

Use HTTPS público:

```bash
git clone https://github.com/pablovercosa/vercosa-ai-framework.git
cd vercosa-ai-framework
```

Ou use SSH, se sua chave já estiver autorizada no GitHub:

```bash
git clone git@github.com:pablovercosa/vercosa-ai-framework.git
cd vercosa-ai-framework
```

Não inclua credenciais, tokens ou segredos no comando de clonagem.

## Criar Ambiente Virtual

Crie um ambiente virtual dentro do checkout:

```bash
python3 -m venv .venv
```

Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

Confirme que `python` e `pip` apontam para o ambiente virtual:

```bash
python --version
python -m pip --version
```

## Instalar Em Modo Desenvolvimento

O projeto possui `pyproject.toml` com configuração de pacote local e extra de desenvolvimento. Para instalar o checkout em modo editável com `pytest`:

```bash
python -m pip install -e ".[dev]"
```

Essa instalação é local ao ambiente virtual ativo. Ela não significa que exista pacote publicado no PyPI e não deve ser confundida com instalação global para uso final.

Após essa instalação, os console scripts declarados no projeto, como `vaf` e `vercosa`, podem existir dentro do ambiente virtual. Use-os apenas quando o ambiente virtual estiver ativado e confirme com `--help` antes de depender deles:

```bash
vaf --help
vercosa --help
```

Forma conservadora, sem depender do console script:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --help
```

## Validar A Instalação Local

Execute os comandos abaixo a partir da raiz do projeto.

Verifique o status operacional dos diretórios de missão:

```bash
./scripts/vaf-status.sh
```

Rode a suíte de testes:

```bash
pytest
```

Valide a compilação dos módulos Python:

```bash
python3 -m compileall src
```

Abra a ajuda da CLI pela forma compatível com o checkout atual:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --help
```

Execute as validações operacionais básicas da CLI:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main status
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor
```

Se o pacote foi instalado em modo desenvolvimento no ambiente virtual ativo, os comandos abaixo também podem funcionar como atalhos locais:

```bash
vaf status
vaf missions
vaf validate
vaf doctor
```

Não trate esses atalhos como requisito global do sistema. Para documentação, automação reproduzível e diagnóstico de checkout, prefira a forma explícita com `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main` quando houver dúvida.

## Fluxo Mínimo Após Instalar

Use este fluxo antes de executar missões ou preparar batches:

```bash
cd vercosa-ai-framework
./scripts/vaf-status.sh
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions
pytest
python3 -m compileall src
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --help
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor
```

Não execute batch sem entender o [playbook de execução em batch](../operations/batch-execution-playbook.md). Os scripts operacionais dependem do estado local do projeto, dos diretórios em `missions/`, de permissões de execução e de convenções do repositório.

## Uso Básico Da CLI

A CLI operacional inicial é local, determinística e não destrutiva para os comandos abaixo. Ela não executa missões, não chama scripts shell, não executa Git, não acessa rede, não acessa banco e não consulta providers.

Ajuda:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --help
```

Status local de missões:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main status
```

Listagem local de missões por estado:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions --state queue
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions --state failed
```

O comando `missions` mostra contagens gerais e nomes de arquivos `.md` em `queue`, `running`, `done` e `failed`. Ele é uma validação opcional de leitura antes ou depois de preparar a fila; não executa, move, cria ou edita missões e não substitui `./scripts/vaf-status.sh`.

Validação estrutural local:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate
```

Diagnóstico local:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor
```

Versão operacional:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --version
```

## Problemas Comuns

`pytest` não encontrado:

```bash
python -m pip install -e ".[dev]"
pytest
```

Ambiente virtual não ativado:

```bash
source .venv/bin/activate
python -m pip --version
```

`python` aponta para versão errada:

```bash
python3 --version
python --version
```

Se necessário, recrie o ambiente virtual usando o `python3` compatível com o projeto.

Scripts sem permissão de execução:

```bash
ls -l scripts/vaf-status.sh scripts/vaf-run-next-safe.sh scripts/vaf-run-batch-safe.sh
```

Se a permissão estiver incorreta no seu checkout local, ajuste somente depois de entender a causa e revisar o diff. Não altere scripts como parte deste guia.

Limite externo de API ao usar runtime com provider:

```text
usage limit has been reached
quota exceeded
insufficient quota
billing hard limit
429
```

Esses sinais indicam condição operacional externa quando aparecem em logs de execução com provider. Pare, preserve os logs e revise o estado local antes de tentar novamente. O diagnóstico local do projeto não consulta quota, billing ou provider real.

Git com alterações pendentes:

```bash
git status --short
```

Não inicie batch ou execução sensível com Git sujo sem entender as alterações pendentes. Não use comandos destrutivos para limpar o worktree sem revisão.

## Próximos Passos

- Leia o [README principal](../../README.md) para entender estado, limites e arquitetura resumida.
- Use o [checklist de instalação limpa](clean-install-checklist.md) quando a meta for validar um ambiente novo antes de release alfa.
- Navegue pelo [índice de módulos](../architecture/module-index.md).
- Revise o [playbook de execução em batch](../operations/batch-execution-playbook.md) antes de executar missões em lote.
- Consulte os [exemplos operacionais](../examples/README.md).
- Use o [backlog estratégico de missões](../roadmap/mission-backlog.md) para entender próximos blocos, sem tratá-lo como fila executável automática.
