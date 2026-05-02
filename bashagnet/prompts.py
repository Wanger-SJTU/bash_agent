"""System prompt management."""

import os
from pathlib import Path
from typing import Optional

import yaml


class PromptManager:
    """Manage system prompts from configuration files."""

    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize prompt manager.

        Args:
            config_dir: Directory containing prompt files. Defaults to:
                        - ~/.config/bashagnet/prompts/
                        - /etc/bashagnet/prompts/
                        - <package>/config/prompts/
        """
        self.config_dir = config_dir
        self._prompts = {}

    def get_prompt(self, name: str = "default") -> str:
        """Get system prompt by name.

        Args:
            name: Prompt name (default, concise, verbose, etc.)

        Returns:
            System prompt string
        """
        if name not in self._prompts:
            self._prompts[name] = self._load_prompt(name)

        return self._prompts[name]

    def _load_prompt(self, name: str) -> str:
        """Load prompt from file or use default."""
        # Search paths for prompt files
        search_paths = [
            Path("~/.config/bashagnet/prompts").expanduser() / f"{name}.yaml",
            Path("/etc/bashagnet/prompts") / f"{name}.yaml",
            Path(__file__).parent.parent / "config" / "prompts" / f"{name}.yaml",
        ]

        # Try to load from file
        for path in search_paths:
            if path.exists():
                try:
                    with open(path) as f:
                        data = yaml.safe_load(f)
                    return data.get("system_prompt", self._default_prompt())
                except Exception:
                    pass

        # Fallback to default
        return self._default_prompt()

    def _default_prompt(self) -> str:
        """Default system prompt."""
        return """You are a bash shell assistant. Your role is to help users execute shell commands safely and efficiently.

When the user asks for something:
1. Generate the appropriate bash command
2. Provide a brief explanation of what the command does
3. Warn about any potential dangers

Format your response as:
COMMAND: <the bash command>
EXPLANATION: <brief explanation>
DANGEROUS: <true/false if the command is destructive>

If the user's request is unclear, ask for clarification."""

    def reload(self):
        """Reload all prompts from disk."""
        self._prompts = {}
