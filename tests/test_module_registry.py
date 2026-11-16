import pytest

from legacy.core.module_registry import ModuleInfo, ModuleRegistry
from legacy.core.modules_catalog import create_module_registry


def test_register_and_retrieve_module():
    registry = ModuleRegistry()
    module = ModuleInfo("ACADEMY", "Education")
    registry.register(module)

    assert registry.get("academy") == module


def test_duplicate_module_is_rejected():
    registry = ModuleRegistry()
    registry.register(ModuleInfo("ACADEMY", "Education"))

    with pytest.raises(ValueError):
        registry.register(ModuleInfo("academy", "Duplicate"))


def test_empty_module_name_is_rejected():
    registry = ModuleRegistry()

    with pytest.raises(ValueError):
        registry.register(ModuleInfo(" ", "Invalid"))


def test_catalog_contains_eleven_modules():
    registry = create_module_registry()

    assert len(registry.list_modules()) == 11


def test_all_official_modules_are_available():
    registry = create_module_registry()
    expected = {
        "academy", "knowledge", "languages", "health", "sports",
        "wealth", "talents", "technology", "global", "community", "avatar",
    }

    assert {module.name.lower() for module in registry.list_modules()} == expected
