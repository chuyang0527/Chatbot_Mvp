# 日志使用规范

## 重要原则

**禁止使用 `print()` 进行调试输出！**

所有系统信息、调试信息、错误信息都必须使用标准日志模块（logging）进行输出，确保可控性和可配置性。

## 日志 vs 用户界面输出

### 日志输出 (logger)

用于记录系统运行状态、调试信息、错误信息：

```python
from src.utils.logger import logger

# ✅ 正确：使用 logger
logger.debug("详细的调试信息")
logger.info("一般信息")
logger.warning("警告信息")
logger.error("错误信息")
logger.critical("严重错误")

# ❌ 错误：禁止使用 print
print("调试信息")  # 禁止！
```

### 用户界面输出 (console)

仅用于向用户显示格式化的交互信息：

```python
from rich.console import Console

console = Console()

# ✅ 正确：用户界面显示
console.print("[green]✓[/green] 操作成功")
console.print(Panel("欢迎信息"))
question = console.input("请输入问题：")

# 这些是用户交互，不是调试信息
```

## 日志级别说明

### DEBUG (调试)

详细的调试信息，仅在开发和调试时使用：

```python
logger.debug(f"函数参数: query={query}, k={k}")
logger.debug(f"中间结果: {intermediate_result}")
logger.debug(f"循环迭代 {i}: {item}")
```

### INFO (信息)

一般的运行信息，记录重要的业务流程：

```python
logger.info("正在加载文档...")
logger.info(f"文档加载完成，共 {len(documents)} 个片段")
logger.info("开始向量检索")
logger.info(f"检索到 {len(results)} 个相关文档")
```

### WARNING (警告)

警告信息，不影响运行但需要注意：

```python
logger.warning("向量数据库为空，请先上传文档")
logger.warning(f"检索结果少于预期: {len(results)} < {expected}")
logger.warning("API 调用接近限额")
```

### ERROR (错误)

错误信息，影响功能但不会导致程序崩溃：

```python
logger.error(f"文档加载失败: {e}")
logger.error(f"向量检索出错: {e}", exc_info=True)
logger.error("LLM 调用失败，正在重试...")
```

### CRITICAL (严重错误)

严重错误，可能导致程序无法继续运行：

```python
logger.critical("无法连接到向量数据库")
logger.critical(f"配置文件损坏: {e}")
logger.critical("API Key 无效，程序无法启动")
```

## 配置日志

### 环境变量配置

在 `.env` 文件中配置：

```env
# 日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# 日志文件路径
LOG_FILE=./logs/chatbot.log

# 是否启用文件日志
ENABLE_FILE_LOGGING=true
```

### 代码中配置

```python
from src.utils.logger import get_logger

# 获取自定义日志记录器
logger = get_logger(
    name="my_module",
    level=logging.DEBUG,
    log_file="./logs/my_module.log"
)
```

## 最佳实践

### 1. 使用合适的日志级别

```python
# ✅ 正确
logger.info("用户登录成功")  # 重要业务事件
logger.debug(f"查询参数: {params}")  # 调试信息
logger.error(f"数据库连接失败: {e}")  # 错误

# ❌ 错误
logger.info(f"循环第 {i} 次")  # 应该用 DEBUG
logger.error("用户登录成功")  # 应该用 INFO
```

### 2. 包含上下文信息

```python
# ✅ 正确：包含足够的上下文
logger.info(f"正在处理文档: {file_path}, 大小: {file_size} bytes")
logger.error(f"文档 {doc_id} 处理失败: {e}", exc_info=True)

# ❌ 错误：信息不足
logger.info("处理文档")
logger.error("失败")
```

### 3. 使用异常追踪

```python
# ✅ 正确：记录完整的异常堆栈
try:
    result = process_document(file_path)
except Exception as e:
    logger.error(f"文档处理失败: {e}", exc_info=True)
    raise

# ❌ 错误：丢失堆栈信息
except Exception as e:
    logger.error(f"错误: {e}")
```

### 4. 避免敏感信息

```python
# ✅ 正确：隐藏敏感信息
logger.info(f"API Key: {api_key[:8]}...")
logger.debug(f"用户: {username}, 邮箱: {email[:3]}***")

# ❌ 错误：暴露敏感信息
logger.info(f"API Key: {api_key}")
logger.debug(f"密码: {password}")
```

### 5. 使用结构化日志

```python
# ✅ 正确：结构化信息
logger.info(
    "文档处理完成",
    extra={
        "file_path": file_path,
        "chunks": len(chunks),
        "duration": duration
    }
)

# 或使用 f-string
logger.info(
    f"文档处理完成: file={file_path}, "
    f"chunks={len(chunks)}, duration={duration}s"
)
```

## 项目中的日志使用

### 文档处理模块

```python
# src/document_processor/loader.py
logger.info(f"正在加载文档: {file_path}")
logger.debug(f"文档格式: {suffix}, 加载器: {loader_class.__name__}")
logger.info(f"成功加载 {len(documents)} 个文档片段")
```

### 检索模块

```python
# src/retrieval/retriever.py
logger.info(f"检索查询: {query[:50]}... (top_k={k})")
logger.debug(f"检索参数: k={k}, threshold={threshold}")
logger.info(f"检索到 {len(results)} 个相关文档片段")
```

### Agent 模块

```python
# src/agent/nodes.py
logger.info("[节点] 检索文档")
logger.debug(f"问题: {question}")
logger.info("[节点] 生成回答")
logger.debug(f"上下文长度: {len(context)} 字符")
```

## 日志文件管理

### 日志文件位置

```
logs/
├── chatbot.log          # 主日志文件
├── error.log            # 错误日志（可选）
└── debug.log            # 调试日志（可选）
```

### 日志轮转

建议使用 `RotatingFileHandler` 或 `TimedRotatingFileHandler`：

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "logs/chatbot.log",
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
```

### 日志清理

定期清理旧日志文件：

```bash
# 删除 30 天前的日志
find logs/ -name "*.log" -mtime +30 -delete
```

## 调试技巧

### 临时启用 DEBUG 级别

```bash
# 设置环境变量
export LOG_LEVEL=DEBUG

# 或在 .env 中修改
LOG_LEVEL=DEBUG
```

### 查看实时日志

```bash
# Linux/Mac
tail -f logs/chatbot.log

# Windows (PowerShell)
Get-Content logs/chatbot.log -Wait
```

### 过滤日志

```bash
# 只看错误
grep "ERROR" logs/chatbot.log

# 只看特定模块
grep "retrieval" logs/chatbot.log
```

## 常见错误

### ❌ 错误 1: 使用 print()

```python
# 错误
print(f"处理文档: {file_path}")

# 正确
logger.info(f"处理文档: {file_path}")
```

### ❌ 错误 2: 日志级别不当

```python
# 错误：调试信息用 INFO
logger.info(f"变量值: x={x}, y={y}")

# 正确：调试信息用 DEBUG
logger.debug(f"变量值: x={x}, y={y}")
```

### ❌ 错误 3: 缺少异常信息

```python
# 错误：丢失堆栈
try:
    process()
except Exception as e:
    logger.error(str(e))

# 正确：保留堆栈
try:
    process()
except Exception as e:
    logger.error(f"处理失败: {e}", exc_info=True)
```

### ❌ 错误 4: 过度日志

```python
# 错误：循环中大量日志
for i in range(10000):
    logger.info(f"处理第 {i} 项")  # 产生 10000 条日志！

# 正确：适度日志
logger.info(f"开始处理 {len(items)} 项")
for i, item in enumerate(items):
    if i % 1000 == 0:
        logger.debug(f"进度: {i}/{len(items)}")
logger.info("处理完成")
```

## 总结

1. **禁止使用 `print()`** - 所有调试信息必须使用 logger
2. **使用合适的日志级别** - DEBUG/INFO/WARNING/ERROR/CRITICAL
3. **包含足够的上下文** - 便于问题定位
4. **记录异常堆栈** - 使用 `exc_info=True`
5. **保护敏感信息** - 不要记录密码、密钥等
6. **适度日志** - 避免过度或不足
7. **结构化日志** - 便于分析和查询

遵循这些规范，确保日志系统的可控性、可配置性和可维护性。
