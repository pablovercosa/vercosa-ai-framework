# Playbook De Execução Em Batch

Links principais: [README principal](../../README.md) | [Uso do runner seguro](safe-runner-usage.md) | [Checklist pós-batch](post-batch-validation-checklist.md) | [Backlog estratégico de missões](../roadmap/mission-backlog.md) | [Roadmap](../alignment/roadmap.md)

## Objetivo

Documentar o uso operacional seguro de `scripts/vaf-run-batch-safe.sh` para preparar, executar, validar e publicar batches de missões no Vercosa AI Framework.

Este playbook descreve operação local. Ele não altera arquitetura, não aprova Specs, não remove governança e não substitui revisão humana.

## Termos Operacionais

- Execução de uma missão: execução de uma única missão da fila por `./scripts/vaf-run-next-safe.sh`, com validações antes e depois do worker.
- Execução em batch: execução sequencial de múltiplas missões por `./scripts/vaf-run-batch-safe.sh`, reaproveitando o runner seguro de uma missão e parando na primeira falha.
- Backlog estratégico: documento de planejamento, como `docs/roadmap/mission-backlog.md`, que organiza missões possíveis por fases, riscos e dependências. Ele não é executável diretamente.
- Fila executável: conjunto de arquivos `.md` em `missions/queue/`, revisados e prontos para execução pelo runner.
- Push manual: publicação feita explicitamente pelo operador depois de revisar status, commits, testes, documentação e logs.
- Push automático opt-in: publicação executada pelo runner somente quando `VAF_AUTO_PUSH=1` é definido de forma consciente.

## Escopo Operacional

O runner em batch é operacional, não arquitetural.

Ele acelera a execução sequencial de missões já presentes em `missions/queue/`. Ele não muda o modelo conceitual do framework, não cria fila estratégica, não seleciona Specs, não interpreta backlog grande e não decide se uma missão deveria existir.

Cada missão no batch precisa continuar sendo um arquivo `.md` completo, revisável e com referências suficientes. O batch não deve ser usado para compensar missões mal escritas, ambíguas, sem critérios de aceite, sem escopo claro ou sem dependências registradas.

## Comandos Principais

Comando padrão:

```bash
./scripts/vaf-run-batch-safe.sh
```

Batch de teste com 3 missões:

```bash
VAF_BATCH_SIZE=3 ./scripts/vaf-run-batch-safe.sh
```

Batch operacional com 10 missões:

```bash
VAF_BATCH_SIZE=10 ./scripts/vaf-run-batch-safe.sh
```

Batch de 10 só deve ser usado depois de um teste bem-sucedido com batch de 3 no mesmo fluxo operacional esperado.

## Variáveis Operacionais

`VAF_BATCH_SIZE` controla quantas missões o batch tenta executar.

- O padrão é `3`.
- Valores aceitos vão de `1` a `10`.
- Valores menores que `1` devem ser recusados.
- Valores maiores que `10` devem ser recusados.
- O limite máximo não deve ser aumentado sem nova decisão explícita.

`VAF_AUTO_PUSH=1` habilita push automático ao final do batch.

- É opcional.
- Não é o padrão.
- Só deve publicar ao final do batch.
- Só deve publicar se todas as missões passarem.
- Deve ser evitado nos primeiros testes.
- Deve ser usado apenas quando o fluxo estiver estável.

`VAF_COMMIT_MESSAGE` deve ser evitado em batch quando não houver decisão consciente.

- Um único `VAF_COMMIT_MESSAGE` pode gerar commits com mensagem genérica.
- Uma mensagem única pode reduzir rastreabilidade.
- Uma mensagem única pode confundir o histórico.
- Cada missão deve ter commit claro e separado.

## Pré-Requisitos Antes Do Batch

Execute as validações abaixo antes de iniciar o batch:

```bash
cd /home/projetos/vercosa-ai-framework
./scripts/vaf-status.sh
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate
git status --short
git log --oneline --decorate -8
pytest
python3 -m compileall src
```

Não inicie o batch se houver falha de testes, falha de `compileall`, Git sujo, missão em `running`, missão em `failed` ou dúvida sobre o escopo da fila.

## Como Preparar Um Batch

1. Crie missões uma por uma como arquivos `.md` individuais.
2. Revise cada Markdown antes de colocar na fila executável.
3. Garanta referências adequadas a Specs, docs, ADRs, scripts e arquivos relevantes.
4. Garanta escopo claro, incluindo o que pode e o que não pode ser alterado.
5. Garanta critérios de aceite verificáveis.
6. Commita as missões na fila antes da execução.
7. Execute o batch somente depois da revisão da fila.

O backlog estratégico pode orientar a escolha do bloco, mas a fila executável deve conter apenas missões pequenas, revisáveis e compatíveis com o estado atual do projeto.

## Como Executar Batch De Teste Com 3 Missões

Use o batch de 3 como teste inicial obrigatório:

```bash
VAF_BATCH_SIZE=3 ./scripts/vaf-run-batch-safe.sh
```

Durante esse teste, prefira não usar `VAF_AUTO_PUSH=1`. Revise localmente o resultado, os commits separados, os logs, os arquivos movidos em `missions/` e as validações finais.

## Como Executar Batch Operacional Com 10 Missões

Use batch de 10 somente depois de um batch de 3 bem-sucedido:

```bash
VAF_BATCH_SIZE=10 ./scripts/vaf-run-batch-safe.sh
```

Batch de 10 é adequado apenas para blocos pequenos ou médios, com dependências claras, baixo risco e critérios de aceite objetivos. Ele deve ser suspenso se houver falha recente, mudança arquitetural sensível ou dúvida sobre a entrega.

## Validações Durante O Batch

O batch deve preservar estas regras operacionais:

- Parar na primeira falha.
- Preservar logs para diagnóstico.
- Preservar commits já criados para revisão.
- Não continuar se `failed > 0`.
- Não continuar se Git ficar sujo.
- Não continuar se testes falharem.
- Não continuar se `python3 -m compileall src` falhar.

Se uma validação falhar, não adicione novas missões à fila antes de entender e corrigir a causa.

Se a falha for sinalizada pelo `Usage/API Limit Guard` como limitação externa de uso/API, suspenda o batch. Isso inclui sinais de `usage limit has been reached`, `quota exceeded`, `insufficient quota`, `billing hard limit`, rate limit persistente ou erro `429` associado a limite. O guard é determinístico e apenas lê o log local já produzido; ele não consulta billing real, não chama providers externos e não acessa rede ou banco.

Batch de 10 deve ser suspenso imediatamente quando houver erro de quota ou rate limit. A ação segura é parar, preservar logs e investigar os limites do provider antes de retomar a fila.

## Eventos Auditáveis De Batch

O módulo Python [audit](../../src/vercosa_ai_framework/audit/README.md) já consegue representar `mission.batch.started`, `mission.batch.completed` e `mission.batch.interrupted` com metadados seguros como `batch_size`, `executed_count`, `queue_count`, `done_count`, `failed_count` e `commit_hash` quando disponível.

O script `scripts/vaf-run-batch-safe.sh` ainda não emite esses eventos automaticamente. Nesta etapa, o batch continua dependendo de logs textuais, resumo no terminal, estado dos diretórios de missão e commits locais separados. Persistência de eventos, exportação e relação automática com commits continuam como próximos passos possíveis.

## Validações Pós-Batch

Checklist detalhado: [Checklist de validação pós-batch](post-batch-validation-checklist.md).

O playbook orienta a execução. O checklist orienta a decisão pós-batch antes de push, novo bloco de missões ou liberação de batch de 10.

Após o batch, execute:

```bash
./scripts/vaf-status.sh
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate
git status --short
git log --oneline --decorate -12
find missions -maxdepth 2 -type f | sort | tail -40
ls -lt logs | head -12
pytest
python3 -m compileall src
```

Revise se as missões esperadas saíram de `missions/queue/`, se nenhuma missão ficou em `missions/running/`, se `missions/failed/` está vazia e se os commits fazem sentido individualmente. O comando `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate` é uma validação estrutural local auxiliar; ele não substitui `./scripts/vaf-status.sh`, `pytest` ou `python3 -m compileall src`.

## Quando Fazer Push

Faça push somente depois de confirmar que:

- `failed` está igual a `0`.
- `missions/running/` está vazio.
- `git status --short` não mostra alterações pendentes.
- `pytest` passou.
- `python3 -m compileall src` passou.
- Os commits separados por missão foram revisados.
- A documentação não promete comportamento inexistente.
- A branch é `main` quando o fluxo operacional exigir publicação direta.

Prefira push manual após revisar o batch. Use `VAF_AUTO_PUSH=1` apenas quando o fluxo já estiver estável e a fila tiver baixo risco.

## Quando NÃO Fazer Push

Não faça push:

- Se `failed > 0`.
- Se `git status --short` mostrar alterações.
- Se testes falharem.
- Se `compileall` falhar.
- Se houver missão em `running`.
- Se a branch não for `main`.
- Se houver dúvida sobre a entrega.
- Se a documentação prometer algo não implementado.

## Como Investigar Falhas

Liste os últimos logs:

```bash
ls -lt logs | head -12
```

Abra o último log:

```bash
less "$(ls -t logs/*.log logs/*.out 2>/dev/null | head -1)"
```

Verifique missões em `failed`:

```bash
find missions/failed -maxdepth 1 -type f -name '*.md' | sort
```

Verifique o estado do Git:

```bash
git status --short
```

Verifique o último commit:

```bash
git log --oneline --decorate -1
```

Depois de diagnosticar, corrija a causa, valide localmente e só então considere novo batch.

Quando o diagnóstico indicar limitação externa de uso/API, trate a falha como condição operacional externa, não como bug interno do framework, até prova em contrário. Não reexecute em loop e não amplie o batch antes de confirmar quota, rate limit, crédito ou billing do provider.

## Política De Batch De 3 Para Batch De 10

- Batch de 3 é obrigatório como teste inicial.
- Batch de 10 só é aceito se batch de 3 passar.
- Batch de 10 deve ser suspenso se houver falha recente.
- Batch de 10 deve ser suspenso se houver erro de quota, rate limit, billing hard limit ou crédito insuficiente.
- Batch de 10 deve ser evitado em alterações arquiteturais sensíveis.
- Batch de 10 é mais adequado para missões pequenas ou médias com dependências claras.

## Tipos De Missão Adequadas Para Batch

- Documentação.
- Testes.
- Integração pequena.
- Refatoração localizada.
- Atualização de índices.
- Exemplos.
- Playbooks.
- Contratos simples.

## Tipos De Missão Inadequadas Para Batch De 10

- Mudança arquitetural profunda.
- Alteração em scripts críticos.
- Mudança de fluxo Git.
- Mudança no Guardian Engine com impacto amplo.
- Mudança no Policy Engine com impacto amplo.
- Mudança no Context Router com impacto amplo.
- Mudança em providers/runtimes.
- Alteração que pode afetar segurança.
- Qualquer missão com dependências incertas.

## Regra Operacional Principal

Batch acelera execução, mas não elimina revisão. Batch não substitui especificação, não deve ser cego e precisa parar cedo para preservar rastreabilidade.
