# Test Structure

This directory contains all tests for bashagnet, organized by type.

## Directory Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── unit/                    # Unit tests (UT)
│   ├── test_config.py       # Configuration management tests
│   ├── test_executor.py     # Command executor tests
│   └── test_safety.py       # Safety check tests
└── system/                  # System tests (ST)
    ├── test_basic.py        # Basic system integration tests
    └── test_openai.py       # OpenAI provider integration tests
```

## Test Types

### Unit Tests (UT)
Located in `tests/unit/`

- Test individual components in isolation
- Fast execution
- No external dependencies (API keys, network, etc.)
- Mock external services

**Examples:**
- Configuration validation
- Data class behavior
- Individual function logic

### System Tests (ST)
Located in `tests/system/`

- Test the entire system integration
- May require external dependencies (API keys, network)
- Slower execution
- Test real-world scenarios

**Examples:**
- End-to-end command execution
- AI provider integration
- Interactive mode

## Running Tests

### All tests
```bash
make test
# or
uv run pytest
```

### Unit tests only
```bash
make test-unit
# or
uv run pytest tests/unit -v
```

### System tests only
```bash
make test-system
# or
uv run pytest tests/system -v
```

### Specific test file
```bash
uv run pytest tests/unit/test_config.py -v
```

### Specific test function
```bash
uv run pytest tests/unit/test_config.py::TestAIProviderConfig::test_default_config -v
```

### With coverage
```bash
make test-coverage
# or
uv run pytest --cov=bashagnet --cov-report=html
```

## Writing Tests

### Unit Test Example

```python
# tests/unit/test_mycomponent.py
import pytest
from bashagnet.mycomponent import MyComponent

class TestMyComponent:
    def test_initialization(self):
        component = MyComponent()
        assert component.value == "default"

    def test_custom_value(self):
        component = MyComponent(value="custom")
        assert component.value == "custom"
```

### System Test Example

```python
# tests/system/test_integration.py
import pytest
from bashagnet.cli import main

@pytest.mark.system
def test_command_generation():
    # This may require API keys
    result = main("list files")
    assert result.exit_code == 0
```

## Test Markers

Tests can be marked with:
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.system` - System tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow running tests

Run specific markers:
```bash
uv run pytest -m unit
uv run pytest -m "not slow"
```

## Fixtures

Common fixtures are defined in `tests/conftest.py`:

- `sample_config` - Provides a Config instance
- `sample_executor` - Provides a CommandExecutor instance

Use fixtures in tests:
```python
def test_with_fixture(sample_config):
    assert sample_config.ai.provider == "claude"
```

## Environment Variables

Some system tests may require:
- `ANTHROPIC_API_KEY` - For Claude tests
- `OPENAI_API_KEY` - For OpenAI tests

These should be set before running system tests:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
make test-system
```

## CI/CD

In CI environments:
- Run unit tests by default (fast, no dependencies)
- Run system tests only when secrets are available
- Use test markers to control execution
