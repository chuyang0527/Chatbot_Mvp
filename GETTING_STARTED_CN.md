# 开始使用 - 中文指南

## 欢迎！👋

这是一个智能文档问答聊天机器人，可以帮你快速从文档中获取信息。

## 第一步：准备工作

### 1. 获取 API Keys

#### OpenAI API Key（必需）

1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 注册/登录账号
3. 进入 [API Keys](https://platform.openai.com/api-keys) 页面
4. 点击 "Create new secret key"
5. 复制生成的 API Key（格式：sk-...）

#### LangSmith API Key（可选，用于调用链追踪）

1. 访问 [LangSmith](https://smith.langchain.com/)
2. 注册/登录账号
3. 点击右上角头像 → Settings → API Keys
4. 点击 "Create API Key"
5. 复制生成的 API Key

### 2. 安装 Python

确保你的电脑上安装了 Python 3.10 或更高版本。

检查 Python 版本：
```bash
python --version
```

如果没有安装，请访问 [Python 官网](https://www.python.org/downloads/) 下载安装。

## 第二步：安装项目

### Windows 用户

1. 打开命令提示符（CMD）或 PowerShell
2. 进入项目目录
3. 运行安装脚本：

```cmd
scripts\setup.bat
```

### Mac/Linux 用户

1. 打开终端
2. 进入项目目录
3. 运行安装脚本：

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 手动安装（如果脚本失败）

```bash
# 1. 安装 uv
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Mac/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 创建虚拟环境
uv venv

# 3. 安装依赖
uv pip install -r requirements.txt
```

## 第三步：配置 API Keys

1. 在项目根目录找到 `.env.example` 文件
2. 复制并重命名为 `.env`
3. 用文本编辑器打开 `.env` 文件
4. 填入你的 API Keys：

```env
# 必需：OpenAI API Key
OPENAI_API_KEY=sk-your-openai-api-key-here

# 可选：LangSmith（用于调用链追踪）
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-api-key-here
LANGCHAIN_PROJECT=chatbot-mvp
```

**重要提示**：
- 不要分享你的 API Keys
- 不要将 `.env` 文件提交到 Git

## 第四步：运行示例

运行内置示例，测试是否配置成功：

```bash
uv run python examples/demo.py
```

你应该看到：
1. ✅ 创建示例文档
2. ✅ 加载和处理文档
3. ✅ 分割文档
4. ✅ 向量化存储
5. ✅ 初始化聊天机器人
6. ✅ 测试问答功能

## 第五步：上传你的文档

### 支持的文档格式

- 📄 PDF (.pdf)
- 📝 Word (.docx)
- 📋 Markdown (.md)
- 📃 文本文件 (.txt)

### 上传命令

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

### 示例

假设你有一个文件 `C:\Documents\report.pdf`：

```bash
uv run python src/upload_document.py --file "C:\Documents\report.pdf"
```

上传成功后，你会看到：
- ✅ 文档加载完成
- ✅ 文档分割完成
- ✅ 文档已添加到向量数据库

## 第六步：开始聊天

启动交互式聊天界面：

```bash
uv run python src/main.py
```

### 使用方法

1. **提问**：直接输入你的问题，按回车
2. **查看历史**：输入 `history`
3. **清除历史**：输入 `clear`
4. **退出**：输入 `exit` 或 `quit`

### 示例对话

```
👤 你的问题： 这份文档主要讲了什么？

🤖 助手回答：
根据文档内容，这份文档主要介绍了人工智能的基本概念、
应用领域和发展历史。[文档片段 1]

📚 引用来源：
  [1] data/documents/sample.txt (页码: N/A)
      # 人工智能简介 人工智能（Artificial Intelligence...
```

## 常见问题

### Q1: 提示 "OpenAI API key not found"

**解决方法**：
1. 确认 `.env` 文件存在
2. 确认 `OPENAI_API_KEY` 已正确填写
3. 确认 API Key 格式正确（以 sk- 开头）

### Q2: 上传文档失败

**可能原因**：
1. 文件路径不正确
2. 文件格式不支持
3. 文件损坏或加密

**解决方法**：
1. 使用绝对路径
2. 确认文件格式在支持列表中
3. 尝试其他文档

### Q3: 回答质量不好

**优化方法**：
1. 上传更多相关文档
2. 调整配置参数（见下文）
3. 使用更强大的模型（如 gpt-4）

### Q4: 速度太慢

**优化方法**：
1. 使用更快的模型（gpt-3.5-turbo）
2. 减少检索的文档数量
3. 优化文档分段大小

## 高级配置

编辑 `.env` 文件，调整参数：

```env
# 使用的模型（gpt-4 更强但更慢更贵）
OPENAI_MODEL=gpt-4o-mini

# 文档分段大小（越大上下文越多，但可能不够精确）
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# 检索文档数量（越多信息越全，但可能有噪音）
TOP_K=4

# 相似度阈值（0-1，越高越严格）
SIMILARITY_THRESHOLD=0.7
```

## 查看调用链追踪（LangSmith）

如果配置了 LangSmith：

1. 访问 [https://smith.langchain.com/](https://smith.langchain.com/)
2. 登录你的账号
3. 选择项目 "chatbot-mvp"
4. 查看 "Traces" 标签页

你可以看到：
- 完整的执行流程
- 每个步骤的输入输出
- 执行时间和 Token 使用
- 错误信息（如果有）

## 使用技巧

### 1. 提问技巧

**好的问题**：
- "文档中提到了哪些主要观点？"
- "关于 X 的定义是什么？"
- "文档中有哪些数据支持 Y？"

**不好的问题**：
- "你好"（太简单）
- "告诉我一切"（太宽泛）
- 文档中没有的内容

### 2. 多轮对话

机器人会记住对话历史，你可以：
- 追问细节："能详细说说吗？"
- 补充问题："那 X 呢？"
- 澄清疑问："你是说 Y 吗？"

### 3. 文档管理

- 定期清理不需要的文档
- 相关文档放在一起上传
- 给文档起有意义的名字

## 成本估算

使用 OpenAI API 是按使用量付费的：

- **gpt-3.5-turbo**: 约 $0.002 / 1000 tokens
- **gpt-4**: 约 $0.03 / 1000 tokens

每次问答大约消耗 1000-2000 tokens，成本约：
- gpt-3.5-turbo: $0.002-$0.004 / 次
- gpt-4: $0.03-$0.06 / 次

**省钱技巧**：
1. 使用 gpt-3.5-turbo（便宜 15 倍）
2. 减少 TOP_K 值（检索更少文档）
3. 精简问题（减少 token 使用）

## 数据安全

- ✅ 所有文档存储在本地
- ✅ API Keys 不会被分享
- ⚠️ 问题和回答会发送到 OpenAI
- ⚠️ 如果启用 LangSmith，调用数据会上传

**隐私建议**：
- 不要上传包含敏感信息的文档
- 不要在问题中包含个人信息
- 定期清理向量数据库

## 获取帮助

### 文档资源

- [README.md](README.md) - 完整项目说明
- [QUICKSTART.md](QUICKSTART.md) - 快速开始
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构
- [DEPLOYMENT.md](DEPLOYMENT.md) - 部署指南

### 遇到问题？

1. 查看错误信息
2. 检查配置是否正确
3. 查看文档和示例
4. 提交 Issue

## 下一步

现在你已经掌握了基本使用方法，可以：

1. 📚 上传更多文档
2. 💬 尝试不同类型的问题
3. ⚙️ 调整配置优化效果
4. 📊 查看 LangSmith 追踪
5. 🚀 部署到生产环境

祝使用愉快！🎉

---

**需要帮助？** 查看其他文档或提交 Issue。
