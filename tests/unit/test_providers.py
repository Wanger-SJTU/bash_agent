"""Unit tests for AI providers using mocks."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from bashagnet.ai.claude import ClaudeProvider
from bashagnet.ai.openai import OpenAIProvider
from bashagnet.ai.base import AIResponse


class TestClaudeProvider:
    """Test Claude provider with mocked API calls."""

    @pytest.fixture
    def mock_config(self):
        """Mock configuration."""
        return {
            "api_key": "test-key-mock",
            "model": "claude-3-5-sonnet-20241022",
            "temperature": 0.7,
            "max_tokens": 4096,
        }

    @pytest.fixture
    def provider(self, mock_config):
        """Create provider with mock config."""
        return ClaudeProvider(mock_config)

    def test_provider_initialization(self, provider):
        """Test provider initializes correctly."""
        assert provider.model == "claude-3-5-sonnet-20241022"
        assert provider.temperature == 0.7
        assert provider.max_tokens == 4096

    @pytest.mark.asyncio
    async def test_generate_with_mock(self, provider):
        """Test generation with mocked API."""
        # Mock the API call
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="COMMAND: ls -la\nEXPLANATION: List files\nDANGEROUS: false")]

        with patch.object(provider.client.messages, 'create', new=AsyncMock(return_value=mock_response)):
            response = await provider.generate("list files")

            assert response.command == "ls -la"
            assert response.explanation == "List files"
            assert response.dangerous is False

    def test_validate_safe_command(self, provider):
        """Test validation of safe command."""
        result = provider.validate_command("ls -la", ["rm -rf", "dd if="])
        assert result.safe is True

    def test_validate_dangerous_command(self, provider):
        """Test validation of dangerous command."""
        result = provider.validate_command("rm -rf /tmp", ["rm -rf", "dd if="])
        assert result.safe is False
        assert "rm -rf" in result.reason


class TestOpenAIProvider:
    """Test OpenAI provider with mocked API calls."""

    @pytest.fixture
    def mock_config(self):
        """Mock configuration."""
        return {
            "api_key": "test-key-mock",
            "model": "gpt-4o",
            "temperature": 0.7,
            "max_tokens": 4096,
        }

    @pytest.fixture
    def provider(self, mock_config):
        """Create provider with mock config."""
        return OpenAIProvider(mock_config)

    def test_provider_initialization(self, provider):
        """Test provider initializes correctly."""
        assert provider.model == "gpt-4o"
        assert provider.temperature == 0.7
        assert provider.max_tokens == 4096

    @pytest.mark.asyncio
    async def test_generate_with_mock(self, provider):
        """Test generation with mocked API."""
        # Mock the API call
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="COMMAND: ls -la\nEXPLANATION: List files\nDANGEROUS: false"))]

        with patch.object(provider.client.chat.completions, 'create', new=AsyncMock(return_value=mock_response)):
            response = await provider.generate("list files")

            assert response.command == "ls -la"
            assert response.explanation == "List files"
            assert response.dangerous is False

    def test_validate_safe_command(self, provider):
        """Test validation of safe command."""
        result = provider.validate_command("ls -la", ["rm -rf", "dd if="])
        assert result.safe is True

    def test_validate_dangerous_command(self, provider):
        """Test validation of dangerous command."""
        result = provider.validate_command("rm -rf /tmp", ["rm -rf", "dd if="])
        assert result.safe is False
        assert "rm -rf" in result.reason


class TestProviderInterface:
    """Test provider interface consistency."""

    def test_response_parsing_claude(self):
        """Test response parsing for Claude provider."""
        config = {"api_key": "test", "model": "claude-3-5-sonnet-20241022"}
        provider = ClaudeProvider(config)

        content = """COMMAND: find / -name "*.py"
EXPLANATION: Find all Python files
DANGEROUS: false"""

        response = provider._parse_response(content)
        assert response.command == "find / -name \"*.py\""
        assert response.explanation == "Find all Python files"
        assert response.dangerous is False

    def test_response_parsing_openai(self):
        """Test response parsing for OpenAI provider."""
        config = {"api_key": "test", "model": "gpt-4o"}
        provider = OpenAIProvider(config)

        content = """COMMAND: find / -name "*.py"
EXPLANATION: Find all Python files
DANGEROUS: false"""

        response = provider._parse_response(content)
        assert response.command == "find / -name \"*.py\""
        assert response.explanation == "Find all Python files"
        assert response.dangerous is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
