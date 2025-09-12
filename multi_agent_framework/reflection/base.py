"""反思器基类"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseReflector(ABC):
    """
    反思器基类 - 所有反思器都应该继承此类
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        
    @abstractmethod
    def reflect(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        对答案进行反思和优化
        
        Args:
            state: 当前状态
            
        Returns:
            反思后的状态
        """
        pass
        
    def get_description(self) -> str:
        """获取反思器描述"""
        return f"Reflector: {self.name}, Description: {self.description}"