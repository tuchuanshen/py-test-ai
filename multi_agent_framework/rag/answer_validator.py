"""答案验证器 - 用于验证RAG系统生成的答案与用户问题的相关性"""

from typing import Dict, Any, List, Tuple, Optional
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from numpy import ndarray


class AnswerValidator:
    """
    答案验证器 - 评估答案与问题的相关性
    """

    def __init__(self, llm=None):
        """
        初始化答案验证器
        
        Args:
            llm: 用于语义相关性评估的语言模型（可选）
        """
        self.llm = llm
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000,
                                                stop_words='english')

    def validate_answer(self,
                        question: str,
                        answer: str,
                        sources: Optional[List[Any]] = None) -> Dict[str, Any]:
        """
        验证答案与问题的相关性
        
        Args:
            question: 用户问题
            answer: RAG系统生成的答案
            sources: 检索到的源文档（可选）
            
        Returns:
            包含相关性评估结果的字典
        """
        # 1. 基于TF-IDF的相似度计算
        tfidf_similarity = self._calculate_tfidf_similarity(question, answer)

        # 2. 基于语义的评估（如果有LLM）
        semantic_evaluation = None
        if self.llm:
            semantic_evaluation = self._evaluate_semantic_relevance(
                question, answer)

        # 3. 基于源文档的验证（如果有源文档）
        source_based_validation = None
        if sources:
            source_based_validation = self._validate_against_sources(
                question, answer, sources)

        # 综合评分
        overall_score = self._calculate_overall_score(tfidf_similarity,
                                                      semantic_evaluation,
                                                      source_based_validation)

        return {
            "question": question,
            "answer": answer,
            "tfidf_similarity": tfidf_similarity,
            "semantic_evaluation": semantic_evaluation,
            "source_based_validation": source_based_validation,
            "overall_score": overall_score,
            "is_relevant": overall_score > 0.5  # 阈值可调整
        }

    def _calculate_tfidf_similarity(self, question: str, answer: str) -> float:
        """
        计算问题和答案之间的TF-IDF相似度
        
        Args:
            question: 用户问题
            answer: 生成的答案
            
        Returns:
            相似度分数 (0-1)
        """
        try:
            # 计算TF-IDF向量
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(
                [question, answer])

            # 计算余弦相似度
            similarity_matrix: ndarray = cosine_similarity(
                tfidf_matrix[0], tfidf_matrix[1])
            similarity = similarity_matrix[0][0]

            return float(similarity)
        except Exception as e:
            print(f"TF-IDF相似度计算出错: {e}")
            return 0.0

    def _evaluate_semantic_relevance(self, question: str,
                                     answer: str) -> Dict[str, Any]:
        """
        使用LLM评估问题和答案之间的语义相关性
        
        Args:
            question: 用户问题
            answer: 生成的答案
            
        Returns:
            语义评估结果
        """
        if not self.llm:
            return {
                "score": 0.5,  # 默认中等分数
                "reasoning": "未提供LLM"
            }

        try:
            # 构建提示模板
            prompt_template = PromptTemplate.from_template("""
            请评估以下问题和答案之间的相关性，并给出1-10分的评分：
            
            问题: {question}
            答案: {answer}
            
            评估标准：
            1. 答案是否直接回答了问题
            2. 答案是否与问题主题相关
            3. 答案是否有用且准确
            
            请严格按照以下格式回复：
            评分: [分数]
            理由: [简要说明评分原因]
            """)

            # 调用LLM进行评估
            prompt = prompt_template.format(question=question, answer=answer)
            response = self.llm.invoke([HumanMessage(content=prompt)])

            # 解析响应
            response_text = response.content if hasattr(
                response, 'content') else str(response)

            # 简单解析评分（实际应用中可以更复杂）
            score = 5  # 默认评分
            if "评分:" in response_text:
                try:
                    score_part = response_text.split("评分:")[1].split()[0]
                    score = int(score_part)
                except:
                    pass

            return {
                "score": score / 10.0,  # 转换为0-1范围
                "reasoning": response_text
            }
        except Exception as e:
            print(f"语义相关性评估出错: {e}")
            return {
                "score": 0.5,  # 默认中等分数
                "reasoning": "评估失败"
            }

    def _validate_against_sources(self, question: str, answer: str,
                                  sources: List[Any]) -> Dict[str, Any]:
        """
        基于源文档验证答案的相关性和支持度
        
        Args:
            question: 用户问题
            answer: 生成的答案
            sources: 检索到的源文档
            
        Returns:
            源文档验证结果
        """
        try:
            # 提取源文档内容
            source_contents = [
                doc.page_content if hasattr(doc, 'page_content') else str(doc)
                for doc in sources[:3]
            ]  # 只考虑前3个源文档

            # 计算答案与源文档的相似度
            all_contents = [answer] + source_contents
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(all_contents)

            # 计算答案与每个源文档的相似度
            similarities = []
            for i in range(1, len(all_contents)):
                similarity_matrix: ndarray = cosine_similarity(
                    tfidf_matrix[0], tfidf_matrix[i])
                similarity = similarity_matrix[0][0]
                similarities.append(float(similarity))

            # 平均相似度
            avg_similarity = np.mean(similarities) if similarities else 0.0

            return {
                "supported_by_sources": avg_similarity > 0.1,  # 阈值可调整
                "average_similarity_to_sources": avg_similarity,
                "number_of_sources": len(sources)
            }
        except Exception as e:
            print(f"源文档验证出错: {e}")
            return {
                "supported_by_sources": False,
                "average_similarity_to_sources": 0.0,
                "number_of_sources": len(sources)
            }

    def _calculate_overall_score(
            self, tfidf_score: float, semantic_eval: Optional[Dict[str, Any]],
            source_validation: Optional[Dict[str, Any]]) -> float:
        """
        计算综合相关性评分
        
        Args:
            tfidf_score: TF-IDF相似度分数
            semantic_eval: 语义评估结果
            source_validation: 源文档验证结果
            
        Returns:
            综合评分 (0-1)
        """
        weights = {"tfidf": 0.4, "semantic": 0.4, "source": 0.2}

        score = tfidf_score * weights["tfidf"]

        if semantic_eval:
            score += semantic_eval["score"] * weights["semantic"]

        if source_validation:
            # 如果答案得到源文档支持，加分
            if source_validation["supported_by_sources"]:
                score += source_validation[
                    "average_similarity_to_sources"] * weights["source"]
            else:
                # 如果没有得到源文档支持，减分
                score -= 0.1

        # 确保分数在0-1范围内
        return max(0.0, min(1.0, score))


def create_answer_validator(llm=None) -> AnswerValidator:
    """
    创建答案验证器实例的工厂函数
    
    Args:
        llm: 用于语义相关性评估的语言模型（可选）
        
    Returns:
        AnswerValidator实例
    """
    return AnswerValidator(llm)
