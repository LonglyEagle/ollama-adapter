# 更新日志

本文档记录了Ollama Adapter项目的所有重要变更。

## 0.1.6 (2024/12/27 13:00:00)

### 重大优化
* 🔧 **优化模型配置管理** - 将支持的模型及相关参数配置化
* 📁 创建独立的模型配置文件 `models_config.json`
* 🏗️ 新增模型管理器类 `ModelManager`，支持动态模型管理
* 🔄 重构模型信息获取逻辑，从硬编码改为配置文件驱动
* 📊 更新模型列表，专注支持通义千问、DeepSeek、硅基流动、火山引擎等提供商
* 🎯 新增文本嵌入模型支持

### 技术改进
* 📝 配置文件驱动的模型管理，提高可维护性
* 🧹 清理硬编码的模型信息，提升代码质量
* 🔧 统一模型参数配置格式
* ✅ 保持API兼容性，所有现有功能正常工作

## 0.1.5 (2024/12/27 12:30:00)

### 修复问题
* 🔧 **修复LlamaIndex集成流式响应格式** - 将自定义GenerateStreamResponse格式改为Ollama兼容的JSON格式
* 📡 流式响应现在包含LlamaIndex期望的message.content字段结构
* ✅ 修复测试函数返回值逻辑，确保测试结果正确显示
* 🧪 添加异常处理机制，提高测试稳定性

### 测试改进
* ✅ LlamaIndex集成测试现在完全通过（2/2测试用例）
* 🎯 支持文本生成、流式生成和聊天功能的完整测试
* 📊 流式响应正确处理.delta属性，符合LlamaIndex期望

## 0.1.4 (2024/12/22 12:00:00)

### 新增功能
* ✨ **重新实现/api/tags接口** - 列出所有本地模型，完全兼容Ollama格式
* 🏷️ 支持模型标签（自动添加:latest后缀）
* 📊 智能识别模型系列（qwen2、llama、claude、gpt、gemini等）
* 🎯 返回所有19个可用模型作为本地模型

### 优化改进
* 🔧 **修复/api/ps接口模型数量问题** - 现在返回所有19个模型（之前只返回3个）
* 📈 /api/ps和get_available_models()方法现在完全一致
* 🧪 新增专门的/api/tags测试脚本
* ✅ 更新完整测试套件，现在包含8个测试用例

### 接口说明
* `/api/tags` - 查询本地模型列表（包含修改时间、大小、摘要等）
* `/api/ps` - 查询运行中模型列表（包含过期时间、VRAM使用量等）

## 0.1.3 (2024/12/22 11:25:00)

### 新增功能
* ✨ **实现Ollama /api/ps接口** - 列出当前运行中的模型
* 📊 完全兼容Ollama官方API格式，包含模型大小、摘要、详细信息、过期时间和VRAM使用量
* 🎯 模拟前3个可用模型为运行状态，支持多种LLM提供商

### 重大变更
* 🗑️ **移除/api/tags接口** - 请使用/api/ps接口查看运行中的模型
* 🔄 更新响应格式以匹配Ollama官方示例（gguf格式、llama系列、Q4_0量化等）
* 📝 优化时间格式，包含时区信息

### 测试改进
* 🧪 新增专门的/api/ps接口测试脚本
* ✅ 更新完整测试套件，移除已废弃接口的测试
* 🎯 所有7个测试用例通过验证

## 0.1.2 (2024/12/19 18:30:00)

### 重大修复
* 🔧 **修复Ollama API兼容性问题**
* ✨ 完善模型定义，添加缺失的字段（think、done_reason等）
* 🔄 修复Chat接口（/api/chat）使用正确的ChatRequest/ChatResponse模型
* 📊 新增符合Ollama规范的嵌入接口（/api/embed）
* 🛠️ 完善LLMAdapter服务层，添加generate、generate_stream和create_embeddings方法
* 🧪 更新测试用例，覆盖所有新旧接口

### 技术改进
* 📝 统一API响应格式，完全兼容Ollama客户端
* 🔧 修复导入错误和模块依赖问题
* ✅ 所有7个测试用例通过验证
* 🎯 提升API稳定性和可靠性

## 0.1.1 (2024/12/19 16:00:00)

### 重大变更
* 🔥 **移除预定义模型映射限制**
* ✨ 直接支持所有LiteLLM兼容的模型名称
* 🚀 无需配置即可使用任何LiteLLM支持的模型
* 🗑️ 移除 `enable_model_mapping` 配置项
* 🗑️ 移除 `model_mapping` 和 `embedding_mapping` 配置
* 🎯 简化配置文件和代码结构

### 技术改进
* 📝 简化模型验证逻辑
* 🧹 清理不必要的导入和配置
* 🔧 优化代码可维护性

## 0.1.0 (2024/12/19 15:30:00)

### 新增功能
* 🎉 初始版本发布
* ✨ 实现Ollama兼容的REST API接口
* 🔄 支持文本生成接口 (`/api/generate`)
* 📊 支持嵌入向量接口 (`/api/embeddings`)
* 🌊 支持流式输出 (Server-Sent Events)
* 🤖 集成多个LLM提供商：
  - 阿里百炼 (Alibaba Qwen)
  - Deepseek
  - 硅基流动 (SiliconFlow)
  - 火山引擎 (Volcengine)
* 📝 实现模型列表接口 (`/api/tags`)
* 🛡️ 统一异常处理和错误响应
* 🐳 提供Docker和Docker Compose部署支持
* 📚 完整的项目文档和使用说明

### 技术实现
* 🏗️ 基于FastAPI框架构建
* 🔧 使用LiteLLM SDK统一调用各提供商API
* ⚙️ 支持环境变量配置
* 📋 完整的数据模型定义
* 🔍 详细的日志记录
* 🏥 健康检查接口

### 支持的模型
* **文本生成模型**:
  - qwen2:7b, qwen2:14b, qwen2:72b (阿里百炼)
  - deepseek-chat, deepseek-coder (Deepseek)
  - yi-34b-chat, llama3-8b (硅基流动)
  - doubao-lite, doubao-pro (火山引擎)
* **嵌入模型**:
  - text-embedding-v1, text-embedding-v2 (阿里百炼)

### 部署方式
* 🐍 本地Python环境运行
* 🐳 Docker容器部署
* 🚀 Docker Compose一键部署
* 🌐 可选Nginx反向代理