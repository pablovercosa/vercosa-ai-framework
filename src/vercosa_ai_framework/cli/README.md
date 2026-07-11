# Módulo cli

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0004](../../../specs/framework/0004-mission-runner.md)

## Objetivo

Fornecer uma CLI Python operacional inicial para consulta local, determinística e sem dependências externas sobre informações básicas do projeto.

## O Que Este Módulo Faz

- Expõe uma função `main` invocável em Python.
- Pode ser exposta como console script local `vaf` após instalação editável do pacote em ambiente virtual.
- Expõe o comando `status` para contar arquivos Markdown em `missions/queue`, `missions/running`, `missions/done` e `missions/failed`.
- Expõe o comando `missions` para listar arquivos Markdown por estado, com contagens gerais e filtro opcional por estado.
- Expõe o comando `validate` para validar a estrutura local mínima do projeto sem executar missões.
- Expõe o comando `doctor` para diagnóstico local amigável, determinístico e não destrutivo sobre prontidão operacional básica.
- Expõe o comando `batch-summary` para resumo pós-batch local, seguro e somente leitura.
- Expõe o comando `docs-links` para validar links relativos em documentos Markdown locais sem acessar rede.
- Expõe o comando `alpha-readiness` para diagnóstico local de prontidão documental e operacional mínima da futura alfa.
- Permite informar `--project-root` para testar ou consultar outro worktree local.
- Mostra versão operacional mínima com `--version` ou `version`.
- Mostra ajuda com `--help`.
- Trata diretórios de missão ausentes como contagem zero no `status` e como problema estrutural no `validate`.

## O Que Este Módulo Não Faz

- Não substitui `scripts/vaf-status.sh`.
- Não substitui `scripts/vaf-run-next-safe.sh` ou `scripts/vaf-run-batch-safe.sh`.
- Não substitui o compositor de missão `vercosa_ai_framework.missions.prompt_composer`, usado pelo runner antes de executar OpenCode.
- Não executa missões nesta fase.
- Não move arquivos entre `queue`, `running`, `done` e `failed`.
- Não chama scripts shell para calcular o status básico.
- Não executa `pytest`.
- Não executa `python3 -m compileall src`.
- Não executa `git`; `batch-summary` apenas lembra o operador de rodar `git status --short` manualmente.
- Não acessa rede, banco, LLM, provider externo, OpenCode ou MCPs para os comandos operacionais iniciais.
- Não adiciona dependências fora da biblioteca padrão do Python.
- Não valida URLs externas, imagens remotas ou existência perfeita de âncoras Markdown.
- Não implementa parser Markdown completo; `docs-links` cobre links inline e imagens básicos e ignora blocos de código cercados por crases ou tils e trechos simples de código inline.
- Não cria tag, não publica release, não publica pacote e não autoriza alfa automaticamente.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `__init__.py` | Exportações públicas da CLI operacional inicial. |
| `main.py` | Parser, função `main`, comandos `status`, `missions`, `validate`, `doctor`, `batch-summary`, `docs-links` e `alpha-readiness`, contagem local de missões, listagem local, validação estrutural, diagnóstico operacional local, resumo pós-batch auxiliar, validação local de links Markdown e diagnóstico de prontidão alfa. |
| `README.md` | Documentação do módulo. |
| `../../../pyproject.toml` | Declara o console script local `vaf` para instalação editável em ambiente virtual. |

## Principais Tipos, Classes E Funções

- `MissionDirectoryStatus`: resumo imutável das contagens de missão por diretório operacional.
- `MissionStateListing`: lista imutável de arquivos de missão para um estado operacional.
- `MissionListingResult`: resultado testável da listagem local de missões.
- `ValidationIssue`: problema estrutural encontrado pela validação local.
- `ValidationResult`: resultado testável da validação estrutural local.
- `DiagnosticIssue`: item de diagnóstico classificado como `error` ou `warning`.
- `DiagnosticResult`: resultado testável do diagnóstico local do `doctor`, com status geral `ok`, `warning` ou `error`.
- `BatchSummaryResult`: resultado testável do resumo pós-batch local.
- `MarkdownLinkIssue`: link Markdown relativo quebrado encontrado em documentação local.
- `MarkdownLinkValidationResult`: resultado testável da validação de links Markdown locais.
- `AlphaReadinessResult`: resultado testável do diagnóstico local de prontidão alfa.
- `build_parser`: cria o parser da CLI.
- `collect_mission_directory_status`: conta arquivos `.md` nos diretórios de missão.
- `list_missions`: lista arquivos `.md` em `queue`, `running`, `done` e `failed` com ordenação determinística.
- `print_status`: imprime o status básico local.
- `print_missions`: imprime a listagem local de missões e contagens por estado.
- `validate_project_structure`: valida a estrutura mínima do projeto sem efeitos colaterais.
- `diagnose_project`: combina validação estrutural e avisos operacionais locais para o `doctor`.
- `summarize_batch`: coleta contagens locais, último log e avisos pós-batch sem executar comandos externos.
- `collect_markdown_documentation_files`: localiza documentos Markdown públicos relevantes para validação local.
- `validate_markdown_links`: valida links relativos de Markdown local sem acessar rede.
- `print_markdown_link_validation`: imprime o resultado do comando `docs-links`.
- `check_alpha_readiness`: verifica arquivos mínimos, diretórios, contagens de missão e CI local para a futura alfa.
- `print_alpha_readiness`: imprime o resultado do comando `alpha-readiness`.
- `run`: executa a CLI e retorna código de saída.
- `main`: ponto de entrada invocável por Python e console script.

## Entradas E Saídas

Entradas:

- Argumentos de linha de comando.
- Caminho raiz do projeto informado por `--project-root` ou o diretório atual.
- Diretórios locais `missions/queue`, `missions/running`, `missions/done` e `missions/failed`, quando existirem.
- Diretório local `logs/`, quando existir, para identificar o último arquivo `.log` ou `.out` no comando `batch-summary`.
- Documentos Markdown relevantes: `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `docs/**/*.md` e `src/vercosa_ai_framework/**/README.md`.
- Arquivo `README.md` e diretório `src/vercosa_ai_framework` para o comando `validate`.
- Documentos auxiliares `docs/operations/post-batch-validation-checklist.md` e `docs/roadmap/mission-backlog.md` para avisos do comando `doctor`.

Saídas:

- Texto no terminal com versão, ajuda, status básico ou validação estrutural.
- Texto no terminal com listagem de missões por estado quando `missions` é usado.
- Texto no terminal com resumo pós-batch, último log encontrado, avisos e lembretes manuais quando `batch-summary` é usado.
- Texto no terminal com resultado da validação local de links Markdown quando `docs-links` é usado.
- Texto no terminal com classificação `PRONTO`, `PRONTO COM RESSALVAS` ou `NÃO PRONTO` quando `alpha-readiness` é usado.
- Código de saída `0` para sucesso.
- Código de saída `0` para `PRONTO COM RESSALVAS` no comando `alpha-readiness`, por decisão conservadora de uso diagnóstico em CI e ambientes com fila pendente.
- Código de saída `1` para estrutura inválida no comando `validate`, erro estrutural relevante no comando `doctor`, link relativo quebrado no comando `docs-links` ou classificação `NÃO PRONTO` no comando `alpha-readiness`.
- Código de saída `2` para erro controlado de argumentos.

## Dependências Internas

- `vercosa_ai_framework.__version__` para exibir a versão do pacote.

## Módulos Relacionados

- Acima: interface operacional local usada por pessoas e automações simples.
- Abaixo: [missions](../missions/README.md) como origem conceitual dos estados de missão.
- Paralelo: [runtime](../runtime/README.md), que permanece responsável por adapters de execução e não é chamado pelo status básico.

## Specs Correspondentes

- [Spec 0004: Mission Runner](../../../specs/framework/0004-mission-runner.md)
- [Spec 0001: Framework Foundation](../../../specs/framework/0001-framework-foundation.md)

## Docs Relacionadas

- [Uso do runner seguro](../../../docs/operations/safe-runner-usage.md)
- [Playbook de execução em batch](../../../docs/operations/batch-execution-playbook.md)
- [Contrato de execução de missões](../../../docs/operations/mission-execution-contract.md)
- [Formato compacto de missão](../../../docs/operations/compact-mission-format.md)
- [Mapa de arquitetura](../../../docs/alignment/architecture-map.md)

## Exemplo Mínimo

Comando de ajuda no checkout local: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --help`.

Comando de ajuda após instalação editável local em ambiente virtual: `vaf --help`.

Status do repositório atual no checkout local: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main status`.

Status de outro caminho local: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto status`.

Listagem de missões do repositório atual: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions`.

Listagem apenas da fila: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions --state queue`.

Listagem apenas de falhas: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions --state failed`.

Listagem de outro caminho local: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto missions`.

Validação estrutural do repositório atual no checkout local: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate`.

Validação estrutural de outro caminho local: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto validate`.

Diagnóstico local do repositório atual: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor`.

Diagnóstico local de outro caminho: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto doctor`.

Resumo pós-batch local: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main batch-summary`.

Resumo pós-batch de outro caminho: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto batch-summary`.

Validação local de links Markdown: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main docs-links`.

Validação local de links Markdown em outro caminho: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main docs-links --base-dir /caminho/do/projeto`.

Alternativa após instalação editável local em ambiente virtual: `vaf docs-links`.

Diagnóstico de prontidão alfa no checkout local: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main alpha-readiness`.

Diagnóstico de prontidão alfa em outro caminho local: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto alpha-readiness`.

Alternativa após instalação editável local em ambiente virtual: `vaf alpha-readiness`.

O comando `validate` verifica, nesta fase:

- se a raiz informada existe e é diretório;
- se `missions/` existe;
- se `missions/queue`, `missions/running`, `missions/done` e `missions/failed` existem;
- se `missions/running` está vazio;
- se `missions/failed` está vazio;
- se `src/vercosa_ai_framework` existe;
- se `README.md` existe.

`validate` é uma validação estrutural local. Ele não substitui `pytest`, não substitui `python3 -m compileall src`, não substitui `scripts/vaf-status.sh`, não executa missões e não altera arquivos.

## Comando `missions`

`missions` é uma leitura diagnóstica dos arquivos `.md` diretamente presentes em `missions/queue`, `missions/running`, `missions/done` e `missions/failed`.

O comando imprime:

- contagens gerais de `queue`, `running`, `done` e `failed`;
- lista ordenada de nomes de arquivos por estado;
- indicação de estado vazio com `- (vazio)`;
- indicação clara quando um diretório de estado está ausente.

Filtro opcional:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions --state queue
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions --state running
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions --state done
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions --state failed
```

Mesmo com filtro, as contagens gerais continuam sendo exibidas para manter contexto operacional. A filtragem afeta apenas a seção de listagem.

`missions` não lê o conteúdo dos arquivos Markdown, não interpreta o backlog estratégico, não move missões, não cria diretórios, não executa missões, não chama scripts shell, não executa Git, não acessa rede, não acessa banco e não consulta providers.

Diferença em relação a `./scripts/vaf-status.sh`: o script continua sendo o resumo operacional dos scripts e diretórios de missão; `missions` é uma listagem Python local e testável dos nomes de arquivos por estado. Eles se complementam e nenhum substitui o runner seguro, o batch, `pytest`, `compileall` ou revisão humana.

## Diferença Entre `status`, `missions`, `validate`, `doctor`, `docs-links` E `alpha-readiness`

`status` é uma leitura simples de contagens. Ele conta arquivos `.md` diretamente em `missions/queue`, `missions/running`, `missions/done` e `missions/failed`. Diretórios ausentes contam como zero nesse comando.

`missions` lista os nomes dos arquivos `.md` por estado, em ordem determinística, e também mostra as contagens gerais. Diretórios ausentes são reportados na saída, mas não geram traceback ou criação automática de diretório.

`validate` é uma validação estrutural local. Ele verifica raiz, `README.md`, `src/vercosa_ai_framework`, `missions/`, subdiretórios obrigatórios e se `running` e `failed` estão vazios. Problemas estruturais retornam código `1`.

`doctor` é um diagnóstico local mais amigável construído sobre a mesma validação estrutural. Ele mostra `status_geral` como `ok`, `warning` ou `error`, reporta contagens, indica se `running` e `failed` estão vazios e sugere ação operacional segura. Erros estruturais retornam código `1`; warnings, como documentos auxiliares ausentes, são reportados sem retornar erro.

`docs-links` valida links relativos em Markdown local. Ele foca coerência de documentação e não avalia prontidão de release.

`alpha-readiness` consolida verificações locais mínimas para a futura alfa: arquivos documentais obrigatórios, diretórios principais, contagens de `queue`, `running` e `failed`, workflow de CI, política de release, checklist pré-tag, release notes alfa, `CHANGELOG.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md` e `pyproject.toml`. Ele classifica o resultado como `PRONTO`, `PRONTO COM RESSALVAS` ou `NÃO PRONTO`.

`doctor` ajuda a entender se o projeto parece pronto para iniciar uma missão, iniciar um batch, investigar falhas ou revisar estado pós-batch. Ele não executa missões e não altera o fluxo `missions/queue`, `missions/running`, `missions/done` e `missions/failed`.

Use os comandos em conjunto conforme a necessidade operacional:

- `status` para leitura rápida de contagens locais.
- `missions` para ver quais arquivos de missão estão em cada estado, sem executar ou mover nada.
- `validate` para validação estrutural mínima e código de saída formal sobre essa estrutura.
- `doctor` para diagnóstico local mais amigável antes de preparar batch, antes de executar batch, depois de batch ou durante investigação.
- `docs-links` para validar links relativos em Markdown local.
- `alpha-readiness` para diagnóstico auxiliar antes de revisão de release alfa, sem autorizar release.
- `./scripts/vaf-status.sh` quando a necessidade for observar o estado operacional dos scripts e missões.
- `pytest` quando a necessidade for validar testes.
- `python3 -m compileall src` quando a necessidade for validar compilação dos módulos Python.

Exemplos:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto doctor
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions --state queue
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main alpha-readiness
```

O comando `doctor` verifica, nesta fase:

- se a raiz informada existe e é diretório;
- se `README.md` existe;
- se `src/vercosa_ai_framework` existe;
- se `missions/` existe;
- se `missions/queue`, `missions/running`, `missions/done` e `missions/failed` existem;
- contagem de arquivos `.md` em `queue`, `running`, `done` e `failed`;
- se `missions/running` está vazio;
- se `missions/failed` está vazio;
- se `docs/operations/post-batch-validation-checklist.md` existe, reportando warning quando ausente;
- se `docs/roadmap/mission-backlog.md` existe, reportando warning quando ausente.

Limites do `doctor` nesta fase:

- Não substitui `pytest`.
- Não substitui `python3 -m compileall src`.
- Não substitui `scripts/vaf-status.sh`.
- Não substitui revisão de logs, revisão de commits ou checklist pós-batch.
- Não chama scripts shell.
- Não executa missões.
- Não executa `git`.
- Não acessa rede.
- Não acessa banco.
- Não chama LLM, provider externo, OpenCode ou MCPs.
- Não consulta quota, billing, rate limit real ou runtime externo.
- Não altera arquivos.

Limites do `missions` nesta fase:

- Não substitui `scripts/vaf-status.sh`.
- Não substitui `validate` ou `doctor`.
- Não executa missões.
- Não move arquivos.
- Não cria diretórios ausentes.
- Não lê o conteúdo das missões.
- Não executa `git`, scripts shell, `pytest` ou `compileall`.
- Não acessa rede, banco, LLM, provider externo, OpenCode ou MCPs.

O uso operacional de `doctor` em batch está descrito no [playbook de execução em batch](../../../docs/operations/batch-execution-playbook.md) e no [checklist de validação pós-batch](../../../docs/operations/post-batch-validation-checklist.md).

## Comando `batch-summary`

`batch-summary` é um diagnóstico auxiliar para revisão pós-batch. Ele lê diretórios locais do projeto e imprime:

- contagens de `missions/queue`, `missions/running`, `missions/done` e `missions/failed`;
- último arquivo `.log` ou `.out` encontrado em `logs/`, escolhido de forma determinística por modificação e nome;
- aviso de que o worker não foi verificado pela CLI;
- aviso de que Git não foi verificado pela CLI;
- atenção quando há missão em `running`, missão em `failed` ou fila ainda pendente;
- lembretes para rodar `pytest`, `python3 -m compileall src`, `git status --short` e revisar push manualmente.

Forma real de execução no checkout local:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main batch-summary
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto batch-summary
```

`batch-summary` não executa missões, não move arquivos, não chama scripts shell, não executa `pytest`, não executa `python3 -m compileall src`, não executa Git, não acessa rede, não acessa banco, não chama providers e não lê o conteúdo completo dos logs.

Diferença prática:

- `batch-summary` resume contagens, último log e próximos passos manuais em saída Python testável.
- `./scripts/vaf-status.sh` continua sendo o status operacional dos scripts, incluindo verificação shell de Git, branch, worker e últimos logs.
- O checklist pós-batch continua sendo a validação operacional obrigatória antes de push, novo batch ou retomada após falha.

`batch-summary` pode indicar estado operacional aparentemente limpo quando `queue=0`, `running=0` e `failed=0`, mas isso não significa validação completa. Testes, `compileall`, revisão de logs, revisão de commits, checklist pós-batch e decisão humana continuam obrigatórios quando aplicáveis.

## Comando `alpha-readiness`

`alpha-readiness` é um diagnóstico auxiliar local, seguro e somente leitura para verificar prontidão documental e operacional mínima da futura alfa pública. Ele não executa release, não cria tag, não publica pacote e não substitui checklist pré-tag ou revisão humana.

Forma real de execução no checkout local:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main alpha-readiness
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto alpha-readiness
```

Após instalação editável local em ambiente virtual, o console script também pode ser usado:

```bash
vaf alpha-readiness
```

Classificações:

- `PRONTO`: arquivos mínimos, diretórios obrigatórios, CI local e contagens bloqueantes estão em estado saudável, sem ressalvas detectadas pela CLI.
- `PRONTO COM RESSALVAS`: não há bloqueio, mas há atenção como `queue > 0`, CI ausente ou release notes ainda preliminares.
- `NÃO PRONTO`: há bloqueio como arquivo obrigatório ausente, diretório obrigatório ausente, `running > 0`, `failed > 0`, ausência de `CHANGELOG.md`, `SECURITY.md`, política de release, `pyproject.toml` ou outra pendência obrigatória.

Código de saída:

- `0` para `PRONTO`.
- `0` para `PRONTO COM RESSALVAS`, para permitir uso diagnóstico em CI e ambientes de desenvolvimento sem transformar ressalvas em falha obrigatória.
- `1` para `NÃO PRONTO`.

Arquivos mínimos verificados incluem `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `LICENSE`, `pyproject.toml`, documentos de release, checklist de instalação limpa, política de uso e índice de módulos. Diretórios mínimos incluem `src/`, `tests/`, `docs/` e `missions/queue`, `missions/running`, `missions/done`, `missions/failed`.

Diferenças práticas:

- `alpha-readiness` verifica prontidão documental e operacional mínima para futura alfa.
- `pre-release-checklist.md` continua sendo checklist humano pré-tag.
- `docs-links` valida links relativos em Markdown local.
- `validate` verifica estrutura local mínima do projeto.
- `doctor` diagnostica prontidão operacional básica para missão ou batch.

Limites intencionais:

- Não executa `pytest`.
- Não executa `python3 -m compileall src`.
- Não executa Git, `git tag`, `git push`, `git push --tags`, `gh release` ou `twine`.
- Não executa scripts shell, batch ou missões.
- Não acessa rede, banco, providers, OpenCode, MCPs ou secrets.
- Não modifica arquivos.
- Não substitui revisão humana, checklist pré-tag, validação limpa, `pytest` ou `compileall`.

## Comando `docs-links`

`docs-links` valida links relativos em documentos Markdown locais para reduzir risco de documentação pública com links quebrados antes de uma futura alfa.

Forma real de execução no checkout local:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main docs-links
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main docs-links --base-dir /caminho/do/projeto
```

Após instalação editável local em ambiente virtual, o console script também pode ser usado:

```bash
vaf docs-links
```

Escopo validado:

- `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `SECURITY.md` e `CODE_OF_CONDUCT.md` na raiz informada.
- `docs/**/*.md`.
- `src/vercosa_ai_framework/**/README.md`.
- Links inline básicos no formato `[texto](destino)`.
- Imagens básicas no formato `![alt](destino)`.
- Links relativos com `./`, `../`, subdiretórios e fragmentos como `arquivo.md#secao`.
- Espaços codificados de forma básica, como `%20`.

Limites intencionais:

- Não acessa `https://`, `http://`, `mailto:` ou `tel:`.
- Não valida links externos, imagens remotas ou disponibilidade HTTP.
- Não valida existência de âncoras; para `arquivo.md#secao`, valida apenas se `arquivo.md` existe.
- Não implementa parser Markdown completo.
- Ignora blocos de código cercados por cercas de crases ou tils e trechos simples de código inline quando possível.
- Ignora diretórios como `.git`, `.venv`, `__pycache__`, `logs`, `runtime`, `dist`, `build` e `.pytest_cache`.
- Não valida documentação operacional arquivada em `missions/done`.

Diferença prática em relação a `validate` e `doctor`:

- `docs-links` verifica coerência local de links relativos em Markdown.
- `validate` verifica estrutura mínima do projeto e diretórios de missão.
- `doctor` agrega diagnóstico operacional amigável baseado na estrutura local.
- Nenhum desses comandos executa missões, scripts shell, Git, `pytest`, `compileall`, rede, banco ou providers.

Uso por Python: `from vercosa_ai_framework.cli import main`.

Uso por console script local após `python -m pip install -e ".[dev]"` em ambiente virtual: `vaf status`.

## Status Atual

Status: `MVP`.

A CLI inicial é uma camada de conveniência para leitura, listagem, diagnóstico básico, resumo pós-batch e validação estrutural local. Ela não altera o fluxo operacional atual baseado nos scripts shell.

## Próximos Passos

- Avaliar comandos futuros como `run-next`, `run-batch`, `audit`, `policy` e `context` em missões próprias.
- Manter comandos futuros atrás das mesmas restrições de governança, sem substituir scripts seguros antes de decisão explícita.
- Integrar validações futuras como Git limpo, branch `main`, `pytest`, `compileall`, logs recentes, audit log, políticas, contexto e providers somente quando houver contratos e testes determinísticos aprovados.
