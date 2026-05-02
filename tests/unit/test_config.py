"""Unit tests for configuration management."""

import pytest
from bashagnet.config import Config, AIProviderConfig, ShellConfig, SecurityConfig


class TestAIProviderConfig:
    """Test AI provider configuration."""

    def test_default_config(self):
        """Test default configuration values."""
        config = AIProviderConfig()
        assert config.provider == "claude"
        assert config.model == "claude-3-5-sonnet-20241022"
        assert config.temperature == 0.7
        assert config.max_tokens == 4096

    def test_custom_config(self):
        """Test custom configuration values."""
        config = AIProviderConfig(
            provider="openai",
            model="gpt-4o",
            temperature=0.5,
            max_tokens=2048,
        )
        assert config.provider == "openai"
        assert config.model == "gpt-4o"
        assert config.temperature == 0.5
        assert config.max_tokens == 2048


class TestShellConfig:
    """Test shell configuration."""

    def test_default_shell_config(self):
        """Test default shell configuration."""
        config = ShellConfig()
        assert config.history_file == "~/.bash_history"
        assert config.max_history == 1000
        assert config.enable_completion is True
        assert config.confirmation_dangerous is True


class TestSecurityConfig:
    """Test security configuration."""

    def test_default_security_config(self):
        """Test default security configuration."""
        config = SecurityConfig()
        assert config.allowed_commands == []
        assert "rm -rf" in config.dangerous_commands
        assert config.require_confirmation is True
        assert config.sandbox_mode is False

    def test_dangerous_commands_list(self):
        """Test dangerous commands list."""
        config = SecurityConfig()
        expected_dangerous = ["rm -rf", "mkfs", "dd if=", ">:", "format", "fdisk"]
        for cmd in expected_dangerous:
            assert cmd in config.dangerous_commands


class TestConfig:
    """Test main configuration."""

    def test_default_main_config(self):
        """Test default main configuration."""
        config = Config()
        assert isinstance(config.ai, AIProviderConfig)
        assert isinstance(config.shell, ShellConfig)
        assert isinstance(config.security, SecurityConfig)

    def test_config_hierarchy(self):
        """Test configuration hierarchy."""
        config = Config()
        # Verify all sub-configs are properly initialized
        assert config.ai.provider == "claude"
        assert config.shell.max_history == 1000
        assert len(config.security.dangerous_commands) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
