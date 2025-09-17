"""
基于配置文件的RAG Agent使用示例
演示从配置文件读取路径和参数的完整使用方法
"""
import stat
import sys
import os

from sympy import im

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multi_agent_framework.agents.rag_agent import RAGAgent
from multi_agent_framework.rag.manager import RAGManager
from multi_agent_framework.rag.router import HybridRAGRouter
from langchain_openai import ChatOpenAI
from wx_agent.local_llm import local_llm_get


def main():
    # 初始化LLM（这里使用ChatOpenAI，也可以替换为其他LLM）
    # 注意：需要设置OPENAI_API_KEY环境变量
    try:
        #llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        llm = local_llm_get()
        print("成功初始化ChatOpenAI")
    except Exception as e:
        print(f"警告：无法初始化ChatOpenAI: {e}")
        print("将使用None作为LLM，这可能会影响RAG功能")
        llm = None

    # 初始化RAG管理器，配置文件路径会自动从rag目录下读取
    config_path = os.path.join(os.path.dirname(__file__), "..", "rag",
                               "config.json")
    print(f"正在加载配置文件: {config_path}")

    rag_manager = RAGManager(llm=llm, config_path=config_path)

    # 从配置文件加载所有领域
    print("正在从配置文件加载所有领域...")
    rag_manager.load_all_domains_from_config()
    rag_reoute = HybridRAGRouter(rag_manager, llm)

    # 检查加载的领域
    domains = rag_manager.list_domains()
    print(f"已加载的领域: {[d['id'] for d in domains]}")

    if not domains:
        print("没有成功加载任何领域，程序退出")
        return

    # 创建RAG智能体
    rag_agent = RAGAgent("rag_001", "ConfigurableRAGAgent", rag_manager)

    while True:
        question = input("请输入问题（输入q退出程序）：")
        if question.lower().startswith('q') or question.lower().startswith(
                'e'):
            print("程序已退出")
            break
        state = {
            "question": question,
            "domain": rag_reoute.route_question(question),
            "messages": []
        }

        print(f"使用 {state['domain']}领域 回答 问题: {question}")
        # 处理问题（不指定领域，使用默认领域）
        result_state = rag_agent.process(state)

        # 输出结果
        print(f"答案: {result_state}")


if __name__ == "__main__":
    main()
