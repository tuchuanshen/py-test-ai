"""状态管理模块"""
from typing import Annotated, Sequence, Dict, Any, List, Optional
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    智能体状态定义
    """
    # 对话历史
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # 当前问题
    question: str
    
    # 当前答案
    answer: str
    
    # RAG检索到的上下文
    context: str
    
    # 工具调用结果
    tool_results: Dict[str, Any]
    
    # 是否需要反思
    needs_reflection: bool
    
    # 最终答案
    final_answer: str
    
    # 下一步要执行的操作
    next_step: str
    
    # 当前处理的智能体
    current_agent: str
    
    # 任务分配信息
    task_assignments: Dict[str, Any]
    
    # 对话历史管理
    chat_history: List[Dict[str, Any]]


class GlobalState(TypedDict):
    """
    全局状态定义 - 用于多智能体协作
    """
    # 所有智能体的状态
    agent_states: Dict[str, AgentState]
    
    # 任务队列
    task_queue: List[Dict[str, Any]]
    
    # 消息总线
    message_bus: List[Dict[str, Any]]
    
    # 协作历史
    collaboration_history: List[Dict[str, Any]]