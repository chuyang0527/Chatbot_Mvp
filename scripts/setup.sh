#!/bin/bash
# 自动化初始化脚本（Linux/macOS）

set -e

echo "=========================================="
echo "  聊天机器人 RAG 系统 - 自动化部署"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 Docker
echo -e "${YELLOW}[1/6] 检查 Docker...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker 未安装，请先安装 Docker${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker 已安装${NC}"

# 检查 Docker Compose
echo -e "${YELLOW}[2/6] 检查 Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}✗ Docker Compose 未安装${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose 已安装${NC}"

# 创建必要的目录
echo -e "${YELLOW}[3/6] 创建目录结构...${NC}"
mkdir -p data/uploads
mkdir -p chroma_db
mkdir -p model
echo -e "${GREEN}✓ 目录创建完成${NC}"

# 复制环境变量文件
echo -e "${YELLOW}[4/6] 配置环境变量...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ 已创建 .env 文件（请根据需要修改）${NC}"
else
    echo -e "${GREEN}✓ .env 文件已存在${NC}"
fi

# 下载 Embedding 模型
echo -e "${YELLOW}[5/6] 下载 Embedding 模型...${NC}"
if [ ! -d "model/paraphrase-multilingual-MiniLM-L12-v2/1_Pooling" ]; then
    echo "正在下载模型（约 470MB）..."
    python3 -c "
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
model.save('model/paraphrase-multilingual-MiniLM-L12-v2')
print('模型下载完成')
" || echo -e "${YELLOW}⚠ 模型下载失败，将在容器启动时自动下载${NC}"
else
    echo -e "${GREEN}✓ 模型已存在${NC}"
fi

# 启动服务
echo -e "${YELLOW}[6/6] 启动 Docker 服务...${NC}"
docker-compose up -d

echo ""
echo -e "${GREEN}=========================================="
echo "  部署完成！"
echo "==========================================${NC}"
echo ""
echo "下一步："
echo "  1. 等待 Ollama 服务启动（约 30 秒）"
echo "  2. 下载 DeepSeek 模型："
echo "     docker exec -it chatbot-ollama ollama pull deepseek-r1:7b"
echo ""
echo "  3. 启动聊天机器人："
echo "     docker exec -it chatbot-app python src/main.py"
echo ""
echo "查看日志："
echo "  docker-compose logs -f"
echo ""
echo "停止服务："
echo "  docker-compose down"
echo ""
