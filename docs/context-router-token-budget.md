# Context Router E Token Budget

Links principais: [README principal](../README.md) | [Índice de módulos](architecture/module-index.md) | [Spec 0014](../specs/framework/0014-context-router-token-budget-memory.md)

## Objetivo

Documentar o MVP determinístico do Context Router, do Token Budget Manager e a avaliação Guardian inicial de Context Packages no Vercosa AI Framework.

## Escopo Atual

O módulo `src/vercosa_ai_framework/context/` cria tipos, portas abstratas e implementações determinísticas mínimas para contexto, memória e orçamento de tokens.

Este escopo implementa um MVP funcional sem LLM. Ele trabalha apenas com candidatos explícitos recebidos pelo chamador ou convertidos deterministicamente a partir de registros já disponíveis do Knowledge Hub. Ele não implementa RAG funcional, Semantic Index, embeddings, pgvector, PostgreSQL, chamadas a LLM, runtime ou providers.

O Guardian Engine possui verificação determinística inicial para `ContextPackage` já montado. Essa verificação é chamada explicitamente pelo componente orquestrador ou por testes; ela não muda o fluxo principal do Context Router.

## Componentes

`Context Router` recebe uma `ContextRequest`, considera candidatos explícitos de contexto, deduplica itens por id, hash ou conteúdo, aplica orçamento simples de tokens e produz um `ContextPackage` rastreável.

`Token Budget Manager` estima tokens de forma determinística, reserva tokens de output, calcula orçamento disponível para contexto, decide se um item cabe e também produz resultado agregado para uma sequência de itens.

`MemoryLayer` descreve camadas conceituais de memória sem escolher storage, provider, runtime ou modelo.

`knowledge.context_adapter` converte `KnowledgeDocument` e `KnowledgeSearchResult` em pares `ContextSource` e `ContextItem`. O adaptador apenas mapeia objetos recebidos; ele não consulta store, não lê filesystem, não acessa banco, não faz busca semântica e não chama provider.

`GuardianEngine.evaluate_context_package()` avalia riscos básicos do pacote final sem escolher contexto, sem fazer RAG e sem chamar LLM. As verificações cobrem rastreabilidade, fontes desconhecidas ou pouco confiáveis, warnings, redactions pendentes ou suspeitas, orçamento inconsistente ou excedido, sensibilidade marcada e omission reasons críticos.

## Fluxo MVP

```text
ContextRequest
↓
DeterministicContextRouter
↓
SimpleTokenBudgetManager
↓
ContextPackage
↓
GuardianEngine.evaluate_context_package() quando chamado explicitamente
```

## Entradas

- `ContextRequest` com objetivo, escopo, orçamento e, opcionalmente, candidatos explícitos.
- Lista explícita de `ContextItem` passada para `DeterministicContextRouter.route()` quando o chamador preferir separar request e candidatos.
- `ContextSource` para fontes já conhecidas pelo chamador.
- `ContextItem` para trechos, referências, evidências, instruções ou metadados candidatos.
- Pares `ContextSource` e `ContextItem` convertidos pelo Knowledge Hub a partir de `KnowledgeDocument` ou `KnowledgeSearchResult` já existentes.

## Saídas

- `ContextPackage` com itens selecionados, fontes, citações, estimativa total, reserva de output, redactions agregadas e omissões.
- `TokenBudgetDecision` para itens omitidos por duplicação, citação obrigatória ausente ou limite de tokens.
- `TokenBudgetResult` com estimativa, reserva de output, orçamento disponível, tokens usados, tokens restantes, itens aceitos e itens omitidos.
- `model_requirements` mínimos derivados do pacote, sem selecionar modelo concreto.
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
- Avaliação Guardian determinística, local e sem chamadas externas quando `evaluate_context_package()` receber um pacote.

## Limites Conhecidos

- A estimativa de tokens usa heurística simples por caracteres.
- O roteador só aceita candidatos explícitos; ele não busca documentos nem consulta Knowledge Hub diretamente.
- O Knowledge Hub fornece candidatos, não memória infinita e não pacote final de contexto.
- O MVP não executa busca semântica, reranking, chunking, sumarização nem recuperação automática.
- A integração atual não implementa Semantic Index, embeddings, pgvector, PostgreSQL ou RAG semântico; esses pontos continuam como etapas futuras.
- Itens de evidência sem citação são omitidos; outros itens sem citação podem ser aceitos com warning quando `citation_required=False`.
- Redaction é apenas preservada quando já existe no item; o módulo não executa redaction.
- Policy Engine ainda não é integrado ao fluxo do pacote.
- Guardian Engine avalia `ContextPackage` por chamada explícita, mas o Context Router ainda não chama Guardian automaticamente.
- Semantic Index e cache persistido continuam como trabalho futuro.

## Relação Com Outros Módulos

- `knowledge/` fornece um adaptador determinístico para transformar documentos e resultados textuais já disponíveis em candidatos citáveis. O Context Router continua sem chamar Knowledge Hub diretamente.
- `canonicalizer/` prepara documentos canônicos, mas não é chamado por este MVP.
- `persistence/` poderá persistir pacotes e registros futuros, mas este MVP não persiste nada.
- `model_selection/` poderá receber requisitos de janela de contexto; este MVP apenas prepara metadados.
- `guardian/` avalia Context Packages por verificações determinísticas iniciais, retornando `allow`, `warn`, `require_approval` ou `block` conforme risco. Ele não escolhe contexto, não faz RAG e não chama LLM.

## Status

Status: `MVP`.

O código possui contratos, implementação mínima determinística, integração inicial com candidatos vindos do Knowledge Hub e avaliação Guardian inicial de Context Packages. Ele ainda não representa o fluxo completo de memória governada, Semantic Index, RAG semântico ou integração automática entre roteamento de contexto e enforcement Guardian.
