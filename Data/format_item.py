import csv
import json
import os
import logging
from concurrent.futures import ThreadPoolExecutor

import requests

patch_version = float(os.environ['FFXIV_PATCH_VERSION'])
check_all = os.environ['CHECK_ALL']
log_level = os.environ['LOG_LEVEL'].upper()
numeric_level = getattr(logging, log_level, "INFO")

logging.basicConfig(level=numeric_level,
                    format='%(asctime)s : [%(levelname)s]  %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )

majar_verion = json.loads(requests.get("https://garlandtools.cn/db/doc/core/chs/3/data.json", timeout=5).text)['patch']['current']
min_verion = json.loads(requests.get(f"https://garlandtools.cn/db/doc/patch/chs/2/{majar_verion}.json", timeout=5).text)['patch']['patches']
garlandtools_version = max([float(key) for key in list(min_verion.keys())])

if patch_version != garlandtools_version:
    exit(0)

"""
可以在市场上交易的物品ID
https://universalis.app/api/marketable
"""
market_filter_address = 'https://universalis.app/api/marketable'
market_filter = requests.get(market_filter_address, timeout=5)

with open('marketable.py', 'w', encoding='utf8') as market_table:
    market_table.write('marketable = {}'.format(market_filter.text))
    market_table.close()
    logging.info("板子过滤数据更新完成")

"""
下载数据文件到本地
"""
Download_addres = f'https://raw.githubusercontent.com/thewakingsands/ffxiv-datamining-cn/master/Item.csv'
item_data = requests.get(Download_addres, timeout=9, verify=False)
logging.info('拆包数据下载成功，准备保存到本地')
with open("Item.csv", "w", encoding='UTF-8') as code:
    code.write(item_data.text)
    code.close()

"""
转换物品列表
"""
with open('Item.csv', 'r', encoding='UTF-8-sig') as item_file:
    item_in_list = csv.DictReader(item_file)
    logging.info('拆包文件读取成功，开始进行内容转换')
    item_out_list = {}
    for i in item_in_list:
        if i['key'] != '#' and i['key'] != 'int32':
            if i['0'] != '':
                item_out_list[i['key']] = {
                    'id': i['key'], 'name': i['0'], 'icon': i['10']}
total = list(item_out_list)[-1]
logging.info('数据列表准备完毕，准备抓取数据，数据集长度 {}'.format(total))

with open('item.Pdt', 'r', encoding='utf-8') as pdt_file:
    local_pdt = json.load(pdt_file)
logging.info('本地数据文件载入完毕')

"""
花环万岁！
"""


def query_item_in_local(item):
    if item not in local_pdt:
        logging.debug('本地不存在{}的数据，开始查询'.format(item))
        get_item_details(item)
    else:
        item_out_list[item].update(local_pdt[item])
        logging.debug('本地已存在{}的数据，跳过'.format(item))


def get_item_details(item_id):
    url = 'https://garlandtools.cn/api/get.php?type=item&lang=chs&version=3&id=' + str(item_id)
    while True:
        try:
            if item_id == '22357':
                logging.debug('物品ID 22357 为礼物盒，跳过')
                break
            logging.debug('开始处理物品ID {} '.format(item_id))
            result = json.loads(requests.get(url, timeout=7).text)['item']
            item_out_list[item_id]['patch'] = result['patch']
            if 'vendors' in result:
                item_out_list[item_id]['priceFromNpc'] = result['price']
            if 'craft' in result:
                item_out_list[item_id]['craft'] = result['craft'][0]['ingredients']
                if 'yield' in result['craft'][0]:
                    item_out_list[item_id]['yield'] = result['craft'][0]['yield']
            logging.info('物品ID {} / {}处理完毕'.format(result['id'], total))
            break
        except:
            logging.warn('物品ID {} 查询失败，重试'.format(item_id))


logging.info('建立线程池，准备进行数据抓取')
tpool = ThreadPoolExecutor(max_workers=20)
if check_all == "true":
    tpool.map(get_item_details, item_out_list)
else:
    tpool.map(query_item_in_local, item_out_list)
tpool.shutdown(wait=True)

"""
数据写入磁盘
"""
version = {'data-version': patch_version}
version.update(item_out_list)

with open('item.Pdt', 'w', encoding='utf8') as item_data:
    json.dump(version, item_data)

with open('version', 'r', encoding='utf8') as version_file:
    data_version = json.load(version_file)
    data_version.update({"data": patch_version})
    version_file.close()
with open('version', 'w', encoding='utf8') as version_file:
    json.dump(data_version, version_file)
    version_file.close()

logging.info('数据写入完毕')
