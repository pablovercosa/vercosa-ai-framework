"""Simple deterministic text search facade for the Knowledge Hub MVP."""

from __future__ import annotations

from typing import Any

from vercosa_ai_framework.knowledge.store import KnowledgeStore
from vercosa_ai_framework.knowledge.types import KnowledgeDocument, KnowledgeDomain, KnowledgeQuery, KnowledgeSearchResult


def index_document(store: KnowledgeStore, document: KnowledgeDocument) -> KnowledgeDocument:
    """Index a canonical document in the provided store."""

    return store.add_document(document)


def search_text(
    store: KnowledgeStore,
    query_text: str,
    *,
    domains: tuple[KnowledgeDomain | str, ...] = (),
    tags: tuple[str, ...] = (),
    filters: dict[str, Any] | None = None,
    source_types: tuple[str, ...] = (),
    top_k: int = 10,
    sensitivity_allowed: tuple[str, ...] = ("public", "internal"),
    include_citations: bool = True,
) -> tuple[KnowledgeSearchResult, ...]:
    """Search indexed documents using deterministic textual matching."""

    query = KnowledgeQuery(
        query_text=query_text,
        domains=tuple(_resolve_domain(domain) for domain in domains),
        tags=tags,
        filters=filters or {},
        source_types=source_types,
        top_k=top_k,
        sensitivity_allowed=sensitivity_allowed,
        include_citations=include_citations,
    )
    return store.search(query)


def _resolve_domain(value: KnowledgeDomain | str) -> KnowledgeDomain:
    if isinstance(value, KnowledgeDomain):
        return value
    try:
        return KnowledgeDomain(str(value))
    except ValueError:
        return KnowledgeDomain.UNKNOWN


__all__ = ["index_document", "search_text"]
