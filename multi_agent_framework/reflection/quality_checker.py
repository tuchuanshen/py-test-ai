"""质量检查反思器"""
from typing import Dict, Any
from .base import BaseReflector


class QualityCheckerReflector(BaseReflector):
    """
    质量检查反思器 - 检查答案质量并提出改进建议
    """
    
    def __init__(self, llm: Any):
        super().__init__("quality_checker", "检查答案质量")
        self.llm = llm
        
    def reflect(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        对答案进行质量检查
        
        Args:
            state: 当前状态
            
        Returns:
            反思后的状态
        """
        question = state.get("question", "")
        answer = state.get("answer", "")
        
        # 构建质量检查提示词
        prompt = f"""
        你是一个质量检查员，需要评估答案是否满足用户问题的要求。
        请检查以下内容：
        1. 答案是否准确回答了问题
        2. 答案是否完整
        3. 答案是否清晰易懂
        4. 是否存在事实错误
        
        问题: {question}
        答案: {answer}
        
        请按以下格式回复:
        评分: [1-10分]
        评价: [简要评价]
        改进建议: [如果需要改进，请提供具体建议，否则写"无需改进"]
        最终答案: [如果需要改进，请提供改进后的答案，否则写"无需改进"]
        """
        
        # 调用LLM进行质量检查
        response = self.llm.invoke(prompt)
        
        # 解析LLM响应
        response_text = response.content
        final_answer = answer  # 默认使用原答案
        
        # 简单解析响应（实际应用中应该更完善）
        if "最终答案:" in response_text:
            lines = response_text.split('\n')
            for line in lines:
                if line.startswith("最终答案:"):
                    suggested_answer = line.replace("最终答案:", "").strip()
                    if suggested_answer != "无需改进":
                        final_answer = suggested_answer
                    break
        
        # 更新状态
        updated_state = state.copy()
        updated_state["final_answer"] = final_answer
        updated_state["reflection_result"] = response_text
        
        return updated_state