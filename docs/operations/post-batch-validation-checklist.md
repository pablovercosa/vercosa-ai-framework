# Checklist De Validação Pós-Batch

Links principais: [README principal](../../README.md) | [Uso do runner seguro](safe-runner-usage.md) | [Playbook de execução em batch](batch-execution-playbook.md)

## Objetivo

Padronizar a validação operacional obrigatória do Vercosa AI Framework depois de uma execução em batch, antes de fazer push, iniciar novo bloco de missões ou retomar execução após interrupção.

Este checklist deve ser usado depois de `./scripts/vaf-run-batch-safe.sh`, depois de qualquer batch com `VAF_BATCH_SIZE=3`, depois de qualquer batch com `VAF_BATCH_SIZE=10`, antes de `git push` e antes de iniciar novo bloco de missões.

Batch é o fluxo operacional padrão quando o bloco estiver bem especificado, revisado e seguro. Este checklist é o bloqueio operacional antes de publicação: sem validação pós-batch, não faça push.

Ele complementa o [playbook de execução em batch](batch-execution-playbook.md). Ele não substitui o runner seguro, não aprova mudanças automaticamente e não elimina revisão humana.

## Checklist rápido

- Worker parado.
- `queue` no estado esperado para o batch executado.
- `running=0`.
- `failed=0`.
- `missions` executado como listagem complementar quando for útil conferir nomes de arquivos por estado.
- `batch-summary` executado como diagnóstico complementar quando for útil reunir contagens, último log e lembretes manuais.
- `doctor` executado como diagnóstico complementar.
- Branch `main`.
- Git limpo.
- Últimos commits coerentes.
- Testes passando.
- `compileall` passando.
- Logs sem falha relevante.
- Logs sem sinal de quota, rate limit, billing hard limit, crédito insuficiente ou `Usage/API Limit Guard`.
- Documentação criada ou atualizada conforme esperado.
- Nenhuma promessa de funcionalidade inexistente.
- Push ainda não feito, salvo se explicitamente solicitado.
- `VAF_AUTO_PUSH` não foi usado sem decisão explícita.

## Comandos de validação pós-batch

Execute os comandos abaixo a partir do repositório:

```bash
cd /home/projetos/vercosa-ai-framework

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

`PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions` lista nomes de arquivos `.md` por estado, com contagens gerais, sem executar ou mover missões. `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main batch-summary` reúne contagens, último log local quando houver, avisos de atenção e lembretes manuais de validação. `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate` é uma validação estrutural local auxiliar. `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor` combina essa validação com mensagens operacionais de diagnóstico local. Esses comandos verificam ou listam diretórios básicos de missão, `README.md`, `src/vercosa_ai_framework` e alguns documentos auxiliares, mas não substituem `./scripts/vaf-status.sh`, `pytest`, `python3 -m compileall src`, revisão dos logs ou revisão dos commits.

`doctor` é etapa complementar de diagnóstico pós-batch. Ele pode ajudar a identificar inconsistências estruturais, como missão presa em `running`, missão em `failed`, diretório obrigatório ausente ou documento operacional auxiliar ausente, mas não é requisito único de aprovação.

`batch-summary` também é complementar. Ele não verifica worker, não executa Git, não executa testes, não executa `compileall`, não aprova push e não promete validação completa.

Se `doctor` apontar erro, não faça push até investigar e corrigir ou justificar o estado local. Se `doctor` apontar warning, avalie o aviso antes de continuar; warning não libera push por si só.

## Validação das missões executadas

Confira se o estado das missões corresponde ao batch executado:

- As missões esperadas saíram de `missions/queue`.
- As missões concluídas foram para `missions/done`.
- Nenhuma missão foi para `missions/failed`.
- Não há missão presa em `missions/running`.
- Os logs recentes correspondem às missões executadas.
- Cada missão gerou commit separado quando o fluxo estava com auto-commit habilitado.

Se uma missão esperada não mudou de estado, se um log não corresponde à missão executada ou se um commit agrupa múltiplas missões sem intenção explícita, pare e investigue antes de novo batch ou push.

## Validação do Git

Antes de publicar ou iniciar outro batch:

- Confirme que a branch atual é `main`.
- Confirme que `git status --short` está vazio.
- Confirme que os últimos commits representam as missões executadas.
- Confirme se `origin/main` ainda está atrás ou já atualizado antes de decidir o push.
- Não use force push.
- Não reescreva histórico.
- Prefira push manual após a validação.
- Confirme que `VAF_AUTO_PUSH=1` não foi usado por acidente.

Use `git log --oneline --decorate -12` para revisar mensagens, ordem e escopo dos commits recentes. Mensagens futuras devem estar em português do Brasil, salvo nomes técnicos consolidados.

## Validação de testes

Execute sempre:

```bash
pytest
python3 -m compileall src
```

- Falha em `pytest` bloqueia push.
- Falha em `python3 -m compileall src` bloqueia push.
- Resultado parcial não é aceito.
- Teste interrompido, pulado sem explicação ou dependente de estado ambíguo deve ser tratado como bloqueio até diagnóstico.

## Validação de documentação

Revise a documentação tocada pelo batch:

- Texto explicativo em português do Brasil.
- Links relativos funcionando, quando aplicável.
- `README.md` atualizado somente quando necessário.
- `docs/architecture/module-index.md` atualizado somente quando necessário.
- Docs operacionais apontando entre si quando houver relação direta.
- Nenhuma promessa de recurso futuro como se já estivesse implementado.

Se documentação, Spec e código ficarem incoerentes, registre a dúvida ou corrija a documentação antes de publicar.

## Quando fazer push

Faça push somente quando todos os itens abaixo forem verdadeiros:

- `failed=0`.
- `running=0`.
- Worker parado.
- `doctor` não aponta erro e warnings foram avaliados.
- `git status --short` vazio.
- Branch `main`.
- `pytest` passa.
- `python3 -m compileall src` passa.
- Últimos commits estão coerentes.
- Não há dúvida sobre a entrega.

Prefira push manual após revisar o batch. `VAF_AUTO_PUSH=1` continua sendo opt-in e deve ser usado apenas quando o fluxo estiver estável e a fila for de baixo risco.

## Quando NÃO fazer push

Não faça push quando qualquer item abaixo ocorrer:

- Qualquer missão foi para `missions/failed`.
- Alguma missão ficou em `missions/running`.
- `doctor` apontou erro ainda não investigado.
- Git está sujo.
- Testes falharam.
- `compileall` falhou.
- Branch não é `main`.
- Logs mostram erro não explicado.
- Documentação ficou incoerente.
- Houve commit com mensagem errada.
- Houve alteração fora do escopo.
- Houve dúvida sobre resultado do batch.
- Houve sinal de `usage limit`, `quota exceeded`, `insufficient quota`, `rate limit` ou erro `429`.

## Quando parar e investigar

Pare antes de novo batch, push ou liberação de batch de 10 quando houver:

- `failed > 0`.
- `running > 0` com worker parado.
- `queue` diferente do esperado.
- Logs incompatíveis com as missões executadas.
- Log sinalizado pelo `Usage/API Limit Guard` como limitação externa de uso/API.
- Commit faltando.
- Commit com escopo errado.
- Arquivo criado em local errado.
- Teste quebrado.
- `compileall` quebrado.
- Documentação prometendo o que não foi implementado.

## Comandos de investigação

Use estes comandos para preservar diagnóstico local antes de tomar nova ação:

```bash
ls -lt logs | head -20
tail -n 160 "$(ls -t logs/*.log | head -1)"
find missions/failed -maxdepth 1 -type f -print | sort
find missions/running -maxdepth 1 -type f -print | sort
git log --oneline --decorate -15
git show --stat --oneline HEAD
git show --name-only --oneline HEAD
```

Se não houver arquivo `.log`, confira também saídas `.out` recentes em `logs/` antes de concluir que não existe evidência.

Se o log mencionar `Usage/API Limit Guard`, `usage limit has been reached`, `quota exceeded`, `insufficient quota`, `billing hard limit`, rate limit persistente ou erro `429` associado a limite, suspenda novo batch e investigue limites do provider. Essa verificação é local e determinística: ela não consulta billing real, não chama provider externo, não acessa rede e não implementa retry inteligente.

Limite externo de API não é, por si só, bug interno do projeto. Não insista em retries. Verifique `missions/queue`, `missions/running`, `missions/done` e `missions/failed`; se houver missão presa em `running`, devolva para `queue` somente quando for seguro e depois de entender o estado real da entrega. Retome com execução individual ou `VAF_BATCH_SIZE=3` apenas quando quota, rate limit, crédito ou billing estiverem disponíveis.

## Quando usar batch de 10

Batch de 10 é o fluxo operacional padrão para blocos normais já revisados e seguros. Use somente quando:

- O fluxo já foi validado ou não há mudança recente no runner, na fila ou no ambiente operacional.
- `failed=0`.
- Testes passaram.
- `compileall` passou.
- Git ficou limpo.
- Commits ficaram separados.
- Documentação ficou coerente.
- Não houve falha recente.
- Não há missão de alto risco no próximo bloco.

O operador deve usar batch de 3 quando o risco, a revisão, a retomada, a recuperação ou a dependência entre missões recomendar blocos menores. Use execução individual para missões sensíveis, arquiteturais, incertas, investigativas ou críticas.

## Quando suspender batch de 10

Suspenda batch de 10 quando:

- Houve falha no batch anterior.
- Houve falha de quota, rate limit, billing hard limit ou crédito insuficiente no batch anterior.
- Haverá mudança estrutural profunda.
- Haverá alteração em scripts críticos.
- Haverá alteração no Guardian Engine com impacto amplo.
- Haverá alteração no Policy Engine com impacto amplo.
- Haverá alteração no Context Router com impacto amplo.
- Haverá alteração em providers/runtimes.
- Dependências entre missões estão incertas.
- Critérios de aceite estão fracos.
- Missões estão pequenas demais ou vagas demais.
- Referências obrigatórias estão incompletas.
- Houve limite de API ou quota recém-ocorrido.

Nesses casos, reduza o batch, revise as missões ou execute uma missão por vez.

## Resultado esperado de um batch saudável

Um batch saudável deve terminar com resultado equivalente a:

```text
queue:   0
running: 0
failed:  0
worker:  stopped
pytest:  passou
compileall: passou
git: limpo
commits: separados por missão
```

O valor de `queue` pode ser maior que `0` quando o batch executou apenas parte de uma fila maior. Nesse caso, ele ainda precisa estar no estado esperado para o número de missões solicitado.

## Regra final

- Se houver dúvida, não fazer push.
- Se houver falha, parar.
- Se houver limite externo de API, parar e retomar somente quando a quota estiver disponível.
- Se a missão for sensível, usar execução individual.
- Se o bloco estiver revisado e seguro, batch de 10 é o fluxo operacional padrão.
