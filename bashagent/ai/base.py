"""Abstract base class for AI providers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AIResponse:
    """Response from AI provider."""

    content: str
    command: str | None = None
    explanation: str | None = None
    dangerous: bool = False


@dataclass
class SafetyCheck:
    """Result of safety check for a command."""

    safe: bool
    reason: str | None = None
    dangerous_patterns: list[str] | None = None


class AIProvider(ABC):
    """Abstract base class for AI providers."""

    def __init__(self, config: dict):
        """Initialize provider with configuration."""
        self.config = config

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        context: str | None = None,
    ) -> AIResponse:
        """Generate response from AI."""
        pass

    @abstractmethod
    async def generate_stream(
        self,
        prompt: str,
        context: str | None = None,
    ):
        """Generate streaming response from AI."""
        pass

    @abstractmethod
    def validate_command(self, command: str, dangerous_patterns: list[str]) -> SafetyCheck:
        """Validate if a command is safe to execute."""
        pass
