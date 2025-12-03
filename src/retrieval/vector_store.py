"""向量存储管理"""

from typing import List, Optional
from pathlib import Path
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from src.document_processor.vectorizer import Vectorizer
from src.config import get_settings
from src.utils.logger import logger


class VectorStoreManager:
    """向量存储管理器"""
    
    def __init__(self, persist_directory: Optional[str] = None):
        """
        初始化向量存储管理器
        
        Args:
            persist_directory: 持久化目录
        """
        settings = get_settings()
        self.persist_directory = persist_directory or settings.vector_db_path
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        
        self.vectorizer = Vectorizer()
        self.vector_store = None
        self._load_or_create()
    
    def _load_or_create(self):
        """加载或创建向量存储"""
        try:
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.vectorizer.get_embeddings()
            )
            logger.info(f"向量存储已加载: {self.persist_directory}")
        except Exception as e:
            logger.warning(f"加载向量存储失败，将创建新的: {e}")
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.vectorizer.get_embeddings()
            )
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """
        添加文档到向量存储
        
        Args:
            documents: 文档列表
            
        Returns:
            文档 ID 列表
        """
        logger.info(f"正在添加 {len(documents)} 个文档到向量存储")
        ids = self.vector_store.add_documents(documents)
        logger.info(f"成功添加 {len(ids)} 个文档")
        return ids
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        相似度搜索
        
        Args:
            query: 查询文本
            k: 返回结果数量
            
        Returns:
            相关文档列表
        """
        return self.vector_store.similarity_search(query, k=k)
    
    def get_retriever(self, k: int = 4):
        """获取检索器"""
        return self.vector_store.as_retriever(search_kwargs={"k": k})
