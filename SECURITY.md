# Security Guide for API Keys and Testing

## 🛡️ Protecting API Keys

### Rule #1: NEVER commit API keys to git

API keys should NEVER be in:
- ❌ Committed code
- ❌ Configuration files in the repo
- ❌ Environment files (.env)
- ❌ README examples
- ❌ Git history

### ✅ Safe Ways to Manage API Keys

#### 1. Environment Variables (Recommended for Development)

```bash
# Set in your shell
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."

# Or in .env file (NEVER commit .env)
echo 'ANTHROPIC_API_KEY=sk-ant-...' > .env
echo 'OPENAI_API_KEY=sk-...' >> .env
```

#### 2. User Configuration File

Create `~/.config/bashagnet/config.yaml`:

```yaml
ai:
  provider: claude
  api_key: ${ANTHROPIC_API_KEY}  # Reference env var
```

The file path is ignored by git and safe to use.

#### 3. CLI Flags (One-time use)

```bash
ANTHROPIC_API_KEY="sk-ant-..." bashagnet "test"
```

## 🧪 Testing Without Real API Keys

### Unit Tests (No API Keys Needed)

Unit tests use **mocks** and don't require real API keys:

```bash
# These work without any API keys
make test-unit
uv run pytest tests/unit -v
```

**How it works:**
- Mock API responses
- Test logic, not external services
- Fast and reliable

Example from `tests/unit/test_providers.py`:

```python
def test_generate_with_mock(self, provider):
    # Mock the API call
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="COMMAND: ls")]

    with patch.object(provider.client.messages, 'create', ...):
        response = await provider.generate("test")
```

### System Tests (Require API Keys)

System tests call real APIs and need keys:

```bash
# Set your keys first
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."

# Run system tests
make test-system
```

**Optional testing:**
- Only run if you have keys
- Skip in CI if secrets not available
- Mark with `@pytest.mark.system`

## 🔒 CI/CD Security

### GitHub Actions Setup

#### 1. Repository Secrets (Recommended)

Go to: Settings → Secrets and variables → Actions

Add as repository secrets:
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`

#### 2. Organization Variables (For teams)

Share across multiple repositories:
- Settings → Secrets and variables → Actions → Variables

#### 3. GitHub Actions Workflow

The `.github/workflows/test.yml` is configured to:
- ✅ Run unit tests without secrets
- ✅ Run system tests only if secrets are available
- ✅ Never log secrets in output

```yaml
system-tests:
  if: "${{ vars.ANTHROPIC_API_KEY != '' }}"
  env:
    ANTHROPIC_API_KEY: ${{ vars.ANTHROPIC_API_KEY }}
```

## 📋 Best Practices

### For Contributors

1. **Never share API keys** in issues, PRs, or discussions
2. **Use mocked tests** for unit tests
3. **Document required keys** in `.env.example`
4. **Test locally** before pushing

### For Maintainers

1. **Use repository secrets** in CI/CD
2. **Rotate keys regularly** (every 90 days)
3. **Audit git history** for accidental commits
4. **Use branch protection** to require review

### For Users

1. **Create .env file** from `.env.example`
2. **Set proper file permissions**: `chmod 600 .env`
3. **Never share .env file**
4. **Use environment variables** in production

## 🔍 Detecting Leaked Keys

### Scan Git History

```bash
# Search for potential API keys in history
git log --all --full-history --source -- "*apiKey*" "*API_KEY*" "*sk-*"
git log -p -S "sk-ant-" --all
git log -p -S "sk-" --all
```

### Use Tools

```bash
# Install truffleHog
pip install truffleHog

# Scan repository
trufflehog --regex --entropy=False /path/to/repo
```

## 🚨 If Keys Are Leaked

### Immediate Actions

1. **Revoke the leaked key** immediately
   - Anthropic: https://console.anthropic.com/
   - OpenAI: https://platform.openai.com/

2. **Rotate to new key**

3. **Remove from git history**
   ```bash
   # Warning: This rewrites history
   git filter-branch --tree-filter 'grep -r "sk-" . && exit 1 || true' HEAD
   ```

4. **Force push** (if on private branch)
   ```bash
   git push origin --force
   ```

5. **Notify users** if public repository

## 📝 Testing Checklist

Before committing, verify:

- [ ] No API keys in code
- [ ] `.env` in `.gitignore`
- [ ] `.env.example` exists (with placeholders)
- [ ] Unit tests use mocks
- [ ] CI/CD uses secrets
- [ ] Documentation updated

## 🔐 File Permissions

Protect your `.env` file:

```bash
# Make it readable only by you
chmod 600 .env

# Verify
ls -la .env
# Should show: -rw------- (600)
```

## 📚 Additional Resources

- [GitHub Docs: Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [OWASP: Key Management](https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html)
- [GitGuardian: Detect Secrets](https://www.gitguardian.com/)

---

Remember: **If in doubt, don't commit it!**
