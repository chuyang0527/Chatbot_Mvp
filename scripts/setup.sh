#!/bin/bash
# 项目设置脚本

echo "🚀 开始设置聊天机器人项目..."

# 检查 Python 版本
echo "检查 Python 版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python 版本: $python_version"

# 安装 uv
echo ""
echo "安装 uv..."
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "✅ uv 安装完成"
else
    echo "✅ uv 已安装"
fi

# 创建虚拟环境
echo ""
echo "创建虚拟环境..."
uv venv
echo "✅ 虚拟环境创建完成"

# 安装依赖
echo ""
echo "安装依赖..."
uv pip install -r requirements.txt
echo "✅ 依赖安装完成"

# 创建 .env 文件
echo ""
if [ ! -f .env ]; then
    echo "创建 .env 文件..."
    cp .env.example .env
    echo "✅ .env 文件已创建，请编辑并填入 API Keys"
else
    echo "✅ .env 文件已存在"
fi

# 创建必要的目录
echo ""
echo "创建数据目录..."
mkdir -p data/documents
mkdir -p data/vector_db
mkdir -p logs
echo "✅ 目录创建完成"

echo ""
echo "🎉 设置完成！"
echo ""
echo "下一步："
echo "1. 编辑 .env 文件，填入你的 API Keys"
echo "2. 运行示例: uv run python examples/demo.py"
echo "3. 启动聊天: uv run python src/main.py"
