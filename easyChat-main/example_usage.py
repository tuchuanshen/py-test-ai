import time
from ui_auto_wechat import WeChat

def main():
    # 微信安装路径，需要根据实际路径修改
    wechat_path = "C:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe"
    
    # 初始化微信对象
    wechat = WeChat(wechat_path, locale="zh-CN")
    
    # 1. 打开微信
    print("正在打开微信...")
    wechat.open_wechat()
    time.sleep(3)  # 等待微信启动
    
    # 2. 向沈圳发送消息"123"
    print("正在向沈圳发送消息...")
    success = wechat.send_msg("沈圳", text="123")
    if success:
        print("消息发送成功")
    else:
        print("消息发送失败")
    
    # 等待几秒确保消息发送完成
    time.sleep(2)
    
    # 3. 监听好友苗是否发送消息来
    print("开始监听好友'苗'的消息...")
    print("监听中... 按 Ctrl+C 退出监听")
    
    try:
        # 设置自动回复的联系人为"苗"
        wechat.set_auto_reply(["苗"])
        
        # 持续监听新消息
        while True:
            wechat.check_new_msg()
            time.sleep(5)  # 每5秒检查一次新消息
            
    except KeyboardInterrupt:
        print("\n监听已停止")

if __name__ == "__main__":
    main()