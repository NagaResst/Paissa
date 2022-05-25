import csv
import json

"""
转换物品列表
"""
with open('item.csv', 'r', encoding='utf8') as item_file:
    item_in_list = csv.DictReader(item_file)
    item_out_list = {}
    for i in item_in_list:
        # print(i)
        if i['16'] != '0' and i['0'] != '':
            item_out_list[i['\ufeffkey']] = {'ID': i['\ufeffkey'], 'Name': i['0'], 'Icon': i['10'],
                                             'priceFromNpc': i['25']}
if '#' in item_out_list:
    del item_out_list['#']
if 'int32' in item_out_list:
    del item_out_list['int32']

"""
查询是否可在商店购买
"""
with open('GilShopInfo.csv', 'r', encoding='utf8') as item_shop_info:
    item_can_buy = csv.DictReader(item_shop_info)
    temp = []
    for i in item_can_buy:
        temp.append(i)
    for key, item in item_out_list.items():
        print(item['ID'])
        for i in temp:
            if i['\ufeffkey'] == item['ID']:
                if i['0'] == '2' or i['0'] == '1':
                    updd = {'canBuy': True}
                else:
                    updd = {'canBuy': False}
                item_out_list[key].update(updd)
                break

"""
配方查询
"""
with open('Recipe.csv', 'r', encoding='utf8') as item_craft_info:
    item_craft = csv.DictReader(item_craft_info)
    temp = []
    for i in item_craft:
        temp.append(i)
    for key, item in item_out_list.items():
        print(item['ID'])
        for i in temp:
            if i['3'] == item['ID']:
                count = {'yield': i['4'], 'craft': [{'ID': i['5'], 'Amount': int(i['6'])}]}
                if int(i['8']) > 0:
                    c1 = {'ID': i['7'], 'Amount': int(i['8'])}
                    count['craft'].append(c1)
                    if int(i['10']) > 0:
                        c2 = {'ID': i['9'], 'Amount': int(i['10'])}
                        count['craft'].append(c2)
                        if int(i['12']) > 0:
                            c3 = {'ID': i['11'], 'Amount': int(i['12'])}
                            count['craft'].append(c3)
                            if int(i['14']) > 0:
                                c4 = {'ID': i['13'], 'Amount': int(i['14'])}
                                count['craft'].append(c4)
                                if int(i['16']) > 0:
                                    c5 = {'ID': i['15'], 'Amount': int(i['16'])}
                                    count['craft'].append(c5)
                c6 = {'ID': i['21'], 'Amount': i['22']}
                count['craft'].append(c6)
                if int(i['24']) > 0:
                    c7 = {'ID': i['23'], 'Amount': i['24']}
                    count['craft'].append(c7)
                item_out_list[key].update(count)
                break

"""
数据写入磁盘
"""
print(item_out_list)
version = {'data-version': '6.05'}
version.update(item_out_list)
with open('item.Pdt', 'w', encoding='utf8') as item_data:
    json.dump(version, item_data)
