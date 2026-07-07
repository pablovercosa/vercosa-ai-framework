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
- Pode consumir `TokenBudgetRequirements` opcional, ou mapping equivalente vindo de `ContextPackage.model_requirements`, para considerar janela mínima de contexto já estimada fora do Model Selection.
- Registra compatibilidade determinística entre candidatos e orçamento informado em `SelectionDecision.token_budget_compatibility`.
- Registra warnings determinísticos em `SelectionDecision.token_budget_warnings` quando candidatos não comportam o orçamento informado ou quando o modelo escolhido fica com margem apertada.

## O Que Este Módulo Não Faz

- Não chama providers de LLM.
- Não descobre modelos reais em OpenCode ou APIs externas por conta própria.
- Não calcula billing real.
- Não consulta limites reais de API, quota ou billing.
- Não resolve políticas declarativas e não chama o Policy Engine.
- Não monta `ContextPackage` e não calcula contexto completo.
- Não estima tokens por conta própria; consome apenas requisitos de orçamento já informados pelo chamador.
- Não executa fallback em runtime.
- Não substitui Guardian ou Context Router.
- Não implementa roteamento avançado, ranking semântico, RAG, embeddings ou precificação real.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | `ModelProfile`, `TokenBudgetRequirements`, `SelectionDecision` e erro. |
| `policy.py` | `ModelSelectionPolicy`. |
| `selector.py` | Registry em memória e `ModelSelector`. |
| `__init__.py` | Exportações públicas do módulo. |

## Principais Tipos, Classes E Funções

- `ModelProfile`: metadados normalizados de modelo.
- `TokenBudgetRequirements`: requisitos mínimos de orçamento de tokens consumidos pelo selector sem importar `context/`.
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
- `TokenBudgetRequirements` opcional ou mapping equivalente com campos como `minimum_context_window`, `estimated_context_tokens` e `reserved_output_tokens`.

Saídas:

- `SelectionDecision` com modelo escolhido e fallback quando aplicável.
- `SelectionDecision.policy_sources`, `security_notes`, `requires_review` e `requires_user_approval` podem refletir políticas resolvidas quando fornecidas.
- `SelectionDecision.token_budget_requirements`, `token_budget_compatibility` e `token_budget_warnings` quando orçamento de tokens for informado.

## Dependências Internas

- Depende de tipos declarativos de `policy/` para receber `ResolvedPolicySet` opcional.
- Não depende diretamente de `context/`, runtime, providers ou Guardian Engine.

## Módulos Relacionados

- Acima: [core](../core/README.md), [policy](../policy/README.md).
- Abaixo: [runtime](../runtime/README.md), [agents](../agents/README.md).
- Transversal: [guardian](../guardian/README.md), [providers](../providers/README.md).
- Integração opcional: [context](../context/README.md) pode produzir `ContextPackage.model_requirements`; o chamador pode repassar esses metadados ao Model Selection sem acoplamento direto entre módulos.

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

Integração inicial com orçamento de tokens:

```python
from vercosa_ai_framework.model_selection import ModelProfile, ModelSelectionPolicy, ModelSelector, TokenBudgetRequirements

decision = ModelSelector([ModelProfile(id="local-small", provider="local", context_window=8000)]).select(
    ModelSelectionPolicy(),
    token_budget_requirements=TokenBudgetRequirements(minimum_context_window=6000),
)
```

O `token_budget_requirements` deve ser produzido fora do Model Selection, normalmente a partir de uma estimativa do Token Budget Manager ou de `ContextPackage.model_requirements`. O selector apenas consome os números já calculados.

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

## Integração Inicial Com Token Budget Manager

O Token Budget Manager estima orçamento e uso de tokens no módulo `context/`. O Model Selection Engine não chama esse módulo e não monta `ContextPackage`; ele apenas aceita `TokenBudgetRequirements` opcional ou um mapping compatível repassado pelo chamador.

Comportamento atual:

- sem orçamento informado, a seleção mantém o comportamento anterior;
- `minimum_context_window` define a menor janela de contexto aceitável para candidatos;
- quando `minimum_context_window` não é informado, o selector deriva a janela mínima de `estimated_context_tokens + reserved_output_tokens`;
- candidatos com `context_window` menor que o requisito mínimo ficam inelegíveis de forma determinística;
- candidatos suficientes permanecem elegíveis e seguem o ranking MVP existente;
- `SelectionDecision.token_budget_compatibility` registra se cada modelo do catálogo parece compatível com o requisito informado;
- `SelectionDecision.token_budget_warnings` registra candidatos insuficientes e margem apertada do modelo selecionado;
- não há precificação real por token, consulta de billing real, consulta a provider externo, descoberta de limites reais de contexto, chamada a LLM, rede ou banco.

Limites atuais:

- o selector confia nos metadados locais de `ModelProfile.context_window`;
- não valida limites reais de providers;
- não calcula o conteúdo do contexto;
- não decide quais itens entram no contexto;
- não executa ranking semântico, RAG, embeddings ou compressão de contexto;
- não seleciona modelo dentro do Token Budget Manager.

## Status Atual

Status: `MVP`.

Há seleção em memória por metadados, consumo opcional de políticas resolvidas e consumo opcional de requisitos de orçamento de tokens. Descoberta real, custo real, billing real, registry persistente, Context Router automático e roteamento avançado ainda são futuros.

## Próximos Passos

- Definir Model Registry persistente.
- Integrar descoberta de modelos por RuntimeAdapter sem acoplar a OpenCode.
- Evoluir interpretação de políticas resolvidas sem mover resolução declarativa para o Model Selection.
- Evoluir a integração com Token Budget Manager somente por contratos estáveis, sem mover montagem de contexto para o Model Selection.
