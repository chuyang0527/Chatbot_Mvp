# 自动化初始化脚本（Windows PowerShell）

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  聊天机器人 RAG 系统 - 自动化部署" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Docker
Write-Host "[1/6] 检查 Docker..." -ForegroundColor Yellow
try {
    docker --version | Out-Null
    Write-Host "✓ Docker 已安装" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker 未安装，请先安装 Docker Desktop" -ForegroundColor Red
    exit 1
}

# 检查 Docker Compose
Write-Host "[2/6] 检查 Docker Compose..." -ForegroundColor Yellow
try {
    docker-compose --version | Out-Null
    Write-Host "✓ Docker Compose 已安装" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker Compose 未安装" -ForegroundColor Red
    exit 1
}

# 创建必要的目录
Write-Host "[3/6] 创建目录结构..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "data\uploads" | Out-Null
New-Item -ItemType Directory -Force -Path "chroma_db" | Out-Null
New-Item -ItemType Directory -Force -Path "model" | Out-Null
Write-Host "✓ 目录创建完成" -ForegroundColor Green

# 复制环境变量文件
Write-Host "[4/6] 配置环境变量..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ 已创建 .env 文件（请根据需要修改）" -ForegroundColor Green
} else {
    Write-Host "✓ .env 文件已存在" -ForegroundColor Green
}

# 下载 Embedding 模型
Write-Host "[5/6] 下载 Embedding 模型..." -ForegroundColor Yellow
if (-not (Test-Path "model\paraphrase-multilingual-MiniLM-L12-v2\1_Pooling")) {
    Write-Host "正在下载模型（约 470MB）..."
    try {
        python -c @"
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
model.save('model/paraphrase-multilingual-MiniLM-L12-v2')
print('模型下载完成')
"@
    } catch {
        Write-Host "⚠ 模型下载失败，将在容器启动时自动下载" -ForegroundColor Yellow
    }
} else {
    Write-Host "✓ 模型已存在" -ForegroundColor Green
}

# 启动服务
Write-Host "[6/6] 启动 Docker 服务..." -ForegroundColor Yellow
docker-compose up -d

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  部署完成！" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "下一步："
Write-Host "  1. 等待 Ollama 服务启动（约 30 秒）"
Write-Host "  2. 下载 DeepSeek 模型："
Write-Host "     docker exec -it chatbot-ollama ollama pull deepseek-r1:7b"
Write-Host ""
Write-Host "  3. 启动聊天机器人："
Write-Host "     docker exec -it chatbot-app python src/main.py"
Write-Host ""
Write-Host "查看日志："
Write-Host "  docker-compose logs -f"
Write-Host ""
Write-Host "停止服务："
Write-Host "  docker-compose down"
Write-Host ""
