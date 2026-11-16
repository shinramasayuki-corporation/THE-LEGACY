from legacy.core.config import LegacyConfig


def test_default_configuration(monkeypatch):
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    config = LegacyConfig.from_environment()

    assert config.name == "THE LEGACY"
    assert config.version == "0.1.0"
    assert config.environment == "development"
    assert config.log_level == "INFO"


def test_environment_configuration(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "testing")
    monkeypatch.setenv("LOG_LEVEL", "debug")

    config = LegacyConfig.from_environment()

    assert config.environment == "testing"
    assert config.log_level == "DEBUG"
