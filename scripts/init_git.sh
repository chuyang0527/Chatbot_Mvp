#!/bin/bash
# Git 初始化脚本

echo "🚀 初始化 Git 仓库..."

# 初始化 Git
git init

# 添加所有文件
git add .

# 首次提交
git commit -m "feat: 初始化聊天机器人 MVP 项目

- 实现文档上传与处理（PDF/Word/MD/TXT）
- 实现向量检索与问答
- 实现多轮对话能力
- 集成 LangSmith 可观测性
- 使用 LangGraph + LangChain + Chroma
- 使用 uv 管理依赖"

echo "✅ Git 仓库初始化完成！"
echo ""
echo "下一步："
echo "1. 在 GitHub/Gitee/GitCode 创建远程仓库"
echo "2. 运行: git remote add origin <your-repo-url>"
echo "3. 运行: git push -u origin main"
