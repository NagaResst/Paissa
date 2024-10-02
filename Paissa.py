import json
import os
import zipfile
import io
from requests import get
from urllib.request import getproxies

from Data.logger import logger

"""
通过阿里云拉取程序版本
"""
proxies = getproxies()
logger.info('获取系统代理 {}'.format(proxies))
version_online = False
try:
    url = 'https://paissa-data.oss-cn-hongkong.aliyuncs.com/version'
    version_online = json.loads(get(url, timeout=3, proxies=proxies).text)
    logger.info(
        "版本更新检查, 主程序版本 {} ， 数据版本 {}".format(version_online['program'], version_online['data']))
except:
    logger.warn("版本更新检查失败 ，没有获取到版本数据")

"""
读取本地版本进行比对
"""
try:
    history_file = os.path.join('Data', "Paissa_query_history.log")
    with open(history_file, 'r', encoding='utf-8') as his:
        history_json = json.load(his)
        program_version = history_json['program_version']
        his.close()
    logger.info("本地主程序版本 {}".format(program_version))
except:
    program_version = None
    logger.error("本地主程序版本检查失败")

try:
    data_file = os.path.join('Data', "item.Pdt")
    with open(data_file, 'r', encoding='utf-8') as data:
        data_json = json.load(data)
        data_version = data_json['data-version']
    logger.info("本地数据版本 {}".format(data_version))
except:
    data_version = None
    logger.error("本地数据版本检查失败")

if version_online['program'] != program_version:
    try:
        logger.info("从网络源更新主程序版本")
        program_text = get('https://paissa-data.oss-cn-hongkong.aliyuncs.com/Window.py', timeout=5, proxies=proxies).text
        query_text = get('https://paissa-data.oss-cn-hongkong.aliyuncs.com/Queryer.py', timeout=5, proxies=proxies).text
        with open('Window.py', 'w', encoding='utf-8') as program:
            program.write(program_text)
            program.close()
        with open('Queryer.py', 'w', encoding='utf-8') as queryer:
            queryer.write(query_text)
            queryer.close()
            logger.info("主程序更新完成")
    except:
        logger.warn("主程序更新失败")

if version_online['data'] != data_version:
    market_filter = False
    try:
        data_zip = get('https://paissa-data.oss-cn-hongkong.aliyuncs.com/item.zip', timeout=7, proxies=proxies).content
        logger.info("版本数据压缩包下载完成")
        zipFile = zipfile.ZipFile(io.BytesIO(data_zip), mode="r")
        data_text = zipFile.read('item.Pdt').decode('utf-8')
        logger.info("版本数据解析完成")
        data_file = os.path.join('Data', "item.Pdt")
        with open(data_file, 'w', encoding='utf-8') as data:
            data.write(data_text)
            data.close()
            logger.info("数据文件更新完成")
    except:
        logger.warn("版本数据下载失败")

    try:
        marketable_file = os.path.join('Data', "marketable.py")
        market_filter = 'marketable = {}'.format(get('https://universalis.app/api/marketable', timeout=5, proxies=proxies).text)
        if market_filter:
            with open(marketable_file, 'w', encoding='utf8') as market_table:
                market_table.write(market_filter)
                market_table.close()
                logger.info("板子过滤数据更新完成")
    except:
        logger.info("市场过滤数据下载失败")

import Window

Window()
