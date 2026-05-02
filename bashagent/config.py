"""Configuration management using Pydantic."""

import os
from pathlib import Path
from typing import Optional

import pydantic.v1 as pydantic
import yaml


class AIProviderConfig(pydantic.BaseModel):
    """AI provider configuration."""

    provider: str = "claude"  # claude, openai, local
    model: str = "claude-3-5-sonnet-20241022"
    api_key: Optional[str] = None
    base_url: Optional[str] = None  # For local models
    temperature: float = 0.7
    max_tokens: int = 4096


class ShellConfig(pydantic.BaseModel):
    """Shell configuration."""

    history_file: str = "~/.bash_history"
    max_history: int = 1000
    enable_completion: bool = True
    confirmation_dangerous: bool = True


class SecurityConfig(pydantic.BaseModel):
    """Security configuration."""

    allowed_commands: list[str] = []  # Empty means all commands allowed
    dangerous_commands: list[str] = [
        "rm -rf",
        "mkfs",
        "dd if=",
        ">:",
        "format",
        "fdisk",
    ]
    require_confirmation: bool = True
    sandbox_mode: bool = False


class Config(pydantic.BaseModel):
    """Main configuration model."""

    ai: AIProviderConfig = pydantic.Field(default_factory=AIProviderConfig)
    shell: ShellConfig = pydantic.Field(default_factory=ShellConfig)
    security: SecurityConfig = pydantic.Field(default_factory=SecurityConfig)

    @classmethod
    def load_from_file(cls, path: Path | str) -> "Config":
        """Load configuration from YAML file."""
        path = Path(path).expanduser()
        if not path.exists():
            return cls()

        with open(path) as f:
            data = yaml.safe_load(f) or {}

        # Expand environment variables in strings
        data = cls._expand_env_vars(data)
        return cls(**data)

    @classmethod
    def load_default(cls) -> "Config":
        """Load configuration from default locations."""
        # Check config directory
        config_paths = [
            Path("~/.config/bashagnet/config.yaml"),
            Path("~/.bashagnet.yaml"),
            Path("./bashagnet.yaml"),
        ]

        for path in config_paths:
            path = path.expanduser()
            if path.exists():
                return cls.load_from_file(path)

        return cls()

    @staticmethod
    def _expand_env_vars(data: dict) -> dict:
        """Recursively expand environment variables in strings."""
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                # Expand ${VAR} and $VAR
                result[key] = os.path.expandvars(value)
            elif isinstance(value, dict):
                result[key] = Config._expand_env_vars(value)
            elif isinstance(value, list):
                result[key] = [
                    Config._expand_env_vars(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                result[key] = value
        return result
