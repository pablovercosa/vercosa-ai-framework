# Módulo cli

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0004](../../../specs/framework/0004-mission-runner.md)

## Objetivo

Fornecer uma CLI Python operacional inicial para consulta local, determinística e sem dependências externas sobre informações básicas do projeto.

## O Que Este Módulo Faz

- Expõe uma função `main` invocável em Python.
- Expõe o comando `status` para contar arquivos Markdown em `missions/queue`, `missions/running`, `missions/done` e `missions/failed`.
- Expõe o comando `validate` para validar a estrutura local mínima do projeto sem executar missões.
- Expõe o comando `doctor` para diagnóstico local amigável, determinístico e não destrutivo sobre prontidão operacional básica.
- Permite informar `--project-root` para testar ou consultar outro worktree local.
- Mostra versão operacional mínima com `--version` ou `version`.
- Mostra ajuda com `--help`.
- Trata diretórios de missão ausentes como contagem zero no `status` e como problema estrutural no `validate`.

## O Que Este Módulo Não Faz

- Não substitui `scripts/vaf-status.sh`.
- Não substitui `scripts/vaf-run-next-safe.sh` ou `scripts/vaf-run-batch-safe.sh`.
- Não executa missões nesta fase.
- Não move arquivos entre `queue`, `running`, `done` e `failed`.
- Não chama scripts shell para calcular o status básico.
- Não executa `pytest`.
- Não executa `python3 -m compileall src`.
- Não executa `git`.
- Não acessa rede, banco, LLM, provider externo, OpenCode ou MCPs para os comandos operacionais iniciais.
- Não adiciona dependências fora da biblioteca padrão do Python.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `__init__.py` | Exportações públicas da CLI operacional inicial. |
| `main.py` | Parser, função `main`, comandos `status`, `validate` e `doctor`, contagem local de missões, validação estrutural e diagnóstico operacional local. |
| `README.md` | Documentação do módulo. |

## Principais Tipos, Classes E Funções

- `MissionDirectoryStatus`: resumo imutável das contagens de missão por diretório operacional.
- `ValidationIssue`: problema estrutural encontrado pela validação local.
- `ValidationResult`: resultado testável da validação estrutural local.
- `DiagnosticIssue`: item de diagnóstico classificado como `error` ou `warning`.
- `DiagnosticResult`: resultado testável do diagnóstico local do `doctor`, com status geral `ok`, `warning` ou `error`.
- `build_parser`: cria o parser da CLI.
- `collect_mission_directory_status`: conta arquivos `.md` nos diretórios de missão.
- `print_status`: imprime o status básico local.
- `validate_project_structure`: valida a estrutura mínima do projeto sem efeitos colaterais.
- `diagnose_project`: combina validação estrutural e avisos operacionais locais para o `doctor`.
- `run`: executa a CLI e retorna código de saída.
- `main`: ponto de entrada invocável por Python e console script.

## Entradas E Saídas

Entradas:

- Argumentos de linha de comando.
- Caminho raiz do projeto informado por `--project-root` ou o diretório atual.
- Diretórios locais `missions/queue`, `missions/running`, `missions/done` e `missions/failed`, quando existirem.
- Arquivo `README.md` e diretório `src/vercosa_ai_framework` para o comando `validate`.
- Documentos auxiliares `docs/operations/post-batch-validation-checklist.md` e `docs/roadmap/mission-backlog.md` para avisos do comando `doctor`.

Saídas:

- Texto no terminal com versão, ajuda, status básico ou validação estrutural.
- Código de saída `0` para sucesso.
- Código de saída `1` para estrutura inválida no comando `validate` ou erro estrutural relevante no comando `doctor`.
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
- [Mapa de arquitetura](../../../docs/alignment/architecture-map.md)

## Exemplo Mínimo

Comando de ajuda no checkout local: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --help`.

Status do repositório atual no checkout local: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main status`.

Status de outro caminho local: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto status`.

Validação estrutural do repositório atual no checkout local: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate`.

Validação estrutural de outro caminho local: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto validate`.

Diagnóstico local do repositório atual: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor`.

Diagnóstico local de outro caminho: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto doctor`.

O comando `validate` verifica, nesta fase:

- se a raiz informada existe e é diretório;
- se `missions/` existe;
- se `missions/queue`, `missions/running`, `missions/done` e `missions/failed` existem;
- se `missions/running` está vazio;
- se `missions/failed` está vazio;
- se `src/vercosa_ai_framework` existe;
- se `README.md` existe.

`validate` é uma validação estrutural local. Ele não substitui `pytest`, não substitui `python3 -m compileall src`, não substitui `scripts/vaf-status.sh`, não executa missões e não altera arquivos.

## Diferença Entre `status`, `validate` E `doctor`

`status` é uma leitura simples de contagens. Ele conta arquivos `.md` diretamente em `missions/queue`, `missions/running`, `missions/done` e `missions/failed`. Diretórios ausentes contam como zero nesse comando.

`validate` é uma validação estrutural local. Ele verifica raiz, `README.md`, `src/vercosa_ai_framework`, `missions/`, subdiretórios obrigatórios e se `running` e `failed` estão vazios. Problemas estruturais retornam código `1`.

`doctor` é um diagnóstico local mais amigável construído sobre a mesma validação estrutural. Ele mostra `status_geral` como `ok`, `warning` ou `error`, reporta contagens, indica se `running` e `failed` estão vazios e sugere ação operacional segura. Erros estruturais retornam código `1`; warnings, como documentos auxiliares ausentes, são reportados sem retornar erro.

`doctor` ajuda a entender se o projeto parece pronto para iniciar uma missão, iniciar um batch, investigar falhas ou revisar estado pós-batch. Ele não executa missões e não altera o fluxo `missions/queue`, `missions/running`, `missions/done` e `missions/failed`.

Exemplos:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto doctor
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

`doctor` não substitui `pytest`, não substitui `python3 -m compileall src`, não substitui `scripts/vaf-status.sh`, não chama scripts shell, não executa `git`, não acessa rede, não acessa banco, não chama LLM, não chama provider externo e não chama OpenCode ou MCPs.

Uso por Python: `from vercosa_ai_framework.cli import main`.

## Status Atual

Status: `MVP`.

A CLI inicial é uma camada de conveniência para leitura, diagnóstico básico e validação estrutural local. Ela não altera o fluxo operacional atual baseado nos scripts shell.

## Próximos Passos

- Avaliar comandos futuros como `run-next`, `run-batch`, `audit`, `policy` e `context` em missões próprias.
- Manter comandos futuros atrás das mesmas restrições de governança, sem substituir scripts seguros antes de decisão explícita.
- Integrar validações futuras como Git limpo, branch `main`, `pytest`, `compileall`, logs recentes, audit log, políticas, contexto e providers somente quando houver contratos e testes determinísticos aprovados.
