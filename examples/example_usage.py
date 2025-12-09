#!/usr/bin/env python3
"""
示例：如何使用聊天机器人 RAG 系统

这个脚本展示了如何以编程方式使用系统的各个组件。
"""

import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import Config
from document_processor import DocumentProcessor
from vector_store import VectorStore
from chat_agent import ChatAgent


def example_basic_usage():
    """基础使用示例"""
    print("=" * 60)
    print("示例 1: 基础使用")
    print("=" * 60)
    
    # 初始化配置
    Config.ensure_directories()
    
    # 初始化组件
    doc_processor = DocumentProcessor()
    vector_store = VectorStore()
    chat_agent = ChatAgent(vector_store)
    
    # 创建示例文档
    example_text = """
    人工智能（AI）是计算机科学的一个分支，致力于创建能够执行
    通常需要人类智能的任务的系统。这包括学习、推理、问题解决、
    感知和语言理解等能力。
    
    机器学习是人工智能的一个子领域，它使计算机能够从数据中学习
    而无需明确编程。深度学习是机器学习的一个分支，使用神经网络
    来模拟人脑的工作方式。
    """
    
    # 保存示例文档
    example_file = Config.UPLOAD_DIR / "example_ai.txt"
    example_file.write_text(example_text, encoding="utf-8")
    
    # 处理文档
    print("\n1. 处理文档...")
    documents = doc_processor.load_document(str(example_file))
    print(f"   文档被分成 {len(documents)} 个片段")
    
    # 添加到向量库
    print("\n2. 添加到向量库...")
    vector_store.add_documents(documents)
    
    # 提问
    print("\n3. 提问...")
    query = "什么是人工智能？"
    print(f"   问题: {query}")
    
    result = chat_agent.chat(query)
    print(f"   回答: {result['answer']}")
    
    # 多轮对话
    print("\n4. 多轮对话...")
    query2 = "机器学习和深度学习有什么关系？"
    print(f"   问题: {query2}")
    
    result2 = chat_agent.chat(query2)
    print(f"   回答: {result2['answer']}")


def example_document_processing():
    """文档处理示例"""
    print("\n" + "=" * 60)
    print("示例 2: 文档处理")
    print("=" * 60)
    
    doc_processor = DocumentProcessor()
    
    # 创建不同类型的示例文档
    examples = {
        "txt": "这是一个文本文件示例。",
        "md": "# Markdown 示例\n\n这是一个 **Markdown** 文件。",
    }
    
    for ext, content in examples.items():
        file_path = Config.UPLOAD_DIR / f"example.{ext}"
        file_path.write_text(content, encoding="utf-8")
        
        print(f"\n处理 {ext.upper()} 文件...")
        try:
            docs = doc_processor.load_document(str(file_path))
            print(f"✓ 成功处理，生成 {len(docs)} 个片段")
        except Exception as e:
            print(f"✗ 处理失败: {e}")


def example_vector_search():
    """向量检索示例"""
    print("\n" + "=" * 60)
    print("示例 3: 向量检索")
    print("=" * 60)
    
    vector_store = VectorStore()
    
    # 检索示例
    query = "人工智能"
    print(f"\n检索查询: {query}")
    
    results = vector_store.similarity_search(query, k=2)
    
    print(f"找到 {len(results)} 个相关片段:")
    for i, doc in enumerate(results, 1):
        print(f"\n片段 {i}:")
        print(f"  来源: {doc.metadata.get('source', '未知')}")
        print(f"  内容: {doc.page_content[:100]}...")


def example_configuration():
    """配置示例"""
    print("\n" + "=" * 60)
    print("示例 4: 配置管理")
    print("=" * 60)
    
    print("\n当前配置:")
    print(f"  基础目录: {Config.BASE_DIR}")
    print(f"  上传目录: {Config.UPLOAD_DIR}")
    print(f"  向量库目录: {Config.VECTOR_DB_DIR}")
    print(f"  Ollama URL: {Config.OLLAMA_BASE_URL}")
    print(f"  Ollama 模型: {Config.OLLAMA_MODEL}")
    print(f"  LLM 温度: {Config.LLM_TEMPERATURE}")
    print(f"  块大小: {Config.CHUNK_SIZE}")
    print(f"  块重叠: {Config.CHUNK_OVERLAP}")
    print(f"  检索数量: {Config.RETRIEVAL_K}")


def main():
    """主函数"""
    print("\n聊天机器人 RAG 系统 - 使用示例\n")
    
    try:
        # 运行示例
        example_configuration()
        example_document_processing()
        example_basic_usage()
        example_vector_search()
        
        print("\n" + "=" * 60)
        print("所有示例运行完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
