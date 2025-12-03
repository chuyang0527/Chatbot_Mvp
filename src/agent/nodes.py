"""Agent 节点定义"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.agent.state import AgentState
from src.retrieval.retriever import DocumentRetriever
from src.config import get_settings
from src.utils.logger import logger


class AgentNodes:
    """Agent 节点集合"""
    
    def __init__(self):
        settings = get_settings()
        self.retriever = DocumentRetriever()
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0.7,
            api_key=settings.openai_api_key
        )
    
    def retrieve_documents(self, state: AgentState) -> Dict[str, Any]:
        """检索相关文档节点"""
        question = state["question"]
        logger.info(f"[节点] 检索文档: {question[:50]}...")
        
        documents = self.retriever.retrieve(question)
        context = self.retriever.format_context(documents)
        
        # 提取引用信息
        citations = []
        for i, doc in enumerate(documents, 1):
            citations.append({
                "index": i,
                "content": doc.page_content[:200] + "...",
                "source": doc.metadata.get("source", "未知"),
                "page": doc.metadata.get("page", "N/A")
            })
        
        return {
            "retrieved_documents": documents,
            "context": context,
            "citations": citations
        }
    
    def generate_answer(self, state: AgentState) -> Dict[str, Any]:
        """生成回答节点"""
        logger.info("[节点] 生成回答")
        
        question = state["question"]
        context = state.get("context", "")
        chat_history = state.get("chat_history", [])
        
        # 构建提示词
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的文档问答助手。请基于提供的文档内容回答用户问题。

要求：
1. 仅基于提供的文档内容回答，不要编造信息
2. 在回答中明确引用文档片段，使用 [文档片段 X] 的格式
3. 如果文档中没有相关信息，请明确告知用户
4. 保持回答简洁、准确、有条理
5. 考虑对话历史，提供连贯的回答

文档内容：
{context}

对话历史：
{history}"""),
            ("human", "{question}")
        ])
        
        # 格式化历史记录
        history_text = "\n".join([
            f"用户: {h['question']}\n助手: {h['answer']}"
            for h in chat_history[-3:]  # 只保留最近3轮对话
        ]) if chat_history else "无"
        
        # 生成回答
        chain = prompt | self.llm
        response = chain.invoke({
            "context": context,
            "history": history_text,
            "question": question
        })
        
        answer = response.content
        logger.info(f"[节点] 回答生成完成: {answer[:100]}...")
        
        return {"answer": answer}
