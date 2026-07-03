"""Governed Tool execution MVP."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass

from vercosa_ai_framework.guardian.policies import GuardianEvaluationContext
from vercosa_ai_framework.guardian.types import GuardianAction, GuardianDecision
from vercosa_ai_framework.providers import ProviderGateway, ProviderKind, ProviderRequest, ProviderResult
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

    def __init__(
        self,
        tool_registry: ToolRegistry,
        adapter: ToolAdapter | ToolCallable | None = None,
        guardian_engine: object | None = None,
        provider_gateway: ProviderGateway | None = None,
    ) -> None:
        self.tool_registry = tool_registry
        self.adapter = adapter if isinstance(adapter, ToolAdapter) or adapter is None else CallableToolAdapter(adapter)
        self.guardian_engine = guardian_engine
        self.provider_gateway = provider_gateway

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

        if self.provider_gateway is not None:
            return self._execute_provider_gateway(request, profile, guardian_decision)

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

    def _execute_provider_gateway(
        self,
        request: ToolExecutionRequest,
        profile: ToolProfile,
        guardian_decision: GuardianDecision | None,
    ) -> ToolExecutionResult:
        provider_request = self._provider_request(request, profile, guardian_decision)
        provider_result = self.provider_gateway.execute(provider_request)
        return self._from_provider_result(request, provider_result, guardian_decision)

    def _provider_request(
        self,
        request: ToolExecutionRequest,
        profile: ToolProfile,
        guardian_decision: GuardianDecision | None,
    ) -> ProviderRequest:
        timeout = _number_or_none(request.limits.get("timeout")) or profile.timeout
        return ProviderRequest(
            operation=profile.operation_type,
            mission_id=request.mission_id,
            workflow_id=request.workflow_id,
            task_id=request.task_id,
            tool_id=profile.tool_id,
            inputs=request.inputs,
            provider_ref=profile.provider_ref,
            provider_kind=_provider_kind(profile.provider_type),
            tool_execution_request_id=request.request_id,
            skill_id=request.skill,
            input_schema_ref=profile.input_schema_ref,
            expected_output_schema_ref=profile.output_schema_ref,
            granted_permissions=request.granted_permissions,
            allowed_effects=request.allowed_effects,
            allowed_paths=tuple(str(path) for path in request.metadata.get("allowed_paths", ())),
            data_sensitivity=profile.data_sensitivity,
            network_policy={"policy": profile.network_policy},
            timeout=timeout,
            retry_policy=profile.retry_policy,
            fallback_allowed=bool(profile.metadata.get("fallback_allowed", False)),
            dry_run=request.dry_run,
            guardian_decision_refs=self._guardian_decision_refs(request, guardian_decision),
            metadata={"tool_request_id": request.request_id, **profile.metadata},
        )

    def _from_provider_result(
        self,
        request: ToolExecutionRequest,
        provider_result: ProviderResult,
        guardian_decision: GuardianDecision | None,
    ) -> ToolExecutionResult:
        metadata = {
            **self._metadata(guardian_decision),
            "provider_request_id": provider_result.provider_request_id,
            "provider_result_id": provider_result.provider_result_id,
            "provider_id": provider_result.provider_id,
            "provider_status": provider_result.status,
        }
        if provider_result.fallback_from is not None:
            metadata["provider_fallback_from"] = provider_result.fallback_from
        if provider_result.fallback_to is not None:
            metadata["provider_fallback_to"] = provider_result.fallback_to
        return ToolExecutionResult(
            tool=request.tool,
            skill=request.skill,
            mission_id=request.mission_id,
            workflow_id=request.workflow_id,
            task_id=request.task_id,
            success=provider_result.success,
            outputs=provider_result.outputs,
            evidence_refs=provider_result.evidence_refs,
            warnings=provider_result.warnings,
            errors=provider_result.errors,
            cost_used=provider_result.cost_used,
            audit_log_ref=provider_result.audit_log_ref,
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

    def _guardian_decision_refs(
        self,
        request: ToolExecutionRequest,
        guardian_decision: GuardianDecision | None,
    ) -> tuple[str, ...]:
        refs = list(request.guardian_decision_refs)
        if guardian_decision is not None:
            refs.append(guardian_decision.evaluation_id)
        return tuple(dict.fromkeys(refs))


def _contains_all(values: tuple[str, ...], required: tuple[str, ...]) -> bool:
    available = set(values)
    return all(value in available for value in required)


def _provider_kind(value: str) -> ProviderKind | None:
    try:
        return ProviderKind(value)
    except ValueError:
        return None


def _number_or_none(value: object) -> float | None:
    if isinstance(value, int | float):
        return float(value)
    return None


__all__ = ["CallableToolAdapter", "ToolAdapter", "ToolCallable", "ToolExecutionError", "ToolExecutor"]
