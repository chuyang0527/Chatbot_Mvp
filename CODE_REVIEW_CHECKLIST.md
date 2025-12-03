# 代码审查清单

## 日志规范检查

### ❌ 禁止项

- [ ] 代码中是否使用了 `print()` 进行调试？
- [ ] 是否有未使用 logger 的调试信息？
- [ ] 是否在日志中暴露了敏感信息（API Key、密码等）？
- [ ] 是否在循环中产生大量日志？

### ✅ 必须项

- [ ] 所有调试信息都使用 `logger` 模块
- [ ] 使用了合适的日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL）
- [ ] 异常处理中使用了 `exc_info=True` 记录堆栈
- [ ] 日志信息包含足够的上下文
- [ ] 敏感信息已脱敏或隐藏

## 代码质量检查

### 代码风格

- [ ] 遵循 PEP 8 规范
- [ ] 使用了类型提示
- [ ] 函数和类有文档字符串
- [ ] 变量命名清晰有意义

### 错误处理

- [ ] 有适当的异常处理
- [ ] 异常信息清晰明确
- [ ] 不会吞掉异常
- [ ] 使用了合适的异常类型

### 性能

- [ ] 没有明显的性能问题
- [ ] 避免了不必要的循环
- [ ] 合理使用了缓存
- [ ] 数据库查询优化

### 安全性

- [ ] 输入验证
- [ ] SQL 注入防护
- [ ] XSS 防护
- [ ] API Key 安全存储

## 测试检查

- [ ] 有单元测试
- [ ] 测试覆盖关键功能
- [ ] 测试用例清晰
- [ ] 边界条件测试

## 文档检查

- [ ] README 更新
- [ ] API 文档更新
- [ ] 注释清晰
- [ ] 示例代码可运行

## 日志使用示例

### ✅ 正确示例

```python
from src.utils.logger import logger

def process_document(file_path: str):
    """处理文档"""
    logger.info(f"开始处理文档: {file_path}")
    
    try:
        # 处理逻辑
        result = load_and_process(file_path)
        logger.info(f"文档处理成功，生成 {len(result)} 个片段")
        return result
        
    except FileNotFoundError as e:
        logger.error(f"文件不存在: {file_path}", exc_info=True)
        raise
        
    except Exception as e:
        logger.error(f"文档处理失败: {e}", exc_info=True)
        raise
```

### ❌ 错误示例

```python
def process_document(file_path: str):
    """处理文档"""
    print(f"处理文档: {file_path}")  # ❌ 禁止使用 print
    
    try:
        result = load_and_process(file_path)
        print("成功")  # ❌ 禁止使用 print
        return result
        
    except Exception as e:
        print(f"错误: {e}")  # ❌ 禁止使用 print
        # ❌ 没有记录堆栈信息
        # ❌ 吞掉了异常
```

## 自动检查命令

### 检查是否使用了 print()

```bash
# Linux/Mac
grep -r "print(" src/ --include="*.py"

# Windows (PowerShell)
Select-String -Path "src\*.py" -Pattern "print\(" -Recurse
```

如果有输出，说明代码中使用了 `print()`，需要修改为 `logger`。

### 代码格式检查

```bash
# 使用 black 格式化
uv run black src/

# 使用 ruff 检查
uv run ruff check src/
```

### 运行测试

```bash
uv run pytest tests/ -v
```

## 提交前检查

在提交代码前，请确保：

1. ✅ 没有使用 `print()` 进行调试
2. ✅ 所有日志使用了合适的级别
3. ✅ 代码通过了格式检查
4. ✅ 所有测试通过
5. ✅ 文档已更新
6. ✅ 没有提交敏感信息

## 审查工具

### 推荐工具

- **pylint**: 代码质量检查
- **black**: 代码格式化
- **ruff**: 快速 linter
- **mypy**: 类型检查
- **pytest**: 单元测试

### 安装审查工具

```bash
uv pip install pylint black ruff mypy pytest
```

### 运行完整检查

```bash
# 格式化代码
uv run black src/

# Lint 检查
uv run ruff check src/

# 类型检查
uv run mypy src/

# 运行测试
uv run pytest tests/
```

## 常见问题

### Q: 什么时候可以使用 console.print()？

A: 仅用于用户界面显示，不用于调试：

```python
from rich.console import Console
console = Console()

# ✅ 正确：用户界面
console.print("[green]✓[/green] 操作成功")
question = console.input("请输入：")

# ❌ 错误：调试信息
console.print(f"变量值: {x}")  # 应该用 logger.debug()
```

### Q: 如何临时启用详细日志？

A: 修改 `.env` 文件：

```env
LOG_LEVEL=DEBUG
ENABLE_FILE_LOGGING=true
```

### Q: 如何查看日志文件？

A: 日志文件位于 `logs/chatbot.log`：

```bash
# 查看最新日志
tail -f logs/chatbot.log

# 搜索错误
grep "ERROR" logs/chatbot.log
```

## 总结

遵循这个检查清单，确保代码质量和日志规范：

1. **禁止使用 `print()`** - 使用 logger
2. **合适的日志级别** - DEBUG/INFO/WARNING/ERROR
3. **完整的异常信息** - exc_info=True
4. **代码质量** - 格式、测试、文档
5. **安全性** - 输入验证、敏感信息保护

在提交 PR 前，请完成所有检查项！
