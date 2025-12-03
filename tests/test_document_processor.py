"""文档处理模块测试"""

import pytest
from pathlib import Path
from src.document_processor import DocumentLoader, TextSplitter


def test_document_loader_txt(tmp_path):
    """测试文本文件加载"""
    # 创建临时文件
    test_file = tmp_path / "test.txt"
    test_file.write_text("这是一个测试文档。", encoding="utf-8")
    
    # 加载文档
    documents = DocumentLoader.load(str(test_file))
    
    assert len(documents) > 0
    assert "测试文档" in documents[0].page_content


def test_document_loader_unsupported_format(tmp_path):
    """测试不支持的文件格式"""
    test_file = tmp_path / "test.xyz"
    test_file.write_text("test", encoding="utf-8")
    
    with pytest.raises(ValueError):
        DocumentLoader.load(str(test_file))


def test_text_splitter():
    """测试文本分割"""
    from langchain.schema import Document
    
    # 创建测试文档
    long_text = "这是一段很长的文本。" * 100
    documents = [Document(page_content=long_text)]
    
    # 分割文档
    splitter = TextSplitter(chunk_size=100, chunk_overlap=20)
    chunks = splitter.split(documents)
    
    assert len(chunks) > 1
    assert all(len(chunk.page_content) <= 150 for chunk in chunks)
