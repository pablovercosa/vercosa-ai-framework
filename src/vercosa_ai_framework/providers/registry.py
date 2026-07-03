"""In-memory Provider Registry contracts."""

from __future__ import annotations

from vercosa_ai_framework.providers.types import ProviderKind, ProviderProfile


class ProviderRegistryError(ValueError):
    """Raised when a Provider Registry operation violates its contract."""


class ProviderRegistry:
    """Deterministic in-memory registry for provider profiles.

    The registry only stores and filters declarative provider contracts. It does
    not execute providers, contact MCPs, call APIs, touch databases or
    filesystems, invoke CLIs, or use subprocesses.
    """

    def __init__(self, profiles: tuple[ProviderProfile, ...] = ()) -> None:
        self._profiles: dict[str, ProviderProfile] = {}
        for profile in profiles:
            self.register(profile)

    def register(self, profile: ProviderProfile) -> ProviderProfile:
        """Register a profile by stable ID and return the stored profile."""

        if profile.provider_id in self._profiles:
            raise ProviderRegistryError(f"provider already registered: {profile.provider_id}")
        self._profiles[profile.provider_id] = profile
        return profile

    def get(self, provider_id: str) -> ProviderProfile:
        """Return a provider profile by ID."""

        try:
            return self._profiles[provider_id]
        except KeyError as exc:
            raise ProviderRegistryError(f"unknown provider: {provider_id}") from exc

    def list_profiles(self) -> tuple[ProviderProfile, ...]:
        """Return provider profiles in deterministic order."""

        return tuple(sorted(self._profiles.values(), key=_profile_sort_key))

    def find_by_name(self, name: str) -> tuple[ProviderProfile, ...]:
        """Return enabled providers matching a concrete provider name."""

        return self.filter_profiles(name=name)

    def filter_profiles(
        self,
        *,
        name: str | None = None,
        kind: ProviderKind | None = None,
        tags: tuple[str, ...] = (),
        domain: str | None = None,
        operation: str | None = None,
        enabled: bool | None = True,
        include_blocked: bool = False,
        include_dangerous: bool = False,
        include_deprecated: bool = False,
        include_experimental: bool = True,
    ) -> tuple[ProviderProfile, ...]:
        """Filter providers by declarative compatibility only."""

        matches: list[ProviderProfile] = []
        for profile in self.list_profiles():
            if name is not None and profile.name != name:
                continue
            if kind is not None and profile.kind != kind:
                continue
            if tags and not profile.has_tags(tags):
                continue
            if domain is not None and not profile.supports_domain(domain):
                continue
            if operation is not None and not profile.supports_operation(operation):
                continue
            if enabled is not None and profile.enabled is not enabled:
                continue
            if profile.blocked and not include_blocked:
                continue
            if profile.dangerous and not include_dangerous:
                continue
            if profile.deprecated and not include_deprecated:
                continue
            if profile.experimental and not include_experimental:
                continue
            matches.append(profile)
        return tuple(matches)

    def select_one(self, **filters: object) -> ProviderProfile:
        """Return the first deterministic match or raise a registry error."""

        matches = self.filter_profiles(**filters)  # type: ignore[arg-type]
        if not matches:
            raise ProviderRegistryError("no compatible provider found")
        return matches[0]


def _profile_sort_key(profile: ProviderProfile) -> tuple[str, str, str, str]:
    return (profile.name, profile.version, profile.kind.value, profile.provider_id)


__all__ = ["ProviderRegistry", "ProviderRegistryError"]
