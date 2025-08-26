# test_dmx.py
from langchain.llms import Tongyi
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

# 从环境变量获取API密钥
QIAN_WEN_KEY = os.getenv("QIAN_WEN_KEY")

# 验证API密钥是否存在
if not QIAN_WEN_KEY:
    raise ValueError("QIAN_WEN_KEY 未在 .env 文件中设置")

# 设置API密钥
os.environ["TONGYI_API_KEY"] = QIAN_WEN_KEY
os.environ["DASHSCOPE_API_KEY"] = QIAN_WEN_KEY

class QwenQAModel:
    def __init__(self):
        # 初始化千问大模型
        self.llm = Tongyi(
            model_name="qwen-turbo",  # 或者使用 qwen-turbo, qwen-max 等
            temperature=0.7,
            max_tokens=2048
        )
        
        # 创建问答提示模板
        self.qa_template = """
        你是一个智能问答助手。请根据以下提供的上下文信息回答问题。
        如果上下文信息不足以回答问题，请说明无法基于提供的信息回答该问题。
        
        上下文信息：
        {context}
        
        问题：{question}
        
        回答：
        """
        
        self.prompt = PromptTemplate(
            template=self.qa_template,
            input_variables=["context", "question"]
        )
        
        # 创建问答链
        self.qa_chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def answer_question(self, question: str, context: str = ""):
        """
        基于给定上下文回答问题
        
        Args:
            question (str): 用户问题
            context (str): 上下文信息
            
        Returns:
            str: 模型回答
        """
        response = self.qa_chain.run({
            "context": context,
            "question": question
        })
        return response
    
    def answer_question_with_docs(self, question: str, documents):
        """
        使用文档列表进行问答
        
        Args:
            question (str): 用户问题
            documents: 文档列表
            
        Returns:
            str: 模型回答
        """
        chain = load_qa_chain(self.llm, chain_type="stuff")
        response = chain.run(input_documents=documents, question=question)
        return response

def interactive_qa_loop():
    """
    交互式问答循环
    """
    # 初始化模型
    qa_model = QwenQAModel()
    
    print("=== 基于千问的智能问答系统 ===")
    print("输入 'quit' 或 'exit' 退出程序")
    print("输入 'docs' 进入文档问答模式")
    print("-" * 40)
    
    # 预设文档用于文档问答模式
    docs = [
        Document(page_content="阿里巴巴集团成立于1999年，由马云和他的团队在杭州创立。"),
        Document(page_content="阿里巴巴的主要业务包括电子商务、云计算、数字媒体及娱乐等。"),
        Document(page_content="阿里巴巴于2014年在纽约证券交易所上市。"),
        Document(page_content="人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。")
    ]
    
    mode = "normal"  # normal 或 docs
    
    while True:
        try:
            if mode == "normal":
                user_input = input("\n请输入问题 (输入 'docs' 切换到文档问答模式, 'quit' 退出): ")
            else:
                user_input = input("\n请输入问题 (输入 'normal' 切换到普通问答模式, 'quit' 退出): ")
            
            # 检查退出命令
            if user_input.lower() in ['quit', 'exit']:
                print("感谢使用，再见！")
                break
            
            # 检查模式切换命令
            if user_input.lower() == 'docs':
                mode = "docs"
                print("已切换到文档问答模式")
                continue
            elif user_input.lower() == 'normal':
                mode = "normal"
                print("已切换到普通问答模式")
                continue
            
            # 处理问题
            if mode == "normal":
                # 普通问答模式
                answer = qa_model.answer_question(user_input)
                print(f"\n回答: {answer}")
            else:
                # 文档问答模式
                answer = qa_model.answer_question_with_docs(user_input, docs)
                print(f"\n回答: {answer}")
                
        except KeyboardInterrupt:
            print("\n\n程序被用户中断，再见！")
            break
        except Exception as e:
            print(f"\n发生错误: {str(e)}")
            print("请重试或联系管理员")

def demo_qa_loop():
    """
    演示问答循环 - 预设几个问题进行演示
    """
    # 初始化模型
    qa_model = QwenQAModel()
    
    # 预设文档
    docs = [
        Document(page_content="Python是一种高级编程语言，由Guido van Rossum于1991年首次发布。"),
        Document(page_content="Python支持多种编程范式，包括面向对象、命令式、函数式和过程式编程。"),
        Document(page_content="Python的语法简洁明了，具有良好的可读性，使得它成为初学者学习编程的首选语言之一。")
    ]
    
    # 预设问题列表
    questions = [
        "什么是Python？",
        "Python是由谁创建的？",
        "为什么Python适合初学者？"
    ]
    
    print("=== 演示问答循环 ===")
    
    # 普通问答演示
    print("\n--- 普通问答演示 ---")
    context = "Python是一种高级编程语言，具有简洁的语法和良好的可读性。"
    for question in questions:
        answer = qa_model.answer_question(question, context)
        print(f"\n问题: {question}")
        print(f"回答: {answer}")
    
    # 文档问答演示
    print("\n--- 文档问答演示 ---")
    for question in questions:
        answer = qa_model.answer_question_with_docs(question, docs)
        print(f"\n问题: {question}")
        print(f"回答: {answer}")

# 使用示例
if __name__ == "__main__":
    print("请选择运行模式:")
    print("1. 交互式问答 (实时输入问题)")
    print("2. 演示问答 (预设问题回答)")
    
    choice = input("请输入选择 (1 或 2): ")
    
    if choice == "1":
        interactive_qa_loop()
    elif choice == "2":
        demo_qa_loop()
    else:
        print("无效选择，运行交互式问答模式")
        interactive_qa_loop()