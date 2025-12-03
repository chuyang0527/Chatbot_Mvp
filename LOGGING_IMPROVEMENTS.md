# 日志系统改进说明

## 改进概述

根据要求"禁止使用 print() 打印调试信息，必须使用标准日志模块（如 logging 或 loguru）进行日志输出，确保可控性和可配置性"，对项目进行了全面的日志系统改进。

## 改进内容

### 1. 增强的日志工具 (`src/utils/logger.py`)

#### 新增功能

- ✅ 支持多种日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL）
- ✅ 支持控制台输出（使用 Rich 美化）
- ✅ 支持文件日志输出（可选）
- ✅ 支持自定义日志记录器
- ✅ 完整的文档字符串和使用说明

#### 代码示例

```python
from src.utils.logger import logger, get_logger

# 使用默认 logger
logger.info("一般信息")
logger.debug("调试信息")
logger.error("错误信息", exc_info=True)

# 创建自定义 logger
custom_logger = get_logger(
    name="my_module",
    level=logging.DEBUG,
    log_file="./logs/my_module.log"
)
```

### 2. 配置管理增强 (`src/config.py`)

#### 新增配置项

```python
# 日志配置
log_level: str = "INFO"              # 日志级别
log_file: str = "./logs/chatbot.log" # 日志文件路径
enable_file_logging: bool = False    # 是否启用文件日志
```

#### 环境变量配置

在 `.env` 文件中可配置：

```env
LOG_LEVEL=INFO
LOG_FILE=./logs/chatbot.log
ENABLE_FILE_LOGGING=false
```

### 3. 完整的文档

#### 新增文档文件

1. **LOGGING_GUIDE.md** - 日志使用规范
   - 日志 vs 用户界面输出的区别
   - 各日志级别的使用说明
   - 最佳实践和常见错误
   - 配置和调试技巧

2. **CODE_REVIEW_CHECKLIST.md** - 代码审查清单
   - 日志规范检查项
   - 代码质量检查项
   - 自动检查命令
   - 提交前检查清单

3. **LOGGING_IMPROVEMENTS.md** - 本文档
   - 改进说明和使用指南

#### 更新的文档

- **README.md** - 添加日志规范说明
- **CONTRIBUTING.md** - 添加日志规范要求
- **CHECKLIST.md** - 添加日志规范检查项

### 4. Git Hooks

#### 自动检查脚本

创建了 pre-commit hooks 自动检查：

- `.githooks/pre-commit` (Linux/Mac)
- `.githooks/pre-commit.bat` (Windows)

#### 设置脚本

- `scripts/setup_hooks.sh` (Linux/Mac)
- `scripts/setup_hooks.bat` (Windows)

#### 使用方法

```bash
# Linux/Mac
chmod +x scripts/setup_hooks.sh
./scripts/setup_hooks.sh

# Windows
scripts\setup_hooks.bat
```

设置后，每次 `git commit` 前会自动检查：
1. 是否使用了 `print()`
2. 代码格式是否符合规范
3. 代码质量检查

## 项目现状验证

### ✅ 无 print() 使用

经过检查，项目中没有使用 `print()` 进行调试：

```bash
grep -r "print(" src/ --include="*.py"
# 结果：无匹配
```

### ✅ 所有模块使用 logger

所有需要日志的模块都正确导入和使用了 logger：

- `src/document_processor/loader.py`
- `src/document_processor/splitter.py`
- `src/document_processor/vectorizer.py`
- `src/retrieval/vector_store.py`
- `src/retrieval/retriever.py`
- `src/agent/graph.py`
- `src/agent/nodes.py`
- `src/main.py`
- `src/upload_document.py`

### ✅ 用户界面输出分离

用户界面输出使用 `console.print()`（Rich），与日志系统分离：

- `src/main.py` - 交互式聊天界面
- `src/upload_document.py` - 文档上传进度显示
- `examples/demo.py` - 演示流程显示

这是合理的设计，因为：
- **logger** 用于系统日志和调试信息
- **console** 用于用户界面和交互显示

## 使用指南

### 基本使用

```python
from src.utils.logger import logger

# 调试信息
logger.debug(f"变量值: x={x}, y={y}")

# 一般信息
logger.info("开始处理文档")
logger.info(f"处理完成，共 {count} 个片段")

# 警告信息
logger.warning("向量数据库为空")

# 错误信息
try:
    process()
except Exception as e:
    logger.error(f"处理失败: {e}", exc_info=True)
```

### 配置日志级别

#### 方法 1: 环境变量

编辑 `.env` 文件：

```env
LOG_LEVEL=DEBUG
ENABLE_FILE_LOGGING=true
LOG_FILE=./logs/chatbot.log
```

#### 方法 2: 临时设置

```bash
# Linux/Mac
export LOG_LEVEL=DEBUG

# Windows (CMD)
set LOG_LEVEL=DEBUG

# Windows (PowerShell)
$env:LOG_LEVEL="DEBUG"
```

### 查看日志

#### 控制台日志

运行程序时自动显示在终端。

#### 文件日志

启用文件日志后：

```bash
# 查看日志文件
cat logs/chatbot.log

# 实时查看
tail -f logs/chatbot.log

# 搜索错误
grep "ERROR" logs/chatbot.log
```

## 最佳实践

### ✅ 正确做法

```python
# 1. 使用合适的日志级别
logger.debug("详细的调试信息")
logger.info("重要的业务事件")
logger.error("错误信息", exc_info=True)

# 2. 包含上下文信息
logger.info(f"处理文档: {file_path}, 大小: {size} bytes")

# 3. 记录异常堆栈
try:
    process()
except Exception as e:
    logger.error(f"处理失败: {e}", exc_info=True)
    raise

# 4. 保护敏感信息
logger.info(f"API Key: {api_key[:8]}...")
```

### ❌ 错误做法

```python
# 1. 使用 print()
print("调试信息")  # 禁止！

# 2. 日志级别不当
logger.info(f"循环第 {i} 次")  # 应该用 DEBUG

# 3. 缺少异常信息
except Exception as e:
    logger.error(str(e))  # 缺少堆栈

# 4. 暴露敏感信息
logger.info(f"密码: {password}")  # 危险！
```

## 检查和验证

### 手动检查

```bash
# 检查是否使用了 print()
grep -r "print(" src/ --include="*.py"

# 应该没有输出（或只有 console.print）
```

### 自动检查

```bash
# 设置 Git hooks
./scripts/setup_hooks.sh  # Linux/Mac
scripts\setup_hooks.bat   # Windows

# 之后每次提交会自动检查
git commit -m "feat: 添加新功能"
```

### 代码格式检查

```bash
# 格式化代码
uv run black src/

# Lint 检查
uv run ruff check src/

# 运行测试
uv run pytest tests/
```

## 常见问题

### Q1: 什么时候可以使用 console.print()？

**A:** 仅用于用户界面显示，不用于调试：

```python
# ✅ 正确：用户界面
console.print("[green]✓[/green] 操作成功")
question = console.input("请输入问题：")

# ❌ 错误：调试信息
console.print(f"变量值: {x}")  # 应该用 logger.debug()
```

### Q2: 如何临时启用详细日志？

**A:** 修改 `.env` 文件或设置环境变量：

```env
LOG_LEVEL=DEBUG
```

### Q3: 日志文件在哪里？

**A:** 默认在 `logs/chatbot.log`，可通过配置修改。

### Q4: 如何关闭文件日志？

**A:** 在 `.env` 中设置：

```env
ENABLE_FILE_LOGGING=false
```

## 总结

### 改进成果

1. ✅ **完全符合要求** - 禁止使用 print()，使用标准 logging 模块
2. ✅ **可控性** - 通过环境变量配置日志级别和输出
3. ✅ **可配置性** - 支持控制台和文件日志，可自定义格式
4. ✅ **完整文档** - 详细的使用指南和最佳实践
5. ✅ **自动检查** - Git hooks 自动检查代码规范
6. ✅ **清晰分离** - 日志系统与用户界面输出分离

### 关键特性

- 🚫 **禁止 print()** - 所有调试信息使用 logger
- 📊 **多级别日志** - DEBUG/INFO/WARNING/ERROR/CRITICAL
- 🎨 **美化输出** - 使用 Rich 美化控制台日志
- 📁 **文件日志** - 可选的文件日志输出
- ⚙️ **灵活配置** - 环境变量配置所有参数
- 🔍 **自动检查** - Git hooks 自动检查规范

### 使用建议

1. 开发时设置 `LOG_LEVEL=DEBUG` 查看详细信息
2. 生产环境设置 `LOG_LEVEL=INFO` 或 `WARNING`
3. 启用文件日志便于问题追踪
4. 定期清理旧日志文件
5. 遵循日志使用规范

项目现在拥有完善的日志系统，完全符合"禁止使用 print()，必须使用标准日志模块"的要求！
