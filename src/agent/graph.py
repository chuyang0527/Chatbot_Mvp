"""LangGraph 状态图定义"""

from langgraph.graph import StateGraph, END
from src.agent.state import AgentState
from src.agent.nodes import AgentNodes
from src.utils.logger import logger


class ChatbotGraph:
    """聊天机器人状态图"""
    
    def __init__(self):
        self.nodes = AgentNodes()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """构建状态图"""
        logger.info("构建 LangGraph 状态图")
        
        # 创建状态图
        workflow = StateGraph(AgentState)
        
        # 添加节点
        workflow.add_node("retrieve", self.nodes.retrieve_documents)
        workflow.add_node("generate", self.nodes.generate_answer)
        
        # 设置入口点
        workflow.set_entry_point("retrieve")
        
        # 添加边
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)
        
        # 编译图
        app = workflow.compile()
        logger.info("状态图构建完成")
        
        return app
    
    def run(self, question: str, chat_history: list = None) -> dict:
        """
        运行状态图
        
        Args:
            question: 用户问题
            chat_history: 对话历史
            
        Returns:
            包含回答和引用的字典
        """
        initial_state = {
            "question": question,
            "chat_history": chat_history or [],
            "retrieved_documents": [],
            "context": "",
            "answer": "",
            "citations": []
        }
        
        logger.info(f"开始处理问题: {question}")
        result = self.graph.invoke(initial_state)
        logger.info("问题处理完成")
        
        return {
            "answer": result["answer"],
            "citations": result["citations"],
            "question": question
        }
