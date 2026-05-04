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

from config import Config
from Data.logger import logger


class HttpClient:
    """HTTP客户端封装类 - 针对国内访问香港优化"""

    def __init__(self):
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self):
        """配置会话参数 - 快速重试策略"""
        # 针对跨境网络优化的重试策略（urllib3层重试，处理服务端错误状态码）
        retry_strategy = Retry(
            total=Config.MAX_RETRY_ATTEMPTS,
            backoff_factor=Config.RETRY_DELAY_BASE,
            status_forcelist=[408, 429, 500, 502, 503, 504, 522, 524],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            raise_on_status=False
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=20,
            pool_maxsize=20
        )

        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # 优化headers
        self.session.headers.update(Config.API_HEADERS)

        # 获取系统代理
        try:
            from urllib.request import getproxies
            self.session.proxies.update(getproxies())
        except Exception as e:
            logger.warning(f"代理设置获取失败: {e}")

    def _retry_request(self, request_func, url, timeout):
        """应用层重试：对超时和连接错误进行额外重试"""
        for attempt in range(Config.MAX_RETRY_ATTEMPTS):
            try:
                return request_func()
            except requests.exceptions.Timeout:
                logger.debug(f"第{attempt + 1}次尝试超时: {url}")
                if attempt == Config.MAX_RETRY_ATTEMPTS - 1:
                    return None
                time.sleep(Config.RETRY_DELAY_BASE)
            except requests.exceptions.ConnectionError:
                logger.debug(f"第{attempt + 1}次连接失败: {url}")
                if attempt == Config.MAX_RETRY_ATTEMPTS - 1:
                    return None
                time.sleep(Config.RETRY_DELAY_BASE)
            except Exception as e:
                logger.debug(f"请求失败 {url}: {type(e).__name__}")
                return None
        return None

    def get_json(self, url: str, timeout: Optional[int] = None) -> Optional[Dict[Any, Any]]:
        """获取JSON数据，带应用层重试"""
        timeout = timeout or Config.TIMEOUT_SETTINGS.get('data_download', 8)

        def _do_request():
            response = self.session.get(url, timeout=timeout)
            if response.status_code == 200:
                try:
                    return response.json()
                except (json.JSONDecodeError, ValueError):
                    logger.warning(f"响应非有效JSON: {url}")
                    return None
            else:
                logger.warning(f"HTTP {response.status_code}: {url}")
                return None

        return self._retry_request(_do_request, url, timeout)

    def get_text(self, url: str, timeout: Optional[int] = None) -> Optional[str]:
        """获取文本数据，带应用层重试"""
        timeout = timeout or Config.TIMEOUT_SETTINGS.get('data_download', 8)

        def _do_request():
            response = self.session.get(url, timeout=timeout)
            if response.status_code == 200:
                return response.text
            else:
                logger.warning(f"HTTP {response.status_code}: {url}")
                return None

        return self._retry_request(_do_request, url, timeout)

    def get_content(self, url: str, timeout: Optional[int] = None) -> Optional[bytes]:
        """获取二进制内容，带应用层重试"""
        timeout = timeout or Config.TIMEOUT_SETTINGS.get('icon_download', 3)

        def _do_request():
            response = self.session.get(url, timeout=timeout)
            if response.status_code == 200:
                return response.content
            else:
                logger.warning(f"HTTP {response.status_code}: {url}")
                return None

        return self._retry_request(_do_request, url, timeout)

    def close(self):
        """关闭会话"""
        self.session.close()


# 全局HTTP客户端实例
http_client = HttpClient()
