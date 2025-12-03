# 快速开始指南

## 5 分钟快速体验

### 前置要求

- Python 3.10 或更高版本
- OpenAI API Key
- LangSmith API Key（可选，用于可观测性）

### 步骤 1: 安装 uv

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 步骤 2: 克隆并设置项目

```bash
# 克隆项目
git clone <your-repo-url>
cd chatbot-mvp

# 创建虚拟环境并安装依赖
uv venv
uv pip install -r requirements.txt
```

### 步骤 3: 配置环境变量

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，至少需要配置：

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

可选配置（启用 LangSmith 追踪）：

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-api-key-here
LANGCHAIN_PROJECT=chatbot-mvp
```

### 步骤 4: 运行演示

```bash
uv run python examples/demo.py
```

这将：
1. 创建一个示例文档
2. 处理并向量化文档
3. 运行几个测试问题
4. 展示完整的问答流程

### 步骤 5: 上传自己的文档

```bash
# 上传 PDF
uv run python src/upload_document.py --file path/to/your/document.pdf

# 上传 Word 文档
uv run python src/upload_document.py --file path/to/your/document.docx

# 上传 Markdown
uv run python src/upload_document.py --file path/to/your/document.md

# 上传文本文件
uv run python src/upload_document.py --file path/to/your/document.txt
```

### 步骤 6: 启动交互式聊天

```bash
uv run python src/main.py
```

现在你可以开始提问了！

## 使用示例

### 交互式命令

在聊天界面中：

- 输入问题进行提问
- 输入 `exit` 或 `quit` 退出
- 输入 `clear` 清除对话历史
- 输入 `history` 查看对话历史

### 示例对话

```
👤 你的问题： 什么是人工智能？

🤖 助手回答：
根据文档内容，人工智能（Artificial Intelligence，简称AI）是计算机科学的一个分支，
致力于创建能够执行通常需要人类智能的任务的系统。[文档片段 1]

📚 引用来源：
  [1] data/documents/sample.txt (页码: N/A)
      # 人工智能简介 人工智能（Artificial Intelligence，简称AI）是计算机科学的一个分支...
```

## 查看调用链追踪

如果配置了 LangSmith：

1. 访问 [https://smith.langchain.com/](https://smith.langchain.com/)
2. 登录你的账号
3. 选择项目 `chatbot-mvp`
4. 查看 "Traces" 标签页
5. 点击任意一条记录查看详细的调用链

你将看到：
- 完整的执行流程
- 每个步骤的输入输出
- 执行时间和 Token 使用
- 错误信息（如果有）

## 常见问题

### Q: 提示 "OpenAI API key not found"

A: 确保在 `.env` 文件中正确配置了 `OPENAI_API_KEY`。

### Q: 文档上传后找不到

A: 检查 `data/vector_db/` 目录是否存在，确保有写入权限。

### Q: 回答质量不好

A: 尝试：
1. 调整 `CHUNK_SIZE` 和 `CHUNK_OVERLAP` 参数
2. 增加 `TOP_K` 值以检索更多文档
3. 使用更强大的模型（如 gpt-4）

### Q: 速度太慢

A: 考虑：
1. 使用更快的模型（如 gpt-3.5-turbo）
2. 减少 `TOP_K` 值
3. 使用云端向量数据库

## 下一步

- 📖 阅读完整的 [README.md](README.md)
- 🔧 查看 [DEPLOYMENT.md](DEPLOYMENT.md) 了解部署选项
- 📊 查看 [LANGSMITH_GUIDE.md](LANGSMITH_GUIDE.md) 学习可观测性
- 🤝 阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 参与贡献

## 获取帮助

遇到问题？

1. 查看 [Issues](https://github.com/your-repo/issues)
2. 创建新的 Issue
3. 查看文档和示例代码

祝使用愉快！🎉
