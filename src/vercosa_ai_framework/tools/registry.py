"""In-memory Tool Registry contracts."""

from __future__ import annotations

from vercosa_ai_framework.tools.types import ToolProfile


class ToolRegistryError(ValueError):
    """Raised when a Tool Registry operation violates its contract."""


class ToolRegistry:
    """Deterministic in-memory registry for tool profiles.

    The registry only stores and filters declarative tool contracts. It does not
    execute tools, contact providers, access MCPs, call APIs, touch databases,
    inspect filesystems, or use subprocesses.
    """

    def __init__(self, profiles: tuple[ToolProfile, ...] = ()) -> None:
        self._profiles: dict[str, ToolProfile] = {}
        for profile in profiles:
            self.register(profile)

    def register(self, profile: ToolProfile) -> ToolProfile:
        """Register a profile by stable ID and return the stored profile."""

        if profile.tool_id in self._profiles:
            raise ToolRegistryError(f"tool already registered: {profile.tool_id}")
        self._profiles[profile.tool_id] = profile
        return profile

    def get(self, tool_id: str) -> ToolProfile:
        """Return a tool profile by ID."""

        try:
            return self._profiles[tool_id]
        except KeyError as exc:
            raise ToolRegistryError(f"unknown tool: {tool_id}") from exc

    def list_profiles(self) -> tuple[ToolProfile, ...]:
        """Return profiles in deterministic order."""

        return tuple(sorted(self._profiles.values(), key=_profile_sort_key))

    def find_by_name(self, name: str) -> tuple[ToolProfile, ...]:
        """Return tools matching a concrete operation name."""

        return self.filter_profiles(name=name)

    def filter_profiles(
        self,
        *,
        name: str | None = None,
        domain: str | None = None,
        tags: tuple[str, ...] = (),
        provider_type: str | None = None,
        operation_type: str | None = None,
        effects: tuple[str, ...] = (),
        required_permissions: tuple[str, ...] = (),
        available: bool | None = True,
        include_dangerous: bool = False,
        include_deprecated: bool = False,
        include_experimental: bool = True,
    ) -> tuple[ToolProfile, ...]:
        """Filter tools by declarative compatibility only."""

        matches: list[ToolProfile] = []
        for profile in self.list_profiles():
            if name is not None and profile.name != name:
                continue
            if domain is not None and profile.domain != domain:
                continue
            if tags and not profile.has_tags(tags):
                continue
            if provider_type is not None and profile.provider_type != provider_type:
                continue
            if operation_type is not None and profile.operation_type != operation_type:
                continue
            if effects and not profile.has_effects(effects):
                continue
            if required_permissions and not _contains_all(profile.required_permissions, required_permissions):
                continue
            if available is not None and profile.available is not available:
                continue
            if profile.dangerous and not include_dangerous:
                continue
            if profile.deprecated and not include_deprecated:
                continue
            if profile.experimental and not include_experimental:
                continue
            matches.append(profile)
        return tuple(matches)

    def select_one(self, **filters: object) -> ToolProfile:
        """Return the first deterministic match or raise a registry error."""

        matches = self.filter_profiles(**filters)  # type: ignore[arg-type]
        if not matches:
            raise ToolRegistryError("no compatible tool found")
        return matches[0]


def _contains_all(values: tuple[str, ...], required: tuple[str, ...]) -> bool:
    available = set(values)
    return all(value in available for value in required)


def _profile_sort_key(profile: ToolProfile) -> tuple[str, str, str, str]:
    return (profile.name, profile.version, profile.domain, profile.tool_id)


__all__ = ["ToolRegistry", "ToolRegistryError"]
