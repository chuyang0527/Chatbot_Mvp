# Makefile for Chatbot RAG System

.PHONY: help install dev test lint format clean docker-build docker-up docker-down docker-logs

# 默认目标
help:
	@echo "可用命令："
	@echo "  make install       - 安装依赖"
	@echo "  make dev           - 启动开发环境"
	@echo "  make test          - 运行测试"
	@echo "  make lint          - 代码检查"
	@echo "  make format        - 代码格式化"
	@echo "  make clean         - 清理临时文件"
	@echo "  make docker-build  - 构建 Docker 镜像"
	@echo "  make docker-up     - 启动 Docker 服务"
	@echo "  make docker-down   - 停止 Docker 服务"
	@echo "  make docker-logs   - 查看 Docker 日志"

# 安装依赖
install:
	@echo "安装依赖..."
	uv sync
	@echo "✓ 依赖安装完成"

# 开发环境
dev:
	@echo "启动开发环境..."
	uv run python src/main.py

# 运行测试
test:
	@echo "运行测试..."
	uv run pytest tests/ -v --tb=short

# 代码检查
lint:
	@echo "代码检查..."
	uv run ruff check src/
	uv run black --check src/

# 代码格式化
format:
	@echo "代码格式化..."
	uv run black src/
	uv run ruff check --fix src/

# 清理临时文件
clean:
	@echo "清理临时文件..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .ruff_cache
	@echo "✓ 清理完成"

# Docker 相关
docker-build:
	@echo "构建 Docker 镜像..."
	docker-compose build

docker-up:
	@echo "启动 Docker 服务..."
	docker-compose up -d
	@echo "✓ 服务已启动"
	@echo "查看日志: make docker-logs"

docker-down:
	@echo "停止 Docker 服务..."
	docker-compose down
	@echo "✓ 服务已停止"

docker-logs:
	docker-compose logs -f

# 下载模型
download-models:
	@echo "下载模型..."
	python scripts/download_model.py

# 初始化项目
init: install download-models
	@echo "创建必要目录..."
	mkdir -p data/uploads chroma_db model
	@echo "复制环境变量文件..."
	cp -n .env.example .env || true
	@echo "✓ 项目初始化完成"
