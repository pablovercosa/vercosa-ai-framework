# Context Router And Token Budget

Links principais: [README principal](../README.md) | [Índice de módulos](architecture/module-index.md) | [Spec 0014](../specs/framework/0014-context-router-token-budget-memory.md)

## Objetivo

Documentar o contrato inicial do Context Router e do Token Budget Manager no Vercosa AI Framework.

## Escopo Atual

O módulo `src/vercosa_ai_framework/context/` cria tipos, portas abstratas e implementações determinísticas mínimas para contexto, memória e orçamento de tokens.

Este escopo implementa contratos iniciais autorizados pela missão atual. Ele não implementa RAG funcional, Semantic Index, embeddings, pgvector, PostgreSQL, chamadas a LLM, runtime ou providers.

## Componentes

`Context Router` recebe uma `ContextRequest`, considera candidatos explícitos de contexto, deduplica itens por hash ou id, aplica orçamento simples de tokens e produz um `ContextPackage` rastreável.

`Token Budget Manager` estima tokens de forma determinística, reserva tokens de output, calcula orçamento disponível para contexto e decide se um item cabe ou deve ser omitido.

`MemoryLayer` descreve camadas conceituais de memória sem escolher storage, provider, runtime ou modelo.

## Fluxo MVP

```text
ContextRequest
↓
DeterministicContextRouter
↓
SimpleTokenBudgetManager
↓
ContextPackage
```

## Entradas

- `ContextRequest` com objetivo, escopo, orçamento e candidatos explícitos.
- `ContextSource` para fontes já conhecidas pelo chamador.
- `ContextItem` para trechos, referências, evidências, instruções ou metadados candidatos.

## Saídas

- `ContextPackage` com itens selecionados, fontes, citações, estimativa total, reserva de output, redactions agregadas e omissões.
- `TokenBudgetDecision` para itens omitidos por duplicação ou limite de tokens.
- `model_requirements` mínimos derivados do pacote, sem selecionar modelo concreto.

## Garantias Do MVP

- Determinístico para o mesmo request e mesmos candidatos.
- Sem chamadas externas.
- Sem leitura ou escrita em banco.
- Sem acesso a filesystem.
- Sem embeddings.
- Sem RAG real.
- Sem provider, runtime, OpenCode, Ollama, Gemini, OpenAI, Claude ou API externa.
- Sem promessa de memória infinita.

## Limites Conhecidos

- A estimativa de tokens usa heurística simples por caracteres.
- O roteador só aceita candidatos explícitos; ele não busca documentos.
- Redaction é apenas preservada quando já existe no item; o módulo não executa redaction.
- Policy Engine e Guardian Engine ainda não são integrados ao fluxo do pacote.
- Semantic Index e cache persistido continuam como trabalho futuro.

## Relação Com Outros Módulos

- `knowledge/` poderá fornecer candidatos citáveis no futuro; hoje o Context Router não chama Knowledge Hub.
- `canonicalizer/` prepara documentos canônicos, mas não é chamado por este MVP.
- `persistence/` poderá persistir pacotes e registros futuros, mas este MVP não persiste nada.
- `model_selection/` poderá receber requisitos de janela de contexto; este MVP apenas prepara metadados.
- `guardian/` poderá avaliar Context Packages sensíveis; este MVP apenas preserva refs recebidas.

## Status

Status: `MVP`.

O código possui contratos e implementação mínima determinística, com testes de contrato. Ele ainda não representa o fluxo completo de memória governada ou RAG.
