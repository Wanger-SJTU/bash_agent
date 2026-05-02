# Bashagnet

AI-enhanced bash shell agent with multi-model support.

## ⚡ Quick Start

```bash
# Clone and install
git clone git@github.com:Wanger-SJTU/bash_agent.git
cd bashagnet
uv sync

# Set up (choose one)
cp .env.example .env && source .env  # or use ~/.config/bashagnet/

# Use
bashagnet "list all python files"
```

**📚 [Full Documentation →](docs/README.md)**

## ✨ Features

- 🤖 **Multiple AI Providers**: Claude (Anthropic) and OpenAI
- 💬 **Interactive Mode**: Chat with your shell
- 🚀 **Direct Execution**: Generate and execute commands in one step
- 🛡️ **Safety Checks**: Built-in protection for dangerous commands
- ⚙️ **Configurable**: YAML-based configuration with environment variables
- 🔒 **Secure**: Git hooks and protections against API key leaks

## 🚀 Usage

### Direct command mode
```bash
bashagnet "list all python files"
bashagnet --provider openai "find files larger than 100MB"
bashagnet -x "show system disk usage"  # Execute the command
```

### Interactive mode
```bash
bashagnet -i  # Start interactive shell
```

### With custom model
```bash
bashagnet --model claude-3-5-sonnet-20241022 "analyze this directory"
bashagnet --provider openai --model gpt-4o "optimize this command"
```

## ⚙️ Configuration

### Quick setup (.env file)
```bash
cp .env.example .env
# Edit .env with your API keys
source .env
```

### User config file (recommended)
```bash
mkdir -p ~/.config/bashagnet
cat > ~/.config/bashagnet/config.yaml << 'EOF'
ai:
  provider: claude
  api_key: ${ANTHROPIC_API_KEY}  # or sk-ant-xxx
EOF
```

**📖 [Configuration Guide →](docs/CONFIG_FILES.md)**

## 🔒 Security

**⚠️ Important**: Read [USER_SECURITY.md](USER_SECURITY.md) before using!

Bashagnet includes protections:
- ✅ Pre-commit git hooks to prevent API key leaks
- ✅ `.gitignore` rules for sensitive files
- ✅ Safety checks for dangerous commands
- ✅ Mocked unit tests (no API keys needed)

**📚 [Security Guide →](USER_SECURITY.md)**

## 🧪 Testing

```bash
# Unit tests (no API keys needed)
make test-unit

# System tests (require API keys)
make test-system

# All tests
make test
```

**📖 [Testing Guide →](TESTING.md)**

## 🤖 AI Providers

### Claude (Anthropic)
- Models: `claude-3-5-sonnet-20241022`, `claude-3-haiku-20240307`
- API Key: https://console.anthropic.com/
- Set: `export ANTHROPIC_API_KEY=sk-ant-...`

### OpenAI
- Models: `gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo`
- API Key: https://platform.openai.com/
- Set: `export OPENAI_API_KEY=sk-...`

### Local Models (Ollama, etc.)
```yaml
ai:
  provider: openai
  base_url: http://localhost:11434/v1
  model: llama2
  api_key: dummy-key
```

## 📚 Documentation

### User Guides
- [Quick Start](docs/user-guide/quickstart.md) - 5分钟上手
- [Quick Reference](docs/user-guide/quickref.md) - 常用命令速查
- [Configuration](docs/CONFIG_FILES.md) - 配置文件详解
- [User Setup](docs/USER_SETUP.md) - 安装配置教程

### Security & Testing
- [User Security](USER_SECURITY.md) - **必读** 保护 API keys
- [Developer Security](SECURITY.md) - 安全开发实践
- [Testing Guide](TESTING.md) - 测试指南

### Project Docs
- [Documentation Index](docs/README.md) - 完整文档导航
- [Implementation Plan](docs/planning/implementation-plan.md) - 开发路线图
- [Project Summary](docs/planning/project-summary.md) - 项目总结

## 🛠️ Development

```bash
# Install dependencies
uv sync

# Install git hooks (prevents API key leaks)
./scripts/install-hooks.sh

# Run tests
make test-unit    # Unit tests (no API keys)
make test-system  # System tests (require API keys)

# Code quality
make format       # Format code
make lint         # Run linter
```

## 📊 Project Status

**Current Version**: v0.1.0

**Implemented Features**:
- ✅ Claude and OpenAI providers
- ✅ Interactive and direct command modes
- ✅ Safety checks and validations
- ✅ Configurable system prompts
- ✅ Comprehensive test suite (26 unit tests)
- ✅ Security protections (git hooks, .gitignore)

**Roadmap**:
- [ ] Local model support (Ollama)
- [ ] Shell completion
- [ ] Pipe integration
- [ ] Web interface
- [ ] Multi-step command planning

## 🤝 Contributing

Contributions welcome! Please read:
1. [Testing Guide](TESTING.md) - How to write tests
2. [Security Guide](SECURITY.md) - Security practices
3. [Implementation Plan](docs/planning/implementation-plan.md) - Roadmap

## 📝 License

[Specify your license here]

## 🔗 Links

- **GitHub**: https://github.com/Wanger-SJTU/bash_agent
- **Issues**: https://github.com/Wanger-SJTU/bash_agent/issues
- **Documentation**: [docs/README.md](docs/README.md)

---

**Made with ❤️ by the bashagnet team**
