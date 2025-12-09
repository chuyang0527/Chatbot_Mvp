# 多阶段构建 - 基础镜像
FROM python:3.11-slim as base

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 安装 uv (Python 包管理器)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# ================================
# 构建阶段
# ================================
FROM base as builder

# 复制依赖文件
COPY pyproject.toml ./

# 安装 Python 依赖
RUN uv pip install --system -r pyproject.toml

# ================================
# 运行阶段
# ================================
FROM base as runtime

# 从构建阶段复制已安装的包
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 复制应用代码
COPY src/ ./src/
COPY .env.example .env

# 创建必要的目录
RUN mkdir -p data/uploads chroma_db model

# 暴露端口（如果后续添加 API 服务）
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# 默认命令
CMD ["python", "src/main.py"]
