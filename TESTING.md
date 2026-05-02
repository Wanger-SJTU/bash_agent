# Testing Guide - Quick Reference

## 🚀 Quick Start

### Run Tests Without API Keys (Recommended)

```bash
# All unit tests - no API keys needed
make test-unit
# or
uv run pytest tests/unit -v
```

**Result:** 26 tests pass ✅ (uses mocks, no network calls)

### Run Tests With API Keys (Optional)

```bash
# 1. Set up environment
cp .env.example .env
# Edit .env and add your keys
export $(cat .env | xargs)

# 2. Run system tests
make test-system
```

## 📊 Test Structure

```
tests/
├── unit/           # 26 tests - No API keys needed
│   ├── test_config.py      # Configuration tests
│   ├── test_executor.py    # Command executor tests
│   ├── test_safety.py      # Safety check tests
│   └── test_providers.py   # AI provider tests (mocked)
│
└── system/         # 4 tests - API keys required
    ├── test_basic.py       # Integration tests
    └── test_openai.py      # OpenAI provider tests
```

## 🧪 How Mocking Works

### Problem: Testing Without Real API Keys

```python
# ❌ This needs real API key
async def test_claude_provider():
    provider = ClaudeProvider({"api_key": "sk-ant-..."})
    response = await provider.generate("test")  # Calls real API
```

### Solution: Use Mocks

```python
# ✅ This works without API key
from unittest.mock import AsyncMock, MagicMock, patch

async def test_claude_provider():
    provider = ClaudeProvider({"api_key": "test-key-mock"})

    # Mock the API response
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="COMMAND: ls")]

    # Patch the API call
    with patch.object(provider.client.messages, 'create',
                     new=AsyncMock(return_value=mock_response)):
        response = await provider.generate("test")  # Uses mock

    assert response.command == "ls"
```

## 🛡️ Security Best Practices

### For Development

```bash
# ✅ DO: Use .env file
cp .env.example .env
# Edit .env with your keys
chmod 600 .env  # Protect file

# ❌ DON'T: Commit .env
git add .env  # Blocked by .gitignore
```

### For Testing

```bash
# ✅ DO: Use mocked unit tests
make test-unit  # No keys needed

# ⚠️  OPTIONAL: System tests require keys
export ANTHROPIC_API_KEY="sk-ant-..."
make test-system
```

### For CI/CD

```yaml
# ✅ GitHub Actions use secrets
env:
  ANTHROPIC_API_KEY: ${{ vars.ANTHROPIC_API_KEY }}

# ✅ Skip if secrets not available
if: "${{ vars.ANTHROPIC_API_KEY != '' }}"
```

## 📝 Writing New Tests

### Unit Test Template

```python
# tests/unit/test_myfeature.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from bashagnet.myfeature import MyFeature

class TestMyFeature:
    def test_initialization(self):
        """Test without API calls."""
        feature = MyFeature(config={"key": "value"})
        assert feature.value == "expected"

    @pytest.mark.asyncio
    async def test_with_mock(self):
        """Test API call with mock."""
        feature = MyFeature(config={"api_key": "mock-key"})

        # Mock the response
        mock_response = MagicMock()
        mock_response.data = "test data"

        # Patch the API call
        with patch.object(feature, 'api_call',
                         new=AsyncMock(return_value=mock_response)):
            result = await feature.do_something()

        assert result == "test data"
```

### System Test Template

```python
# tests/system/test_integration.py
import os
import pytest

@pytest.mark.system
@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="No API key provided"
)
def test_real_api_call():
    """Test with real API (requires key)."""
    from bashagnet.ai.claude import ClaudeProvider

    provider = ClaudeProvider({
        "api_key": os.environ["ANTHROPIC_API_KEY"]
    })

    response = await provider.generate("test")
    assert response.command is not None
```

## 🔍 Debugging Failed Tests

### View Detailed Output

```bash
# Show print statements
uv run pytest tests/unit/test_providers.py -v -s

# Stop on first failure
uv run pytest tests/unit -x

# Show local variables on failure
uv run pytest tests/unit -l
```

### Run Specific Test

```bash
# Single test
uv run pytest tests/unit/test_providers.py::TestClaudeProvider::test_provider_initialization

# Single class
uv run pytest tests/unit/test_providers.py::TestClaudeProvider

# Single file
uv run pytest tests/unit/test_providers.py
```

## 📈 Test Coverage

```bash
# Generate coverage report
make test-coverage

# View HTML report
open htmlcov/index.html
```

## ✅ Checklist Before Committing

- [ ] All unit tests pass: `make test-unit`
- [ ] No API keys in code
- [ ] `.env` in `.gitignore`
- [ ] New tests use mocks
- [ ] Documentation updated

## 🎯 Common Scenarios

### "I want to test AI provider logic"

```bash
# Use unit tests with mocks
uv run pytest tests/unit/test_providers.py -v
# No API key needed!
```

### "I want to test real AI integration"

```bash
# Set your key
export ANTHROPIC_API_KEY="sk-ant-..."

# Run system tests
uv run pytest tests/system/test_openai.py -v
```

### "I want to run all tests in CI"

```yaml
# .github/workflows/test.yml
# Already configured!
# Unit tests run without secrets
# System tests skip if secrets not available
```

## 📚 More Information

- Full security guide: `SECURITY.md`
- Test organization: `tests/README.md`
- GitHub Actions: `.github/workflows/test.yml`

---

**Remember:** Unit tests with mocks are fast, reliable, and secure! 🚀
