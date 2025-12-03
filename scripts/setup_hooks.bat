@echo off
REM 设置 Git hooks (Windows)

echo 🔧 设置 Git hooks...

REM 创建 hooks 目录
if not exist .git\hooks mkdir .git\hooks

REM 复制 pre-commit hook
copy .githooks\pre-commit.bat .git\hooks\pre-commit.bat

echo ✅ Git hooks 设置完成！
echo.
echo 现在每次提交前会自动检查：
echo   - 是否使用了 print()
echo   - 代码格式是否符合规范
echo   - 代码质量检查
echo.
echo 如需跳过检查，使用: git commit --no-verify

pause
