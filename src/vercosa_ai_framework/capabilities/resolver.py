"""Capability to Skill resolution MVP.

The resolver keeps agents behind the capability boundary. It selects a
compatible SkillProfile using declarative registries only; it does not execute
skills, call tools, contact providers, access MCPs, or use subprocesses.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from vercosa_ai_framework.capabilities.registry import CapabilityRegistry, CapabilityRegistryError
from vercosa_ai_framework.capabilities.types import CapabilityProfile, CapabilityRequest
from vercosa_ai_framework.guardian.policies import GuardianEvaluationContext
from vercosa_ai_framework.guardian.types import GuardianAction, GuardianDecision
from vercosa_ai_framework.skills.registry import SkillRegistry
from vercosa_ai_framework.skills.types import SkillProfile
from vercosa_ai_framework.tools.registry import ToolRegistry, ToolRegistryError


class CapabilityResolutionError(ValueError):
    """Raised when a capability cannot be resolved safely."""


@dataclass(frozen=True, slots=True)
class CapabilityResolutionResult:
    """Auditable result of Capability -> Skill resolution."""

    capability: CapabilityProfile
    skill: SkillProfile
    request: CapabilityRequest
    guardian_decision: GuardianDecision | None = None
    fallback_applied: bool = False
    fallback_from: str | None = None
    reasons: tuple[str, ...] = field(default_factory=tuple)


class CapabilityResolver:
    """Resolve abstract capability requests to compatible skill profiles."""

    def __init__(
        self,
        capability_registry: CapabilityRegistry,
        skill_registry: SkillRegistry,
        tool_registry: ToolRegistry | None = None,
        guardian_engine: object | None = None,
    ) -> None:
        self.capability_registry = capability_registry
        self.skill_registry = skill_registry
        self.tool_registry = tool_registry
        self.guardian_engine = guardian_engine

    def resolve(self, request: CapabilityRequest) -> CapabilityResolutionResult:
        """Return the first deterministic compatible skill for a request."""

        capability = self._select_capability(request)
        self._ensure_permissions(
            request.granted_permissions,
            capability.required_permissions,
            f"capability lacks permissions: {capability.name}",
        )
        guardian_decision = self._evaluate_guardian(request, capability)
        if guardian_decision is not None and guardian_decision.decision not in {GuardianAction.ALLOW, GuardianAction.WARN}:
            raise CapabilityResolutionError(f"guardian blocked capability resolution: {guardian_decision.decision.value}")

        failures: list[str] = []
        for candidate in self.skill_registry.find_by_capability(capability.name):
            result = self._try_skill(request, capability, candidate, guardian_decision)
            if result is not None:
                return result
            failures.append(candidate.skill_id)

            for fallback_skill_id in candidate.fallback_skills:
                fallback = self.skill_registry.get(fallback_skill_id)
                fallback_result = self._try_skill(
                    request,
                    capability,
                    fallback,
                    guardian_decision,
                    fallback_from=candidate.skill_id,
                )
                if fallback_result is not None:
                    return fallback_result
                failures.append(fallback.skill_id)

        detail = ", ".join(failures) if failures else capability.name
        raise CapabilityResolutionError(f"no compatible skill found for capability: {detail}")

    def _select_capability(self, request: CapabilityRequest) -> CapabilityProfile:
        matches = self.capability_registry.find_by_name(request.capability)
        if not matches:
            raise CapabilityResolutionError(f"unknown capability: {request.capability}")
        for profile in matches:
            if profile.deprecated:
                continue
            return profile
        raise CapabilityResolutionError(f"no active capability found: {request.capability}")

    def _try_skill(
        self,
        request: CapabilityRequest,
        capability: CapabilityProfile,
        skill: SkillProfile,
        guardian_decision: GuardianDecision | None,
        *,
        fallback_from: str | None = None,
    ) -> CapabilityResolutionResult | None:
        if skill.deprecated or not skill.implements_capability(capability.name):
            return None
        if not _contains_all(request.granted_permissions, skill.permission_requirements):
            return None
        if self.tool_registry is not None and not self._required_tools_available(skill):
            return None
        return CapabilityResolutionResult(
            capability=capability,
            skill=skill,
            request=request,
            guardian_decision=guardian_decision,
            fallback_applied=fallback_from is not None,
            fallback_from=fallback_from,
            reasons=("selected compatible skill",),
        )

    def _required_tools_available(self, skill: SkillProfile) -> bool:
        assert self.tool_registry is not None
        for tool_name in skill.required_tools:
            try:
                self.tool_registry.select_one(name=tool_name)
            except ToolRegistryError:
                return False
        return True

    def _evaluate_guardian(
        self,
        request: CapabilityRequest,
        capability: CapabilityProfile,
    ) -> GuardianDecision | None:
        if self.guardian_engine is None:
            return None
        context = GuardianEvaluationContext(
            mission_id=request.mission_id,
            evaluation_id=request.request_id,
            evaluation_type="capability_resolution",
            mission_goal=f"Resolve capability {capability.name}",
            requested_action=capability.intent,
            spec_refs=("specs/framework/0009-capabilities-skills-tools.md",),
            prior_decision_refs=request.guardian_decision_refs,
            execution_limits=request.limits,
            metadata={
                "capability_id": capability.capability_id,
                "risk_level": capability.risk_level,
                "required_permissions": capability.required_permissions,
            },
        )
        return self.guardian_engine.evaluate(context)  # type: ignore[attr-defined]

    def _ensure_permissions(self, granted: tuple[str, ...], required: tuple[str, ...], message: str) -> None:
        if not _contains_all(granted, required):
            raise CapabilityResolutionError(message)


def _contains_all(values: tuple[str, ...], required: tuple[str, ...]) -> bool:
    available = set(values)
    return all(value in available for value in required)


__all__ = ["CapabilityResolutionError", "CapabilityResolutionResult", "CapabilityResolver"]
