import os
from typing import Optional
from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from langchain.tools import BaseTool
from langchain.callbacks import StdOutCallbackHandler

# 加载环境变量
load_dotenv('./../.env')

# 获取千问API密钥
dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")

# 初始化千问模型
llm = ChatTongyi(api_key=dashscope_api_key, model="qwen-turbo")

# 初始化对话记忆
memory = ConversationBufferMemory(memory_key="chat_history",
                                  return_messages=True)


class CalculatorTool(BaseTool):
    """计算器工具，用于执行简单的数学计算"""
    name: str = "calculator_tool"
    description: str = "用于执行简单的数学计算，如加减乘除运算。当用户询问数学计算问题时使用此工具。"

    def _run(self, query: str) -> str:
        try:
            # 简单的安全计算实现
            # 移除可能的危险字符，只保留数字和基本运算符
            allowed_chars = set('0123456789+-*/(). ')
            cleaned_query = ''.join(c for c in query if c in allowed_chars)

            # 计算结果
            result = eval(cleaned_query)
            return f"{query} = {result}"
        except Exception as e:
            return f"计算出错: {str(e)}"


class DateTimeTool(BaseTool):
    """日期时间工具，用于获取当前日期和时间"""
    name: str = "datetime_tool"
    description: str = "用于获取当前日期和时间信息。当用户询问当前时间或日期时使用此工具。"

    def _run(self, query: str) -> str:
        from datetime import datetime
        now = datetime.now()
        return f"当前日期和时间: {now.strftime('%Y年%m月%d日 %H:%M:%S')}"


# 初始化工具列表
tools = [CalculatorTool(), DateTimeTool()]

# 初始化Agent
agent = initialize_agent(tools,
                         llm,
                         agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                         memory=memory,
                         verbose=True,
                         handle_parsing_errors=True)


def explain_agent_decision_process():
    """解释Agent的决策过程"""
    print("=" * 60)
    print("Agent决策机制说明:")
    print("=" * 60)
    print("1. Agent会根据问题内容和工具描述决定是否使用工具")
    print("2. 工具描述非常重要，它告诉Agent在什么情况下使用该工具")
    print("3. 如果问题可以直接回答，Agent不会使用任何工具")
    print("4. 如果问题需要特定信息(如时间、计算)，Agent会使用相应工具")
    print("5. Agent的记忆功能让它能够记住之前的对话内容")
    print("=" * 60)


def chat_with_qwen():
    """与千问进行对话的主函数"""
    print("千问智能问答系统（输入'quit'或'exit'退出）")
    print("输入 'help' 查看Agent决策机制说明")
    print("-" * 40)

    while True:
        try:
            user_input = input("\n请输入您的问题: ").strip()

            if user_input.lower() in ['quit', 'exit', '退出']:
                print("感谢使用千问智能问答系统！")
                break

            if user_input.lower() == 'help':
                explain_agent_decision_process()
                continue

            if not user_input:
                continue

            # 使用Agent运行用户输入
            response = agent.run(user_input)
            print(f"\n千问回答: {response}")

        except KeyboardInterrupt:
            print("\n\n程序已退出，再见！")
            break
        except Exception as e:
            print(f"\n发生错误: {str(e)}")
            print("请重新输入或尝试其他问题")


if __name__ == "__main__":
    chat_with_qwen()
