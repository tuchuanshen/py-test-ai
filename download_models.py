#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
下载RAG系统所需的嵌入模型
"""

import logging
from langchain_huggingface import HuggingFaceEmbeddings

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def download_model(model_name: str):
    """
    下载指定的嵌入模型
    
    Args:
        model_name: 模型名称
    """
    try:
        logger.info(f"开始下载模型: {model_name}")
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        logger.info(f"模型 {model_name} 下载完成")
        return embeddings
    except Exception as e:
        logger.error(f"下载模型 {model_name} 失败: {e}")
        raise


def main():
    """主函数"""
    # 下载主要使用的多语言模型
    models_to_download = [
        "BAAI/bge-m3",
        "sentence-transformers/all-MiniLM-L6-v2"
    ]
    
    for model_name in models_to_download:
        try:
            download_model(model_name)
        except Exception as e:
            logger.error(f"无法下载模型 {model_name}: {e}")
            return False
    
    logger.info("所有模型下载完成")
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)