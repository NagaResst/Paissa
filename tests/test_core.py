import pytest
import json
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config
from Data.logger import logger
from network.client import HttpClient
from cache.manager import CacheManager

class TestConfig:
    """测试配置管理"""
    
    def test_config_paths(self):
        """测试配置路径"""
        assert Config.BASE_DIR.exists()
        assert Config.DATA_DIR.exists()
        assert Config.UI_DIR.exists()
        
    def test_get_data_path(self):
        """测试数据路径获取"""
        test_file = "test.txt"
        expected_path = Config.DATA_DIR / test_file
        actual_path = Config.get_data_path(test_file)
        assert actual_path == expected_path

class TestHttpClient:
    """测试HTTP客户端"""
    
    def test_client_initialization(self):
        """测试客户端初始化"""
        client = HttpClient()
        assert client.session is not None
        client.close()
    
    @patch('requests.Session.get')
    def test_get_json_success(self, mock_get):
        """测试JSON获取成功"""
        mock_response = Mock()
        mock_response.json.return_value = {"test": "data"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        client = HttpClient()
        result = client.get_json("http://test.com")
        
        assert result == {"test": "data"}
        client.close()
    
    @patch('requests.Session.get')
    def test_get_json_failure(self, mock_get):
        """测试JSON获取失败"""
        mock_get.side_effect = Exception("Network error")
        
        client = HttpClient()
        result = client.get_json("http://test.com")
        
        assert result is None
        client.close()

class TestCacheManager:
    """测试缓存管理器"""
    
    def setup_method(self):
        """每个测试前的设置"""
        self.cache = CacheManager(max_size=5)
    
    def test_cache_set_get(self):
        """测试缓存设置和获取"""
        self.cache.set("test_key", "test_value")
        result = self.cache.get("test_key")
        assert result == "test_value"
    
    def test_cache_expiration(self):
        """测试缓存过期"""
        import time
        
        self.cache.set("test_key", "test_value", expire_time=1)  # 1秒过期
        time.sleep(1.1)  # 等待过期
        result = self.cache.get("test_key")
        assert result is None
    
    def test_cache_size_limit(self):
        """测试缓存大小限制"""
        # 添加超过限制的条目
        for i in range(7):
            self.cache.set(f"key_{i}", f"value_{i}")
        
        # 应该只有最新的5个条目
        assert len(self.cache.cache) <= 5
    
    def test_cache_stats(self):
        """测试缓存统计"""
        # 测试命中率计算
        self.cache.set("key1", "value1")
        self.cache.get("key1")  # 命中
        self.cache.get("nonexistent")  # 未命中
        
        stats = self.cache.get_stats()
        assert stats['hits'] == 1
        assert stats['misses'] == 1
        assert stats['hit_rate'] == 50.0

class TestLogger:
    """测试日志系统"""
    
    def test_logger_instance(self):
        """测试日志实例创建"""
        assert logger is not None
        assert logger.name == '猴面雀'

if __name__ == "__main__":
    pytest.main(["-v", __file__])