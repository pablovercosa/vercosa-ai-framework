"""Canonicalizer MVP for plain text and Markdown.

This engine is local, deterministic, provider agnostic, and side-effect free.
It does not read files, call APIs, create embeddings, or convert binary formats.
"""

from __future__ import annotations

import re
from hashlib import sha256
from uuid import uuid5, NAMESPACE_URL

from vercosa_ai_framework.canonicalizer.adapter import CanonicalizerAdapter
from vercosa_ai_framework.canonicalizer.markdown import (
    canonicalize_markdown_text,
    extract_title,
    normalize_title,
    split_markdown_frontmatter,
    text_to_markdown,
)
from vercosa_ai_framework.canonicalizer.types import (
    CanonicalDocument,
    CanonicalMetadata,
    CanonicalSource,
    CanonicalSourceType,
    CanonicalizationRequest,
    CanonicalizationResult,
    CanonicalizationStatus,
)
from vercosa_ai_framework.knowledge.types import KnowledgeDocument, KnowledgeDomain, KnowledgeSource


PROMPT_INJECTION_WARNING = "canonicalizer.prompt_injection.suspicious_content"
SECRET_WARNING = "canonicalizer.secret.probable_secret_redacted"
UNSUPPORTED_SOURCE_WARNING = "canonicalizer.source_type.unsupported"

_PROMPT_INJECTION_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions\b", re.I),
    re.compile(r"\bdisregard\s+(?:all\s+)?(?:previous|prior|above)\s+instructions\b", re.I),
    re.compile(r"\breveal\s+(?:the\s+)?(?:system|developer)\s+(?:prompt|message|instructions)\b", re.I),
    re.compile(r"\b(?:system|developer|tool)\s+(?:prompt|message)\s*:", re.I),
    re.compile(r"\b(?:override|bypass)\s+(?:policy|policies|spec|specs|guardian|security)\b", re.I),
    re.compile(r"\b(?:exfiltrate|leak|send)\s+(?:secrets?|tokens?|credentials?)\b", re.I),
    re.compile(r"\brun\s+(?:this\s+)?command\b", re.I),
)

_SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("private_key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S)),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("assignment", re.compile(r"(?i)\b(api[_-]?key|secret|token|password|passwd|pwd)\s*[:=]\s*['\"]?[^\s'\"]{8,}")),
    ("connection_string", re.compile(r"(?i)\b(?:postgres|postgresql|mysql|mongodb|redis)://[^\s]+:[^\s]+@[^\s]+")),
    ("authorization_header", re.compile(r"(?i)\bauthorization\s*:\s*bearer\s+[^\s]+")),
)


class CanonicalizerEngine(CanonicalizerAdapter):
    """Deterministic Canonicalizer MVP for text and Markdown."""

    def supported_source_types(self) -> tuple[CanonicalSourceType, ...]:
        """Return source types supported by this engine."""

        return (CanonicalSourceType.TEXT, CanonicalSourceType.MARKDOWN)

    def can_handle(self, request: CanonicalizationRequest) -> bool:
        """Return whether the request source type is supported."""

        return request.source_type in self.supported_source_types()

    def canonicalize(self, request: CanonicalizationRequest) -> CanonicalizationResult:
        """Canonicalize content supplied in request.metadata["content"]."""

        content = request.metadata.get("content")
        if not isinstance(content, str):
            return CanonicalizationResult(
                request_id=request.request_id,
                status=CanonicalizationStatus.FAILED,
                errors=("canonicalizer.content.required",),
                guardian_decision_refs=request.guardian_decision_refs,
            )
        if request.source_type == CanonicalSourceType.TEXT:
            return self.canonicalize_text(content, request=request)
        if request.source_type == CanonicalSourceType.MARKDOWN:
            return self.canonicalize_markdown(content, request=request)
        return CanonicalizationResult(
            request_id=request.request_id,
            status=CanonicalizationStatus.FAILED,
            warnings=(UNSUPPORTED_SOURCE_WARNING,),
            errors=("canonicalizer.source_type.unsupported",),
            guardian_decision_refs=request.guardian_decision_refs,
        )

    def canonicalize_text(
        self,
        text: str,
        *,
        request: CanonicalizationRequest | None = None,
        source_uri: str = "memory://text",
        domain: str = "unknown",
        title_hint: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> CanonicalizationResult:
        """Canonicalize plain text into a CanonicalDocument."""

        resolved_request = request or _request(source_uri, CanonicalSourceType.TEXT, domain, title_hint, metadata)
        markdown = text_to_markdown(text)
        return self._build_result(markdown, text, resolved_request, frontmatter={}, frontmatter_warnings=())

    def canonicalize_markdown(
        self,
        markdown: str,
        *,
        request: CanonicalizationRequest | None = None,
        source_uri: str = "memory://markdown",
        domain: str = "unknown",
        title_hint: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> CanonicalizationResult:
        """Canonicalize Markdown with optional simple YAML frontmatter."""

        resolved_request = request or _request(source_uri, CanonicalSourceType.MARKDOWN, domain, title_hint, metadata)
        frontmatter, body, frontmatter_warnings = split_markdown_frontmatter(markdown)
        canonical_body = canonicalize_markdown_text(body)
        return self._build_result(canonical_body, markdown, resolved_request, frontmatter=frontmatter, frontmatter_warnings=frontmatter_warnings)

    def to_knowledge_document(self, document: CanonicalDocument) -> KnowledgeDocument:
        """Convert a CanonicalDocument to a KnowledgeDocument without storing it."""

        source = KnowledgeSource(
            source_uri=document.source_uri,
            source_type=document.source_type.value,
            domain=_knowledge_domain(document.domain),
            title=document.title,
            version=document.version,
            language=document.language,
            sensitivity=document.sensitivity,
            trust_level=document.trust_level,
            provenance=document.provenance,
            metadata=document.metadata.extra,
        )
        metadata = {
            **document.metadata.extra,
            "warnings": document.warnings,
            "prompt_injection_warnings": document.prompt_injection_warnings,
            "redactions_applied": document.redactions_applied,
            "canonicalizer_content_hash": document.content_hash,
        }
        return KnowledgeDocument(
            document_id=document.document_id,
            content=document.content,
            domain=_knowledge_domain(document.domain),
            title=document.title,
            source=source,
            canonical_uri=document.canonical_uri,
            source_uri=document.source_uri,
            source_type=document.source_type.value,
            version=document.version,
            canonical_format=document.canonical_format,
            language=document.language,
            sensitivity=document.sensitivity,
            trust_level=document.trust_level,
            frontmatter=document.frontmatter,
            metadata=metadata,
            provenance=document.provenance,
            redactions_applied=document.redactions_applied,
            guardian_decision_refs=document.guardian_decision_refs,
            content_hash=document.content_hash,
        )

    def _build_result(
        self,
        markdown: str,
        source_content: str,
        request: CanonicalizationRequest,
        *,
        frontmatter: dict[str, object],
        frontmatter_warnings: tuple[str, ...],
    ) -> CanonicalizationResult:
        redacted_content, redactions = redact_probable_secrets(markdown)
        redacted_frontmatter, frontmatter_redactions = _redact_metadata(frontmatter, prefix="frontmatter")
        redacted_source_metadata, source_metadata_redactions = _redact_metadata(request.source.metadata, prefix="source_metadata")
        redacted_request_metadata, request_metadata_redactions = _redact_metadata(
            {key: value for key, value in request.metadata.items() if key != "content"},
            prefix="request_metadata",
        )
        safe_source_title = _safe_title(request.source.title)
        title = _resolve_title(redacted_content, request, redacted_frontmatter, safe_source_title)
        prompt_warnings = detect_prompt_injection_warnings(redacted_content)
        metadata_redactions = (*frontmatter_redactions, *source_metadata_redactions, *request_metadata_redactions)
        warnings = tuple(dict.fromkeys((*frontmatter_warnings, *((SECRET_WARNING,) if redactions or metadata_redactions else ()), *prompt_warnings)))
        source_hash = request.source.source_hash or _sha256(source_content)
        content_hash = _sha256(redacted_content)
        document_id = str(uuid5(NAMESPACE_URL, f"{request.domain}:{request.source_uri}:{content_hash}"))
        title_source = _title_source(redacted_content, request, redacted_frontmatter, safe_source_title)

        metadata = CanonicalMetadata(
            domain=request.domain,
            title=title,
            language=request.language_hint or str(redacted_frontmatter.get("language") or request.source.language),
            sensitivity=request.sensitivity_hint or str(redacted_frontmatter.get("sensitivity") or request.source.sensitivity),
            trust_level=request.trust_level_hint or str(redacted_frontmatter.get("trust_level") or request.source.trust_level),
            usage_policy=request.usage_policy,
            privacy_policy=request.privacy_policy,
            conversion_policy=request.conversion_policy,
            redaction_policy=request.redaction_policy,
            deduplication_policy=request.deduplication_policy,
            extra={
                **redacted_source_metadata,
                **redacted_request_metadata,
                "canonicalizer": "mvp-text-markdown",
                "source_size_bytes": len(source_content.encode("utf-8")),
                "canonical_size_bytes": len(redacted_content.encode("utf-8")),
                "title_source": title_source,
                "detected_secret_types": tuple(redactions),
                "metadata_redactions": tuple(metadata_redactions),
            },
        )
        document = CanonicalDocument(
            document_id=document_id,
            content=redacted_content,
            source_uri=request.source_uri,
            source_type=request.source_type,
            domain=request.domain,
            title=title,
            version=str(redacted_frontmatter.get("version") or "1"),
            content_hash=content_hash,
            source_hash=source_hash,
            language=metadata.language,
            sensitivity=metadata.sensitivity,
            trust_level=metadata.trust_level,
            frontmatter=redacted_frontmatter,
            metadata=metadata,
            provenance={**request.source.provenance, "source_uri": request.source_uri, "source_hash": source_hash},
            conversion_confidence=1.0,
            warnings=warnings,
            redactions_applied=tuple(dict.fromkeys((*redactions, *metadata_redactions))),
            prompt_injection_warnings=prompt_warnings,
            guardian_decision_refs=request.guardian_decision_refs,
        )
        return CanonicalizationResult(
            request_id=request.request_id,
            status=CanonicalizationStatus.SUCCESS,
            document=document,
            content_hash=document.content_hash,
            source_hash=source_hash,
            warnings=warnings,
            redactions_applied=document.redactions_applied,
            prompt_injection_warnings=prompt_warnings,
            conversion_confidence=1.0,
            metadata={"title_source": title_source, "detected_secret_types": tuple(redactions)},
            provenance=document.provenance,
            guardian_decision_refs=request.guardian_decision_refs,
        )


def detect_prompt_injection_warnings(markdown: str) -> tuple[str, ...]:
    """Return warning IDs for deterministic prompt injection indicators."""

    if any(pattern.search(markdown) for pattern in _PROMPT_INJECTION_PATTERNS):
        return (PROMPT_INJECTION_WARNING,)
    return ()


def redact_probable_secrets(text: str) -> tuple[str, tuple[str, ...]]:
    """Redact probable secrets while returning only secret type metadata."""

    redacted = text
    secret_types: list[str] = []
    for secret_type, pattern in _SECRET_PATTERNS:
        if pattern.search(redacted):
            secret_types.append(secret_type)
            redacted = pattern.sub(lambda match: _redacted_value(match.group(0)), redacted)
    return redacted, tuple(dict.fromkeys(secret_types))


def _redacted_value(value: str) -> str:
    if ":" in value and "=" not in value:
        prefix = value.split(":", 1)[0]
        return f"{prefix}: [REDACTED]"
    if "=" in value:
        prefix = value.split("=", 1)[0].rstrip()
        return f"{prefix}= [REDACTED]"
    return "[REDACTED]"


def _redact_metadata(metadata: dict[str, object], *, prefix: str) -> tuple[dict[str, object], tuple[str, ...]]:
    redacted: dict[str, object] = {}
    redactions: list[str] = []
    for key, value in metadata.items():
        if isinstance(value, str):
            safe_value, detected = redact_probable_secrets(value)
            redacted[key] = safe_value
            redactions.extend(f"{prefix}.{item}" for item in detected)
        else:
            redacted[key] = value
    return redacted, tuple(dict.fromkeys(redactions))


def _request(
    source_uri: str,
    source_type: CanonicalSourceType,
    domain: str,
    title_hint: str | None,
    metadata: dict[str, object] | None,
) -> CanonicalizationRequest:
    source = CanonicalSource(source_uri=source_uri, source_type=source_type, domain=domain)
    return CanonicalizationRequest(source=source, title_hint=title_hint, metadata=dict(metadata or {}))


def _resolve_title(
    markdown: str,
    request: CanonicalizationRequest,
    frontmatter: dict[str, object],
    source_title: str,
) -> str:
    for candidate in (request.title_hint, frontmatter.get("title"), source_title):
        title = _safe_title(candidate)
        if title:
            return title
    return extract_title(markdown)[0]


def _title_source(markdown: str, request: CanonicalizationRequest, frontmatter: dict[str, object], source_title: str) -> str:
    if _safe_title(request.title_hint):
        return "request.title_hint"
    if _safe_title(frontmatter.get("title")):
        return "frontmatter.title"
    if source_title:
        return "source.title"
    return extract_title(markdown)[1]


def _safe_title(value: object) -> str:
    title, redactions = redact_probable_secrets(normalize_title(value))
    if redactions:
        return "[REDACTED]"
    return title


def _sha256(content: str) -> str:
    return sha256(content.encode("utf-8")).hexdigest()


def _knowledge_domain(value: str) -> KnowledgeDomain:
    try:
        return KnowledgeDomain(value)
    except ValueError:
        return KnowledgeDomain.UNKNOWN


__all__ = [
    "PROMPT_INJECTION_WARNING",
    "SECRET_WARNING",
    "UNSUPPORTED_SOURCE_WARNING",
    "CanonicalizerEngine",
    "detect_prompt_injection_warnings",
    "redact_probable_secrets",
]
