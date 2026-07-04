import socket

from vercosa_ai_framework.context import (
    ContextItemType,
    ContextOmissionReason,
    ContextRequest,
    ContextSourceType,
    DeterministicContextRouter,
    TokenBudget,
)
from vercosa_ai_framework.knowledge import (
    KnowledgeDocument,
    KnowledgeDomain,
    KnowledgeSearchResult,
    knowledge_document_to_context_candidate,
    knowledge_search_result_to_context_candidate,
)


def test_convert_knowledge_document_to_context_item() -> None:
    document = KnowledgeDocument(
        document_id="doc-1",
        title="Spec de contexto",
        content="Context Router monta pacotes citaveis.",
        domain=KnowledgeDomain.SPECS,
        canonical_uri="knowledge/specs/doc-1.md",
        source_uri="specs/framework/doc-1.md",
        source_type="markdown",
        trust_level="authoritative",
    )

    source, item = knowledge_document_to_context_candidate(document)

    assert source.source_id == "doc-1"
    assert source.source_type is ContextSourceType.SPEC
    assert source.uri == "knowledge/specs/doc-1.md"
    assert source.content_hash == document.content_hash
    assert source.metadata["title"] == "Spec de contexto"
    assert item.source_ref == "doc-1"
    assert item.content == document.content
    assert item.content_hash == document.content_hash
    assert item.metadata["title"] == "Spec de contexto"


def test_convert_knowledge_search_result_preserves_origin_and_title() -> None:
    result = KnowledgeSearchResult(
        query_id="query-1",
        result_id="result-1",
        domain=KnowledgeDomain.DOCS,
        document_id="doc-2",
        title="Guia de contexto",
        snippet="Knowledge Hub fornece candidatos, nao pacote final.",
        score=3.0,
        rank=1,
        citations=("docs/context-router-token-budget.md",),
        source_uri="docs/context-router-token-budget.md",
        content_hash="hash-doc-2",
    )

    source, item = knowledge_search_result_to_context_candidate(result)

    assert source.source_type is ContextSourceType.TEXT_SEARCH_RESULT
    assert source.uri == "docs/context-router-token-budget.md"
    assert source.metadata["title"] == "Guia de contexto"
    assert item.content == result.snippet
    assert item.metadata["knowledge_result_id"] == "result-1"
    assert item.metadata["title"] == "Guia de contexto"
    assert item.citations[0].path == "docs/context-router-token-budget.md"


def test_search_result_without_formal_citation_gets_traceable_reference() -> None:
    result = KnowledgeSearchResult(
        query_id="query-2",
        result_id="result-2",
        domain=KnowledgeDomain.DOCS,
        document_id="doc-3",
        title="Documento sem citacao formal",
        snippet="Trecho citavel por referencia minima.",
        score=1.0,
        rank=1,
        source_uri="docs/minimo.md",
        content_hash="hash-doc-3",
    )

    _source, item = knowledge_search_result_to_context_candidate(result)

    assert item.citations[0].document_id == "doc-3"
    assert item.citations[0].path == "docs/minimo.md"
    assert item.citations[0].content_hash == "hash-doc-3"


def test_context_router_uses_converted_knowledge_candidates() -> None:
    document = KnowledgeDocument(
        document_id="doc-router",
        title="Documento roteavel",
        content="Conteudo curto vindo do Knowledge Hub.",
        domain=KnowledgeDomain.DOCS,
        source_uri="docs/router.md",
    )
    source, item = knowledge_document_to_context_candidate(document)
    request = ContextRequest(
        request_id="req-knowledge-router",
        request_goal="montar pacote com candidato de conhecimento",
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
        candidate_sources=(source,),
        candidate_items=(item,),
    )

    package = DeterministicContextRouter().route(request)

    assert [selected.context_item_id for selected in package.items] == [item.context_item_id]
    assert package.sources == (source,)
    assert package.citations == item.citations


def test_router_deduplicates_converted_knowledge_candidates_by_hash() -> None:
    first = KnowledgeSearchResult(
        query_id="query-dedupe",
        result_id="result-a",
        domain=KnowledgeDomain.DOCS,
        document_id="doc-a",
        title="A",
        snippet="Primeiro trecho.",
        score=2.0,
        rank=1,
        content_hash="same-hash",
    )
    second = KnowledgeSearchResult(
        query_id="query-dedupe",
        result_id="result-b",
        domain=KnowledgeDomain.DOCS,
        document_id="doc-b",
        title="B",
        snippet="Segundo trecho.",
        score=2.0,
        rank=2,
        content_hash="same-hash",
    )
    source_a, item_a = knowledge_search_result_to_context_candidate(first)
    source_b, item_b = knowledge_search_result_to_context_candidate(second)
    request = ContextRequest(
        request_id="req-knowledge-dedupe",
        request_goal="deduplicar candidatos do Knowledge Hub",
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
        candidate_sources=(source_a, source_b),
        candidate_items=(item_a, item_b),
    )

    package = DeterministicContextRouter().route(request)

    assert [selected.context_item_id for selected in package.items] == [item_a.context_item_id]
    assert package.omission_reasons[0].item_ref == item_b.context_item_id
    assert package.omission_reasons[0].omission_reason is ContextOmissionReason.DUPLICATE


def test_router_omits_converted_knowledge_candidate_when_budget_is_exceeded() -> None:
    document = KnowledgeDocument(
        document_id="doc-large",
        title="Documento grande",
        content="x" * 200,
        domain=KnowledgeDomain.DOCS,
        source_uri="docs/large.md",
    )
    source, item = knowledge_document_to_context_candidate(document)
    request = ContextRequest(
        request_id="req-knowledge-budget",
        request_goal="limitar candidato do Knowledge Hub",
        token_budget=TokenBudget(max_input_tokens=20, reserved_output_tokens=10),
        candidate_sources=(source,),
        candidate_items=(item,),
    )

    package = DeterministicContextRouter().route(request)

    assert package.items == ()
    assert package.omission_reasons[0].item_ref == item.context_item_id
    assert package.omission_reasons[0].omission_reason is ContextOmissionReason.TOKEN_BUDGET_EXCEEDED


def test_conversion_preserves_citations_for_required_evidence() -> None:
    result = KnowledgeSearchResult(
        query_id="query-evidence",
        result_id="result-evidence",
        domain=KnowledgeDomain.SPECS,
        document_id="spec-1",
        title="Spec",
        snippet="Evidencia com citacao preservada.",
        score=1.0,
        rank=1,
        citations=("specs/framework/0014.md",),
        content_hash="hash-spec-1",
    )
    source, item = knowledge_search_result_to_context_candidate(result, item_type=ContextItemType.EVIDENCE)
    request = ContextRequest(
        request_id="req-knowledge-evidence",
        request_goal="aceitar evidencia citada",
        citation_required=True,
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
        candidate_sources=(source,),
        candidate_items=(item,),
    )

    package = DeterministicContextRouter().route(request)

    assert len(package.items) == 1
    assert package.items[0].citations == item.citations
    assert package.omission_reasons == ()


def test_knowledge_context_conversion_is_deterministic() -> None:
    result = KnowledgeSearchResult(
        query_id="query-stable",
        result_id="result-stable",
        domain=KnowledgeDomain.DOCS,
        document_id="doc-stable",
        title="Estavel",
        snippet="Mesmo resultado deve gerar mesmo candidato.",
        score=1.0,
        rank=1,
        source_uri="docs/stable.md",
        content_hash="hash-stable",
    )

    first = knowledge_search_result_to_context_candidate(result)
    second = knowledge_search_result_to_context_candidate(result)

    assert first == second


def test_adapter_and_router_do_not_require_network(monkeypatch) -> None:
    def fail_socket(*args, **kwargs):  # noqa: ANN001, ANN002, ANN003
        raise AssertionError("network access is not allowed")

    monkeypatch.setattr(socket, "socket", fail_socket)
    document = KnowledgeDocument(
        document_id="doc-no-network",
        content="Conversao local e deterministica.",
        domain=KnowledgeDomain.DOCS,
        source_uri="docs/no-network.md",
    )
    source, item = knowledge_document_to_context_candidate(document)
    request = ContextRequest(
        request_id="req-no-network-knowledge",
        request_goal="validar ausencia de rede",
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
        candidate_sources=(source,),
        candidate_items=(item,),
    )

    package = DeterministicContextRouter().route(request)

    assert package.metadata["router"] == "deterministic"
    assert package.items[0].metadata["knowledge_kind"] == "document"
