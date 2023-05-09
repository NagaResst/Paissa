import csv
import json
from concurrent.futures import ThreadPoolExecutor
import logging
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
market_filter = requests.get(market_filter_address)

with open('marketable.py', 'w', encoding='utf8') as market_table:
    market_table.write('marketable = {}'.format(market_filter.text))
    market_table.close()


"""
下载数据文件到本地
"""
Download_addres = 'https://raw.githubusercontent.com/thewakingsands/ffxiv-datamining-cn/master/Item.csv'
f = requests.get(Download_addres)
logging.info('拆包数据下载成功，准备保存到本地')
# 下载文件
with open("Item.csv", "w") as code:
    code.write(f.text)
    code.close()

#TODO: 数据文件不保存到本地 直接使用
"""
转换物品列表
"""
with open('Item.csv', 'r', encoding='utf8') as item_file:
    item_in_list = csv.DictReader(item_file)
    logging.info('拆包文件读取成功，开始进行内容转换')
    item_out_list = {}
    for i in item_in_list:
        # print(i)
        # 不确定为什么有的时候会出现 \ufeff
        if '\ufeffkey' in i:
            if i['\ufeffkey'] != '#' and i['\ufeffkey'] != 'int32':
                if i['0'] != '':
                    item_out_list[i['\ufeffkey']] = {'id': i['\ufeffkey'], 'name': i['0'], 'icon': i['10']}
        else:
            if i['key'] != '#' and i['key'] != 'int32':
                if i['0'] != '':
                    item_out_list[i['key']] = {'id': i['key'], 'name': i['0'], 'icon': i['10']}
logging.info('数据转换完毕，开始除杂')
if '#' in item_out_list:
    del item_out_list['#']
if 'int32' in item_out_list:
    del item_out_list['int32']
logging.info('数据列表准备完毕，准备抓取数据，数据集长度 {}'.format(len(item_out_list)))

"""
花环万岁！
"""


def get_item_details(item_id):
    url = 'https://garlandtools.cn/api/get.php?type=item&lang=chs&version=3&id=' + str(item_id)
    while True:
        try:
            logging.info('开始处理物品ID {} '.format(item_id))
            result = requests.get(url, timeout=5)
            if result.status_code == 200:
                result = json.loads(result.text)['item']
                if 'vendors' in result:
                    item_out_list[item_id]['priceFromNpc'] = result['price']
                if 'craft' in result:
                    item_out_list[item_id]['craft'] = result['craft'][0]['ingredients']
                    if 'yield' in result['craft'][0]:
                        item_out_list[item_id]['yield'] = result['craft'][0]['yield']
                logging.info('物品ID {} 处理完毕'.format(result['id']))
                break
            else:
                break
        except:
            logging.warning('物品ID {} 查询失败，重试'.format(item_id))

logging.info('建立线程池，准备进行数据抓取')
tpool = ThreadPoolExecutor(max_workers=100)
tpool.map(get_item_details, item_out_list)
tpool.shutdown(wait=True)

"""
数据写入磁盘
"""
# print(item_out_list)
version = {'data-version': '6.3'}
version.update(item_out_list)
with open('item.Pdt', 'w', encoding='utf8') as item_data:
    json.dump(version, item_data)
logging.info('数据写入完毕')
