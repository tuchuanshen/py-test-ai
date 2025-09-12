"""计算器工具"""
from typing import Dict, Any
from multi_agent_framework.tools.base import BaseTool


class CalculatorTool(BaseTool):
    """
    计算器工具 - 执行数学计算
    """
    
    def __init__(self):
        super().__init__("calculator", "执行数学计算")
        
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行数学计算
        
        Args:
            input_data: 包含expression字段的字典
            
        Returns:
            计算结果
        """
        expression = input_data.get("expression", "")
        
        try:
            # 安全计算
            allowed_chars = set('0123456789+-*/(). ')
            cleaned_expr = ''.join(c for c in expression if c in allowed_chars)
            result = eval(cleaned_expr)
            
            return {
                "success": True,
                "result": f"{expression} = {result}",
                "original_expression": expression
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"计算错误: {str(e)}",
                "original_expression": expression
            }