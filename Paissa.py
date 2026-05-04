#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paissa - FF14市场价格查询工具
主程序入口文件（引导程序）

本文件作为自动更新的引导程序，必须在所有新模块（network/、cache/等）就绪之前
就能独立运行。因此更新逻辑仅依赖标准库 + requests + Data.logger，
不导入任何新分支新增的模块。

自动更新兼容流程：
  旧版 Paissa.py 按顺序下载 files 列表中的文件：
  1. Paissa.py（首位）→ 写入成功
  2. 其他根目录文件 → 写入成功
  3. network/client.py → 因缺少子目录失败，异常被捕获
  4. import Window; Window() → 新 Window 不可调用，程序崩溃
  用户重新启动 → 新版 Paissa.py 运行 → 创建子目录并下载全部文件 → 正常启动

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

# ---- 引导阶段：仅使用标准库 + requests（旧版已有此依赖） ----
from requests import get as requests_get
from urllib.request import getproxies

# 项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Data.logger 在旧版就存在，可安全导入
from Data.logger import logger


# ---- 配置常量（引导阶段不能依赖 config.py，硬编码必要值） ----
_OSS_BASE_URL = 'https://paissa-data.oss-cn-hongkong.aliyuncs.com'
_UNIVERSALIS_BASE_URL = 'https://universalis.app/api'
_MAX_RETRIES = 3
_TIMEOUT_VERSION = 3
_TIMEOUT_DOWNLOAD = 5
_TIMEOUT_DATA = 8


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


# ---- 引导阶段 HTTP 请求（不依赖 network.client） ----

def _get_proxies_and_headers():
    """获取代理和请求头"""
    return getproxies(), {"referer": "http://Paissa.public/"}


def _request_json(url, timeout=3):
    """获取JSON数据，带重试"""
    proxies, headers = _get_proxies_and_headers()
    for attempt in range(_MAX_RETRIES):
        try:
            resp = requests_get(url, timeout=timeout, proxies=proxies, headers=headers)
            if resp.status_code == 200:
                return resp.json()
            logger.debug(f"HTTP {resp.status_code}: {url}")
        except Exception as e:
            logger.debug(f"请求失败第{attempt+1}次: {e}")
    return None


def _request_text(url, timeout=5):
    """获取文本数据"""
    proxies, headers = _get_proxies_and_headers()
    try:
        resp = requests_get(url, timeout=timeout, proxies=proxies, headers=headers)
        resp.encoding = 'utf-8'
        if resp.status_code == 200:
            return resp.text
    except Exception:
        pass
    return None


def _request_content(url, timeout=8):
    """获取二进制内容"""
    proxies, headers = _get_proxies_and_headers()
    try:
        resp = requests_get(url, timeout=timeout, proxies=proxies, headers=headers)
        if resp.status_code == 200:
            return resp.content
    except Exception:
        pass
    return None


# ---- 版本与更新逻辑 ----

def load_local_versions():
    """加载本地版本信息"""
    program_version = None
    data_version = 0.0

    try:
        history_file = Path('Data') / 'Paissa_query_history.log'
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as his:
                history_json = json.load(his)
                program_version = history_json.get('program_version')
    except Exception:
        pass

    try:
        data_file = Path('Data') / 'item.Pdt'
        if data_file.exists():
            with open(data_file, 'r', encoding='utf-8') as data:
                data_json = json.load(data)
                data_version = float(data_json.get('data-version', 0))
    except Exception:
        pass

    return program_version, data_version


def update_program(files):
    """下载并写入所有程序文件，自动创建子目录和 __init__.py"""
    created_dirs = set()

    for file in files:
        remote_url = f"{_OSS_BASE_URL}/{file}"
        content = _request_text(remote_url, _TIMEOUT_DOWNLOAD)
        if content:
            file_path = Path(file)
            # 自动创建父目录
            if file_path.parent != Path('.'):
                file_path.parent.mkdir(parents=True, exist_ok=True)
                # 为新增的子目录自动创建 __init__.py
                parent_str = str(file_path.parent)
                if parent_str not in created_dirs:
                    init_file = file_path.parent / '__init__.py'
                    if not init_file.exists():
                        init_file.write_text('', encoding='utf-8')
                    created_dirs.add(parent_str)
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"已更新: {file}")
        else:
            logger.warning(f"下载失败: {file}")

    logger.info("程序文件更新完成")


def update_data():
    """下载并更新数据文件"""
    try:
        data_zip = _request_content(_OSS_BASE_URL + '/item.zip', _TIMEOUT_DATA)
        if data_zip:
            with zipfile.ZipFile(io.BytesIO(data_zip), mode="r") as zip_file:
                data_text = zip_file.read('item.Pdt').decode('utf-8')
            data_file = Path('Data') / 'item.Pdt'
            data_file.parent.mkdir(exist_ok=True)
            with open(data_file, 'w', encoding='utf-8') as f:
                f.write(data_text)
            logger.info("数据文件更新完成")

        market_data = _request_text(_UNIVERSALIS_BASE_URL + '/marketable')
        if market_data:
            marketable_file = Path('Data') / 'marketable.py'
            marketable_file.parent.mkdir(exist_ok=True)
            with open(marketable_file, 'w', encoding='utf8') as f:
                f.write(f'marketable = {market_data}')
            logger.info("市场数据更新完成")
    except Exception as e:
        logger.error(f"数据更新失败: {e}")


def save_program_version(version):
    """更新成功后写入新版本号，避免重复下载"""
    try:
        history_file = Path('Data') / 'Paissa_query_history.log'
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = {}
        history['program_version'] = version
        history_file.parent.mkdir(exist_ok=True)
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False)
        logger.info(f"版本号已更新: {version}")
    except Exception as e:
        logger.warning(f"版本号写入失败: {e}")


# ---- 主入口 ----

def main():
    """主程序入口 - 引导更新后再启动UI"""
    args = parse_args()

    if args.dev:
        logger.setLevel(logging.DEBUG)
        logger.info("开发模式启动")

    skip_update = args.dev or args.skip_update

    if not skip_update:
        # 获取在线版本
        version_online = _request_json(_OSS_BASE_URL + '/version', _TIMEOUT_VERSION)

        if version_online:
            program_version, data_version = load_local_versions()

            if args.version is not None:
                program_version = args.version
                logger.info(f"手动指定版本号: {args.version}")

            # 程序更新
            if version_online.get('program') != program_version:
                logger.info("检测到程序版本更新")
                files = version_online.get('files', [])
                update_program(files)
                # 更新成功后保存版本号，避免下次重复下载
                save_program_version(version_online.get('program'))

            # 数据更新
            if float(version_online.get('data', 0)) > float(data_version):
                logger.info("检测到数据版本更新")
                update_data()
        else:
            logger.warning("版本检查失败，跳过更新")
    else:
        logger.info("跳过版本更新检查")

    # === 所有文件已就绪，安全导入应用模块 ===
    import Window
    Window.run_app()


if __name__ == "__main__":
    main()
