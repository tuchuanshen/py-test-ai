"""
多语言RAG管理器
继承自RAGManager，使用bge-m3模型和Qdrant向量数据库实现多语言支持
"""

import os
import json
from typing import Dict, Any, List, Optional, Union
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.schema import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.document_loaders import (
    PDFMinerLoader, UnstructuredWordDocumentLoader, UnstructuredExcelLoader,
    CSVLoader, PythonLoader)
import logging

from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

# 导入原始的RAGManager
from .manager import RAGManager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MultilingualRAGManager(RAGManager):
    """
    多语言RAG管理器
    继承自RAGManager，使用bge-m3嵌入模型和Qdrant向量数据库支持多语言检索
    """

    def __init__(self,
                 llm=None,
                 config_path: Optional[str] = None,
                 qdrant_host: str = "localhost",
                 qdrant_port: int = 6333):
        """
        初始化多语言RAG管理器
        
        Args:
            llm: 大型语言模型实例
            config_path: 配置文件路径
            qdrant_host: Qdrant服务器主机地址
            qdrant_port: Qdrant服务器端口
        """
        # 调用父类初始化方法
        super().__init__(llm, config_path)

        # 初始化Qdrant客户端
        self.qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)

        # 使用bge-m3作为嵌入模型，支持多语言
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-m3",
            model_kwargs={'device': 'cpu'},  # 根据需要改为'cuda'
            encode_kwargs={'normalize_embeddings': True})

        logger.info("多语言RAG管理器初始化完成")

    def _create_rag_chain(self, path: str, domain_id: str) -> RetrievalQA:
        """
        创建RAG链，重写父类方法以使用Qdrant和bge-m3
        
        Args:
            path: 文档路径（可以是文件或目录）
            domain_id: 领域ID，用于创建独立的向量存储
            
        Returns:
            RetrievalQA链
        """
        # 创建Qdrant集合
        collection_name = f"rag_collection_{domain_id}"

        try:
            # 尝试创建集合，如果已存在会抛出异常
            self.qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=1024,
                                            distance=Distance.COSINE),
            )
            logger.info(f"创建新的Qdrant集合: {collection_name}")
        except Exception as e:
            logger.info(f"Qdrant集合 {collection_name} 已存在或创建失败: {str(e)}")

        # 创建Qdrant实例
        qdrant = Qdrant(
            client=self.qdrant_client,
            collection_name=collection_name,
            embeddings=self.embeddings,
        )

        # 检查集合是否为空，如果为空则加载文档
        collection_info = self.qdrant_client.get_collection(
            collection_name=collection_name)
        if collection_info.points_count == 0:
            logger.info(f"集合 {collection_name} 为空，正在加载文档...")
            # 加载文档
            if os.path.isfile(path):
                # 单个文件
                loader = self._get_loader(path)
                documents = loader.load()
            else:
                # 目录中的所有支持的文件
                loader = DirectoryLoader(path,
                                         glob="**/*",
                                         show_progress=True,
                                         use_multithreading=True)
                documents = loader.load()

            if not documents:
                raise ValueError(f"在路径 {path} 中未找到文档")

            # 为文档添加元数据
            for i, doc in enumerate(documents):
                if 'source' not in doc.metadata:
                    doc.metadata['source'] = path
                doc.metadata['domain'] = domain_id

            # 文本分割
            text_splitter_config = self.config.get("text_splitter", {})
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=text_splitter_config.get("chunk_size", 1000),
                chunk_overlap=text_splitter_config.get("chunk_overlap", 200))
            splits = text_splitter.split_documents(documents)

            logger.info(f"文档分割完成，共 {len(splits)} 个片段")

            # 将文档添加到Qdrant
            qdrant.add_documents(splits)
            logger.info(f"文档已添加到Qdrant集合 {collection_name}")

        # 创建检索链
        retriever_config = self.config.get("retriever", {})
        search_kwargs = retriever_config.get("search_kwargs", {"k": 4})

        # 创建检索器
        retriever = qdrant.as_retriever(search_type=retriever_config.get(
            "search_type", "similarity"),
                                        search_kwargs=search_kwargs)

        # 定义提示模板
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                '请根据以下上下文回答问题：{context}',
            ),
            MessagesPlaceholder(variable_name="messages"),
        ])

        # 创建RAG链
        from langchain.chains import ConversationalRetrievalChain

        rag_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            chain_type="stuff",
            condense_question_prompt=prompt,
            return_source_documents=True)

        return rag_chain

    def query(self,
              question: str,
              domain: str = None,
              filter: Optional[Dict[str, Any]] = None,
              **kwargs) -> Dict[str, Any]:
        """
        查询RAG系统
        
        Args:
            question: 问题
            domain: 领域ID，如果为None则使用默认领域
            filter: 过滤条件，用于过滤检索结果
            **kwargs: 传递给prompt的额外变量
            
        Returns:
            查询结果
        """
        # 如果没有指定领域，则使用默认领域
        if domain is None or domain not in self.rag_chains:
            domain = self.config.get("default_domain", "technical")

        if domain not in self.rag_chains:
            return {
                "success": False,
                "error": f"未找到领域 {domain} 的知识库",
                "answer": ""
            }

        rag_chain = self.rag_chains[domain]

        # 创建输入消息
        input_messages = [HumanMessage(content=question)]

        # 合并question和kwargs作为输入
        input_data = {
            "question": question,
            "messages": input_messages,
            "chat_history": [],  # ConversationalRetrievalChain需要chat_history
            **kwargs
        }

        # 如果提供了过滤器，则临时修改检索器
        if filter is not None:
            # 获取原始检索器的配置
            original_retriever = rag_chain.retriever
            retriever_config = self.config.get("retriever", {})
            search_kwargs = retriever_config.get("search_kwargs", {"k": 4})
            search_kwargs["filter"] = filter

            # 创建新的带过滤器的检索器
            new_retriever = original_retriever.vectorstore.as_retriever(
                search_type=retriever_config.get("search_type", "similarity"),
                search_kwargs=search_kwargs)

            # 临时替换检索器
            rag_chain.retriever = new_retriever
            result = rag_chain.invoke(input_data)
            # 恢复原始检索器
            rag_chain.retriever = original_retriever
        else:
            result = rag_chain.invoke(input_data)

        return {
            "success": True,
            "answer": result.get("answer", ""),
            "sources": result.get("source_documents", [])
        }
