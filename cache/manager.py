import time
import os
import sys
from typing import Dict, Any, Optional
from functools import wraps

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from Data.logger import logger

class CacheManager:
    """数据缓存管理器"""
    
    def __init__(self, max_size: int = 1000):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def _get_cache_key(self, func_name: str, *args, **kwargs) -> str:
        """生成缓存键"""
        key_parts = [func_name]
        key_parts.extend(str(arg) for arg in args)
        key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
        return "|".join(key_parts)
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存数据"""
        if key in self.cache:
            item = self.cache[key]
            if time.time() - item['timestamp'] < item['expire_time']:
                self.hits += 1
                logger.debug(f"缓存命中: {key}")
                return item['data']
            else:
                # 缓存过期，删除
                del self.cache[key]
                logger.debug(f"缓存过期已清理: {key}")
        self.misses += 1
        return None
    
    def set(self, key: str, data: Any, expire_time: int = 300):
        """设置缓存数据"""
        # 如果缓存满了，删除最旧的条目
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]
            logger.debug(f"缓存已满，删除最旧条目: {oldest_key}")
        
        self.cache[key] = {
            'data': data,
            'timestamp': time.time(),
            'expire_time': expire_time
        }
        logger.debug(f"缓存已设置: {key}")
    
    def cache_with_expire(self, expire_time: int = 300):
        """缓存装饰器"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = self._get_cache_key(func.__name__, *args, **kwargs)
                
                # 尝试从缓存获取
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # 执行函数并缓存结果
                result = func(*args, **kwargs)
                if result is not None:
                    self.set(cache_key, result, expire_time)
                
                return result
            return wrapper
        return decorator
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'cache_size': len(self.cache),
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': round(hit_rate, 2),
            'max_size': self.max_size
        }
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        logger.info("缓存已清空")

# 全局缓存实例
cache_manager = CacheManager()