from wxauto import WeChat
import time
from datetime import datetime
import hashlib

wx = WeChat()

# 保持程序运行
wx.KeepRunning()

def schedule_message_sender():
    def send_hourly_message():
        last_sent_hour = -1  # 记录上次发送消息的小时
        
        while True:
            now = datetime.now()
            
            # 检查是否为整点且还未发送过该小时的消息
            if now.minute == 0 and now.hour != last_sent_hour:
                try:
                    # 发送整点报时消息
                    chat_person = wx.GetChat("苗秋秋[爱心]")
                    if chat_person:
                        message = f"亲爱的宝，现在是北京时间 {now.strftime('%Y年%m月%d日 %H:%M')} 整点报时"
                        chat_person.SendMsg(message)
                        print(f"已发送整点报时消息: {message}")
                        last_sent_hour = now.hour  # 记录已发送的小时
                        
                except Exception as e:
                    print(f"发送整点报时消息失败: {e}")
            
            # 等待5分钟
            time.sleep(300)  # 300秒 = 5分钟
    
    # 创建并启动定时器线程
    timer_thread = threading.Thread(target=send_hourly_message, daemon=True)
    timer_thread.start()
    print("定时消息发送器已启动")