"""天气查询工具"""
from typing import Dict, Any
from multi_agent_framework.tools.base import BaseTool


class WeatherTool(BaseTool):
    """
    天气查询工具 - 获取天气信息
    """
    
    def __init__(self):
        super().__init__("weather", "查询天气信息")
        
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        查询天气信息
        
        Args:
            input_data: 包含city字段的字典
            
        Returns:
            天气信息
        """
        city = input_data.get("city", "北京")
        
        # 模拟天气查询
        # 实际应用中这里会调用真实的天气API
        weather_info = f"{city}的天气是晴天，温度25°C，湿度60%，风力3级"
        
        return {
            "success": True,
            "result": weather_info,
            "city": city
        }