"""RAG智能体"""
from typing import Dict, Any, Optional
from multi_agent_framework.agents.base import BaseAgent
from multi_agent_framework.rag.manager import RAGManager
from multi_agent_framework.rag.answer_validator import AnswerValidator
from langchain_core.messages import HumanMessage, AIMessage


class RAGAgent(BaseAgent):
    """
    RAG智能体 - 处理基于检索增强生成的知识问答任务
    """

    def __init__(self,
                 agent_id: str,
                 name: str,
                 rag_manager: RAGManager,
                 llm=None):
        super().__init__(agent_id, name, "处理基于RAG的知识问答任务")
        self.rag_manager = rag_manager
        self.answer_validator = AnswerValidator(llm)
        self.capabilities = ["knowledge_qa", "document_retrieval", "rag"]

    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理基于RAG的知识问答任务
        
        Args:
            state: 当前状态，应包含问题和可能的领域信息
            
        Returns:
            更新后的状态，包含答案和其他相关信息
        """
        # 获取问题、领域信息和过滤器
        question = state.get("question", "")
        domain = state.get("domain", None)
        filter = state.get("filter", None)

        # 获取额外的prompt变量（除了question、domain、filter之外的所有字段）
        extra_kwargs = {
            key: value
            for key, value in state.items()
            if key not in ["question", "domain", "filter"]
        }

        # 使用RAG管理器查询答案（如果未指定领域，将使用默认领域）
        result = self.rag_manager.query(question, domain, filter,
                                        **extra_kwargs)

        # 更新状态
        updated_state = state.copy()
        if result["success"]:
            # 将答案转换为AIMessage格式
            answer_content = result["answer"]
            updated_state["answer"] = AIMessage(content=answer_content)
            updated_state["sources"] = result.get("sources", [])

            # 验证答案相关性
            validation_result = self.answer_validator.validate_answer(
                question, answer_content, result.get("sources", []))
            updated_state["answer_validation"] = validation_result
        else:
            # 错误情况下也转换为AIMessage格式
            error_message = f"查询失败: {result.get('error', '未知错误')}"
            updated_state["answer"] = AIMessage(content=error_message)

            # 错误情况下的验证结果
            updated_state["answer_validation"] = {
                "question": question,
                "answer": error_message,
                "tfidf_similarity": 0.0,
                "semantic_evaluation": None,
                "source_based_validation": None,
                "overall_score": 0.0,
                "is_relevant": False
            }

        updated_state["needs_reflection"] = True
        updated_state["next_step"] = "reflect"

        return updated_state
