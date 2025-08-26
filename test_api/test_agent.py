from langchain_community.chat_models import ChatTongyi
from langchain.agents import initialize_agent,AgentType
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool,BaseTool
import requests, os
from typing import Optional
from pydantic import Field
from dotenv import load_dotenv

load_dotenv('./../.env')

dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")

llm = ChatTongyi(dashscope_api_key=dashscope_api_key, model="qwen-turbo", temperature=1)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

class WeatherTool(BaseTool):
    name : str="weather_tool"
    description : str ="主要是描述天气情况，需要城市和日期信息，如果没有给城市和日期信息，则使用默认城市和日期，默认使用杭州今天的天气"
    #args_schema: Optional[Type[BaseModel]] = None

    def _run(self, query: str) -> str:
        #url = f"https://api.tianapi.com/tianqi/index?key={dashscope_api_key}&city={query}"
        #response = requests.get(url)
        print("query:", query)
        memory.save_context({"input": query}, {"output": "今天多云，温度时20度，风向时南风"})
        return "今天多云，温度时20度，风向时南风"

tools = [
    WeatherTool()
]

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, memory=memory, verbose=True)

w_resp=agent.run("天气如何")

print("天气查询结果：", memory.load_memory_variables({}), w_resp)

history_resp = agent.run("这天气适合什么衣服")

print("穿衣查询结果：", memory.load_memory_variables({}))

print("历史记录：", memory.load_memory_variables({})["chat_history"])




