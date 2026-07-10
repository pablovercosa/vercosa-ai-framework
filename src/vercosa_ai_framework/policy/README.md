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
- Fornece `ResolvedPolicySet` para consumidores como o Guardian Engine quando o chamador decidir passar políticas resolvidas adiante.
- Fornece `ResolvedPolicySet` para o Context Router quando o chamador quiser que o pacote de contexto considere políticas já resolvidas.
- Fornece `ResolvedPolicySet` para o Model Selection Engine quando o chamador quiser que a seleção considere políticas já resolvidas.
- Pode ter `PolicyResolutionResult` transformado em evento auditável por helper opcional do módulo `audit/`, sem dependência obrigatória do Policy Engine para um event log.

## O Que Este Módulo Não Faz

- Não substitui o Guardian Engine.
- Não emite decisões operacionais `allow`, `warn`, `block` ou `require_approval` sobre ações concretas.
- Não executa tools, providers, runtimes, comandos, MCPs, APIs, rede, banco ou filesystem.
- Não chama LLM, OpenCode, Ollama, Gemini, OpenAI, Claude ou qualquer provider externo.
- Não implementa DSL completa de políticas.
- Não implementa parser externo de arquivos de política.
- Não carrega política dinâmica remota.
- Não chama `guardian/` e não aplica enforcement operacional.
- Não chama `context/` e não monta `ContextPackage`.
- Não chama `model_selection/` e não seleciona, ranqueia ou descobre modelos.
- Não transforma `ResolvedPolicySet` em decisão Guardian por conta própria.
- Não registra eventos auditáveis automaticamente e não persiste resultados.

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

O `ResolvedPolicySet` pode ser passado pelo chamador ao Guardian Engine, ao Context Router ou ao Model Selection Engine. Essas integrações são iniciais e unidirecionais: Policy Engine resolve políticas declarativas; Guardian Engine avalia ação concreta; Context Router monta pacote de contexto a partir de candidatos explícitos; Model Selection seleciona modelos a partir de catálogo local e pode considerar efeitos simples já resolvidos.

## Dependências Internas

- Nenhuma dependência interna obrigatória além do próprio pacote `policy/`.
- O módulo `policy/` não importa `guardian/`.
- O módulo `policy/` não importa `context/`.
- O módulo `policy/` não importa `model_selection/`.

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

## Integração Opcional Com Audit/Event Log

O módulo `audit/` fornece `policy_resolution_event()` e `record_policy_resolution_event()` para transformar um `PolicyResolutionResult` já produzido em evento auditável estruturado. A chamada é responsabilidade do orquestrador ou do chamador.

O evento pode registrar categoria `policy`, quantidade de policy sets considerados, quantidade de políticas resolvidas, conflitos, warnings, refs de `deny` e refs de `require_approval`. Os helpers priorizam refs, contadores e metadados seguros, sem registrar prompts completos, segredos ou conteúdo bruto por padrão.

Essa integração é opcional, em memória quando usada com `InMemoryEventLog` ou em JSONL local quando usada explicitamente com `JsonlAuditEventLog`, sem persistência externa, sem observabilidade externa e sem alterar a assinatura do `PolicyEngine.resolve()`.

## Integração Inicial Com Guardian Engine

O contrato atual permite que um chamador resolva políticas com `DeterministicPolicyEngine` e entregue o `ResolvedPolicySet` ao contexto de avaliação do Guardian Engine.

Limites atuais:

- `allow` não bloqueia por si só.
- `warn` pode elevar a decisão Guardian para `warn`.
- `require_approval` pode elevar a decisão Guardian para `require_approval`.
- `deny` pode elevar a decisão Guardian para `block`.
- conflitos de política resolvida podem gerar `warn` ou `require_approval`, conforme severidade.
- efeitos como `set_limit` e `prefer` continuam declarativos nesta etapa e não viram enforcement operacional automático.

## Integração Inicial Com Context Router

O contrato atual permite que um chamador resolva políticas com `DeterministicPolicyEngine` e entregue o `ResolvedPolicySet` em `ContextRequest.resolved_policy_set`.

Limites atuais:

- o Context Router consome políticas resolvidas, mas não chama o Policy Engine;
- `allow` não altera seleção de contexto por si só;
- `warn` é refletido em warnings e refs de política do `ContextPackage`;
- `require_approval` é refletido em warnings e metadados rastreáveis;
- `deny` só causa omissão quando há alvo determinístico para item, fonte, tipo ou sensibilidade;
- conflitos são registrados como warning ou aprovação requerida conforme severidade;
- não há DSL, parser, RAG semântico, embeddings, pgvector, banco, provider externo, chamada de LLM ou rede.

## Integração Inicial Com Model Selection

O contrato atual permite que um chamador resolva políticas com `DeterministicPolicyEngine` e entregue o `ResolvedPolicySet` ao `ModelSelector.select()` ou ao helper `select_model()`.

Limites atuais:

- o Model Selection consome políticas resolvidas, mas não chama o Policy Engine;
- o Policy Engine não chama Model Selection, não descobre modelos e não ranqueia candidatos;
- `allow` não força escolha de modelo por si só;
- `warn` é refletido em notas e fontes de política da decisão de seleção;
- `require_approval` pode marcar revisão ou aprovação requerida;
- `deny` só exclui candidato quando há alvo determinístico, como modelo, provider, runtime, classe de preço ou flags declaradas do perfil;
- conflitos são registrados de forma determinística e conflitos `high` ou `critical` exigem aprovação;
- não há precificação real, consulta de billing real, chamada a provider externo, OpenCode, Ollama, OpenAI, Gemini, Claude, MCP, rede, banco, RAG, embeddings ou ranking semântico.

## Status Atual

Status: `MVP`.

O módulo possui contratos iniciais e resolução determinística simples. Existem integrações iniciais e unidirecionais com Guardian Engine, Context Router e Model Selection Engine via `ResolvedPolicySet` opcional. Resultados de resolução também podem ser convertidos em eventos auditáveis por helper opcional de `audit/`. A integração com Token Budget Manager e Persistence Layer ainda não foi implementada.

## Próximos Passos

- Definir uma Spec própria ou atualização explícita de Spec para Policy Engine quando a superfície crescer além do MVP.
- Definir formato persistível de `Policy Resolution Record` pela Persistence Layer.
- Evoluir a integração com Guardian Engine sem fundir responsabilidades.
- Evoluir a integração com Context Router sem permitir que Policy Engine monte contexto ou que Context Router resolva políticas.
- Evoluir a integração com Model Selection sem permitir que Policy Engine selecione modelos ou que Model Selection resolva políticas.
- Registrar resoluções de política em fluxos orquestrados quando Mission Runner ou Worker tiverem contrato explícito de auditoria.
- Evoluir composição de políticas sem introduzir DSL complexa antes de estabilizar contratos.
