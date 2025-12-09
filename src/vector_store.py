"""向量存储模块（兼容 LangChain 2025 最新版本）"""

import os
import shutil
from typing import List, Optional

from langchain_chroma import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

from config import Config

# 禁用 LangChain Telemetry（可选）
os.environ["LANGCHAIN_TELEMETRY"] = "false"


class VectorStore:
    """向量存储管理器"""

    def __init__(self):
        # 本地 embedding 模型（离线）
        # 优先使用本地模型，如果不存在则从 HuggingFace 下载
        local_model_path = Config.BASE_DIR / "model" / "paraphrase-multilingual-MiniLM-L12-v2"
        
        if local_model_path.exists():
            model_name = str(local_model_path)
            print(f"✓ 使用本地 Embedding 模型: {model_name}")
        else:
            model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
            print(f"ℹ 本地模型不存在，将从 HuggingFace 下载: {model_name}")
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        self.vectorstore: Optional[Chroma] = None
        self._load_or_create_vectorstore()

    def _load_or_create_vectorstore(self):
        """加载或创建向量存储"""

        try:
            self.vectorstore = Chroma(
                collection_name="rag_store",
                persist_directory=str(Config.VECTOR_DB_DIR),
                embedding_function=self.embeddings,
            )
            print(f"✓ 向量库已加载，文档片段数量：{self._count_docs()}")
        except Exception as e:
            print(f"向量库加载失败，重新创建: {e}")
            self.vectorstore = Chroma(
                collection_name="rag_store",
                persist_directory=str(Config.VECTOR_DB_DIR),
                embedding_function=self.embeddings,
            )

    def _count_docs(self) -> int:
        """更安全的统计方法"""
        try:
            col = self.vectorstore._client.get_collection("rag_store")
            return col.count()
        except:
            return 0

    def add_documents(self, documents: List[Document]) -> List[str]:
        """添加文档到向量库"""
        if not documents:
            return []

        ids = self.vectorstore.add_documents(documents)
        # self.vectorstore.persist()

        print(f"✓ 已添加 {len(documents)} 个文档片段（当前总数：{self._count_docs()}）")
        return ids

    def similarity_search(self, query: str, k: int = None) -> List[Document]:
        """相似度搜索"""
        if k is None:
            k = Config.RETRIEVAL_K

        return self.vectorstore.similarity_search(query, k=k)

    def clear(self):
        """清空所有向量"""
        print("⚠ 清空向量库...")
        shutil.rmtree(Config.VECTOR_DB_DIR, ignore_errors=True)
        self._load_or_create_vectorstore()
        print("✓ 向量库已重建")

    def get_retriever(self, k: int = None):
        """获取检索器"""
        if k is None:
            k = Config.RETRIEVAL_K

        return self.vectorstore.as_retriever(search_kwargs={"k": k})
