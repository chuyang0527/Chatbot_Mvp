"""完整使用示例"""

import os
from pathlib import Path
from dotenv import load_dotenv
from src.document_processor import DocumentLoader, TextSplitter
from src.retrieval import VectorStoreManager
from src.agent.graph import ChatbotGraph
from src.utils.logger import logger

load_dotenv()


def demo():
    """演示完整流程"""
    
    logger.info("=" * 60)
    logger.info("🚀 聊天机器人 MVP 演示")
    logger.info("=" * 60)
    
    # 1. 创建示例文档
    logger.info("\n步骤 1: 创建示例文档")
    sample_doc_path = "data/documents/sample.txt"
    Path("data/documents").mkdir(parents=True, exist_ok=True)
    
    sample_content = """
# 人工智能简介

人工智能（Artificial Intelligence，简称AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。

## 主要应用领域

1. 自然语言处理：使计算机能够理解、解释和生成人类语言
2. 计算机视觉：使计算机能够识别和处理图像和视频
3. 机器学习：使计算机能够从数据中学习并改进性能
4. 机器人技术：创建能够在物理世界中执行任务的智能机器

## 发展历史

人工智能的概念最早可以追溯到1950年代，当时艾伦·图灵提出了著名的"图灵测试"。
在接下来的几十年里，AI经历了多次繁荣和低谷期。

## 当前趋势

近年来，深度学习技术的突破推动了AI的快速发展。大型语言模型（如GPT系列）展示了令人印象深刻的能力。

## 未来展望

AI技术将继续在医疗、教育、交通等领域发挥重要作用，但同时也需要关注伦理和安全问题。
    """
    
    with open(sample_doc_path, "w", encoding="utf-8") as f:
        f.write(sample_content)
    logger.info(f"✓ 示例文档已创建: {sample_doc_path}")
    
    # 2. 加载和处理文档
    logger.info("\n步骤 2: 加载和处理文档")
    documents = DocumentLoader.load(sample_doc_path)
    logger.info("✓ 文档加载完成")
    
    # 3. 分割文档
    logger.info("\n步骤 3: 分割文档")
    splitter = TextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split(documents)
    logger.info(f"✓ 文档分割完成，共 {len(chunks)} 个片段")
    
    # 4. 向量化存储
    logger.info("\n步骤 4: 向量化并存储")
    vector_store = VectorStoreManager()
    vector_store.add_documents(chunks)
    logger.info("✓ 文档已添加到向量数据库")
    
    # 5. 创建聊天机器人
    logger.info("\n步骤 5: 初始化聊天机器人")
    chatbot = ChatbotGraph()
    logger.info("✓ 聊天机器人已就绪")
    
    # 6. 测试问答
    logger.info("\n步骤 6: 测试问答功能")
    logger.info("-" * 60)
    
    test_questions = [
        "什么是人工智能？",
        "AI有哪些主要应用领域？",
        "谁提出了图灵测试？",
    ]
    
    chat_history = []
    for i, question in enumerate(test_questions, 1):
        logger.info(f"\n问题 {i}: {question}")
        
        result = chatbot.run(question, chat_history)
        
        logger.info(f"回答: {result['answer']}")
        logger.info(f"引用数量: {len(result['citations'])}")
        
        # 显示引用详情
        if result['citations']:
            logger.debug("引用详情:")
            for cite in result['citations']:
                logger.debug(f"  [{cite['index']}] {cite['source']} - {cite['content'][:80]}...")
        
        chat_history.append({
            "question": question,
            "answer": result["answer"]
        })
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 演示完成！")
    logger.info("=" * 60)
    logger.info("\n提示：")
    logger.info("- 查看 LangSmith 控制台可以看到完整的调用链追踪")
    logger.info("- 运行 'uv run python src/main.py' 启动交互式聊天")
    logger.info("- 运行 'uv run python src/upload_document.py --file <path>' 上传新文档")


if __name__ == "__main__":
    demo()
