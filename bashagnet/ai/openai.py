"""OpenAI AI provider implementation."""

import os
from typing import AsyncIterator

from openai import AsyncOpenAI

from bashagnet.ai.base import AIProvider, AIResponse, SafetyCheck
from bashagnet.prompts import PromptManager


class OpenAIProvider(AIProvider):
    """OpenAI API provider."""

    def __init__(self, config: dict):
        """Initialize OpenAI provider."""
        super().__init__(config)
        api_key = config.get("api_key") or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found\n\n"
                "To use bashagnet:\n"
                "1. Get your API key from https://platform.openai.com/\n"
                "2. Set it as environment variable:\n"
                "   export OPENAI_API_KEY='sk-...'\n"
                "3. Or create a .env file:\n"
                "   echo 'OPENAI_API_KEY=sk-...' > .env\n"
                "   source .env\n\n"
                "See docs/QUICKSTART.md for more information."
            )

        base_url = config.get("base_url")
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,  # Support custom endpoints (e.g., local models)
        )
        self.model = config.get("model", "gpt-4o")
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
        """Generate response from OpenAI."""
        user_message = self._build_user_message(prompt, context)

        response = await self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message},
            ],
        )

        content = response.choices[0].message.content
        return self._parse_response(content)

    async def generate_stream(
        self,
        prompt: str,
        context: str | None = None,
    ) -> AsyncIterator[str]:
        """Generate streaming response from OpenAI."""
        user_message = self._build_user_message(prompt, context)

        stream = await self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message},
            ],
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

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
        """Parse OpenAI's response into AIResponse."""
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
