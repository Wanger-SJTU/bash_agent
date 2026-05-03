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
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 4096)

        # Initialize prompt manager
        prompt_name = config.get("system_prompt", "default")
        self.prompt_manager = PromptManager()
        self.system_prompt = self.prompt_manager.get_prompt(prompt_name)
