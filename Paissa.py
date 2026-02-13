#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paissa - FF14市场价格查询工具
主程序入口文件

作者: 夕山菀 @ 紫水栈桥
协议: LGPL 2.1
"""

import json
import sys
import zipfile
import io
from pathlib import Path
from typing import Dict, Any, Optional

# 添加项目路径到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 导入本地模块
import config
from network.client import http_client
from Data.logger import logger, log_performance


class VersionManager:
    """版本管理器 - 快速重试优化"""
    
    def __init__(self):
        self.version_online: Optional[Dict[str, Any]] = None
        self.program_version: Optional[str] = None
        self.data_version: Optional[float] = None
        
    @log_performance
    def check_online_version(self) -> bool:
        """快速版本检查 - 短快多重试"""
        try:
            url = 'https://paissa-data.oss-cn-hongkong.aliyuncs.com/version'
            
            for attempt in range(config.Config.MAX_RETRY_ATTEMPTS):
                # 快速重试，短间隔
                if attempt > 0:
                    logger.info(f"🔄 重试第{attempt + 1}次...")
                
                version_data = http_client.get_json(url, config.Config.TIMEOUT_SETTINGS['version_check'])
                if version_data:
                    self.version_online = version_data
                    logger.info(f"✅ 版本检查成功 v{version_data['program']}")
                    return True
                    
                logger.debug(f"⏳ 第{attempt + 1}次尝试失败")
                
                if attempt == config.Config.MAX_RETRY_ATTEMPTS - 1:
                    logger.warning("❌ 版本检查最终失败")
                    return False
                    
        except Exception as e:
            logger.error(f"版本检查异常: {e}")
            return False
            
        return False
    
    @log_performance
    def load_local_versions(self):
        """加载本地版本信息"""
        try:
            if config.Config.HISTORY_FILE.exists():
                with open(config.Config.HISTORY_FILE, 'r', encoding='utf-8') as his:
                    history_json = json.load(his)
                    self.program_version = history_json.get('program_version')
            else:
                self.program_version = None
                
            if config.Config.ITEM_DATA_FILE.exists():
                with open(config.Config.ITEM_DATA_FILE, 'r', encoding='utf-8') as data:
                    data_json = json.load(data)
                    self.data_version = float(data_json.get('data-version', 0))
            else:
                self.data_version = 0.0
                
        except Exception:
            self.program_version = None
            self.data_version = 0.0
    
    def need_program_update(self) -> bool:
        """检查是否需要更新程序"""
        if not self.version_online or not self.program_version:
            return False
        return self.version_online.get('program') != self.program_version
    
    def need_data_update(self) -> bool:
        """检查是否需要更新数据"""
        if not self.version_online or self.data_version is None:
            return False
        return float(self.version_online.get('data', 0)) > self.data_version


class UpdateManager:
    """更新管理器"""
    
    def __init__(self, version_manager: VersionManager):
        self.version_manager = version_manager
    
    def update_program(self):
        """快速程序更新"""
        if not self.version_manager.version_online:
            return
            
        try:
            files_to_update = self.version_manager.version_online.get('files', [])
            for file in files_to_update:
                remote_url = f"https://paissa-data.oss-cn-hongkong.aliyuncs.com/{file}"
                file_content = http_client.get_text(remote_url, config.Config.TIMEOUT_SETTINGS['data_download'])
                if file_content:
                    with open(file, 'w', encoding='utf-8') as f:
                        f.write(file_content)
        except:
            pass
    
    def update_data(self):
        """快速数据更新"""
        try:
            # 快速下载数据包
            data_zip = http_client.get_content(
                'https://paissa-data.oss-cn-hongkong.aliyuncs.com/item.zip',
                config.Config.TIMEOUT_SETTINGS['data_download']
            )
            
            if data_zip:
                with zipfile.ZipFile(io.BytesIO(data_zip), mode="r") as zip_file:
                    data_text = zip_file.read('item.Pdt').decode('utf-8')
                with open(config.Config.ITEM_DATA_FILE, 'w', encoding='utf-8') as f:
                    f.write(data_text)
                    
                # 快速更新市场数据
                market_data = http_client.get_text('https://universalis.app/api/marketable')
                if market_data:
                    with open(config.Config.MARKETABLE_FILE, 'w', encoding='utf8') as f:
                        f.write(f'marketable = {market_data}')
                        
        except:
            pass


@log_performance
def main():
    """主程序入口 - 快速启动"""
    logger.info("🚀 猴面雀启动")
    
    try:
        # 快速版本检查
        version_manager = VersionManager()
        if version_manager.check_online_version():
            version_manager.load_local_versions()
            update_manager = UpdateManager(version_manager)
            
            # 快速更新
            if version_manager.need_program_update():
                update_manager.update_program()
            if version_manager.need_data_update():
                update_manager.update_data()
        
        # 快速启动主窗口
        import Window
        Window.Window()
        
    except KeyboardInterrupt:
        logger.info("用户退出")
        sys.exit(0)
    except Exception as e:
        logger.error(f"启动失败: {e}")
        sys.exit(1)
    finally:
        http_client.close()


if __name__ == "__main__":
    main()