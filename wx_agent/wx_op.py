import time
import threading
from datetime import datetime, timedelta
import pythoncom
import sys
import os

# 添加easyChat-main目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
easychat_path = os.path.join(project_root, '..', 'easyChat-main')
sys.path.insert(0, os.path.abspath(easychat_path))

from ui_auto_wechat import WeChat
from typing import List
global WX

def extract_user_messages(messages):
    """
    从messages中提取用户发送的消息
    
    Args:
        messages: 包含消息信息的数组，每个元素是一个元组
                 格式如: [('时间信息', '', '12:02'), ('用户发送', '沈圳', '消息内容'), ...]
    
    Returns:
        list: 包含所有用户发送消息内容的列表
    """
    user_messages = []
    
    # 遍历所有消息
    for message in messages:
        # 检查消息类型是否为"用户发送"
        if len(message) >= 3 and message[0] == '用户发送':
            # 提取消息内容（第三个元素）
            user_messages.append(message[2])
    
    return user_messages


def process_user_messages(messages):
    """
    处理用户消息，提取并格式化输出
    
    Args:
        messages: 包含消息信息的数组
        
    Returns:
        str: 格式化后的用户消息字符串
    """
    user_messages = extract_user_messages(messages)
    
    # 将所有用户消息连接成一个字符串
    processed_messages = "\n".join(user_messages)
    
    return processed_messages



def wx_start(wechat_path="C:\\Program Files\\Tencent\\WeChat\\WeChat.exe"):
    #wechat_path = r"D:\Program Files (x86)\Tencent\WeChat\WeChat.exe"
    global WX
    WX = WeChat(wechat_path, locale="zh-CN")
    print("正在打开微信...")
    return WX

if __name__ == '__main__':
    wx_start()