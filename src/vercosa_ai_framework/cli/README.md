# Módulo cli

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0004](../../../specs/framework/0004-mission-runner.md)

## Objetivo

Fornecer uma CLI Python operacional inicial para consulta local, determinística e sem dependências externas sobre informações básicas do projeto.

## O Que Este Módulo Faz

- Expõe uma função `main` invocável em Python.
- Expõe o comando `status` para contar arquivos Markdown em `missions/queue`, `missions/running`, `missions/done` e `missions/failed`.
- Permite informar `--project-root` para testar ou consultar outro worktree local.
- Mostra versão operacional mínima com `--version` ou `version`.
- Mostra ajuda com `--help`.
- Trata diretórios de missão ausentes como contagem zero.

## O Que Este Módulo Não Faz

- Não substitui `scripts/vaf-status.sh`.
- Não substitui `scripts/vaf-run-next-safe.sh` ou `scripts/vaf-run-batch-safe.sh`.
- Não executa missões nesta fase.
- Não move arquivos entre `queue`, `running`, `done` e `failed`.
- Não chama scripts shell para calcular o status básico.
- Não acessa rede, banco, LLM, provider externo, OpenCode ou MCPs para os comandos operacionais iniciais.
- Não adiciona dependências fora da biblioteca padrão do Python.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `__init__.py` | Exportações públicas da CLI operacional inicial. |
| `main.py` | Parser, função `main`, comando `status` e contagem local de missões. |
| `README.md` | Documentação do módulo. |

## Principais Tipos, Classes E Funções

- `MissionDirectoryStatus`: resumo imutável das contagens de missão por diretório operacional.
- `build_parser`: cria o parser da CLI.
- `collect_mission_directory_status`: conta arquivos `.md` nos diretórios de missão.
- `print_status`: imprime o status básico local.
- `run`: executa a CLI e retorna código de saída.
- `main`: ponto de entrada invocável por Python e console script.

## Entradas E Saídas

Entradas:

- Argumentos de linha de comando.
- Caminho raiz do projeto informado por `--project-root` ou o diretório atual.
- Diretórios locais `missions/queue`, `missions/running`, `missions/done` e `missions/failed`, quando existirem.

Saídas:

- Texto no terminal com versão, ajuda ou status básico.
- Código de saída `0` para sucesso.
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

Comando de ajuda: `python3 -m vercosa_ai_framework.cli.main --help`.

Status do repositório atual: `python3 -m vercosa_ai_framework.cli.main status`.

Status de outro caminho local: `python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto status`.

Uso por Python: `from vercosa_ai_framework.cli import main`.

## Status Atual

Status: `MVP`.

A CLI inicial é uma camada de conveniência para leitura e diagnóstico básico. Ela não altera o fluxo operacional atual baseado nos scripts shell.

## Próximos Passos

- Avaliar comandos futuros como `run-next`, `run-batch`, `validate`, `audit`, `policy`, `context` e `doctor` em missões próprias.
- Manter comandos futuros atrás das mesmas restrições de governança, sem substituir scripts seguros antes de decisão explícita.
- Integrar diagnósticos mais ricos somente quando houver contratos e testes determinísticos aprovados.
