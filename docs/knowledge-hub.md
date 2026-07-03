# Knowledge Hub MVP

O Knowledge Hub MVP implementa ingestao local de Markdown e busca textual simples, sem embeddings, PostgreSQL, APIs externas ou dependencias pesadas.

## Escopo

- Le Markdown local com `load_markdown_document` e `ingest_markdown_file`.
- Extrai frontmatter YAML simples via `parse_markdown_frontmatter`.
- Cria `KnowledgeDocument` canonico em Markdown.
- Indexa documentos em `InMemoryKnowledgeStore`.
- Executa busca textual deterministica com `search_text`.
- Filtra por dominio, tags, metadados, tipo de fonte e sensibilidade.
- Detecta indicios basicos de prompt injection e marca warnings em `metadata`.

## Limites

- Nao gera embeddings.
- Nao acessa PostgreSQL ou pgvector.
- Nao chama APIs externas.
- Nao executa comandos.
- Nao substitui scanner completo de prompt injection ou segredos.

## Uso

```python
from vercosa_ai_framework.knowledge import InMemoryKnowledgeStore, ingest_markdown_file, search_text

store = InMemoryKnowledgeStore()
ingest_markdown_file("docs/knowledge-hub.md", store)

results = search_text(store, "Markdown", domains=("docs",), tags=("knowledge",))
```

Resultados carregam referencias auditaveis como `document_id`, `source_uri`, `content_hash`, `citations` e `warnings` quando aplicavel.
