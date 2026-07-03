from __future__ import annotations

from vercosa_ai_framework.guardian.policies import StaticGuardianPolicy
from vercosa_ai_framework.guardian.types import GuardianAction
from vercosa_ai_framework.tools import ToolExecutionRequest, ToolExecutionResult, ToolExecutor, ToolProfile, ToolRegistry


def make_request(*, dry_run: bool = True, permissions: tuple[str, ...] = ("read_workspace",), command: str | None = None) -> ToolExecutionRequest:
    inputs = {"query": "ToolExecutor"}
    if command is not None:
        inputs["command"] = command
    return ToolExecutionRequest(
        tool="workspace_search",
        skill="search_code_in_workspace",
        mission_id="mission-1",
        workflow_id="wf-1",
        task_id="task-1",
        inputs=inputs,
        granted_permissions=permissions,
        allowed_effects=("read",),
        dry_run=dry_run,
    )


def make_tool() -> ToolProfile:
    return ToolProfile(
        tool_id="tool-search",
        name="workspace_search",
        version="1.0",
        description="Search workspace through injected adapter.",
        provider_type="local_adapter",
        operation_type="read",
        domain="framework",
        effects=("read",),
        required_permissions=("read_workspace",),
        network_policy="none",
    )


def test_dry_run_does_not_call_adapter():
    calls = []

    def fake_adapter(request, profile):
        calls.append((request, profile))
        return {"called": True}

    executor = ToolExecutor(ToolRegistry((make_tool(),)), adapter=fake_adapter)

    result = executor.execute(make_request(dry_run=True))

    assert result.success is True
    assert result.outputs["dry_run"] is True
    assert calls == []


def test_non_dry_run_executes_injected_callable_only():
    calls = []

    def fake_adapter(request, profile):
        calls.append(profile.name)
        return ToolExecutionResult(
            tool=request.tool,
            skill=request.skill,
            mission_id=request.mission_id,
            workflow_id=request.workflow_id,
            task_id=request.task_id,
            success=True,
            outputs={"matches": []},
        )

    executor = ToolExecutor(ToolRegistry((make_tool(),)), adapter=fake_adapter)

    result = executor.execute(make_request(dry_run=False))
    assert result.success is True
    assert calls == ["workspace_search"]


def test_blocks_tool_when_guardian_blocks_before_adapter_is_called():
    calls = []

    def fake_adapter(request, profile):
        calls.append(profile.name)
        return {"called": True}

    executor = ToolExecutor(
        ToolRegistry((make_tool(),)),
        adapter=fake_adapter,
        guardian_engine=StaticGuardianPolicy(
            policy_id="test.block",
            title="Block tool",
            default_action=GuardianAction.BLOCK,
        ),
    )

    result = executor.execute(make_request(dry_run=False))
    assert result.success is False
    assert "guardian blocked" in result.errors[0]
    assert result.metadata["guardian_decision"] == "block"
    assert calls == []


def test_blocks_tool_when_permissions_are_missing():
    executor = ToolExecutor(ToolRegistry((make_tool(),)), adapter=lambda request, profile: {"called": True})

    result = executor.execute(make_request(dry_run=False, permissions=()))
    assert result.success is False
    assert "permissions" in result.errors[0]
