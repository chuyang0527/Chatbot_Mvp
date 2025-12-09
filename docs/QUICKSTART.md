# 快速开始指南

5 分钟快速上手聊天机器人 RAG 系统。

## 🚀 最快方式：Docker 一键部署

### 前置要求

- ✅ 已安装 Docker Desktop
- ✅ 至少 8GB 可用内存
- ✅ 稳定的网络连接

### 步骤

#### 1. 克隆项目

```bash
git clone <your-repo-url>
cd chatbot-rag
```

#### 2. 一键启动

**Linux/macOS:**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

**Windows PowerShell:**
```powershell
.\scripts\setup.ps1
```

#### 3. 下载 AI 模型

```bash
# 等待 Ollama 服务启动（约 30 秒）
docker-compose ps

# 下载 DeepSeek 模型（约 4GB，需要几分钟）
docker exec -it chatbot-ollama ollama pull deepseek-r1:7b
```

#### 4. 开始聊天

```bash
docker exec -it chatbot-app python src/main.py
```

### 🎉 完成！

现在你可以：

```
你: upload example.pdf
✓ 文档已成功上传并向量化

你: 这个文档讲了什么？
机器人: 根据文档内容，这是关于...
```

---

## 💻 本地开发方式

适合需要修改代码的开发者。

### 前置要求

- Python 3.10+
- Ollama

### 步骤

#### 1. 安装 uv（Python 包管理器）

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 2. 安装依赖

```bash
git clone <your-repo-url>
cd chatbot-rag
make install
```

#### 3. 下载模型

```bash
# Embedding 模型
make download-models

# LLM 模型
ollama pull deepseek-r1:7b
```

#### 4. 启动应用

```bash
make dev
```

---

## 📝 基本使用

### 上传文档

支持格式：PDF、Word、Markdown、TXT

```bash
你: upload /path/to/document.pdf
✓ 文档已成功上传并向量化
```

### 提问

```bash
你: 文档的主要内容是什么？
机器人: 根据文档，主要内容包括...

你: 能详细说说第二部分吗？
机器人: 第二部分主要讨论了...
```

### 管理命令

```bash
clear    # 清空向量库
history  # 清空对话历史
help     # 显示帮助
exit     # 退出程序
```

---

## 🛠️ 常用命令

### Docker 方式

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart
```

### 本地方式

```bash
# 启动应用
make dev

# 运行测试
make test

# 代码检查
make lint

# 格式化代码
make format
```

---

## ⚙️ 配置（可选）

### 环境变量

编辑 `.env` 文件：

```env
# LLM 配置
OLLAMA_MODEL=deepseek-r1:7b
LLM_TEMPERATURE=0.7

# 文档处理
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# LangSmith 追踪（可选）
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_key
```

### 模型选择

```bash
# 查看可用模型
ollama list

# 切换模型
# 编辑 .env 中的 OLLAMA_MODEL
```

---

## 🐛 遇到问题？

### Ollama 连接失败

```bash
# 检查 Ollama 是否运行
docker-compose ps ollama

# 重启 Ollama
docker-compose restart ollama
```

### 内存不足

```bash
# 增加 Docker 内存限制
# Docker Desktop -> Settings -> Resources -> Memory (建议 8GB+)
```

### 模型下载慢

```bash
# 使用国内镜像（如果可用）
# 或者手动下载模型文件
```

### 更多问题

查看 [完整文档](../README.md) 或 [部署指南](DEPLOYMENT.md)

---

## 📚 下一步

- 📖 阅读 [完整文档](../README.md)
- 🔧 查看 [部署指南](DEPLOYMENT.md)
- 🤝 了解 [贡献指南](../CONTRIBUTING.md)
- 💡 浏览 [示例代码](../examples/)

---

## 🎯 快速测试

想快速测试系统？试试这个：

```bash
# 1. 创建测试文档
echo "人工智能是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。" > test.txt

# 2. 上传文档
你: upload test.txt

# 3. 提问
你: 什么是人工智能？
```

---

**祝你使用愉快！** 🚀

有问题？[提交 Issue](https://github.com/yourusername/chatbot-rag/issues)
