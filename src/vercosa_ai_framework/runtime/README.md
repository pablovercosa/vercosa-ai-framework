# Runtime Module

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0003](../../../specs/framework/0003-opencode-runtime-adapter.md)

## Objetivo

Isolar execução concreta em runtimes substituíveis, começando por OpenCode como adapter inicial.

## O Que Este Módulo Faz

- Define contrato abstrato de RuntimeAdapter.
- Define tipos de runtime, capabilities, planos e resultados.
- Implementa `OpenCodeRuntimeAdapter` MVP.
- Monta comandos `opencode run` de forma controlada e suporta dry-run.

## O Que Este Módulo Não Faz

- Não define arquitetura central do framework.
- Não decide política, modelo, custo ou aprovação por conta própria.
- Não altera configuração global do OpenCode.
- Não executa `sudo`.
- Não substitui Provider Gateway ou Tool Executor.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | Tipos de runtime, plano, request e resultado. |
| `adapter.py` | Contrato abstrato `RuntimeAdapter`. |
| `opencode.py` | Adapter inicial para OpenCode. |
| `__init__.py` | Exportações públicas do módulo. |

## Principais Tipos, Classes E Funções

- `RuntimeStatus`: disponibilidade do runtime.
- `RuntimeCapability`: capability detectada/declarada.
- `RuntimeInfo`: informações do runtime.
- `RuntimeExecutionRequest`: pedido governado de execução.
- `RuntimeExecutionPlan`: plano de execução.
- `RuntimeExecutionResult`: resultado normalizado.
- `RuntimeAdapter`: contrato abstrato.
- `OpenCodeRuntimeAdapter`: adapter inicial para OpenCode.
- `OpenCodeRunOptions`: opções de execução OpenCode.
- `CommandExecutor`: protocolo para execução de comando.

## Entradas E Saídas

Entradas:

- `RuntimeExecutionRequest` produzido por missão, workflow ou agente.
- Opções de execução e workspace.

Saídas:

- `RuntimeExecutionPlan` em dry-run.
- `RuntimeExecutionResult` com status, saída, erro e metadados.

## Dependências Internas

- Recebe decisões de módulos superiores; não deve depender deles para escolher política.

## Módulos Relacionados

- Acima: [missions](../missions/README.md), [workflows](../workflows/README.md), [agents](../agents/README.md).
- Abaixo: OpenCode e runtimes externos futuros.
- Paralelo: [providers](../providers/README.md), [tools](../tools/README.md).

## Specs Correspondentes

- [Spec 0003: OpenCode Runtime Adapter](../../../specs/framework/0003-opencode-runtime-adapter.md)
- [Spec 0002: Model Selection Engine](../../../specs/framework/0002-model-selection-engine.md)

## Docs Relacionadas

- [OpenCode Runtime Adapter](../../../docs/opencode-runtime-adapter.md)
- [External Framework Positioning](../../../docs/alignment/external-framework-positioning.md)
- [Architecture Map](../../../docs/alignment/architecture-map.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.runtime import OpenCodeRunOptions, OpenCodeRuntimeAdapter

runtime = OpenCodeRuntimeAdapter(options=OpenCodeRunOptions(dry_run=True))
```

## Status Atual

Status: `MVP`.

O adapter OpenCode existe como implementação inicial, mas conformance comum para outros runtimes ainda precisa ser formalizada.

## Próximos Passos

- Definir contrato de conformidade para RuntimeAdapter.
- Adicionar descoberta de capabilities e modelos sem acoplar ao núcleo.
