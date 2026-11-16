"""Main entry point for THE LEGACY."""

import logging

from dotenv import load_dotenv

from legacy.core.config import LegacyConfig
from legacy.core.logging import configure_logging
from legacy.core.modules_catalog import create_module_registry


def main() -> None:
    load_dotenv()
    configure_logging()

    config = LegacyConfig.from_environment()
    logger = logging.getLogger("legacy")
    registry = create_module_registry()

    logger.info("%s v%s", config.name, config.version)
    logger.info("Environment: %s", config.environment)
    logger.info("Registered modules: %s", len(registry.list_modules()))

    for module in registry.list_modules():
        logger.info("Module available: %s", module.name)


if __name__ == "__main__":
    main()
