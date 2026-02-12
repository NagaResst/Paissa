import logging
import logging.handlers
import os
from pathlib import Path


class Log(object):
    def __init__(self, level="INFO", log_file="Data/Paissa.log"):
        self.log = logging.getLogger('猴面雀')
        self.log.setLevel(level)
        
        # 创建日志目录
        log_path = Path(log_file)
        log_path.parent.mkdir(exist_ok=True)
        
        # 详细的日志格式
        self.log_format = "%(asctime)s : <%(module)s:%(lineno)d> [%(levelname)s] %(message)s"
        self.date_format = "%Y-%m-%d %H:%M:%S"
        
        # 性能日志格式
        self.perf_format = "%(asctime)s : [PERFORMANCE] %(message)s"

    def console_handle(self):
        console_handle = logging.StreamHandler()
        console_formatter = logging.Formatter(
            fmt=self.log_format,
            datefmt=self.date_format
        )
        console_handle.setFormatter(console_formatter)
        return console_handle

    def file_handle(self, log_file):
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, 
            maxBytes=50*1024*1024,  # 50MB
            backupCount=5, 
            encoding='utf-8'
        )
        
        file_formatter = logging.Formatter(
            fmt=self.log_format,
            datefmt=self.date_format
        )
        file_handler.setFormatter(file_formatter)
        return file_handler

    def performance_handle(self, log_file):
        """专门用于性能日志的处理器"""
        perf_handler = logging.handlers.RotatingFileHandler(
            log_file.replace('.log', '_perf.log'),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=3,
            encoding='utf-8'
        )
        
        perf_formatter = logging.Formatter(
            fmt=self.perf_format,
            datefmt=self.date_format
        )
        perf_handler.setFormatter(perf_formatter)
        perf_handler.setLevel(logging.INFO)
        return perf_handler

    def get_log(self, log_file="Data/Paissa.log"):
        # 清除现有处理器
        for handler in self.log.handlers[:]:
            self.log.removeHandler(handler)
            handler.close()
        
        # 添加处理器
        self.log.addHandler(self.console_handle())
        self.log.addHandler(self.file_handle(log_file))
        self.log.addHandler(self.performance_handle(log_file))
        return self.log


# 创建全局logger实例
logger = Log().get_log()


def log_performance(func):
    """性能监控装饰器"""
    import time
    from functools import wraps
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            logger.info(f"函数 {func.__name__} 执行耗时: {duration:.4f}秒")
            return result
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            logger.error(f"函数 {func.__name__} 执行出错，耗时: {duration:.4f}秒, 错误: {e}")
            raise
    return wrapper
