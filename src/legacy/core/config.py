"""Application configuration."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class LegacyConfig:
    name: str = "THE LEGACY"
    version: str = "0.1.0"
    environment: str = "development"
    log_level: str = "INFO"

    @classmethod
    def from_environment(cls) -> "LegacyConfig":
        return cls(
            environment=os.getenv("ENVIRONMENT", "development"),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )
