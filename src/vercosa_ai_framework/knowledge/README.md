# Knowledge Module

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0011](../../../specs/framework/0011-knowledge-hub.md)

## Objetivo

Representar documentos de conhecimento e busca textual determinística no MVP do Knowledge Hub.

## O Que Este Módulo Faz

- Define domínios, fontes, documentos, queries e resultados de conhecimento.
- Lê Markdown e frontmatter simples.
- Detecta warnings básicos de prompt injection em documentos.
- Mantém store em memória.
- Executa busca textual determinística.

## O Que Este Módulo Não Faz

- Não implementa Semantic Index com embeddings.
- Não usa PostgreSQL, pgvector ou Ollama diretamente.
- Não decide contexto final para prompts; isso pertence ao futuro Context Router.
- Não processa binários diretamente.
- Não substitui Canonicalizer.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | Tipos de domínio, fonte, documento, query e resultado. |
| `markdown.py` | Ingestão Markdown e frontmatter. |
| `store.py` | Store abstrato e implementação em memória. |
| `search.py` | Helpers de indexação e busca textual. |
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

## Entradas E Saídas

Entradas:

- Markdown canônico ou texto já autorizado.
- `KnowledgeQuery` com texto, domínio e filtros.

Saídas:

- `KnowledgeDocument` e `KnowledgeSearchResult` com citações e snippets.

## Dependências Internas

- Pode receber documentos vindos de `../canonicalizer/`.

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
- [Architecture Map](../../../docs/alignment/architecture-map.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.knowledge import InMemoryKnowledgeStore, markdown_to_document, search_text

store = InMemoryKnowledgeStore()
doc = markdown_to_document("# Spec\n\nConteúdo")
store.add(doc)
results = search_text(store, "Spec")
```

## Status Atual

Status: `MVP`.

O módulo implementa ingestão Markdown e busca textual em memória, mas ainda não é o Knowledge Hub semântico completo.

## Próximos Passos

- Definir Context Router antes de expandir retrieval.
- Projetar Semantic Index com citações, redaction e adapters substituíveis.
