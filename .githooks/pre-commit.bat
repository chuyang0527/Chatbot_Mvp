@echo off
REM Pre-commit hook for Windows: 检查代码规范

echo 🔍 运行 pre-commit 检查...

REM 检查是否使用了 print()
echo 检查是否使用了 print()...
findstr /S /R "print(" src\*.py > nul 2>&1
if %errorlevel% equ 0 (
    findstr /S /R "console\.print" src\*.py > nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ 错误：代码中使用了 print() 进行调试！
        echo 请使用 logger 模块替代 print()
        echo 详见: LOGGING_GUIDE.md
        exit /b 1
    )
)
echo ✅ 未发现 print() 使用

REM 检查代码格式
echo 检查代码格式...
where black >nul 2>nul
if %errorlevel% equ 0 (
    black --check src\
    if %errorlevel% neq 0 (
        echo ❌ 代码格式不符合规范
        echo 运行: uv run black src/
        exit /b 1
    )
    echo ✅ 代码格式检查通过
) else (
    echo ⚠️  未安装 black，跳过格式检查
)

REM 检查 lint
echo 检查代码质量...
where ruff >nul 2>nul
if %errorlevel% equ 0 (
    ruff check src\ --quiet
    if %errorlevel% neq 0 (
        echo ❌ 代码质量检查失败
        echo 运行: uv run ruff check src/
        exit /b 1
    )
    echo ✅ 代码质量检查通过
) else (
    echo ⚠️  未安装 ruff，跳过 lint 检查
)

echo ✅ 所有检查通过！
exit /b 0
