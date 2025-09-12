"""通用对话智能体"""
from typing import Dict, Any
from multi_agent_framework.agents.base import BaseAgent
from langchain_core.messages import HumanMessage, AIMessage


class ChatAgent(BaseAgent):
    """
    通用对话智能体 - 处理普通聊天任务
    """
    
    def __init__(self, agent_id: str, name: str, llm: Any):
        super().__init__(agent_id, name, "处理普通聊天任务")
        self.llm = llm
        self.capabilities = ["chat", "conversation"]
        
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理聊天任务
        """
        messages = state.get("messages", [])
        question = state.get("question", "")
        
        # 构建对话历史
        conversation_history = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                conversation_history.append(f"Human: {msg.content}")
            elif isinstance(msg, AIMessage):
                conversation_history.append(f"AI: {msg.content}")
        
        # 构建提示词
        prompt = f"""
        你是一个智能助手，能够进行自然对话。请以友好、专业的语气回答用户问题。
        
        对话历史:
        {"\n".join(conversation_history)}
        
        当前问题: {question}
        
        请回答:
        """
        
        # 调用LLM
        response = self.llm.invoke(prompt)
        
        # 更新状态
        updated_state = state.copy()
        updated_state["answer"] = response.content
        updated_state["needs_reflection"] = True
        updated_state["next_step"] = "reflect"
        
        return updated_state