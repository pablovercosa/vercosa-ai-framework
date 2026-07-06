# Uso Do Runner Seguro

## Objetivo

Documentar o uso operacional de `scripts/vaf-run-next-safe.sh` para executar uma missão local de baixo risco com validações automáticas antes de considerar a entrega concluída.

## Propósito

O runner seguro executa a próxima missão da fila usando o worker local com limites conservadores. Ele existe para reduzir risco operacional em execuções simples ao combinar preflight, execução de uma missão, status do worker, testes, `compileall`, auto-commit e push opcional em um único fluxo abortável.

Ele não substitui revisão humana em mudanças sensíveis, alterações de arquitetura, segurança, infraestrutura, dados, dependências ou qualquer entrega que exija aprovação explícita por política.

## Uso Básico

```bash
./scripts/vaf-run-next-safe.sh
```

Por padrão, o script executa uma missão, porque define `VAF_MAX_CYCLES=1` quando a variável não foi informada.

## Uso Com Push Automático

```bash
VAF_AUTO_PUSH=1 ./scripts/vaf-run-next-safe.sh
```

O push automático é opt-in. Sem `VAF_AUTO_PUSH=1`, o runner não executa `git push`.

Quando solicitado, o push automático só prossegue depois das validações locais e das verificações de segurança do próprio script.

## Uso Com Mensagem Customizada

```bash
VAF_COMMIT_MESSAGE="implementação: exemplo" ./scripts/vaf-run-next-safe.sh
```

Quando `VAF_COMMIT_MESSAGE` existe e não está vazia, a mensagem é repassada ao worker para o commit automático. A mensagem deve estar em português do Brasil, conforme o padrão do projeto.

## Pré-Condições

- Git limpo antes da execução.
- Worker parado antes da execução.
- Uma missão disponível em `missions/queue`.
- Branch `main` para uso com push automático.
- Testes devem passar para a missão ser considerada validada.

## Fluxo Seguro

O script executa o seguinte fluxo local:

1. Cria diretórios operacionais de missões e logs quando necessário.
2. Aborta se o Git tiver alterações pendentes.
3. Aborta se houver worker em execução.
4. Aborta se `missions/running` não estiver vazio antes de iniciar.
5. Aborta se houver missão em `missions/failed`.
6. Define defaults seguros para executar uma missão com auto-aprovação e auto-commit local.
7. Executa `./scripts/vaf-worker.sh` em foreground.
8. Mostra o status via `./scripts/vaf-status.sh`.
9. Aborta se o worker ainda estiver em execução após o ciclo.
10. Aborta se restar missão em `missions/running` ou `missions/failed`.
11. Executa `pytest`.
12. Executa `python3 -m compileall src`.
13. Confirma que o Git ficou limpo quando `VAF_AUTO_COMMIT=1`.
14. Executa push somente quando `VAF_AUTO_PUSH=1`.
15. Exibe um resumo com commit, fila, testes, `compileall` e push.

## Comportamento Em Caso De Erro

O runner usa `set -euo pipefail` e aborta em caso de erro. Falhas de preflight, worker, estado da fila, `pytest`, `compileall`, auto-commit ou push interrompem o fluxo.

Esse comportamento preserva evidências locais para revisão, em vez de seguir com entrega parcial.

## Auto-Commit

O runner define `VAF_AUTO_COMMIT=1` por padrão, salvo quando a variável já foi definida pelo usuário. O commit automático é responsabilidade do worker acionado pelo runner e deve respeitar `VAF_COMMIT_MESSAGE` quando informada.

Se `VAF_AUTO_COMMIT=1`, o runner exige Git limpo ao final. Se restarem alterações pendentes, a execução falha para impedir entrega ambígua.

## Limites

- O runner é adequado para missões locais simples e de baixo risco.
- O runner não aprova Specs.
- O runner não substitui revisão humana.
- O runner não torna seguro alterar produção, segredos, infraestrutura ou dependências sem política apropriada.
- O runner não deve ser usado para contornar validações manuais exigidas por Guardian Specs.

## Validações Recomendadas

Antes de considerar uma alteração documental concluída, execute ou confirme que o runner executou:

```bash
pytest
python3 -m compileall src
bash -n scripts/vaf-run-next-safe.sh
```
