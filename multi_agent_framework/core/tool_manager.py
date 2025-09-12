"""工具管理器"""
from typing import Dict, Any, List
from ..tools.base import BaseTool


class ToolManager:
    """
    工具管理器 - 管理所有可用工具
    """
    
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        
    def register_tool(self, tool: BaseTool) -> None:
        """
        注册工具
        
        Args:
            tool: 工具实例
        """
        self.tools[tool.name] = tool
        print(f"工具 {tool.name} 注册成功")
        
    def get_tool(self, tool_name: str) -> BaseTool:
        """
        获取工具
        
        Args:
            tool_name: 工具名称
            
        Returns:
            工具实例
        """
        return self.tools.get(tool_name)
        
    def list_tools(self) -> List[Dict[str, str]]:
        """
        列出所有工具
        
        Returns:
            工具列表
        """
        tool_list = []
        for name, tool in self.tools.items():
            tool_list.append({
                "name": name,
                "description": tool.get_description()
            })
        return tool_list
        
    def execute_tool(self, tool_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行工具
        
        Args:
            tool_name: 工具名称
            input_data: 输入数据
            
        Returns:
            执行结果
        """
        tool = self.get_tool(tool_name)
        if not tool:
            return {
                "success": False,
                "error": f"工具 {tool_name} 未找到"
            }
            
        try:
            result = tool.run(input_data)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"工具执行失败: {str(e)}"
            }