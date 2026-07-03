from __future__ import annotations

from dataclasses import asdict

import pytest

from vercosa_ai_framework.capabilities import (
    CapabilityProfile,
    CapabilityRegistry,
    CapabilityRegistryError,
    CapabilityRequest,
)


def make_capability(
    capability_id: str,
    *,
    name: str = "SearchCode",
    domain: str = "framework",
    tags: tuple[str, ...] = (),
) -> CapabilityProfile:
    return CapabilityProfile(
        capability_id=capability_id,
        name=name,
        version="1.0",
        description="Search code through an abstract capability boundary.",
        intent="Find relevant code context without exposing concrete tools to agents.",
        domain=domain,
        input_schema_ref="schemas/capabilities/search-code.input.json",
        output_schema_ref="schemas/capabilities/search-code.output.json",
        risk_level="low",
        required_permissions=("read_workspace",),
        allowed_agent_roles=("implementation_architect", "developer"),
        allowed_task_types=("implementation", "review"),
        tags=tags,
        guardian_policy_refs=("Security by Design",),
    )


def test_capability_profile_describes_intent_not_tools_or_mcp():
    profile = make_capability("cap-search-code", tags=("code", "local"))

    assert profile.name == "SearchCode"
    assert profile.intent.startswith("Find relevant code context")
    assert profile.allows_agent_role("implementation_architect") is True
    assert profile.allows_task_type("implementation") is True
    assert profile.has_tags(("code", "local")) is True
    assert "tool" not in asdict(profile)
    assert "provider" not in asdict(profile)
    assert "mcp" not in asdict(profile)


def test_capability_request_is_traceable_and_abstract():
    request = CapabilityRequest(
        capability="SearchCode",
        mission_id="mission-1",
        workflow_id="wf-1",
        task_id="task-1",
        agent_assignment_id="assignment-1",
        inputs={"query": "CapabilityRegistry"},
        context_refs=("specs/framework/0009-capabilities-skills-tools.md",),
        granted_permissions=("read_workspace",),
    )

    assert request.capability == "SearchCode"
    assert request.granted_permissions == ("read_workspace",)
    assert "tool" not in asdict(request)
    assert "provider" not in asdict(request)
    assert "mcp" not in asdict(request)


def test_capability_registry_filters_by_name_tags_and_domain():
    registry = CapabilityRegistry(
        (
            make_capability("cap-search-code", name="SearchCode", domain="framework", tags=("code", "local")),
            make_capability("cap-review-architecture", name="ReviewArchitecture", domain="architecture", tags=("review",)),
        )
    )

    matches = registry.filter_profiles(name="SearchCode", domain="framework", tags=("code",))

    assert [profile.capability_id for profile in matches] == ["cap-search-code"]
    assert [profile.capability_id for profile in registry.find_by_name("ReviewArchitecture")] == ["cap-review-architecture"]


def test_capability_registry_rejects_duplicates_and_blocks_missing_selection():
    registry = CapabilityRegistry((make_capability("cap-1"),))

    with pytest.raises(CapabilityRegistryError, match="already registered"):
        registry.register(make_capability("cap-1"))

    with pytest.raises(CapabilityRegistryError, match="no compatible"):
        registry.select_one(name="RunValidation")
