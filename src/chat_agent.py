"""对话代理模块（重构版）

特性：
- 保持功能完全一致
- 使用更清晰的结构与注释
- 更严格的类型提示
- 具备更好的异常处理
- 更可维护、可扩展
"""

from typing import TypedDict, Annotated, Sequence, List
from operator import add

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END

from config import Config
from vector_store import VectorStore


# ================================
# Agent 状态结构
# ================================
class AgentState(TypedDict):
    """LangGraph 中的状态定义。"""
    messages: Annotated[Sequence[BaseMessage], add]
    context: str
    query: str


# ================================
# 主 Agent
# ================================
class ChatAgent:
    """
    基于 LangGraph + LangChain 的对话代理。

    功能：
    - 向量检索上下文
    - 使用 Ollama 模型生成回答
    - 支持对话历史
    - 可扩展的 LangGraph 工作流
    """

    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.chat_history: List[BaseMessage] = []

        # 初始化 LLM（Ollama）
        self.llm = ChatOllama(
            base_url=Config.OLLAMA_BASE_URL,
            model=Config.OLLAMA_MODEL,
            temperature=Config.LLM_TEMPERATURE,
        )

        # Prompt 模板
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """你是一个智能助手，基于提供的上下文回答用户问题。

规则：
1. 仅根据提供的上下文回答问题
2. 如果上下文中没有相关信息，明确告知用户
3. 回答时引用具体的文档片段
4. 保持回答简洁准确

上下文：
{context}
"""
            ),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{query}")
        ])

        # 构建工作流
        self.graph = self._build_graph()

    # ================================
    # LangGraph 构建
    # ================================
    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(AgentState)

        workflow.add_node("retrieve", self._retrieve_context)
        workflow.add_node("generate", self._generate_response)

        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)

        return workflow.compile()

    # ================================
    # Step 1：向量检索
    # ================================
    def _retrieve_context(self, state: AgentState) -> AgentState:
        query = state["query"]

        try:
            docs = self.vector_store.similarity_search(query)
        except Exception as e:
            state["context"] = f"检索失败：{e}"
            return state

        if not docs:
            state["context"] = "没有找到相关文档。"
            return state

        # 格式化上下文
        context_parts = []
        for idx, doc in enumerate(docs, start=1):
            source = doc.metadata.get("source", "未知")
            context_parts.append(
                f"[文档片段 {idx} - 来源: {source}]\n{doc.page_content}\n"
            )

        state["context"] = "\n".join(context_parts)
        return state

    # ================================
    # Step 2：模型生成回答
    # ================================
    def _generate_response(self, state: AgentState) -> AgentState:
        # 限制历史长度（避免上下文过大）
        history_messages = self.chat_history[-6:]

        formatted_messages = self.prompt.format_messages(
            context=state["context"],
            history=history_messages,
            query=state["query"]
        )
        # 调用 LLM
        try:
            ai_msg = self.llm.invoke(formatted_messages)
        except Exception as e:
            ai_msg = AIMessage(content=f"生成回答失败：{e}")

        # 更新 LangGraph 状态
        state["messages"] = [
            HumanMessage(content=state["query"]),
            ai_msg
        ]

        return state

    # ================================
    # 外部接口
    # ================================
    def chat(self, query: str) -> dict:
        """对外的聊天接口。"""
        initial_state: AgentState = {
            "messages": [],
            "context": "",
            "query": query
        }

        result = self.graph.invoke(initial_state)

        # 更新历史
        self.chat_history.extend(result["messages"])

        return {
            "query": query,
            "answer": result["messages"][-1].content,
            "context": result["context"]
        }

    def clear_history(self):
        """清空对话历史。"""
        self.chat_history = []
        print("✓ 对话历史已清空")
