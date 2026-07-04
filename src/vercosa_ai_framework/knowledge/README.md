# Módulo knowledge

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0011](../../../specs/framework/0011-knowledge-hub.md)

## Objetivo

Representar documentos de conhecimento e busca textual determinística no MVP do Knowledge Hub.

## O Que Este Módulo Faz

- Define domínios, fontes, documentos, queries e resultados de conhecimento.
- Lê Markdown e frontmatter simples.
- Detecta warnings básicos de prompt injection em documentos.
- Mantém store em memória.
- Executa busca textual determinística.
- Converte `KnowledgeDocument` e `KnowledgeSearchResult` em candidatos `ContextSource` e `ContextItem` para o Context Router.

## O Que Este Módulo Não Faz

- Não implementa Semantic Index com embeddings.
- Não usa PostgreSQL, pgvector ou Ollama diretamente.
- Não decide contexto final para prompts; isso pertence ao Context Router.
- Não monta `ContextPackage`.
- Não fornece memória infinita; fornece documentos e resultados candidatos sob contratos explícitos.
- Não processa binários diretamente.
- Não substitui Canonicalizer.
- Não chama providers, LLMs, APIs, MCPs, bancos, pgvector, embeddings ou runtimes.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | Tipos de domínio, fonte, documento, query e resultado. |
| `markdown.py` | Ingestão Markdown e frontmatter. |
| `store.py` | Store abstrato e implementação em memória. |
| `search.py` | Helpers de indexação e busca textual. |
| `context_adapter.py` | Mapeamento determinístico de documentos e resultados de busca para candidatos do Context Router. |
| `__init__.py` | Exportações públicas do módulo. |

## Principais Tipos, Classes E Funções

- `KnowledgeDomain`: domínio do conhecimento.
- `KnowledgeSource`: origem do documento.
- `KnowledgeDocument`: documento textual governado.
- `KnowledgeQuery`: consulta.
- `KnowledgeSearchResult`: resultado citável.
- `KnowledgeStore`: contrato de store.
- `InMemoryKnowledgeStore`: store em memória.
- `markdown_to_document`: converte Markdown em documento.
- `ingest_markdown_file`: ingere arquivo Markdown.
- `search_text`: busca textual simples.
- `knowledge_document_to_context_candidate`: converte documento do Knowledge Hub em `ContextSource` e `ContextItem`.
- `knowledge_search_result_to_context_candidate`: converte resultado textual do Knowledge Hub em `ContextSource` e `ContextItem`.
- `knowledge_search_results_to_context_candidates`: converte uma sequência de resultados textuais preservando a ordem recebida.

## Entradas E Saídas

Entradas:

- Markdown canônico ou texto já autorizado.
- `KnowledgeQuery` com texto, domínio e filtros.
- `KnowledgeDocument` e `KnowledgeSearchResult` já existentes para conversão em candidatos de contexto.

Saídas:

- `KnowledgeDocument` e `KnowledgeSearchResult` com citações e snippets.
- Pares `ContextSource` e `ContextItem` para o Context Router, preservando id, título, referência, tipo de fonte, hash e citações ou referência rastreável mínima.

## Dependências Internas

- Pode receber documentos vindos de `../canonicalizer/`.
- Usa tipos públicos de `../context/` no adaptador de candidatos, sem fazer busca, roteamento, providers ou chamadas externas.

## Módulos Relacionados

- Acima: [capabilities](../capabilities/README.md), [skills](../skills/README.md), [tools](../tools/README.md).
- Abaixo: [canonicalizer](../canonicalizer/README.md), [persistence](../persistence/README.md).
- Transversal: [guardian](../guardian/README.md).

## Specs Correspondentes

- [Spec 0011: Knowledge Hub](../../../specs/framework/0011-knowledge-hub.md)
- [Spec 0012: Canonicalizer](../../../specs/framework/0012-canonicalizer.md)

## Docs Relacionadas

- [Knowledge Hub](../../../docs/knowledge-hub.md)
- [Canonicalizer](../../../docs/canonicalizer.md)
- [Mapa de arquitetura](../../../docs/alignment/architecture-map.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.knowledge import InMemoryKnowledgeStore, markdown_to_document, search_text

store = InMemoryKnowledgeStore()
doc = markdown_to_document("# Spec\n\nConteúdo")
store.add(doc)
results = search_text(store, "Spec")
```

## Integração Com Context Router

O adaptador `context_adapter.py` permite transformar documentos e resultados já disponíveis do Knowledge Hub em candidatos explícitos para o Context Router:

```python
from vercosa_ai_framework.context import ContextRequest, DeterministicContextRouter, TokenBudget
from vercosa_ai_framework.knowledge import knowledge_search_result_to_context_candidate

source, item = knowledge_search_result_to_context_candidate(results[0])
request = ContextRequest(
    request_id="req-1",
    request_goal="Montar contexto com candidato textual",
    token_budget=TokenBudget(max_input_tokens=1000, reserved_output_tokens=200),
    candidate_sources=(source,),
    candidate_items=(item,),
)
package = DeterministicContextRouter().route(request)
```

Esse fluxo é determinístico. O adaptador não executa busca semântica, não faz embeddings, não acessa pgvector, não acessa banco, não lê filesystem e não chama LLM ou provider. O Context Router monta o `ContextPackage`; o Knowledge Hub apenas fornece candidatos rastreáveis.

## Status Atual

Status: `MVP`.

O módulo implementa ingestão Markdown, busca textual em memória e conversão determinística de documentos/resultados em candidatos para o Context Router. Ele ainda não é o Knowledge Hub semântico completo.

## Próximos Passos

- Definir ranking, chunking e políticas adicionais para candidatos antes de expandir retrieval.
- Projetar Semantic Index futuro com citações, redaction e adapters substituíveis.
- Definir integração futura com Policy Engine e Guardian Engine antes de RAG semântico.
