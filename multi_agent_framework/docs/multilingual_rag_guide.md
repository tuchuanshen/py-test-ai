# 多语言RAG系统使用指南

本文档介绍如何使用bge-m3、LangChain和Qdrant构建多语言RAG系统，确保中文和英文文档都能被有效检索。

## 系统架构

```
┌─────────────────┐    ┌──────────────┐    ┌──────────────┐
│   Documents     │───▶│  LangChain   │───▶│    LLM       │
│ (中文/英文等)    │    │   (bge-m3)   │    │ (本地/远程)   │
└─────────────────┘    └──────────────┘    └──────────────┘
                              │
                              ▼
                       ┌──────────────┐
                       │   Qdrant     │
                       │ (向量数据库)  │
                       └──────────────┘
```

## 技术选型说明

### 1. bge-m3 嵌入模型
- 支持100+种语言
- 支持多种嵌入功能（密集、稀疏、多向量）
- 在多语言任务中表现优秀
- 本地运行，保护数据隐私

### 2. Qdrant 向量数据库
- 高性能向量搜索引擎
- 支持多种索引类型
- 提供丰富的过滤和搜索功能
- 易于部署和扩展

### 3. LangChain 框架
- 简化RAG应用开发
- 提供丰富的文档加载和处理工具
- 支持多种LLM集成

## 部署步骤

### 1. 安装依赖

```bash
pip install langchain langchain-community langchain-huggingface qdrant-client sentence-transformers
```

### 2. 启动Qdrant向量数据库

有两种方式启动Qdrant:

#### 方式一：使用Docker（推荐）

```bash
# 创建存储目录
mkdir qdrant_storage

# 启动Qdrant容器
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage \
    qdrant/qdrant
```

#### 方式二：直接安装并运行

参考 [Qdrant官方安装指南](https://qdrant.tech/documentation/install/)

### 3. 准备文档数据

将中英文文档放置在指定目录中，支持的格式包括：
- .txt 文本文件
- .pdf PDF文档
- .doc/.docx Word文档
- .xls/.xlsx Excel表格
- .csv CSV文件
- .py Python源代码

### 4. 配置领域信息

在 `rag/config.json` 中配置领域信息：

```json
{
  "persist_directory": "./qdrant_data",
  "embeddings_model": "BAAI/bge-m3",
  "default_domain": "technical",
  "domains": {
    "technical": {
      "path": "./domains/technical",
      "description": "Technical domain knowledge base"
    },
    "dns_professor": {
      "path": "./domains/dns",
      "description": "DNS相关技术知识库，包括域名解析、递归服务器等"
    }
  }
}
```

### 5. 运行示例

```bash
python multi_agent_framework/examples/multilingual_rag_example.py
```

## 多语言支持说明

### 1. bge-m3模型优势

bge-m3是BAAI开发的多语言嵌入模型，具有以下优势：
- 支持超过100种语言
- 在多语言检索任务中表现优异
- 支持多种嵌入模式（单向量、多向量、稀疏向量）
- 适用于多种下游任务

### 2. 中文处理优化

为确保中文文档被正确处理：
- 使用UTF-8编码加载所有文档
- 采用适合中文的文本分割策略
- 在向量检索中保持语义完整性

### 3. 混合语言文档支持

系统能够处理包含中英文混合内容的文档，bge-m3模型能够：
- 识别不同语言的文本片段
- 为不同语言生成相应的嵌入向量
- 在检索时正确匹配查询和文档内容

## 性能优化建议

### 1. 文档预处理
- 合理设置文本分割大小（默认1000字符）
- 保留文档元数据以支持过滤检索
- 对大文档进行适当预处理

### 2. 向量索引优化
- 根据数据量选择合适的索引类型
- 定期优化向量索引以提高检索速度
- 合理设置检索参数（如top-k值）

### 3. 缓存策略
- 利用Qdrant的持久化功能避免重复加载
- 对频繁查询的内容实现应用层缓存
- 合理使用嵌入模型的缓存机制

## 故障排除

### 1. Qdrant连接问题
- 检查Qdrant服务是否正常运行
- 确认端口配置是否正确
- 检查防火墙设置

### 2. 文档加载失败
- 确认文档格式是否受支持
- 检查文件权限和路径
- 验证文档编码是否为UTF-8

### 3. 检索效果不佳
- 检查查询语言是否与文档语言匹配
- 调整文本分割参数
- 尝试不同的检索算法

## 扩展功能

### 1. 添加新领域
在配置文件中添加新的领域定义，系统会自动处理文档加载和索引。

### 2. 自定义过滤器
可以基于文档元数据实现过滤检索，例如按日期、类型等过滤。

### 3. 集成其他LLM
支持集成各种大语言模型，包括本地模型和API模型。

通过以上方案，你可以构建一个功能完整的多语言RAG系统，能够有效处理中英文混合的文档内容，并提供高质量的检索增强生成能力。