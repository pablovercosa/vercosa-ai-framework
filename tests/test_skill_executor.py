from __future__ import annotations

import pytest

from vercosa_ai_framework.skills import SkillExecutionError, SkillExecutionRequest, SkillExecutor, SkillProfile, SkillRegistry
from vercosa_ai_framework.tools import ToolExecutionResult, ToolExecutor, ToolProfile, ToolRegistry


def make_request(*, allowed_tools: tuple[str, ...] = ("workspace_search",), permissions: tuple[str, ...] = ("read_workspace",)) -> SkillExecutionRequest:
    return SkillExecutionRequest(
        skill="skill-search",
        capability="SearchCode",
        mission_id="mission-1",
        workflow_id="wf-1",
        task_id="task-1",
        agent_assignment_id="assignment-1",
        inputs={"query": "SkillExecutor"},
        granted_permissions=permissions,
        allowed_tools=allowed_tools,
    )


def make_skill(*, required_tools: tuple[str, ...] = ("workspace_search",)) -> SkillProfile:
    return SkillProfile(
        skill_id="skill-search",
        name="search_code_in_workspace",
        version="1.0",
        description="Search code in workspace.",
        implemented_capabilities=("SearchCode",),
        domain="framework",
        required_tools=required_tools,
        permission_requirements=("read_workspace",),
    )


def make_tool(name: str, *, available: bool = True, fallback_tools: tuple[str, ...] = ()) -> ToolProfile:
    return ToolProfile(
        tool_id=name,
        name=name,
        version="1.0",
        description="Tool profile for tests.",
        provider_type="local_adapter",
        operation_type="read",
        domain="framework",
        effects=("read",),
        required_permissions=("read_workspace",),
        available=available,
        fallback_tools=fallback_tools,
    )


def test_builds_tool_execution_request_from_skill_execution_request():
    executor = SkillExecutor(
        SkillRegistry((make_skill(),)),
        ToolRegistry((make_tool("workspace_search"),)),
    )

    tool_request = executor.build_tool_request(make_request(), dry_run=True)

    assert tool_request.tool == "workspace_search"
    assert tool_request.skill == "search_code_in_workspace"
    assert tool_request.dry_run is True
    assert tool_request.allowed_effects == ("read",)
    assert tool_request.granted_permissions == ("read_workspace",)


def test_builds_tool_request_using_declared_tool_fallback():
    executor = SkillExecutor(
        SkillRegistry((make_skill(required_tools=("primary_search",)),)),
        ToolRegistry(
            (
                make_tool("primary_search", available=False, fallback_tools=("workspace_search",)),
                make_tool("workspace_search"),
            )
        ),
    )

    tool_request = executor.build_tool_request(make_request(allowed_tools=("workspace_search",)))

    assert tool_request.tool == "workspace_search"
    assert tool_request.metadata["fallback_from"] == "primary_search"


def test_rejects_tool_not_allowed_by_skill_request():
    executor = SkillExecutor(
        SkillRegistry((make_skill(),)),
        ToolRegistry((make_tool("workspace_search"),)),
    )

    with pytest.raises(SkillExecutionError, match="not allowed"):
        executor.build_tool_request(make_request(allowed_tools=("other_tool",)))


def test_execute_delegates_to_tool_executor_without_real_tools():
    def fake_adapter(request, profile):
        return ToolExecutionResult(
            tool=request.tool,
            skill=request.skill,
            mission_id=request.mission_id,
            workflow_id=request.workflow_id,
            task_id=request.task_id,
            success=True,
            outputs={"matches": [profile.name]},
            metadata={"result_ref": "tool-result-1"},
        )

    tool_registry = ToolRegistry((make_tool("workspace_search"),))
    tool_executor = ToolExecutor(tool_registry, adapter=fake_adapter)
    executor = SkillExecutor(SkillRegistry((make_skill(),)), tool_registry, tool_executor)

    result = executor.execute(make_request(), dry_run=False)

    assert result.success is True
    assert result.outputs == {"matches": ["workspace_search"]}
    assert result.tool_result_refs == ("tool-result-1",)
