"""RAG管理器"""
import os
from typing import Dict, Any, List, Optional
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


class RAGManager:
    """
    RAG管理器 - 管理多个领域的知识库
    """
    
    def __init__(self):
        self.rag_chains: Dict[str, RetrievalQA] = {}
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
    def add_domain(self, domain_id: str, doc_path: str, description: str = "") -> bool:
        """
        添加领域知识库
        
        Args:
            domain_id: 领域ID
            doc_path: 文档路径
            description: 领域描述
            
        Returns:
            是否添加成功
        """
        try:
            if not os.path.exists(doc_path):
                print(f"文档路径不存在: {doc_path}")
                return False
                
            # 创建RAG链
            rag_chain = self._create_rag_chain(doc_path)
            self.rag_chains[domain_id] = rag_chain
            print(f"成功添加领域: {domain_id}")
            return True
        except Exception as e:
            print(f"添加领域 {domain_id} 失败: {str(e)}")
            return False
            
    def _create_rag_chain(self, doc_path: str) -> RetrievalQA:
        """
        创建RAG链
        
        Args:
            doc_path: 文档路径
            
        Returns:
            RetrievalQA链
        """
        # 这里需要根据实际文档加载方式实现
        # 暂时返回一个空的RAG链
        pass
        
    def query(self, question: str, domain: str) -> Dict[str, Any]:
        """
        查询RAG系统
        
        Args:
            question: 问题
            domain: 领域ID
            
        Returns:
            查询结果
        """
        if domain not in self.rag_chains:
            return {
                "success": False,
                "error": f"未找到领域 {domain} 的知识库",
                "answer": ""
            }
            
        try:
            rag_chain = self.rag_chains[domain]
            result = rag_chain.invoke({"query": question})
            
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