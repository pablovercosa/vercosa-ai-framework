"""Knowledge Store abstract contract and in-memory implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

from vercosa_ai_framework.knowledge.types import (
    KnowledgeDocument,
    KnowledgeDomain,
    KnowledgeQuery,
    KnowledgeSearchResult,
)


class KnowledgeStoreError(ValueError):
    """Raised when a Knowledge Store operation violates its contract."""


class KnowledgeStore(ABC):
    """Abstract boundary for provider-agnostic knowledge storage and search."""

    @abstractmethod
    def add_document(self, document: KnowledgeDocument) -> KnowledgeDocument:
        """Add a canonical document to the store."""

    @abstractmethod
    def get_document(self, document_id: str) -> KnowledgeDocument:
        """Return a document by ID."""

    @abstractmethod
    def search(self, query: KnowledgeQuery) -> tuple[KnowledgeSearchResult, ...]:
        """Search documents by domain, tags, metadata, source type, and text."""


class InMemoryKnowledgeStore(KnowledgeStore):
    """Deterministic in-memory Knowledge Store for contract tests and local use."""

    def __init__(self, documents: Iterable[KnowledgeDocument] = ()) -> None:
        self._documents: dict[str, KnowledgeDocument] = {}
        for document in documents:
            self.add_document(document)

    def add_document(self, document: KnowledgeDocument) -> KnowledgeDocument:
        """Add a canonical document and reject duplicate document IDs."""

        if document.document_id in self._documents:
            raise KnowledgeStoreError(f"knowledge document already registered: {document.document_id}")
        self._documents[document.document_id] = document
        return document

    def get_document(self, document_id: str) -> KnowledgeDocument:
        """Return a document by ID."""

        try:
            return self._documents[document_id]
        except KeyError as exc:
            raise KnowledgeStoreError(f"unknown knowledge document: {document_id}") from exc

    def list_documents(self) -> tuple[KnowledgeDocument, ...]:
        """Return documents in deterministic order."""

        return tuple(sorted(self._documents.values(), key=_document_sort_key))

    def search(self, query: KnowledgeQuery) -> tuple[KnowledgeSearchResult, ...]:
        """Search documents with provider-neutral filters and simple text ranking."""

        matches: list[tuple[KnowledgeDocument, float]] = []
        for document in self.list_documents():
            if not _matches_domains(document, query.domains):
                continue
            if query.tags and not document.has_tags(query.tags):
                continue
            if query.source_types and document.source_type not in set(query.source_types):
                continue
            if query.sensitivity_allowed and document.sensitivity not in set(query.sensitivity_allowed):
                continue
            if not _matches_filters(document, query.filters):
                continue
            score = _text_score(document, query.query_text)
            if query.query_text and score <= 0:
                continue
            matches.append((document, score))

        ranked = sorted(matches, key=lambda item: (-item[1], _document_sort_key(item[0])))[: max(query.top_k, 0)]
        return tuple(_result_from_document(query, document, score, rank) for rank, (document, score) in enumerate(ranked, start=1))


def _matches_domains(document: KnowledgeDocument, domains: tuple[KnowledgeDomain, ...]) -> bool:
    return not domains or document.domain in set(domains)


def _matches_filters(document: KnowledgeDocument, filters: dict[str, object]) -> bool:
    for key, expected in filters.items():
        actual = _field_or_metadata(document, key)
        if actual != expected:
            return False
    return True


def _field_or_metadata(document: KnowledgeDocument, key: str) -> object:
    if hasattr(document, key):
        return getattr(document, key)
    if key in document.metadata:
        return document.metadata[key]
    return document.frontmatter.get(key)


def _text_score(document: KnowledgeDocument, query_text: str) -> float:
    normalized_query = query_text.strip().lower()
    if not normalized_query:
        return 1.0
    haystack = "\n".join((document.title, document.content, " ".join(document.tags))).lower()
    terms = [term for term in normalized_query.split() if term]
    if not terms:
        return 1.0
    term_matches = sum(1 for term in terms if term in haystack)
    exact_bonus = 1 if normalized_query in haystack else 0
    return float(term_matches + exact_bonus)


def _result_from_document(query: KnowledgeQuery, document: KnowledgeDocument, score: float, rank: int) -> KnowledgeSearchResult:
    return KnowledgeSearchResult(
        query_id=query.query_id,
        domain=document.domain,
        document_id=document.document_id,
        title=document.title,
        snippet=_snippet(document.content, query.query_text),
        score=score,
        rank=rank,
        citations=_citations(document) if query.include_citations else (),
        source_uri=document.source_uri,
        content_hash=document.content_hash,
        sensitivity=document.sensitivity,
        trust_level=document.trust_level,
        warnings=_document_warnings(document),
        redactions_applied=document.redactions_applied,
        metadata={"ranking_policy": query.ranking_policy},
    )


def _document_warnings(document: KnowledgeDocument) -> tuple[str, ...]:
    value = document.metadata.get("warnings", ())
    if isinstance(value, str):
        return (value,)
    if isinstance(value, tuple | list | set):
        return tuple(str(item) for item in value)
    return ()


def _citations(document: KnowledgeDocument) -> tuple[str, ...]:
    if document.canonical_uri:
        return (document.canonical_uri,)
    if document.source_uri:
        return (document.source_uri,)
    return (document.document_id,)


def _snippet(content: str, query_text: str, *, max_length: int = 240) -> str:
    normalized_query = query_text.strip().lower()
    if not normalized_query:
        return content[:max_length]
    lower_content = content.lower()
    index = lower_content.find(normalized_query)
    if index < 0:
        for term in normalized_query.split():
            index = lower_content.find(term)
            if index >= 0:
                break
    if index < 0:
        return content[:max_length]
    start = max(index - 60, 0)
    end = min(start + max_length, len(content))
    return content[start:end]


def _document_sort_key(document: KnowledgeDocument) -> tuple[str, str, str]:
    return (document.domain.value, document.title, document.document_id)


__all__ = ["InMemoryKnowledgeStore", "KnowledgeStore", "KnowledgeStoreError"]
