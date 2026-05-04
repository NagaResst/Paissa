import time
import copy
import threading
from typing import Dict, Any, Optional

from Data.logger import logger


class CacheManager:
    """成本树专用缓存管理器
    
    为成本树计算提供两级缓存：
    1. price_cache: 物品板子价格缓存（带过期时间）
    2. craft_cache: 物品制作配方缓存（带过期时间，深复制保护原始数据）
    
    线程安全，所有操作通过 RLock 保护。
    """

    def __init__(self, max_size: int = 500, default_expire: int = 300):
        self._lock = threading.RLock()
        self._max_size = max_size
        self._default_expire = default_expire

        # 价格缓存: {item_id: {"pricePerUnit": ..., "lowestPriceServer": ..., "_ts": timestamp}}
        self._price_cache: Dict[str, Dict[str, Any]] = {}
        # 配方缓存: {item_id: {"data": ..., "_ts": timestamp}}
        self._craft_cache: Dict[str, Dict[str, Any]] = {}

        self._price_hits = 0
        self._price_misses = 0
        self._craft_hits = 0
        self._craft_misses = 0

    # ---- 价格缓存 ----

    def get_price(self, item_id: str) -> Optional[Dict[str, Any]]:
        """获取物品价格缓存，命中返回深复制，未命中返回 None"""
        key = str(item_id)
        with self._lock:
            entry = self._price_cache.get(key)
            if entry is not None:
                if time.time() - entry['_ts'] < self._default_expire:
                    self._price_hits += 1
                    logger.debug(f"价格缓存命中: {key}")
                    return copy.deepcopy(entry['data'])
                else:
                    del self._price_cache[key]
                    logger.debug(f"价格缓存过期已清理: {key}")
            self._price_misses += 1
            return None

    def set_price(self, item_id: str, price_per_unit, lowest_price_server):
        """设置物品价格缓存"""
        key = str(item_id)
        with self._lock:
            if len(self._price_cache) >= self._max_size:
                self._evict_oldest(self._price_cache)
            self._price_cache[key] = {
                'data': {
                    'pricePerUnit': copy.deepcopy(price_per_unit),
                    'lowestPriceServer': copy.deepcopy(lowest_price_server),
                },
                '_ts': time.time(),
            }
            logger.debug(f"价格缓存已设置: {key}")

    # ---- 配方缓存 ----

    def get_craft(self, item_id: str) -> Optional[Dict[str, Any]]:
        """获取物品配方缓存，命中返回深复制，未命中返回 None"""
        key = str(item_id)
        with self._lock:
            entry = self._craft_cache.get(key)
            if entry is not None:
                if time.time() - entry['_ts'] < self._default_expire:
                    self._craft_hits += 1
                    logger.debug(f"配方缓存命中: {key}")
                    return copy.deepcopy(entry['data'])
                else:
                    del self._craft_cache[key]
                    logger.debug(f"配方缓存过期已清理: {key}")
            self._craft_misses += 1
            return None

    def set_craft(self, item_id: str, craft_data: Dict[str, Any]):
        """设置物品配方缓存，内部存储深复制"""
        key = str(item_id)
        with self._lock:
            if len(self._craft_cache) >= self._max_size:
                self._evict_oldest(self._craft_cache)
            self._craft_cache[key] = {
                'data': copy.deepcopy(craft_data),
                '_ts': time.time(),
            }
            logger.debug(f"配方缓存已设置: {key}")

    # ---- 统计与管理 ----

    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        with self._lock:
            price_total = self._price_hits + self._price_misses
            craft_total = self._craft_hits + self._craft_misses
            return {
                'price_cache_size': len(self._price_cache),
                'price_hits': self._price_hits,
                'price_misses': self._price_misses,
                'price_hit_rate': round(self._price_hits / price_total * 100, 1) if price_total else 0,
                'craft_cache_size': len(self._craft_cache),
                'craft_hits': self._craft_hits,
                'craft_misses': self._craft_misses,
                'craft_hit_rate': round(self._craft_hits / craft_total * 100, 1) if craft_total else 0,
            }

    def clear(self):
        """清空所有缓存"""
        with self._lock:
            self._price_cache.clear()
            self._craft_cache.clear()
            self._price_hits = 0
            self._price_misses = 0
            self._craft_hits = 0
            self._craft_misses = 0
        logger.info("成本树缓存已清空")

    def clear_price(self):
        """仅清空价格缓存"""
        with self._lock:
            self._price_cache.clear()
            self._price_hits = 0
            self._price_misses = 0
        logger.debug("价格缓存已清空")

    def _evict_oldest(self, cache: dict):
        """淘汰最旧的缓存条目"""
        if not cache:
            return
        oldest_key = min(cache.keys(), key=lambda k: cache[k]['_ts'])
        del cache[oldest_key]
        logger.debug(f"缓存已满，淘汰最旧条目: {oldest_key}")


# 全局缓存实例
cache_manager = CacheManager()
