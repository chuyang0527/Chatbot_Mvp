"""文档加载器 - 支持多种文档格式"""

from pathlib import Path
from typing import List
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredMarkdownLoader
)
from langchain.schema import Document
from src.utils.logger import logger


class DocumentLoader:
    """文档加载器，支持 PDF、Word、Markdown、TXT"""
    
    SUPPORTED_FORMATS = {
        '.pdf': PyPDFLoader,
        '.docx': Docx2txtLoader,
        '.md': UnstructuredMarkdownLoader,
        '.txt': TextLoader,
    }
    
    @classmethod
    def load(cls, file_path: str) -> List[Document]:
        """
        加载文档
        
        Args:
            file_path: 文档路径
            
        Returns:
            文档列表
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        suffix = path.suffix.lower()
        if suffix not in cls.SUPPORTED_FORMATS:
            raise ValueError(
                f"不支持的文件格式: {suffix}. "
                f"支持的格式: {', '.join(cls.SUPPORTED_FORMATS.keys())}"
            )
        
        loader_class = cls.SUPPORTED_FORMATS[suffix]
        loader = loader_class(str(path))
        
        logger.info(f"正在加载文档: {file_path}")
        documents = loader.load()
        logger.info(f"成功加载 {len(documents)} 个文档片段")
        
        return documents
