import csv
import json
import logging
from concurrent.futures import ThreadPoolExecutor

import requests

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s : <%(module)s>  [%(levelname)s]  %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )

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
# 这里使用了镜像站下载资源，如果镜像站不可用，需要修改资源下载地址
Download_addres = 'https://mirror.ghproxy.com/https://raw.githubusercontent.com/thewakingsands/ffxiv-datamining-cn/master/Item.csv'
item_data = requests.get(Download_addres, timeout=9)
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
        logging.info('本地不存在{}的数据，开始查询'.format(item))
        get_item_details(item)
    else:
        item_out_list[item].update(local_pdt[item])
        logging.debug('本地已存在{}的数据，跳过'.format(item))


def get_item_details(item_id):
    url = 'https://garlandtools.cn/api/get.php?type=item&lang=chs&version=3&id=' + str(item_id)
    while True:
        try:
            if item_id == '22357':
                logging.warning('物品ID 22357 查询失败，跳过')
                break
            logging.info('开始处理物品ID {} '.format(item_id))
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
            logging.warning('物品ID {} 查询失败，重试'.format(item_id))


logging.info('建立线程池，准备进行数据抓取')
tpool = ThreadPoolExecutor(max_workers=20)
# tpool.map(query_item_in_local, item_out_list)
# 强制更新所有数据
tpool.map(get_item_details, item_out_list)
tpool.shutdown(wait=True)

"""
数据写入磁盘
"""
version = {'data-version': '6.45'}
version.update(item_out_list)

with open('item.Pdt', 'w', encoding='utf8') as item_data:
    json.dump(version, item_data)
logging.info('数据写入完毕')
