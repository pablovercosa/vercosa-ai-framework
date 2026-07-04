# Módulo workflows

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0006](../../../specs/framework/0006-workflow-engine.md)

## Objetivo

Representar e executar workflows sequenciais mínimos derivados de missões.

## O Que Este Módulo Faz

- Define tipos de workflow, task de workflow, dependência e resultado.
- Executa tasks em ordem determinística no MVP.
- Consulta Guardian antes da execução de tasks quando configurado.
- Delega execução concreta para RuntimeAdapter.

## O Que Este Módulo Não Faz

- Não é o Task Queue completo.
- Não escolhe agentes ou modelos diretamente.
- Não executa providers, MCPs ou tools.
- Não implementa paralelismo distribuído.
- Não substitui Mission Runner nem Mission Orchestrator.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | Tipos de workflow, task, dependência e resultado. |
| `engine.py` | `WorkflowEngine` sequencial. |
| `__init__.py` | Exportações públicas do módulo. |

## Principais Tipos, Classes E Funções

- `Workflow`: plano executável de alto nível.
- `WorkflowTask`: unidade de trabalho dentro do workflow.
- `TaskDependency`: dependência entre tasks.
- `WorkflowResult`: resultado agregado.
- `TaskResult`: resultado individual.
- `WorkflowEngine`: executor sequencial MVP.

## Entradas E Saídas

Entradas:

- `Workflow` com tasks e dependências.
- `RuntimeAdapter` para executar tasks.
- `GuardianEvaluator` opcional para política.

Saídas:

- `WorkflowResult` com resultados por task e status final.

## Dependências Internas

- `../guardian/`: avaliação de tasks.
- `../runtime/`: execução concreta.

## Módulos Relacionados

- Acima: [missions](../missions/README.md).
- Abaixo: [tasks](../tasks/README.md).
- Futuro executor: [agents](../agents/README.md).

## Specs Correspondentes

- [Spec 0006: Workflow Engine](../../../specs/framework/0006-workflow-engine.md)
- [Spec 0007: Task Queue](../../../specs/framework/0007-task-queue.md)

## Docs Relacionadas

- [Workflow Engine](../../../docs/workflow-engine.md)
- [Task Queue](../../../docs/task-queue.md)
- [Mapa de arquitetura](../../../docs/alignment/architecture-map.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.workflows import Workflow, WorkflowTask

workflow = Workflow(
    mission_id="mission-docs",
    title="Docs",
    goal="Atualizar documentação",
    workflow_id="wf-docs",
    tasks=(
        WorkflowTask(
            title="README",
            goal="Criar README",
            workflow_id="wf-docs",
            mission_id="mission-docs",
            task_id="task-1",
        ),
    ),
)
```

## Status Atual

Status: `MVP`.

Há execução sequencial mínima; a integração padrão com Task Queue e Agent Orchestrator ainda é lacuna arquitetural.

## Próximos Passos

- Definir contrato Workflow Engine -> Task Queue.
- Registrar decisão sobre execução sequencial direta versus uso obrigatório da Task Queue.
