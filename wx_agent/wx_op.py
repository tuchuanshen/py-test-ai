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


def wx_start(wechat_path="C:\\Program Files\\Tencent\\WeChat\\WeChat.exe"):
    #wechat_path = r"D:\Program Files (x86)\Tencent\WeChat\WeChat.exe"
    global WX
    WX = WeChat(wechat_path, locale="zh-CN")
    print("正在打开微信...")
    return WX

if __name__ == '__main__':
    wx_start()