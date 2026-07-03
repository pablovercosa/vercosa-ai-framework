from __future__ import annotations

from vercosa_ai_framework.providers import ProviderGateway, ProviderKind, ProviderProfile, ProviderRegistry
from vercosa_ai_framework.tools import ToolExecutionRequest, ToolExecutor, ToolProfile, ToolRegistry


def make_tool() -> ToolProfile:
    return ToolProfile(
        tool_id="tool-search",
        name="workspace_search",
        version="1.0",
        description="Search workspace through Provider Gateway.",
        provider_type="mock",
        provider_ref="provider-search",
        operation_type="search",
        domain="framework",
        effects=("read",),
        required_permissions=("read_workspace",),
        timeout=2.0,
    )


def make_provider() -> ProviderProfile:
    return ProviderProfile(
        provider_id="provider-search",
        name="mock_search_provider",
        version="1.0",
        description="Mock provider fixture.",
        kind=ProviderKind.MOCK,
        adapter_ref="adapters.search",
        supported_operations=("search",),
        effects=("read",),
        required_permissions=("read_workspace",),
    )


def make_request(*, dry_run: bool = False) -> ToolExecutionRequest:
    return ToolExecutionRequest(
        tool="workspace_search",
        skill="search_code_in_workspace",
        mission_id="mission-1",
        workflow_id="wf-1",
        task_id="task-1",
        inputs={"query": "ToolExecutor"},
        granted_permissions=("read_workspace",),
        allowed_effects=("read",),
        dry_run=dry_run,
    )


def test_tool_executor_delegates_dry_run_to_provider_gateway():
    calls = []
    gateway = ProviderGateway(
        ProviderRegistry((make_provider(),)),
        adapters={"adapters.search": lambda request, profile: calls.append(profile.provider_id)},
    )
    executor = ToolExecutor(ToolRegistry((make_tool(),)), provider_gateway=gateway)

    result = executor.execute(make_request(dry_run=True))

    assert result.success is True
    assert result.outputs["dry_run"] is True
    assert result.metadata["provider_id"] == "provider-search"
    assert result.metadata["provider_status"] == "dry_run"
    assert calls == []


def test_tool_executor_delegates_execution_to_provider_gateway():
    seen = []

    def adapter(request, profile):
        seen.append((request.tool_execution_request_id, request.dry_run, profile.provider_id))
        return {"matches": [request.inputs["query"]]}

    gateway = ProviderGateway(ProviderRegistry((make_provider(),)), adapters={"adapters.search": adapter})
    executor = ToolExecutor(ToolRegistry((make_tool(),)), provider_gateway=gateway)

    request = make_request(dry_run=False)
    result = executor.execute(request)

    assert result.success is True
    assert result.outputs == {"matches": ["ToolExecutor"]}
    assert result.metadata["provider_status"] == "success"
    assert seen == [(request.request_id, False, "provider-search")]
