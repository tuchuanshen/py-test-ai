from langchain_community.chat_models import ChatTongyi
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import BaseTool
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.document_loaders import (TextLoader, PDFMinerLoader,
                                        UnstructuredWordDocumentLoader,
                                        UnstructuredExcelLoader, CSVLoader,
                                        PythonLoader)
from typing import Type, Optional
from pydantic import Field, BaseModel
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('./../.env')


def get_llm():
    # 获取千问API密钥
    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
    # 初始化千问模型
    llm = ChatTongyi(api_key=dashscope_api_key, model="qwen-turbo")
    return llm


class FileLoadInput(BaseModel):
    file_path: str = Field(description="要加载的文件路径")
    question: str = Field(description="用户提出的问题")


class RAGTool(BaseTool):
    name: str = "rag_tool"
    description: str = "用于读取文件并基于文件内容回答问题的RAG工具"
    args_schema: Type[BaseModel] = FileLoadInput

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

    def _run(self, file_path: str, question: str) -> str:
        """执行RAG流程"""
        try:
            # 1. 加载文档
            if not os.path.exists(file_path):
                return f"错误：文件 {file_path} 不存在"

            loader = self._get_loader(file_path)
            documents = loader.load()

            # 2. 分割文本
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
            texts = text_splitter.split_documents(documents)

            # 3. 创建向量嵌入
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2")

            # 4. 创建向量存储
            vectorstore = Chroma.from_documents(
                texts, embeddings, collection_name="rag_collection")

            # 5. 创建检索器
            retriever = vectorstore.as_retriever(search_type="similarity",
                                                 search_kwargs={"k": 4})

            # 6. 创建RAG链
            llm = get_llm()
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True)

            # 7. 执行问答
            result = qa_chain({"query": question})

            # 清理向量存储
            vectorstore.delete_collection()

            return result["result"]

        except Exception as e:
            return f"处理文件时出错: {str(e)}"


# 改进的提示模板
def get_rag_prompt():
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个有用的助手，可以使用工具读取文件并基于文件内容回答问题。
        当用户要求你读取文件并回答相关问题时，请使用rag_tool工具。"""), ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    return prompt


if __name__ == "__main__":
    # 创建工具
    tools = [RAGTool()]

    # 获取LLM
    llm = get_llm()

    # 获取提示模板
    prompt = get_rag_prompt()

    # 初始化Agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # 示例使用
    print("RAG系统已启动")
    print("您可以询问类似以下的问题：")
    print("- 请读取data.txt文件并告诉我其中的主要内容")
    print("- 请分析report.pdf文件中的关键数据")
    print("- 请从config.py中提取配置信息并解释")

    while True:
        query = input("\n请输入您的问题（输入'退出'结束）：")
        if query.lower() == '退出':
            break

        response = agent_executor.invoke({"input": query})
        print(f"回答: {response['output']}")
