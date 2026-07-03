from __future__ import annotations

import pytest

from vercosa_ai_framework.knowledge import (
    KnowledgeDocument,
    KnowledgeDomain,
    KnowledgeQuery,
    KnowledgeSearchResult,
    KnowledgeSource,
    KnowledgeStore,
    split_frontmatter,
)


def test_knowledge_domains_match_initial_spec_scope():
    assert {domain.value for domain in KnowledgeDomain} == {
        "specs",
        "adrs",
        "docs",
        "code",
        "legal",
        "books",
        "conversations",
        "decisions",
        "projects",
        "agents",
        "skills",
        "commands",
        "hooks",
        "guardian",
        "architecture",
        "unknown",
    }


def test_knowledge_source_is_provider_agnostic_metadata():
    source = KnowledgeSource(
        source_id="source-spec-0011",
        source_uri="specs/framework/0011-knowledge-hub.md",
        source_type="markdown",
        domain=KnowledgeDomain.SPECS,
        title="Knowledge Hub",
        trust_level="authoritative",
        tags=("knowledge", "spec"),
    )

    assert source.domain == KnowledgeDomain.SPECS
    assert source.source_type == "markdown"
    assert source.tags == ("knowledge", "spec")
    assert source.metadata == {}


def test_knowledge_document_parses_frontmatter_metadata_without_external_yaml_dependency():
    markdown = """---
document_id: spec-framework-0011
domain: specs
source_type: markdown
title: Knowledge Hub
version: 1
language: pt-BR
sensitivity: internal
trust_level: authoritative
rag_allowed: true
tags: [knowledge, rag]
---
# Knowledge Hub

Busca governada por dominio.
"""

    document = KnowledgeDocument.from_markdown(markdown)

    assert document.document_id == "spec-framework-0011"
    assert document.domain == KnowledgeDomain.SPECS
    assert document.title == "Knowledge Hub"
    assert document.content.startswith("# Knowledge Hub")
    assert document.frontmatter["rag_allowed"] is True
    assert document.metadata["language"] == "pt-BR"
    assert document.tags == ("knowledge", "rag")
    assert document.content_hash


def test_split_frontmatter_returns_original_content_when_header_is_absent():
    frontmatter, content = split_frontmatter("# Plain Markdown\n")

    assert frontmatter == {}
    assert content == "# Plain Markdown\n"


def test_knowledge_query_and_result_are_traceable_contracts():
    query = KnowledgeQuery(
        query_text="provider agnostic",
        domains=(KnowledgeDomain.SPECS,),
        tags=("knowledge",),
        top_k=3,
        mission_id="mission-knowledge",
    )
    result = KnowledgeSearchResult(
        query_id=query.query_id,
        domain=KnowledgeDomain.SPECS,
        document_id="spec-framework-0011",
        title="Knowledge Hub",
        snippet="provider agnostic",
        score=2.0,
        rank=1,
        citations=("specs/framework/0011-knowledge-hub.md",),
        content_hash="hash",
    )

    assert query.query_id
    assert query.include_citations is True
    assert result.query_id == query.query_id
    assert result.rank == 1
    assert result.citations == ("specs/framework/0011-knowledge-hub.md",)


def test_knowledge_store_is_abstract():
    with pytest.raises(TypeError):
        KnowledgeStore()
