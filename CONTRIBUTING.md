# 贡献指南

感谢你对本项目的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 报告 Bug

如果你发现了 bug，请创建一个 Issue，包含：

1. Bug 描述
2. 复现步骤
3. 期望行为
4. 实际行为
5. 环境信息（操作系统、Python 版本等）

### 提出新功能

如果你有新功能的想法，请先创建一个 Issue 讨论：

1. 功能描述
2. 使用场景
3. 实现思路

### 提交代码

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 开发规范

### 分支命名

- `feature/*`: 新功能
- `bugfix/*`: Bug 修复
- `hotfix/*`: 紧急修复
- `refactor/*`: 代码重构
- `docs/*`: 文档更新

### Commit 规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

示例：
```
feat: 添加 PDF 文档支持
fix: 修复向量检索错误
docs: 更新 README 安装说明
```

### 代码风格

- 使用 Black 格式化代码
- 使用 Ruff 进行 lint 检查
- 遵循 PEP 8 规范
- 添加必要的注释和文档字符串

运行格式化：
```bash
uv run black src/
uv run ruff check src/
```

### 日志规范

**重要：禁止使用 `print()` 进行调试！**

所有调试信息必须使用标准日志模块：

```python
from src.utils.logger import logger

# ✅ 正确
logger.debug("调试信息")
logger.info("一般信息")
logger.warning("警告信息")
logger.error("错误信息", exc_info=True)

# ❌ 错误
print("调试信息")  # 禁止！
```

详细规范请查看 [日志使用规范](LOGGING_GUIDE.md)

提交前检查：
```bash
# 检查是否使用了 print()
grep -r "print(" src/ --include="*.py"
# 如果有输出，说明需要修改
```

### 测试

- 为新功能添加测试
- 确保所有测试通过
- 保持测试覆盖率

运行测试：
```bash
uv run pytest
```

## Pull Request 流程

1. 确保代码通过所有测试
2. 更新相关文档
3. 在 PR 描述中说明更改内容
4. 等待 Code Review
5. 根据反馈进行修改
6. 合并到主分支

## 行为准则

- 尊重他人
- 保持专业
- 接受建设性批评
- 关注项目目标

## 联系方式

如有问题，可以通过以下方式联系：

- 创建 Issue
- 发送邮件
- 加入讨论组

感谢你的贡献！🎉
