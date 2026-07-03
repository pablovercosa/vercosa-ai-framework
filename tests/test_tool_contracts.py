from __future__ import annotations

import pytest

from vercosa_ai_framework.tools import (
    ToolExecutionRequest,
    ToolExecutionResult,
    ToolProfile,
    ToolRegistry,
    ToolRegistryError,
)


def make_tool(
    tool_id: str,
    *,
    name: str = "workspace_text_search",
    domain: str = "framework",
    tags: tuple[str, ...] = (),
    available: bool = True,
    dangerous: bool = False,
) -> ToolProfile:
    return ToolProfile(
        tool_id=tool_id,
        name=name,
        version="1.0",
        description="Declarative contract for workspace text search.",
        provider_type="local_adapter",
        operation_type="read",
        domain=domain,
        effects=("read",),
        required_permissions=("read_workspace",),
        input_schema_ref="schemas/tools/workspace-text-search.input.json",
        output_schema_ref="schemas/tools/workspace-text-search.output.json",
        timeout=5.0,
        network_policy="none",
        data_sensitivity="internal",
        tags=tags,
        available=available,
        dangerous=dangerous,
    )


def test_tool_profile_declares_concrete_mechanism_without_execution():
    profile = make_tool("tool-search", tags=("code", "local"))

    assert profile.provider_type == "local_adapter"
    assert profile.mcp_ref is None
    assert profile.has_effects(("read",)) is True
    assert profile.has_tags(("code", "local")) is True
    assert profile.network_policy == "none"


def test_tool_execution_request_defaults_to_dry_run_contract():
    request = ToolExecutionRequest(
        tool="workspace_text_search",
        skill="search_code_in_workspace",
        mission_id="mission-1",
        workflow_id="wf-1",
        task_id="task-1",
        inputs={"query": "ToolRegistry"},
        granted_permissions=("read_workspace",),
        allowed_effects=("read",),
    )
    result = ToolExecutionResult(
        tool=request.tool,
        skill=request.skill,
        mission_id=request.mission_id,
        workflow_id=request.workflow_id,
        task_id=request.task_id,
        success=True,
        outputs={"matches": []},
    )

    assert request.dry_run is True
    assert request.allowed_effects == ("read",)
    assert result.success is True


def test_tool_registry_filters_by_name_tags_and_domain():
    registry = ToolRegistry(
        (
            make_tool("tool-search", tags=("code", "local")),
            make_tool("tool-db", name="database_read", domain="knowledge", tags=("database",)),
        )
    )

    matches = registry.filter_profiles(name="workspace_text_search", domain="framework", tags=("code",))

    assert [profile.tool_id for profile in matches] == ["tool-search"]
    assert [profile.tool_id for profile in registry.find_by_name("database_read")] == ["tool-db"]


def test_tool_registry_filters_availability_and_dangerous_tools_safely():
    registry = ToolRegistry(
        (
            make_tool("safe-tool"),
            make_tool("dangerous-tool", name="command_executor", dangerous=True),
            make_tool("unavailable-tool", name="offline_search", available=False),
        )
    )

    assert [profile.tool_id for profile in registry.filter_profiles()] == ["safe-tool"]
    assert registry.filter_profiles(name="command_executor") == ()
    assert registry.filter_profiles(name="command_executor", include_dangerous=True) != ()
    assert registry.filter_profiles(name="offline_search") == ()
    assert registry.filter_profiles(name="offline_search", available=False) != ()


def test_tool_registry_rejects_duplicates_and_blocks_missing_selection():
    registry = ToolRegistry((make_tool("tool-1"),))

    with pytest.raises(ToolRegistryError, match="already registered"):
        registry.register(make_tool("tool-1"))

    with pytest.raises(ToolRegistryError, match="no compatible"):
        registry.select_one(name="external_provider_call")
