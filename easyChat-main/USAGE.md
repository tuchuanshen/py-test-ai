# easyChat 使用说明

## 简介

easyChat 是一个基于 UI 自动化技术的 PC 端微信助手，支持定时发送消息、群发消息、自动回复等功能。

## 安装依赖

在使用之前，请确保安装了所有必要的依赖：

```bash
pip install uiautomation pyperclip keyboard numpy pandas pyautogui Pillow PyQt5
```

## 基本使用

### 1. 初始化微信对象

```python
from ui_auto_wechat import WeChat

# 微信安装路径，需要根据实际路径修改
wechat_path = "C:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe"

# 初始化微信对象
wechat = WeChat(wechat_path, locale="zh-CN")
```

### 2. 打开微信

```python
# 打开微信客户端
wechat.open_wechat()
```

### 3. 发送消息

```python
# 向指定用户发送文本消息
success = wechat.send_msg("沈圳", text="123")

# 在群聊中@某人并发送消息
wechat.send_msg("工作群", at_names=["张三"], text="请查看这个任务")

# 发送文件
wechat.send_file("沈圳", "C:\\path\\to\\file.txt")
```

### 4. 监听消息

```python
# 设置自动回复的联系人
wechat.set_auto_reply(["苗"])

# 检查新消息并自动回复
wechat.check_new_msg()
```

### 5. 打开朋友圈

```python
# 打开朋友圈界面
wechat.open_moments()
```

## 完整示例

请参考 [complete_example.py](file:///d%3A/Tuchuan/py-test-ai/easyChat-main/complete_example.py) 文件，其中包含了：

1. 打开微信
2. 向沈圳发送消息"123"
3. 监听好友苗的消息
4. 打开朋友圈并点赞第一个（示例实现）

## 功能限制说明

### 朋友圈操作

原始的 easyChat 项目并未提供朋友圈相关操作功能。现在我们新增了 [open_moments()](file:///D:/Tuchuan/py-test-ai/easyChat-main/ui_auto_wechat.py#L541-L562) 方法用于打开朋友圈界面。

测试示例请参考 [test_moments.py](file:///d%3A/Tuchuan/py-test-ai/easyChat-main/test_moments.py)。

其他朋友圈操作（如点赞、评论等）需要根据实际界面元素进行进一步开发。

## 故障排除

### 1. 微信路径问题

如果遇到"设置了正确的路径，却总是报错打不开文件"的问题，请按以下步骤排查：

#### 使用调试脚本
我们提供了调试脚本 [debug_wechat.py](file:///d%3A/Tuchuan/py-test-ai/easyChat-main/debug_wechat.py) 来帮助诊断问题：

```bash
python debug_wechat.py
```

#### 常见原因及解决方案：

1. **微信已在运行**
   - 解决方案：先手动关闭微信，再运行脚本

2. **路径包含特殊字符或空格**
   - 解决方案：确保路径用双引号括起来，或使用转义字符

3. **权限不足**
   - 解决方案：以管理员权限运行脚本

4. **微信安装路径不正确**
   - 解决方案：使用改进版示例 [improved_example.py](file:///d%3A/Tuchuan/py-test-ai/easyChat-main/improved_example.py)，该脚本会自动查找微信安装路径

5. **防病毒软件阻止**
   - 解决方案：将脚本和微信添加到防病毒软件的白名单

#### 自动查找微信路径
[improved_example.py](file:///d%3A/Tuchuan/py-test-ai/easyChat-main/improved_example.py) 提供了自动查找微信路径的功能：

```python
# 脚本会自动检查以下常见路径：
# - C:\Program Files (x86)\Tencent\WeChat\WeChat.exe
# - C:\Program Files\Tencent\WeChat\WeChat.exe
# - D:\Program Files (x86)\Tencent\WeChat\WeChat.exe
# - D:\Program Files\Tencent\WeChat\WeChat.exe

# 如果以上路径都不正确，还会尝试从Windows注册表读取
```

### 2. UI自动化相关问题

#### 控件查找失败
如果出现类似以下错误：
```
LookupError: Control not found
```

可能的原因：
1. 微信版本与脚本不兼容
2. 微信界面语言设置不正确
3. 微信窗口被遮挡或最小化

解决方案：
1. 确保微信界面语言设置与脚本中设置的一致（默认为简体中文）
2. 运行脚本时确保微信窗口可见且未被遮挡
3. 更新微信到最新版本

#### 控件交互失败
如果出现类似以下错误：
```
RuntimeError: Click failed
```

可能的原因：
1. 控件坐标计算错误
2. 窗口焦点问题

解决方案：
1. 在操作之间添加适当的等待时间
2. 确保操作时微信窗口处于活动状态

## 注意事项

1. 程序运行时请确保微信窗口不被遮挡
2. 频繁操作可能导致账号风险，请合理使用
3. 所有配置会自动保存到 `wechat_config.json` 文件中
4. 可通过 Ctrl+Alt 组合键终止发送过程

## 常见问题

### 1. 无法找到控件

如果出现无法找到控件的情况，请检查：
- 微信版本是否与程序兼容
- 微信界面语言设置是否正确
- 窗口是否被遮挡

### 2. 消息发送失败

如果消息发送失败，请检查：
- 联系人名称是否正确
- 微信是否正常运行
- 是否有网络连接问题