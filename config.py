import os
from pathlib import Path

class Config:
    """应用程序配置管理类"""
    
    # 项目根目录
    BASE_DIR = Path(__file__).parent
    
    # 数据目录
    DATA_DIR = BASE_DIR / "Data"
    
    # UI目录
    UI_DIR = BASE_DIR / "UI"
    
    # 日志配置
    LOG_FILE = DATA_DIR / "Paissa.log"
    HISTORY_FILE = DATA_DIR / "Paissa_query_history.log"
    ITEM_DATA_FILE = DATA_DIR / "item.Pdt"
    MARKETABLE_FILE = DATA_DIR / "marketable.py"
    VERSION_FILE = DATA_DIR / "version"
    
    # API配置 - 针对国内访问优化
    API_HEADERS = {
        "User-Agent": "Paissa/1.0",
        "referer": "http://Paissa.public/",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate"
    }
    
    # 网络超时设置 - 短而快
    TIMEOUT_SETTINGS = {
        "version_check": 1,       # 版本检查3秒超时
        "data_download": 8,       # 数据下载8秒超时  
        "market_data": 3,         # 市场数据6秒超时
        "icon_download": 3        # 图标下载3秒超时
    }
    
    # 并发设置 - 多重试
    MAX_WORKERS = 20
    MAX_RETRY_ATTEMPTS = 8        # 增加重试次数到8次
    RETRY_DELAY_BASE = 0.5        # 基础重试延迟0.5秒
    
    # 缓存设置
    PRICE_CACHE_SIZE = 1000
    CACHE_EXPIRE_TIME = 300  # 5分钟
    
    @classmethod
    def get_data_path(cls, filename):
        """获取数据文件完整路径"""
        return cls.DATA_DIR / filename
    
    @classmethod
    def get_ui_path(cls, filename):
        """获取UI文件完整路径"""
        return cls.UI_DIR / filename