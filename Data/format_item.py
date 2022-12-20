import csv
import json
from concurrent.futures import ThreadPoolExecutor

import requests

"""
转换物品列表
"""
with open('item.csv', 'r', encoding='utf8') as item_file:
    item_in_list = csv.DictReader(item_file)
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
if '#' in item_out_list:
    del item_out_list['#']
if 'int32' in item_out_list:
    del item_out_list['int32']

"""
花环万岁！
"""


def get_item_details(item_id):
    url = 'https://garlandtools.cn/api/get.php?type=item&lang=chs&version=3&id=' + str(item_id)
    while True:
        try:
            result = requests.get(url, timeout=5)
            if result.status_code == 200:
                result = json.loads(result.text)['item']
                print(result['id'], end='\n')
                if 'vendors' in result:
                    item_out_list[item_id]['priceFromNpc'] = result['price']
                if 'craft' in result:
                    item_out_list[item_id]['craft'] = result['craft'][0]['ingredients']
                    if 'yield' in result['craft'][0]:
                        item_out_list[item_id]['yield'] = result['craft'][0]['yield']
                break
            else:
                break
        except:
            print(item_id, '查询失败，重试')


tpool = ThreadPoolExecutor(max_workers=100)
tpool.map(get_item_details, item_out_list)
tpool.shutdown(wait=True)

"""
数据写入磁盘
"""
# print(item_out_list)
version = {'data-version': '6.20'}
version.update(item_out_list)
with open('item.Pdt', 'w', encoding='utf8') as item_data:
    json.dump(version, item_data)
