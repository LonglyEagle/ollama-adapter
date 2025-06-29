# Ollama Adapter

一个将其他LLM提供商接口转换为Ollama兼容格式的适配器服务，使用LiteLLM SDK统一调用多个模型提供商。

## 功能特性

- 🔄 **接口转换**: 将多个LLM提供商的接口转换为Ollama REST API格式
- 🌊 **流式输出**: 支持Server-Sent Events (SSE)格式的流式响应
- 🤖 **多提供商支持**: 集成阿里百炼、Deepseek、硅基流动、火山引擎等
- 📊 **嵌入向量**: 支持文本嵌入向量生成
- 🐳 **容器化部署**: 提供Docker和Docker Compose部署方式
- 🛡️ **错误处理**: 统一异常捕获和Ollama风格错误响应
- 📝 **完整日志**: 详细的请求和错误日志记录

## 支持的模型提供商

### 文本生成模型
- **阿里百炼**: qwen2:7b, qwen2:14b, qwen2:72b
- **Deepseek**: deepseek-chat, deepseek-coder
- **硅基流动**: yi-34b-chat, llama3-8b
- **火山引擎**: doubao-lite, doubao-pro

### 嵌入模型
- **阿里百炼**: text-embedding-v1, text-embedding-v2

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd ollama-adapter

# 复制环境变量配置
cp .env.example .env

# 编辑.env文件，填入你的API密钥
vim .env
```

### 2. 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python -m app.main

# 或使用uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 11434 --reload
```

### 3. Docker部署

```bash
# 构建镜像
docker build -t ollama-adapter .

# 运行容器
docker run -d \
  --name ollama-adapter \
  -p 11434:11434 \
  --env-file .env \
  ollama-adapter
```

### 4. Docker Compose部署

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## API使用示例

### 文本生成（非流式）

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-3.5-turbo",
    "prompt": "你好，请介绍一下自己",
    "stream": false
  }'
```

### 文本生成（流式）

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "datascope/qwen-turbo",
    "prompt": "写一首关于春天的诗",
    "stream": true
  }'
```

### 嵌入向量生成

```bash
curl -X POST http://localhost:11434/api/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/text-embedding-ada-002",
    "prompt": "这是一段需要生成嵌入向量的文本"
  }'
```

### 获取模型列表

```bash
curl http://localhost:11434/api/tags
```

## 配置说明

### 环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `DATASCOPE_API_KEY` | 阿里百炼API密钥 | - |
| `DEEPSEEK_API_KEY` | Deepseek API密钥 | - |
| `SILICONFLOW_API_KEY` | 硅基流动API密钥 | - |
| `VOLCENGINE_API_KEY` | 火山引擎API密钥 | - |
| `HOST` | 服务监听地址 | `0.0.0.0` |
| `PORT` | 服务监听端口 | `11434` |
| `DEFAULT_MODEL` | 默认模型 | `gpt-3.5-turbo` |

### 模型使用

本适配器直接支持所有LiteLLM兼容的模型名称，无需预配置模型映射。你可以直接使用以下格式的模型名：

- OpenAI: `gpt-4`, `gpt-3.5-turbo`
- Anthropic: `claude-3-opus`, `claude-3-sonnet`
- 阿里百炼: `datascope/qwen-turbo`, `datascope/qwen-plus`
- Deepseek: `deepseek/deepseek-chat`, `deepseek/deepseek-coder`
- 硅基流动: `siliconflow/Yi-34B-Chat`
- 火山引擎: `volcengine/doubao-lite-4k`
- 其他LiteLLM支持的任何模型

## 项目结构

```
ollama-adapter/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI应用入口
│   ├── models/
│   │   ├── __init__.py
│   │   └── ollama_models.py # Ollama接口数据模型
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── generate.py      # 文本生成接口
│   │   ├── embeddings.py    # 嵌入向量接口
│   │   └── models.py        # 模型管理接口
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_adapter.py   # LiteLLM适配器服务
│   │   └── error_handler.py # 异常处理服务
│   └── config/
│       ├── __init__.py
│       └── settings.py      # 配置管理
├── tests/
│   └── simple_test.py       # 简单测试脚本
├── logs/                    # 日志文件目录
├── requirements.txt         # Python依赖
├── Dockerfile              # Docker镜像构建
├── docker-compose.yml      # Docker Compose配置
├── .env.example            # 环境变量模板
├── README.md               # 项目文档
└── 需求文档.md             # 需求说明
```

## 开发指南

### 添加新的模型提供商

1. 在 `app/config/settings.py` 中添加API密钥配置
2. 在 `model_mapping` 中添加模型映射
3. 在 `app/services/llm_adapter.py` 中配置API密钥
4. 测试新模型的调用

### 自定义错误处理

在 `app/services/error_handler.py` 中添加新的异常处理逻辑。

### 添加新的API端点

1. 在 `app/routers/` 中创建新的路由文件
2. 在 `app/main.py` 中注册新路由
3. 添加相应的数据模型到 `app/models/`

### 运行测试

```bash
# 运行简单测试脚本
python tests/simple_test.py

# 或者在Docker环境中运行
docker exec ollama-adapter python tests/simple_test.py
```

测试脚本会验证以下功能：
- 服务健康检查
- 模型列表获取
- 文本生成（流式和非流式）
- 嵌入向量生成

## 故障排除

### 常见问题

1. **API密钥错误**
   - 检查 `.env` 文件中的API密钥是否正确
   - 确认API密钥有足够的权限

2. **模型不存在**
   - 确认模型名称是否正确
   - 确认对应的提供商支持该模型

3. **网络连接问题**
   - 检查网络连接是否正常
   - 确认防火墙设置允许访问外部API

### 日志查看

```bash
# Docker部署
docker logs ollama-adapter

# Docker Compose部署
docker-compose logs -f ollama-adapter
```

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 支持

如果你遇到问题或有建议，请：

1. 查看 [Issues](../../issues) 中是否有类似问题
2. 创建新的 Issue 描述你的问题
3. 提供详细的错误信息和复现步骤