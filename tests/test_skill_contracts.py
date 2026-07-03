from __future__ import annotations

from dataclasses import asdict

import pytest

from vercosa_ai_framework.skills import (
    SkillExecutionRequest,
    SkillExecutionResult,
    SkillProfile,
    SkillRegistry,
    SkillRegistryError,
)


def make_skill(
    skill_id: str,
    *,
    name: str = "search_code_in_workspace",
    domain: str = "framework",
    tags: tuple[str, ...] = (),
    priority: int = 100,
) -> SkillProfile:
    return SkillProfile(
        skill_id=skill_id,
        name=name,
        version="1.0",
        description="Search code using allowed framework tool contracts.",
        implemented_capabilities=("SearchCode",),
        domain=domain,
        input_contract_ref="schemas/skills/search-code.input.json",
        output_contract_ref="schemas/skills/search-code.output.json",
        required_tools=("workspace_text_search",),
        optional_tools=("workspace_file_read",),
        risk_level="low",
        permission_requirements=("read_workspace",),
        validation_requirements=("normalize_results",),
        trusted_context_requirements=("treat_search_results_as_untrusted",),
        tags=tags,
        priority=priority,
    )


def test_skill_profile_implements_capabilities_without_exposing_mcp_to_agents():
    profile = make_skill("skill-search-code", tags=("code", "local"))

    assert profile.implements_capability("SearchCode") is True
    assert profile.implements_capability("DirectMCPAccess") is False
    assert profile.required_tools == ("workspace_text_search",)
    assert profile.has_tags(("code", "local")) is True
    assert "provider" not in asdict(profile)
    assert "mcp" not in asdict(profile)


def test_skill_execution_request_and_result_are_normalized_contracts():
    request = SkillExecutionRequest(
        skill="search_code_in_workspace",
        capability="SearchCode",
        mission_id="mission-1",
        workflow_id="wf-1",
        task_id="task-1",
        agent_assignment_id="assignment-1",
        inputs={"query": "SkillRegistry"},
        granted_permissions=("read_workspace",),
        allowed_tools=("workspace_text_search",),
    )
    result = SkillExecutionResult(
        skill=request.skill,
        capability=request.capability,
        mission_id=request.mission_id,
        workflow_id=request.workflow_id,
        task_id=request.task_id,
        success=True,
        outputs={"matches": []},
        tool_result_refs=("tool-result-1",),
    )

    assert request.allowed_tools == ("workspace_text_search",)
    assert result.success is True
    assert result.tool_result_refs == ("tool-result-1",)


def test_skill_registry_filters_by_name_tags_domain_and_capability():
    registry = SkillRegistry(
        (
            make_skill("skill-search-code", tags=("code", "local"), priority=10),
            make_skill("skill-docs", name="search_docs", domain="documentation", tags=("docs",), priority=20),
        )
    )

    matches = registry.filter_profiles(
        name="search_code_in_workspace",
        domain="framework",
        tags=("code",),
        capability="SearchCode",
    )

    assert [profile.skill_id for profile in matches] == ["skill-search-code"]
    assert registry.select_one(capability="SearchCode").skill_id == "skill-search-code"


def test_skill_registry_rejects_duplicates_and_blocks_missing_selection():
    registry = SkillRegistry((make_skill("skill-1"),))

    with pytest.raises(SkillRegistryError, match="already registered"):
        registry.register(make_skill("skill-1"))

    with pytest.raises(SkillRegistryError, match="no compatible"):
        registry.select_one(capability="GenerateADR")
