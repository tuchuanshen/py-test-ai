from rag_op import retriever_tool_get,RAGWorkflow
from local_llm import local_llm_get, get_llm
from wx_op import extract_user_messages
from ui_auto_wechat import WeChat
from listener_manager import ListenerManager
from local_log import (LogLevel, debug_log, info_log, error_log, set_logger)
import os, sys, time

def wx_msg_handler(wx_chat:WeChat, contact_name, messages):
    print(f"[自动回复] 收到来自 {contact_name} 的消息:", messages)
    
    # 提取并打印用户发送的消息
    user_messages = extract_user_messages(messages)
    print("提取的用户消息:", user_messages)
    wx_chat.send_msg(contact_name, text="hehele", search_user=True)

def wx_auto_reply():
    wechat_path = "D:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe"
    #wechat_path = "C:\\Program Files\\Tencent\\WeChat\\WeChat.exe"

    # 初始化微信对象
    wechat = WeChat(wechat_path, locale="zh-CN")

    # 初始化监听管理器
    listener_manager = ListenerManager(wechat)

    # 1. 添加初始监听对象
    print("=== 添加初始监听对象 ===")
    # 使用默认消息处理函数
    listener_manager.add_listener("沈圳", wx_msg_handler)
    listener_manager.start_global_listening(check_interval=5)
    
    set_logger(min_level=LogLevel.DEBUG)
    #llm = local_llm_get()
    llm = get_llm()
    while True:
        time.sleep(10)

    # print("\n支持的用户类型: default, technical, business")
    # user_type = input("请输入用户类型（输入'退出'结束）：")
    # if user_type.lower() == '退出':
    #     return
    user_type = "default"
    # 使用工作流方式，初始化时指定用户类型
    # workflow = RAGWorkflow(llm, user_type)

    # debug_log("RAG工作流准备就绪")


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
    wx_auto_reply()
