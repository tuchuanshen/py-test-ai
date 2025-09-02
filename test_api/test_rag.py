from langchain_community.chat_models import ChatTongyi
from langchain.prompts import ChatPromptTemplate
from langchain.agents import initialize_agent, AgentType
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool, BaseTool
import requests, os
from typing import Optional, Type
from pydantic import Field, BaseModel
from dotenv import load_dotenv
import time

# 加载环境变量
load_dotenv('./../.env')


def get_llm():
    # 获取千问API密钥
    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")

    # 初始化千问模型
    llm = ChatTongyi(api_key=dashscope_api_key, model="qwen-turbo")
    return llm


def get_prompt():
    prompt = ChatPromptTemplate.from_messages([("system", "你是一个有用的助手"),
                                               ("human", "{input}"),
                                               ("placeholder",
                                                "{agent_scratchpad}")])
    return prompt


# 定义输入模型
class WeatherInput(BaseModel):
    city: str = Field(description="城市名称")
    country: Optional[str] = Field(default="CN", description="国家代码")


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


class WeatherTool(BaseTool):
    name: str = "weather_tool"
    description: str = "用于获取天气信息。当用户询问天气问题时使用此工具。"
    args_schema: Type[BaseModel] = WeatherInput

    def _run(self, city: str, country: str = "CN") -> str:
        """同步执行天气查询"""
        # 这里可以调用真实的天气API
        return f"{city}, {country} 的天气是晴天，温度25°C"


if __name__ == "__main__":
    tools = [CalculatorTool(), WeatherTool()]
    llm = get_llm()
    prompt = get_prompt()
    # 初始化Agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    while True:
        query = input("请输入您的问题（输入'退出'结束）：")
        if query.lower() == '退出':
            break
        response = agent_executor.invoke({"input": query})
        print(f"回答: {response}")
        time.sleep(1)
