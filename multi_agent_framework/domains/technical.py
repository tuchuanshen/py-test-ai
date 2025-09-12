"""技术文档领域RAG"""
from typing import Dict, Any, List
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import DirectoryLoader


class TechnicalRAG:
    """
    技术文档领域RAG - 处理技术相关问题
    """
    
    def __init__(self, doc_path: str):
        self.doc_path = doc_path
        self.rag_chain = None
        self._initialize_rag()
        
    def _initialize_rag(self) -> None:
        """初始化RAG链"""
        if not os.path.exists(self.doc_path):
            print(f"文档路径不存在: {self.doc_path}")
            return
            
        try:
            # 加载文档
            loader = DirectoryLoader(self.doc_path, glob="**/*.txt")
            documents = loader.load()
            
            if not documents:
                print(f"在路径 {self.doc_path} 中未找到文档")
                return
            
            # 分割文档
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=100,
                length_function=len
            )
            texts = text_splitter.split_documents(documents)
            
            # 创建向量存储
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            
            vectorstore = Chroma.from_documents(
                texts,
                embeddings,
                collection_name="technical_docs"
            )
            
            # 创建检索器
            retriever = vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
            
            # 创建提示词模板
            prompt_template = """
            你是一个技术专家，请根据以下技术文档内容回答问题。
            如果文档中没有相关信息，请说明无法从提供的文档中找到答案。
            
            技术文档内容:
            {context}
            
            问题: {question}
            
            请提供准确的技术解答:
            """
            
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            # 创建QA链
            try:
                from local_llm import get_llm
                llm = get_llm()
            except ImportError:
                # 如果无法导入local_llm，则使用一个模拟的LLM
                from langchain_community.chat_models import ChatOpenAI
                llm = ChatOpenAI(
                    base_url="http://127.0.0.1:8080/v1",
                    api_key="sk-my-local-key-12345",
                    temperature=0.7,
                    max_tokens=1000
                )
            
            self.rag_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": prompt}
            )
            
            print(f"技术文档RAG初始化成功，共处理 {len(texts)} 个文档块")
            
        except Exception as e:
            print(f"技术文档RAG初始化失败: {str(e)}")
            
    def query(self, question: str) -> Dict[str, Any]:
        """
        查询技术文档
        
        Args:
            question: 问题
            
        Returns:
            查询结果
        """
        if not self.rag_chain:
            return {
                "success": False,
                "error": "RAG链未初始化",
                "answer": ""
            }
            
        try:
            result = self.rag_chain.invoke({"query": question})
            
            return {
                "success": True,
                "answer": result.get("result", ""),
                "sources": result.get("source_documents", [])
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"查询失败: {str(e)}",
                "answer": ""
            }