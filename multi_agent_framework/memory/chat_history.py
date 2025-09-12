"""对话历史管理器"""
from typing import List, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage


class ChatHistoryManager:
    """
    对话历史管理器 - 管理用户和AI之间的对话历史
    """
    
    def __init__(self, max_history_length: int = 10):
        self.max_history_length = max_history_length
        self.history: List[Dict[str, Any]] = []
        
    def add_user_message(self, content: str) -> None:
        """
        添加用户消息
        
        Args:
            content: 消息内容
        """
        self.history.append({
            "role": "user",
            "content": content,
            "type": "HumanMessage"
        })
        self._trim_history()
        
    def add_ai_message(self, content: str) -> None:
        """
        添加AI消息
        
        Args:
            content: 消息内容
        """
        self.history.append({
            "role": "assistant",
            "content": content,
            "type": "AIMessage"
        })
        self._trim_history()
        
    def _trim_history(self) -> None:
        """修剪历史记录，保持最大长度"""
        if len(self.history) > self.max_history_length:
            self.history = self.history[-self.max_history_length:]
            
    def get_history(self) -> List[Dict[str, Any]]:
        """
        获取对话历史
        
        Returns:
            对话历史列表
        """
        return self.history
        
    def get_langchain_messages(self) -> List[BaseMessage]:
        """
        获取LangChain格式的消息列表
        
        Returns:
            LangChain消息列表
        """
        messages = []
        for item in self.history:
            if item["type"] == "HumanMessage":
                messages.append(HumanMessage(content=item["content"]))
            elif item["type"] == "AIMessage":
                messages.append(AIMessage(content=item["content"]))
        return messages
        
    def clear_history(self) -> None:
        """清空对话历史"""
        self.history.clear()
        
    def get_history_length(self) -> int:
        """
        获取历史记录长度
        
        Returns:
            历史记录长度
        """
        return len(self.history)