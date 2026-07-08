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
- `vaf validate`: valida a estrutura local mínima do projeto sem executar missões.

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

Exemplo via módulo Python no checkout local: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto status`.

## Validação Estrutural Local

`vaf validate` verifica condições locais básicas para iniciar uma missão, iniciar um batch ou revisar um pós-batch. O comando é determinístico, usa apenas biblioteca padrão do Python e não altera arquivos.

Validação no diretório atual: `vaf validate`.

Validação em outro diretório local: `vaf --project-root /caminho/do/projeto validate`.

Exemplo via módulo Python no checkout local: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --project-root /caminho/do/projeto validate`.

Nesta fase, o comando verifica:

- raiz do projeto existente e em formato de diretório;
- existência de `missions/`;
- existência de `missions/queue`, `missions/running`, `missions/done` e `missions/failed`;
- ausência de missão `.md` presa em `missions/running`;
- ausência de missão `.md` em `missions/failed`;
- existência de `src/vercosa_ai_framework`;
- existência de `README.md`.

Se a estrutura estiver saudável, o comando retorna código `0` e imprime `resultado: saudavel`. Se encontrar problema, retorna código `1` e imprime mensagens `problema[...]` em português do Brasil.

`vaf validate` não substitui `pytest`, não substitui `python3 -m compileall src` e não substitui `scripts/vaf-status.sh`. Ele também não executa missões, não move arquivos entre diretórios de missão, não executa `git`, não chama scripts shell, não acessa rede, não acessa banco, não chama LLM e não chama provider externo.

## Relação Com Scripts Shell

Os scripts shell continuam sendo a base operacional atual para execução segura de missões:

- `scripts/vaf-status.sh`
- `scripts/vaf-run-next-safe.sh`
- `scripts/vaf-run-batch-safe.sh`
- `scripts/vaf-worker.sh`
- `scripts/vaf-run-one-mission.sh`

A CLI Python inicial não chama esses scripts para calcular status ou validação estrutural. Ela também não substitui os fluxos de preflight, worker, testes, `compileall`, auto-commit ou push opt-in documentados nos guias operacionais.

## Limites Atuais

- Não há comando `run-next` na CLI Python desta fase.
- Não há comando `run-batch` na CLI Python desta fase.
- Não há comando de validação de critérios de missão na CLI Python desta fase; `validate` valida apenas estrutura local básica.
- Não há integração com Audit/Event Log persistente.
- Não há descoberta de runtime, modelo, provider, banco ou rede.
- `--queue-dir` está reservado para compatibilidade futura e não muda o fluxo operacional nesta fase.

## Próximos Passos Possíveis

Comandos como `run-next`, `run-batch`, `audit`, `policy`, `context` e `doctor` podem ser avaliados em missões futuras.

Validações futuras como Git limpo, branch `main`, `pytest`, `compileall`, logs recentes, audit log, políticas, contexto e providers ainda não existem no `validate` e não devem ser documentadas como implementadas antes de Spec, testes e decisão operacional explícita.

## Códigos De Saída

- `0`: sucesso.
- `1`: estrutura inválida em `validate`.
- `2`: erro controlado de argumentos.

## Segurança E Determinismo

- A CLI usa biblioteca padrão do Python para os comandos iniciais.
- A CLI não usa `sudo`.
- A CLI não acessa rede.
- A CLI não acessa banco.
- A CLI não chama OpenCode.
- A CLI não chama LLM ou provider externo.
- A CLI não altera arquivos ao executar `status`, `validate`, `version`, `diagnose` ou `--help`.
