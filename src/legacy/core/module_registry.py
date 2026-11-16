"""Central registry for independent THE LEGACY modules."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ModuleInfo:
    name: str
    description: str
    enabled: bool = True


class ModuleRegistry:
    def __init__(self) -> None:
        self._modules: dict[str, ModuleInfo] = {}

    def register(self, module: ModuleInfo) -> None:
        key = module.name.strip().lower()
        if not key:
            raise ValueError("Module name cannot be empty.")
        if key in self._modules:
            raise ValueError(f"Module already registered: {module.name}")
        self._modules[key] = module

    def get(self, name: str) -> ModuleInfo | None:
        return self._modules.get(name.strip().lower())

    def list_modules(self) -> list[ModuleInfo]:
        return list(self._modules.values())
