# test_dmx.py
import os
from typing import Any, Dict
import openai
from openai import OpenAI

# 配置API密钥和基础URL
client = OpenAI(
    api_key="sk-kgBFfisUff6UIEQsFFRaGQ9Xygk1BbbHHwekn2hvu",
    base_url="https://www.dmxapi.cn"
)

def ask_question(question: str) -> str:
    """
    向模型提问
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个有帮助的AI助手。"},
                {"role": "user", "content": question}
            ],
            stream=False  # 先关闭流式输出避免问题
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"错误: {str(e)}"

def chat_loop():
    """
    聊天循环
    """
    print("开始对话 (输入'quit'退出):")
    while True:
        user_input = input("\n你: ")
        if user_input.lower() == 'quit':
            break
        
        print("AI: ", end="")
        response = ask_question(user_input)
        print(response)

# 如果你想使用LangChain，这里是更新后的版本
def langchain_version():
    """
    使用更新后的LangChain版本
    """
    # 首先需要安装: pip install langchain-openai langchain-core
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage, SystemMessage
        from langchain_core.runnables.history import RunnableWithMessageHistory
        from langchain_core.chat_history import InMemoryChatMessageHistory
        
        # 配置模型
        chat_model = ChatOpenAI(
            model="gpt-3.5-turbo",
            openai_api_key="sk-kgBFfisUff6UIEQsFFRaGQ9Xygk1BbbHHwekn2hvuPbSAnIc",
            openai_api_base="https://www.dmxapi.cn",
            streaming=False  # 暂时关闭流式输出
        )
        
        # 简单问答函数
        def simple_qa(question: str):
            messages = [
                SystemMessage(content="你是一个有帮助的AI助手。"),
                HumanMessage(content=question)
            ]
            response = chat_model.invoke(messages)
            return response.content
        
        print("LangChain版本对话 (输入'quit'退出):")
        while True:
            user_input = input("\n你: ")
            if user_input.lower() == 'quit':
                break
            
            print("AI: ", end="")
            response = simple_qa(user_input)
            print(response)
            
    except ImportError as e:
        print(f"缺少必要的包: {e}")
        print("请运行: pip install langchain-openai langchain-core")

if __name__ == "__main__":
    print("选择模式:")
    print("1. 基础OpenAI API")
    print("2. LangChain版本 (需要额外安装包)")
    
    choice = input("请输入选择 (1 或 2): ")
    
    if choice == "1":
        chat_loop()
    elif choice == "2":
        langchain_version()
    else:
        print("无效选择，使用基础版本")
        chat_loop()