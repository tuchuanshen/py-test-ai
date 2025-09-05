import time
import threading
from datetime import datetime, timedelta
import pythoncom
from ui_auto_wechat import WeChat
from typing import List
global WX


def wx_start(wechat_path="C:\\Program Files\\Tencent\\WeChat\\WeChat.exe"):
    #wechat_path = "D:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe"
    global WX
    WX = WeChat(wechat_path, locale="zh-CN")
    return WX
