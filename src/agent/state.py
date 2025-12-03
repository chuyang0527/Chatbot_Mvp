"""Agent 状态定义"""

from typing import List, Dict, Any, TypedDict, Annotated
from operator import add


class AgentState(TypedDict):
    """Agent 状态"""
    
    # 当前用户问题
    question: str
    
    # 对话历史
    chat_history: Annotated[List[Dict[str, str]], add]
    
    # 检索到的文档
    retrieved_documents: List[Any]
    
    # 格式化的上下文
    context: str
    
    # 生成的回答
    answer: str
    
    # 引用的文档片段
    citations: List[Dict[str, Any]]
