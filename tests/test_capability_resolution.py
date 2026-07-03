from __future__ import annotations

import pytest

from vercosa_ai_framework.capabilities import (
    CapabilityProfile,
    CapabilityRegistry,
    CapabilityRequest,
    CapabilityResolutionError,
    CapabilityResolver,
)
from vercosa_ai_framework.guardian.policies import StaticGuardianPolicy
from vercosa_ai_framework.guardian.types import GuardianAction
from vercosa_ai_framework.skills import SkillProfile, SkillRegistry
from vercosa_ai_framework.tools import ToolProfile, ToolRegistry


def make_request(*, permissions: tuple[str, ...] = ("read_workspace",)) -> CapabilityRequest:
    return CapabilityRequest(
        capability="SearchCode",
        mission_id="mission-1",
        workflow_id="wf-1",
        task_id="task-1",
        agent_assignment_id="assignment-1",
        inputs={"query": "CapabilityResolver"},
        granted_permissions=permissions,
    )


def make_capability() -> CapabilityProfile:
    return CapabilityProfile(
        capability_id="cap-search-code",
        name="SearchCode",
        version="1.0",
        description="Search code by intent.",
        intent="Find code context without exposing tools.",
        domain="framework",
        required_permissions=("read_workspace",),
    )


def make_skill(skill_id: str, *, required_tools: tuple[str, ...], fallback_skills: tuple[str, ...] = ()) -> SkillProfile:
    return SkillProfile(
        skill_id=skill_id,
        name=skill_id,
        version="1.0",
        description="Search code through a reusable procedure.",
        implemented_capabilities=("SearchCode",),
        domain="framework",
        required_tools=required_tools,
        fallback_skills=fallback_skills,
        permission_requirements=("read_workspace",),
        priority=10 if skill_id == "primary-skill" else 20,
    )


def make_tool(name: str, *, available: bool = True) -> ToolProfile:
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
    )


def test_resolves_capability_request_to_compatible_skill_profile():
    resolver = CapabilityResolver(
        CapabilityRegistry((make_capability(),)),
        SkillRegistry((make_skill("primary-skill", required_tools=("workspace_search",)),)),
        ToolRegistry((make_tool("workspace_search"),)),
    )

    result = resolver.resolve(make_request())

    assert result.skill.skill_id == "primary-skill"
    assert result.capability.name == "SearchCode"
    assert result.fallback_applied is False


def test_uses_declared_skill_fallback_when_primary_required_tool_is_unavailable():
    resolver = CapabilityResolver(
        CapabilityRegistry((make_capability(),)),
        SkillRegistry(
            (
                make_skill("primary-skill", required_tools=("missing_tool",), fallback_skills=("fallback-skill",)),
                make_skill("fallback-skill", required_tools=("workspace_search",)),
            )
        ),
        ToolRegistry((make_tool("workspace_search"),)),
    )

    result = resolver.resolve(make_request())

    assert result.skill.skill_id == "fallback-skill"
    assert result.fallback_applied is True
    assert result.fallback_from == "primary-skill"


def test_blocks_resolution_when_permissions_are_missing():
    resolver = CapabilityResolver(
        CapabilityRegistry((make_capability(),)),
        SkillRegistry((make_skill("primary-skill", required_tools=("workspace_search",)),)),
        ToolRegistry((make_tool("workspace_search"),)),
    )

    with pytest.raises(CapabilityResolutionError, match="permissions"):
        resolver.resolve(make_request(permissions=()))


def test_blocks_resolution_when_guardian_blocks():
    resolver = CapabilityResolver(
        CapabilityRegistry((make_capability(),)),
        SkillRegistry((make_skill("primary-skill", required_tools=("workspace_search",)),)),
        ToolRegistry((make_tool("workspace_search"),)),
        guardian_engine=StaticGuardianPolicy(
            policy_id="test.block",
            title="Block resolution",
            default_action=GuardianAction.BLOCK,
        ),
    )

    with pytest.raises(CapabilityResolutionError, match="guardian blocked"):
        resolver.resolve(make_request())
