import re
from rag_op import retriever_tool_get, RAGWorkflow
from local_llm import local_llm_get, get_llm
from ui_auto_wechat import WeChat
from listener_manager import ListenerManager
from local_log import (LogLevel, debug_log, info_log, error_log, set_logger)
import os, sys, time
from wx_op import extract_user_messages
from ai_talk import create_chat_session
from langchain_core.messages import HumanMessage


def format_messages_as_dialogue(messages, username=None):
    """
    将消息列表格式化为易读的对话格式
    
    Args:
        messages: 消息列表，每个元素为(消息类型, 发送者, 消息内容)的元组
        username: 当前用户名，如果发送者是该用户则显示为"你"
        
    Returns:
        str: 格式化后的对话字符串
    """
    dialogue_lines = []
    
    for msg_type, sender, content in messages:
        # 只处理用户发送的消息
        if msg_type == '用户发送' and sender and content:
            # 如果发送者是当前用户，显示为"你"
            display_sender = "我" if username and sender == username else sender
            dialogue_lines.append(f"{display_sender}：{content}")
        # 时间信息可以按需要处理，这里暂时忽略
    
    return "\n".join(dialogue_lines)


def make_wx_msg_handler(talk_ai):

    def wx_msg_handler(wx_chat: WeChat, contact_name, new_msg, messages):
        if new_msg:
            print(f"收到来自 {contact_name} 的新消息:")
        else:
            print(f"获取 {contact_name} 的历史消息：")
        
        # 格式化为对话形式，将联系人名称显示为"你"
        dialogue = format_messages_as_dialogue(messages, username="土川啊")
        print(dialogue)
        ai_resp = talk_ai.chat(dialogue)
        #ai_resp = workflow.get_response(",".join(user_messages))["answer"]
        print("[自动回复] 回复:", ai_resp)
        wx_chat.send_msg(contact_name, text=ai_resp, search_user=True)
        wx_chat.press_minimize()

    return wx_msg_handler


def wx_rag_reply():
    wechat_path = "D:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe"
    #wechat_path = "C:\\Program Files\\Tencent\\WeChat\\WeChat.exe"

    # 初始化微信对象
    wechat = WeChat(wechat_path, locale="zh-CN")

    # 初始化监听管理器
    listener_manager = ListenerManager(wechat)

    # 1. 添加初始监听对象
    print("=== 添加初始监听对象 ===")

    #llm = local_llm_get()
    llm = get_llm()
    user_type = "default"
    workflow = RAGWorkflow(llm, user_type)
    my_handler = make_wx_msg_handler(workflow)
    # 使用默认消息处理函数
    listener_manager.add_listener("沈圳", my_handler)
    listener_manager.start_global_listening(check_interval=5)

    set_logger(min_level=LogLevel.DEBUG)
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


def wx_prompt_talk():
    talk_ai = create_chat_session()
    
    wechat_path = "D:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe"

    # 初始化微信对象
    wechat = WeChat(wechat_path, locale="zh-CN")

    # 初始化监听管理器
    listener_manager = ListenerManager(wechat)

    my_handler = make_wx_msg_handler(talk_ai)
    # 使用默认消息处理函数
    listener_manager.add_listener("沈圳", my_handler)
    listener_manager.start_global_listening(check_interval=5)

    set_logger(min_level=LogLevel.DEBUG)
    while True:
        time.sleep(10)


if __name__ == "__main__":
    wx_prompt_talk()
