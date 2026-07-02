# Workflow Engine MVP

O Workflow Engine MVP executa um `Workflow` sequencialmente por meio de um `RuntimeAdapter` abstrato e consulta o Guardian Engine antes de cada task.

## Escopo implementado

- Executa uma task por vez.
- Ordena tasks por dependências obrigatórias simples, prioridade e metadados estáveis.
- Bloqueia o workflow quando uma task obrigatória falha.
- Marca como `skipped` uma task cuja dependência obrigatória falhou.
- Consulta o Guardian Engine antes de chamar o runtime para uma task.
- Usa apenas o contrato `RuntimeAdapter`; não chama OpenCode diretamente.
- Não usa `subprocess`, `sudo`, shell ou comandos reais.

## API

```python
from vercosa_ai_framework.guardian import GuardianEngine
from vercosa_ai_framework.runtime import OpenCodeRuntimeAdapter
from vercosa_ai_framework.workflows import WorkflowEngine

engine = WorkflowEngine(
    runtime=OpenCodeRuntimeAdapter(),
    guardian=GuardianEngine(),
    workspace=".",
)

result = engine.execute(workflow)
```

`execute()` retorna um `WorkflowResult`. O último workflow com estados atualizados fica disponível em `engine.last_workflow` para inspeção pelo Mission Runner, Task Queue ou testes.

## Regras de task obrigatória

Por padrão, toda task é obrigatória. Uma task pode ser declarada opcional com:

```python
WorkflowTask(
    ...,
    validation_policy={"required": False},
)
```

Falha de task obrigatória encerra o workflow como `failed`. Falha de task opcional não encerra o workflow, mas qualquer task que dependa obrigatoriamente dela é marcada como `skipped`.

## Guardian

Antes de executar cada task, o engine monta um `GuardianEvaluationContext` com:

- `mission_id`, `workflow_id` e `task_id`;
- objetivo do workflow;
- título e objetivo da task;
- `spec_refs` e `guardian_refs`;
- paths esperados pela task;
- limites de execução do workflow e da task;
- critérios de aceite e nível de risco.

Decisões `allow` e `warn` permitem prosseguir. Decisão `require_approval` pausa o workflow. Decisão `block` falha a task e, se ela for obrigatória, falha o workflow.

## Runtime

O engine chama somente `RuntimeAdapter.execute_task()` com um `RuntimeExecutionRequest` governado. Testes usam runtime fake e não executam OpenCode real nem subprocess real.

## Limitações do MVP

- Não implementa paralelismo.
- Não implementa retries.
- Não persiste eventos em banco ou arquivo.
- Não escolhe modelo concreto.
- Não substitui Mission Runner, Task Queue ou Agent Orchestrator.
