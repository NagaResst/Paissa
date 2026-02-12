import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import os
import sys
import time
from typing import Optional, Dict, Any

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from Data.logger import logger

class HttpClient:
    """HTTP客户端封装类 - 针对国内访问香港优化"""
    
    def __init__(self):
        self.session = requests.Session()
        self._setup_session()
        
    def _setup_session(self):
        """配置会话参数 - 快速重试策略"""
        # 针对跨境网络优化的重试策略
        retry_strategy = Retry(
            total=config.Config.MAX_RETRY_ATTEMPTS,
            backoff_factor=config.Config.RETRY_DELAY_BASE,  # 短延迟快速重试
            status_forcelist=[408, 429, 500, 502, 503, 504, 522, 524],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            raise_on_status=False  # 不立即抛出异常
        )
        
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=20,    # 增加连接池
            pool_maxsize=20
        )
        
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # 优化headers
        self.session.headers.update(config.Config.API_HEADERS)
        
        # 获取系统代理
        try:
            from urllib.request import getproxies
            self.session.proxies.update(getproxies())
        except Exception as e:
            logger.warning(f"代理设置获取失败: {e}")
    
    def get_json(self, url: str, timeout: Optional[int] = None) -> Optional[Dict[Any, Any]]:
        """快速获取JSON数据"""
        timeout = timeout or config.Config.TIMEOUT_SETTINGS.get('data_download', 8)
        
        try:
            response = self.session.get(url, timeout=timeout)
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"HTTP {response.status_code}: {url}")
                return None
        except requests.exceptions.Timeout:
            logger.debug(f"⏱️ 超时 {url}")
            return None
        except requests.exceptions.ConnectionError:
            logger.debug(f"🔗 连接失败 {url}")
            return None
        except Exception as e:
            logger.debug(f"❌ 请求失败 {url}: {type(e).__name__}")
            return None
    
    def get_text(self, url: str, timeout: Optional[int] = None) -> Optional[str]:
        """快速获取文本数据"""
        timeout = timeout or config.Config.TIMEOUT_SETTINGS.get('data_download', 8)
        
        try:
            response = self.session.get(url, timeout=timeout)
            if response.status_code == 200:
                return response.text
            else:
                return None
        except:
            return None
    
    def get_content(self, url: str, timeout: Optional[int] = None) -> Optional[bytes]:
        """快速获取二进制内容"""
        timeout = timeout or config.Config.TIMEOUT_SETTINGS.get('icon_download', 3)
        
        try:
            response = self.session.get(url, timeout=timeout)
            if response.status_code == 200:
                return response.content
            else:
                return None
        except:
            return None
    
    def close(self):
        """关闭会话"""
        self.session.close()

# 全局HTTP客户端实例
http_client = HttpClient()