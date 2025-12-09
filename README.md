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

## 快速开始

### 方式一：Docker 部署（推荐）

**一键启动所有服务：**

```bash
# Linux/macOS
chmod +x scripts/setup.sh
./scripts/setup.sh

# Windows PowerShell
.\scripts\setup.ps1
```

**或使用 Docker Compose：**

```bash
# 启动服务
docker-compose up -d

# 下载 DeepSeek 模型
docker exec -it chatbot-ollama ollama pull deepseek-r1:7b

# 启动聊天机器人
docker exec -it chatbot-app python src/main.py

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 方式二：本地开发

#### 1. 安装 uv

```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 2. 克隆项目

```bash
git clone <your-repo-url>
cd chatbot-rag
```

#### 3. 安装依赖

```bash
# 使用 Makefile（推荐）
make install

# 或直接使用 uv
uv sync
```

#### 4. 下载模型

```bash
# 自动下载 Embedding 模型
python scripts/download_model.py

# 或使用 Makefile
make download-models
```

#### 5. 配置环境变量

创建 `.env` 文件（可选，用于 LangSmith）:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=chatbot-rag
OLLAMA_BASE_URL=http://localhost:11434
```

#### 6. 确保 Ollama 运行

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
# 本地运行
uv run python src/main.py

# 或使用 Makefile
make dev

# Docker 运行
docker exec -it chatbot-app python src/main.py
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

### Makefile 快捷命令

```bash
make help           # 查看所有命令
make install        # 安装依赖
make dev            # 启动开发环境
make test           # 运行测试
make lint           # 代码检查
make format         # 代码格式化
make docker-up      # 启动 Docker 服务
make docker-down    # 停止 Docker 服务
make docker-logs    # 查看日志
```

## 项目结构

```
chatbot-rag/
├── src/                      # 源代码
│   ├── __init__.py           # 包初始化
│   ├── main.py               # 主程序入口
│   ├── document_processor.py # 文档处理模块
│   ├── vector_store.py       # 向量存储模块
│   ├── chat_agent.py         # 对话代理模块
│   └── config.py             # 配置管理
├── scripts/                  # 自动化脚本
│   ├── setup.sh              # Linux/macOS 部署脚本
│   ├── setup.ps1             # Windows 部署脚本
│   └── download_model.py     # 模型下载脚本
├── .github/                  # GitHub 配置
│   ├── workflows/            # CI/CD 流水线
│   │   ├── ci.yml            # 持续集成
│   │   └── docker-publish.yml # Docker 发布
│   ├── ISSUE_TEMPLATE/       # Issue 模板
│   └── pull_request_template.md # PR 模板
├── data/
│   └── uploads/              # 文档上传目录
├── chroma_db/                # 向量数据库
├── model/                    # 本地模型
├── Dockerfile                # Docker 镜像构建
├── docker-compose.yml        # 多服务编排
├── Makefile                  # 快捷命令
├── CONTRIBUTING.md           # 贡献指南
├── CHANGELOG.md              # 变更日志
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

## 工程化特性

### 容器化部署
- ✅ Dockerfile 多阶段构建
- ✅ Docker Compose 多服务编排
- ✅ 自动化健康检查
- ✅ 数据持久化

### 自动化脚本
- ✅ 一键部署脚本（Linux/macOS/Windows）
- ✅ 模型自动下载
- ✅ 环境初始化
- ✅ Makefile 快捷命令

### CI/CD
- ✅ GitHub Actions 自动化测试
- ✅ 代码质量检查（Ruff + Black）
- ✅ Docker 镜像自动构建
- ✅ 安全扫描（Trivy）

### 版本控制
- ✅ Git 工作流规范
- ✅ Conventional Commits
- ✅ Pull Request 模板
- ✅ Issue 模板

## 开发指南

### 贡献代码

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细的开发规范。

**分支命名规范：**
- `feat/功能名称` - 新功能
- `fix/问题描述` - Bug 修复
- `docs/文档说明` - 文档更新

**提交信息规范：**
```bash
feat(upload): 添加批量文档上传功能
fix(vector): 修复相似度搜索空指针异常
docs(readme): 更新安装步骤说明
```

### 代码质量

```bash
# 代码格式化
make format

# 代码检查
make lint

# 运行测试
make test
```

## 常见问题

**Q: Ollama 连接失败？**
A: 确认 Ollama 服务运行中，检查端口 11434 是否可访问。

**Q: 文档上传失败？**
A: 检查文件格式是否支持，确保 data/uploads 目录存在。

**Q: 向量检索结果不准确？**
A: 尝试调整 chunk_size 和 chunk_overlap 参数。

**Q: Docker 容器启动失败？**
A: 检查 Docker 服务是否运行，端口是否被占用。

**Q: 模型下载慢？**
A: 可以手动下载模型文件，放到 model/ 目录。

## 路线图

- [ ] Web API 接口
- [ ] 前端界面
- [ ] 更多文档格式支持
- [ ] 多语言支持
- [ ] 性能优化

## 贡献者

感谢所有贡献者！查看 [贡献指南](CONTRIBUTING.md) 了解如何参与。

## License

MIT
