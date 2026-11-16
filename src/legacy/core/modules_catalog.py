"""Official catalog of THE LEGACY modules."""

from legacy.core.module_registry import ModuleInfo, ModuleRegistry


MODULES = (
    ("ACADEMY", "Education and learning paths."),
    ("KNOWLEDGE", "Knowledge and critical thinking."),
    ("LANGUAGES", "Multilingual learning."),
    ("HEALTH", "Health education and prevention."),
    ("SPORTS", "Sports and physical activity."),
    ("WEALTH", "Financial education and autonomy."),
    ("TALENTS", "Creative and professional development."),
    ("TECHNOLOGY", "Technology and artificial intelligence."),
    ("GLOBAL", "International information and discovery."),
    ("COMMUNITY", "Community and social interaction."),
    ("AVATAR", "Personalized digital assistant."),
)


def create_module_registry() -> ModuleRegistry:
    registry = ModuleRegistry()
    for name, description in MODULES:
        registry.register(ModuleInfo(name=name, description=description))
    return registry
