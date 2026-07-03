"""Governed Tool execution MVP."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass

from vercosa_ai_framework.guardian.policies import GuardianEvaluationContext
from vercosa_ai_framework.guardian.types import GuardianAction, GuardianDecision
from vercosa_ai_framework.tools.registry import ToolRegistry, ToolRegistryError
from vercosa_ai_framework.tools.types import ToolExecutionRequest, ToolExecutionResult, ToolProfile


class ToolExecutionError(ValueError):
    """Raised when a tool execution request violates its contract."""


class ToolAdapter(ABC):
    """Abstract boundary for concrete provider, MCP, API, or local adapters."""

    @abstractmethod
    def execute(self, request: ToolExecutionRequest, profile: ToolProfile) -> ToolExecutionResult:
        """Execute a validated tool request."""


ToolCallable = Callable[[ToolExecutionRequest, ToolProfile], ToolExecutionResult | dict[str, object]]


@dataclass(frozen=True, slots=True)
class CallableToolAdapter(ToolAdapter):
    """Wrap a test or runtime callable as a ToolAdapter."""

    fn: ToolCallable

    def execute(self, request: ToolExecutionRequest, profile: ToolProfile) -> ToolExecutionResult:
        result = self.fn(request, profile)
        if isinstance(result, ToolExecutionResult):
            return result
        return ToolExecutionResult(
            tool=request.tool,
            skill=request.skill,
            mission_id=request.mission_id,
            workflow_id=request.workflow_id,
            task_id=request.task_id,
            success=True,
            outputs=dict(result),
        )


class ToolExecutor:
    """Validate, guard, and execute tools through injected adapters."""

    def __init__(self, tool_registry: ToolRegistry, adapter: ToolAdapter | ToolCallable | None = None, guardian_engine: object | None = None) -> None:
        self.tool_registry = tool_registry
        self.adapter = adapter if isinstance(adapter, ToolAdapter) or adapter is None else CallableToolAdapter(adapter)
        self.guardian_engine = guardian_engine

    def execute(self, request: ToolExecutionRequest) -> ToolExecutionResult:
        """Execute a tool request, blocking when Guardian does not allow it."""

        profile = self._select_profile(request)
        validation_error = self._validation_error(request, profile)
        if validation_error is not None:
            return self._failure(request, validation_error)

        guardian_decision = self._evaluate_guardian(request, profile)
        if guardian_decision is not None and guardian_decision.decision not in {GuardianAction.ALLOW, GuardianAction.WARN}:
            return self._failure(
                request,
                f"guardian blocked tool execution: {guardian_decision.decision.value}",
                guardian_decision=guardian_decision,
            )

        if request.dry_run:
            return ToolExecutionResult(
                tool=request.tool,
                skill=request.skill,
                mission_id=request.mission_id,
                workflow_id=request.workflow_id,
                task_id=request.task_id,
                success=True,
                outputs={"dry_run": True, "tool": profile.name, "effects": profile.effects},
                warnings=("dry_run: adapter was not executed",),
                metadata=self._metadata(guardian_decision),
            )

        if self.adapter is None:
            return self._failure(request, "tool adapter is required when dry_run is false", guardian_decision=guardian_decision)

        result = self.adapter.execute(request, profile)
        metadata = {**result.metadata, **self._metadata(guardian_decision)}
        return ToolExecutionResult(
            tool=result.tool,
            skill=result.skill,
            mission_id=result.mission_id,
            workflow_id=result.workflow_id,
            task_id=result.task_id,
            success=result.success,
            outputs=result.outputs,
            evidence_refs=result.evidence_refs,
            warnings=result.warnings,
            errors=result.errors,
            cost_used=result.cost_used,
            audit_log_ref=result.audit_log_ref,
            metadata=metadata,
        )

    def _select_profile(self, request: ToolExecutionRequest) -> ToolProfile:
        try:
            return self.tool_registry.select_one(name=request.tool)
        except ToolRegistryError as exc:
            raise ToolExecutionError(f"unknown or unavailable tool: {request.tool}") from exc

    def _validation_error(self, request: ToolExecutionRequest, profile: ToolProfile) -> str | None:
        if not _contains_all(request.granted_permissions, profile.required_permissions):
            return f"tool lacks permissions: {profile.name}"
        if request.allowed_effects and not _contains_all(request.allowed_effects, profile.effects):
            return f"tool effects are not allowed: {profile.name}"
        if profile.dangerous:
            return f"dangerous tool cannot be executed automatically: {profile.name}"
        return None

    def _evaluate_guardian(self, request: ToolExecutionRequest, profile: ToolProfile) -> GuardianDecision | None:
        if self.guardian_engine is None:
            return None
        context = GuardianEvaluationContext(
            mission_id=request.mission_id,
            evaluation_id=request.request_id,
            evaluation_type="tool_execution",
            mission_goal=f"Execute tool {profile.name}",
            requested_action=f"tool={profile.name}; effects={','.join(profile.effects)}; provider_type={profile.provider_type}",
            planned_command=request.inputs.get("command") if isinstance(request.inputs.get("command"), str) else None,
            spec_refs=("specs/framework/0009-capabilities-skills-tools.md",),
            prior_decision_refs=request.guardian_decision_refs,
            data_sensitivity=profile.data_sensitivity,
            network_policy={"policy": profile.network_policy},
            execution_limits=request.limits,
            metadata={
                "tool_id": profile.tool_id,
                "skill": request.skill,
                "dry_run": request.dry_run,
                "required_permissions": profile.required_permissions,
            },
        )
        return self.guardian_engine.evaluate(context)  # type: ignore[attr-defined]

    def _failure(
        self,
        request: ToolExecutionRequest,
        error: str,
        *,
        guardian_decision: GuardianDecision | None = None,
    ) -> ToolExecutionResult:
        return ToolExecutionResult(
            tool=request.tool,
            skill=request.skill,
            mission_id=request.mission_id,
            workflow_id=request.workflow_id,
            task_id=request.task_id,
            success=False,
            errors=(error,),
            metadata=self._metadata(guardian_decision),
        )

    def _metadata(self, guardian_decision: GuardianDecision | None) -> dict[str, object]:
        if guardian_decision is None:
            return {}
        return {
            "guardian_decision": guardian_decision.decision.value,
            "guardian_decision_ref": guardian_decision.evaluation_id,
        }


def _contains_all(values: tuple[str, ...], required: tuple[str, ...]) -> bool:
    available = set(values)
    return all(value in available for value in required)


__all__ = ["CallableToolAdapter", "ToolAdapter", "ToolCallable", "ToolExecutionError", "ToolExecutor"]
