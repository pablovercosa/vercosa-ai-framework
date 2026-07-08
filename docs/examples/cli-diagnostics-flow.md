# Fluxo De Diagnóstico Da CLI Operacional

Links principais: [Exemplos](README.md) | [Módulo cli](../../src/vercosa_ai_framework/cli/README.md) | [Uso do runner seguro](../operations/safe-runner-usage.md) | [Checklist pós-batch](../operations/post-batch-validation-checklist.md)

## Objetivo

Explicar como usar a CLI operacional inicial para leitura de status, validação estrutural local e diagnóstico básico, sem confundir a CLI com os scripts shell seguros.

Status deste exemplo: exemplo operacional executável para comandos locais de leitura e validação estrutural.

## Estado Atual

Implementado:

- `status`: conta arquivos Markdown em `missions/queue`, `missions/running`, `missions/done` e `missions/failed`.
- `validate`: valida estrutura mínima local do projeto.
- `doctor`: combina validação estrutural e diagnóstico operacional básico.
- `--project-root`: permite consultar outro worktree local.
- `--version` e `version`: mostram versão operacional mínima.

Fora do escopo atual:

- Executar missões.
- Mover arquivos entre diretórios de missão.
- Chamar scripts shell.
- Executar `pytest` ou `python3 -m compileall src`.
- Executar `git`.
- Chamar rede, banco, providers, LLMs, OpenCode ou MCPs.

## Comando `status`

Use `status` para leitura simples das contagens de missão:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main status
```

O comando lê diretamente:

- `missions/queue`
- `missions/running`
- `missions/done`
- `missions/failed`

Diretórios ausentes contam como zero no `status`, mas isso não significa que a estrutura esteja válida para execução.

## Comando `validate`

Use `validate` para validação estrutural local:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate
```

No estado atual, `validate` verifica:

- raiz do projeto;
- `README.md`;
- `src/vercosa_ai_framework`;
- `missions/`;
- `missions/queue`;
- `missions/running`;
- `missions/done`;
- `missions/failed`;
- se `missions/running` está vazio;
- se `missions/failed` está vazio.

Se houver problema estrutural, o comando retorna código `1`.

## Comando `doctor`

Use `doctor` para diagnóstico local mais amigável:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor
```

O `doctor` ajuda a decidir se o projeto parece pronto para iniciar missão, iniciar batch, investigar falha ou revisar estado pós-batch. Ele não executa a decisão operacional por você.

No estado atual, o diagnóstico pode reportar:

- status geral `ok`, `warning` ou `error`;
- contagens de missão;
- se `running` está vazio;
- se `failed` está vazio;
- presença do checklist pós-batch;
- presença do backlog estratégico de missões.

## Outro Worktree Local

Para consultar outro checkout local:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto status
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto validate
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto doctor
```

O caminho deve ser local. Este exemplo não envolve rede, banco ou provider externo.

## Diferença Entre CLI E Scripts Shell

CLI operacional inicial:

- Faz leitura e validação estrutural local.
- Não executa missões.
- Não chama scripts shell.
- Não executa testes ou `compileall`.
- Não faz commit nem push.

Scripts shell seguros:

- `scripts/vaf-status.sh` mostra status operacional usado pelo fluxo shell.
- `scripts/vaf-run-next-safe.sh` executa uma missão com validações.
- `scripts/vaf-run-batch-safe.sh` executa múltiplas missões em sequência controlada.
- Os runners shell executam validações como `pytest` e `python3 -m compileall src`.

## Uso Em Validação Pós-Batch

Depois de batch, a CLI pode complementar o checklist:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor
```

Esses comandos não substituem:

```bash
./scripts/vaf-status.sh
pytest
python3 -m compileall src
```

## Limites Do Exemplo

- A CLI operacional é MVP.
- Este exemplo não promete comandos futuros como `run-next`, `run-batch`, `audit`, `policy` ou `context`.
- Este exemplo não altera scripts.
- Este exemplo não substitui o runner seguro.
- Este exemplo não substitui revisão humana, Specs, testes ou playbooks.
