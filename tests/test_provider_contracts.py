from __future__ import annotations

import pytest

from vercosa_ai_framework.providers import (
    ProviderAdapter,
    ProviderKind,
    ProviderProfile,
    ProviderRequest,
    ProviderResult,
)


def make_profile() -> ProviderProfile:
    return ProviderProfile(
        provider_id="provider-mock-search",
        name="mock_search_provider",
        version="1.0",
        description="Mock provider profile for contract tests.",
        kind=ProviderKind.MOCK,
        adapter_ref="adapters.mock.search",
        supported_operations=("search",),
        supported_domains=("framework",),
        effects=("read",),
        required_permissions=("read_workspace",),
        tags=("mock", "local"),
    )


def test_provider_kind_values_match_initial_gateway_scope():
    assert {kind.value for kind in ProviderKind} == {
        "mcp",
        "api",
        "cli",
        "filesystem",
        "database",
        "local_service",
        "mock",
    }


def test_provider_profile_declares_provider_without_execution_details():
    profile = make_profile()

    assert profile.kind == ProviderKind.MOCK
    assert profile.adapter_ref == "adapters.mock.search"
    assert profile.has_tags(("mock", "local")) is True
    assert profile.supports_domain("framework") is True
    assert profile.supports_operation("search") is True
    assert profile.enabled is True
    assert profile.secret_refs == ()


def test_provider_request_defaults_to_dry_run_and_carries_audit_context():
    request = ProviderRequest(
        operation="search",
        mission_id="mission-1",
        workflow_id="wf-1",
        task_id="task-1",
        tool_id="tool-search",
        provider_kind=ProviderKind.MOCK,
        inputs={"query": "ProviderRegistry"},
        granted_permissions=("read_workspace",),
        allowed_effects=("read",),
    )

    assert request.dry_run is True
    assert request.provider_ref is None
    assert request.provider_kind == ProviderKind.MOCK
    assert request.provider_request_id


def test_provider_result_normalizes_status_without_secrets():
    request = ProviderRequest(
        operation="search",
        mission_id="mission-1",
        workflow_id="wf-1",
        task_id="task-1",
        tool_id="tool-search",
    )
    result = ProviderResult(
        provider_request_id=request.provider_request_id,
        provider_id="provider-mock-search",
        adapter_ref="adapters.mock.search",
        operation=request.operation,
        success=True,
        status="dry_run",
        outputs={"matches": []},
        redactions_applied=("secret_refs",),
    )

    assert result.success is True
    assert result.status == "dry_run"
    assert result.outputs == {"matches": []}
    assert result.redactions_applied == ("secret_refs",)


def test_provider_adapter_is_abstract():
    with pytest.raises(TypeError):
        ProviderAdapter()
