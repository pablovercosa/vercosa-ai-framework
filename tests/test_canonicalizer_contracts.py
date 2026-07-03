from __future__ import annotations

import pytest

from vercosa_ai_framework.canonicalizer import (
    CanonicalDocument,
    CanonicalMetadata,
    CanonicalSource,
    CanonicalSourceType,
    CanonicalizationRequest,
    CanonicalizationResult,
    CanonicalizationStatus,
    CanonicalizerAdapter,
    canonical_content_hash,
)


def test_canonical_source_types_match_initial_canonicalizer_scope():
    assert {source_type.value for source_type in CanonicalSourceType} == {
        "text",
        "markdown",
        "pdf",
        "docx",
        "html",
        "image",
        "audio",
        "video",
        "unknown",
    }


def test_canonical_source_is_traceable_provider_agnostic_metadata():
    source = CanonicalSource(
        source_uri="specs/framework/0012-canonicalizer.md",
        source_type=CanonicalSourceType.MARKDOWN,
        domain="specs",
        title="Canonicalizer",
        language="pt-BR",
        sensitivity="internal",
        trust_level="authoritative",
        metadata={"declared_by": "contract_test"},
    )

    assert source.source_type == CanonicalSourceType.MARKDOWN
    assert source.domain == "specs"
    assert source.source_id
    assert source.metadata == {"declared_by": "contract_test"}


def test_canonical_document_defaults_to_markdown_and_hashes_content():
    metadata = CanonicalMetadata(
        domain="specs",
        title="Canonicalizer",
        language="pt-BR",
        sensitivity="internal",
        trust_level="authoritative",
    )
    document = CanonicalDocument(
        document_id="spec-framework-0012",
        source_uri="specs/framework/0012-canonicalizer.md",
        source_type=CanonicalSourceType.MARKDOWN,
        domain="specs",
        title="Canonicalizer",
        content="# Canonicalizer\n",
        metadata=metadata,
        guardian_decision_refs=("guardian-decision-1",),
    )

    assert document.canonical_format == "markdown"
    assert document.content_hash == canonical_content_hash("# Canonicalizer\n")
    assert document.metadata.trust_level == "authoritative"
    assert document.guardian_decision_refs == ("guardian-decision-1",)


def test_canonical_document_rejects_non_markdown_canonical_format_initially():
    with pytest.raises(ValueError):
        CanonicalDocument(
            document_id="doc-1",
            source_uri="docs/example.txt",
            source_type=CanonicalSourceType.TEXT,
            domain="docs",
            title="Example",
            content="Example",
            canonical_format="html",
        )


def test_canonicalization_request_exposes_audit_fields_from_source():
    source = CanonicalSource(
        source_uri="docs/example.md",
        source_type=CanonicalSourceType.MARKDOWN,
        domain="docs",
    )
    request = CanonicalizationRequest(
        source=source,
        mission_id="mission-canonicalizer",
        title_hint="Example",
        guardian_decision_refs=("guardian-decision-1",),
    )

    assert request.request_id
    assert request.source_uri == "docs/example.md"
    assert request.source_type == CanonicalSourceType.MARKDOWN
    assert request.domain == "docs"
    assert request.guardian_decision_refs == ("guardian-decision-1",)


def test_canonicalization_result_is_traceable_and_status_aware():
    document = CanonicalDocument(
        document_id="doc-1",
        source_uri="docs/example.md",
        source_type=CanonicalSourceType.MARKDOWN,
        domain="docs",
        title="Example",
        content="# Example\n",
    )
    result = CanonicalizationResult(
        request_id="request-1",
        status=CanonicalizationStatus.SUCCESS,
        document=document,
        content_hash=document.content_hash,
        source_hash="source-hash",
        conversion_confidence=1.0,
    )

    assert result.success is True
    assert result.blocked is False
    assert result.document == document
    assert result.content_hash == document.content_hash


def test_blocked_result_is_not_successful():
    result = CanonicalizationResult(
        request_id="request-1",
        status=CanonicalizationStatus.BLOCKED,
        errors=("blocked by policy",),
        guardian_decision_refs=("guardian-decision-1",),
    )

    assert result.success is False
    assert result.blocked is True
    assert result.document is None


def test_canonicalizer_adapter_is_abstract():
    with pytest.raises(TypeError):
        CanonicalizerAdapter()


def test_canonicalizer_adapter_supports_any_helper_uses_declared_types():
    class TextAdapter(CanonicalizerAdapter):
        def supported_source_types(self) -> tuple[CanonicalSourceType, ...]:
            return (CanonicalSourceType.TEXT, CanonicalSourceType.MARKDOWN)

        def can_handle(self, request: CanonicalizationRequest) -> bool:
            return request.source_type in self.supported_source_types()

        def canonicalize(self, request: CanonicalizationRequest) -> CanonicalizationResult:
            return CanonicalizationResult(request_id=request.request_id, status=CanonicalizationStatus.FAILED)

    adapter = TextAdapter()

    assert adapter.supports_any((CanonicalSourceType.PDF, CanonicalSourceType.TEXT)) is True
    assert adapter.supports_any((CanonicalSourceType.AUDIO, CanonicalSourceType.VIDEO)) is False
