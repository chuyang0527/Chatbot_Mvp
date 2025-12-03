# 智能文档问答聊天机器人

基于 LangGraph、LangChain 和 LangSmith 的智能文档问答系统，支持多种文档格式上传、向量检索和多轮对话。

## 功能特性

- 📄 **多格式文档支持**: PDF、Word(.docx)、Markdown(.md)、TXT
- 🔍 **智能检索**: 基于向量相似度的文档片段检索
- 💬 **多轮对话**: 支持上下文跟踪和历史回顾
- 📊 **可观测性**: 集成 LangSmith 追踪调用链
- 🎯 **引用溯源**: 回答中显式引用原文段落

## 技术栈

- **框架**: LangGraph, LangChain
- **可观测性**: LangSmith
- **向量数据库**: Chroma (本地) / 可替换为云端服务
- **LLM**: OpenAI GPT (可配置其他模型)
- **依赖管理**: uv

## 环境要求

- Python 3.10+
- uv (Python 包管理器)

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
cd chatbot-mvp
```

### 3. 创建虚拟环境并安装依赖

```bash
uv venv
uv pip install -r requirements.txt
```

### 4. 配置环境变量

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入必要的 API 密钥：

```
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=chatbot-mvp
```

## 使用方法

### 启动聊天机器人

```bash
uv run python src/main.py
```

### 上传文档

```bash
uv run python src/upload_document.py --file path/to/your/document.pdf
```

### 运行示例

```bash
uv run python examples/demo.py
```

## 项目结构

```
chatbot-mvp/
├── src/
│   ├── __init__.py
│   ├── main.py                 # 主程序入口
│   ├── config.py               # 配置管理
│   ├── document_processor/     # 文档处理模块
│   │   ├── __init__.py
│   │   ├── loader.py          # 文档加载器
│   │   ├── splitter.py        # 文本分段器
│   │   └── vectorizer.py      # 向量化处理
│   ├── retrieval/              # 检索模块
│   │   ├── __init__.py
│   │   ├── vector_store.py    # 向量存储
│   │   └── retriever.py       # 检索器
│   ├── agent/                  # Agent 模块
│   │   ├── __init__.py
│   │   ├── graph.py           # LangGraph 状态图
│   │   ├── nodes.py           # 图节点定义
│   │   └── state.py           # 状态管理
│   └── utils/                  # 工具函数
│       ├── __init__.py
│       └── logger.py          # 日志工具
├── data/
│   ├── documents/              # 上传的文档
│   └── vector_db/              # 向量数据库存储
├── examples/
│   └── demo.py                 # 使用示例
├── tests/                      # 测试文件
│   └── __init__.py
├── .env.example                # 环境变量模板
├── .gitignore
├── requirements.txt            # 项目依赖
├── pyproject.toml             # uv 项目配置
└── README.md
```

## 核心功能说明

### 1. 文档处理流程

- 支持多种格式文档上传
- 自动文本抽取和清洗
- 智能分段（支持语义分段）
- 向量化存储

### 2. 检索与问答

- 基于向量相似度的语义检索
- 返回 Top-K 相关文档片段
- LLM 生成回答并引用原文
- 支持自定义检索参数

### 3. 多轮对话

- 会话状态管理
- 上下文信息追踪
- 历史对话回顾
- 支持补充提问和澄清

### 4. 可观测性

- LangSmith 集成，自动追踪所有调用
- 记录输入输出、延迟、token 使用
- 可视化调用链路
- 错误追踪和调试

## 示例命令

```bash
# 上传文档
uv run python src/upload_document.py --file data/documents/sample.pdf

# 启动交互式聊天
uv run python src/main.py

# 运行完整示例
uv run python examples/demo.py

# 查看帮助
uv run python src/main.py --help
```

## 开发指南

### 日志规范

**重要：禁止使用 `print()` 进行调试输出！**

所有调试信息必须使用标准日志模块：

```python
from src.utils.logger import logger

# ✅ 正确
logger.debug("调试信息")
logger.info("一般信息")
logger.warning("警告信息")
logger.error("错误信息", exc_info=True)

# ❌ 错误
print("调试信息")  # 禁止！
```

详见 [日志使用规范](LOGGING_GUIDE.md)

### 分支规范

- `main`: 主分支，稳定版本
- `develop`: 开发分支
- `feature/*`: 功能分支
- `bugfix/*`: 修复分支

### Commit 规范

- `feat`: 新功能
- `fix`: 修复问题
- `docs`: 文档更新
- `refactor`: 代码重构
- `test`: 测试相关

## 后续规划

- [ ] 支持更多文档格式
- [ ] 优化检索算法
- [ ] 添加 Web UI 界面
- [ ] 支持多用户会话管理
- [ ] 性能优化和缓存机制

## 许可证

MIT License

## 联系方式

如有问题，请提交 Issue 或 Pull Request。
