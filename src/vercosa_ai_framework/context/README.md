# Módulo context

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0014](../../../specs/framework/0014-context-router-token-budget-memory.md)

## Objetivo

Definir contratos e MVP determinístico para Context Router, Token Budget Manager, Context Package e camadas conceituais de memória.

## O Que Este Módulo Faz

- Define tipos conceituais para fontes, itens, citações, redactions, omissões, risco, budgets e camadas de memória.
- Define a porta abstrata `ContextRouter`.
- Implementa `DeterministicContextRouter` para candidatos explícitos de contexto.
- Define a porta abstrata `TokenBudgetManager`.
- Implementa `SimpleTokenBudgetManager` com estimativa determinística simples.
- Deduplica candidatos por id, hash ou conteúdo.
- Respeita limite básico de tokens estimados.
- Reserva tokens de output antes de preencher contexto.
- Preserva citações e redactions já presentes nos itens.
- Registra omissões por duplicação, orçamento insuficiente ou citação obrigatória ausente.
- Gera warnings determinísticos para itens citáveis sem citação quando citação não for obrigatória.
- Produz `ContextPackage` rastreável.
- Produz `ContextPackage.model_requirements` com requisitos mínimos derivados do orçamento estimado, para que outros módulos possam consumir metadados sem o Context Router escolher modelo.
- Pode receber um `ResolvedPolicySet` opcional já produzido pelo Policy Engine e considerar efeitos simples de forma determinística.
- Registra refs de políticas resolvidas no `ContextPackage` quando elas forem fornecidas pelo chamador.
- Reflete políticas `warn`, `require_approval` e conflitos em warnings e metadados rastreáveis.
- Omite itens por política `deny` somente quando a regra possui alvo claro e determinístico para o item ou fonte.
- Recebe normalmente candidatos `ContextItem` originados do Knowledge Hub quando eles já foram convertidos por adaptador externo ao roteador.
- Produz pacotes que podem ser avaliados pelo Guardian Engine por chamada explícita do componente orquestrador.
- Pode ter `ContextPackage` transformado em evento auditável por helper opcional do módulo `audit/`, sem dependência obrigatória do Context Router para um event log.

## O Que Este Módulo Não Faz

- Não implementa Semantic Index.
- Não gera embeddings.
- Não usa PostgreSQL, pgvector, SQLite ou qualquer banco.
- Não implementa RAG funcional.
- Não acessa filesystem.
- Não consulta Knowledge Hub diretamente; o Knowledge Hub fornece candidatos por adaptador determinístico.
- Não chama providers, LLMs, APIs, MCPs, OpenCode, Ollama, Gemini, OpenAI, Claude ou runtimes.
- Não escolhe modelos concretos.
- Não ranqueia modelos e não decide se um modelo concreto deve ser usado.
- Não executa redaction; apenas preserva registros já recebidos.
- Não avalia risco operacional do pacote final; essa responsabilidade pertence ao Guardian Engine.
- Não resolve políticas; políticas precisam chegar como `ResolvedPolicySet` opcional já resolvido pelo Policy Engine ou como refs simples.
- Não registra eventos auditáveis automaticamente e não persiste pacotes de contexto.
- Não implementa DSL, parser de política ou carregamento de políticas.
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
- `TokenBudgetResult`: resultado agregado com estimativa, reserva, tokens usados, tokens restantes, itens aceitos e omitidos.
- `MemoryLayer`: descrição storage agnostic de uma camada de memória.
- `ContextRouter`: contrato abstrato do roteador.
- `DeterministicContextRouter`: roteador MVP sem efeitos externos.
- `TokenBudgetManager`: contrato abstrato de orçamento.
- `SimpleTokenBudgetManager`: estimador MVP sem chamadas externas.

## Entradas E Saídas

Entradas:

- `ContextRequest` com objetivo, escopo, orçamento e candidatos explícitos.
- `ResolvedPolicySet` opcional em `ContextRequest.resolved_policy_set`, já produzido por `policy/` quando o chamador quiser aplicar a integração inicial.
- Lista explícita de `ContextItem` passada para `DeterministicContextRouter.route()` quando o chamador não quiser armazenar candidatos no request.
- `ContextSource` e `ContextItem` criados por chamadores autorizados.
- `ContextSource` e `ContextItem` produzidos por `knowledge_document_to_context_candidate()` ou `knowledge_search_result_to_context_candidate()` quando a origem for o Knowledge Hub.

Saídas:

- `ContextPackage` com itens, fontes, citações, estimativas, redactions e omissões.
- `ContextPackage.model_requirements` com `minimum_context_window`, `estimated_context_tokens` e `reserved_output_tokens` derivados do pacote montado.
- `ContextPackage.policy_refs`, `warnings` e `metadata` com rastreabilidade de políticas resolvidas quando fornecidas.
- `TokenBudgetDecision` para itens incluídos ou omitidos.
- `TokenBudgetResult` produzido pelo `SimpleTokenBudgetManager` para avaliação agregada de orçamento.

## Integração Inicial Com Policy Engine

O Policy Engine resolve políticas declarativas e produz `ResolvedPolicySet`. O Context Router não chama o Policy Engine e não resolve precedência, conflitos ou DSL. Quando o chamador passa `ContextRequest.resolved_policy_set`, o roteador apenas consome esse conjunto já resolvido.

Comportamento atual:

- `allow` não bloqueia nem seleciona contexto por si só.
- `warn` gera warning rastreável no `ContextPackage`.
- `require_approval` gera warning e metadados `requires_approval` e `approval_policy_refs`.
- `deny` omite item com `policy_denied` somente quando `target_refs` ou valor simples apontam de forma determinística para `context_item_id`, `source_ref`, tipo de item ou sensibilidade.
- `deny` sem alvo claro é registrado em `metadata["blocked_policy_refs"]`, sem omissão ambígua.
- conflitos de política geram warning ou marcação de aprovação conforme severidade.

Essa integração é inicial, local e determinística. Ela não implementa RAG semântico, embeddings, pgvector, PostgreSQL, provider externo, LLM, runtime, rede ou banco.

## Integração Opcional Com Audit/Event Log

O módulo `audit/` fornece `context_package_event()` e `record_context_package_event()` para transformar um `ContextPackage` já montado em evento auditável estruturado. A chamada é explícita e deve ser feita pelo orquestrador ou pelo chamador que possui um `EventLog`.

O evento pode registrar categoria `context`, quantidade de candidatos quando informada, itens selecionados, itens omitidos, uso estimado de tokens, reserva de output, warnings, motivos agregados de omissão, refs de políticas, refs Guardian e sinal de `require_approval`. O evento não registra conteúdo integral dos itens, prompts completos, segredos ou credenciais por padrão.

Essa integração é opcional, em memória quando usada com `InMemoryEventLog` ou em JSONL local quando usada explicitamente com `JsonlAuditEventLog`, sem persistência externa, sem observabilidade externa e sem alterar o comportamento de `DeterministicContextRouter.route()`.

## Dependências Internas

- Depende apenas dos tipos declarativos de `policy/` para aceitar `ResolvedPolicySet` opcional.
- Não importa `guardian/` e não chama Guardian Engine automaticamente.
- Não importa `model_selection/` e não chama Model Selection Engine.
- A integração com `knowledge/` é feita no módulo `knowledge`, por adaptador que produz tipos de `context/` sem fazer o roteador buscar documentos.

## Módulos Relacionados

- Acima: [agents](../agents/README.md), [capabilities](../capabilities/README.md), [skills](../skills/README.md).
- Abaixo: [knowledge](../knowledge/README.md), [canonicalizer](../canonicalizer/README.md), [persistence](../persistence/README.md).
- Transversal: [guardian](../guardian/README.md), [model_selection](../model_selection/README.md).
- `policy/` resolve políticas declarativas antes do roteamento quando o chamador solicitar essa etapa.
- `guardian/` avalia riscos determinísticos básicos de `ContextPackage` quando chamado explicitamente. O Context Router não chama Guardian automaticamente nesta fase.
- `model_selection/` pode consumir requisitos de orçamento repassados pelo chamador, mas o Context Router não seleciona modelo e não chama esse módulo.

## Specs Correspondentes

- [Spec 0014: Context Router, Token Budget Manager e Memory Architecture](../../../specs/framework/0014-context-router-token-budget-memory.md)
- [Spec 0011: Knowledge Hub](../../../specs/framework/0011-knowledge-hub.md)
- [Spec 0013: Persistence Layer](../../../specs/framework/0013-persistence-layer.md)

## Docs Relacionadas

- [Context Router e Token Budget](../../../docs/context-router-token-budget.md)
- [Mapa de arquitetura](../../../docs/alignment/architecture-map.md)
- [Estado atual](../../../docs/alignment/current-state.md)
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
)

candidates = (
    ContextItem(context_item_id="item-1", source_ref="spec-0014", content="Texto candidato."),
)

package = DeterministicContextRouter().route(request, candidates=candidates)
```

O exemplo acima não executa busca, RAG, embeddings, banco, provider ou runtime. Os candidatos já precisam ter sido preparados pelo chamador.

## Integração Inicial Com Model Selection

O Token Budget Manager estima tokens e o Context Router registra requisitos mínimos em `ContextPackage.model_requirements`. Esses metadados podem ser repassados pelo chamador ao Model Selection Engine como entrada opcional.

Limites atuais:

- o Context Router não importa `model_selection/`;
- o Context Router não seleciona modelos;
- o Token Budget Manager não ranqueia candidatos de modelo;
- o Model Selection não monta `ContextPackage`;
- não há consulta de limites reais de providers;
- não há billing real, precificação real por token, chamada a LLM, rede, banco, RAG ou embeddings.

## Status Atual

Status: `MVP`.

O módulo possui contratos, portas abstratas e implementação determinística mínima. Ele aceita candidatos convertidos do Knowledge Hub, pode consumir `ResolvedPolicySet` opcional já resolvido pelo Policy Engine e expõe requisitos mínimos de orçamento em `ContextPackage.model_requirements`. `ContextPackage` pode ser convertido em evento auditável por helper opcional de `audit/`. Ele não consulta Knowledge Hub diretamente e não integra automaticamente Guardian Engine, Persistence Layer, Model Selection Engine ou Semantic Index.

Limitações atuais:

- Não há RAG real.
- Não há embeddings.
- Não há pgvector ou PostgreSQL.
- Não há recuperação automática de documentos.
- Não há busca semântica.
- Knowledge Hub fornece candidatos explícitos; ele não representa memória infinita.
- Não há memória infinita.
- Não há chamadas externas.
- A integração com Policy Engine é limitada a efeitos simples já resolvidos; não há DSL, parser ou resolução de políticas dentro do Context Router.
- A avaliação Guardian de Context Packages existe no módulo `guardian/`, mas depende de chamada explícita e não muda a montagem determinística do pacote.
- A integração com Model Selection é indireta: somente o chamador repassa metadados de orçamento, se desejar.
- A integração com Audit/Event Log é indireta: somente o chamador cria ou registra eventos, se desejar.

## Próximos Passos

- Evoluir contrato formal com Policy Engine somente quando novas Specs ou ADRs aprovarem regras mais ricas de contexto.
- Integrar avaliação Guardian para Context Packages sensíveis ao fluxo orquestrado quando houver contrato de execução aprovado.
- Expandir o contrato de candidatos vindos de Knowledge Hub somente após novas Specs ou ADRs para ranking, chunking e governança adicional.
- Definir persistência futura de Context Packages e Token Budget Records por `persistence/`.
- Registrar eventos de contexto no Mission Runner, Worker ou Provider Gateway apenas quando houver contrato de auditoria aprovado para esses fluxos.
- Definir Semantic Index apenas após estabilizar contratos e governança.
- Evoluir o contrato de requisitos para Model Selection sem criar import circular entre `context/` e `model_selection/`.
