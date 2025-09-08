import time
import threading
from ui_auto_wechat import WeChat
from listener_manager import ListenerManager


def custom_handler_a(contact_name, messages):
    """自定义消息处理函数A"""
    print(f"[自定义处理A] 收到 {contact_name} 的消息:")
    for msg_type, sender, content in messages:
        if msg_type == '用户发送':
            print(f"  -> {sender} 发送: {content}")


def custom_handler_b(contact_name, messages):
    """自定义消息处理函数B"""
    print(f"[自定义处理B] 检测到 {contact_name} 的活动:")
    for msg_type, sender, content in messages:
        print(f"  [{msg_type}] 内容: {content}")


def dynamic_add_listener(listener_manager):
    """模拟动态添加监听对象"""
    time.sleep(8)  # 等待一段时间后再添加
    print("\n=== 动态添加监听对象 ===")
    listener_manager.add_listener("动态添加的朋友")
    listener_manager.add_listener("动态群聊", custom_handler_a)


def main():
    # 微信安装路径，需要根据实际路径修改
    wechat_path = "D:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe"
    
    # 初始化微信对象
    wechat = WeChat(wechat_path, locale="zh-CN")
    
    # 初始化监听管理器
    listener_manager = ListenerManager(wechat)
    
    # 1. 添加初始监听对象
    print("=== 添加初始监听对象 ===")
    # 使用默认消息处理函数
    listener_manager.add_listener("朋友A")
    
    # 使用自定义消息处理函数
    listener_manager.add_listener("同事B", custom_handler_a)
    listener_manager.add_listener("群聊C", custom_handler_b)
    
    # 查看当前所有监听对象
    print("当前监听对象:", listener_manager.get_listeners())
    
    # 启动一个线程用于动态添加监听对象
    dynamic_add_thread = threading.Thread(target=dynamic_add_listener, args=(listener_manager,))
    dynamic_add_thread.daemon = True
    dynamic_add_thread.start()
    
    # 2. 启动监听方式一：全局监听（一个线程处理所有对象）
    print("\n=== 启动全局监听 ===")
    listener_manager.start_global_listening(check_interval=3)
    
    # 运行15秒，以便观察动态添加监听对象的效果
    time.sleep(15)
    
    # 停止全局监听
    listener_manager.stop_global_listening()
    
    # 3. 启动监听方式二：单独监听（每个对象一个线程）
    print("\n=== 启动单独监听 ===")
    # 先为已有的监听对象启动线程
    listener_manager.start_individual_listening()
    
    # 再次启动一个线程用于动态添加监听对象
    dynamic_add_thread2 = threading.Thread(target=dynamic_add_listener, args=(listener_manager,))
    dynamic_add_thread2.daemon = True
    dynamic_add_thread2.start()
    
    # 运行10秒
    time.sleep(10)
    
    # 停止特定对象的监听
    listener_manager.stop_individual_listening("同事B")
    print("已停止同事B的监听")
    
    # 再运行5秒
    time.sleep(5)
    
    # 停止所有单独监听
    listener_manager.stop_individual_listening()
    
    # 4. 删除监听对象
    print("\n=== 删除监听对象 ===")
    listener_manager.remove_listener("朋友A")
    print("删除朋友A后，当前监听对象:", listener_manager.get_listeners())
    
    # 5. 重新设置消息处理函数
    print("\n=== 重新设置消息处理函数 ===")
    listener_manager.set_message_handler("同事B", custom_handler_b)
    print("已为同事B重新设置消息处理函数")


if __name__ == "__main__":
    main()