# 配置详解

## 配置方式

| 方式 | 适用场景 | 安全性 |
|------|----------|--------|
| 环境变量 | 最佳实践 | ⭐⭐⭐⭐⭐ |
| 用户配置 | 多个项目 | ⭐⭐⭐⭐ |
| .env 文件 | 项目本地 | ⭐⭐⭐⭐ |

## 配置位置

1. `~/.config/bashagnet/config.yaml`（推荐）
2. `./.env`（项目本地）
3. 环境变量（最安全）

## 配置示例

### Claude
```yaml
ai:
  provider: claude
  api_key: ${ANTHROPIC_API_KEY}
```

### OpenAI
```yaml
ai:
  provider: openai
  api_key: ${OPENAI_API_KEY}
```

### 本地模型
```yaml
ai:
  provider: openai
  base_url: http://localhost:11434/v1
  model: llama2
```

**⚠️ 重要：** 阅读 [SECURITY.md](../SECURITY.md)
