"""文档处理模块测试"""

import pytest
from pathlib import Path
from src.document_processor import DocumentProcessor


@pytest.fixture
def processor():
    """创建文档处理器实例"""
    return DocumentProcessor()


def test_processor_initialization(processor):
    """测试处理器初始化"""
    assert processor.text_splitter is not None
    assert processor.text_splitter.chunk_size > 0


def test_unsupported_file_format(processor):
    """测试不支持的文件格式"""
    with pytest.raises(ValueError):
        processor.load_document("test.xyz")


def test_file_not_found(processor):
    """测试文件不存在"""
    with pytest.raises(FileNotFoundError):
        processor.load_document("nonexistent.pdf")
