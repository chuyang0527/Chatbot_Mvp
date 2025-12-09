# 贡献指南

感谢你对本项目的关注！本文档将帮助你了解如何参与项目开发。

## 开发流程

### 1. Fork 和 Clone

```bash
# Fork 项目到你的 GitHub 账号
# 然后 clone 到本地
git clone https://github.com/YOUR_USERNAME/chatbot-rag.git
cd chatbot-rag
```

### 2. 创建功能分支

遵循命名规范：

- `feat/功能名称` - 新功能
- `fix/问题描述` - Bug 修复
- `docs/文档说明` - 文档更新
- `refactor/重构说明` - 代码重构
- `test/测试说明` - 测试相关
- `chore/任务说明` - 构建/工具相关

```bash
# 示例
git checkout -b feat/upload-handler
git checkout -b fix/vector-search-bug
git checkout -b docs/api-documentation
```

### 3. 开发和提交

#### 提交信息规范（Conventional Commits）

格式：`<type>(<scope>): <subject>`

**Type 类型：**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

**示例：**
```bash
git commit -m "feat(upload): 添加批量文档上传功能"
git commit -m "fix(vector): 修复相似度搜索空指针异常"
git commit -m "docs(readme): 更新安装步骤说明"
git commit -m "refactor(agent): 优化对话历史管理逻辑"
```

### 4. 推送和创建 Pull Request

```bash
# 推送到你的 fork
git push origin feat/upload-handler

# 在 GitHub 上创建 Pull Request
# 标题：简洁描述（如：添加批量文档上传功能）
# 描述：详细说明改动内容、原因、测试情况
```

#### Pull Request 模板

```markdown
## 改动说明
简要描述本次改动的内容和目的

## 改动类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 文档更新
- [ ] 代码重构
- [ ] 性能优化
- [ ] 其他

## 测试情况
- [ ] 本地测试通过
- [ ] 添加了单元测试
- [ ] 更新了文档

## 相关 Issue
Closes #issue_number

## 截图（如适用）
```

### 5. 代码审查

- 等待维护者审查
- 根据反馈修改代码
- 保持分支与主分支同步

```bash
# 同步主分支
git fetch upstream
git rebase upstream/main
```

## 开发规范

### 代码风格

使用 Black 和 Ruff 进行代码格式化和检查：

```bash
# 格式化代码
uv run black src/

# 检查代码质量
uv run ruff check src/
```

### 类型提示

尽量使用类型提示：

```python
from typing import List, Optional

def process_documents(files: List[str]) -> Optional[dict]:
    """处理文档列表"""
    pass
```

### 文档字符串

使用清晰的文档字符串：

```python
def similarity_search(query: str, k: int = 4) -> List[Document]:
    """
    执行相似度搜索
    
    Args:
        query: 查询文本
        k: 返回结果数量
        
    Returns:
        相关文档列表
        
    Raises:
        ValueError: 当 k 小于 1 时
    """
    pass
```

### 测试

为新功能添加测试：

```python
# tests/test_vector_store.py
def test_add_documents():
    """测试文档添加功能"""
    store = VectorStore()
    docs = [Document(page_content="test")]
    ids = store.add_documents(docs)
    assert len(ids) == 1
```

## 本地开发环境

### 安装依赖

```bash
# 使用 uv
uv sync

# 或使用 pip
pip install -e ".[dev]"
```

### 运行测试

```bash
uv run pytest tests/ -v
```

### 启动开发服务

```bash
# 使用 Docker Compose
docker-compose up -d

# 或本地运行
uv run python src/main.py
```

## 发布流程

### 版本号规范（Semantic Versioning）

- `MAJOR.MINOR.PATCH` (如 1.2.3)
- MAJOR: 不兼容的 API 改动
- MINOR: 向后兼容的新功能
- PATCH: 向后兼容的 Bug 修复

### 发布步骤

1. 更新版本号（`pyproject.toml`）
2. 更新 CHANGELOG.md
3. 创建 Git tag
4. 推送 tag 触发 CI/CD

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## 问题反馈

### 提交 Issue

使用 Issue 模板，包含：
- 问题描述
- 复现步骤
- 预期行为
- 实际行为
- 环境信息（OS、Python 版本等）

### 功能请求

- 清晰描述需求
- 说明使用场景
- 提供示例（如适用）

## 行为准则

- 尊重所有贡献者
- 保持友好和专业
- 接受建设性批评
- 关注项目最佳利益

## 联系方式

- GitHub Issues: 项目问题和讨论
- Pull Requests: 代码贡献
- Discussions: 一般性讨论

感谢你的贡献！🎉
