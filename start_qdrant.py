"""
启动Qdrant向量数据库
"""

import subprocess
import sys
import os


def start_qdrant():
    """启动Qdrant数据库"""
    try:
        # 检查是否已安装qdrant
        subprocess.run(["qdrant", "--help"], check=True, capture_output=True)
        
        # 启动Qdrant
        print("正在启动Qdrant...")
        qdrant_process = subprocess.Popen([
            "qdrant",
            "--config-path",
            "qdrant_config.yaml"
        ])
        
        print("Qdrant已在后台启动")
        print("HTTP端口: 6333")
        print("gRPC端口: 6334")
        return qdrant_process
        
    except subprocess.CalledProcessError:
        print("错误: 未找到Qdrant可执行文件")
        print("请先安装Qdrant:")
        print("  使用Docker: docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant")
        print("  或参考 https://qdrant.tech/documentation/install/")
        return None
    except FileNotFoundError:
        print("错误: 未找到Qdrant可执行文件")
        print("请先安装Qdrant:")
        print("  使用Docker: docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant")
        print("  或参考 https://qdrant.tech/documentation/install/")
        return None


def start_qdrant_with_docker():
    """使用Docker启动Qdrant"""
    try:
        # 检查Docker是否可用
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        
        # 创建存储目录
        os.makedirs("qdrant_storage", exist_ok=True)
        
        # 使用Docker启动Qdrant
        print("正在使用Docker启动Qdrant...")
        docker_process = subprocess.Popen([
            "docker", "run",
            "-p", "6333:6333",
            "-p", "6334:6334",
            "-v", f"{os.path.abspath('qdrant_storage')}:/qdrant/storage",
            "qdrant/qdrant"
        ])
        
        print("Qdrant已在Docker容器中启动")
        print("HTTP端口: 6333")
        print("gRPC端口: 6334")
        return docker_process
        
    except subprocess.CalledProcessError:
        print("错误: Docker不可用")
        return None
    except FileNotFoundError:
        print("错误: 未找到Docker可执行文件")
        return None


if __name__ == "__main__":
    print("Qdrant启动选项:")
    print("1. 直接启动 (需要已安装Qdrant)")
    print("2. 使用Docker启动")
    
    choice = input("请选择启动方式 (1 或 2): ").strip()
    
    if choice == "1":
        process = start_qdrant()
    elif choice == "2":
        process = start_qdrant_with_docker()
    else:
        print("无效选择")
        sys.exit(1)
    
    if process:
        print("Qdrant启动成功，请保持此窗口打开")
        print("按Ctrl+C停止Qdrant")
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n正在停止Qdrant...")
            process.terminate()
            process.wait()
            print("Qdrant已停止")