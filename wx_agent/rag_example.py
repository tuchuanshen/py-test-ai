"""
RAG功能完整使用示例
演示如何在PromptChat中集成和使用RAG功能
"""

import os
from prompt_chat import create_chat_session
from rag_extension import RAGExtension

def create_sample_documents():
    """创建示例文档用于测试"""
    # 创建示例文档目录
    os.makedirs("./sample_docs/tech", exist_ok=True)
    os.makedirs("./sample_docs/health", exist_ok=True)
    os.makedirs("./sample_docs/finance", exist_ok=True)
    
    # 技术领域文档
    tech_doc = """
    人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。
    机器学习是人工智能的一个子领域，它使计算机能够从数据中学习并做出决策。
    深度学习是机器学习的一个分支，使用神经网络来模拟人脑的工作方式。
    自然语言处理（NLP）是AI的一个领域，专注于计算机与人类语言之间的交互。
    神经网络是由相互连接的节点（或称"神经元"）组成的计算系统，这些节点松散地基于人脑的神经元。
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
    均衡饮食应包含蛋白质、碳水化合物、脂肪、维生素和矿物质。
    每天至少喝8杯水以保持身体水分充足。
    """
    
    with open("./sample_docs/health/health_tips.txt", "w", encoding="utf-8") as f:
        f.write(health_doc)
    
    # 金融领域文档
    finance_doc = """
    投资是指将资金投入到某种资产中，期望在未来获得收益。
    股票代表对公司所有权的一部分，购买股票即成为公司的股东。
    债券是借款人发行的债务工具，购买债券即成为债权人。
    分散投资是降低风险的重要策略，不要把所有资金投入到单一资产中。
    复利是指投资收益再投资产生的收益，长期来看具有强大的增长潜力。
    应急基金是应对突发事件的资金储备，通常建议储备3-6个月的生活费用。
    通货膨胀会降低货币的购买力，因此投资回报率应超过通胀率。
    """
    
    with open("./sample_docs/finance/finance_basics.txt", "w", encoding="utf-8") as f:
        f.write(finance_doc)

def setup_rag_system():
    """设置RAG系统"""
    # 创建RAG扩展实例
    rag_extension = RAGExtension()
    
    # 添加不同领域的文档和关键词
    rag_extension.add_domain(
        "technology", 
        "./sample_docs/tech", 
        ["人工智能", "AI", "机器学习", "深度学习", "神经网络", "算法"]
    )
    
    rag_extension.add_domain(
        "health", 
        "./sample_docs/health", 
        ["健康", "饮食", "锻炼", "睡眠", "营养", "运动", "健身"]
    )
    
    rag_extension.add_domain(
        "finance", 
        "./sample_docs/finance", 
        ["投资", "股票", "基金", "债券", "理财", "金融", "财务"]
    )
    
    return rag_extension

def main():
    """主函数"""
    print("RAG功能集成演示")
    print("=" * 50)
    
    # 创建示例文档
    print("正在创建示例文档...")
    create_sample_documents()
    print("示例文档创建完成")
    
    # 创建聊天实例
    print("正在创建聊天实例...")
    chatbot = create_chat_session()
    
    # 设置RAG系统
    print("正在设置RAG系统...")
    rag_extension = setup_rag_system()
    
    # 启用RAG功能
    print("正在启用RAG功能...")
    chatbot.enable_rag(rag_extension)
    print("RAG功能已启用")
    
    print("\n" + "=" * 50)
    print("RAG功能已集成到聊天系统中")
    print("当您提到相关领域关键词时，系统会自动检索相关文档并基于文档内容回答")
    print("支持的领域:")
    print("1. 技术领域: 人工智能、机器学习等")
    print("2. 健康领域: 健康饮食、锻炼等")
    print("3. 金融领域: 投资、股票等")
    print("=" * 50)
    
    # 交互式对话
    print("\n开始对话 (输入 'quit' 或 'exit' 退出):")
    session_id = "rag_demo_session"
    
    while True:
        try:
            user_input = input("\n你: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("助手: 再见！")
                break
            
            if not user_input:
                continue
            
            # 进行对话（自动使用RAG功能）
            response = chatbot.chat(user_input, session_id)
            print(f"助手: {response}")
            
        except KeyboardInterrupt:
            print("\n\n助手: 再见！")
            break
        except Exception as e:
            print(f"\n助手: 发生错误: {str(e)}")

# 测试不同领域的查询
def test_rag_functionality():
    """测试RAG功能"""
    print("测试RAG功能")
    print("=" * 30)
    
    # 创建示例文档
    create_sample_documents()
    
    # 创建聊天实例
    chatbot = create_chat_session()
    
    # 设置RAG系统
    rag_extension = setup_rag_system()
    
    # 启用RAG功能
    chatbot.enable_rag(rag_extension)
    
    # 测试查询
    test_queries = [
        "什么是人工智能？",
        "如何保持健康饮食？",
        "投资股票的基本原理是什么？",
        "今天天气怎么样？"  # 这个查询不涉及特定领域
    ]
    
    session_id = "test_session"
    
    for query in test_queries:
        print(f"\n查询: {query}")
        response = chatbot.chat(query, session_id)
        print(f"回复: {response}")

if __name__ == "__main__":
    # 运行主程序
    main()
    
    # 如果想要单独测试RAG功能，可以取消下面的注释
    # test_rag_functionality()