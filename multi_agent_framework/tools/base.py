"""工具基类"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class BaseTool(ABC):
    """
    工具基类 - 所有工具都应该继承此类
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        
    @abstractmethod
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行工具
        
        Args:
            input_data: 工具输入数据
            
        Returns:
            工具执行结果
        """
        pass
        
    def get_description(self) -> str:
        """获取工具描述"""
        return f"Tool: {self.name}, Description: {self.description}"