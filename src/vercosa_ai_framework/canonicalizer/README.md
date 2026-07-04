# Módulo canonicalizer

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0012](../../../specs/framework/0012-canonicalizer.md)

## Objetivo

Converter texto e Markdown suportados em documentos canônicos antes de ingestão no Knowledge Hub.

## O Que Este Módulo Faz

- Define fontes, metadados, documentos e resultados de canonicalização.
- Normaliza Markdown e texto simples.
- Extrai frontmatter simples e título.
- Calcula hashes determinísticos.
- Detecta prompt injection provável e redige segredos prováveis no MVP.
- Converte para estruturas compatíveis com Knowledge Hub.

## O Que Este Módulo Não Faz

- Não indexa documentos.
- Não gera embeddings.
- Não executa RAG.
- Não processa PDF, DOCX, imagens, áudio ou vídeo nesta implementação.
- Não depende diretamente de Docling, Pandoc, Tesseract ou provider específico.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | Tipos de canonicalização. |
| `adapter.py` | Contrato `CanonicalizerAdapter`. |
| `markdown.py` | Normalização de Markdown e texto. |
| `engine.py` | `CanonicalizerEngine` MVP. |
| `__init__.py` | Exportações públicas do módulo. |

## Principais Tipos, Classes E Funções

- `CanonicalSourceType`: tipo de fonte.
- `CanonicalizationStatus`: status da conversão.
- `CanonicalSource`: origem do conteúdo.
- `CanonicalMetadata`: metadados canônicos.
- `CanonicalDocument`: documento canônico.
- `CanonicalizationRequest`: pedido de conversão.
- `CanonicalizationResult`: resultado da conversão.
- `CanonicalizerAdapter`: contrato abstrato.
- `CanonicalizerEngine`: engine MVP.
- `canonicalize_markdown_text`: normalização de Markdown.
- `text_to_markdown`: conversão simples de texto.

## Entradas E Saídas

Entradas:

- Texto ou Markdown suportado.
- `CanonicalizationRequest` com fonte, domínio e hints.

Saídas:

- `CanonicalizationResult` contendo `CanonicalDocument`, hash, warnings e status.

## Dependências Internas

- `../knowledge/`: conversão para tipos de Knowledge Hub quando aplicável.

## Módulos Relacionados

- Acima: [knowledge](../knowledge/README.md).
- Abaixo: [persistence](../persistence/README.md).
- Transversal: [guardian](../guardian/README.md).

## Specs Correspondentes

- [Spec 0012: Canonicalizer](../../../specs/framework/0012-canonicalizer.md)
- [Spec 0011: Knowledge Hub](../../../specs/framework/0011-knowledge-hub.md)

## Docs Relacionadas

- [Canonicalizer](../../../docs/canonicalizer.md)
- [Knowledge Hub](../../../docs/knowledge-hub.md)
- [Mapa de arquitetura](../../../docs/alignment/architecture-map.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.canonicalizer import CanonicalizerEngine

engine = CanonicalizerEngine()
result = engine.canonicalize_text("# Título\n\nConteúdo")
```

## Status Atual

Status: `MVP`.

O módulo canonicaliza texto e Markdown, mas adapters para formatos binários e integração completa com policies ainda são futuros.

## Próximos Passos

- Definir adapters para formatos não Markdown por Spec específica.
- Conectar canonicalização ao fluxo governado de ingestão do Knowledge Hub.
