# Model Selection Module

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0002](../../../specs/framework/0002-model-selection-engine.md)

## Objetivo

Selecionar modelos por política, disponibilidade e atributos declarados, sem hardcode de provider ou runtime.

## O Que Este Módulo Faz

- Define perfis de modelo e decisões de seleção.
- Implementa policy mínima de seleção.
- Mantém registry em memória.
- Seleciona modelo compatível e retorna justificativa auditável.

## O Que Este Módulo Não Faz

- Não chama providers de LLM.
- Não descobre modelos reais em OpenCode ou APIs externas por conta própria.
- Não calcula billing real.
- Não executa fallback em runtime.
- Não substitui Guardian ou Context Router.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | `ModelProfile`, `SelectionDecision` e erro. |
| `policy.py` | `ModelSelectionPolicy`. |
| `selector.py` | Registry em memória e `ModelSelector`. |
| `__init__.py` | Exportações públicas do módulo. |

## Principais Tipos, Classes E Funções

- `ModelProfile`: metadados normalizados de modelo.
- `SelectionDecision`: modelo selecionado e justificativa.
- `ModelSelectionPolicy`: restrições de seleção.
- `InMemoryModelRegistry`: catálogo local em memória.
- `ModelSelector`: motor de seleção MVP.
- `select_model`: helper para seleção simples.

## Entradas E Saídas

Entradas:

- `ModelSelectionPolicy` e catálogo de `ModelProfile`.

Saídas:

- `SelectionDecision` com modelo escolhido e fallback quando aplicável.

## Dependências Internas

- Não depende diretamente de runtime ou providers.

## Módulos Relacionados

- Acima: [core](../core/README.md).
- Abaixo: [runtime](../runtime/README.md), [agents](../agents/README.md).
- Transversal: [guardian](../guardian/README.md), [providers](../providers/README.md).

## Specs Correspondentes

- [Spec 0002: Model Selection Engine](../../../specs/framework/0002-model-selection-engine.md)

## Docs Relacionadas

- [Architecture Map](../../../docs/alignment/architecture-map.md)
- [Current State](../../../docs/alignment/current-state.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.model_selection import ModelProfile, ModelSelector

selector = ModelSelector([ModelProfile(id="local-small", provider="local")])
```

## Status Atual

Status: `MVP`.

Há seleção em memória por metadados, mas descoberta real, custo, registry persistente e Context Router ainda são futuros.

## Próximos Passos

- Definir Model Registry persistente.
- Integrar descoberta de modelos por RuntimeAdapter sem acoplar a OpenCode.
