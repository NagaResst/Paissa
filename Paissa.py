#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paissa - FF14市场价格查询工具
主程序入口文件

作者: 夕山菀 @ 紫水栈桥
协议: LGPL 2.1
"""

import argparse
import json
import logging
import sys
import zipfile
import io
from pathlib import Path
from typing import Dict, Any, Optional

# 添加项目路径到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 导入本地模块
from config import Config
from network.client import http_client
from Data.logger import logger, log_performance

from PyQt5 import QtCore


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="Paissa - FF14市场价格查询工具")
    parser.add_argument('--dev', action='store_true', default=False,
                        help='开发模式：跳过更新，启用DEBUG日志')
    parser.add_argument('--skip-update', action='store_true', default=False,
                        help='跳过版本检查和更新')
    parser.add_argument('--version', type=str, default=None,
                        help='手动指定本地程序版本号')
    return parser.parse_args()


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
            url = Config.OSS_DATA_BASE_URL + '/version'
            
            for attempt in range(Config.MAX_RETRY_ATTEMPTS):
                # 快速重试，短间隔
                if attempt > 0:
                    logger.info(f"🔄 重试第{attempt + 1}次...")
                
                version_data = http_client.get_json(url, Config.TIMEOUT_SETTINGS['version_check'])
                if version_data:
                    self.version_online = version_data
                    logger.info(f"✅ 版本检查成功 v{version_data['program']}")
                    return True
                    
                logger.debug(f"⏳ 第{attempt + 1}次尝试失败")
                
                if attempt == Config.MAX_RETRY_ATTEMPTS - 1:
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
            if Config.HISTORY_FILE.exists():
                with open(Config.HISTORY_FILE, 'r', encoding='utf-8') as his:
                    history_json = json.load(his)
                    self.program_version = history_json.get('program_version')
            else:
                self.program_version = None
                
            if Config.ITEM_DATA_FILE.exists():
                with open(Config.ITEM_DATA_FILE, 'r', encoding='utf-8') as data:
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
                remote_url = f"{Config.OSS_DATA_BASE_URL}/{file}"
                file_content = http_client.get_text(remote_url, Config.TIMEOUT_SETTINGS['data_download'])
                if file_content:
                    with open(file, 'w', encoding='utf-8') as f:
                        f.write(file_content)
        except Exception as e:
            logger.error(f"程序更新失败: {e}")
    
    def update_data(self):
        """快速数据更新"""
        try:
            # 快速下载数据包
            data_zip = http_client.get_content(
                Config.OSS_DATA_BASE_URL + '/item.zip',
                timeout = 8
            )
            
            if data_zip:
                with zipfile.ZipFile(io.BytesIO(data_zip), mode="r") as zip_file:
                    data_text = zip_file.read('item.Pdt').decode('utf-8')
                with open(Config.ITEM_DATA_FILE, 'w', encoding='utf-8') as f:
                    f.write(data_text)
                    
                # 快速更新市场数据
                market_data = http_client.get_text(Config.UNIVERSALIS_BASE_URL + '/api/marketable')
                if market_data:
                    with open(Config.MARKETABLE_FILE, 'w', encoding='utf8') as f:
                        f.write(f'marketable = {market_data}')
                        
        except Exception as e:
            logger.error(f"数据更新失败: {e}")


class UpdateThread(QtCore.QThread):
    """异步执行版本检查和数据更新的线程"""
    
    def __init__(self, version_manager: VersionManager):
        super().__init__()
        self.version_manager = version_manager

    def run(self):
        if not self.version_manager.check_online_version():
            return
        update_manager = UpdateManager(self.version_manager)
        if self.version_manager.need_program_update():
            update_manager.update_program()
        if self.version_manager.need_data_update():
            update_manager.update_data()


@log_performance
def main():
    """主程序入口 - 快速启动"""
    args = parse_args()

    if args.dev:
        logger.setLevel(logging.DEBUG)
        logger.info("开发模式启动")

    skip_update = args.dev or args.skip_update

    try:
        version_manager = VersionManager()
        version_manager.load_local_versions()

        if args.version is not None:
            version_manager.program_version = args.version
            logger.info(f"手动指定版本号: {args.version}")

        # 启动主窗口
        import Window
        Window.Window()

        # UI 创建后异步执行版本检查和更新
        if not skip_update:
            update_thread = UpdateThread(version_manager)
            update_thread.start()
        else:
            logger.info("跳过版本更新检查")

    except KeyboardInterrupt:
        logger.info("用户退出")
        sys.exit(0)
    except Exception as e:
        logger.error(f"启动失败: {e}")
        print(f"启动失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()