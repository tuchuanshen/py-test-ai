import sys
import os
import time
import threading
from datetime import datetime, timedelta
import pythoncom
from ui_auto_wechat import WeChat

global WX


def wx_run():
    #wechat_path = "D:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe"
    wechat_path = "C:\\Program Files\\Tencent\\WeChat\\WeChat.exe"
    global WX
    WX = WeChat(wechat_path, locale="zh-CN")


# 添加定时发送消息的函数
def schedule_message_sender():

    def send_hourly_message():
        pythoncom.CoInitialize()
        global WX
        while True:
            now = datetime.now()
            # 检查是否为整点（分钟为0）
            if now.minute == 0:
                # 获取指定聊天对象并发送消息
                try:
                    # 获取聊天对象（可以是个人或群聊）
                    message = f"多喝点水，多溜达溜达"
                    WX.send_msg("苗秋秋[爱心]", text=message, search_user=True)

                except Exception as e:
                    print(f"发送整点报时消息失败: {e}")

            if now.hour == 9 and now.minute == 0:
                try:
                    WX.send_msg("苗秋秋[爱心]",
                                text='D3 AD DHA 喂了吗',
                                search_user=True)
                except Exception as e:
                    print(f"发送消息失败: {e}")
            WX.press_close()
            # 等待5分钟
            time.sleep(50)

    # 创建并启动定时器线程
    timer_thread = threading.Thread(target=send_hourly_message, daemon=True)
    timer_thread.start()
    print("定时消息发送器已启动")


if __name__ == "__main__":
    wx_run()
    time.sleep(5)  # 等待微信初始化完成
    schedule_message_sender()

    # 主线程保持运行
    while True:
        time.sleep(100)
