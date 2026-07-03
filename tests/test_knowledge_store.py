from __future__ import annotations

import pytest

from vercosa_ai_framework.knowledge import (
    InMemoryKnowledgeStore,
    KnowledgeDocument,
    KnowledgeDomain,
    KnowledgeQuery,
    KnowledgeStoreError,
)


def make_document(
    document_id: str,
    *,
    title: str,
    content: str,
    domain: KnowledgeDomain,
    tags: tuple[str, ...] = (),
    sensitivity: str = "public",
) -> KnowledgeDocument:
    return KnowledgeDocument(
        document_id=document_id,
        title=title,
        content=content,
        domain=domain,
        source_uri=f"knowledge/{document_id}.md",
        tags=tags,
        sensitivity=sensitivity,
        trust_level="authoritative",
    )


def test_in_memory_store_adds_and_gets_document():
    document = make_document(
        "doc-knowledge",
        title="Knowledge Hub",
        content="Canonical documents and semantic indexes.",
        domain=KnowledgeDomain.SPECS,
    )
    store = InMemoryKnowledgeStore()

    assert store.add_document(document) == document
    assert store.get_document("doc-knowledge") == document
    assert store.list_documents() == (document,)


def test_in_memory_store_rejects_duplicate_and_missing_documents():
    document = make_document(
        "doc-knowledge",
        title="Knowledge Hub",
        content="Canonical documents.",
        domain=KnowledgeDomain.SPECS,
    )
    store = InMemoryKnowledgeStore((document,))

    with pytest.raises(KnowledgeStoreError, match="already registered"):
        store.add_document(document)

    with pytest.raises(KnowledgeStoreError, match="unknown knowledge document"):
        store.get_document("missing")


def test_search_filters_by_domain_tags_and_simple_text():
    store = InMemoryKnowledgeStore(
        (
            make_document(
                "spec-knowledge",
                title="Knowledge Hub",
                content="RAG por dominio com Markdown canonico e provider agnostic.",
                domain=KnowledgeDomain.SPECS,
                tags=("knowledge", "rag"),
            ),
            make_document(
                "adr-provider",
                title="Provider Gateway ADR",
                content="Providers sao adapters substituiveis.",
                domain=KnowledgeDomain.ADRS,
                tags=("provider",),
            ),
            make_document(
                "doc-runtime",
                title="Runtime",
                content="OpenCode e apenas um adapter inicial.",
                domain=KnowledgeDomain.DOCS,
                tags=("runtime",),
            ),
        )
    )

    results = store.search(
        KnowledgeQuery(
            query_text="provider agnostic",
            domains=(KnowledgeDomain.SPECS,),
            tags=("knowledge",),
        )
    )

    assert [result.document_id for result in results] == ["spec-knowledge"]
    assert results[0].rank == 1
    assert results[0].source_uri == "knowledge/spec-knowledge.md"
    assert results[0].citations == ("knowledge/spec-knowledge.md",)


def test_search_supports_frontmatter_metadata_filters():
    document = KnowledgeDocument.from_markdown(
        """---
document_id: spec-framework-0011
domain: specs
title: Knowledge Hub
status: aprovada
language: pt-BR
tags: [knowledge]
---
Busca por metadados de frontmatter.
"""
    )
    store = InMemoryKnowledgeStore((document,))

    results = store.search(
        KnowledgeQuery(
            domains=(KnowledgeDomain.SPECS,),
            filters={"status": "aprovada", "language": "pt-BR"},
        )
    )

    assert [result.document_id for result in results] == ["spec-framework-0011"]


def test_search_respects_top_k_and_sensitivity_filter():
    public = make_document(
        "public-doc",
        title="Public Knowledge",
        content="knowledge hub",
        domain=KnowledgeDomain.DOCS,
        tags=("knowledge",),
    )
    internal = make_document(
        "internal-doc",
        title="Internal Knowledge",
        content="knowledge hub",
        domain=KnowledgeDomain.DOCS,
        tags=("knowledge",),
        sensitivity="internal",
    )
    store = InMemoryKnowledgeStore((internal, public))

    results = store.search(
        KnowledgeQuery(
            query_text="knowledge",
            domains=(KnowledgeDomain.DOCS,),
            top_k=1,
            sensitivity_allowed=("public",),
        )
    )

    assert [result.document_id for result in results] == ["public-doc"]


def test_search_returns_empty_tuple_when_no_document_matches():
    store = InMemoryKnowledgeStore(
        (
            make_document(
                "spec-knowledge",
                title="Knowledge Hub",
                content="Canonical Markdown.",
                domain=KnowledgeDomain.SPECS,
                tags=("knowledge",),
            ),
        )
    )

    assert store.search(KnowledgeQuery(query_text="embedding", domains=(KnowledgeDomain.SPECS,))) == ()
