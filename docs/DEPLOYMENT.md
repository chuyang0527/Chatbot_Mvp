# 部署指南

本文档详细说明如何在不同环境中部署聊天机器人 RAG 系统。

## 目录

- [Docker 部署](#docker-部署)
- [本地开发部署](#本地开发部署)
- [生产环境部署](#生产环境部署)
- [云平台部署](#云平台部署)

## Docker 部署

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少 8GB 内存
- 20GB 可用磁盘空间

### 快速部署

#### Linux/macOS

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd chatbot-rag

# 2. 运行自动化脚本
chmod +x scripts/setup.sh
./scripts/setup.sh

# 3. 等待服务启动（约 30 秒）
docker-compose ps

# 4. 下载 LLM 模型
docker exec -it chatbot-ollama ollama pull deepseek-r1:7b

# 5. 启动聊天机器人
docker exec -it chatbot-app python src/main.py
```

#### Windows

```powershell
# 1. 克隆项目
git clone <your-repo-url>
cd chatbot-rag

# 2. 运行自动化脚本
.\scripts\setup.ps1

# 3. 等待服务启动（约 30 秒）
docker-compose ps

# 4. 下载 LLM 模型
docker exec -it chatbot-ollama ollama pull deepseek-r1:7b

# 5. 启动聊天机器人
docker exec -it chatbot-app python src/main.py
```

### 手动部署

```bash
# 1. 创建必要目录
mkdir -p data/uploads chroma_db model

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 3. 构建镜像
docker-compose build

# 4. 启动服务
docker-compose up -d

# 5. 查看日志
docker-compose logs -f
```

### 服务管理

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f [service_name]

# 进入容器
docker exec -it chatbot-app bash

# 查看服务状态
docker-compose ps
```

### 数据持久化

数据卷配置：

```yaml
volumes:
  - ./data:/app/data              # 上传的文档
  - ./chroma_db:/app/chroma_db    # 向量数据库
  - ./model:/app/model            # 本地模型
  - ./.env:/app/.env              # 环境变量
```

备份数据：

```bash
# 备份向量数据库
tar -czf chroma_db_backup.tar.gz chroma_db/

# 备份上传的文档
tar -czf data_backup.tar.gz data/

# 恢复数据
tar -xzf chroma_db_backup.tar.gz
tar -xzf data_backup.tar.gz
```

## 本地开发部署

### 前置要求

- Python 3.10+
- uv (Python 包管理器)
- Ollama
- 8GB+ 内存

### 安装步骤

```bash
# 1. 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 克隆项目
git clone <your-repo-url>
cd chatbot-rag

# 3. 安装依赖
make install
# 或
uv sync

# 4. 下载模型
make download-models
# 或
python scripts/download_model.py

# 5. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 6. 启动 Ollama
ollama serve

# 7. 下载 LLM 模型
ollama pull deepseek-r1:7b

# 8. 启动应用
make dev
# 或
uv run python src/main.py
```

### 开发工具

```bash
# 代码格式化
make format

# 代码检查
make lint

# 运行测试
make test

# 清理临时文件
make clean
```

## 生产环境部署

### 性能优化

#### 1. 使用 GPU 加速（可选）

修改 `docker-compose.yml`：

```yaml
services:
  ollama:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

#### 2. 调整资源限制

```yaml
services:
  chatbot:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
```

#### 3. 优化向量数据库

在 `.env` 中调整参数：

```env
CHUNK_SIZE=500          # 减小块大小
CHUNK_OVERLAP=100       # 减小重叠
RETRIEVAL_K=3           # 减少检索数量
```

### 安全配置

#### 1. 环境变量管理

```bash
# 使用 Docker secrets
echo "your_api_key" | docker secret create langsmith_key -

# 在 docker-compose.yml 中引用
secrets:
  - langsmith_key
```

#### 2. 网络隔离

```yaml
networks:
  chatbot-network:
    driver: bridge
    internal: true  # 内部网络
```

#### 3. 只读文件系统

```yaml
services:
  chatbot:
    read_only: true
    tmpfs:
      - /tmp
```

### 监控和日志

#### 1. 日志配置

```yaml
services:
  chatbot:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

#### 2. 健康检查

```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## 云平台部署

### AWS ECS

```bash
# 1. 构建并推送镜像
docker build -t chatbot-rag .
docker tag chatbot-rag:latest <aws-account>.dkr.ecr.region.amazonaws.com/chatbot-rag:latest
docker push <aws-account>.dkr.ecr.region.amazonaws.com/chatbot-rag:latest

# 2. 创建 ECS 任务定义
# 3. 创建 ECS 服务
# 4. 配置负载均衡器
```

### Google Cloud Run

```bash
# 1. 构建镜像
gcloud builds submit --tag gcr.io/PROJECT-ID/chatbot-rag

# 2. 部署到 Cloud Run
gcloud run deploy chatbot-rag \
  --image gcr.io/PROJECT-ID/chatbot-rag \
  --platform managed \
  --region us-central1 \
  --memory 8Gi
```

### Azure Container Instances

```bash
# 1. 创建资源组
az group create --name chatbot-rg --location eastus

# 2. 部署容器
az container create \
  --resource-group chatbot-rg \
  --name chatbot-rag \
  --image chatbot-rag:latest \
  --cpu 4 \
  --memory 8
```

## 故障排查

### 常见问题

#### 1. Ollama 连接失败

```bash
# 检查 Ollama 服务
docker-compose logs ollama

# 重启 Ollama
docker-compose restart ollama

# 检查端口
netstat -an | grep 11434
```

#### 2. 内存不足

```bash
# 查看容器资源使用
docker stats

# 增加 Docker 内存限制
# Docker Desktop -> Settings -> Resources -> Memory
```

#### 3. 模型下载失败

```bash
# 手动下载模型
docker exec -it chatbot-ollama bash
ollama pull deepseek-r1:7b

# 或使用代理
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
```

#### 4. 向量数据库损坏

```bash
# 清空并重建
docker-compose down
rm -rf chroma_db/
docker-compose up -d
```

### 日志查看

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f chatbot

# 查看最近 100 行
docker-compose logs --tail=100 chatbot
```

## 性能基准

### 硬件要求

| 配置 | CPU | 内存 | 磁盘 | 适用场景 |
|------|-----|------|------|----------|
| 最小 | 2核 | 4GB | 10GB | 开发测试 |
| 推荐 | 4核 | 8GB | 20GB | 小规模生产 |
| 高性能 | 8核+ | 16GB+ | 50GB+ | 大规模生产 |

### 性能指标

- 文档处理速度：~1MB/s
- 向量检索延迟：<100ms
- LLM 生成速度：~20 tokens/s
- 并发支持：10+ 用户

## 更新和维护

### 更新应用

```bash
# 1. 拉取最新代码
git pull origin main

# 2. 重新构建镜像
docker-compose build

# 3. 重启服务
docker-compose up -d
```

### 数据库迁移

```bash
# 备份现有数据
docker-compose exec chatbot python scripts/backup_db.py

# 执行迁移
docker-compose exec chatbot python scripts/migrate_db.py
```

### 版本回滚

```bash
# 1. 停止服务
docker-compose down

# 2. 切换到旧版本
git checkout v1.0.0

# 3. 重新构建
docker-compose build

# 4. 启动服务
docker-compose up -d
```

## 支持

如有问题，请：
1. 查看 [常见问题](../README.md#常见问题)
2. 提交 [Issue](https://github.com/yourusername/chatbot-rag/issues)
3. 查看 [讨论区](https://github.com/yourusername/chatbot-rag/discussions)
