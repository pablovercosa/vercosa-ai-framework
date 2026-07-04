from vercosa_ai_framework.context import (
    ContextCitation,
    ContextItem,
    ContextItemType,
    ContextOmissionReason,
    ContextRequest,
    ContextSource,
    ContextSourceType,
    DeterministicContextRouter,
    SimpleTokenBudgetManager,
    TokenBudget,
    stable_content_hash,
)


def test_route_empty_candidate_list() -> None:
    request = ContextRequest(
        request_id="req-empty",
        request_goal="sem candidatos",
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=20),
    )

    package = DeterministicContextRouter().route(request)

    assert package.items == ()
    assert package.omission_reasons == ()
    assert package.token_estimate.estimated_tokens == 0


def test_route_selects_single_item() -> None:
    item = ContextItem(context_item_id="item-1", source_ref="src-1", content="texto curto")
    request = ContextRequest(
        request_id="req-one",
        request_goal="selecionar um item",
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
    )

    package = DeterministicContextRouter().route(request, candidates=(item,))

    assert package.items[0].context_item_id == "item-1"
    assert package.metadata["accepted_items"] == ("item-1",)


def test_route_preserves_selected_item_citation() -> None:
    source = ContextSource(source_id="src-1", source_type=ContextSourceType.SPEC)
    citation = ContextCitation(citation_id="cite-1", source_ref="src-1", path="specs/framework/0014.md")
    item = ContextItem(context_item_id="item-1", source_ref="src-1", content="texto citavel", citations=(citation,))
    request = ContextRequest(
        request_id="req-cite",
        request_goal="preservar citacao",
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
        candidate_sources=(source,),
        candidate_items=(item,),
    )

    package = DeterministicContextRouter().route(request)

    assert package.items[0].citations == (citation,)
    assert package.citations == (citation,)


def test_route_deduplicates_by_explicit_hash() -> None:
    shared_hash = stable_content_hash("mesmo significado")
    first = ContextItem(context_item_id="item-1", source_ref="src", content="primeiro", content_hash=shared_hash)
    duplicate = ContextItem(context_item_id="item-2", source_ref="src", content="segundo", content_hash=shared_hash)
    request = ContextRequest(
        request_id="req-hash",
        request_goal="deduplicar hash",
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
        candidate_items=(first, duplicate),
    )

    package = DeterministicContextRouter().route(request)

    assert [item.context_item_id for item in package.items] == ["item-1"]
    assert package.omission_reasons[0].omission_reason is ContextOmissionReason.DUPLICATE


def test_route_deduplicates_by_content_fallback() -> None:
    first = ContextItem(context_item_id="item-1", source_ref="src", content="conteudo igual", content_hash="hash-a")
    duplicate = ContextItem(context_item_id="item-2", source_ref="src", content="conteudo igual", content_hash="hash-b")
    request = ContextRequest(
        request_id="req-content",
        request_goal="deduplicar conteudo",
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
        candidate_items=(first, duplicate),
    )

    package = DeterministicContextRouter().route(request)

    assert [item.context_item_id for item in package.items] == ["item-1"]
    assert package.omission_reasons[0].item_ref == "item-2"
    assert package.omission_reasons[0].omission_reason is ContextOmissionReason.DUPLICATE


def test_route_omits_item_when_budget_is_insufficient() -> None:
    item = ContextItem(context_item_id="large", source_ref="src", content="x" * 100)
    request = ContextRequest(
        request_id="req-small-budget",
        request_goal="orcamento insuficiente",
        token_budget=TokenBudget(max_input_tokens=20, reserved_output_tokens=10, safety_margin_tokens=5),
        candidate_items=(item,),
    )

    package = DeterministicContextRouter().route(request)

    assert package.items == ()
    assert package.omission_reasons[0].omission_reason is ContextOmissionReason.TOKEN_BUDGET_EXCEEDED


def test_budget_manager_reserves_output_tokens() -> None:
    budget = TokenBudget(max_input_tokens=50, reserved_output_tokens=20, instruction_tokens=5)

    result = SimpleTokenBudgetManager().evaluate_items((), budget)

    assert result.reserved_output_tokens == 20
    assert result.available_context_tokens == 25
    assert result.remaining_context_tokens == 25


def test_route_orders_candidates_deterministically_by_rank_priority_and_id() -> None:
    later = ContextItem(context_item_id="b", source_ref="src", content="b", rank=2)
    first = ContextItem(context_item_id="a", source_ref="src", content="a", rank=1, metadata={"priority": 1})
    second = ContextItem(context_item_id="c", source_ref="src", content="c", rank=1, metadata={"priority": 2})
    request = ContextRequest(
        request_id="req-order",
        request_goal="ordenar",
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
        candidate_items=(later, second, first),
    )

    package = DeterministicContextRouter().route(request)

    assert [item.context_item_id for item in package.items] == ["a", "c", "b"]


def test_package_contains_omission_reasons() -> None:
    item = ContextItem(context_item_id="item-1", source_ref="src", content="sem citacao", item_type=ContextItemType.EVIDENCE)
    request = ContextRequest(
        request_id="req-omit-reason",
        request_goal="registrar omissao",
        citation_required=True,
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
        candidate_items=(item,),
    )

    package = DeterministicContextRouter().route(request)

    assert package.omission_reasons[0].item_ref == "item-1"
    assert package.omission_reasons[0].omission_reason is ContextOmissionReason.MISSING_CITATION


def test_route_is_repeatable_for_same_input() -> None:
    item = ContextItem(context_item_id="item-1", source_ref="src", content="estavel")
    request = ContextRequest(
        request_id="req-repeat",
        request_goal="repetir",
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
        candidate_items=(item,),
    )
    router = DeterministicContextRouter()

    assert router.route(request) == router.route(request)


def test_items_without_citation_are_allowed_for_non_citable_types_with_no_warning() -> None:
    item = ContextItem(context_item_id="meta", source_ref="src", content="metadado", item_type=ContextItemType.METADATA)
    request = ContextRequest(
        request_id="req-metadata",
        request_goal="permitir metadado sem citacao",
        citation_required=True,
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
        candidate_items=(item,),
    )

    package = DeterministicContextRouter().route(request)

    assert [selected.context_item_id for selected in package.items] == ["meta"]
    assert package.omission_reasons == ()
    assert package.warnings == ()


def test_evidence_without_citation_is_omitted_even_when_citation_is_not_globally_required() -> None:
    item = ContextItem(context_item_id="evidence", source_ref="src", content="evidencia", item_type=ContextItemType.EVIDENCE)
    request = ContextRequest(
        request_id="req-warning",
        request_goal="omitir evidencia sem citacao",
        citation_required=False,
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
        candidate_items=(item,),
    )

    package = DeterministicContextRouter().route(request)

    assert package.items == ()
    assert package.omission_reasons[0].omission_reason is ContextOmissionReason.MISSING_CITATION


def test_excerpt_without_citation_is_allowed_with_warning_when_not_required() -> None:
    item = ContextItem(context_item_id="excerpt", source_ref="src", content="trecho", item_type=ContextItemType.EXCERPT)
    request = ContextRequest(
        request_id="req-excerpt-warning",
        request_goal="avisar trecho sem citacao",
        citation_required=False,
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
        candidate_items=(item,),
    )

    package = DeterministicContextRouter().route(request)

    assert [selected.context_item_id for selected in package.items] == ["excerpt"]
    assert package.warnings == ("context_item_without_citation:excerpt",)


def test_router_does_not_require_external_callables() -> None:
    router = DeterministicContextRouter(budget_manager=SimpleTokenBudgetManager())
    request = ContextRequest(
        request_id="req-no-external",
        request_goal="sem chamadas externas",
        token_budget=TokenBudget(max_input_tokens=100, reserved_output_tokens=10),
    )

    package = router.route(request)

    assert package.metadata["router"] == "deterministic"
    assert package.sources == ()
