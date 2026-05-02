"""Unit tests for safety checks."""

import pytest
from bashagnet.ai.base import SafetyCheck


class TestSafetyCheck:
    """Test safety check dataclass."""

    def test_safe_command(self):
        """Test safe command check."""
        check = SafetyCheck(safe=True)
        assert check.safe is True
        assert check.reason is None
        assert check.dangerous_patterns is None

    def test_unsafe_command(self):
        """Test unsafe command check."""
        check = SafetyCheck(
            safe=False,
            reason="Contains dangerous pattern: rm -rf",
            dangerous_patterns=["rm -rf"],
        )
        assert check.safe is False
        assert "rm -rf" in check.reason
        assert "rm -rf" in check.dangerous_patterns

    def test_multiple_dangerous_patterns(self):
        """Test multiple dangerous patterns."""
        check = SafetyCheck(
            safe=False,
            reason="Multiple dangerous patterns",
            dangerous_patterns=["rm -rf", "dd if=", "mkfs"],
        )
        assert len(check.dangerous_patterns) == 3
        assert check.safe is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
