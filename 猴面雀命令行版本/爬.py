#! /usr/bin/python3
from json import loads
from time import sleep

import pymysql
from requests import get


class ItemQuerier(object):
    def __init__(self, item_id):
        """
        对象初始化
        """
        self.id = item_id
        self.result = None

    def query_item(self):
        """
        查询物品的市场交易记录
        """
        query_url = 'https://universalis.app/api/猫小胖/%s?listings=20' % self.id
        while True:
            try:
                result = get(query_url, timeout=5)
                try:
                    self.result = loads(result.text)
                    break
                except:
                    pass
            except:
                sleep(3)

    def output_sell_list(self):
        """
        输出正在板子上售卖的商品
        """
        return self.result['listings']

    def output_buyer(self):
        """
        输出最近5次收购记录
        """
        return self.result['recentHistory']


def query_item_in_market():
    """
    查询所有可以在板子上交易的物品
    """
    query_url = 'https://universalis.app/api/marketable'
    result = get(query_url, timeout=5)
    result = result.text.replace('[', '').replace(']', '').split(',')
    return result


def query_user_id():
    """
    查询要匹配的身份ID
    """
    c = db.cursor()
    c.execute("select user_id from mid")
    record = c.fetchall()
    re_list = []
    for i in record:
        re_list.append(i[0])
    return re_list


def query_user_name():
    """
    查询用来匹配的用户名
    """
    c = db.cursor()
    c.execute("select * from userid")
    record = c.fetchall()
    re_list = {}
    for i in record:
        re_list[i[1]] = i[0]
    return re_list


def insert_sell_to_db(server, userId, retainerName, retainerId, itemId, itemName, creator):
    """
    当发现匹配目标时插入数据库
    """
    c = db.cursor()
    c.execute(
        "INSERT INTO sell_record ( server, userid,retainer,retainerid,item,itemname ,creator) VALUES  ( '%s','%s','%s','%s','%s','%s','%s' );" % (
            server, userId, retainerName, retainerId, itemId, itemName, creator))
    db.commit()


def insert_buy_to_db(itemId, server, timestamp):
    """
    当发现目标的购买行为时 插入数据库
    """
    c = db.cursor()
    c.execute(
        "INSERT INTO buy_record ( item,server, timestamp ) VALUES  ( '%s','%s','%s' );" % (
            itemId, server, str(timestamp)))
    db.commit()


def query_item_form_db():
    """
    只查询目标售卖的物品id
    """
    c = db.cursor()
    c.execute("select item from sell_record")
    record = c.fetchall()
    return record


def query_item_detial(itemid):
    """
    查询物品的详细信息，查询制作配方和统计成本的前置方法
    """
    query_url = 'https://garlandtools.cn/api/get.php?type=item&lang=chs&version=3&id=' + str(itemid)
    while True:
        try:
            result = get(query_url, timeout=5)
            result = loads(result.text)
            break
        except:
            print("%s 查询失败，重新查询物品名称" % item_id)
            sleep(1)
    return result['item']['name']


def delete_data_at_db():
    """
    清除数据库中上次查询的记录
    """
    c = db.cursor()
    c.execute("delete from buy_record; delete from sell_record;")
    db.commit()


db = pymysql.connect(
    host='192.168.10.100',
    port=4000,
    user='uupa',
    password='lingchuan',
    database='uupa',
    charset='utf8'
)

# db = pymysql.connect(
#     host='127.0.0.1',
#     port=3309,
#     user='root',
#     password='NagaResst123456',
#     database='papapa',
#     charset='utf8'
# )

m_id = query_user_id()
u_id = query_user_name()
print("已经获取到需要匹配的对象%d个。" % len(m_id))
# print(m_id)
# yon = input("是否需要清楚上次查询的记录")
# if yon == 'y':
delete_data_at_db()
i_id = query_item_in_market()
print("已经获取到可查询物品的ID。")
# startid = int(input('请输入开始ID \n'))
startid = 1
for item_id in i_id:
    if int(item_id) >= startid:
        print('正在查询物品id %s' % item_id)
        item_record = ItemQuerier(item_id)
        item_record.query_item()
        listings = item_record.output_sell_list()
        history = item_record.output_buyer()
        relist = []
        for record in listings:
            if record['creatorID'] in m_id or record['sellerID'] in m_id or record['retainerID'] in m_id:
                print("已发现雇员 %s 正在售卖物品 %s" % (record['retainerName'], item_record.id))
                if record['retainerID'] not in relist:
                    itemName = query_item_detial(item_id)
                    if record['sellerID'] in u_id:
                        seller = u_id[record['sellerID']]
                    else:
                        seller = record['sellerID']
                    if record['creatorID'] in u_id:
                        creator = u_id[record['creatorID']]
                    else:
                        creator = record['creatorID']
                    insert_sell_to_db(record['worldName'], seller, record['retainerName'],
                                      record['retainerID'], item_record.id, itemName, creator)
                    print('已将雇员 %s 记录到数据库中' % record['retainerName'])
                    relist.append(record['retainerID'])
        for record in history:
            if record['buyerName'] in ['爱丽丝铃']:
                insert_buy_to_db(item_record.id, record['worldName'], record['timestamp'])
db.close()
