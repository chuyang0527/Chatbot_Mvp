"""文档检索器"""

from typing import List, Dict, Any
from langchain.schema import Document
from src.retrieval.vector_store import VectorStoreManager
from src.config import get_settings
from src.utils.logger import logger


class DocumentRetriever:
    """文档检索器，负责检索相关文档片段"""
    
    def __init__(self, vector_store: VectorStoreManager = None):
        """
        初始化检索器
        
        Args:
            vector_store: 向量存储管理器
        """
        self.vector_store = vector_store or VectorStoreManager()
        self.settings = get_settings()
    
    def retrieve(self, query: str, k: int = None) -> List[Document]:
        """
        检索相关文档
        
        Args:
            query: 查询文本
            k: 返回结果数量
            
        Returns:
            相关文档列表
        """
        k = k or self.settings.top_k
        logger.info(f"检索查询: {query[:50]}... (top_k={k})")
        
        results = self.vector_store.similarity_search(query, k=k)
        logger.info(f"检索到 {len(results)} 个相关文档片段")
        
        return results
    
    def format_context(self, documents: List[Document]) -> str:
        """
        格式化上下文
        
        Args:
            documents: 文档列表
            
        Returns:
            格式化后的上下文字符串
        """
        context_parts = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get('source', '未知来源')
            context_parts.append(f"[文档片段 {i}] (来源: {source})\n{doc.page_content}\n")
        
        return "\n".join(context_parts)
