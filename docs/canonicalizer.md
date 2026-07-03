# Canonicalizer MVP

O Canonicalizer MVP converte texto puro e Markdown em `CanonicalDocument` local, deterministico e text-only.

## Escopo

- Canonicaliza texto puro como Markdown minimo.
- Canonicaliza Markdown existente com frontmatter YAML simples.
- Calcula `source_hash` e `content_hash` SHA-256 deterministicos.
- Normaliza titulo por `title_hint`, frontmatter, metadados da fonte, H1 ou primeira linha util.
- Preserva metadados, frontmatter, proveniencia, warnings e referencias Guardian.
- Detecta prompt injection basico por padroes deterministicos.
- Detecta provaveis segredos e aplica redaction antes de gerar o documento canonico.
- Converte `CanonicalDocument` para `KnowledgeDocument` com `to_knowledge_document`, sem armazenar nem indexar.

## Limites

- Nao converte PDF, DOCX ou outros formatos binarios.
- Nao chama APIs externas.
- Nao acessa banco de dados, filesystem, embeddings ou providers.
- Nao substitui scanner completo de segredos nem o Guardian Engine final.
- Nao executa comandos e nao usa `sudo`.

## Uso

```python
from vercosa_ai_framework.canonicalizer import CanonicalizerEngine

engine = CanonicalizerEngine()
result = engine.canonicalize_markdown(
    """---
title: Example
domain: docs
---
# Example

Body
""",
    source_uri="docs/example.md",
    domain="docs",
)

document = result.document
knowledge_document = engine.to_knowledge_document(document)
```

Warnings e redactions usam codigos estruturados e nao incluem valores secretos em claro.
