"""向量化处理器"""

from typing import List
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.utils.logger import logger


class Vectorizer:
    """向量化处理器，将文本转换为向量"""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        初始化向量化器
        
        Args:
            model_name: 嵌入模型名称
        """
        logger.info(f"正在加载嵌入模型: {model_name}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        logger.info("嵌入模型加载完成")
    
    def get_embeddings(self):
        """获取嵌入模型实例"""
        return self.embeddings
