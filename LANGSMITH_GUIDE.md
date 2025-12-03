# LangSmith 可观测性指南

## 什么是 LangSmith？

LangSmith 是 LangChain 官方提供的可观测性和调试平台，用于追踪、监控和调试 LLM 应用。

## 配置步骤

### 1. 注册 LangSmith 账号

访问 [https://smith.langchain.com/](https://smith.langchain.com/) 注册账号。

### 2. 获取 API Key

1. 登录后，点击右上角头像
2. 选择 "Settings" -> "API Keys"
3. 点击 "Create API Key"
4. 复制生成的 API Key

### 3. 配置环境变量

在 `.env` 文件中添加：

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=chatbot-mvp
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

## 使用方法

### 自动追踪

配置完成后，所有的 LangChain 调用都会自动上报到 LangSmith。

### 查看调用链

1. 访问 [https://smith.langchain.com/](https://smith.langchain.com/)
2. 选择你的项目（如 `chatbot-mvp`）
3. 查看 "Traces" 标签页

### 调用链包含的信息

- **输入输出**: 每个节点的输入和输出数据
- **延迟**: 每个步骤的执行时间
- **Token 使用**: LLM 调用的 token 消耗
- **错误信息**: 如果有错误，会显示详细的堆栈信息
- **元数据**: 模型参数、温度等配置信息

## 典型调用链示例

一个完整的问答流程包含以下步骤：

```
1. ChatbotGraph.run
   ├── 2. retrieve_documents (检索节点)
   │   ├── 向量检索
   │   └── 格式化上下文
   └── 3. generate_answer (生成节点)
       ├── 构建提示词
       ├── LLM 调用 (OpenAI)
       └── 返回回答
```

## 截图说明

运行示例后，在 LangSmith 控制台可以看到：

1. **Traces 列表**: 显示所有的调用记录
2. **详细视图**: 点击某个 trace 可以看到完整的调用链
3. **性能指标**: 延迟、token 使用等统计信息
4. **输入输出**: 每个步骤的详细数据

## 调试技巧

### 1. 查看检索结果

在 `retrieve_documents` 节点中可以看到：
- 检索到的文档片段
- 相似度分数
- 文档来源

### 2. 分析 LLM 调用

在 `generate_answer` 节点中可以看到：
- 完整的提示词
- LLM 的原始响应
- Token 消耗统计

### 3. 性能优化

通过 LangSmith 可以：
- 识别慢速节点
- 优化提示词长度
- 调整检索参数

## 常见问题

### Q: 为什么看不到追踪数据？

A: 检查以下几点：
1. 确认 `LANGCHAIN_TRACING_V2=true`
2. 确认 API Key 正确
3. 确认网络连接正常

### Q: 如何关闭追踪？

A: 设置 `LANGCHAIN_TRACING_V2=false` 或删除该环境变量。

### Q: 数据会保存多久？

A: 免费版保存 14 天，付费版可以保存更长时间。

## 最佳实践

1. **使用有意义的项目名称**: 便于区分不同的应用
2. **添加标签**: 可以为不同的运行添加标签，便于筛选
3. **定期查看**: 定期检查性能指标，及时发现问题
4. **保护敏感信息**: 注意不要在追踪中暴露敏感数据

## 参考资源

- [LangSmith 官方文档](https://docs.smith.langchain.com/)
- [LangChain 追踪指南](https://python.langchain.com/docs/langsmith/walkthrough)
