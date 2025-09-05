from langchain_community.document_loaders import DirectoryLoader

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from local_log import info_log
from sympy import false
from pathlib import Path

from langchain_community.chat_models import ChatTongyi
from langchain.tools import BaseTool
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

from langchain_community.document_loaders import (
    TextLoader, PDFMinerLoader, UnstructuredWordDocumentLoader,
    UnstructuredExcelLoader, CSVLoader, PythonLoader)

from typing import Type, Optional
from pydantic import Field, BaseModel
import os, sys

from local_llm import local_llm_get

from local_log import (LogLevel, debug_log, info_log, warning_log, error_log,
                       set_logger)


def load_doc_dir(dir_path, file_type=".txt"):
    # 自动加载目录下所有支持的文件
    loader = DirectoryLoader(
        dir_path,
        glob=f"**/*{file_type}",  # 匹配所有文件
        show_progress=false)
    docs = loader.load()
    return docs


def retriever_tool_get(dir_path, llm):

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
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                           chain_type="stuff",
                                           retriever=retriever,
                                           return_source_documents=True)
    info_log(f"QA模型加载完成")
    return qa_chain


def test_talk():
    set_logger(min_level=LogLevel.DEBUG)
    llm = local_llm_get()
    debug_log("local_llm_get ready", llm)
    heart_talk = retriever_tool_get(r"D:\tuchuan\tc_test\py-test-ai\wx_agent",
                                    llm)

    debug_log("heart_talk ready", heart_talk)
    while True:
        query = input("\n请输入您的问题（输入'退出'结束）：")
        if query.lower() == '退出':
            break
        response = heart_talk.invoke(query)
        print(f"回答: {response}")


if __name__ == "__main__":
    test_talk()
