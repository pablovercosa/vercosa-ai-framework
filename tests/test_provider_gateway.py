from __future__ import annotations

from vercosa_ai_framework.guardian.policies import StaticGuardianPolicy
from vercosa_ai_framework.guardian.types import GuardianAction
from vercosa_ai_framework.providers import ProviderGateway, ProviderKind, ProviderProfile, ProviderRegistry, ProviderRequest, ProviderResult


def make_provider(
    provider_id: str = "provider-primary",
    *,
    adapter_ref: str = "adapters.primary",
    enabled: bool = True,
    fallback_providers: tuple[str, ...] = (),
) -> ProviderProfile:
    return ProviderProfile(
        provider_id=provider_id,
        name=provider_id,
        version="1.0",
        description="Provider gateway fixture.",
        kind=ProviderKind.MOCK,
        adapter_ref=adapter_ref,
        supported_operations=("search",),
        effects=("read",),
        required_permissions=("read_workspace",),
        default_timeout=3.0,
        enabled=enabled,
        fallback_providers=fallback_providers,
    )


def make_request(*, provider_ref: str | None = "provider-primary", dry_run: bool = False, fallback_allowed: bool = False) -> ProviderRequest:
    return ProviderRequest(
        operation="search",
        mission_id="mission-1",
        workflow_id="wf-1",
        task_id="task-1",
        tool_id="tool-search",
        provider_ref=provider_ref,
        provider_kind=ProviderKind.MOCK,
        inputs={"query": "ProviderGateway"},
        granted_permissions=("read_workspace",),
        allowed_effects=("read",),
        dry_run=dry_run,
        fallback_allowed=fallback_allowed,
    )


def test_provider_gateway_dry_run_validates_without_calling_adapter():
    calls = []
    gateway = ProviderGateway(
        ProviderRegistry((make_provider(),)),
        adapters={"adapters.primary": lambda request, profile: calls.append(profile.provider_id)},
    )

    result = gateway.execute(make_request(dry_run=True))

    assert result.success is True
    assert result.status == "dry_run"
    assert result.outputs["dry_run"] is True
    assert result.timeout_applied == 3.0
    assert calls == []


def test_provider_gateway_executes_callable_adapter_after_guardian_allows():
    gateway = ProviderGateway(
        ProviderRegistry((make_provider(),)),
        adapters={"adapters.primary": lambda request, profile: {"provider": profile.provider_id, "query": request.inputs["query"]}},
        guardian_engine=StaticGuardianPolicy(policy_id="test.allow", title="Allow", default_action=GuardianAction.ALLOW),
    )

    result = gateway.execute(make_request())

    assert result.success is True
    assert result.outputs == {"provider": "provider-primary", "query": "ProviderGateway"}
    assert result.guardian_decision_refs == (result.provider_request_id,)


def test_provider_gateway_blocks_when_guardian_blocks_before_adapter():
    calls = []
    gateway = ProviderGateway(
        ProviderRegistry((make_provider(),)),
        adapters={"adapters.primary": lambda request, profile: calls.append(profile.provider_id)},
        guardian_engine=StaticGuardianPolicy(policy_id="test.block", title="Block", default_action=GuardianAction.BLOCK),
    )

    result = gateway.execute(make_request())

    assert result.success is False
    assert result.status == "blocked"
    assert "guardian blocked" in result.errors[0]
    assert calls == []


def test_provider_gateway_blocks_disabled_provider():
    gateway = ProviderGateway(ProviderRegistry((make_provider(enabled=False),)))

    result = gateway.execute(make_request())

    assert result.success is False
    assert result.status == "blocked"
    assert "disabled" in result.blocked_reason


def test_provider_gateway_falls_back_to_compatible_provider():
    primary = make_provider(fallback_providers=("provider-fallback",))
    fallback = make_provider("provider-fallback", adapter_ref="adapters.fallback")

    def fail(request: ProviderRequest, profile: ProviderProfile) -> ProviderResult:
        return ProviderResult(
            provider_request_id=request.provider_request_id,
            provider_id=profile.provider_id,
            adapter_ref=profile.adapter_ref,
            operation=request.operation,
            success=False,
            status="failed",
            errors=("primary failed",),
        )

    gateway = ProviderGateway(
        ProviderRegistry((primary, fallback)),
        adapters={"adapters.primary": fail, "adapters.fallback": lambda request, profile: {"fallback": profile.provider_id}},
    )

    result = gateway.execute(make_request(fallback_allowed=True))

    assert result.success is True
    assert result.outputs == {"fallback": "provider-fallback"}
    assert result.fallback_from == "provider-primary"
    assert result.fallback_to == "provider-fallback"
