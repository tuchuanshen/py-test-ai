from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model


def local_llm_get():
    llm = ChatOpenAI(base_url="http://127.0.0.1:8080/v1",
                     api_key="sk-my-local-key-12345",
                     temperature=0.7,
                     max_tokens=1000)
    return llm


def qwen_llm_get():
    llm = init_chat_model(
        model="qwen2.5-7b-instruct-q4_0",  # 模型名称
        model_provider="openai",  # 使用openai提供者（兼容模式）
        base_url="http://127.0.0.1:8080/v1",
        api_key="sk-my-local-key-12345",
        temperature=0.7,
        max_tokens=1000)
    return llm
