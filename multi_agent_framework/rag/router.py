"""
RAG路由模块
提供基于语义相似度和LLM的智能路由选择功能
"""

import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import logging
from typing import Dict, Any

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SemanticRAGRouter:
    """
    基于语义相似度的RAG路由选择器
    使用嵌入模型计算问题与各领域描述的相似度
    """

    def __init__(self, rag_manager):
        """
        初始化语义路由选择器
        
        Args:
            rag_manager: RAG管理器实例
        """
        self.rag_manager = rag_manager
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2")

        # 获取各领域的描述
        domains_config = rag_manager.config.get("domains", {})
        self.domain_descriptions = {}
        for domain_id, domain_info in domains_config.items():
            self.domain_descriptions[domain_id] = domain_info.get(
                "description", "")

        # 预计算领域描述的嵌入向量
        self.domain_embeddings = {}
        for domain_id, description in self.domain_descriptions.items():
            self.domain_embeddings[domain_id] = self.embeddings.embed_query(
                description)

        logger.info(f"语义路由初始化完成，加载了{len(self.domain_descriptions)}个领域")

    def route_question(self, question):
        """
        使用语义相似度选择最合适的领域
        
        Args:
            question: 用户问题
            
        Returns:
            最匹配的领域ID
        """
        # 计算问题的嵌入向量
        question_embedding = self.embeddings.embed_query(question)

        # 计算与各领域描述的相似度
        similarities: Dict[str, float] = {}
        for domain_id, domain_embedding in self.domain_embeddings.items():
            similarity = cosine_similarity(
                np.array(question_embedding).reshape(1, -1),
                np.array(domain_embedding).reshape(1, -1))[0][0]
            similarities[domain_id] = float(similarity)

        # 返回相似度最高的领域
        best_domain = max(similarities, key=lambda x: similarities[x])
        logger.info(
            f"语义路由选择领域: {best_domain} (相似度: {similarities[best_domain]:.4f})")
        return best_domain


class LLMBasedRAGRouter:
    """
    基于LLM的RAG路由选择器
    使用大型语言模型来决定应该使用哪个领域
    """

    def __init__(self, rag_manager, llm):
        """
        初始化LLM路由选择器
        
        Args:
            rag_manager: RAG管理器实例
            llm: 大型语言模型实例
        """
        self.rag_manager = rag_manager
        self.llm = llm

        # 构建领域信息描述
        domains_config = rag_manager.config.get("domains", {})
        domain_info = []
        for domain_id, domain_info_dict in domains_config.items():
            domain_info.append(
                f"- {domain_id}: {domain_info_dict.get('description', '')}")

        self.domains_description = "\n".join(domain_info)

        # 创建路由提示模板
        routing_template = """
你是一个智能路由助手，需要根据用户问题选择最合适的知识库领域。

可用的领域包括:
{domains}

请分析用户问题，并选择最相关的领域。只返回领域名称，不要包含其他内容。

用户问题: {question}

最相关的领域是: """

        self.routing_prompt = PromptTemplate(
            template=routing_template, input_variables=["domains", "question"])

        self.routing_chain = LLMChain(llm=self.llm, prompt=self.routing_prompt)
        logger.info(f"LLM路由初始化完成，加载了{len(domains_config)}个领域")

    def route_question(self, question):
        """
        使用LLM选择最合适的领域
        
        Args:
            question: 用户问题
            
        Returns:
            最匹配的领域ID
        """
        try:
            result = self.routing_chain.invoke({
                "domains": self.domains_description,
                "question": question
            })

            selected_domain = result["text"].strip()
            # 验证选择的领域是否有效
            domains_config = self.rag_manager.config.get("domains", {})
            if selected_domain in domains_config:
                logger.info(f"LLM路由选择领域: {selected_domain}")
                return selected_domain
            else:
                # 如果LLM返回无效领域，使用默认领域
                default_domain = self.rag_manager.config.get(
                    "default_domain", "technical")
                logger.warning(
                    f"LLM选择了无效领域: {selected_domain}，回退到默认领域: {default_domain}")
                return default_domain
        except Exception as e:
            # 出现错误时回退到默认领域
            default_domain = self.rag_manager.config.get(
                "default_domain", "technical")
            logger.error(f"LLM路由出现错误: {e}，回退到默认领域: {default_domain}")
            return default_domain


class HybridRAGRouter:
    """
    混合RAG路由选择器
    结合语义相似度和LLM的路由策略
    """

    def __init__(self, rag_manager, llm=None):
        """
        初始化混合路由选择器
        
        Args:
            rag_manager: RAG管理器实例
            llm: 大型语言模型实例（可选）
        """
        self.rag_manager = rag_manager
        self.llm = llm

        # 初始化各种路由方法
        self.semantic_router = SemanticRAGRouter(rag_manager)
        self.llm_router = LLMBasedRAGRouter(rag_manager, llm) if llm else None

        logger.info("混合路由初始化完成")

    def route_question(self, question, strategy="hybrid"):
        """
        使用指定策略路由问题
        
        Args:
            question: 用户问题
            strategy: 路由策略 ("semantic", "llm", "hybrid")
            
        Returns:
            最匹配的领域ID
        """
        if strategy == "semantic":
            return self.semantic_router.route_question(question)
        elif strategy == "llm" and self.llm_router:
            return self.llm_router.route_question(question)
        elif strategy == "hybrid":
            # 默认使用语义路由
            semantic_domain = self.semantic_router.route_question(question)

            # 如果有LLM，可以进一步确认
            if self.llm_router:
                llm_domain = self.llm_router.route_question(question)
                # 如果两种方法结果一致，更有信心
                if semantic_domain == llm_domain:
                    logger.info(f"混合路由: 语义和LLM结果一致，选择领域: {semantic_domain}")
                    return semantic_domain
                else:
                    # 如果结果不一致，优先使用LLM的结果
                    logger.info(
                        f"混合路由: 语义路由选择{semantic_domain}，LLM路由选择{llm_domain}，优先使用LLM结果"
                    )
                    return llm_domain
            else:
                return semantic_domain
        else:
            # 默认策略
            default_domain = self.rag_manager.config.get(
                "default_domain", "technical")
            logger.info(f"使用默认领域: {default_domain}")
            return default_domain
