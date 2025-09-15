"""RAG管理器"""
import os
import json
from typing import Dict, Any, List, Optional
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.schema import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.document_loaders import (
    PDFMinerLoader, UnstructuredWordDocumentLoader, UnstructuredExcelLoader,
    CSVLoader, PythonLoader)


class RAGManager:
    """
    RAG管理器 - 管理多个领域的知识库
    支持多种文件类型加载、目录加载和向量数据库持久化
    """

    def __init__(self, llm=None, config_path: str = None):
        # 默认配置文件路径
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__),
                                       "config.json")

        # 加载配置
        self.config = self._load_config(config_path)

        self.rag_chains: Dict[str, RetrievalQA] = {}
        self.embeddings = HuggingFaceEmbeddings(model_name=self.config.get(
            "embeddings_model", "sentence-transformers/all-MiniLM-L6-v2"))
        self.llm = llm
        self.persist_directory = self.config.get("persist_directory",
                                                 "./chroma_db")
        # 确保持久化目录存在
        os.makedirs(self.persist_directory, exist_ok=True)

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        if not os.path.exists(config_path):
            # 创建默认配置文件
            default_config = {
                "persist_directory": "./chroma_db",
                "embeddings_model": "sentence-transformers/all-MiniLM-L6-v2",
                "default_domain": "technical",
                "domains": {
                    "technical": {
                        "path": "./domains",
                        "description": "技术领域知识库"
                    }
                },
                "retriever": {
                    "search_type": "similarity",
                    "search_kwargs": {
                        "k": 4
                    }
                },
                "text_splitter": {
                    "chunk_size": 1000,
                    "chunk_overlap": 200
                }
            }

            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)

            return default_config
        else:
            # 读取现有配置文件
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)

    def add_domain(self,
                   domain_id: str,
                   path: str = None,
                   description: str = "") -> bool:
        """
        添加领域知识库
        
        Args:
            domain_id: 领域ID
            path: 文档路径（可以是文件或目录），如果为None则从配置文件读取
            description: 领域描述
            
        Returns:
            是否添加成功
        """
        try:
            # 如果没有提供路径，则从配置文件中读取
            if path is None:
                domain_config = self.config.get("domains", {}).get(domain_id)
                if domain_config:
                    path = domain_config.get("path")
                    description = domain_config.get("description", description)
                else:
                    print(f"未在配置文件中找到领域 {domain_id} 的配置")
                    return False

            if not os.path.exists(path):
                print(f"路径不存在: {path}")
                return False

            # 创建RAG链
            rag_chain = self._create_rag_chain(path, domain_id)
            self.rag_chains[domain_id] = rag_chain
            print(f"成功添加领域: {domain_id}")
            return True
        except Exception as e:
            print(f"添加领域 {domain_id} 失败: {str(e)}")
            return False

    def _get_loader(self, file_path: str):
        """根据文件扩展名选择合适的加载器"""
        _, extension = os.path.splitext(file_path)
        extension = extension.lower()

        if extension == '.txt':
            return TextLoader(file_path, encoding='utf-8')
        elif extension == '.pdf':
            return PDFMinerLoader(file_path)
        elif extension in ['.doc', '.docx']:
            return UnstructuredWordDocumentLoader(file_path)
        elif extension in ['.xls', '.xlsx']:
            return UnstructuredExcelLoader(file_path)
        elif extension == '.csv':
            return CSVLoader(file_path)
        elif extension == '.py':
            return PythonLoader(file_path)
        else:
            # 默认使用文本加载器
            return TextLoader(file_path, encoding='utf-8')

    def _create_rag_chain(self, path: str, domain_id: str) -> RetrievalQA:
        """
        创建RAG链
        
        Args:
            path: 文档路径（可以是文件或目录）
            domain_id: 领域ID，用于创建独立的向量存储
            
        Returns:
            RetrievalQA链
        """
        # 创建向量存储（支持持久化）
        domain_persist_directory = os.path.join(self.persist_directory,
                                                domain_id)
        os.makedirs(domain_persist_directory, exist_ok=True)

        # 检查是否已存在向量数据库
        if os.path.exists(
                os.path.join(domain_persist_directory, 'chroma.sqlite3')):
            print(f"加载现有的向量数据库: {domain_persist_directory}")
            # 加载现有的向量数据库
            vectorstore = Chroma(persist_directory=domain_persist_directory,
                                 embedding_function=self.embeddings)
        else:
            print(f"创建新的向量数据库: {domain_persist_directory}")
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

            # 创建新的向量数据库
            vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=self.embeddings,
                persist_directory=domain_persist_directory)
            # 持久化数据
            vectorstore.persist()

        # 创建检索链
        retriever_config = self.config.get("retriever", {})
        search_kwargs = retriever_config.get("search_kwargs", {"k": 4})

        # 创建检索器，支持过滤器
        retriever = vectorstore.as_retriever(search_type=retriever_config.get(
            "search_type", "similarity"),
                                             search_kwargs=search_kwargs)

        # 定义提示模板 - 使用ChatPromptTemplate支持更复杂的对话
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                '请根据以下上下文回答问题：{context}',
            ),
            MessagesPlaceholder(variable_name="messages"),
        ])

        # 创建RAG链 - 使用ConversationalRetrievalChain来支持ChatPromptTemplate
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

    def list_domains(self) -> List[Dict[str, str]]:
        """
        列出所有领域
        
        Returns:
            领域列表
        """
        domains = []
        for domain_id in self.rag_chains:
            domains.append({
                "id": domain_id,
                "description": f"{domain_id} 领域知识库"
            })
        return domains

    def load_all_domains_from_config(self) -> None:
        """
        从配置文件加载所有领域
        """
        domains_config = self.config.get("domains", {})
        for domain_id, domain_info in domains_config.items():
            path = domain_info.get("path")
            description = domain_info.get("description", "")
            self.add_domain(domain_id, path, description)
