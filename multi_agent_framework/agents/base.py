"""智能体基类"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from langchain_core.messages import BaseMessage


class BaseAgent(ABC):
    """
    智能体基类 - 所有智能体都应该继承此类
    """
    
    def __init__(self, agent_id: str, name: str, description: str):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.tools = []
        self.capabilities = []
        
    @abstractmethod
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理输入状态并返回更新后的状态
        
        Args:
            state: 当前状态
            
        Returns:
            更新后的状态
        """
        pass
    
    def add_tool(self, tool) -> None:
        """添加工具"""
        self.tools.append(tool)
        
    def get_tools(self) -> List:
        """获取工具列表"""
        return self.tools
        
    def can_handle(self, task_type: str) -> bool:
        """检查是否能处理特定类型的任务"""
        return task_type in self.capabilities
        
    def get_description(self) -> str:
        """获取智能体描述"""
        return f"ID: {self.agent_id}, Name: {self.name}, Description: {self.description}"