"""In-memory Agent Registry contracts."""

from __future__ import annotations

from vercosa_ai_framework.agents.types import AgentProfile, AgentRole


class AgentRegistryError(ValueError):
    """Raised when an Agent Registry operation violates its contract."""


class AgentRegistry:
    """Deterministic in-memory registry for agent profiles.

    The registry only stores and filters provider-neutral profiles. It does not
    execute agents, call runtime adapters, resolve capabilities, or contact MCPs,
    APIs, providers, databases, or subprocesses.
    """

    def __init__(self, profiles: tuple[AgentProfile, ...] = ()) -> None:
        self._profiles: dict[str, AgentProfile] = {}
        for profile in profiles:
            self.register(profile)

    def register(self, profile: AgentProfile) -> AgentProfile:
        """Register a profile by stable ID and return the stored profile."""

        if profile.agent_profile_id in self._profiles:
            raise AgentRegistryError(f"agent profile already registered: {profile.agent_profile_id}")
        self._profiles[profile.agent_profile_id] = profile
        return profile

    def get(self, agent_profile_id: str) -> AgentProfile:
        """Return a profile by ID."""

        try:
            return self._profiles[agent_profile_id]
        except KeyError as exc:
            raise AgentRegistryError(f"unknown agent profile: {agent_profile_id}") from exc

    def list_profiles(self) -> tuple[AgentProfile, ...]:
        """Return profiles in deterministic selection order."""

        return tuple(sorted(self._profiles.values(), key=_profile_sort_key))

    def find_by_role(self, role: AgentRole | str) -> tuple[AgentProfile, ...]:
        """Return profiles matching a role in deterministic order."""

        agent_role = AgentRole(role)
        return self.filter_profiles(role=agent_role)

    def filter_profiles(
        self,
        *,
        role: AgentRole | str | None = None,
        domain: str | None = None,
        tags: tuple[str, ...] = (),
        required_capabilities: tuple[str, ...] = (),
        task_type: str | None = None,
        complexity: str | None = None,
        risk_level: str | None = None,
    ) -> tuple[AgentProfile, ...]:
        """Filter profiles by declarative compatibility only."""

        agent_role = AgentRole(role) if role is not None else None
        matches: list[AgentProfile] = []
        for profile in self.list_profiles():
            if agent_role is not None and profile.role != agent_role:
                continue
            if domain is not None and profile.domain != domain:
                continue
            if tags and not profile.has_tags(tags):
                continue
            if required_capabilities and not profile.supports_capabilities(required_capabilities):
                continue
            if task_type is not None and task_type not in profile.supported_task_types:
                continue
            if complexity is not None and complexity not in profile.complexity_range:
                continue
            if risk_level is not None and risk_level not in profile.risk_range:
                continue
            matches.append(profile)
        return tuple(matches)

    def select_one(
        self,
        *,
        role: AgentRole | str | None = None,
        domain: str | None = None,
        tags: tuple[str, ...] = (),
        required_capabilities: tuple[str, ...] = (),
        task_type: str | None = None,
        complexity: str | None = None,
        risk_level: str | None = None,
    ) -> AgentProfile:
        """Return the first deterministic match or raise a registry error."""

        matches = self.filter_profiles(
            role=role,
            domain=domain,
            tags=tags,
            required_capabilities=required_capabilities,
            task_type=task_type,
            complexity=complexity,
            risk_level=risk_level,
        )
        if not matches:
            raise AgentRegistryError("no compatible agent profile found")
        return matches[0]


def _profile_sort_key(profile: AgentProfile) -> tuple[str, str, str]:
    return (profile.role.value, profile.domain, profile.agent_profile_id)


__all__ = ["AgentRegistry", "AgentRegistryError"]
