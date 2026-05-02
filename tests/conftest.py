"""Pytest configuration and fixtures."""

import pytest
import sys
from pathlib import Path


# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_config():
    """Fixture providing sample configuration."""
    from bashagnet.config import Config

    return Config()


@pytest.fixture
def sample_executor():
    """Fixture providing command executor."""
    from bashagnet.core.executor import CommandExecutor

    return CommandExecutor()
