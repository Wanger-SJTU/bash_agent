# 快速开始

## 5 分钟上手

### 1. 安装
```bash
git clone git@github.com:Wanger-SJTU/bash_agent.git
cd bashagent
uv sync
```

### 2. 配置

**方式 A: 使用 .env（最简单）**
```bash
cp .env.example .env
# 编辑 .env 添加你的 API keys
source .env
```

**方式 B: 用户配置（全局）**
```bash
mkdir -p ~/.config/bashagnet
cat > ~/.config/bashagnet/config.yaml << 'EOF'
ai:
  provider: claude
  api_key: sk-ant-your-key
EOF
```

### 3. 使用
```bash
bashagnet "list all python files"
bashagnet -x "show disk usage"
bashagnet -i  # 交互模式
```

**⚠️ 重要：** 阅读 [SECURITY.md](../SECURITY.md) 保护 API keys
