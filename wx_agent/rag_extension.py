"""
RAG功能扩展模块
用于在PromptChat中集成RAG功能，根据聊天内容相关领域从数据库中检索上下文
"""

import os
from typing import Dict, List, Optional, Any, Tuple
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate,ChatPromptTemplate
from langchain.docstore.document import Document
import re

class RAGExtension:
    """RAG功能扩展类"""
    
    def __init__(self, embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        初始化RAG扩展
        
        Args:
            embeddings_model: 用于生成嵌入的模型名称
        """
        self.embeddings = HuggingFaceEmbeddings(model_name=embeddings_model)
        self.vector_stores: Dict[str, Chroma] = {}  # 不同领域的向量数据库
        self.domain_keywords: Dict[str, List[str]] = {}  # 领域关键词映射
        self.retrievers: Dict[str, Any] = {}  # 检索器
        
    def add_domain(self, domain_name: str, documents_path: str, keywords: List[str]):
        """
        添加一个领域及其相关文档和关键词
        
        Args:
            domain_name: 领域名称
            documents_path: 文档路径
            keywords: 用于检测该领域的关键词列表
        """
        # 加载文档
        documents = self._load_documents(documents_path)
        
        # 分割文档
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)
        
        # 创建向量数据库
        vector_store = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=f"./chroma_db/{domain_name}"
        )
        
        self.vector_stores[domain_name] = vector_store
        self.domain_keywords[domain_name] = keywords
        self.retrievers[domain_name] = vector_store.as_retriever(search_kwargs={"k": 4})
        
        print(f"领域 '{domain_name}' 已添加，包含 {len(splits)} 个文档片段")
    
    def _load_documents(self, path: str) -> List[Document]:
        """
        从指定路径加载文档
        
        Args:
            path: 文档路径
            
        Returns:
            文档列表
        """
        documents = []
        
        if os.path.isfile(path):
            # 单个文件
            documents.extend(self._load_single_file(path))
        elif os.path.isdir(path):
            # 目录中的所有文件
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(('.txt', '.md', '.pdf')):
                        file_path = os.path.join(root, file)
                        documents.extend(self._load_single_file(file_path))
        
        return documents
    
    def _load_single_file(self, file_path: str) -> List[Document]:
        """
        加载单个文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            文档列表
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return [Document(page_content=content, metadata={"source": file_path})]
        except Exception as e:
            print(f"加载文件 {file_path} 时出错: {e}")
            return []
    
    def detect_relevant_domain(self, query: str) -> Optional[str]:
        """
        检测查询相关的领域
        
        Args:
            query: 用户查询
            
        Returns:
            相关领域名称，如果没有找到则返回None
        """
        query_lower = query.lower()
        
        # 基于关键词检测相关领域
        for domain, keywords in self.domain_keywords.items():
            for keyword in keywords:
                if keyword.lower() in query_lower:
                    return domain
        
        return None
    
    def retrieve_context(self, query: str, domain: str) -> List[Document]:
        """
        从指定领域检索相关上下文
        
        Args:
            query: 查询内容
            domain: 领域名称
            
        Returns:
            相关文档片段列表
        """
        if domain not in self.retrievers:
            return []
        
        return self.retrievers[domain].get_relevant_documents(query)
    
    def format_context(self, documents: List[Document]) -> str:
        """
        格式化检索到的上下文
        
        Args:
            documents: 文档列表
            
        Returns:
            格式化后的上下文字符串
        """
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"片段 {i}:\n{doc.page_content}")
        
        return "\n\n".join(context_parts)

# 扩展PromptChat以支持RAG功能
class PromptChatWithRAG:
    """支持RAG功能的PromptChat扩展"""
    
    def __init__(self, prompt_chat_instance, rag_extension: RAGExtension):
        """
        初始化
        
        Args:
            prompt_chat_instance: PromptChat实例
            rag_extension: RAG扩展实例
        """
        self.prompt_chat = prompt_chat_instance
        self.rag_extension = rag_extension
    
    def chat_with_rag(self, message: str, session_id: str = "default", 
                      template_name: str = "general") -> str:
        """
        使用RAG功能进行对话
        
        Args:
            message: 用户消息
            session_id: 会话ID
            template_name: 提示词模板名称
            
        Returns:
            AI回复
        """
        # 检测相关领域
        relevant_domain = self.rag_extension.detect_relevant_domain(message)
        
        if relevant_domain:
            print(f"检测到相关领域: {relevant_domain}")
            
            # 检索相关上下文
            context_docs = self.rag_extension.retrieve_context(message, relevant_domain)
            
            if context_docs:
                # 格式化上下文
                context = self.rag_extension.format_context(context_docs)
                
                # 修改提示词以包含上下文
                rag_prompt = ChatPromptTemplate.from_messages([
                    ("system", "你是一个有帮助的AI助手。请根据提供的上下文信息回答用户问题。如果上下文信息不足以回答问题，请说明无法基于提供的信息回答该问题。"),
                    ("human", f"上下文信息：\n{context}\n\n问题：{message}")
                ])
                
                # 临时替换提示词模板
                original_template = self.prompt_chat.prompt_templates.get(template_name)
                self.prompt_chat.prompt_templates[template_name] = rag_prompt
                
                # 进行对话
                response = self.prompt_chat.chat(message, session_id, template_name)
                
                # 恢复原始提示词模板
                if original_template:
                    self.prompt_chat.prompt_templates[template_name] = original_template
                else:
                    del self.prompt_chat.prompt_templates[template_name]
                
                return response
        
        # 如果没有相关领域或检索不到上下文，使用普通对话
        return self.prompt_chat.chat(message, session_id, template_name)

# 使用示例和测试代码
def create_sample_documents():
    """创建示例文档用于测试"""
    # 创建示例文档目录
    os.makedirs("./sample_docs/tech", exist_ok=True)
    os.makedirs("./sample_docs/health", exist_ok=True)
    
    # 技术领域文档
    tech_doc = """
    人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。
    机器学习是人工智能的一个子领域，它使计算机能够从数据中学习并做出决策。
    深度学习是机器学习的一个分支，使用神经网络来模拟人脑的工作方式。
    自然语言处理（NLP）是AI的一个领域，专注于计算机与人类语言之间的交互。
    """
    
    with open("./sample_docs/tech/ai_basics.txt", "w", encoding="utf-8") as f:
        f.write(tech_doc)
    
    # 健康领域文档
    health_doc = """
    健康饮食对于维持身体健康至关重要。
    建议每天摄入五种不同颜色的蔬菜和水果。
    保持充足的睡眠对身心健康都有益处，成年人每晚应睡7-9小时。
    定期锻炼有助于增强免疫系统和心血管健康。
    压力管理是健康生活的重要组成部分，可以通过冥想、瑜伽等方式来缓解压力。
    """
    
    with open("./sample_docs/health/health_tips.txt", "w", encoding="utf-8") as f:
        f.write(health_doc)

if __name__ == "__main__":
    print("RAG功能扩展模块")
    print("=" * 50)
    print("该模块提供了以下功能：")
    print("1. 多领域文档管理")
    print("2. 基于关键词的领域检测")
    print("3. 向量数据库检索")
    print("4. 与PromptChat集成")
    print("\n使用方法：")
    print("1. 创建RAGExtension实例")
    print("2. 添加领域、文档和关键词")
    print("3. 使用PromptChatWithRAG进行对话")