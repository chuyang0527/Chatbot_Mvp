"""文本分段器"""

from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from src.config import get_settings
from src.utils.logger import logger


class TextSplitter:
    """文本分段器，将长文档切分为小片段"""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        settings = get_settings()
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""]
        )
    
    def split(self, documents: List[Document]) -> List[Document]:
        """
        分割文档
        
        Args:
            documents: 原始文档列表
            
        Returns:
            分割后的文档片段列表
        """
        logger.info(f"开始分割文档，chunk_size={self.chunk_size}, overlap={self.chunk_overlap}")
        chunks = self.splitter.split_documents(documents)
        logger.info(f"文档分割完成，共 {len(chunks)} 个片段")
        return chunks
