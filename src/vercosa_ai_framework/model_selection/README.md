# Módulo model_selection

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0002](../../../specs/framework/0002-model-selection-engine.md)

## Objetivo

Selecionar modelos por política, disponibilidade e atributos declarados, sem hardcode de provider ou runtime.

## O Que Este Módulo Faz

- Define perfis de modelo e decisões de seleção.
- Implementa policy mínima de seleção.
- Mantém registry em memória.
- Seleciona modelo compatível e retorna justificativa auditável.
- Pode consumir `ResolvedPolicySet` opcional já produzido pelo Policy Engine para registrar warnings, aprovação requerida e exclusões determinísticas de candidatos.

## O Que Este Módulo Não Faz

- Não chama providers de LLM.
- Não descobre modelos reais em OpenCode ou APIs externas por conta própria.
- Não calcula billing real.
- Não consulta limites reais de API, quota ou billing.
- Não resolve políticas declarativas e não chama o Policy Engine.
- Não executa fallback em runtime.
- Não substitui Guardian ou Context Router.
- Não implementa roteamento avançado, ranking semântico, RAG, embeddings ou precificação real.

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
- `ResolvedPolicySet`: entrada opcional consumida sem resolução local de políticas.

## Entradas E Saídas

Entradas:

- `ModelSelectionPolicy` e catálogo de `ModelProfile`.
- `ResolvedPolicySet` opcional já resolvido pelo Policy Engine.

Saídas:

- `SelectionDecision` com modelo escolhido e fallback quando aplicável.
- `SelectionDecision.policy_sources`, `security_notes`, `requires_review` e `requires_user_approval` podem refletir políticas resolvidas quando fornecidas.

## Dependências Internas

- Depende de tipos declarativos de `policy/` para receber `ResolvedPolicySet` opcional.
- Não depende diretamente de runtime, providers ou Guardian Engine.

## Módulos Relacionados

- Acima: [core](../core/README.md), [policy](../policy/README.md).
- Abaixo: [runtime](../runtime/README.md), [agents](../agents/README.md).
- Transversal: [guardian](../guardian/README.md), [providers](../providers/README.md).

## Specs Correspondentes

- [Spec 0002: Model Selection Engine](../../../specs/framework/0002-model-selection-engine.md)

## Docs Relacionadas

- [Mapa de arquitetura](../../../docs/alignment/architecture-map.md)
- [Estado atual](../../../docs/alignment/current-state.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.model_selection import ModelProfile, ModelSelector

selector = ModelSelector([ModelProfile(id="local-small", provider="local")])
```

Integração inicial com política resolvida:

```python
from vercosa_ai_framework.model_selection import ModelProfile, ModelSelectionPolicy, ModelSelector

decision = ModelSelector([ModelProfile(id="local-small", provider="local")]).select(
    ModelSelectionPolicy(),
    resolved_policy_set=resolved_policy_set,
)
```

O `resolved_policy_set` deve ser produzido fora do Model Selection. O selector apenas consome a estrutura já resolvida.

## Integração Inicial Com Policy Engine

O contrato atual permite que o chamador entregue um `ResolvedPolicySet` opcional ao Model Selection Engine.

Limites atuais:

- `allow` não força escolha de modelo por si só;
- `warn` é refletido em `security_notes` e `policy_sources`;
- `require_approval` marca `requires_review` e `requires_user_approval` de forma rastreável;
- `deny` exclui candidatos somente quando a regra tem alvo determinístico, como `model`, `model_id`, `provider`, `runtime`, `pricing_class`, `local`, `free`, `paid` ou `target_refs` compatível;
- conflitos são refletidos em `security_notes` e `policy_sources`; conflitos `high` ou `critical` exigem aprovação;
- não há chamada a provider externo, LLM, OpenCode, Ollama, OpenAI, Gemini, Claude, MCP, rede ou banco;
- não há precificação real, consulta de billing real, rate limit real, ranking semântico, RAG ou embeddings.

## Status Atual

Status: `MVP`.

Há seleção em memória por metadados e consumo opcional de políticas resolvidas, mas descoberta real, custo real, billing real, registry persistente, Context Router e roteamento avançado ainda são futuros.

## Próximos Passos

- Definir Model Registry persistente.
- Integrar descoberta de modelos por RuntimeAdapter sem acoplar a OpenCode.
- Evoluir interpretação de políticas resolvidas sem mover resolução declarativa para o Model Selection.
- Integrar Token Budget Manager em missão separada e sem RAG ou embeddings.
