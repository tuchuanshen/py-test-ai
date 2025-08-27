import time
import os
import subprocess
from ui_auto_wechat import WeChat

def check_wechat_path(wechat_path):
    """
    检查微信路径是否正确
    """
    print(f"检查微信路径: {wechat_path}")
    
    # 1. 检查路径是否存在
    if not os.path.exists(wechat_path):
        print("错误: 微信路径不存在")
        return False
    
    # 2. 检查是否是可执行文件
    if not os.path.isfile(wechat_path):
        print("错误: 路径不是文件")
        return False
        
    # 3. 检查文件扩展名
    if not wechat_path.endswith('.exe'):
        print("错误: 文件不是.exe可执行文件")
        return False
    
    # 4. 检查文件是否可执行
    if not os.access(wechat_path, os.X_OK):
        print("错误: 文件没有执行权限")
        return False
        
    print("微信路径检查通过")
    return True

def test_open_wechat_directly(wechat_path):
    """
    直接测试打开微信
    """
    print("尝试直接打开微信...")
    try:
        # 使用subprocess测试打开
        process = subprocess.Popen(wechat_path)
        print("微信启动进程已创建")
        time.sleep(5)  # 等待5秒
        
        # 检查进程是否仍在运行
        if process.poll() is None:
            print("微信进程正在运行")
            # 终止进程以便后续测试
            process.terminate()
            process.wait()
            print("已终止微信进程")
        else:
            print(f"微信进程已退出，返回码: {process.returncode}")
            return False
            
        return True
    except Exception as e:
        print(f"打开微信时出错: {e}")
        return False

def test_wechat_class(wechat_path):
    """
    测试WeChat类
    """
    print("测试WeChat类...")
    try:
        # 初始化WeChat对象
        wechat = WeChat(wechat_path, locale="zh-CN")
        print(f"WeChat对象创建成功，路径: {wechat.path}")
        
        # 测试open_wechat方法
        print("调用open_wechat方法...")
        wechat.open_wechat()
        print("open_wechat方法调用完成")
        time.sleep(5)  # 等待微信启动
        
        return True
    except Exception as e:
        print(f"WeChat类测试出错: {e}")
        return False

def main():
    # 微信安装路径，需要根据实际路径修改
    wechat_path = "D:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe"
    
    print("=== 微信路径调试工具 ===\n")
    
    # 首先检查路径
    if not check_wechat_path(wechat_path):
        print("\n请检查微信安装路径是否正确，修改脚本中的 wechat_path 变量")
        return
    
    print("\n=== 直接测试打开微信 ===")
    if not test_open_wechat_directly(wechat_path):
        print("直接打开微信失败")
    
    print("\n=== 测试WeChat类 ===")
    if not test_wechat_class(wechat_path):
        print("WeChat类测试失败")
    
    print("\n=== 调试完成 ===")
    print("如果仍有问题，请检查:")
    print("1. 微信是否已经运行，如果是，请先关闭")
    print("2. 是否有足够的权限运行微信")
    print("3. 微信路径是否包含特殊字符或空格，可能需要用引号括起来")
    print("4. 防病毒软件是否阻止了程序运行")

if __name__ == "__main__":
    main()