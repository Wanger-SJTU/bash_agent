"""Claude AI provider implementation."""

import os
from typing import AsyncIterator

import anthropic
from anthropic import AsyncAnthropic

from bashagnet.ai.base import AIProvider, AIResponse, SafetyCheck
from bashagnet.prompts import PromptManager


class ClaudeProvider(AIProvider):
    """Claude API provider."""

    def __init__(self, config: dict):
        """Initialize Claude provider."""
        super().__init__(config)
        api_key = config.get("api_key") or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")

        self.client = AsyncAnthropic(api_key=api_key)
        self.model = config.get("model", "claude-3-5-sonnet-20241022")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 4096)

        # Initialize prompt manager
        prompt_name = config.get("system_prompt", "default")
        self.prompt_manager = PromptManager()
        self.system_prompt = self.prompt_manager.get_prompt(prompt_name)

    async def generate(
        self,
        prompt: str,
        context: str | None = None,
    ) -> AIResponse:
        """Generate response from Claude."""
        user_message = self._build_user_message(prompt, context)

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=self.system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )

        content = response.content[0].text
        return self._parse_response(content)

    async def generate_stream(
        self,
        prompt: str,
        context: str | None = None,
    ) -> AsyncIterator[str]:
        """Generate streaming response from Claude."""
        user_message = self._build_user_message(prompt, context)

        async with self.client.messages.stream(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=self.system_prompt,
            messages=[{"role": "user", "content": user_message}],
        ) as stream:
            async for text in stream.text_stream:
                yield text

    def validate_command(self, command: str, dangerous_patterns: list[str]) -> SafetyCheck:
        """Validate if a command is safe to execute."""
        dangerous_found = []
        for pattern in dangerous_patterns:
            if pattern in command:
                dangerous_found.append(pattern)

        if dangerous_found:
            return SafetyCheck(
                safe=False,
                reason=f"Command contains dangerous patterns: {', '.join(dangerous_found)}",
                dangerous_patterns=dangerous_found,
            )

        return SafetyCheck(safe=True)

    def _build_user_message(self, prompt: str, context: str | None = None) -> str:
        """Build user message with context."""
        message = f"User request: {prompt}"
        if context:
            message += f"\n\nContext: {context}"
        return message

    def _parse_response(self, content: str) -> AIResponse:
        """Parse Claude's response into AIResponse."""
        command = None
        explanation = None
        dangerous = False

        for line in content.split("\n"):
            if line.startswith("COMMAND:"):
                command = line.split("COMMAND:", 1)[1].strip()
            elif line.startswith("EXPLANATION:"):
                explanation = line.split("EXPLANATION:", 1)[1].strip()
            elif line.startswith("DANGEROUS:"):
                dangerous_str = line.split("DANGEROUS:", 1)[1].strip().lower()
                dangerous = dangerous_str in ["true", "yes", "1"]

        return AIResponse(
            content=content,
            command=command,
            explanation=explanation,
            dangerous=dangerous,
        )
