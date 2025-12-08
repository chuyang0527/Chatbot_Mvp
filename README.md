# 聊天机器人 RAG 系统

基于 LangGraph、LangChain 和向量检索的智能问答系统，支持多种文档格式上传和多轮对话。

## 功能特性

- 📄 **文档处理**: 支持 PDF、Word、Markdown、TXT 格式
- 🔍 **向量检索**: 基于语义相似度的智能检索
- 💬 **多轮对话**: 上下文管理和历史追踪
- 🔗 **可观测性**: LangSmith 调用链追踪
- 🤖 **本地模型**: 使用 Ollama DeepSeek 7B

## 技术栈

- **LangChain**: LLM 应用框架
- **LangGraph**: 状态图工作流
- **LangSmith**: 调用链追踪
- **Chroma**: 向量数据库
- **Ollama**: 本地 LLM 服务

## 环境依赖

- Python 3.10+
- uv (Python 包管理器)
- Ollama (运行 DeepSeek 7B)

## 安装步骤

### 1. 安装 uv

```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 克隆项目

```bash
git clone <your-repo-url>
cd chatbot-rag
```

### 3. 安装依赖

```bash
uv sync
```

### 4. 配置环境变量

创建 `.env` 文件（可选，用于 LangSmith）:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=chatbot-rag
OLLAMA_BASE_URL=http://localhost:11434
```

### 5. 确保 Ollama 运行

```bash
# 确认 DeepSeek 模型已下载
ollama list

# 如果没有，拉取模型
ollama pull deepseek-r1:7b

# 启动 Ollama 服务（通常自动运行）
ollama serve
```

## 使用方法

### 启动聊天机器人

```bash
uv run python src/main.py
```

### 示例命令

```python
# 上传文档
> upload document.pdf

# 提问
> 这个文档主要讲了什么？

# 多轮对话
> 能详细说说第二部分吗？

# 退出
> exit
```

## 项目结构

```
chatbot-rag/
├── src/
│   ├── __init__.py           # 包初始化
│   ├── main.py               # 主程序入口
│   ├── document_processor.py # 文档处理模块
│   ├── vector_store.py       # 向量存储模块
│   ├── chat_agent.py         # 对话代理模块
│   └── config.py             # 配置管理
├── data/
│   └── uploads/              # 文档上传目录
├── .gitignore
├── README.md
└── pyproject.toml            # 项目依赖配置
```

## 开发指南

### 添加新的文档类型支持

在 `document_processor.py` 中扩展 `DocumentProcessor` 类。

### 自定义向量存储

修改 `vector_store.py` 中的 `VectorStore` 类配置。

### 调整 LLM 参数

在 `config.py` 中修改模型配置。

## 调用链追踪

项目集成了 LangSmith 进行调用链追踪。配置 API Key 后，可在 LangSmith 平台查看：

- 每次查询的完整流程
- 检索到的文档片段
- LLM 生成过程
- 性能指标

访问: https://smith.langchain.com/

## 常见问题

**Q: Ollama 连接失败？**
A: 确认 Ollama 服务运行中，检查端口 11434 是否可访问。

**Q: 文档上传失败？**
A: 检查文件格式是否支持，确保 data/uploads 目录存在。

**Q: 向量检索结果不准确？**
A: 尝试调整 chunk_size 和 chunk_overlap 参数。

## License

MIT
