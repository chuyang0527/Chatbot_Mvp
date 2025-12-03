"""检索模块测试"""

import pytest
from langchain.schema import Document
from src.retrieval import VectorStoreManager


@pytest.fixture
def sample_documents():
    """示例文档"""
    return [
        Document(page_content="人工智能是计算机科学的一个分支。", metadata={"source": "test1"}),
        Document(page_content="机器学习是人工智能的子领域。", metadata={"source": "test2"}),
        Document(page_content="深度学习使用神经网络。", metadata={"source": "test3"}),
    ]


def test_vector_store_add_documents(tmp_path, sample_documents):
    """测试添加文档到向量存储"""
    vector_store = VectorStoreManager(persist_directory=str(tmp_path / "test_db"))
    
    ids = vector_store.add_documents(sample_documents)
    
    assert len(ids) == len(sample_documents)


def test_vector_store_similarity_search(tmp_path, sample_documents):
    """测试相似度搜索"""
    vector_store = VectorStoreManager(persist_directory=str(tmp_path / "test_db"))
    vector_store.add_documents(sample_documents)
    
    results = vector_store.similarity_search("什么是人工智能", k=2)
    
    assert len(results) <= 2
    assert any("人工智能" in doc.page_content for doc in results)
