# py-test-ai 项目

这是一个基于Python的AI测试项目，包含多智能体框架、RAG系统等功能。

## 安装依赖

基础依赖安装：
```bash
pip install -r requirements.txt
```

### 文档处理额外依赖

为了处理不同类型的文档（如Word、PPT、Excel等），需要安装额外的依赖：

```bash
# 安装处理docx文件的依赖
pip install "unstructured[docx]"

# 或者安装所有支持的文档类型依赖
pip install "unstructured[all]"

# 或者安装requirements-extra.txt中列出的所有额外依赖
pip install -r requirements-extra.txt
```

## 项目结构

- `multi_agent_framework/`: 多智能体框架
- `wx_agent/`: 微信智能体相关
- `test_api/`: API测试
- `easyChat-main/`: 简易聊天应用

## 使用说明

1. 配置环境变量
2. 安装依赖
3. 运行相应的测试脚本