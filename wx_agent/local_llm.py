from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from langchain_community.chat_models import ChatTongyi
from dotenv import load_dotenv
from langchain_core.globals import set_llm_cache
import os
from pydantic import SecretStr
# 加载环境变量
load_dotenv('./../.env')


def get_llm():
    # 获取千问API密钥
    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
    # 初始化千问模型
    llm = ChatTongyi(api_key=dashscope_api_key, model="qwen-turbo")
    return llm



def local_llm_get():
    llm = ChatOpenAI(base_url="http://127.0.0.1:8080/v1",
                     api_key="sk-my-local-key-12345",
                     temperature=0.7)
    return llm


def qwen_llm_get():
    llm = init_chat_model(
        model="qwen2.5-7b-instruct-q4_0",  # 模型名称
        model_provider="openai",  # 使用openai提供者（兼容模式）
        base_url="http://127.0.0.1:8080/v1",
        api_key="sk-my-local-key-12345",
        temperature=0.7)
    return llm