import json
import os
import zipfile
import io
from requests import get

from Data.logger import logger

"""
通过gitee拉取程序版本
"""
version_online = False
try:
    url = 'https://gitee.com/nagaresst/paissa/raw/master/Data/version'
    version_online = json.loads(get(url, timeout=3).text)
    logger.info(
        "版本更新检查 Gitee Success, 主程序版本 {} ， 数据版本 {}".format(version_online['program'], version_online['data']))
except:
    logger.info(
        "版本更新检查 Gitee Success, 失败 ， 没有获取到版本数据")

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
    logger.info("本地主程序版本检查失败")

data_file = os.path.join('Data', "item.Pdt")
marketable_file = os.path.join('Data', "marketable.py")

try:
    with open(data_file, 'r', encoding='utf-8') as data:
        data_json = json.load(data)
        data_version = data_json['data-version']
    logger.info("本地数据版本 {}".format(data_version))
except:
    data_version = None
    logger.info("本地数据版本检查失败")

if version_online['program'] != program_version:
    try:
        logger.info("从 Gitee 更新主程序版本")
        # program_text = get('https://raw.githubusercontent.com/NagaResst/Paissa/master/Window.py', timeout=5).text
        # query_text = get('https://raw.githubusercontent.com/NagaResst/Paissa/master/Queryer.py', timeout=5).text
        program_text = get('https://gitee.com/nagaresst/paissa/raw/master/Window.py', timeout=5).text
        query_text = get('https://gitee.com/nagaresst/paissa/raw/master/Queryer.py', timeout=5).text
        with open('Window.py', 'w', encoding='utf-8') as program:
            program.write(program_text)
            program.close()
        with open('Queryer.py', 'w', encoding='utf-8') as queryer:
            queryer.write(query_text)
            queryer.close()
            logger.info("主程序更新完成")
    except:
        logger.info("主程序更新失败")

if version_online['data'] != data_version:
    market_filter = False
    try:
        # data_text = get('https://raw.githubusercontent.com/NagaResst/Paissa/master/Data/item.Pdt', timeout=5).text
        logger.info("从 gitee 更新数据版本")
        data_zip = get('https://gitee.com/nagaresst/paissa/raw/master/Data/item.zip', timeout=7).content
        logger.info("版本数据压缩包下载完成")
        zipFile = zipfile.ZipFile(io.BytesIO(data_zip), mode="r")
        data_text = zipFile.read('item.Pdt').decode('utf-8')
        logger.info("版本数据解析完成")
        with open(data_file, 'w', encoding='utf-8') as data:
            data.write(data_text)
            data.close()
            logger.info("数据文件更新完成")
    except:
        logger.info("版本数据下载失败")

    try:
        market_filter = 'marketable = {}'.format(get('https://universalis.app/api/marketable', timeout=5).text)
        if market_filter:
            with open(marketable_file, 'w', encoding='utf8') as market_table:
                market_table.write(market_filter)
                market_table.close()
                logger.info("板子过滤数据更新完成")
    except:
        logger.info("市场过滤数据下载失败")


import Window

Window()
