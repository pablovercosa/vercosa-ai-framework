"""In-memory Skill Registry contracts."""

from __future__ import annotations

from vercosa_ai_framework.skills.types import SkillProfile


class SkillRegistryError(ValueError):
    """Raised when a Skill Registry operation violates its contract."""


class SkillRegistry:
    """Deterministic in-memory registry for skill profiles.

    The registry only stores and filters declarative skill contracts. It does
    not execute skills, call tools, contact providers, access MCPs, or use
    subprocesses.
    """

    def __init__(self, profiles: tuple[SkillProfile, ...] = ()) -> None:
        self._profiles: dict[str, SkillProfile] = {}
        for profile in profiles:
            self.register(profile)

    def register(self, profile: SkillProfile) -> SkillProfile:
        """Register a profile by stable ID and return the stored profile."""

        if profile.skill_id in self._profiles:
            raise SkillRegistryError(f"skill already registered: {profile.skill_id}")
        self._profiles[profile.skill_id] = profile
        return profile

    def get(self, skill_id: str) -> SkillProfile:
        """Return a skill profile by ID."""

        try:
            return self._profiles[skill_id]
        except KeyError as exc:
            raise SkillRegistryError(f"unknown skill: {skill_id}") from exc

    def list_profiles(self) -> tuple[SkillProfile, ...]:
        """Return profiles in deterministic selection order."""

        return tuple(sorted(self._profiles.values(), key=_profile_sort_key))

    def find_by_name(self, name: str) -> tuple[SkillProfile, ...]:
        """Return skills matching a reusable procedure name."""

        return self.filter_profiles(name=name)

    def find_by_capability(self, capability: str) -> tuple[SkillProfile, ...]:
        """Return candidate skills for a capability."""

        return self.filter_profiles(capability=capability)

    def filter_profiles(
        self,
        *,
        name: str | None = None,
        domain: str | None = None,
        tags: tuple[str, ...] = (),
        capability: str | None = None,
        risk_level: str | None = None,
        required_tools: tuple[str, ...] = (),
        permission_requirements: tuple[str, ...] = (),
        include_deprecated: bool = False,
        include_experimental: bool = True,
    ) -> tuple[SkillProfile, ...]:
        """Filter skills by declarative compatibility only."""

        matches: list[SkillProfile] = []
        for profile in self.list_profiles():
            if name is not None and profile.name != name:
                continue
            if domain is not None and profile.domain != domain:
                continue
            if tags and not profile.has_tags(tags):
                continue
            if capability is not None and not profile.implements_capability(capability):
                continue
            if risk_level is not None and profile.risk_level != risk_level:
                continue
            if required_tools and not _contains_all(profile.required_tools, required_tools):
                continue
            if permission_requirements and not _contains_all(profile.permission_requirements, permission_requirements):
                continue
            if profile.deprecated and not include_deprecated:
                continue
            if profile.experimental and not include_experimental:
                continue
            matches.append(profile)
        return tuple(matches)

    def select_one(self, **filters: object) -> SkillProfile:
        """Return the first deterministic match or raise a registry error."""

        matches = self.filter_profiles(**filters)  # type: ignore[arg-type]
        if not matches:
            raise SkillRegistryError("no compatible skill found")
        return matches[0]


def _contains_all(values: tuple[str, ...], required: tuple[str, ...]) -> bool:
    available = set(values)
    return all(value in available for value in required)


def _profile_sort_key(profile: SkillProfile) -> tuple[int, str, str, str, str]:
    return (profile.priority, profile.name, profile.version, profile.domain, profile.skill_id)


__all__ = ["SkillRegistry", "SkillRegistryError"]
