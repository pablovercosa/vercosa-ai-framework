# CLI

Links principais: [README principal](../README.md) | [Módulo cli](../src/vercosa_ai_framework/cli/README.md) | [Uso do runner seguro](operations/safe-runner-usage.md) | [Índice de módulos](architecture/module-index.md)

## Objetivo

Documentar a CLI Python operacional inicial do Vercosa AI Framework.

A CLI desta fase é uma camada de conveniência para leitura e diagnóstico básico local. Ela não substitui os scripts shell existentes, não executa missões, não move arquivos entre diretórios de missão e não acessa rede, banco, LLM, provider externo, OpenCode ou MCPs.

## Comandos Implementados

- `vaf --help`: mostra ajuda.
- `vaf --version`: mostra a versão operacional mínima.
- `vaf version`: mostra a versão operacional mínima.
- `vaf diagnose`: mostra diagnóstico local básico de Python, sistema e arquitetura.
- `vaf status`: conta missões locais em `missions/queue`, `missions/running`, `missions/done` e `missions/failed`.

## Status Básico

`vaf status` calcula o estado localmente a partir dos diretórios de missão do projeto.

O comando conta apenas arquivos `.md` diretamente em cada diretório operacional:

- `missions/queue`
- `missions/running`
- `missions/done`
- `missions/failed`

Diretórios ausentes contam como zero. Esse comportamento permite testes com diretórios temporários e consultas em worktrees incompletos sem falha inesperada.

## Caminho Raiz Do Projeto

Use `--project-root` para informar explicitamente o caminho raiz consultado.

Exemplo de status no diretório atual: `vaf status`.

Exemplo de status em outro diretório local: `vaf --project-root /caminho/do/projeto status`.

Exemplo via módulo Python: `python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto status`.

## Relação Com Scripts Shell

Os scripts shell continuam sendo a base operacional atual para execução segura de missões:

- `scripts/vaf-status.sh`
- `scripts/vaf-run-next-safe.sh`
- `scripts/vaf-run-batch-safe.sh`
- `scripts/vaf-worker.sh`
- `scripts/vaf-run-one-mission.sh`

A CLI Python inicial não chama esses scripts para calcular status. Ela também não substitui os fluxos de preflight, worker, testes, `compileall`, auto-commit ou push opt-in documentados nos guias operacionais.

## Limites Atuais

- Não há comando `run-next` na CLI Python desta fase.
- Não há comando `run-batch` na CLI Python desta fase.
- Não há comando de validação de missão na CLI Python desta fase.
- Não há integração com Audit/Event Log persistente.
- Não há descoberta de runtime, modelo, provider, banco ou rede.
- `--queue-dir` está reservado para compatibilidade futura e não muda o fluxo operacional nesta fase.

## Próximos Passos Possíveis

Comandos como `run-next`, `run-batch`, `validate`, `audit`, `policy`, `context` e `doctor` podem ser avaliados em missões futuras.

Esses comandos ainda não existem nesta CLI inicial e não devem ser documentados como implementados antes de Spec, testes e decisão operacional explícita.

## Códigos De Saída

- `0`: sucesso.
- `2`: erro controlado de argumentos.

## Segurança E Determinismo

- A CLI usa biblioteca padrão do Python para os comandos iniciais.
- A CLI não usa `sudo`.
- A CLI não acessa rede.
- A CLI não acessa banco.
- A CLI não chama OpenCode.
- A CLI não chama LLM ou provider externo.
- A CLI não altera arquivos ao executar `status`, `version`, `diagnose` ou `--help`.
