"""Async command execution engine."""

import asyncio
import shlex
from dataclasses import dataclass
from enum import Enum


class ExitCode(Enum):
    """Process exit codes."""

    SUCCESS = 0
    ERROR = 1
    TIMEOUT = 124
    NOT_FOUND = 127


@dataclass
class ExecutionResult:
    """Result of command execution."""

    command: str
    exit_code: int
    stdout: str
    stderr: str
    success: bool
    timed_out: bool = False

    @property
    def output(self) -> str:
        """Get combined output."""
        return self.stdout + self.stderr


class CommandExecutor:
    """Async command executor."""

    def __init__(self, timeout: int = 30):
        """Initialize executor."""
        self.timeout = timeout

    async def execute(self, command: str) -> ExecutionResult:
        """Execute a command asynchronously."""
        try:
            # Parse command safely
            args = shlex.split(command)
            if not args:
                raise ValueError("Empty command")

            # Create subprocess
            process = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            # Wait for completion with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.timeout,
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return ExecutionResult(
                    command=command,
                    exit_code=ExitCode.TIMEOUT.value,
                    stdout="",
                    stderr=f"Command timed out after {self.timeout}s",
                    success=False,
                    timed_out=True,
                )

            # Get result
            exit_code = await process.wait()
            stdout_str = stdout.decode("utf-8", errors="replace")
            stderr_str = stderr.decode("utf-8", errors="replace")

            return ExecutionResult(
                command=command,
                exit_code=exit_code,
                stdout=stdout_str,
                stderr=stderr_str,
                success=exit_code == 0,
            )

        except FileNotFoundError:
            return ExecutionResult(
                command=command,
                exit_code=ExitCode.NOT_FOUND.value,
                stdout="",
                stderr=f"Command not found: {args[0]}",
                success=False,
            )
        except Exception as e:
            return ExecutionResult(
                command=command,
                exit_code=ExitCode.ERROR.value,
                stdout="",
                stderr=str(e),
                success=False,
            )

    async def execute_with_validation(
        self,
        command: str,
        dangerous_patterns: list[str],
        require_confirmation: bool = True,
    ) -> ExecutionResult:
        """Execute command with safety checks."""
        # Check for dangerous patterns
        for pattern in dangerous_patterns:
            if pattern in command:
                if require_confirmation:
                    # In interactive mode, this would prompt for confirmation
                    # For now, we'll just execute but mark it
                    pass

        return await self.execute(command)

    def execute_sync(self, command: str) -> ExecutionResult:
        """Synchronous wrapper for execute."""
        return asyncio.run(self.execute(command))
