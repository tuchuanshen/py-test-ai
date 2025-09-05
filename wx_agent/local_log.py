import os
import sys
import traceback
from datetime import datetime
from enum import Enum
from typing import Optional, Any


class LogLevel(Enum):
    """日志级别枚举"""
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


class Logger:
    """自定义日志记录器"""

    def __init__(self,
                 log_file: Optional[str] = None,
                 min_level: LogLevel = LogLevel.INFO):
        """
        初始化日志记录器
        
        Args:
            log_file: 日志文件路径，如果为None则只输出到终端
            min_level: 最小日志级别，低于此级别的日志不会被记录
        """
        self.log_file = log_file
        self.min_level = min_level

        # 确保日志目录存在
        if self.log_file:
            log_dir = os.path.dirname(self.log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)

    def _get_caller_info(self):
        """
        获取调用者信息（文件名、行号、函数名）
        通过遍历调用栈找到第一个非日志模块的调用者
        """
        try:
            # 获取当前调用栈
            stack = traceback.extract_stack()

            # 需要过滤掉的文件名列表
            skip_files = [
                'local_log.py', 'pydevd_runpy.py', 'runpy.py', 'threading.py',
                'pydevd.py'
            ]

            # 从栈底向上查找（排除最底部的几帧）
            # 通常真实的调用者在中间部分
            for i in range(len(stack) - 2, -1, -1):
                frame = stack[i]
                filename = os.path.basename(frame.filename)

                # 跳过已知的系统和调试器文件
                if filename not in skip_files:
                    return filename, frame.lineno, frame.name

            # 如果没找到合适的，返回倒数第三帧作为备选
            if len(stack) >= 3:
                frame = stack[-3]
                return os.path.basename(
                    frame.filename), frame.lineno, frame.name

            return "unknown", 0, "unknown"
        except Exception as e:
            return "error", 0, f"get_caller_failed_{str(e)}"

    def _format_message(self, level: LogLevel, message: str) -> str:
        """格式化日志消息"""
        filename, lineno, function = self._get_caller_info()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        formatted_message = (f"[{timestamp}] "
                             f"[{level.name}] "
                             f"[{filename}:{lineno} in {function}()] "
                             f"- {message}")

        return formatted_message

    def _write_log(self, level: LogLevel, *args, **kwargs):
        """
        写入日志，支持print格式的参数
        
        Args:
            level: 日志级别
            *args: 位置参数，类似print函数
            **kwargs: 关键字参数，类似print函数
        """
        # 检查日志级别
        if level.value < self.min_level.value:
            return

        # 处理print格式的参数
        sep = kwargs.get('sep', ' ')
        message = sep.join(str(arg) for arg in args)

        formatted_message = self._format_message(level, message)

        # 输出到终端
        if level.value >= LogLevel.WARNING.value:
            # WARNING及以上级别输出到stderr
            print(formatted_message, file=sys.stderr)
        else:
            # INFO及以下级别输出到stdout
            print(formatted_message)

        # 输出到文件
        if self.log_file:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(formatted_message + '\n')
            except Exception as e:
                print(f"写入日志文件失败: {e}", file=sys.stderr)

    def debug_log(self, *args, **kwargs):
        """调试级别日志，支持print格式参数"""
        self._write_log(LogLevel.DEBUG, *args, **kwargs)

    def info_log(self, *args, **kwargs):
        """信息级别日志，支持print格式参数"""
        self._write_log(LogLevel.INFO, *args, **kwargs)

    def warning_log(self, *args, **kwargs):
        """警告级别日志，支持print格式参数"""
        self._write_log(LogLevel.WARNING, *args, **kwargs)

    def error_log(self, *args, **kwargs):
        """错误级别日志，支持print格式参数"""
        self._write_log(LogLevel.ERROR, *args, **kwargs)

    def critical_log(self, *args, **kwargs):
        """严重错误级别日志，支持print格式参数"""
        self._write_log(LogLevel.CRITICAL, *args, **kwargs)


# 创建全局日志实例
_default_logger = Logger()


def set_logger(log_file: Optional[str] = None,
               min_level: LogLevel = LogLevel.INFO):
    """
    设置全局日志配置
    
    Args:
        log_file: 日志文件路径
        min_level: 最小日志级别
    """
    global _default_logger
    _default_logger = Logger(log_file, min_level)


def debug_log(*args, **kwargs):
    """记录调试日志，支持print格式参数"""
    _default_logger.debug_log(*args, **kwargs)


def info_log(*args, **kwargs):
    """记录信息日志，支持print格式参数"""
    _default_logger.info_log(*args, **kwargs)


def warning_log(*args, **kwargs):
    """记录警告日志，支持print格式参数"""
    _default_logger.warning_log(*args, **kwargs)


def error_log(*args, **kwargs):
    """记录错误日志，支持print格式参数"""
    _default_logger.error_log(*args, **kwargs)


def critical_log(*args, **kwargs):
    """记录严重错误日志，支持print格式参数"""
    _default_logger.critical_log(*args, **kwargs)


# 测试代码
if __name__ == "__main__":
    # 设置日志配置
    set_logger("logs/app.log", LogLevel.DEBUG)

    # 测试日志记录
    def test_function():
        debug_log("这是一条调试信息")
        info_log("这是一条普通信息")
        warning_log("这是一条警告信息")
        error_log("这是一条错误信息")
        critical_log("这是一条严重错误信息")

        # 支持print格式的多种参数
        debug_log("支持多个参数:", 1, 2, 3, sep=", ")
        info_log("变量值:", {"key": "value"}, [1, 2, 3])
        error_log("错误码:", 404, "消息:", "Not Found")

    test_function()
