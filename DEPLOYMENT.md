# 部署指南

## 本地开发环境

### 快速开始

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd chatbot-mvp

# 2. 安装 uv
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 3. 创建虚拟环境
uv venv

# 4. 激活虚拟环境
# Windows
.venv\Scripts\activate

# 5. 安装依赖
uv pip install -r requirements.txt

# 6. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入 API Keys

# 7. 运行示例
uv run python examples/demo.py

# 8. 启动聊天机器人
uv run python src/main.py
```

## 生产环境部署

### Docker 部署（推荐）

创建 `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装 uv
RUN pip install uv

# 复制项目文件
COPY . .

# 安装依赖
RUN uv pip install --system -r requirements.txt

# 暴露端口（如果有 Web 界面）
EXPOSE 8000

# 启动命令
CMD ["python", "src/main.py"]
```

构建和运行：

```bash
docker build -t chatbot-mvp .
docker run -it --env-file .env chatbot-mvp
```

### 云服务部署

#### AWS EC2

1. 启动 EC2 实例（推荐 t3.medium 或更高）
2. 安装 Python 3.10+
3. 克隆项目并安装依赖
4. 使用 systemd 或 supervisor 管理进程

#### Google Cloud Run

```bash
gcloud run deploy chatbot-mvp \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Azure Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name chatbot-mvp \
  --image chatbot-mvp:latest \
  --environment-variables \
    OPENAI_API_KEY=$OPENAI_API_KEY \
    LANGCHAIN_API_KEY=$LANGCHAIN_API_KEY
```

## 性能优化

### 1. 向量数据库优化

- 使用云端向量数据库（Pinecone, Weaviate, Qdrant）
- 启用索引优化
- 调整 chunk_size 和 overlap 参数

### 2. LLM 调用优化

- 使用缓存减少重复调用
- 调整 temperature 参数
- 考虑使用更快的模型（如 gpt-3.5-turbo）

### 3. 并发处理

- 使用异步 I/O
- 实现请求队列
- 添加负载均衡

## 监控和日志

### 日志配置

修改 `src/utils/logger.py` 添加文件日志：

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RichHandler(),
        logging.FileHandler("logs/app.log")
    ]
)
```

### 监控指标

建议监控：
- 响应时间
- Token 使用量
- 错误率
- 并发用户数

## 安全建议

1. **API Key 管理**: 使用密钥管理服务（AWS Secrets Manager, Azure Key Vault）
2. **访问控制**: 添加身份验证和授权
3. **速率限制**: 防止滥用
4. **数据加密**: 传输和存储都使用加密
5. **定期更新**: 及时更新依赖包

## 备份策略

### 向量数据库备份

```bash
# 备份
tar -czf vector_db_backup_$(date +%Y%m%d).tar.gz data/vector_db/

# 恢复
tar -xzf vector_db_backup_20241203.tar.gz
```

### 配置备份

定期备份 `.env` 和配置文件（注意不要提交到 Git）。

## 故障排查

### 常见问题

1. **向量数据库加载失败**
   - 检查路径权限
   - 确认数据完整性

2. **LLM 调用超时**
   - 增加超时时间
   - 检查网络连接
   - 考虑使用代理

3. **内存不足**
   - 减少 chunk_size
   - 限制并发数
   - 增加服务器内存

## 扩展性考虑

### 水平扩展

- 使用云端向量数据库
- 实现无状态服务
- 使用消息队列处理异步任务

### 垂直扩展

- 增加服务器配置
- 优化代码性能
- 使用缓存

## 成本优化

1. **选择合适的模型**: gpt-3.5-turbo 比 gpt-4 便宜很多
2. **缓存策略**: 缓存常见问题的回答
3. **批量处理**: 合并多个请求
4. **监控使用量**: 设置预算告警
