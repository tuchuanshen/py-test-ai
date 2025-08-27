import time
import os
import subprocess
from ui_auto_wechat import WeChat

def find_wechat_path():
    """
    尝试自动查找微信安装路径
    """
    # 常见的微信安装路径
    common_paths = [
        "C:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe",
        "C:\\Program Files\\Tencent\\WeChat\\WeChat.exe",
        "D:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe",
        "D:\\Program Files\\Tencent\\WeChat\\WeChat.exe",
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    # 如果常见路径都不存在，尝试从注册表读取
    try:
        import winreg
        reg_path = r"SOFTWARE\Tencent\WeChat"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
            install_dir, _ = winreg.QueryValueEx(key, "InstallDir")
            wechat_exe = os.path.join(install_dir, "WeChat.exe")
            if os.path.exists(wechat_exe):
                return wechat_exe
    except Exception:
        pass
    
    return None

def main():
    # 尝试自动查找微信路径
    wechat_path = find_wechat_path()
    
    if not wechat_path:
        # 如果找不到，使用默认路径并提示用户修改
        wechat_path = "C:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe"
        print(f"警告: 未找到微信安装路径，请确认路径是否正确: {wechat_path}")
    else:
        print(f"找到微信安装路径: {wechat_path}")
    
    # 检查路径是否存在
    if not os.path.exists(wechat_path):
        print(f"错误: 微信路径不存在: {wechat_path}")
        print("请修改脚本中的 wechat_path 变量为正确的微信安装路径")
        return
    
    print(f"使用微信路径: {wechat_path}")
    
    try:
        # 初始化微信对象
        print("初始化微信对象...")
        wechat = WeChat(wechat_path, locale="zh-CN")
        print("微信对象初始化成功")
        
        # 1. 打开微信
        print("\n1. 正在打开微信...")
        wechat.open_wechat()
        print("微信启动命令已发送")
        time.sleep(5)  # 等待微信启动
        
        # 2. 向沈圳发送消息"123"
        print("\n2. 正在向沈圳发送消息 '123'...")
        try:
            success = wechat.send_msg("沈圳", text="123")
            if success:
                print("消息发送成功")
            else:
                print("消息发送失败")
        except Exception as e:
            print(f"发送消息时出错: {e}")
            print("可能的原因:")
            print("1. 联系人名称不正确")
            print("2. 微信未完全启动")
            print("3. 微信界面被其他窗口遮挡")
            print("4. 微信版本不兼容")
        
        # 等待几秒确保消息发送完成
        time.sleep(2)
        
        # 3. 监听好友苗是否发送消息来
        print("\n3. 设置监听好友'苗'的消息...")
        try:
            # 设置自动回复的联系人为"苗"
            wechat.set_auto_reply(["苗"])
            print("已设置自动回复联系人: 苗")
            
            # 检查一次新消息作为示例
            print("检查新消息...")
            wechat.check_new_msg()
            print("新消息检查完成")
        except Exception as e:
            print(f"监听消息时出错: {e}")
            
    except Exception as e:
        print(f"运行时出错: {e}")
        print("可能的解决方案:")
        print("1. 确保微信未在运行，先手动关闭微信再运行脚本")
        print("2. 以管理员权限运行脚本")
        print("3. 检查微信安装路径是否正确")
        print("4. 确保Windows UI Automation功能未被禁用")

if __name__ == "__main__":
    main()
    
    print("\n按回车键退出...")
    input()