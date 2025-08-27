import time
from ui_auto_wechat import WeChat

def main():
    # 微信安装路径，需要根据实际路径修改
    wechat_path = "D:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe"
    
    # 初始化微信对象
    wechat = WeChat(wechat_path, locale="zh-CN")
    
    # 1. 打开微信
    print("正在打开微信...")
    wechat.open_wechat()
    time.sleep(3)  # 等待微信启动
    
    # 2. 打开朋友圈
    print("正在打开朋友圈...")
    success = wechat.open_moments()
    if success:
        print("朋友圈打开成功")
    else:
        print("朋友圈打开失败")
    
    # 等待查看效果
    time.sleep(5)
    
    print("测试完成")

if __name__ == "__main__":
    main()