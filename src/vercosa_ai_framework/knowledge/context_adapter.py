"""Deterministic adapters from Knowledge Hub records to context candidates.

This module only maps already available Knowledge Hub objects into Context
Router candidates. It does not search, read files, access storage, call
providers, create embeddings, or contact external services.
"""

from __future__ import annotations

from vercosa_ai_framework.context import (
    ContextCitation,
    ContextItem,
    ContextItemType,
    ContextSource,
    ContextSourceType,
    stable_id,
)
from vercosa_ai_framework.knowledge.types import KnowledgeDocument, KnowledgeDomain, KnowledgeSearchResult


def knowledge_document_to_context_candidate(
    document: KnowledgeDocument,
    *,
    rank: int = 0,
    item_type: ContextItemType = ContextItemType.EXCERPT,
) -> tuple[ContextSource, ContextItem]:
    """Convert a canonical knowledge document into one context candidate."""

    source = ContextSource(
        source_id=document.document_id,
        source_type=_source_type_for_document(document),
        domain=document.domain.value,
        uri=document.canonical_uri or document.source_uri,
        content_hash=document.content_hash,
        trust_level=document.trust_level,
        sensitivity=document.sensitivity,
        canonical_ref=document.canonical_uri,
        metadata={
            "knowledge_document_id": document.document_id,
            "title": document.title,
            "source_type": document.source_type,
            "source_uri": document.source_uri,
            "version": document.version,
            "language": document.language,
            "tags": document.tags,
            "redactions_applied": document.redactions_applied,
            "guardian_decision_refs": document.guardian_decision_refs,
        },
    )
    item = ContextItem(
        context_item_id=stable_id("knowledge_context_item", document.document_id, document.content_hash, rank),
        source_ref=source.source_id,
        content=document.content,
        content_ref=document.canonical_uri or document.source_uri,
        item_type=item_type,
        rank=rank,
        reason_selected="knowledge_document_candidate",
        citations=_document_citations(document, source.source_id),
        trust_level=document.trust_level,
        sensitivity=document.sensitivity,
        content_hash=document.content_hash,
        metadata={
            "knowledge_kind": "document",
            "knowledge_document_id": document.document_id,
            "title": document.title,
            "source_uri": document.source_uri,
            "canonical_uri": document.canonical_uri,
            "source_type": document.source_type,
            "domain": document.domain.value,
            "version": document.version,
            "warnings": _metadata_warnings(document.metadata),
        },
    )
    return source, item


def knowledge_search_result_to_context_candidate(
    result: KnowledgeSearchResult,
    *,
    item_type: ContextItemType = ContextItemType.EXCERPT,
) -> tuple[ContextSource, ContextItem]:
    """Convert one Knowledge Hub search result into one context candidate."""

    source = ContextSource(
        source_id=result.document_id,
        source_type=ContextSourceType.TEXT_SEARCH_RESULT,
        domain=result.domain.value,
        uri=result.source_uri,
        content_hash=result.content_hash,
        trust_level=result.trust_level,
        sensitivity=result.sensitivity,
        metadata={
            "knowledge_result_id": result.result_id,
            "knowledge_document_id": result.document_id,
            "title": result.title,
            "source_uri": result.source_uri,
            "chunk_id": result.chunk_id,
            "score": result.score,
            "rank": result.rank,
            "warnings": result.warnings,
            "redactions_applied": result.redactions_applied,
        },
    )
    item = ContextItem(
        context_item_id=stable_id("knowledge_context_item", result.query_id, result.result_id, result.document_id, result.chunk_id or "", result.rank),
        source_ref=source.source_id,
        content=result.snippet,
        content_ref=result.source_uri,
        item_type=item_type,
        rank=result.rank,
        reason_selected="knowledge_search_result_candidate",
        citations=_result_citations(result, source.source_id),
        trust_level=result.trust_level,
        sensitivity=result.sensitivity,
        content_hash=result.content_hash,
        metadata={
            "knowledge_kind": "search_result",
            "knowledge_result_id": result.result_id,
            "knowledge_query_id": result.query_id,
            "knowledge_document_id": result.document_id,
            "title": result.title,
            "source_uri": result.source_uri,
            "chunk_id": result.chunk_id,
            "domain": result.domain.value,
            "score": result.score,
            "warnings": result.warnings,
        },
    )
    return source, item


def knowledge_search_results_to_context_candidates(
    results: tuple[KnowledgeSearchResult, ...],
    *,
    item_type: ContextItemType = ContextItemType.EXCERPT,
) -> tuple[tuple[ContextSource, ContextItem], ...]:
    """Convert search results into context candidates preserving result order."""

    return tuple(knowledge_search_result_to_context_candidate(result, item_type=item_type) for result in results)


def _source_type_for_document(document: KnowledgeDocument) -> ContextSourceType:
    if document.domain is KnowledgeDomain.SPECS:
        return ContextSourceType.SPEC
    if document.domain is KnowledgeDomain.ADRS:
        return ContextSourceType.ADR
    if document.domain is KnowledgeDomain.DECISIONS:
        return ContextSourceType.DECISION_RECORD
    if document.source_type.lower() == "readme":
        return ContextSourceType.README
    return ContextSourceType.CANONICAL_DOCUMENT


def _document_citations(document: KnowledgeDocument, source_ref: str) -> tuple[ContextCitation, ...]:
    reference = document.canonical_uri or document.source_uri or document.document_id
    return (
        ContextCitation(
            citation_id=stable_id("context_citation", source_ref, reference, document.content_hash),
            source_ref=source_ref,
            document_id=document.document_id,
            canonical_uri=document.canonical_uri,
            source_uri=document.source_uri,
            path=document.source_uri or document.canonical_uri,
            content_hash=document.content_hash,
            metadata={"title": document.title, "reference": reference},
        ),
    )


def _result_citations(result: KnowledgeSearchResult, source_ref: str) -> tuple[ContextCitation, ...]:
    references = result.citations or (result.source_uri or result.document_id,)
    return tuple(
        ContextCitation(
            citation_id=stable_id("context_citation", source_ref, reference, result.content_hash or "", result.chunk_id or ""),
            source_ref=source_ref,
            document_id=result.document_id,
            source_uri=result.source_uri,
            path=reference,
            chunk_id=result.chunk_id,
            content_hash=result.content_hash,
            metadata={"title": result.title, "reference": reference, "knowledge_result_id": result.result_id},
        )
        for reference in references
    )


def _metadata_warnings(metadata: dict[str, object]) -> tuple[str, ...]:
    value = metadata.get("warnings", ())
    if isinstance(value, str):
        return (value,)
    if isinstance(value, tuple | list | set):
        return tuple(str(item) for item in value)
    return ()


__all__ = [
    "knowledge_document_to_context_candidate",
    "knowledge_search_result_to_context_candidate",
    "knowledge_search_results_to_context_candidates",
]
