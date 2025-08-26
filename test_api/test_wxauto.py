from wxauto import WeChat
wx = WeChat()
# 给文件传输助手发送消息
#wx.SendMsg('今天是个什么好日子啊！', '文件传输助手')
wx.SendMsg("你好", who="AI聊天群")