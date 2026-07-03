"""In-memory Capability Registry contracts."""

from __future__ import annotations

from vercosa_ai_framework.capabilities.types import CapabilityProfile


class CapabilityRegistryError(ValueError):
    """Raised when a Capability Registry operation violates its contract."""


class CapabilityRegistry:
    """Deterministic in-memory registry for capability profiles.

    The registry only stores and filters declarative capability contracts. It
    does not execute skills, call tools, contact providers, access MCPs, or use
    subprocesses.
    """

    def __init__(self, profiles: tuple[CapabilityProfile, ...] = ()) -> None:
        self._profiles: dict[str, CapabilityProfile] = {}
        for profile in profiles:
            self.register(profile)

    def register(self, profile: CapabilityProfile) -> CapabilityProfile:
        """Register a profile by stable ID and return the stored profile."""

        if profile.capability_id in self._profiles:
            raise CapabilityRegistryError(f"capability already registered: {profile.capability_id}")
        self._profiles[profile.capability_id] = profile
        return profile

    def get(self, capability_id: str) -> CapabilityProfile:
        """Return a capability profile by ID."""

        try:
            return self._profiles[capability_id]
        except KeyError as exc:
            raise CapabilityRegistryError(f"unknown capability: {capability_id}") from exc

    def list_profiles(self) -> tuple[CapabilityProfile, ...]:
        """Return profiles in deterministic order."""

        return tuple(sorted(self._profiles.values(), key=_profile_sort_key))

    def find_by_name(self, name: str) -> tuple[CapabilityProfile, ...]:
        """Return capabilities matching a functional name."""

        return self.filter_profiles(name=name)

    def filter_profiles(
        self,
        *,
        name: str | None = None,
        domain: str | None = None,
        tags: tuple[str, ...] = (),
        risk_level: str | None = None,
        required_permissions: tuple[str, ...] = (),
        agent_role: str | None = None,
        task_type: str | None = None,
        include_deprecated: bool = False,
        include_experimental: bool = True,
    ) -> tuple[CapabilityProfile, ...]:
        """Filter capabilities by declarative compatibility only."""

        matches: list[CapabilityProfile] = []
        for profile in self.list_profiles():
            if name is not None and profile.name != name:
                continue
            if domain is not None and profile.domain != domain:
                continue
            if tags and not profile.has_tags(tags):
                continue
            if risk_level is not None and profile.risk_level != risk_level:
                continue
            if required_permissions and not _contains_all(profile.required_permissions, required_permissions):
                continue
            if agent_role is not None and not profile.allows_agent_role(agent_role):
                continue
            if task_type is not None and not profile.allows_task_type(task_type):
                continue
            if profile.deprecated and not include_deprecated:
                continue
            if profile.experimental and not include_experimental:
                continue
            matches.append(profile)
        return tuple(matches)

    def select_one(self, **filters: object) -> CapabilityProfile:
        """Return the first deterministic match or raise a registry error."""

        matches = self.filter_profiles(**filters)  # type: ignore[arg-type]
        if not matches:
            raise CapabilityRegistryError("no compatible capability found")
        return matches[0]


def _contains_all(values: tuple[str, ...], required: tuple[str, ...]) -> bool:
    available = set(values)
    return all(value in available for value in required)


def _profile_sort_key(profile: CapabilityProfile) -> tuple[str, str, str, str]:
    return (profile.name, profile.version, profile.domain, profile.capability_id)


__all__ = ["CapabilityRegistry", "CapabilityRegistryError"]
