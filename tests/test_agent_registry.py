from __future__ import annotations

import pytest

from vercosa_ai_framework.agents import AgentProfile, AgentRegistry, AgentRegistryError, AgentRole


def make_profile(
    agent_profile_id: str,
    *,
    role: AgentRole = AgentRole.DEVELOPER,
    domain: str = "application",
    tags: tuple[str, ...] = (),
    capabilities: tuple[str, ...] = ("ReadContext",),
    task_types: tuple[str, ...] = ("implementation",),
    risk_range: tuple[str, ...] = ("low", "medium"),
) -> AgentProfile:
    return AgentProfile(
        agent_profile_id=agent_profile_id,
        role=role,
        domain=domain,
        supported_task_types=task_types,
        supported_capabilities=capabilities,
        tags=tags,
        risk_range=risk_range,
    )


def test_registry_registers_and_lists_agents_deterministically():
    registry = AgentRegistry()
    developer = make_profile("dev-b", role=AgentRole.DEVELOPER)
    architect = make_profile("architect-a", role=AgentRole.ARCHITECT, domain="framework")

    registry.register(developer)
    registry.register(architect)

    assert [profile.agent_profile_id for profile in registry.list_profiles()] == ["architect-a", "dev-b"]
    assert registry.get("dev-b") == developer


def test_registry_rejects_duplicate_agent_profile_ids():
    registry = AgentRegistry((make_profile("agent-1"),))

    with pytest.raises(AgentRegistryError, match="already registered"):
        registry.register(make_profile("agent-1"))


def test_registry_finds_agents_by_role():
    registry = AgentRegistry(
        (
            make_profile("dev-1", role=AgentRole.DEVELOPER),
            make_profile("reviewer-1", role=AgentRole.REVIEWER),
            make_profile("dev-2", role=AgentRole.DEVELOPER, domain="framework"),
        )
    )

    assert [profile.agent_profile_id for profile in registry.find_by_role(AgentRole.DEVELOPER)] == [
        "dev-1",
        "dev-2",
    ]
    assert [profile.agent_profile_id for profile in registry.find_by_role("reviewer")] == ["reviewer-1"]


def test_registry_filters_by_tags_domain_and_capabilities():
    registry = AgentRegistry(
        (
            make_profile(
                "framework-python",
                role=AgentRole.IMPLEMENTATION_ARCHITECT,
                domain="framework",
                tags=("python", "contracts"),
                capabilities=("ReadContext", "SearchCode", "RunValidation"),
                risk_range=("low", "medium", "high"),
            ),
            make_profile(
                "docs-python",
                role=AgentRole.DOCUMENTATION,
                domain="documentation",
                tags=("python",),
                capabilities=("ReadContext", "GenerateDocumentation"),
            ),
        )
    )

    matches = registry.filter_profiles(
        role=AgentRole.IMPLEMENTATION_ARCHITECT,
        domain="framework",
        tags=("python", "contracts"),
        required_capabilities=("ReadContext", "RunValidation"),
        task_type="implementation",
        risk_level="high",
    )

    assert [profile.agent_profile_id for profile in matches] == ["framework-python"]


def test_registry_select_one_blocks_when_no_agent_is_compatible():
    registry = AgentRegistry((make_profile("dev-1", capabilities=("ReadContext",)),))

    with pytest.raises(AgentRegistryError, match="no compatible"):
        registry.select_one(required_capabilities=("RunValidation",))
