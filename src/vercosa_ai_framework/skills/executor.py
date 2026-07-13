"""Skill execution MVP.

The executor converts an authorized skill execution into a governed tool
execution request. It does not expose tools, providers, MCPs, or adapters to
agents.
"""

from __future__ import annotations

from dataclasses import dataclass

from vercosa_ai_framework.skills.registry import SkillRegistry
from vercosa_ai_framework.skills.types import SkillExecutionRequest, SkillExecutionResult, SkillProfile
from vercosa_ai_framework.tools.executor import ToolExecutor
from vercosa_ai_framework.tools.registry import ToolRegistry, ToolRegistryError
from vercosa_ai_framework.tools.types import ToolExecutionRequest, ToolExecutionResult, ToolProfile


class SkillExecutionError(ValueError):
    """Raised when a skill cannot create a safe tool execution request."""


@dataclass(frozen=True, slots=True)
class SkillToolSelection:
    """Selected tool and fallback metadata for a skill execution."""

    skill: SkillProfile
    tool: ToolProfile
    fallback_applied: bool = False
    fallback_from: str | None = None


class SkillExecutor:
    """Build tool requests from skill execution requests."""

    def __init__(self, skill_registry: SkillRegistry, tool_registry: ToolRegistry, tool_executor: ToolExecutor | None = None) -> None:
        self.skill_registry = skill_registry
        self.tool_registry = tool_registry
        self.tool_executor = tool_executor

    def build_tool_request(self, request: SkillExecutionRequest, *, dry_run: bool = True) -> ToolExecutionRequest:
        """Build a ToolExecutionRequest for the first compatible skill tool."""

        selection = self.select_tool(request)
        allowed_effects = _tuple_str(request.metadata.get("allowed_effects")) or selection.tool.effects
        metadata = dict(request.metadata)
        metadata["agent_assignment_id"] = request.agent_assignment_id
        metadata["skill_request_id"] = request.request_id
        if selection.fallback_applied:
            metadata["fallback_from"] = selection.fallback_from
            metadata["fallback_to"] = selection.tool.name

        return ToolExecutionRequest(
            tool=selection.tool.name,
            skill=selection.skill.name,
            mission_id=request.mission_id,
            workflow_id=request.workflow_id,
            task_id=request.task_id,
            inputs=request.inputs,
            granted_permissions=request.granted_permissions,
            allowed_effects=allowed_effects,
            dry_run=dry_run,
            limits={**selection.skill.execution_limits, **request.limits},
            guardian_decision_refs=request.guardian_decision_refs,
            metadata=metadata,
        )

    def execute(self, request: SkillExecutionRequest, *, dry_run: bool = True) -> SkillExecutionResult:
        """Execute the selected tool through an injected ToolExecutor."""

        if self.tool_executor is None:
            raise SkillExecutionError("tool executor is required to execute a skill")
        tool_request = self.build_tool_request(request, dry_run=dry_run)
        tool_result = self.tool_executor.execute(tool_request)
        return self._to_skill_result(request, tool_result)

    def select_tool(self, request: SkillExecutionRequest) -> SkillToolSelection:
        """Select a required tool or declared fallback tool deterministically."""

        skill = self.skill_registry.get(request.skill)
        if not skill.implements_capability(request.capability):
            raise SkillExecutionError(f"skill does not implement capability: {request.capability}")
        if not _contains_all(request.granted_permissions, skill.permission_requirements):
            raise SkillExecutionError(f"skill lacks permissions: {skill.name}")

        for tool_name in skill.required_tools:
            selection = self._select_tool_name(tool_name, request, skill)
            if selection is not None:
                return selection

        raise SkillExecutionError(f"no compatible tool found for skill: {skill.name}")

    def _select_tool_name(
        self,
        tool_name: str,
        request: SkillExecutionRequest,
        skill: SkillProfile,
    ) -> SkillToolSelection | None:
        try:
            tool = self.tool_registry.select_one(name=tool_name)
            self._validate_tool(tool, request)
            return SkillToolSelection(skill=skill, tool=tool)
        except ToolRegistryError:
            pass

        unavailable = self.tool_registry.filter_profiles(name=tool_name, available=False)
        fallback_names = unavailable[0].fallback_tools if unavailable else ()
        for fallback_name in fallback_names:
            try:
                fallback = self.tool_registry.select_one(name=fallback_name)
                self._validate_tool(fallback, request)
                return SkillToolSelection(skill=skill, tool=fallback, fallback_applied=True, fallback_from=tool_name)
            except (ToolRegistryError, SkillExecutionError):
                continue
        return None

    def _validate_tool(self, tool: ToolProfile, request: SkillExecutionRequest) -> None:
        if request.allowed_tools and tool.name not in request.allowed_tools:
            raise SkillExecutionError(f"tool not allowed for skill request: {tool.name}")
        if not _contains_all(request.granted_permissions, tool.required_permissions):
            raise SkillExecutionError(f"tool lacks permissions: {tool.name}")

    def _to_skill_result(self, request: SkillExecutionRequest, tool_result: ToolExecutionResult) -> SkillExecutionResult:
        metadata = {**request.metadata, **tool_result.metadata, "skill_request_id": request.request_id}
        return SkillExecutionResult(
            skill=request.skill,
            capability=request.capability,
            mission_id=request.mission_id,
            workflow_id=request.workflow_id,
            task_id=request.task_id,
            success=tool_result.success,
            outputs=tool_result.outputs,
            tool_result_refs=(tool_result.metadata.get("result_ref", tool_result.tool),),
            evidence_refs=tool_result.evidence_refs,
            warnings=tool_result.warnings,
            errors=tool_result.errors,
            audit_log_ref=tool_result.audit_log_ref,
            metadata=metadata,
        )


def _contains_all(values: tuple[str, ...], required: tuple[str, ...]) -> bool:
    available = set(values)
    return all(value in available for value in required)


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


__all__ = ["SkillExecutionError", "SkillExecutor", "SkillToolSelection"]
