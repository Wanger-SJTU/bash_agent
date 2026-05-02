#!/usr/bin/env python3
"""Test OpenAI provider integration."""

import asyncio
import os
from bashagnet.ai.openai import OpenAIProvider
from bashagnet.config import Config


async def test_openai_provider():
    """Test OpenAI provider with a simple prompt."""
    # Check for API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not set, skipping OpenAI test")
        print("   Set it with: export OPENAI_API_KEY='your-key'")
        return

    print("=" * 60)
    print("Testing OpenAI Provider")
    print("=" * 60 + "\n")

    # Create provider config
    config = {
        "api_key": os.environ["OPENAI_API_KEY"],
        "model": "gpt-4o-mini",  # Use cheaper model for testing
        "temperature": 0.7,
        "max_tokens": 500,
    }

    try:
        # Initialize provider
        provider = OpenAIProvider(config)
        print("✓ OpenAI provider initialized\n")

        # Test 1: Generate a simple command
        print("Test 1: Generate simple command")
        print("-" * 60)
        response = await provider.generate("list all files in current directory")

        print(f"Command: {response.command}")
        print(f"Explanation: {response.explanation}")
        print(f"Dangerous: {response.dangerous}")
        assert response.command, "Command should be generated"
        print("✓ Test 1 passed\n")

        # Test 2: Safety check
        print("Test 2: Safety validation")
        print("-" * 60)
        dangerous_patterns = ["rm -rf", "dd if=", "mkfs"]

        safe_check = provider.validate_command("ls -la", dangerous_patterns)
        print(f"Safe command: {safe_check.safe}")
        assert safe_check.safe, "Should be safe"
        print("✓ Safe command check passed")

        dangerous_check = provider.validate_command("rm -rf /tmp/test", dangerous_patterns)
        print(f"Dangerous command: {dangerous_check.safe}")
        print(f"Reason: {dangerous_check.reason}")
        assert not dangerous_check.safe, "Should be dangerous"
        print("✓ Dangerous command check passed\n")

        # Test 3: Streaming (optional)
        print("Test 3: Streaming test")
        print("-" * 60)
        print("Streaming response: ", end="", flush=True)
        async for chunk in provider.generate_stream("say hello"):
            print(chunk, end="", flush=True)
        print("\n✓ Streaming test passed\n")

        print("=" * 60)
        print("All OpenAI tests passed! ✓")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_openai_provider())
