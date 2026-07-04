# Context Module

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0014](../../../specs/framework/0014-context-router-token-budget-memory.md)

## Objetivo

Definir contratos e MVP determinístico para Context Router, Token Budget Manager, Context Package e camadas conceituais de memória.

## O Que Este Módulo Faz

- Define tipos conceituais para fontes, itens, citações, redactions, omissões, risco, budgets e camadas de memória.
- Define a porta abstrata `ContextRouter`.
- Implementa `DeterministicContextRouter` para candidatos explícitos de contexto.
- Define a porta abstrata `TokenBudgetManager`.
- Implementa `SimpleTokenBudgetManager` com estimativa determinística simples.
- Deduplica candidatos por hash ou id.
- Respeita limite básico de tokens estimados.
- Preserva citações e redactions já presentes nos itens.
- Produz `ContextPackage` rastreável.

## O Que Este Módulo Não Faz

- Não implementa Semantic Index.
- Não gera embeddings.
- Não usa PostgreSQL, pgvector, SQLite ou qualquer banco.
- Não implementa RAG funcional.
- Não acessa filesystem.
- Não chama providers, LLMs, APIs, MCPs, OpenCode, Ollama, Gemini, OpenAI, Claude ou runtimes.
- Não escolhe modelos concretos.
- Não executa redaction; apenas preserva registros já recebidos.
- Não substitui Policy Engine, Guardian Engine, Knowledge Hub, Canonicalizer, Persistence Layer ou Model Selection Engine.
- Não promete memória infinita.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | Enums e dataclasses de contexto, tokens e memória. |
| `router.py` | Porta `ContextRouter` e `DeterministicContextRouter`. |
| `budget.py` | Porta `TokenBudgetManager` e `SimpleTokenBudgetManager`. |
| `__init__.py` | Exportações públicas do módulo. |

## Principais Tipos, Classes E Funções

- `ContextSourceType`: tipos iniciais de fonte de contexto.
- `ContextItemType`: tipos de item de contexto.
- `ContextOmissionReason`: motivos de omissão.
- `ContextRiskLevel`: níveis de risco de contexto.
- `MemoryLayerType`: camadas conceituais de memória.
- `ContextSource`: fonte candidata ou selecionada.
- `ContextCitation`: citação auditável.
- `ContextRedaction`: registro de redaction sem valor original.
- `ContextItem`: item candidato ou selecionado.
- `ContextRequest`: entrada do roteador.
- `ContextPackage`: pacote final de contexto.
- `TokenBudget`: orçamento máximo e reserva de output.
- `TokenEstimate`: estimativa determinística de tokens.
- `TokenBudgetDecision`: decisão de inclusão ou omissão por orçamento.
- `MemoryLayer`: descrição storage agnostic de uma camada de memória.
- `ContextRouter`: contrato abstrato do roteador.
- `DeterministicContextRouter`: roteador MVP sem efeitos externos.
- `TokenBudgetManager`: contrato abstrato de orçamento.
- `SimpleTokenBudgetManager`: estimador MVP sem chamadas externas.

## Entradas E Saídas

Entradas:

- `ContextRequest` com objetivo, escopo, orçamento e candidatos explícitos.
- `ContextSource` e `ContextItem` criados por chamadores autorizados.

Saídas:

- `ContextPackage` com itens, fontes, citações, estimativas, redactions e omissões.
- `TokenBudgetDecision` para itens incluídos ou omitidos.

## Dependências Internas

- Não depende de outros módulos do framework na implementação atual.

## Módulos Relacionados

- Acima: [agents](../agents/README.md), [capabilities](../capabilities/README.md), [skills](../skills/README.md).
- Abaixo: [knowledge](../knowledge/README.md), [canonicalizer](../canonicalizer/README.md), [persistence](../persistence/README.md).
- Transversal: [guardian](../guardian/README.md), [model_selection](../model_selection/README.md).

## Specs Correspondentes

- [Spec 0014: Context Router, Token Budget Manager e Memory Architecture](../../../specs/framework/0014-context-router-token-budget-memory.md)
- [Spec 0011: Knowledge Hub](../../../specs/framework/0011-knowledge-hub.md)
- [Spec 0013: Persistence Layer](../../../specs/framework/0013-persistence-layer.md)

## Docs Relacionadas

- [Context Router And Token Budget](../../../docs/context-router-token-budget.md)
- [Architecture Map](../../../docs/alignment/architecture-map.md)
- [Current State](../../../docs/alignment/current-state.md)
- [ADR: Context Router, Token Budget Manager e arquitetura de memoria](../../../knowledge/decisions/2026-07-04-context-router-token-budget-memory-architecture.md)
- [ADR: Policy Engine e Guardian Engine](../../../knowledge/decisions/2026-07-04-policy-engine-vs-guardian-engine.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.context import (
    ContextItem,
    ContextRequest,
    DeterministicContextRouter,
    TokenBudget,
)

request = ContextRequest(
    request_id="req-1",
    request_goal="Selecionar contexto mínimo",
    token_budget=TokenBudget(max_input_tokens=1000, reserved_output_tokens=200),
    candidate_items=(
        ContextItem(context_item_id="item-1", source_ref="spec-0014", content="Texto citável."),
    ),
)

package = DeterministicContextRouter().route(request)
```

## Status Atual

Status: `MVP`.

O módulo possui contratos, portas abstratas e implementação determinística mínima. Ele ainda não integra Knowledge Hub, Policy Engine, Guardian Engine, Persistence Layer, Model Selection Engine ou Semantic Index.

## Próximos Passos

- Definir contrato formal com Policy Engine quando existir.
- Definir avaliação Guardian para Context Packages sensíveis.
- Definir candidatos vindos de Knowledge Hub sem acoplar a storage.
- Definir persistência futura de Context Packages e Token Budget Records por `persistence/`.
- Definir Semantic Index apenas após estabilizar contratos e governança.
