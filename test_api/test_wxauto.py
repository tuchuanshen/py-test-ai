from wxauto import WeChat
import time
from datetime import datetime
import hashlib

wx = WeChat()

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
llm = ChatTongyi(
    api_key=dashscope_api_key,
    model="qwen-turbo"
)

# 初始化对话记忆
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

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
tools = [
    CalculatorTool(),
    DateTimeTool()
]

# 初始化Agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

def on_message(msg, chat):
    wx.RemoveListenChat(chat.who, False)
    print(f"收到来自 {chat.who} 的消息: {msg.content}")
    
    # 回复消息
    reply_content = agent.run(msg.content)
    print(f"\n千问回答: {reply_content}")
    time.sleep(1)
    chat.SendMsg(f"亲爱的宝，{reply_content}")
    time.sleep(0.1)
    wx.AddListenChat(nickname="苗秋秋[爱心]", callback=on_message)

wx.AddListenChat(nickname="苗秋秋[爱心]", callback=on_message)
wx.AddListenChat(nickname="沈圳、沈学年、苗秋秋[爱心]", callback=on_message)

# 保持程序运行
wx.KeepRunning()