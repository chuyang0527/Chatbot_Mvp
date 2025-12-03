@echo off
REM 项目设置脚本 (Windows)

echo 🚀 开始设置聊天机器人项目...

REM 检查 Python 版本
echo 检查 Python 版本...
python --version
if errorlevel 1 (
    echo ❌ 未找到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)

REM 安装 uv
echo.
echo 安装 uv...
where uv >nul 2>nul
if errorlevel 1 (
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    echo ✅ uv 安装完成
) else (
    echo ✅ uv 已安装
)

REM 创建虚拟环境
echo.
echo 创建虚拟环境...
uv venv
echo ✅ 虚拟环境创建完成

REM 安装依赖
echo.
echo 安装依赖...
uv pip install -r requirements.txt
echo ✅ 依赖安装完成

REM 创建 .env 文件
echo.
if not exist .env (
    echo 创建 .env 文件...
    copy .env.example .env
    echo ✅ .env 文件已创建，请编辑并填入 API Keys
) else (
    echo ✅ .env 文件已存在
)

REM 创建必要的目录
echo.
echo 创建数据目录...
if not exist data\documents mkdir data\documents
if not exist data\vector_db mkdir data\vector_db
if not exist logs mkdir logs
echo ✅ 目录创建完成

echo.
echo 🎉 设置完成！
echo.
echo 下一步：
echo 1. 编辑 .env 文件，填入你的 API Keys
echo 2. 运行示例: uv run python examples/demo.py
echo 3. 启动聊天: uv run python src/main.py

pause
