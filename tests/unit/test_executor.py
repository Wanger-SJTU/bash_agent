"""Unit tests for command executor."""

import pytest
from bashagnet.core.executor import CommandExecutor, ExecutionResult, ExitCode


class TestCommandExecutor:
    """Test command executor."""

    def test_executor_initialization(self):
        """Test executor initialization."""
        executor = CommandExecutor()
        assert executor.timeout == 30

    def test_custom_timeout(self):
        """Test executor with custom timeout."""
        executor = CommandExecutor(timeout=60)
        assert executor.timeout == 60


class TestExecutionResult:
    """Test execution result dataclass."""

    def test_successful_result(self):
        """Test successful execution result."""
        result = ExecutionResult(
            command="echo test",
            exit_code=0,
            stdout="test\n",
            stderr="",
            success=True,
        )
        assert result.command == "echo test"
        assert result.exit_code == 0
        assert result.success is True
        assert "test" in result.output

    def test_failed_result(self):
        """Test failed execution result."""
        result = ExecutionResult(
            command="false",
            exit_code=1,
            stdout="",
            stderr="",
            success=False,
        )
        assert result.success is False
        assert result.exit_code == 1

    def test_timed_out_result(self):
        """Test timed out execution result."""
        result = ExecutionResult(
            command="sleep 100",
            exit_code=124,
            stdout="",
            stderr="Timeout",
            success=False,
            timed_out=True,
        )
        assert result.timed_out is True
        assert result.exit_code == 124


class TestExitCode:
    """Test exit code enum."""

    def test_exit_code_values(self):
        """Test exit code enum values."""
        assert ExitCode.SUCCESS.value == 0
        assert ExitCode.ERROR.value == 1
        assert ExitCode.TIMEOUT.value == 124
        assert ExitCode.NOT_FOUND.value == 127


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
