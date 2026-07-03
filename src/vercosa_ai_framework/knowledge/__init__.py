"""Knowledge Hub public contracts."""

from vercosa_ai_framework.knowledge.store import InMemoryKnowledgeStore, KnowledgeStore, KnowledgeStoreError
from vercosa_ai_framework.knowledge.markdown import (
    PROMPT_INJECTION_WARNING,
    detect_prompt_injection_warnings,
    ingest_markdown_file,
    load_markdown_document,
    markdown_to_document,
    parse_markdown_frontmatter,
    read_markdown_file,
)
from vercosa_ai_framework.knowledge.search import index_document, search_text
from vercosa_ai_framework.knowledge.types import (
    KnowledgeDocument,
    KnowledgeDomain,
    KnowledgeQuery,
    KnowledgeSearchResult,
    KnowledgeSource,
    content_hash,
    split_frontmatter,
)

__all__ = [
    "InMemoryKnowledgeStore",
    "KnowledgeDocument",
    "KnowledgeDomain",
    "KnowledgeQuery",
    "KnowledgeSearchResult",
    "KnowledgeSource",
    "KnowledgeStore",
    "KnowledgeStoreError",
    "PROMPT_INJECTION_WARNING",
    "content_hash",
    "detect_prompt_injection_warnings",
    "index_document",
    "ingest_markdown_file",
    "load_markdown_document",
    "markdown_to_document",
    "parse_markdown_frontmatter",
    "read_markdown_file",
    "search_text",
    "split_frontmatter",
]
