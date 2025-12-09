# 快速参考指南

## 🚀 一键部署

### Linux/macOS
```bash
chmod +x scripts/setup.sh && ./scripts/setup.sh
```

### Windows
```powershell
.\scripts\setup.ps1
```

## 📦 Docker 命令

```bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 查看状态
docker-compose ps

# 进入容器
docker exec -it chatbot-app bash

# 下载 LLM 模型
docker exec -it chatbot-ollama ollama pull deepseek-r1:7b

# 启动聊天机器人
docker exec -it chatbot-app python src/main.py
```

## 🛠️ Makefile 命令

```bash
make help           # 查看所有命令
make install        # 安装依赖
make dev            # 启动开发环境
make test           # 运行测试
make lint           # 代码检查
make format         # 代码格式化
make clean          # 清理临时文件
make docker-build   # 构建 Docker 镜像
make docker-up      # 启动 Docker 服务
make docker-down    # 停止 Docker 服务
make docker-logs    # 查看 Docker 日志
```

## 📝 Git 工作流

### 分支命名
```bash
feat/功能名称      # 新功能
fix/问题描述       # Bug 修复
docs/文档说明      # 文档更新
refactor/重构说明  # 代码重构
test/测试说明      # 测试相关
chore/任务说明     # 构建/工具相关
```

### 提交信息
```bash
feat(upload): 添加批量文档上传功能
fix(vector): 修复相似度搜索空指针异常
docs(readme): 更新安装步骤说明
refactor(agent): 优化对话历史管理逻辑
test(processor): 添加文档处理单元测试
chore(docker): 更新 Docker 镜像配置
```

### 工作流程
```bash
# 1. 创建分支
git checkout -b feat/new-feature

# 2. 开发和提交
git add .
git commit -m "feat(module): add new feature"

# 3. 推送
git push origin feat/new-feature

# 4. 创建 PR
# 在 GitHub 上创建 Pull Request
```

## 🧪 测试命令

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_config.py

# 显示详细输出
pytest -v

# 显示覆盖率
pytest --cov=src

# 使用 Makefile
make test
```

## 🔍 代码质量

```bash
# 代码检查
ruff check src/

# 代码格式化
black src/

# 使用 Makefile
make lint
make format
```

## 📚 文档结构

```
README.md              # 项目概览
CONTRIBUTING.md        # 贡献指南
CHANGELOG.md           # 变更日志
PROJECT_SUMMARY.md     # 项目总结
CHECKLIST.md           # 完成检查清单
QUICK_REFERENCE.md     # 快速参考（本文件）

docs/
├── DEPLOYMENT.md      # 详细部署指南
├── QUICKSTART.md      # 5分钟快速上手
└── ENGINEERING.md     # 工程化总结
```

## 🔧 配置文件

```
.env                   # 环境变量（从 .env.example 复制）
docker-compose.yml     # Docker 服务编排
Dockerfile             # Docker 镜像构建
Makefile               # 快捷命令
pyproject.toml         # 项目配置
pytest.ini             # 测试配置
```

## 📂 目录结构

```
chatbot-rag/
├── src/               # 源代码
├── tests/             # 测试代码
├── scripts/           # 自动化脚本
├── docs/              # 文档
├── examples/          # 示例代码
├── data/              # 数据目录
├── chroma_db/         # 向量数据库
└── model/             # 本地模型
```

## 🐛 故障排查

### Ollama 连接失败
```bash
docker-compose logs ollama
docker-compose restart ollama
```

### 内存不足
```bash
# 增加 Docker 内存限制
# Docker Desktop -> Settings -> Resources -> Memory (建议 8GB+)
```

### 模型下载失败
```bash
# 手动下载
docker exec -it chatbot-ollama bash
ollama pull deepseek-r1:7b
```

### 向量数据库损坏
```bash
docker-compose down
rm -rf chroma_db/
docker-compose up -d
```

## 🌐 环境变量

```env
# Ollama 配置
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-r1:7b

# LLM 参数
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000

# 文档处理
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# 检索参数
RETRIEVAL_K=4

# LangSmith（可选）
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_api_key
LANGCHAIN_PROJECT=chatbot-rag
```

## 🔗 相关链接

- [GitHub Repository](https://github.com/yourusername/chatbot-rag)
- [Issues](https://github.com/yourusername/chatbot-rag/issues)
- [Pull Requests](https://github.com/yourusername/chatbot-rag/pulls)
- [Discussions](https://github.com/yourusername/chatbot-rag/discussions)

## 📞 获取帮助

1. 查看 [README.md](README.md)
2. 查看 [docs/QUICKSTART.md](docs/QUICKSTART.md)
3. 查看 [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
4. 提交 [Issue](https://github.com/yourusername/chatbot-rag/issues)

---

**快速参考指南** | 版本 v0.2.0 | 更新时间：2024-12-09
