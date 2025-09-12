"""多智能体协作框架主入口"""
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from multi_agent_framework.core.engine import MultiAgentEngine
from multi_agent_framework.agents.chat_agent import ChatAgent
from multi_agent_framework.tools.calculator import CalculatorTool
from multi_agent_framework.tools.weather import WeatherTool
from multi_agent_framework.core.tool_manager import ToolManager
from multi_agent_framework.domains.technical import TechnicalRAG
from multi_agent_framework.reflection.quality_checker import QualityCheckerReflector

from wx_agent.local_llm import local_llm_get


def single_agent_demo():
    """单智能体演示"""
    print("单智能体演示开始...")
    try:
        llm = local_llm_get()
        agent = ChatAgent("agent_001", "演示智能体", llm)
        initial_state = {
            "messages": [{
                "role": "user",
                "content": "你好，能介绍一下你自己吗？"
            }],
            "question": "你是谁？"
        }
        updated_state = agent.process(initial_state)
        print("智能体回答:", updated_state.get("answer", "无回答"))
    except Exception as e:
        print(f"单智能体演示失败: {str(e)}")


def main():
    """主函数"""
    print("多智能体协作框架启动...")

    # 初始化引擎
    engine = MultiAgentEngine()

    # 初始化工具管理器
    tool_manager = ToolManager()

    # 注册工具
    calculator = CalculatorTool()
    weather = WeatherTool()
    tool_manager.register_tool(calculator)
    tool_manager.register_tool(weather)

    # 初始化智能体
    # 这里需要获取LLM实例
    try:
        llm = local_llm_get()

        # 创建聊天智能体
        chat_agent = ChatAgent("chat_agent_001", "通用聊天智能体", llm)
        engine.register_agent("chat_agent_001", chat_agent)

        # 初始化反思器
        reflector = QualityCheckerReflector(llm)

        # 初始化技术文档RAG
        tech_docs_path = r"D:\tuchuan\tc_test\py-test-ai\wx_agent"
        technical_rag = TechnicalRAG(tech_docs_path)

        print("框架初始化完成")
        print("可用工具:", [tool["name"] for tool in tool_manager.list_tools()])

        # 简单交互循环
        while True:
            user_input = input("\n请输入您的问题（输入'退出'结束）：")
            if user_input.lower() == '退出':
                break

            # 简单的任务处理流程
            print(f"处理问题: {user_input}")
            print("这是一个演示框架，具体实现需要根据需求完善...")

    except Exception as e:
        print(f"框架启动失败: {str(e)}")


if __name__ == "__main__":
    single_agent_demo()
