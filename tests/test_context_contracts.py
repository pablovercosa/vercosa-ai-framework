from vercosa_ai_framework.context import (
    ContextCitation,
    ContextItem,
    ContextItemType,
    ContextOmissionReason,
    ContextPackage,
    ContextRequest,
    ContextSource,
    ContextSourceType,
    DeterministicContextRouter,
    MemoryLayer,
    MemoryLayerType,
    SimpleTokenBudgetManager,
    TokenBudget,
)


def test_create_context_source() -> None:
    source = ContextSource(
        source_id="spec-0014",
        source_type=ContextSourceType.SPEC,
        domain="specs",
        uri="specs/framework/0014-context-router-token-budget-memory.md",
        content_hash="hash-1",
        trust_level="high",
    )

    assert source.source_id == "spec-0014"
    assert source.source_type is ContextSourceType.SPEC
    assert source.domain == "specs"


def test_create_context_citation() -> None:
    citation = ContextCitation(
        citation_id="cite-1",
        source_ref="spec-0014",
        path="specs/framework/0014-context-router-token-budget-memory.md",
        line_range=(391, 400),
    )

    assert citation.source_ref == "spec-0014"
    assert citation.line_range == (391, 400)


def test_create_context_item_and_hash() -> None:
    item = ContextItem(
        context_item_id="item-1",
        source_ref="spec-0014",
        content="Reservar tokens de output antes de preencher contexto.",
        item_type=ContextItemType.EVIDENCE,
    )

    assert item.item_type is ContextItemType.EVIDENCE
    assert item.content_hash is not None


def test_create_context_package() -> None:
    package = ContextPackage(
        context_package_id="pkg-1",
        request_id="req-1",
        request_goal="testar contratos",
        scope="unit-test",
    )

    assert package.context_package_id == "pkg-1"
    assert package.items == ()


def test_router_deduplicates_by_content_hash() -> None:
    source = ContextSource(source_id="src-1", source_type=ContextSourceType.SPEC)
    first = ContextItem(context_item_id="item-1", source_ref="src-1", content="conteudo duplicado", rank=1)
    duplicate = ContextItem(context_item_id="item-2", source_ref="src-1", content="conteudo duplicado", rank=2)
    request = ContextRequest(
        request_id="req-dedupe",
        request_goal="deduplicar",
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
        candidate_sources=(source,),
        candidate_items=(first, duplicate),
    )

    package = DeterministicContextRouter().route(request)

    assert [item.context_item_id for item in package.items] == ["item-1"]
    assert package.omission_reasons[0].item_ref == "item-2"
    assert package.omission_reasons[0].omission_reason is ContextOmissionReason.DUPLICATE


def test_router_respects_token_budget_and_records_omission() -> None:
    source = ContextSource(source_id="src-1", source_type=ContextSourceType.SPEC)
    small = ContextItem(context_item_id="small", source_ref="src-1", content="abcd", rank=1)
    large = ContextItem(context_item_id="large", source_ref="src-1", content="x" * 80, rank=2)
    request = ContextRequest(
        request_id="req-budget",
        request_goal="limitar tokens",
        token_budget=TokenBudget(max_input_tokens=20, reserved_output_tokens=10),
        candidate_sources=(source,),
        candidate_items=(small, large),
    )

    package = DeterministicContextRouter().route(request)

    assert [item.context_item_id for item in package.items] == ["small"]
    assert package.omission_reasons[0].item_ref == "large"
    assert package.omission_reasons[0].omission_reason is ContextOmissionReason.TOKEN_BUDGET_EXCEEDED


def test_router_preserves_citations() -> None:
    source = ContextSource(source_id="src-1", source_type=ContextSourceType.ADR)
    citation = ContextCitation(citation_id="cite-1", source_ref="src-1", path="knowledge/decisions/example.md")
    item = ContextItem(
        context_item_id="item-1",
        source_ref="src-1",
        content="Context Router preserva citacoes.",
        citations=(citation,),
    )
    request = ContextRequest(
        request_id="req-citations",
        request_goal="preservar citacoes",
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
        candidate_sources=(source,),
        candidate_items=(item,),
    )

    package = DeterministicContextRouter().route(request)

    assert package.items[0].citations == (citation,)
    assert package.citations == (citation,)


def test_token_budget_output_reservation() -> None:
    budget = TokenBudget(
        max_input_tokens=100,
        reserved_output_tokens=25,
        instruction_tokens=10,
        safety_margin_tokens=5,
    )

    assert budget.available_context_tokens == 60
    assert SimpleTokenBudgetManager().available_context_tokens(budget) == 60


def test_simple_token_budget_manager_decides_fit_and_omit() -> None:
    manager = SimpleTokenBudgetManager(chars_per_token=4)
    budget = TokenBudget(max_input_tokens=3, reserved_output_tokens=1)
    item = ContextItem(context_item_id="item-1", source_ref="src-1", content="123456789")

    decision = manager.decide_item(item, budget)

    assert decision.included is False
    assert decision.omission_reason is ContextOmissionReason.TOKEN_BUDGET_EXCEEDED


def test_router_is_deterministic() -> None:
    source = ContextSource(source_id="src-1", source_type=ContextSourceType.SPEC)
    item = ContextItem(context_item_id="item-1", source_ref="src-1", content="conteudo estavel")
    request = ContextRequest(
        request_id="req-stable",
        request_goal="determinismo",
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
        candidate_sources=(source,),
        candidate_items=(item,),
        policy_refs=("policy-a",),
    )
    router = DeterministicContextRouter()

    first = router.route(request)
    second = router.route(request)

    assert first == second
    assert first.context_package_id == second.context_package_id
    assert first.cache_key == second.cache_key


def test_create_memory_layer() -> None:
    layer = MemoryLayer(layer_type=MemoryLayerType.CONTEXT_PACKAGES, name="context packages")

    assert layer.layer_type is MemoryLayerType.CONTEXT_PACKAGES
    assert layer.storage_agnostic is True
