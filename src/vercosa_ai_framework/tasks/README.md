# Tasks Module

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0007](../../../specs/framework/0007-task-queue.md)

## Objetivo

Gerenciar estado, elegibilidade, tentativas e agendamento determinístico de tasks.

## O Que Este Módulo Faz

- Define tasks operacionais, prioridades, estados e tentativas.
- Mantém `TaskQueue` em memória.
- Calcula elegibilidade por dependências.
- Registra início, conclusão, falha, bloqueio, cancelamento e retry.
- Oferece scheduler sequencial determinístico.

## O Que Este Módulo Não Faz

- Não planeja workflows.
- Não executa providers, tools, runtime ou agentes diretamente.
- Não escolhe modelos.
- Não persiste estado final em banco.
- Não implementa paralelismo distribuído.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | `Task`, estados, prioridades, tentativas e resultados. |
| `queue.py` | `TaskQueue` em memória. |
| `scheduler.py` | `TaskScheduler` sequencial. |
| `__init__.py` | Exportações públicas do módulo. |

## Principais Tipos, Classes E Funções

- `Task`: unidade operacional de trabalho.
- `TaskPriority`: ordenação de prioridade.
- `TaskQueueState`: estados da fila.
- `TaskAttempt`: tentativa de execução.
- `TaskQueue`: gerenciador de estado de tasks.
- `TaskScheduler`: despachante sequencial.
- `TaskExecutionOutcome`: resultado de execução usado pelo scheduler.

## Entradas E Saídas

Entradas:

- `Task` com dependências, prioridade e limites.
- Resultado de execução fornecido por executor externo ao módulo.

Saídas:

- `TaskQueueResult` ou `TaskSchedulerResult` com estado atualizado e tentativas.

## Dependências Internas

- Não depende diretamente de runtime, guardian ou providers.

## Módulos Relacionados

- Acima: [workflows](../workflows/README.md).
- Abaixo: [agents](../agents/README.md).
- Transversal: [persistence](../persistence/README.md).

## Specs Correspondentes

- [Spec 0007: Task Queue](../../../specs/framework/0007-task-queue.md)
- [Spec 0006: Workflow Engine](../../../specs/framework/0006-workflow-engine.md)

## Docs Relacionadas

- [Task Queue](../../../docs/task-queue.md)
- [Architecture Map](../../../docs/alignment/architecture-map.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.tasks import Task, TaskQueue

queue = TaskQueue()
queue.add(
    Task(
        task_id="task-1",
        title="Validar",
        goal="Executar validação",
        workflow_id="wf-1",
        mission_id="mission-1",
    )
)
```

## Status Atual

Status: `MVP`.

O módulo cobre fila e scheduler em memória, mas ainda não é o substrato padrão de todos os workflows.

## Próximos Passos

- Integrar Task Queue como executor padrão do Workflow Engine.
- Definir persistência de estado e retries além de memória.
