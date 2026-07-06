# Módulo policy

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0005](../../../specs/framework/0005-guardian-engine.md) | [ADR Policy Engine e Guardian Engine](../../../knowledge/decisions/2026-07-04-policy-engine-vs-guardian-engine.md)

## Objetivo

Representar a camada declarativa de políticas do Vercosa AI Framework, separada do Guardian Engine.

## O Que Este Módulo Faz

- Define contratos iniciais para políticas declarativas, escopos, fontes, efeitos, severidades, conflitos e resultados de resolução.
- Fornece a porta `PolicyEngine` para resolução de políticas.
- Fornece `DeterministicPolicyEngine`, uma implementação MVP local, determinística e sem efeitos externos.
- Aceita uma lista explícita de `PolicySet` fornecida pelo chamador.
- Ordena políticas de forma determinística e aplica precedência simples por prioridade.
- Detecta conflitos básicos entre regras habilitadas com o mesmo escopo e chave quando efeitos ou valores divergem.
- Produz `ResolvedPolicySet` e `PolicyResolutionResult` rastreáveis.

## O Que Este Módulo Não Faz

- Não substitui o Guardian Engine.
- Não emite decisões operacionais `allow`, `warn`, `block` ou `require_approval` sobre ações concretas.
- Não executa tools, providers, runtimes, comandos, MCPs, APIs, rede, banco ou filesystem.
- Não chama LLM, OpenCode, Ollama, Gemini, OpenAI, Claude ou qualquer provider externo.
- Não implementa DSL completa de políticas.
- Não implementa parser externo de arquivos de política.
- Não carrega política dinâmica remota.
- Não faz integração profunda com `guardian/` nesta etapa.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | Tipos, enums, dataclasses e porta `PolicyEngine`. |
| `engine.py` | `DeterministicPolicyEngine` MVP para resolução local e determinística. |
| `__init__.py` | Exportações públicas do módulo. |
| `README.md` | Documentação do módulo e limites arquiteturais. |

## Principais Tipos, Classes E Funções

- `PolicyScope`: escopo declarativo da regra.
- `PolicySource`: origem declarada da política.
- `PolicyEffect`: efeito declarativo da regra.
- `PolicySeverity`: severidade associada à regra ou conflito.
- `PolicyRule`: regra declarativa individual.
- `PolicySet`: conjunto nomeado de regras.
- `PolicyConflict`: conflito básico detectado na resolução.
- `ResolvedPolicySet`: conjunto efetivo após precedência.
- `PolicyEvaluationContext`: contexto opcional para filtrar escopos e chaves.
- `PolicyResolutionResult`: resultado auditável da resolução.
- `PolicyEngine`: porta para implementações de resolução declarativa.
- `DeterministicPolicyEngine.resolve()`: resolução MVP sem efeitos externos.

## Entradas E Saídas

Entradas:

- Lista explícita de `PolicySet`.
- `PolicyEvaluationContext` opcional para limitar escopos e chaves solicitadas.

Saídas:

- `PolicyResolutionResult` com `ResolvedPolicySet`, ordem determinística dos conjuntos, conflitos e warnings.

## Dependências Internas

- Nenhuma dependência interna obrigatória além do próprio pacote `policy/`.

## Módulos Relacionados

- Acima: [capabilities](../capabilities/README.md), [agents](../agents/README.md), [workflows](../workflows/README.md), [missions](../missions/README.md).
- Complementar: [guardian](../guardian/README.md).
- Abaixo: [skills](../skills/README.md), [tools](../tools/README.md), [providers](../providers/README.md), [model_selection](../model_selection/README.md), [context](../context/README.md).

## Specs Correspondentes

- [Spec 0005: Guardian Engine](../../../specs/framework/0005-guardian-engine.md)
- [Spec 0009: Capabilities, Skills e Tools](../../../specs/framework/0009-capabilities-skills-tools.md)

## Docs Relacionadas

- [ADR: Policy Engine e Guardian Engine como camadas complementares](../../../knowledge/decisions/2026-07-04-policy-engine-vs-guardian-engine.md)
- [Mapa de arquitetura](../../../docs/alignment/architecture-map.md)
- [Estado atual](../../../docs/alignment/current-state.md)
- [Roadmap](../../../docs/alignment/roadmap.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.policy import (
    DeterministicPolicyEngine,
    PolicyEffect,
    PolicyRule,
    PolicySet,
    PolicySource,
)

policy_set = PolicySet(
    policy_set_id="framework-defaults",
    name="Defaults do framework",
    source=PolicySource.FRAMEWORK_DEFAULT,
    rules=(PolicyRule(rule_id="network.none", key="network", effect=PolicyEffect.DENY),),
)

result = DeterministicPolicyEngine().resolve([policy_set])
```

O resultado é declarativo. A avaliação operacional de uma ação concreta continua pertencendo ao Guardian Engine.

## Status Atual

Status: `MVP`.

O módulo possui contratos iniciais e resolução determinística simples. A integração com Guardian Engine, Context Router, Model Selection Engine, Token Budget Manager e Persistence Layer ainda não foi implementada.

## Próximos Passos

- Definir uma Spec própria ou atualização explícita de Spec para Policy Engine quando a superfície crescer além do MVP.
- Definir formato persistível de `Policy Resolution Record` pela Persistence Layer.
- Integrar políticas resolvidas ao Guardian Engine sem fundir responsabilidades.
- Evoluir composição de políticas sem introduzir DSL complexa antes de estabilizar contratos.
