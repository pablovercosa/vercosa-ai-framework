# Missions Module

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0004](../../../specs/framework/0004-mission-runner.md)

## Objetivo

Controlar o ciclo operacional de missões em uma implementação local inicial.

## O Que Este Módulo Faz

- Define tipos de missão e resultado.
- Mantém uma fila local baseada em diretório.
- Executa uma missão por meio de `MissionRunner` com avaliação Guardian e RuntimeAdapter injetado.
- Controla estados básicos como fila, execução, conclusão, falha e cancelamento.

## O Que Este Módulo Não Faz

- Não substitui o Mission Orchestrator conceitual.
- Não decompõe missões em workflows completos por conta própria.
- Não escolhe modelos diretamente.
- Não chama providers, MCPs, tools ou bancos diretamente.
- Não altera configuração global nem usa `sudo`.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | `Mission`, `MissionStatus` e `MissionResult`. |
| `queue.py` | `DirectoryMissionQueue` para fila local. |
| `runner.py` | `MissionRunner` e contratos auxiliares de execução. |
| `__init__.py` | Exportações públicas do módulo. |

## Principais Tipos, Classes E Funções

- `Mission`: unidade auditável de intenção e execução.
- `MissionStatus`: estados operacionais da missão.
- `MissionResult`: resultado normalizado de execução.
- `DirectoryMissionQueue`: fila local de missões em filesystem.
- `MissionRunner`: executa uma missão com Guardian e RuntimeAdapter.
- `AutoCommitter`: protocolo para commit automático quando política permitir.
- `GuardianEvaluator`: protocolo para avaliação de política.

## Entradas E Saídas

Entradas:

- `Mission` carregada de arquivo, fila ou chamada Python.
- `GuardianEngine` ou avaliador compatível.
- `RuntimeAdapter` para execução concreta.

Saídas:

- `MissionResult` com status, saída, erro e metadados.
- Arquivos de fila atualizados quando `DirectoryMissionQueue` é usado.

## Dependências Internas

- `../guardian/`: avaliação de políticas antes da execução.
- `../runtime/`: execução concreta por adapter.

## Módulos Relacionados

- Acima: [core](../core/README.md).
- Abaixo: [workflows](../workflows/README.md).
- Transversal: [persistence](../persistence/README.md), [guardian](../guardian/README.md).

## Specs Correspondentes

- [Spec 0004: Mission Runner](../../../specs/framework/0004-mission-runner.md)
- [Spec 0001: Framework Foundation](../../../specs/framework/0001-framework-foundation.md)

## Docs Relacionadas

- [Mission Runner](../../../docs/mission-runner.md)
- [Architecture Map](../../../docs/alignment/architecture-map.md)
- [SDD Lifecycle](../../../docs/alignment/sdd-lifecycle.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.missions import Mission

mission = Mission(title="Documentar módulo", goal="Criar README técnico")
```

## Status Atual

Status: `MVP`.

Existe execução local mínima, mas a separação final entre Mission Runner e Mission Orchestrator ainda está em aberto.

## Próximos Passos

- Resolver a fronteira Mission Runner versus Mission Orchestrator.
- Integrar formalmente com Workflow Engine e Task Queue.
