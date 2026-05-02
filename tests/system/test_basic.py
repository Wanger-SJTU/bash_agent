#!/usr/bin/env python3
"""Basic functionality tests without AI."""

import asyncio
from bashagnet.core.executor import CommandExecutor
from bashagnet.config import Config


def test_executor():
    """Test command executor."""
    print("Testing command executor...")

    executor = CommandExecutor()

    # Test simple command
    result = executor.execute_sync("echo 'Hello, World!'")

    print(f"Command: {result.command}")
    print(f"Exit code: {result.exit_code}")
    print(f"Success: {result.success}")
    print(f"Output: {result.stdout}")

    assert result.success
    assert "Hello, World!" in result.stdout
    print("✓ Executor test passed!\n")


def test_config():
    """Test configuration loading."""
    print("Testing configuration...")

    # Load default config
    cfg = Config.load_default()

    print(f"AI Provider: {cfg.ai.provider}")
    print(f"Model: {cfg.ai.model}")
    print(f"History file: {cfg.shell.history_file}")
    print(f"Dangerous commands: {len(cfg.security.dangerous_commands)}")

    assert cfg.ai.provider == "claude"
    assert len(cfg.security.dangerous_commands) > 0
    print("✓ Config test passed!\n")


def test_safety_check():
    """Test command safety validation."""
    print("Testing safety checks...")

    from bashagnet.ai.claude import ClaudeProvider

    # Mock config
    config = {
        "api_key": "test-key",  # Not used for safety check
        "model": "claude-3-5-sonnet-20241022",
    }

    provider = ClaudeProvider(config)

    # Safe command
    safe_result = provider.validate_command("ls -la", ["rm -rf", "dd if="])
    print(f"Safe command validation: {safe_result.safe}")
    assert safe_result.safe

    # Dangerous command
    dangerous_result = provider.validate_command("rm -rf /", ["rm -rf", "dd if="])
    print(f"Dangerous command validation: {dangerous_result.safe}")
    print(f"Reason: {dangerous_result.reason}")
    assert not dangerous_result.safe

    print("✓ Safety check test passed!\n")


if __name__ == "__main__":
    print("=" * 60)
    print("Bashagnet Basic Tests")
    print("=" * 60 + "\n")

    test_config()
    test_executor()
    test_safety_check()

    print("=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
