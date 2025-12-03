# 项目结构说明

## 目录结构

```
chatbot-mvp/
├── src/                          # 源代码目录
│   ├── __init__.py              # 包初始化
│   ├── main.py                  # 主程序入口（交互式聊天）
│   ├── config.py                # 配置管理（环境变量、设置）
│   ├── upload_document.py       # 文档上传工具
│   │
│   ├── document_processor/      # 文档处理模块
│   │   ├── __init__.py
│   │   ├── loader.py           # 文档加载器（支持 PDF/Word/MD/TXT）
│   │   ├── splitter.py         # 文本分段器（智能切分）
│   │   └── vectorizer.py       # 向量化处理器（嵌入模型）
│   │
│   ├── retrieval/               # 检索模块
│   │   ├── __init__.py
│   │   ├── vector_store.py     # 向量存储管理（Chroma）
│   │   └── retriever.py        # 文档检索器（相似度搜索）
│   │
│   ├── agent/                   # Agent 模块（LangGraph）
│   │   ├── __init__.py
│   │   ├── graph.py            # 状态图定义（工作流）
│   │   ├── nodes.py            # 图节点实现（检索、生成）
│   │   └── state.py            # 状态管理（对话状态）
│   │
│   └── utils/                   # 工具函数
│       ├── __init__.py
│       └── logger.py           # 日志工具（Rich 格式化）
│
├── data/                        # 数据目录
│   ├── documents/              # 上传的文档存储
│   │   └── .gitkeep
│   └── vector_db/              # 向量数据库存储（Chroma）
│       └── .gitkeep
│
├── examples/                    # 示例代码
│   ├── __init__.py
│   └── demo.py                 # 完整使用示例
│
├── tests/                       # 测试文件
│   └── __init__.py
│
├── .env.example                 # 环境变量模板
├── .gitignore                   # Git 忽略文件
├── requirements.txt             # Python 依赖列表
├── pyproject.toml              # uv 项目配置
├── README.md                    # 项目说明文档
├── QUICKSTART.md               # 快速开始指南
├── CONTRIBUTING.md             # 贡献指南
├── DEPLOYMENT.md               # 部署指南
├── LANGSMITH_GUIDE.md          # LangSmith 使用指南
└── PROJECT_STRUCTURE.md        # 本文件
```

## 核心模块说明

### 1. 文档处理模块 (`document_processor/`)

负责文档的加载、处理和向量化。

#### `loader.py` - 文档加载器
- 支持多种文档格式（PDF、Word、Markdown、TXT）
- 自动选择合适的加载器
- 提取文本内容

#### `splitter.py` - 文本分段器
- 智能文本切分
- 支持自定义 chunk_size 和 overlap
- 保留文档元数据

#### `vectorizer.py` - 向量化处理器
- 使用 HuggingFace 嵌入模型
- 将文本转换为向量表示
- 支持自定义模型

### 2. 检索模块 (`retrieval/`)

负责向量存储和文档检索。

#### `vector_store.py` - 向量存储管理
- 管理 Chroma 向量数据库
- 添加和持久化文档
- 提供检索接口

#### `retriever.py` - 文档检索器
- 基于向量相似度检索
- 格式化检索结果
- 支持 Top-K 检索

### 3. Agent 模块 (`agent/`)

基于 LangGraph 的智能 Agent 实现。

#### `state.py` - 状态定义
- 定义对话状态结构
- 包含问题、历史、文档、回答等

#### `nodes.py` - 节点实现
- `retrieve_documents`: 检索相关文档
- `generate_answer`: 生成回答
- 集成 LLM 调用

#### `graph.py` - 状态图
- 定义工作流程
- 连接各个节点
- 管理状态转换

### 4. 工具模块 (`utils/`)

#### `logger.py` - 日志工具
- 使用 Rich 库美化输出
- 统一日志格式
- 支持多级别日志

### 5. 配置模块 (`config.py`)

- 使用 Pydantic 管理配置
- 从环境变量加载设置
- 提供类型安全的配置访问

## 数据流程

```
1. 文档上传
   └─> DocumentLoader.load()
       └─> TextSplitter.split()
           └─> VectorStoreManager.add_documents()

2. 用户提问
   └─> ChatbotGraph.run()
       ├─> retrieve_documents (节点)
       │   └─> DocumentRetriever.retrieve()
       │       └─> VectorStoreManager.similarity_search()
       └─> generate_answer (节点)
           └─> ChatOpenAI (LLM 调用)
               └─> 返回回答和引用
```

## 关键技术

### LangChain
- 文档加载和处理
- LLM 集成
- 提示词模板

### LangGraph
- 状态图管理
- 工作流编排
- 节点定义

### LangSmith
- 调用链追踪
- 性能监控
- 调试工具

### Chroma
- 向量数据库
- 相似度搜索
- 本地持久化

### HuggingFace
- 嵌入模型
- 文本向量化

## 扩展点

### 添加新的文档格式

在 `loader.py` 中添加新的加载器：

```python
SUPPORTED_FORMATS = {
    '.pdf': PyPDFLoader,
    '.docx': Docx2txtLoader,
    '.md': UnstructuredMarkdownLoader,
    '.txt': TextLoader,
    '.html': UnstructuredHTMLLoader,  # 新增
}
```

### 更换向量数据库

修改 `vector_store.py`，替换 Chroma 为其他向量数据库：

```python
from langchain_community.vectorstores import Pinecone
# 或 Weaviate, Qdrant, Milvus 等
```

### 添加新的 Agent 节点

在 `nodes.py` 中添加新节点，在 `graph.py` 中连接：

```python
def new_node(self, state: AgentState) -> Dict[str, Any]:
    # 实现新功能
    pass

# 在 graph.py 中
workflow.add_node("new_node", self.nodes.new_node)
workflow.add_edge("retrieve", "new_node")
workflow.add_edge("new_node", "generate")
```

### 自定义 LLM

在 `nodes.py` 中更换 LLM：

```python
from langchain_anthropic import ChatAnthropic
self.llm = ChatAnthropic(model="claude-3-opus-20240229")
```

## 配置文件

### `.env` - 环境变量
- API Keys
- 模型配置
- 路径配置

### `pyproject.toml` - 项目配置
- 依赖管理
- 项目元数据
- 脚本定义

### `requirements.txt` - 依赖列表
- 所有 Python 包
- 版本锁定

## 最佳实践

1. **模块化设计**: 每个模块职责单一
2. **配置外部化**: 使用环境变量
3. **日志记录**: 关键步骤都有日志
4. **错误处理**: 完善的异常处理
5. **类型提示**: 使用 Python 类型注解
6. **文档字符串**: 所有函数都有说明

## 性能考虑

- **向量数据库**: 使用持久化避免重复加载
- **嵌入模型**: 首次加载较慢，后续复用
- **LLM 调用**: 主要性能瓶颈，考虑缓存
- **文档分段**: chunk_size 影响检索质量和速度

## 安全注意事项

- **API Keys**: 不要提交到 Git
- **敏感数据**: 注意文档内容隐私
- **输入验证**: 验证用户输入
- **访问控制**: 生产环境需要认证
