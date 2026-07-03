from __future__ import annotations

import pytest

from vercosa_ai_framework.providers import ProviderKind, ProviderProfile, ProviderRegistry, ProviderRegistryError


def make_provider(
    provider_id: str,
    *,
    name: str = "mock_search_provider",
    kind: ProviderKind = ProviderKind.MOCK,
    domains: tuple[str, ...] = ("framework",),
    tags: tuple[str, ...] = (),
    enabled: bool = True,
    dangerous: bool = False,
    blocked: bool = False,
) -> ProviderProfile:
    return ProviderProfile(
        provider_id=provider_id,
        name=name,
        version="1.0",
        description="Declarative provider registry fixture.",
        kind=kind,
        adapter_ref=f"adapters.{provider_id}",
        supported_operations=("search",),
        supported_domains=domains,
        effects=("read",),
        required_permissions=("read_workspace",),
        tags=tags,
        enabled=enabled,
        dangerous=dangerous,
        blocked=blocked,
    )


def test_provider_registry_filters_by_name_kind_tags_and_domain():
    registry = ProviderRegistry(
        (
            make_provider("provider-search", tags=("code", "local")),
            make_provider("provider-db", name="knowledge_db", kind=ProviderKind.DATABASE, domains=("knowledge",), tags=("database",)),
        )
    )

    matches = registry.filter_profiles(name="mock_search_provider", kind=ProviderKind.MOCK, domain="framework", tags=("code",))

    assert [profile.provider_id for profile in matches] == ["provider-search"]
    assert [profile.provider_id for profile in registry.find_by_name("knowledge_db")] == ["provider-db"]


def test_provider_registry_supports_enabled_disabled_and_safe_defaults():
    registry = ProviderRegistry(
        (
            make_provider("safe-provider"),
            make_provider("disabled-provider", name="offline_provider", enabled=False),
            make_provider("dangerous-provider", name="local_cli", kind=ProviderKind.CLI, dangerous=True),
            make_provider("blocked-provider", name="blocked_api", kind=ProviderKind.API, blocked=True),
        )
    )

    assert [profile.provider_id for profile in registry.filter_profiles()] == ["safe-provider"]
    assert registry.filter_profiles(name="offline_provider") == ()
    assert registry.filter_profiles(name="offline_provider", enabled=False) != ()
    assert registry.filter_profiles(name="local_cli") == ()
    assert registry.filter_profiles(name="local_cli", include_dangerous=True) != ()
    assert registry.filter_profiles(name="blocked_api") == ()
    assert registry.filter_profiles(name="blocked_api", include_blocked=True) != ()


def test_provider_registry_filters_by_operation_and_gets_by_id():
    registry = ProviderRegistry((make_provider("provider-search"),))

    assert registry.get("provider-search").name == "mock_search_provider"
    assert registry.filter_profiles(operation="search") != ()
    assert registry.filter_profiles(operation="write") == ()


def test_provider_registry_rejects_duplicates_and_blocks_missing_selection():
    registry = ProviderRegistry((make_provider("provider-1"),))

    with pytest.raises(ProviderRegistryError, match="already registered"):
        registry.register(make_provider("provider-1"))

    with pytest.raises(ProviderRegistryError, match="no compatible"):
        registry.select_one(name="missing_provider")

    with pytest.raises(ProviderRegistryError, match="unknown provider"):
        registry.get("missing-provider")
