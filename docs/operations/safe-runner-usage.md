# Uso Do Runner Seguro

## Objetivo

Documentar o uso operacional de `scripts/vaf-run-next-safe.sh` para executar uma missão local de baixo risco e de `scripts/vaf-run-batch-safe.sh` para executar múltiplas missões em sequência controlada com validações automáticas antes de considerar a entrega concluída.

## Propósito

O runner seguro de próxima missão executa a próxima missão da fila usando o worker local com limites conservadores. Ele existe para reduzir risco operacional em execuções simples ao combinar preflight, execução de uma missão, status do worker, testes, `compileall`, auto-commit e push opcional em um único fluxo abortável.

A CLI Python inicial em `src/vercosa_ai_framework/cli/` pode consultar status básico local e executar validação estrutural local por conveniência, mas não substitui este runner, não substitui `scripts/vaf-status.sh`, não substitui `pytest`, não substitui `python3 -m compileall src` e não executa missões nesta fase.

O runner seguro em batch executa várias chamadas sequenciais ao runner de próxima missão. Ele não transforma o projeto em execução cega: o batch para na primeira falha, mantém validações após cada missão por reaproveitamento do runner seguro existente, exige Git limpo após cada missão e só permite push automático ao final quando `VAF_AUTO_PUSH=1`.

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

## Runner Seguro Em Batch

Playbook detalhado: [Playbook de execução em batch](batch-execution-playbook.md).

Checklist pós-batch: [Checklist de validação pós-batch](post-batch-validation-checklist.md).

`scripts/vaf-run-next-safe.sh` executa uma missão por vez. `scripts/vaf-run-batch-safe.sh` executa múltiplas missões em sequência controlada. O playbook de batch detalha como preparar a fila, executar, validar, investigar falhas e decidir quando publicar.

Depois de qualquer execução em batch, use o checklist pós-batch para validar fila, worker, Git, testes, `compileall`, logs, documentação e decisão de push sem duplicar o fluxo do runner seguro.

Uso básico:

```bash
./scripts/vaf-run-batch-safe.sh
```

Por padrão, o batch usa `VAF_BATCH_SIZE=3`. Esse valor é o padrão inicial para testar execução sequencial controlada sem ampliar demais o risco operacional.

Uso com tamanho explícito:

```bash
VAF_BATCH_SIZE=3 ./scripts/vaf-run-batch-safe.sh
```

Uso com limite máximo inicial:

```bash
VAF_BATCH_SIZE=10 ./scripts/vaf-run-batch-safe.sh
```

`VAF_BATCH_SIZE` deve ser um inteiro entre 1 e 10. O limite máximo seguro inicial é 10. Batch de 10 só deve ser usado depois de um teste bem-sucedido com `VAF_BATCH_SIZE=3` no mesmo padrão operacional esperado.

O batch executa cada missão chamando `./scripts/vaf-run-next-safe.sh` com push desativado para aquela iteração. Os commits continuam separados por missão, porque o commit continua sendo feito pelo worker acionado pelo runner de uma missão. O push automático, quando solicitado, ocorre somente ao final do batch e somente se todas as missões executadas passarem.

Uso com push automático ao final do batch:

```bash
VAF_AUTO_PUSH=1 ./scripts/vaf-run-batch-safe.sh
```

O push automático é opt-in. Sem `VAF_AUTO_PUSH=1`, o batch não executa `git push`.

O batch para quando não há missão pendente em `missions/queue`. Se a fila acabar antes de atingir `VAF_BATCH_SIZE`, o script encerra sem tratar isso como falha e mostra o resumo final.

O batch para na primeira falha. Falhas no runner de uma missão, em `pytest`, em `python3 -m compileall src`, no Git limpo, em `missions/failed`, em `missions/running` ou no push final interrompem o fluxo.

Riscos de batch grande:

- Mais missões executadas antes de revisão humana aumentam o volume de mudanças a auditar.
- Falhas tardias podem exigir análise de múltiplos commits locais já criados.
- `VAF_COMMIT_MESSAGE` único pode ser inadequado para múltiplas missões, porque a mesma mensagem será repassada para cada commit do batch.
- Use `VAF_BATCH_SIZE=10` apenas depois de validar o fluxo com `VAF_BATCH_SIZE=3`.

## Uso Com Mensagem Customizada

```bash
VAF_COMMIT_MESSAGE="implementação: exemplo" ./scripts/vaf-run-next-safe.sh
```

Quando `VAF_COMMIT_MESSAGE` existe e não está vazia, a mensagem é repassada ao worker para o commit automático. A mensagem deve estar em português do Brasil, conforme o padrão do projeto.

No runner em batch, `VAF_COMMIT_MESSAGE` também é repassada para cada missão. Use essa variável em batch apenas quando a mesma mensagem fizer sentido para todos os commits; caso contrário, não defina uma mensagem única e permita que o worker use a mensagem padrão por missão.

## Pré-Condições

- Git limpo antes da execução.
- Worker parado antes da execução.
- Uma missão disponível em `missions/queue`.
- Branch `main` para uso com push automático.
- Testes devem passar para a missão ser considerada validada.

## Fluxo Seguro De Uma Missão

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

## Fluxo Seguro Em Batch

O script `scripts/vaf-run-batch-safe.sh` executa o seguinte fluxo local:

1. Valida `VAF_BATCH_SIZE`, usando 3 por padrão e recusando valores menores que 1 ou maiores que 10.
2. Cria diretórios operacionais de missões e logs quando necessário.
3. Para se não houver missão pendente em `missions/queue`.
4. Para na primeira falha do runner de próxima missão.
5. Chama `./scripts/vaf-run-next-safe.sh` com `VAF_AUTO_PUSH=0` para cada missão do batch.
6. Reaproveita as validações por missão do runner seguro: Git limpo, worker parado, `missions/running` vazio, `missions/failed` vazio, `pytest` e `python3 -m compileall src`.
7. Confirma Git limpo, worker parado e `failed=0` após cada missão.
8. Executa `pytest` e `python3 -m compileall src` novamente ao final do batch.
9. Executa push somente ao final, quando `VAF_AUTO_PUSH=1` e todas as missões executadas passaram.
10. Exibe resumo com missões solicitadas, missões executadas, último commit, status de `queue`, `running`, `done`, `failed`, resultado de testes, resultado de `compileall` e push.

## Comportamento Em Caso De Erro

O runner usa `set -euo pipefail` e aborta em caso de erro. Falhas de preflight, worker, estado da fila, `pytest`, `compileall`, auto-commit ou push interrompem o fluxo.

Esse comportamento preserva evidências locais para revisão, em vez de seguir com entrega parcial.

O runner em batch também usa `set -euo pipefail` e herda a parada por falha do runner de próxima missão. O batch não continua para a próxima missão quando qualquer validação falha.

Quando uma missão falha, `scripts/vaf-run-one-mission.sh` inspeciona o log local com o `Usage/API Limit Guard`. Essa inspeção é determinística, case-insensitive e não consulta billing real, provider externo, rede, banco, OpenAI, Gemini, Ollama, Claude, OpenCode ou MCPs. Se o log contiver sinais como `usage limit has been reached`, `quota exceeded`, `insufficient quota`, `billing hard limit`, rate limit persistente ou erro `429` associado a limite, o runner sinaliza a falha como limitação externa de uso/API e recomenda parada segura para investigar quota, rate limit ou billing do provider.

Essa classificação não altera missões bem-sucedidas e não mascara falhas comuns de teste, sintaxe, código ou documentação. O código de falha original da missão continua sendo usado, a missão vai para `missions/failed` e o worker para para revisão.

## Eventos Auditáveis

Os scripts seguros continuam usando logs textuais e movimentação de arquivos em `missions/queue`, `missions/running`, `missions/done` e `missions/failed`. Eles não emitem eventos auditáveis estruturados automaticamente nesta etapa.

O módulo Python [audit](../../src/vercosa_ai_framework/audit/README.md) já possui helpers opcionais para representar eventos `mission.*` e `mission.batch.*`, e o `MissionRunner` Python pode registrar eventos quando recebe um `EventLog` opcional. Essa base não substitui os logs dos scripts, não cria persistência externa e não muda o fluxo operacional atual.

Integração completa dos scripts com Audit/Event Log pode ser feita em missão futura, com cuidado para não registrar conteúdo integral de missão, prompts completos, secrets, credenciais ou tokens.

## Auto-Commit

O runner define `VAF_AUTO_COMMIT=1` por padrão, salvo quando a variável já foi definida pelo usuário. O commit automático é responsabilidade do worker acionado pelo runner e deve respeitar `VAF_COMMIT_MESSAGE` quando informada.

Se `VAF_AUTO_COMMIT=1`, o runner exige Git limpo ao final. Se restarem alterações pendentes, a execução falha para impedir entrega ambígua.

## Limites

- O runner é adequado para missões locais simples e de baixo risco.
- O runner em batch é adequado apenas para missões locais simples, de baixo risco e com fila preparada para execução sequencial.
- O runner não aprova Specs.
- O runner não substitui revisão humana.
- O runner não torna seguro alterar produção, segredos, infraestrutura ou dependências sem política apropriada.
- O runner não deve ser usado para contornar validações manuais exigidas por Guardian Specs.
- O runner em batch não deve ser usado para ampliar execução sem revisão quando as missões forem sensíveis, ambíguas ou arquiteturalmente relevantes.
- O runner não consulta limites reais de billing ou quota; ele apenas reconhece sinais textuais já presentes no log da missão.

## Validações Recomendadas

Antes de considerar uma alteração documental concluída, execute ou confirme que o runner executou:

```bash
pytest
python3 -m compileall src
bash -n scripts/vaf-run-next-safe.sh
bash -n scripts/vaf-run-batch-safe.sh
```

Próximos passos possíveis para esse diagnóstico são event log, classificação estruturada de falhas, integração futura com Provider Gateway e backoff configurável. O MVP atual não implementa retry inteligente nem consulta automática de billing.
