# Fluxo Operacional De Missões Em Batch

Links principais: [Exemplos](README.md) | [Uso do runner seguro](../operations/safe-runner-usage.md) | [Playbook de execução em batch](../operations/batch-execution-playbook.md) | [Checklist pós-batch](../operations/post-batch-validation-checklist.md)

## Objetivo

Explicar o fluxo operacional atual de missões locais no Vercosa AI Framework, incluindo execução segura de uma missão, execução segura em batch como padrão quando seguro, batch de 3 e batch de 10.

Status deste exemplo: exemplo operacional executável quando houver missões revisadas em `missions/queue/` e o ambiente local estiver pronto.

## Estado Atual

Implementado:

- Diretórios operacionais de missão em `missions/queue`, `missions/running`, `missions/done` e `missions/failed`.
- Runner seguro de uma missão em `scripts/vaf-run-next-safe.sh`.
- Runner seguro em batch em `scripts/vaf-run-batch-safe.sh`.
- Diagnóstico local auxiliar com `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor`.
- Validação por missão com `pytest` e `python3 -m compileall src` por reaproveitamento do runner seguro.
- Push automático opt-in com `VAF_AUTO_PUSH=1`.

Fora do escopo atual deste exemplo:

- Alterar scripts.
- Executar providers externos.
- Automatizar aprovação humana.
- Prometer integração completa com Audit/Event Log nos scripts shell.

## Fluxo De Diretórios

O fluxo operacional usa quatro diretórios principais:

```text
missions/queue
↓
missions/running
↓
missions/done
```

Quando ocorre falha, a missão pode ir para:

```text
missions/failed
```

Significado atual:

- `missions/queue`: missões pendentes, revisadas e prontas para execução.
- `missions/running`: missão em execução no momento.
- `missions/done`: missões concluídas.
- `missions/failed`: missões com falha que exigem investigação antes de continuar.

## Runner Seguro De Uma Missão

O runner seguro de uma missão executa a próxima missão da fila com limites conservadores.

Ele continua sendo o fluxo correto para missões sensíveis, arquiteturais, incertas, investigativas, de recuperação ou de alto risco.

Comando básico:

```bash
./scripts/vaf-run-next-safe.sh
```

Comportamento implementado:

- Aborta se o Git não estiver limpo antes de iniciar.
- Aborta se houver worker em execução.
- Aborta se houver missão em `missions/running` ou `missions/failed` antes da execução.
- Executa uma missão por padrão.
- Executa `pytest`.
- Executa `python3 -m compileall src`.
- Exige Git limpo ao final quando auto-commit estiver habilitado.
- Só faz push quando `VAF_AUTO_PUSH=1` for definido.

Push automático é opt-in:

```bash
VAF_AUTO_PUSH=1 ./scripts/vaf-run-next-safe.sh
```

Sem `VAF_AUTO_PUSH=1`, o runner não executa `git push`.

## Runner Seguro Em Batch

O runner seguro em batch executa múltiplas missões em sequência controlada, chamando o runner seguro de uma missão para cada item.

Comando sem variável explícita, usando o default implementado pelo script:

```bash
./scripts/vaf-run-batch-safe.sh
```

O padrão implementado pelo script é `VAF_BATCH_SIZE=3` quando a variável não é informada. O padrão operacional recomendado para blocos normais já revisados e seguros é `VAF_BATCH_SIZE=10`.

Com tamanho explícito:

```bash
VAF_BATCH_SIZE=3 ./scripts/vaf-run-batch-safe.sh
```

Comportamento implementado:

- Valida `VAF_BATCH_SIZE` entre 1 e 10.
- Para quando não há missão pendente em `missions/queue`.
- Para na primeira falha.
- Reaproveita validações do runner seguro de uma missão.
- Exige Git limpo, worker parado e `missions/failed` vazio após cada missão.
- Executa `pytest` e `python3 -m compileall src` novamente ao final do batch.
- Mantém commits separados por missão quando o worker cria commit automático.
- Só faz push automático ao final quando `VAF_AUTO_PUSH=1` for definido.

## Batch De 3

Batch de 3 é o fluxo de validação, retomada, bloco pequeno ou recuperação.

Comando:

```bash
VAF_BATCH_SIZE=3 ./scripts/vaf-run-batch-safe.sh
```

Use batch de 3 quando:

- O bloco ainda não foi validado no fluxo atual.
- As missões são pequenas ou médias.
- A fila foi revisada manualmente.
- Você quer preservar revisão frequente.
- Há alguma dúvida operacional leve, mas não bloqueante.
- Houve falha corrigida, limite externo resolvido ou retomada após interrupção.

## Batch De 10

Batch de 10 é o limite máximo seguro inicial documentado.

Comando:

```bash
VAF_BATCH_SIZE=10 ./scripts/vaf-run-batch-safe.sh
```

Use batch de 10 como fluxo operacional padrão somente quando:

- O fluxo já foi validado ou não há mudança recente no runner, na fila ou no ambiente operacional.
- As missões são pequenas ou médias.
- As dependências são claras.
- Os testes estão estáveis.
- Não há falha recente.
- O risco de conflito entre missões é baixo.
- Commits separados por missão continuam aceitáveis para revisão.

Não use batch de 10 quando:

- Houver mudança arquitetural profunda.
- Houver alteração em scripts críticos.
- Houver mudança de segurança, credenciais, rede, provider, banco ou infraestrutura.
- Houver falha recente sem diagnóstico.
- Houver dependências incertas entre missões.
- A revisão humana precisar ocorrer entre missões.
- O bloco alterar Guardian Engine, Policy Engine, Context Router, runtime ou providers com impacto amplo.
- Houver limite de API, quota, rate limit ou erro `429` recém-ocorrido.
- A recuperação após falha ainda estiver em andamento.

## Validação Pós-Batch

Validação pós-batch é obrigatória antes de push, novo batch ou liberação de batch de 10.

Comandos recomendados pelo checklist operacional:

```bash
./scripts/vaf-status.sh
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor
pytest
python3 -m compileall src
```

Use o checklist completo em [Checklist de validação pós-batch](../operations/post-batch-validation-checklist.md).

`doctor` neste exemplo é apenas diagnóstico local complementar. Ele não substitui `./scripts/vaf-status.sh`, `pytest`, `python3 -m compileall src`, revisão dos logs ou revisão dos commits.

## Limites Do Exemplo

- Este exemplo não altera scripts.
- Este exemplo não executa missões por si só.
- Este exemplo não promete push automático por padrão.
- Este exemplo não promete eventos auditáveis estruturados emitidos automaticamente pelos scripts shell.
- Este exemplo não substitui o [Playbook de execução em batch](../operations/batch-execution-playbook.md).
