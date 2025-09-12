# 多智能体协作框架

这是一个可扩展的多智能体协作框架，支持以下功能：

## 功能特性

1. **多智能体协作** - 支持多个专用智能体协同工作
2. **多领域RAG** - 支持不同领域的知识库问答
3. **复杂工具系统** - 可扩展的工具注册和执行机制
4. **反思机制** - 对生成答案进行质量检查和优化
5. **对话历史管理** - 管理用户与AI的对话历史

## 目录结构

```
multi_agent_framework/
├── agents/           # 智能体模块
│   ├── __init__.py
│   ├── base.py       # 智能体基类
│   └── chat_agent.py # 通用对话智能体
├── domains/          # 领域RAG模块
│   ├── __init__.py
│   └── technical.py  # 技术文档领域RAG
├── tools/            # 工具模块
│   ├── __init__.py
│   ├── base.py       # 工具基类
│   ├── calculator.py  # 计算器工具
│   └── weather.py    # 天气查询工具
├── core/             # 核心框架模块
│   ├── __init__.py
│   ├── engine.py     # 核心引擎
│   ├── state.py      # 状态管理
│   └── tool_manager.py # 工具管理器
├── memory/           # 记忆管理模块
│   ├── __init__.py
│   └── chat_history.py # 对话历史管理
├── rag/              # RAG核心模块
│   ├── __init__.py
│   └── manager.py    # RAG管理器
├── reflection/       # 反思机制模块
│   ├── __init__.py
│   ├── base.py       # 反思器基类
│   └── quality_checker.py # 质量检查反思器
├── utils/            # 工具类
│   └── __init__.py
├── main.py           # 主入口文件
└── README.md         # 说明文档
```

## 扩展方式

### 添加新的智能体

1. 在 `agents/` 目录下创建新的智能体类
2. 继承 `BaseAgent` 基类
3. 实现 `process` 方法
4. 在 `main.py` 中注册智能体

### 添加新的领域RAG

1. 在 `domains/` 目录下创建新的领域RAG类
2. 实现领域特定的文档加载和查询逻辑
3. 在 `main.py` 中初始化并使用

### 添加复杂工具

1. 在 `tools/` 目录下创建新的工具类
2. 继承 `BaseTool` 基类
3. 实现 `run` 方法
4. 在 `main.py` 中注册工具

### 改进反思机制

1. 在 `reflection/` 目录下创建新的反思器类
2. 继承 `BaseReflector` 基类
3. 实现 `reflect` 方法
4. 在流程中使用新的反思器

### 增强对话历史管理

1. 在 `memory/` 目录下扩展对话历史管理功能
2. 可实现持久化存储、摘要机制等高级功能

## 使用方法

```bash
python main.py
```

## 设计原则

1. **模块化设计** - 各个组件职责清晰，易于维护和扩展
2. **可插拔架构** - 工具、智能体、RAG领域支持动态注册和卸载
3. **可配置性** - 支持多种配置方式，适应不同环境
4. **可扩展性** - 易于添加新功能和工具
5. **健壮性** - 内置错误处理和重试机制