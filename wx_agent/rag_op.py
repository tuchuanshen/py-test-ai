from langchain_community.document_loaders import DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatTongyi
from langchain.tools import BaseTool
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain

from langchain_community.document_loaders import (
    TextLoader, PDFMinerLoader, UnstructuredWordDocumentLoader,
    UnstructuredExcelLoader, CSVLoader, PythonLoader)

from typing import Type, Optional
from pydantic import Field, BaseModel
import os, sys
import json

from local_llm import local_llm_get
from local_log import (LogLevel, debug_log, info_log, warning_log, error_log,
                       set_logger)

# 配置文件路径
CONFIG_FILE_PATH = r"D:\tuchuan\tc_test\py-test-ai\wx_agent\rag_config.json"

# 定义提示词模板

DETAILED_PROMPT_TEMPLATE = """
你是一个智能助手，请仔细阅读以下文档内容，并根据文档内容回答用户问题。

文档内容:
{context}

用户问题: {question}

请按照以下步骤回答:
1. 首先分析问题类型和关键信息
2. 在文档中查找相关信息
3. 组织语言，提供准确、完整的回答
4. 如果文档中没有相关信息，请明确说明

回答:
"""

# 添加针对不同用户的提示词模板
USER_PROMPTS = {
    "default": DETAILED_PROMPT_TEMPLATE,
}

# 添加用户到文档路径的映射
USER_DOC_PATHS = {
    "default": r"D:\tuchuan\tc_test\py-test-ai\wx_agent",
}


def load_config():
    """从配置文件加载用户配置"""
    global USER_PROMPTS, USER_DOC_PATHS

    # 如果配置文件不存在，创建默认配置文件
    if not os.path.exists(CONFIG_FILE_PATH):
        default_config = {
            "users": {
                "default": {
                    "prompt_type": "default",
                    "doc_path": r"D:\tuchuan\tc_test\py-test-ai\wx_agent"
                }
            },
            "prompts": {
                "default": DETAILED_PROMPT_TEMPLATE
            }
        }

        # 创建配置文件目录（如果不存在）
        config_dir = os.path.dirname(CONFIG_FILE_PATH)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        with open(CONFIG_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=4)
        info_log(f"已创建默认配置文件: {CONFIG_FILE_PATH}")

    # 读取配置文件
    try:
        with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # 解析用户配置
        USER_DOC_PATHS.clear()
        USER_PROMPTS.clear()

        # 加载提示词模板
        if "prompts" in config:
            USER_PROMPTS.update(config["prompts"])

        # 加载用户配置
        if "users" in config:
            for user_type, user_config in config["users"].items():
                USER_DOC_PATHS[user_type] = user_config.get("doc_path", "")
                # 如果用户有自己的提示词模板，则使用该模板
                prompt_type = user_config.get("prompt_type", "default")
                if prompt_type in USER_PROMPTS:
                    # 已经在USER_PROMPTS中了，不需要额外处理
                    pass
                else:
                    # 如果配置中指定了提示词内容而不是类型
                    prompt_content = user_config.get("prompt_content")
                    if prompt_content:
                        USER_PROMPTS[user_type] = prompt_content

        info_log(f"配置文件加载成功: {CONFIG_FILE_PATH}")

    except Exception as e:
        error_log(f"配置文件加载失败: {e}")
        # 使用默认配置
        USER_PROMPTS.update({
            "default": DETAILED_PROMPT_TEMPLATE,
        })

        USER_DOC_PATHS.update(
            {"default": r"D:\tuchuan\tc_test\py-test-ai\wx_agent"})


def load_doc_dir(dir_path, file_type=".txt"):
    # 自动加载目录下所有支持的文件
    loader = DirectoryLoader(
        dir_path,
        glob=f"**/*{file_type}",  # 匹配所有文件
        show_progress=False)
    docs = loader.load()
    return docs


def retriever_tool_get(dir_path, llm, prompt_type="default"):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                   chunk_overlap=100,
                                                   length_function=len)
    info_log(f"文档加载中...")

    documents = load_doc_dir(dir_path)
    texts = text_splitter.split_documents(documents)
    info_log(f"文档加载完成，文本块数量为{len(texts)}")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2")

    info_log(f"向量库创建中...")
    vectorstore = Chroma.from_documents(texts,
                                        embeddings,
                                        collection_name="rag_collection")
    info_log(f"向量库加载中...")
    retriever = vectorstore.as_retriever(search_type="similarity",
                                         search_kwargs={"k": 4})
    info_log(f"向量库加载完成，向量库大小为{len(texts)}")

    # 根据提示词类型选择模板
    prompt_template = USER_PROMPTS.get(prompt_type, DETAILED_PROMPT_TEMPLATE)
    prompt = PromptTemplate(template=prompt_template,
                            input_variables=["context", "question"])

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt})

    info_log(f"QA模型加载完成")
    return qa_chain


def conversational_retriever_tool_get(dir_path, llm):
    """
    创建支持多轮对话的RAG系统
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                   chunk_overlap=100,
                                                   length_function=len)
    info_log(f"文档加载中...")

    documents = load_doc_dir(dir_path)
    texts = text_splitter.split_documents(documents)
    info_log(f"文档加载完成，文本块数量为{len(texts)}")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2")

    info_log(f"向量库创建中...")
    vectorstore = Chroma.from_documents(texts,
                                        embeddings,
                                        collection_name="rag_collection")
    info_log(f"向量库加载中...")
    retriever = vectorstore.as_retriever(search_type="similarity",
                                         search_kwargs={"k": 4})
    info_log(f"向量库加载完成，向量库大小为{len(texts)}")

    # 创建支持对话历史的Chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=retriever, return_source_documents=True)

    info_log(f"对话式QA模型加载完成")
    return qa_chain


# 添加工作流类来管理不同用户的RAG配置
class RAGWorkflow:

    def __init__(self, llm, user_type="default"):
        self.llm = llm
        self.user_type = user_type  # 添加用户类型属性
        self.user_chains = {}
        # 加载配置文件
        load_config()
        self._init_user_chains()

    def _init_user_chains(self):
        """为不同用户初始化RAG链"""
        for user_type, doc_path in USER_DOC_PATHS.items():
            if os.path.exists(doc_path):
                prompt_type = user_type
                self.user_chains[user_type] = retriever_tool_get(
                    doc_path, self.llm, prompt_type)

    def get_response(self, query):
        """根据初始化时指定的用户类型获取响应"""
        if self.user_type in self.user_chains:
            chain = self.user_chains[self.user_type]
            response = chain.invoke({"query": query})
            return response
        else:
            # 使用默认链
            chain = self.user_chains.get("default")
            if chain:
                response = chain.invoke({"query": query})
                return response
            else:
                return {"result": "未找到合适的问答链", "source_documents": []}

    def add_user_config(self, user_type, doc_path, prompt_type="default"):
        """动态添加用户配置"""
        if os.path.exists(doc_path):
            self.user_chains[user_type] = retriever_tool_get(
                doc_path, self.llm, prompt_type)


def test_talk():
    set_logger(min_level=LogLevel.DEBUG)
    llm = local_llm_get()
    debug_log("local_llm_get ready", llm)

    print("\n支持的用户类型: default, technical, business")
    user_type = input("请输入用户类型（输入'退出'结束）：")
    if user_type.lower() == '退出':
        return

    # 使用工作流方式，初始化时指定用户类型
    workflow = RAGWorkflow(llm, user_type)

    debug_log("RAG工作流准备就绪")
    chat_history = []

    while True:
        query = input("请输入您的问题（输入'退出'结束）：")
        if query.lower() == '退出':
            break

        response = workflow.get_response(query)
        print(f"回答: {response['result']}")

        # 添加循环思考功能：允许用户基于回答继续提问
        continue_chat = input("是否需要进一步了解？(y/n): ")
        while continue_chat.lower() == 'y':
            follow_up = input("请继续提问: ")
            follow_up_response = workflow.get_response(follow_up)
            print(f"回答: {follow_up_response['result']}")
            continue_chat = input("是否需要进一步了解？(y/n): ")


if __name__ == "__main__":
    test_talk()
