from wxauto import WeChat
import time
from datetime import datetime
import hashlib

wx = WeChat()

# test_dmx.py
from langchain.llms import Tongyi
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv("./../env")

# 从环境变量获取API密钥
QIAN_WEN_KEY = os.getenv("QIAN_WEN_KEY")

# 验证API密钥是否存在
if not QIAN_WEN_KEY:
    raise ValueError("QIAN_WEN_KEY 未在 .env 文件中设置")

# 设置API密钥
os.environ["TONGYI_API_KEY"] = QIAN_WEN_KEY
os.environ["DASHSCOPE_API_KEY"] = QIAN_WEN_KEY

class QwenQAModel:
    def __init__(self):
        # 初始化千问大模型
        self.llm = Tongyi(
            model_name="qwen-turbo",  # 或者使用 qwen-turbo, qwen-max 等
            temperature=0.7,
            max_tokens=2048
        )
        
        # 创建问答提示模板
        self.qa_template = """
        你是一个智能问答助手,情感调节师，别人无论如何，让他保持好心情。        
        """
        
        self.prompt = PromptTemplate(
            template=self.qa_template,
            input_variables=[ "question"]
        )
        
        # 创建问答链
        self.qa_chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def answer_question(self, question: str, context: str = ""):
        """
        基于给定上下文回答问题
        
        Args:
            question (str): 用户问题
            context (str): 上下文信息
            
        Returns:
            str: 模型回答
        """
        response = self.qa_chain.run({
            "question": question
        })
        return response

def interactive_qa_loop(input_text):
    """
    交互式问答循环
    """
    global qa_model 
    
    answer = qa_model.answer_question(input_text)
    return answer

# 用于跟踪已发送消息的集合，存储消息内容和时间戳的组合
sent_messages = set()
qa_model = QwenQAModel()

def generate_message_id(content, timestamp):
    """生成消息的唯一标识"""
    return hashlib.md5(f"{content}_{timestamp}".encode()).hexdigest()

def on_message(msg, chat):
    print(f"收到来自 {chat.who} 的消息: {msg.content}")
    
    # 回复消息
    reply_content = interactive_qa_loop(msg.content)
    print(f"回复给 {chat.who} 的消息: {reply_content}")
    
    
    time.sleep(2)
    chat.SendMsg(reply_content)

wx.AddListenChat(nickname="沈圳", callback=on_message)

# 保持程序运行
wx.KeepRunning()