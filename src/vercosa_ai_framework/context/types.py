"""Context Router and Token Budget contract types.

These contracts are deterministic and provider agnostic. They do not call LLMs,
providers, embeddings, databases, filesystems, runtimes, tools, or MCPs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
from typing import Any

from vercosa_ai_framework.policy.types import ResolvedPolicySet


class ContextSourceType(str, Enum):
    """Initial source categories from Spec 0014."""

    SPEC = "spec"
    ADR = "adr"
    README = "readme"
    CANONICAL_DOCUMENT = "canonical_document"
    TEXT_SEARCH_RESULT = "text_search_result"
    SEMANTIC_INDEX_RESULT = "semantic_index_result"
    TASK_RECORD = "task_record"
    DECISION_RECORD = "decision_record"
    VALIDATION_RESULT = "validation_result"
    ARTIFACT = "artifact"
    CONVERSATION = "conversation"
    UNKNOWN = "unknown"


class ContextItemType(str, Enum):
    """Kinds of payloads that can appear in a context package."""

    EXCERPT = "excerpt"
    SUMMARY = "summary"
    REFERENCE = "reference"
    INSTRUCTION = "instruction"
    METADATA = "metadata"
    EVIDENCE = "evidence"


class ContextOmissionReason(str, Enum):
    """Reasons why a candidate context item was omitted."""

    TOKEN_BUDGET_EXCEEDED = "token_budget_exceeded"
    POLICY_DENIED = "policy_denied"
    SENSITIVITY_DENIED = "sensitivity_denied"
    LOW_RELEVANCE = "low_relevance"
    DUPLICATE = "duplicate"
    STALE_INDEX = "stale_index"
    MISSING_CITATION = "missing_citation"
    UNCANONICALIZED_SOURCE = "uncanonicalized_source"
    GUARDIAN_BLOCKED = "guardian_blocked"
    REQUIRES_APPROVAL = "requires_approval"
    PROMPT_INJECTION_RISK = "prompt_injection_risk"
    UNTRUSTED_SOURCE = "untrusted_source"
    CACHE_INVALID = "cache_invalid"
    OUTSIDE_SCOPE = "outside_scope"


class ContextRiskLevel(str, Enum):
    """Risk level for context sources, items, and packages."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class MemoryLayerType(str, Enum):
    """Memory layers from Spec 0014."""

    EPHEMERAL_CONTEXT = "ephemeral_context"
    WORKING_MEMORY = "working_memory"
    PERSISTENT_MEMORY = "persistent_memory"
    CANONICAL_KNOWLEDGE = "canonical_knowledge"
    DERIVED_INDEXES = "derived_indexes"
    CONTEXT_PACKAGES = "context_packages"
    AUDIT_MEMORY = "audit_memory"


@dataclass(frozen=True, slots=True)
class ContextSource:
    """Traceable source for a candidate or selected context item."""

    source_id: str
    source_type: ContextSourceType = ContextSourceType.UNKNOWN
    domain: str = "unknown"
    uri: str | None = None
    content_hash: str | None = None
    trust_level: str = "unknown"
    sensitivity: str = "public"
    canonical_ref: str | None = None
    policy_refs: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ContextCitation:
    """Auditable reference to the origin of a context item."""

    citation_id: str
    source_ref: str
    document_id: str | None = None
    canonical_uri: str | None = None
    source_uri: str | None = None
    path: str | None = None
    heading: str | None = None
    line_range: tuple[int, int] | None = None
    chunk_id: str | None = None
    content_hash: str | None = None
    retrieved_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ContextRedaction:
    """Record of removed or masked context without exposing the original value."""

    redaction_id: str
    redaction_type: str
    target_ref: str
    policy_ref: str | None = None
    reason: str = ""
    approximate_location: str | None = None
    replacement: str | None = None
    guardian_decision_ref: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class TokenBudget:
    """Token limits for one context routing request."""

    max_input_tokens: int
    reserved_output_tokens: int = 0
    max_output_tokens: int | None = None
    instruction_tokens: int = 0
    safety_margin_tokens: int = 0

    @property
    def available_context_tokens(self) -> int:
        """Return the non-negative budget left for context items."""

        return max(0, self.max_input_tokens - self.reserved_output_tokens - self.instruction_tokens - self.safety_margin_tokens)


@dataclass(frozen=True, slots=True)
class TokenEstimate:
    """Deterministic token estimate for content, item, or package."""

    estimated_tokens: int
    estimation_method: str = "chars_div_4_ceil"
    confidence: str = "low"
    content_chars: int = 0


@dataclass(frozen=True, slots=True)
class TokenBudgetDecision:
    """Decision indicating whether an item fits the available token budget."""

    item_ref: str
    included: bool
    token_estimate: TokenEstimate
    tokens_before: int
    tokens_after: int
    available_context_tokens: int
    omission_reason: ContextOmissionReason | None = None
    reason: str = ""


@dataclass(frozen=True, slots=True)
class TokenBudgetResult:
    """Aggregate deterministic budget result for a set of context items."""

    token_estimate: TokenEstimate
    reserved_output_tokens: int
    available_context_tokens: int
    used_context_tokens: int
    remaining_context_tokens: int
    accepted_items: tuple[str, ...] = field(default_factory=tuple)
    omitted_items: tuple[TokenBudgetDecision, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class ContextItem:
    """Context payload candidate or selected item."""

    context_item_id: str
    source_ref: str
    content: str = ""
    content_ref: str | None = None
    item_type: ContextItemType = ContextItemType.EXCERPT
    rank: int = 0
    reason_selected: str = ""
    token_estimate: TokenEstimate | None = None
    citations: tuple[ContextCitation, ...] = field(default_factory=tuple)
    redactions: tuple[ContextRedaction, ...] = field(default_factory=tuple)
    trust_level: str = "unknown"
    sensitivity: str = "public"
    risk_level: ContextRiskLevel = ContextRiskLevel.UNKNOWN
    is_untrusted_data: bool = True
    content_hash: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.content_hash is None and self.content:
            object.__setattr__(self, "content_hash", stable_content_hash(self.content))


@dataclass(frozen=True, slots=True)
class ContextRequest:
    """Input contract for Context Router implementations."""

    request_id: str
    request_goal: str
    mission_id: str | None = None
    workflow_id: str | None = None
    task_id: str | None = None
    attempt_id: str | None = None
    agent_assignment_id: str | None = None
    task_type: str | None = None
    agent_role: str | None = None
    domains_requested: tuple[str, ...] = field(default_factory=tuple)
    required_sources: tuple[str, ...] = field(default_factory=tuple)
    optional_sources: tuple[str, ...] = field(default_factory=tuple)
    scope: str = ""
    sensitivity_allowed: tuple[str, ...] = ("public", "internal")
    trust_level_min: str | None = None
    token_budget: TokenBudget = field(default_factory=lambda: TokenBudget(max_input_tokens=4096, reserved_output_tokens=1024))
    citation_required: bool = False
    policy_refs: tuple[str, ...] = field(default_factory=tuple)
    resolved_policy_set: ResolvedPolicySet | None = None
    guardian_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    prior_context_package_refs: tuple[str, ...] = field(default_factory=tuple)
    candidate_sources: tuple[ContextSource, ...] = field(default_factory=tuple)
    candidate_items: tuple[ContextItem, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ContextPackage:
    """Traceable context bundle produced by a Context Router."""

    context_package_id: str
    request_id: str
    request_goal: str
    scope: str
    items: tuple[ContextItem, ...] = field(default_factory=tuple)
    sources: tuple[ContextSource, ...] = field(default_factory=tuple)
    citations: tuple[ContextCitation, ...] = field(default_factory=tuple)
    token_estimate: TokenEstimate = field(default_factory=lambda: TokenEstimate(estimated_tokens=0))
    output_token_reservation: int = 0
    redactions: tuple[ContextRedaction, ...] = field(default_factory=tuple)
    omission_reasons: tuple[TokenBudgetDecision, ...] = field(default_factory=tuple)
    policy_refs: tuple[str, ...] = field(default_factory=tuple)
    guardian_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    model_requirements: dict[str, Any] = field(default_factory=dict)
    content_hash: str = ""
    cache_key: str | None = None
    warnings: tuple[str, ...] = field(default_factory=tuple)
    created_at: str = "deterministic"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class MemoryLayer:
    """Describes a memory layer without binding it to storage technology."""

    layer_type: MemoryLayerType
    name: str
    description: str = ""
    storage_agnostic: bool = True
    provider_agnostic: bool = True
    runtime_agnostic: bool = True
    model_agnostic: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


def stable_content_hash(content: str) -> str:
    """Return a stable SHA-256 hash for text content."""

    return sha256(content.encode("utf-8")).hexdigest()


def stable_id(prefix: str, *parts: object) -> str:
    """Build a deterministic identifier from stable string parts."""

    raw = "\x1f".join(str(part) for part in parts)
    return f"{prefix}_{sha256(raw.encode('utf-8')).hexdigest()[:16]}"


__all__ = [
    "ContextCitation",
    "ContextItem",
    "ContextItemType",
    "ContextOmissionReason",
    "ContextPackage",
    "ContextRedaction",
    "ContextRequest",
    "ContextRiskLevel",
    "ContextSource",
    "ContextSourceType",
    "MemoryLayer",
    "MemoryLayerType",
    "TokenBudget",
    "TokenBudgetDecision",
    "TokenBudgetResult",
    "TokenEstimate",
    "stable_content_hash",
    "stable_id",
]
