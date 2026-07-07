# Context Router E Token Budget

Links principais: [README principal](../README.md) | [Índice de módulos](architecture/module-index.md) | [Spec 0014](../specs/framework/0014-context-router-token-budget-memory.md)

## Objetivo

Documentar o MVP determinístico do Context Router, do Token Budget Manager, a avaliação Guardian inicial de Context Packages e a integração inicial de orçamento com Model Selection no Vercosa AI Framework.

## Escopo Atual

O módulo `src/vercosa_ai_framework/context/` cria tipos, portas abstratas e implementações determinísticas mínimas para contexto, memória e orçamento de tokens.

Este escopo implementa um MVP funcional sem LLM. Ele trabalha apenas com candidatos explícitos recebidos pelo chamador ou convertidos deterministicamente a partir de registros já disponíveis do Knowledge Hub. Ele não implementa RAG funcional, Semantic Index, embeddings, pgvector, PostgreSQL, chamadas a LLM, runtime ou providers.

O Context Router também pode consumir um `ResolvedPolicySet` opcional já produzido pelo Policy Engine. Essa integração é inicial: o Policy Engine resolve políticas declarativas; o Context Router apenas considera efeitos simples já resolvidos ao montar o pacote. O roteador não chama o Policy Engine, não resolve política e não implementa DSL.

O `ContextPackage` expõe `model_requirements` mínimos derivados do orçamento estimado. Esses metadados podem ser repassados pelo chamador ao Model Selection Engine. Essa integração é inicial e indireta: o Context Router não chama Model Selection, e o Model Selection não monta contexto.

O Guardian Engine possui verificação determinística inicial para `ContextPackage` já montado. Essa verificação é chamada explicitamente pelo componente orquestrador ou por testes; ela não muda o fluxo principal do Context Router.

## Componentes

`Context Router` recebe uma `ContextRequest`, considera candidatos explícitos de contexto, deduplica itens por id, hash ou conteúdo, aplica orçamento simples de tokens e produz um `ContextPackage` rastreável.

Quando `ContextRequest.resolved_policy_set` é fornecido, o roteador registra refs de políticas resolvidas, reflete `warn`, `require_approval` e conflitos em warnings/metadados e pode omitir item por `deny` apenas quando a regra possui alvo determinístico. Políticas `allow` não alteram seleção de contexto por si só.

`Token Budget Manager` estima tokens de forma determinística, reserva tokens de output, calcula orçamento disponível para contexto, decide se um item cabe e também produz resultado agregado para uma sequência de itens.

`Model Selection Engine` pode consumir requisitos de orçamento já calculados fora dele, como `minimum_context_window`, `estimated_context_tokens` e `reserved_output_tokens`, para filtrar candidatos com janela de contexto insuficiente e registrar warnings determinísticos. Ele não calcula billing real e não consulta limites reais de providers.

`MemoryLayer` descreve camadas conceituais de memória sem escolher storage, provider, runtime ou modelo.

`knowledge.context_adapter` converte `KnowledgeDocument` e `KnowledgeSearchResult` em pares `ContextSource` e `ContextItem`. O adaptador apenas mapeia objetos recebidos; ele não consulta store, não lê filesystem, não acessa banco, não faz busca semântica e não chama provider.

`GuardianEngine.evaluate_context_package()` avalia riscos básicos do pacote final sem escolher contexto, sem fazer RAG e sem chamar LLM. As verificações cobrem rastreabilidade, fontes desconhecidas ou pouco confiáveis, warnings, redactions pendentes ou suspeitas, orçamento inconsistente ou excedido, sensibilidade marcada e omission reasons críticos.

## Fluxo MVP

```text
ContextRequest
↓
ResolvedPolicySet opcional já resolvido pelo Policy Engine
↓
DeterministicContextRouter
↓
SimpleTokenBudgetManager
↓
ContextPackage
↓
GuardianEngine.evaluate_context_package() quando chamado explicitamente

ContextPackage.model_requirements
↓
Model Selection Engine quando o chamador repassar os requisitos de orçamento
```

## Entradas

- `ContextRequest` com objetivo, escopo, orçamento e, opcionalmente, candidatos explícitos.
- `ResolvedPolicySet` opcional em `ContextRequest.resolved_policy_set`, já resolvido pelo Policy Engine.
- Lista explícita de `ContextItem` passada para `DeterministicContextRouter.route()` quando o chamador preferir separar request e candidatos.
- `ContextSource` para fontes já conhecidas pelo chamador.
- `ContextItem` para trechos, referências, evidências, instruções ou metadados candidatos.
- Pares `ContextSource` e `ContextItem` convertidos pelo Knowledge Hub a partir de `KnowledgeDocument` ou `KnowledgeSearchResult` já existentes.

## Saídas

- `ContextPackage` com itens selecionados, fontes, citações, estimativa total, reserva de output, redactions agregadas e omissões.
- `ContextPackage` com `policy_refs`, `warnings` e metadados de aprovação ou bloqueio quando políticas resolvidas forem fornecidas.
- `TokenBudgetDecision` para itens omitidos por duplicação, citação obrigatória ausente ou limite de tokens.
- `TokenBudgetResult` com estimativa, reserva de output, orçamento disponível, tokens usados, tokens restantes, itens aceitos e itens omitidos.
- `model_requirements` mínimos derivados do pacote, sem selecionar modelo concreto e sem consultar providers.
- `GuardianDecision` quando o pacote for enviado ao Guardian por chamada explícita.

## Garantias Do MVP

- Determinístico para o mesmo request e mesmos candidatos.
- Sem chamadas externas.
- Sem leitura ou escrita em banco.
- Sem acesso a filesystem.
- Sem embeddings.
- Sem RAG real.
- Sem provider, runtime, OpenCode, Ollama, Gemini, OpenAI, Claude ou API externa.
- Sem promessa de memória infinita.
- Mesmo resultado para o mesmo request, candidatos, políticas e orçamento.
- Preservação de citações e redactions já presentes nos itens selecionados.
- Conversão determinística de registros do Knowledge Hub em candidatos de contexto, preservando id, título, referência, tipo de fonte, hash e citações ou referência rastreável mínima.
- Registro de omissões no `ContextPackage`.
- Exposição de requisitos mínimos de orçamento para consumo opcional por Model Selection sem acoplamento circular.
- Integração opcional com `ResolvedPolicySet` sem chamada a Policy Engine, Guardian Engine, LLM, provider, rede ou banco.
- Avaliação Guardian determinística, local e sem chamadas externas quando `evaluate_context_package()` receber um pacote.

## Limites Conhecidos

- A estimativa de tokens usa heurística simples por caracteres.
- O roteador só aceita candidatos explícitos; ele não busca documentos nem consulta Knowledge Hub diretamente.
- O Knowledge Hub fornece candidatos, não memória infinita e não pacote final de contexto.
- O MVP não executa busca semântica, reranking, chunking, sumarização nem recuperação automática.
- A integração atual não implementa Semantic Index, embeddings, pgvector, PostgreSQL ou RAG semântico; esses pontos continuam como etapas futuras.
- Itens de evidência sem citação são omitidos; outros itens sem citação podem ser aceitos com warning quando `citation_required=False`.
- Redaction é apenas preservada quando já existe no item; o módulo não executa redaction.
- A integração com Policy Engine é inicial e limitada a `ResolvedPolicySet` opcional já resolvido.
- O Context Router não resolve políticas, não interpreta DSL, não carrega arquivos de política e não aplica enforcement operacional amplo.
- Guardian Engine avalia `ContextPackage` por chamada explícita, mas o Context Router ainda não chama Guardian automaticamente.
- Model Selection pode consumir requisitos de orçamento repassados pelo chamador, mas o Context Router e o Token Budget Manager não selecionam modelos.
- Não há precificação real por token, consulta de billing real ou consulta real de limites de contexto de providers.
- Semantic Index e cache persistido continuam como trabalho futuro.

## Relação Com Outros Módulos

- `knowledge/` fornece um adaptador determinístico para transformar documentos e resultados textuais já disponíveis em candidatos citáveis. O Context Router continua sem chamar Knowledge Hub diretamente.
- `policy/` resolve políticas declarativas e pode entregar `ResolvedPolicySet` ao chamador. O Context Router consome esse conjunto opcional sem chamar `policy/` em tempo de roteamento.
- `canonicalizer/` prepara documentos canônicos, mas não é chamado por este MVP.
- `persistence/` poderá persistir pacotes e registros futuros, mas este MVP não persiste nada.
- `model_selection/` pode receber requisitos de janela de contexto como entrada opcional repassada pelo chamador; este MVP apenas prepara metadados e não cria chamada direta entre módulos.
- `guardian/` avalia Context Packages por verificações determinísticas iniciais, retornando `allow`, `warn`, `require_approval` ou `block` conforme risco. Ele não escolhe contexto, não faz RAG e não chama LLM.

## Status

Status: `MVP`.

O código possui contratos, implementação mínima determinística, integração inicial com candidatos vindos do Knowledge Hub, consumo opcional de `ResolvedPolicySet`, avaliação Guardian inicial de Context Packages e metadados de orçamento consumíveis pelo Model Selection quando o chamador repassar essa entrada. Ele ainda não representa o fluxo completo de memória governada, Semantic Index, RAG semântico, integração automática entre roteamento de contexto e enforcement Guardian ou consulta real de limites e custos de providers.
