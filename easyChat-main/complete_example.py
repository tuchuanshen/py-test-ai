"""
完整使用示例：
1. 打开微信
2. 向沈圳发送消息"123"
3. 监听好友苗是否发送消息来
4. 打开朋友圈点赞第一个（说明实现方式）
"""

import time
import uiautomation as auto
from ui_auto_wechat import WeChat, click

def open_moments(wechat):
    """
    打开朋友圈功能（需要手动实现）
    注意：此功能在 easyChat 原始代码中未提供，需要根据实际界面元素进行操作
    """
    try:
        # 确保微信已打开并获取焦点
        wechat.open_wechat()
        wechat_window = wechat.get_wechat()
        wechat_window.SetActive()
        time.sleep(1)
        
        # 查找并点击"朋友圈"按钮
        # 根据 wechat_locale.py 中的定义，"moments" 对应中文为"朋友圈"
        moments_button = auto.ButtonControl(Name=wechat.lc.moments, Depth=8)
        if moments_button.Exists():
            click(moments_button)
            time.sleep(2)
            print("朋友圈已打开")
            return True
        else:
            print("未找到朋友圈按钮")
            return False
    except Exception as e:
        print(f"打开朋友圈时出错: {e}")
        return False

def like_first_moment():
    """
    给第一个朋友圈点赞（需要手动实现）
    注意：此功能在 easyChat 原始代码中未提供，需要根据实际界面元素进行操作
    """
    try:
        # 查找第一个朋友圈的点赞按钮
        # 这里的实现需要根据实际的朋友圈界面结构进行调整
        moments_list = auto.ListControl(Name="朋友圈", Depth=10)
        if moments_list.Exists():
            # 获取第一个朋友圈条目
            first_moment = moments_list.GetFirstChildControl()
            if first_moment:
                # 查找点赞按钮（具体名称可能需要根据实际界面调整）
                like_button = first_moment.ButtonControl(Name="点赞", foundIndex=1)
                if like_button.Exists():
                    click(like_button)
                    print("已给第一个朋友圈点赞")
                    return True
                else:
                    print("未找到点赞按钮")
                    return False
            else:
                print("未找到朋友圈内容")
                return False
        else:
            print("未进入朋友圈界面")
            return False
    except Exception as e:
        print(f"点赞时出错: {e}")
        return False

def main():
    # 微信安装路径，需要根据实际路径修改
    wechat_path = "D:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe"
    
    # 初始化微信对象
    wechat = WeChat(wechat_path, locale="zh-CN")
    
    # 1. 打开微信
    print("正在打开微信...")
    wechat.open_wechat()
    time.sleep(3)  # 等待微信启动
    
    # 2. 向沈圳发送消息"123"
    print("正在向沈圳发送消息 '123'...")
    success = wechat.send_msg("沈圳", text="123")
    if success:
        print("消息发送成功")
    else:
        print("消息发送失败")
    
    # 等待几秒确保消息发送完成
    time.sleep(2)
    
    # 3. 监听好友苗是否发送消息来
    print("设置监听好友'苗'的消息...")
    # 设置自动回复的联系人为"苗"
    wechat.set_auto_reply(["苗"])
    print("已设置自动回复联系人: 苗")
    
    # 检查一次新消息作为示例
    print("检查新消息...")
    wechat.check_new_msg()
    
    # 4. 打开朋友圈点赞第一个
    print("\n尝试打开朋友圈...")
    if open_moments(wechat):
        print("尝试给第一个朋友圈点赞...")
        # 注意：以下函数需要根据实际界面结构调整实现
        # like_first_moment()
        print("注意：朋友圈点赞功能需要根据实际界面结构调整实现")
    else:
        print("无法打开朋友圈")

    print("\n示例执行完成。")
    print("\n关于朋友圈功能的说明：")
    print("1. easyChat 原始代码未提供朋友圈相关操作")
    print("2. 示例中提供了基础的实现思路")
    print("3. 实际使用时需要根据微信界面结构调整选择器参数")
    print("4. 可能需要处理更多异常情况和边界条件")

if __name__ == "__main__":
    main()