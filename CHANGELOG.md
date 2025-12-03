# 更新日志

所有重要的项目变更都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 计划功能
- Web UI 界面
- 多用户会话管理
- 更多文档格式支持
- 缓存机制优化
- 异步处理支持

## [0.1.0] - 2024-12-03

### 新增
- 文档上传与处理功能
  - 支持 PDF、Word、Markdown、TXT 格式
  - 智能文本分段
  - 向量化存储
- 检索与问答功能
  - 基于向量相似度的语义检索
  - LLM 生成回答
  - 显式引用原文段落
- 多轮对话能力
  - 上下文管理
  - 对话历史追踪
  - 连续提问支持
- 可观测性
  - LangSmith 集成
  - 调用链追踪
  - 性能监控
- 工程化
  - uv 依赖管理
  - 完整的项目文档
  - 示例代码
  - 单元测试

### 技术栈
- LangGraph: 状态图管理
- LangChain: LLM 集成
- LangSmith: 可观测性
- Chroma: 向量数据库
- HuggingFace: 嵌入模型
- OpenAI: LLM 服务

### 文档
- README.md: 项目说明
- QUICKSTART.md: 快速开始指南
- DEPLOYMENT.md: 部署指南
- LANGSMITH_GUIDE.md: LangSmith 使用指南
- PROJECT_STRUCTURE.md: 项目结构说明
- CONTRIBUTING.md: 贡献指南

[未发布]: https://github.com/your-repo/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/your-repo/releases/tag/v0.1.0
