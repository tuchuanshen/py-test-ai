from rag_op import retriever_tool_get
from local_llm import local_llm_get
#from wx_op import wx_start
from local_log import (LogLevel, debug_log, set_logger)

from local_log import (LogLevel, debug_log, info_log, error_log, set_logger)
import os, sys


def test_talk():

    llm = local_llm_get()
    debug_log("local_llm_get ready", llm)

    heart_talk = retriever_tool_get(r"D:\tuchuan\tc_test\py-test-ai\wx_agent",
                                    llm)

    if heart_talk is None:
        error_log("heart_talk 初始化失败")
        return

    while True:
        query = input("\n请输入您的问题（输入'退出'结束）：")
        if query.lower() == '退出':
            break
        try:
            response = heart_talk.invoke({"query": query})
            print(f"回答: {response}")
        except Exception as e:
            error_log(f"问答过程中出错: {str(e)}")


if __name__ == "__main__":
    test_talk()
