"""Governed Provider Gateway MVP."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from vercosa_ai_framework.guardian.policies import GuardianEvaluationContext
from vercosa_ai_framework.guardian.types import GuardianAction, GuardianDecision
from vercosa_ai_framework.providers.adapter import ProviderAdapter
from vercosa_ai_framework.providers.registry import ProviderRegistry, ProviderRegistryError
from vercosa_ai_framework.providers.types import ProviderProfile, ProviderRequest, ProviderResult, utc_now_iso


class ProviderGatewayError(ValueError):
    """Raised when Provider Gateway configuration violates its contract."""


ProviderCallable = Callable[[ProviderRequest, ProviderProfile], ProviderResult | dict[str, object]]


@dataclass(frozen=True, slots=True)
class CallableProviderAdapter(ProviderAdapter):
    """Wrap a test or runtime callable as a ProviderAdapter."""

    fn: ProviderCallable

    def execute(self, request: ProviderRequest, profile: ProviderProfile) -> ProviderResult:
        result = self.fn(request, profile)
        if isinstance(result, ProviderResult):
            return result
        return ProviderResult(
            provider_request_id=request.provider_request_id,
            provider_id=profile.provider_id,
            adapter_ref=profile.adapter_ref,
            operation=request.operation,
            success=True,
            status="success",
            outputs=dict(result),
            timeout_applied=request.timeout or profile.default_timeout,
        )


class ProviderGateway:
    """Select, guard, and invoke injected provider adapters."""

    def __init__(
        self,
        provider_registry: ProviderRegistry,
        adapters: dict[str, ProviderAdapter | ProviderCallable] | None = None,
        guardian_engine: object | None = None,
        default_timeout: float | None = None,
    ) -> None:
        self.provider_registry = provider_registry
        self.adapters = {
            adapter_ref: adapter if isinstance(adapter, ProviderAdapter) else CallableProviderAdapter(adapter)
            for adapter_ref, adapter in (adapters or {}).items()
        }
        self.guardian_engine = guardian_engine
        self.default_timeout = default_timeout

    def execute(self, request: ProviderRequest) -> ProviderResult:
        """Execute or simulate a governed provider request."""

        started_at = utc_now_iso()
        try:
            profile = self._select_profile(request)
        except ProviderRegistryError as exc:
            return self._blocked(request, str(exc), started_at=started_at)

        validation_error = self._validation_error(request, profile)
        if validation_error is not None:
            return self._blocked(request, validation_error, profile=profile, started_at=started_at)

        guardian_decision = self._evaluate_guardian(request, profile)
        if guardian_decision is not None and guardian_decision.decision not in {GuardianAction.ALLOW, GuardianAction.WARN}:
            return self._blocked(
                request,
                f"guardian blocked provider execution: {guardian_decision.decision.value}",
                profile=profile,
                guardian_decision=guardian_decision,
                started_at=started_at,
            )

        if request.dry_run:
            return ProviderResult(
                provider_request_id=request.provider_request_id,
                provider_id=profile.provider_id,
                adapter_ref=profile.adapter_ref,
                operation=request.operation,
                success=True,
                status="dry_run",
                outputs={
                    "dry_run": True,
                    "provider_id": profile.provider_id,
                    "operation": request.operation,
                    "effects": profile.effects,
                    "timeout": self._timeout_for(request, profile),
                },
                warnings=("dry_run: provider adapter was not executed",),
                timeout_applied=self._timeout_for(request, profile),
                guardian_decision_refs=self._guardian_refs(request, guardian_decision),
                started_at=started_at,
            )

        result = self._execute_adapter(request, profile, guardian_decision, started_at=started_at)
        if result.success or not request.fallback_allowed:
            return result
        return self._fallback(request, profile, result, started_at=started_at)

    def _select_profile(self, request: ProviderRequest) -> ProviderProfile:
        if request.provider_ref is not None:
            return self.provider_registry.get(request.provider_ref)
        return self.provider_registry.select_one(kind=request.provider_kind, operation=request.operation)

    def _validation_error(self, request: ProviderRequest, profile: ProviderProfile) -> str | None:
        if not profile.enabled:
            return f"provider disabled: {profile.provider_id}"
        if profile.blocked:
            return f"provider blocked: {profile.provider_id}"
        if profile.dangerous:
            return f"dangerous provider cannot be executed automatically: {profile.provider_id}"
        if profile.deprecated:
            return f"deprecated provider cannot be selected automatically: {profile.provider_id}"
        if not profile.supports_operation(request.operation):
            return f"provider does not support operation: {request.operation}"
        if not _contains_all(request.granted_permissions, profile.required_permissions):
            return f"provider lacks permissions: {profile.provider_id}"
        if request.allowed_effects and not _contains_all(request.allowed_effects, profile.effects):
            return f"provider effects are not allowed: {profile.provider_id}"
        if request.data_sensitivity not in profile.data_sensitivity_allowed:
            return f"provider does not allow data sensitivity: {request.data_sensitivity}"
        return None

    def _execute_adapter(
        self,
        request: ProviderRequest,
        profile: ProviderProfile,
        guardian_decision: GuardianDecision | None,
        *,
        started_at: str,
    ) -> ProviderResult:
        adapter = self.adapters.get(profile.adapter_ref)
        if adapter is None:
            return self._failure(request, "provider adapter is not configured", profile=profile, guardian_decision=guardian_decision, started_at=started_at)
        try:
            result = adapter.execute(request, profile)
        except Exception as exc:  # noqa: BLE001 - normalize adapter failures at the boundary.
            return self._failure(request, f"provider adapter failed: {exc}", profile=profile, guardian_decision=guardian_decision, started_at=started_at)
        return self._normalize_result(request, profile, result, guardian_decision, started_at=started_at)

    def _fallback(self, request: ProviderRequest, original: ProviderProfile, failure: ProviderResult, *, started_at: str) -> ProviderResult:
        for provider_id in original.fallback_providers:
            try:
                profile = self.provider_registry.get(provider_id)
            except ProviderRegistryError:
                continue
            validation_error = self._validation_error(request, profile)
            if validation_error is not None:
                continue
            guardian_decision = self._evaluate_guardian(request, profile, fallback_from=original.provider_id)
            if guardian_decision is not None and guardian_decision.decision not in {GuardianAction.ALLOW, GuardianAction.WARN}:
                continue
            result = self._execute_adapter(request, profile, guardian_decision, started_at=started_at)
            if result.success:
                return ProviderResult(
                    provider_request_id=result.provider_request_id,
                    provider_id=result.provider_id,
                    adapter_ref=result.adapter_ref,
                    operation=result.operation,
                    success=result.success,
                    status=result.status,
                    provider_result_id=result.provider_result_id,
                    outputs=result.outputs,
                    normalized_output_schema_ref=result.normalized_output_schema_ref,
                    evidence_refs=result.evidence_refs,
                    artifact_refs=result.artifact_refs,
                    warnings=result.warnings + (f"fallback applied from {original.provider_id} to {profile.provider_id}",),
                    errors=result.errors,
                    fallback_from=original.provider_id,
                    fallback_to=profile.provider_id,
                    retry_count=result.retry_count,
                    timeout_applied=result.timeout_applied,
                    cost_used=result.cost_used,
                    rate_limit_state=result.rate_limit_state,
                    guardian_decision_refs=result.guardian_decision_refs,
                    redactions_applied=result.redactions_applied,
                    audit_log_ref=result.audit_log_ref,
                    started_at=result.started_at,
                    finished_at=result.finished_at,
                    metadata={**result.metadata, "fallback_reason": failure.status},
                )
        return ProviderResult(
            provider_request_id=failure.provider_request_id,
            provider_id=failure.provider_id,
            adapter_ref=failure.adapter_ref,
            operation=failure.operation,
            success=False,
            status="fallback_failed",
            outputs=failure.outputs,
            warnings=failure.warnings,
            errors=failure.errors + ("no compatible fallback provider succeeded",),
            timeout_applied=failure.timeout_applied,
            guardian_decision_refs=failure.guardian_decision_refs,
            started_at=failure.started_at,
            metadata=failure.metadata,
        )

    def _evaluate_guardian(
        self,
        request: ProviderRequest,
        profile: ProviderProfile,
        *,
        fallback_from: str | None = None,
    ) -> GuardianDecision | None:
        if self.guardian_engine is None:
            return None
        context = GuardianEvaluationContext(
            mission_id=request.mission_id,
            evaluation_id=request.provider_request_id,
            evaluation_type="provider_request",
            mission_goal=f"Execute provider operation {request.operation}",
            requested_action=f"provider={profile.provider_id}; operation={request.operation}; effects={','.join(profile.effects)}",
            planned_command=request.inputs.get("command") if isinstance(request.inputs.get("command"), str) else None,
            spec_refs=("specs/framework/0010-provider-gateway.md",),
            prior_decision_refs=request.guardian_decision_refs,
            target_paths=request.allowed_paths,
            data_sensitivity=request.data_sensitivity,
            network_policy={"policy": profile.network_policy, **request.network_policy},
            provider_policy={"provider_id": profile.provider_id, "provider_kind": profile.kind.value, "fallback_from": fallback_from},
            budget_policy=request.budget_policy,
            execution_limits={"timeout": self._timeout_for(request, profile)},
            metadata={
                "tool_id": request.tool_id,
                "dry_run": request.dry_run,
                "required_permissions": profile.required_permissions,
                "granted_permissions": request.granted_permissions,
            },
        )
        return self.guardian_engine.evaluate(context)  # type: ignore[attr-defined]

    def _normalize_result(
        self,
        request: ProviderRequest,
        profile: ProviderProfile,
        result: ProviderResult,
        guardian_decision: GuardianDecision | None,
        *,
        started_at: str,
    ) -> ProviderResult:
        return ProviderResult(
            provider_request_id=request.provider_request_id,
            provider_id=profile.provider_id,
            adapter_ref=profile.adapter_ref,
            operation=request.operation,
            success=result.success,
            status=result.status,
            provider_result_id=result.provider_result_id,
            outputs=result.outputs,
            normalized_output_schema_ref=result.normalized_output_schema_ref,
            evidence_refs=result.evidence_refs,
            artifact_refs=result.artifact_refs,
            warnings=result.warnings,
            errors=result.errors,
            blocked_reason=result.blocked_reason,
            fallback_from=result.fallback_from,
            fallback_to=result.fallback_to,
            retry_count=result.retry_count,
            timeout_applied=result.timeout_applied or self._timeout_for(request, profile),
            cost_used=result.cost_used,
            rate_limit_state=result.rate_limit_state,
            guardian_decision_refs=self._guardian_refs(request, guardian_decision, result.guardian_decision_refs),
            redactions_applied=result.redactions_applied,
            audit_log_ref=result.audit_log_ref,
            started_at=result.started_at or started_at,
            finished_at=result.finished_at,
            metadata=result.metadata,
        )

    def _blocked(
        self,
        request: ProviderRequest,
        reason: str,
        *,
        profile: ProviderProfile | None = None,
        guardian_decision: GuardianDecision | None = None,
        started_at: str,
    ) -> ProviderResult:
        return ProviderResult(
            provider_request_id=request.provider_request_id,
            provider_id=profile.provider_id if profile else request.provider_ref or "unresolved",
            adapter_ref=profile.adapter_ref if profile else "unresolved",
            operation=request.operation,
            success=False,
            status="blocked",
            errors=(reason,),
            blocked_reason=reason,
            timeout_applied=self._timeout_for(request, profile),
            guardian_decision_refs=self._guardian_refs(request, guardian_decision),
            started_at=started_at,
        )

    def _failure(
        self,
        request: ProviderRequest,
        error: str,
        *,
        profile: ProviderProfile,
        guardian_decision: GuardianDecision | None,
        started_at: str,
    ) -> ProviderResult:
        return ProviderResult(
            provider_request_id=request.provider_request_id,
            provider_id=profile.provider_id,
            adapter_ref=profile.adapter_ref,
            operation=request.operation,
            success=False,
            status="failed",
            errors=(error,),
            timeout_applied=self._timeout_for(request, profile),
            guardian_decision_refs=self._guardian_refs(request, guardian_decision),
            started_at=started_at,
        )

    def _timeout_for(self, request: ProviderRequest, profile: ProviderProfile | None) -> float | None:
        if request.timeout is not None:
            return request.timeout
        if profile is not None and profile.default_timeout is not None:
            return profile.default_timeout
        return self.default_timeout

    def _guardian_refs(
        self,
        request: ProviderRequest,
        guardian_decision: GuardianDecision | None,
        extra_refs: tuple[str, ...] = (),
    ) -> tuple[str, ...]:
        refs = list(request.guardian_decision_refs)
        refs.extend(extra_refs)
        if guardian_decision is not None:
            refs.append(guardian_decision.evaluation_id)
        return tuple(dict.fromkeys(refs))


def _contains_all(values: tuple[str, ...], required: tuple[str, ...]) -> bool:
    available = set(values)
    return all(value in available for value in required)


__all__ = ["CallableProviderAdapter", "ProviderCallable", "ProviderGateway", "ProviderGatewayError"]
