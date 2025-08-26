#!/bin/bash

# 定义 pip 命令变量
PIP_CMD=pip3  # 可以根据需要改为 pip

# 使用变量安装包
$PIP_CMD install openai
$PIP_CMD install langchain
$PIP_CMD install langchain-community
$PIP_CMD install langchain-experimental
$PIP_CMD install "langserve[all]"
$PIP_CMD install langchain-cli
$PIP_CMD install langsmith
$PIP_CMD install wxauto
$PIP_CMD install dashscope