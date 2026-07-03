from __future__ import annotations

from dataclasses import asdict

from vercosa_ai_framework.agents import (
    AgentCapabilityRequest,
    AgentExecutionRequest,
    AgentExecutionResult,
    AgentMode,
    AgentProfile,
    AgentRole,
    AgentState,
)


def profile() -> AgentProfile:
    return AgentProfile(
        agent_profile_id="agent-implementation-architect",
        role=AgentRole.IMPLEMENTATION_ARCHITECT,
        domain="framework",
        supported_task_types=("implementation",),
        supported_capabilities=("ReadContext", "SearchCode", "RunValidation"),
        tags=("python", "contracts"),
        risk_range=("low", "medium", "high"),
        default_model_policy={"provider": "auto", "model": "auto"},
        default_execution_limits={"max_cycles": 3},
    )


def test_agent_states_match_spec_0008():
    assert {state.value for state in AgentState} == {
        "idle",
        "planning",
        "executing",
        "reflecting",
        "validating",
        "replanning",
        "done",
        "failed",
    }


def test_agent_profile_describes_capabilities_not_runtime_or_mcp():
    agent_profile = profile()

    assert agent_profile.role == AgentRole.IMPLEMENTATION_ARCHITECT
    assert agent_profile.domain == "framework"
    assert agent_profile.supports_capabilities(("ReadContext", "SearchCode")) is True
    assert agent_profile.supports_capabilities(("DirectMCPAccess",)) is False
    assert agent_profile.has_tags(("python", "contracts")) is True
    assert "opencode" not in asdict(agent_profile)
    assert "mcp" not in asdict(agent_profile)
    assert agent_profile.default_model_policy == {"provider": "auto", "model": "auto"}


def test_agent_capability_request_is_abstract_and_traceable():
    request = AgentCapabilityRequest(
        capability="SearchCode",
        mission_id="mission-1",
        workflow_id="wf-1",
        task_id="task-1",
        agent_assignment_id="assignment-1",
        context_refs=("specs/framework/0008-agent-orchestrator.md",),
        limits={"max_results": 5},
    )

    assert request.capability == "SearchCode"
    assert request.context_refs == ("specs/framework/0008-agent-orchestrator.md",)
    assert "tool" not in asdict(request)
    assert "provider" not in asdict(request)
    assert "mcp" not in asdict(request)


def test_agent_execution_request_and_result_are_normalized_contracts():
    agent_profile = profile()
    request = AgentExecutionRequest(
        mission_id="mission-1",
        workflow_id="wf-1",
        task_id="task-1",
        attempt_id="attempt-1",
        agent_assignment_id="assignment-1",
        agent_profile=agent_profile,
        required_capabilities=("ReadContext", "RunValidation"),
        task_type="implementation",
        mode=AgentMode.PRIMARY,
        context_refs=("src/vercosa_ai_framework/tasks/",),
        expected_outputs=("tests pass",),
        execution_limits={"max_cycles": 3},
    )
    result = AgentExecutionResult(
        mission_id=request.mission_id,
        workflow_id=request.workflow_id,
        task_id=request.task_id,
        attempt_id=request.attempt_id,
        agent_assignment_id=request.agent_assignment_id,
        agent_profile_id=agent_profile.agent_profile_id,
        state=AgentState.DONE,
        success=True,
        artifact_refs=("src/vercosa_ai_framework/agents/types.py",),
        validation_results=("pytest", "compileall"),
        cycle_count=1,
    )

    assert request.state == AgentState.IDLE
    assert request.required_capabilities == ("ReadContext", "RunValidation")
    assert result.state == AgentState.DONE
    assert result.success is True
    assert result.validation_results == ("pytest", "compileall")
