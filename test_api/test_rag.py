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


if __name__ == "__main__":
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
