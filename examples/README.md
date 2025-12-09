# 示例代码

本目录包含聊天机器人 RAG 系统的使用示例。

## 文件说明

- `example_usage.py` - 基础使用示例

## 运行示例

### 前置要求

确保已经：
1. 安装了依赖（`make install` 或 `uv sync`）
2. 启动了 Ollama 服务
3. 下载了必要的模型

### 运行方式

```bash
# 使用 uv
uv run python examples/example_usage.py

# 或直接运行
python examples/example_usage.py
```

## 示例内容

### 1. 配置管理
展示如何访问和使用系统配置。

### 2. 文档处理
演示如何处理不同格式的文档。

### 3. 基础使用
完整的工作流程：
- 创建文档
- 处理和向量化
- 提问和回答
- 多轮对话

### 4. 向量检索
展示如何进行相似度搜索。

## 自定义示例

你可以基于这些示例创建自己的应用：

```python
from src.config import Config
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore
from src.chat_agent import ChatAgent

# 初始化
Config.ensure_directories()
doc_processor = DocumentProcessor()
vector_store = VectorStore()
chat_agent = ChatAgent(vector_store)

# 处理文档
documents = doc_processor.load_document("your_file.pdf")
vector_store.add_documents(documents)

# 提问
result = chat_agent.chat("你的问题")
print(result['answer'])
```

## 更多示例

查看 [文档](../docs/) 了解更多使用方式。
