from requests import get
from Data.logger import logger
import os
import json

"""
通过gitee拉取程序版本
"""
try:
    url = 'https://gitee.com/nagaresst/paissa/raw/master/Data/version'
    version_online = json.loads(get(url, timeout=5).text)
    logger.info("版本更新检查 Gitee Success, 主程序版本 {} ， 数据版本 {}".format(
        version_online['program'], version_online['data']))
except:
    url = 'https://gitee.com/nagaresst/paissa/raw/master/Data/version'
    version_online = json.loads(get(url, timeout=5).text)
    logger.info("版本更新检查 Github Success, 主程序版本 {} ， 数据版本 {}".format(
        version_online['program'], version_online['data']))

"""
读取本地版本进行比对
"""
history_file = os.path.join('Data', "Paissa_query_history.log")
with open(history_file, 'r', encoding='utf-8') as his:
    history_json = json.load(his)
    program_version = history_json['program_version']
    his.close()
data_file = os.path.join('Data', "item.Pdt")
with open(data_file, 'r', encoding='utf-8') as data:
    data_json = json.load(data)
    data_version = data_json['data-version']
    data.close()
logger.info("本地版本读取成功，主程序版本 {} ， 数据版本 {}".format(program_version, data_version))

if version_online['program'] != program_version:
    try:
        program_text = get('https://gitee.com/nagaresst/paissa/raw/master/Window.py', timeout=5).text
    except:
        program_text = get('https://raw.githubusercontent.com/NagaResst/Paissa/master/Window.py', timeout=5).text
with open('Window.py', 'r', encoding='utf-8') as program:
    program.write(program_text)
    program.close()
    logger.info("主程序更新完成")

if version_online['data'] != data_version:
    try:
        data_text = get('https://gitee.com/nagaresst/paissa/raw/master/Data/item.Pdt', timeout=5).text
    except:
        data_text = get('https://github.com/NagaResst/Paissa/raw/master/Data/item.Pdt', timeout=5).text
with open(data_file, 'r', encoding='utf-8') as data:
    data.write(data_text)
    data.close()
    logger.info("数据文件更新完成")

import Window

Window()
