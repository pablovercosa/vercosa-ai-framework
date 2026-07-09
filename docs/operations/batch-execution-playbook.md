# Playbook De Execução Em Batch

Links principais: [README principal](../../README.md) | [Uso do runner seguro](safe-runner-usage.md) | [Checklist pós-batch](post-batch-validation-checklist.md) | [Backlog estratégico de missões](../roadmap/mission-backlog.md) | [Roadmap](../alignment/roadmap.md)

## Objetivo

Documentar o uso operacional seguro de `scripts/vaf-run-batch-safe.sh` como fluxo normal para preparar, executar, validar e publicar batches de missões no Vercosa AI Framework quando o bloco estiver bem especificado, revisado e seguro.

Este playbook descreve operação local. Ele não altera arquitetura, não aprova Specs, não remove governança e não substitui revisão humana.

## Termos Operacionais

- Execução de uma missão: execução de uma única missão da fila por `./scripts/vaf-run-next-safe.sh`, com validações antes e depois do worker.
- Execução em batch: execução sequencial de múltiplas missões por `./scripts/vaf-run-batch-safe.sh`, reaproveitando o runner seguro de uma missão e parando na primeira falha.
- Fluxo operacional padrão: execução em batch de missões completas, revisadas e seguras, com validação obrigatória antes de push.
- Fluxo sensível: execução individual de missões críticas, arquiteturais, incertas, de alto risco, investigativas ou de recuperação.
- Fluxo de retomada: batch reduzido, normalmente com `VAF_BATCH_SIZE=3`, após teste, limite externo, falha corrigida ou bloco pequeno.
- Backlog estratégico: documento de planejamento, como `docs/roadmap/mission-backlog.md`, que organiza missões possíveis por fases, riscos e dependências. Ele não é executável diretamente.
- Fila executável: conjunto de arquivos `.md` em `missions/queue/`, revisados e prontos para execução pelo runner.
- Push manual: publicação feita explicitamente pelo operador depois de revisar status, commits, testes, documentação e logs.
- Push automático opt-in: publicação executada pelo runner somente quando `VAF_AUTO_PUSH=1` é definido de forma consciente.

## Escopo Operacional

O runner em batch é operacional, não arquitetural. Ele é o fluxo operacional padrão do projeto quando a fila contém um bloco seguro de missões completas, revisadas e com critérios de aceite objetivos.

Ele acelera a execução sequencial de missões já presentes em `missions/queue/`. Ele não muda o modelo conceitual do framework, não cria fila estratégica, não seleciona Specs, não interpreta backlog grande e não decide se uma missão deveria existir.

Cada missão no batch precisa continuar sendo um arquivo `.md` completo, revisável e com referências suficientes. O batch não deve ser usado para compensar missões mal escritas, ambíguas, sem critérios de aceite, sem escopo claro ou sem dependências registradas.

Batch não significa execução cega. Ele não substitui missões completas em Markdown, revisão, testes, `python3 -m compileall src`, commits separados, validação pós-batch nem decisão consciente de push.

## Decisão De Fluxo

Use batch como padrão quando:

- o bloco de missões estiver revisado;
- cada missão tiver objetivo, escopo, restrições, referências e critérios de aceite claros;
- as dependências entre missões forem conhecidas;
- as mudanças forem pequenas ou médias;
- não houver falha recente sem diagnóstico;
- o operador aceitar revisar commits separados após a execução.

Use execução individual quando houver:

- mudança arquitetural profunda;
- alteração em scripts críticos;
- alteração no Guardian Engine com impacto amplo;
- alteração no Policy Engine com impacto amplo;
- alteração no Context Router com impacto amplo;
- alteração em providers ou runtimes;
- dependências incertas;
- critérios de aceite fracos;
- recuperação após falha;
- investigação de erro;
- limite de API ou quota recém-ocorrido.

## Comandos Principais

Comando sem variável explícita, usando o default implementado pelo script:

```bash
./scripts/vaf-run-batch-safe.sh
```

Batch de validação, retomada ou bloco pequeno com 3 missões:

```bash
VAF_BATCH_SIZE=3 ./scripts/vaf-run-batch-safe.sh
```

Batch operacional padrão com 10 missões:

```bash
VAF_BATCH_SIZE=10 ./scripts/vaf-run-batch-safe.sh
```

Batch de 10 é o tamanho recomendado para blocos normais já revisados e seguros. Batch de 3 é recomendado para testes, retomadas, blocos pequenos ou recuperação.

## Diagnóstico Local Com `doctor` E `batch-summary`

O comando `doctor` entra no fluxo de batch como diagnóstico local auxiliar. Use-o para obter uma leitura amigável da estrutura mínima do projeto, contagens de missões, presença de missão presa em `running`, presença de missão em `failed` e avisos sobre documentos operacionais auxiliares.

No checkout local atual, a forma documentada de invocação é:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor
```

Use `doctor` nestes momentos:

- Antes de preparar um batch, para identificar inconsistência estrutural antes de organizar a fila.
- Antes de executar um batch, junto com `validate`, `vaf-status.sh`, Git, testes e `compileall`.
- Depois de um batch, como diagnóstico complementar ao checklist pós-batch.
- Durante investigação de estado inconsistente, especialmente quando houver missão em `running` ou `failed`.
- Após interrupção por limite externo de API, para confirmar o estado local antes de decidir retomada.

Diferença prática entre ferramentas:

- `./scripts/vaf-status.sh` mostra estado operacional dos scripts e diretórios de missão.
- `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate` verifica a estrutura mínima local.
- `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor` fornece diagnóstico local mais amigável e não destrutivo sobre a mesma base estrutural, com avisos operacionais simples.
- `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main batch-summary` fornece resumo pós-batch auxiliar, último log local quando houver e lembretes manuais de validação.
- `pytest` valida o comportamento coberto por testes.
- `python3 -m compileall src` valida compilação dos módulos Python.

`doctor` não substitui `./scripts/vaf-status.sh`, `pytest`, `python3 -m compileall src`, revisão dos logs nem revisão dos commits. Ele também não executa missões, não chama scripts shell, não executa Git, não acessa rede, não consulta provider, não verifica quota real e não deve ser tratado como aprovação única para batch ou push.

Use `batch-summary` depois de um batch para obter um resumo local e somente leitura das contagens de `queue`, `running`, `done` e `failed`, do último log encontrado em `logs/` e dos lembretes manuais de validação:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main batch-summary
```

`batch-summary` é complementar ao resumo exibido por `./scripts/vaf-run-batch-safe.sh`. Ele não executa missões, não chama scripts shell, não verifica worker, não executa Git, não executa `pytest`, não executa `python3 -m compileall src`, não acessa rede, não acessa banco e não consulta providers. Se ele indicar `running > 0`, `failed > 0` ou `queue > 0`, trate como atenção operacional antes de novo batch ou push.

## Listagem Local Com `missions`

O comando `missions` ajuda a inspecionar a fila executável e os demais estados antes e depois de batch, sem executar ou mover missões.

Forma documentada de invocação no checkout local:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions --state queue
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions --state failed
```

Use `missions` nestes momentos:

- Antes de executar um batch, para conferir nomes de arquivos em `missions/queue/`.
- Depois de um batch, para conferir se os arquivos esperados saíram de `queue` e se `running` e `failed` estão vazios.
- Durante investigação, para listar rapidamente missões em `running` ou `failed` sem usar comandos shell adicionais.

`missions` não substitui `./scripts/vaf-status.sh`. O script mostra o resumo operacional dos scripts e diretórios; a CLI lista os nomes dos arquivos `.md` por estado, com contagens gerais e ordenação determinística. O comando também não executa Git, não acessa logs, não roda testes, não roda `compileall`, não chama providers e não deve ser tratado como aprovação automática para push.

Exemplo operacional claro antes de executar um batch:

```bash
./scripts/vaf-status.sh
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main batch-summary
git status --short
pytest
python3 -m compileall src
```

Se `doctor` retornar `status_geral: error`, não inicie nem retome batch antes de investigar. Se retornar `status_geral: warning`, avalie o aviso antes de continuar; warning não é aprovação automática.

## Variáveis Operacionais

`VAF_BATCH_SIZE` controla quantas missões o batch tenta executar.

- O padrão implementado no script é `3` quando `VAF_BATCH_SIZE` não é informado.
- O padrão operacional recomendado para blocos normais já revisados é `10`.
- O padrão operacional recomendado para testes, retomadas, blocos pequenos ou recuperação é `3`.
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
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main batch-summary
git status --short
git log --oneline --decorate -8
pytest
python3 -m compileall src
```

Não inicie o batch se houver falha de testes, falha de `compileall`, Git sujo, missão em `running`, missão em `failed`, dúvida sobre o escopo da fila, alteração fora do escopo ou limite externo de API recém-ocorrido.

## Como Preparar Um Batch

1. Crie missões uma por uma como arquivos `.md` individuais.
2. Revise cada Markdown antes de colocar na fila executável.
3. Garanta referências adequadas a Specs, docs, ADRs, scripts e arquivos relevantes.
4. Garanta escopo claro, incluindo o que pode e o que não pode ser alterado.
5. Garanta critérios de aceite verificáveis.
6. Commita as missões na fila antes da execução.
7. Execute o batch somente depois da revisão da fila.

O backlog estratégico pode orientar a escolha do bloco, mas a fila executável deve conter apenas missões pequenas, revisáveis e compatíveis com o estado atual do projeto.

## Como Executar Batch De Validação Ou Retomada Com 3 Missões

Use o batch de 3 para validar fluxo, retomar depois de interrupção, executar bloco pequeno ou recuperar após falha corrigida:

```bash
VAF_BATCH_SIZE=3 ./scripts/vaf-run-batch-safe.sh
```

Durante esse teste, prefira não usar `VAF_AUTO_PUSH=1`. Revise localmente o resultado, os commits separados, os logs, os arquivos movidos em `missions/` e as validações finais.

## Como Executar Batch Operacional Padrão Com 10 Missões

Use batch de 10 para blocos normais já revisados, seguros e com dependências claras:

```bash
VAF_BATCH_SIZE=10 ./scripts/vaf-run-batch-safe.sh
```

Batch de 10 é o fluxo operacional padrão quando essas condições forem atendidas. Ele deve ser suspenso se houver falha recente, mudança arquitetural sensível, limite externo de API, Git sujo, missão presa em `running`, missão em `failed`, alteração fora do escopo ou dúvida sobre a entrega.

## Validações Durante O Batch

O batch deve preservar estas regras operacionais:

- Parar na primeira falha.
- Preservar logs para diagnóstico.
- Preservar commits já criados para revisão.
- Não continuar se `failed > 0`.
- Não continuar se Git ficar sujo.
- Não continuar se testes falharem.
- Não continuar se `python3 -m compileall src` falhar.
- Não continuar se houver missão presa em `running`.
- Não continuar se houver alteração fora do escopo.
- Não continuar se houver dúvida sobre a entrega.

Se uma validação falhar, não adicione novas missões à fila antes de entender e corrigir a causa.

Se a falha for sinalizada pelo `Usage/API Limit Guard` como limitação externa de uso/API, suspenda o batch. Isso inclui sinais de `usage limit has been reached`, `quota exceeded`, `insufficient quota`, `billing hard limit`, rate limit persistente ou erro `429` associado a limite. O guard é determinístico e apenas lê o log local já produzido; ele não consulta billing real, não chama providers externos e não acessa rede ou banco.

Limite externo de API não deve ser tratado automaticamente como bug interno do projeto. Não insista em retries. Pare, preserve logs, verifique `missions/queue`, `missions/running`, `missions/done` e `missions/failed`, devolva missão presa em `running` para `queue` somente quando for seguro e continue apenas depois que quota, rate limit, crédito ou billing estiverem disponíveis.

## Eventos Auditáveis De Batch

O módulo Python [audit](../../src/vercosa_ai_framework/audit/README.md) já consegue representar `mission.batch.started`, `mission.batch.completed` e `mission.batch.interrupted` com metadados seguros como `batch_size`, `executed_count`, `queue_count`, `done_count`, `failed_count` e `commit_hash` quando disponível.

O script `scripts/vaf-run-batch-safe.sh` ainda não emite esses eventos automaticamente. Nesta etapa, o batch continua dependendo de logs textuais, resumo no terminal, estado dos diretórios de missão e commits locais separados. Persistência de eventos, exportação e relação automática com commits continuam como próximos passos possíveis.

## Validações Pós-Batch

Checklist detalhado: [Checklist de validação pós-batch](post-batch-validation-checklist.md).

O playbook orienta a execução. O checklist é obrigatório antes de push, novo bloco de missões ou continuação após falha.

Após o batch, execute:

```bash
./scripts/vaf-status.sh
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main batch-summary
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor
git status --short
git log --oneline --decorate -12
find missions -maxdepth 2 -type f | sort | tail -40
ls -lt logs | head -12
pytest
python3 -m compileall src
```

Revise se as missões esperadas saíram de `missions/queue/`, se nenhuma missão ficou em `missions/running/`, se `missions/failed/` está vazia e se os commits fazem sentido individualmente. Os comandos `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions`, `batch-summary`, `validate` e `doctor` são auxiliares locais; eles não substituem `./scripts/vaf-status.sh`, `pytest` ou `python3 -m compileall src`.

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

Prefira push manual após revisar o batch. `VAF_AUTO_PUSH=1` continua opt-in, não é padrão operacional e deve ser usado apenas quando o fluxo já estiver estável e a fila tiver baixo risco.

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

Depois de diagnosticar, corrija a causa, valide localmente e só então considere novo batch. Para recuperação, prefira execução individual ou `VAF_BATCH_SIZE=3` antes de voltar a `VAF_BATCH_SIZE=10`.

Quando o diagnóstico indicar limitação externa de uso/API, trate a falha como condição operacional externa, não como bug interno do framework, até prova em contrário. Não reexecute em loop e não amplie o batch antes de confirmar quota, rate limit, crédito ou billing do provider.

## Política De Batch De 3 E Batch De 10

- Batch de 10 é o fluxo operacional padrão para blocos normais já revisados e seguros.
- Batch de 3 é o fluxo de validação, retomada, recuperação ou blocos pequenos.
- Batch de 10 deve ser suspenso se houver falha recente.
- Batch de 10 deve ser suspenso se houver erro de quota, rate limit, billing hard limit ou crédito insuficiente.
- Batch de 10 deve ser evitado em alterações arquiteturais sensíveis.
- Batch de 10 é mais adequado para missões pequenas ou médias com dependências claras.
- Execução individual continua sendo o fluxo correto para missões sensíveis, críticas, investigativas ou incertas.

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
- Qualquer missão com critérios de aceite fracos.
- Recuperação após falha.
- Investigação de erro.
- Limite de API ou quota recém-ocorrido.

## Regra Operacional Principal

Batch acelera execução, mas não elimina revisão. Batch não substitui especificação, não deve ser cego e precisa parar cedo para preservar rastreabilidade.
