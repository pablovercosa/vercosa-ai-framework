"""Capability execution boundary.

This module bridges a resolved Capability to the selected Skill without making
agents aware of tools, providers, MCPs, adapters, network, databases, or
subprocesses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from vercosa_ai_framework.capabilities.resolver import CapabilityResolutionResult
from vercosa_ai_framework.skills import SkillExecutionRequest, SkillExecutionResult, SkillExecutor


class CapabilityExecutionError(ValueError):
    """Raised when a resolved capability cannot be executed safely."""


@dataclass(frozen=True, slots=True)
class CapabilityExecutionResult:
    """Traceable normalized result for Capability -> Skill execution."""

    capability: str
    skill: str
    mission_id: str
    workflow_id: str
    task_id: str
    agent_assignment_id: str
    success: bool
    capability_request_id: str
    skill_request_id: str | None = None
    skill_result_ref: str | None = None
    outputs: dict[str, Any] = field(default_factory=dict)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
    guardian_decision_refs: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)


class CapabilityExecutor(Protocol):
    """High-level injectable contract used by the Agent Orchestrator."""

    def execute(self, resolution: CapabilityResolutionResult) -> CapabilityExecutionResult:
        """Execute an already resolved capability."""


class ResolvedCapabilityExecutor:
    """Execute the exact Skill selected by CapabilityResolver."""

    def __init__(self, skill_executor: SkillExecutor, *, dry_run: bool = True) -> None:
        self.skill_executor = skill_executor
        self.dry_run = dry_run

    def build_skill_request(self, resolution: CapabilityResolutionResult) -> SkillExecutionRequest:
        """Build a SkillExecutionRequest from a CapabilityResolutionResult."""

        request = resolution.request
        guardian_refs = list(request.guardian_decision_refs)
        if resolution.guardian_decision is not None:
            guardian_refs.append(resolution.guardian_decision.evaluation_id)

        metadata = dict(request.metadata)
        metadata.update(
            {
                "capability_request_id": request.request_id,
                "capability_id": resolution.capability.capability_id,
                "capability_resolution_reasons": resolution.reasons,
                "selected_skill_id": resolution.skill.skill_id,
                "selected_skill_name": resolution.skill.name,
                "selected_skill_version": resolution.skill.version,
                "allowed_effects": _allowed_effects_for_capability(request.metadata, resolution.capability.name),
            }
        )
        if resolution.fallback_applied:
            metadata["skill_fallback_from"] = resolution.fallback_from

        return SkillExecutionRequest(
            skill=resolution.skill.skill_id,
            capability=resolution.capability.name,
            mission_id=request.mission_id,
            workflow_id=request.workflow_id,
            task_id=request.task_id,
            agent_assignment_id=request.agent_assignment_id,
            inputs=request.inputs,
            context_refs=request.context_refs,
            granted_permissions=request.granted_permissions,
            allowed_tools=_allowed_tools_for_capability(request.metadata, resolution.capability.name),
            limits=request.limits,
            guardian_decision_refs=tuple(dict.fromkeys(guardian_refs)),
            request_id=request.request_id,
            metadata=metadata,
        )

    def execute(self, resolution: CapabilityResolutionResult) -> CapabilityExecutionResult:
        """Execute a resolved capability through the selected Skill."""

        skill_request = self.build_skill_request(resolution)
        try:
            skill_result = self.skill_executor.execute(skill_request, dry_run=self.dry_run)
        except Exception as exc:  # noqa: BLE001 - normalize boundary failures for orchestrators.
            return self._failure(resolution, skill_request, str(exc))
        return self._from_skill_result(resolution, skill_request, skill_result)

    def _from_skill_result(
        self,
        resolution: CapabilityResolutionResult,
        skill_request: SkillExecutionRequest,
        skill_result: SkillExecutionResult,
    ) -> CapabilityExecutionResult:
        metadata = {
            **skill_result.metadata,
            "capability_request_id": resolution.request.request_id,
            "capability_id": resolution.capability.capability_id,
            "skill_result_refs": skill_result.tool_result_refs,
        }
        return CapabilityExecutionResult(
            capability=resolution.capability.name,
            skill=resolution.skill.skill_id,
            mission_id=resolution.request.mission_id,
            workflow_id=resolution.request.workflow_id,
            task_id=resolution.request.task_id,
            agent_assignment_id=resolution.request.agent_assignment_id,
            success=skill_result.success,
            capability_request_id=resolution.request.request_id,
            skill_request_id=skill_request.request_id,
            skill_result_ref=skill_result.audit_log_ref,
            outputs=skill_result.outputs,
            evidence_refs=skill_result.evidence_refs,
            warnings=skill_result.warnings,
            errors=skill_result.errors,
            guardian_decision_refs=skill_request.guardian_decision_refs,
            metadata=metadata,
        )

    def _failure(
        self,
        resolution: CapabilityResolutionResult,
        skill_request: SkillExecutionRequest,
        error: str,
    ) -> CapabilityExecutionResult:
        return CapabilityExecutionResult(
            capability=resolution.capability.name,
            skill=resolution.skill.skill_id,
            mission_id=resolution.request.mission_id,
            workflow_id=resolution.request.workflow_id,
            task_id=resolution.request.task_id,
            agent_assignment_id=resolution.request.agent_assignment_id,
            success=False,
            capability_request_id=resolution.request.request_id,
            skill_request_id=skill_request.request_id,
            errors=(error,),
            guardian_decision_refs=skill_request.guardian_decision_refs,
            metadata={
                "capability_request_id": resolution.request.request_id,
                "capability_id": resolution.capability.capability_id,
                "selected_skill_id": resolution.skill.skill_id,
            },
        )


def _allowed_tools_for_capability(metadata: dict[str, Any], capability: str) -> tuple[str, ...]:
    allowed_tools = metadata.get("allowed_tools")
    if isinstance(allowed_tools, dict):
        return _tuple_str(allowed_tools.get(capability))
    return _tuple_str(allowed_tools)


def _allowed_effects_for_capability(metadata: dict[str, Any], capability: str) -> tuple[str, ...]:
    allowed_effects = metadata.get("allowed_effects")
    if isinstance(allowed_effects, dict):
        return _tuple_str(allowed_effects.get(capability))
    return _tuple_str(allowed_effects)


def _tuple_str(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, tuple):
        return tuple(str(item) for item in value)
    if isinstance(value, list):
        return tuple(str(item) for item in value)
    return (str(value),)


__all__ = [
    "CapabilityExecutionError",
    "CapabilityExecutionResult",
    "CapabilityExecutor",
    "ResolvedCapabilityExecutor",
]
