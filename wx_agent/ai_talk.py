"""
基于LangChain框架的带提示词的聊天工具
支持自定义提示词模板和对话历史管理
"""

import os
from typing import Dict, Optional, Any
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 加载环境变量
load_dotenv("./../.env")

class PromptChat:
    """带提示词的聊天工具类"""
    
    def __init__(self, model_name: str = "qwen-turbo", temperature: float = 0.7):
        """
        初始化聊天工具
        
        Args:
            model_name: 使用的模型名称
            temperature: 模型温度参数，控制输出的随机性
        """
        self.llm = self._init_model(model_name, temperature)
        self.prompt_templates: Dict[str, ChatPromptTemplate] = {}
        self.memories: Dict[str, ConversationBufferMemory] = {}
        self.chains: Dict[str, LLMChain] = {}
        
        # 初始化默认提示词模板
        self._init_default_prompts()
        
    def _init_model(self, model_name: str, temperature: float):
        """
        初始化语言模型
        
        Args:
            model_name: 模型名称
            temperature: 温度参数
            
        Returns:
            初始化的语言模型
        """
        dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
        if not dashscope_api_key:
            raise ValueError("DASHSCOPE_API_KEY 环境变量未设置")
            
        return ChatTongyi(
            api_key=dashscope_api_key,
            model=model_name,
            temperature=temperature
        )
    
    def _init_default_prompts(self):
        """初始化默认提示词模板"""
        # 通用聊天提示词模板
        self.add_prompt_template(
            "general",
            ChatPromptTemplate.from_messages([
                ("system", "你是一个有帮助的AI助手。根据我提供的这段对话信息，帮助我下一句该如何回复。回答的内容要尽量短小，简练。回答的语气一定要温柔谦和、轻松、略带文采。直接给出该说的内容即可，不要包含任何多余的提示。"),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
            ])
        )
        
        # 专业助手提示词模板
        self.add_prompt_template(
            "professional",
            ChatPromptTemplate.from_messages([
                ("system", "你是一个专业的助手，会用专业的术语和知识回答用户问题。"),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
            ])
        )
        
        # 友好助手提示词模板
        self.add_prompt_template(
            "friendly",
            ChatPromptTemplate.from_messages([
                ("system", "你是一个友好、幽默的助手，会用轻松的语气回答用户问题。"),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
            ])
        )
        
        # 诗歌创作助手提示词模板
        self.add_prompt_template(
            "poet",
            ChatPromptTemplate.from_messages([
                ("system", "你是一个专职诗词创作的助手，用户给你任意题材，你都需要写出一首诗作答，不需要回答其他内容。"),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
            ])
        )
    
    def add_prompt_template(self, name: str, template: ChatPromptTemplate):
        """
        添加提示词模板
        
        Args:
            name: 模板名称
            template: 提示词模板对象
        """
        self.prompt_templates[name] = template
    
    def create_memory(self, session_id: str, memory_key: str = "chat_history"):
        """
        为会话创建记忆
        
        Args:
            session_id: 会话ID
            memory_key: 记忆键名
            
        Returns:
            创建的记忆对象
        """
        memory = ConversationBufferMemory(
            memory_key=memory_key,
            return_messages=True
        )
        self.memories[session_id] = memory
        return memory
    
    def get_memory(self, session_id: str) -> Optional[ConversationBufferMemory]:
        """
        获取会话记忆
        
        Args:
            session_id: 会话ID
            
        Returns:
            记忆对象，如果不存在则返回None
        """
        return self.memories.get(session_id)
    
    def create_chain(self, template_name: str, session_id: str) -> LLMChain:
        """
        创建对话链
        
        Args:
            template_name: 提示词模板名称
            session_id: 会话ID
            
        Returns:
            创建的对话链
        """
        if template_name not in self.prompt_templates:
            raise ValueError(f"提示词模板 '{template_name}' 不存在")
        
        # 如果会话记忆不存在，则创建
        if session_id not in self.memories:
            self.create_memory(session_id)
        
        # 创建链
        chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_templates[template_name],
            memory=self.memories[session_id]
        )
        
        self.chains[session_id] = chain
        return chain
    
    def get_chain(self, session_id: str) -> Optional[LLMChain]:
        """
        获取对话链
        
        Args:
            session_id: 会话ID
            
        Returns:
            对话链对象，如果不存在则返回None
        """
        return self.chains.get(session_id)
    
    def chat(self, message: str, session_id: str = "default", template_name: str = "general") -> str:
        """
        进行对话
        
        Args:
            message: 用户消息
            session_id: 会话ID
            template_name: 使用的提示词模板名称
            
        Returns:
            AI回复
        """
        # 获取或创建对话链
        chain = self.get_chain(session_id)
        if not chain:
            chain = self.create_chain(template_name, session_id)
        
        # 进行对话
        response = chain.invoke({"input": message})
        return response["text"]
    
    def clear_memory(self, session_id: str):
        """
        清除会话记忆
        
        Args:
            session_id: 会话ID
        """
        if session_id in self.memories:
            self.memories[session_id].clear()

def create_chat_session(model_name: str = "qwen-turbo", temperature: float = 0.7) -> PromptChat:
    """
    创建聊天会话实例
    
    Args:
        model_name: 模型名称
        temperature: 温度参数
        
    Returns:
        PromptChat实例
    """
    return PromptChat(model_name, temperature)

# 使用示例
if __name__ == "__main__":
    # 创建聊天实例
    chatbot = create_chat_session()
    
    print("基于LangChain的提示词聊天工具")
    print("支持的提示词模板: general, professional, friendly, poet")
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'clear' 清除对话历史")
    print("输入 'template:<name>' 切换提示词模板（如: template:friendly）")
    print("-" * 50)
    
    session_id = "interactive_session"
    template_name = "general"
    
    while True:
        try:
            user_input = input(f"\n[{template_name}] 你: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("助手: 再见！")
                break
            
            if user_input.lower() == 'clear':
                chatbot.clear_memory(session_id)
                print("助手: 对话历史已清除")
                continue
            
            if user_input.startswith('template:'):
                new_template = user_input.split(':')[1]
                if new_template in chatbot.prompt_templates:
                    template_name = new_template
                    print(f"助手: 已切换到 '{template_name}' 提示词模板")
                else:
                    print(f"助手: 未找到 '{new_template}' 模板，请使用: general, professional, friendly, poet")
                continue
            
            if not user_input:
                continue
            
            # 进行对话
            response = chatbot.chat(user_input, session_id, template_name)
            print(f"助手: {response}")
            
        except KeyboardInterrupt:
            print("\n\n助手: 再见！")
            break
        except Exception as e:
            print(f"\n助手: 发生错误: {str(e)}")