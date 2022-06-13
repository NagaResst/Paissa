import copy
import re
import threading
import time
# from concurrent.futures import ThreadPoolExecutor
from json import loads, load
from math import ceil

from requests import get

from marketable import marketable


class Queryer(object):
    def __init__(self, query_server, item_id=None):
        """
        对象初始化
        """
        self.name = None
        self.hq = False
        # item_list 代表本次查询的结果集
        self.item_list = []
        self.id = item_id
        self.stuff = {}
        self.avgp = 0
        self.yields = 1
        self.nqs = 0
        self.hqs = 0
        self.d_cost = 0
        self.o_cost = 0
        self.server = query_server
        self.every_server = []
        self.icon = None
        self.item_data = {}
        self.static = True
        self.proxy = False
        self.filter_item = True
        self.clipboard = ''
        self.header = {'User-Agent': 'Paissa 0.8.0'}
        self.price_cache = {}

    def init_query_result(self, url, site=None):
        """
        查询结果序列化成字典
        """
        if site == 'universalis' and self.proxy is True:
            url = 'http://43.142.142.18/universalis' + url
        elif site == 'universalis' and self.proxy is False:
            url = 'https://universalis.app' + url
        while True:
            try:
                result = get(url, timeout=5, headers=self.header)
                if result.status_code == 200:
                    result = loads(result.text)
                    break
                else:
                    print(url, result.status_code)
            except:
                print(url, 'failed')
        return result

    @staticmethod
    def timestamp_to_time(timestamp):
        """
        时间戳转换方法
        """
        if timestamp > 9999999999:
            timestamp = float(timestamp / 1000)
        timearray = time.localtime(timestamp)
        result = time.strftime("%Y-%m-%d %H:%M:%S", timearray)
        return result

    def get_icon(self, icon_url=None):
        """
        获取图标的方法，数据源不一致，获取图标的地址也不同
        """
        self.icon = None
        if len(self.item_list) == 0:
            self.query_item_id(self.name)
        if len(self.item_list) > 1 and self.static is False:
            for i in self.item_list:
                if str(i['id']) == str(self.id):
                    icon_url = "https://cafemaker.wakingsands.com" + i['icon']
        elif len(self.item_list) > 1 and self.static is True:
            icon_url = "https://garlandtools.cn/files/icons/item/" + self.item_data[str(self.id)]['icon'] + '.png'
        elif len(self.item_list) == 1 and self.static is False:
            icon_url = "https://cafemaker.wakingsands.com" + self.item_list[0]['icon']
        elif len(self.item_list) == 1 and self.static is True:
            icon_url = "https://garlandtools.cn/files/icons/item/" + self.item_data[str(self.id)]['icon'] + '.png'
        try:
            result = get(icon_url, timeout=3, headers=self.header)
            self.icon = result.content
        except:
            print('图标获取失败')

    def server_list(self):
        """
        为查询所有区服最低价提供支持
        https://ff.web.sdo.com/web8/index.html#/servers
        跨大区开放后 server_list 将返回所有区服的列表
        """
        select_server_mao = ['猫小胖', '紫水栈桥', '延夏', '静语庄园', '摩杜纳', '海猫茶屋', '柔风海湾', '琥珀原']
        select_server_zhu = ['莫古力', '白银乡', '白金幻象', '神拳痕', '潮风亭', '旅人栈桥', '拂晓之间', '龙巢神殿', '梦羽宝境']
        select_server_niao = ['陆行鸟', '红玉海', '神意之地', '拉诺西亚', '幻影群岛', '萌芽池', '宇宙和音', '沃仙曦染', '晨曦王座']
        select_server_gou = ['豆豆柴', '水晶塔', '银泪湖', '太阳海岸', '伊修加德', '红茶川']
        # 设置默认大区为猫区
        server_list = select_server_mao
        # 根据服务器所在大区选择比价的服务器
        if self.server in select_server_mao:
            server_list = select_server_mao[1:]
        elif self.server in select_server_niao:
            server_list = select_server_niao[1:]
        elif self.server in select_server_zhu:
            server_list = select_server_zhu[1:]
        elif self.server in select_server_gou:
            server_list = select_server_gou[1:]
        return server_list

    def query_item_id(self, name):
        """
        查询官方的物品ID，为后面的查询提供支持
        """
        self.item_list = []
        if self.static is False:
            query_url = 'https://cafemaker.wakingsands.com/search?indexes=item&string=' + name
            result = self.init_query_result(query_url)
            all_list = result["Results"]
            for item in all_list:
                # 过滤掉不可在市场上交易的物品
                if self.filter_item is True and item['ID'] in marketable:
                    this_item = {'id': item['ID'], 'name': item['Name'], 'icon': item['Icon']}
                    self.item_list.append(this_item)
                elif self.filter_item is False:
                    this_item = {'id': item['ID'], 'name': item['Name'], 'icon': item['Icon']}
                    self.item_list.append(this_item)
            self.item_list = sorted(self.item_list, key=lambda e: e.__getitem__('id'), reverse=False)
        elif self.static is True:
            for item in self.item_data.values():
                if re.search(name, item['name']) is not None and self.filter_item is True and int(
                        item['id']) in marketable:
                    self.item_list.append(item)
                elif re.search(name, item['name']) is not None and self.filter_item is False:
                    self.item_list.append(item)

    def query_item_price(self):
        """
        查询市场价格，根据HQ参数选择查询方法
        """
        if self.hq is True:
            query_url = '/api/v2/%s/%s?listings=50&hq=true&noGst=true' % (
                self.server, self.id)
        else:
            query_url = '/api/%s/%s?listings=50&noGst=true' % (self.server, self.id)
        result = self.init_query_result(query_url, 'universalis')
        # 如果查询不到物品，强制重查一次NQ
        if self.hq is True and len(result['listings']) == 0:
            self.hq = False
            query_url = '/api/%s/%s?listings=50&noGst=true' % (self.server, self.id)
            result = self.init_query_result(query_url, 'universalis')
        if result['nqSaleVelocity'] == 0:
            self.avgp = int(result['averagePriceHQ'])
        elif result['hqSaleVelocity'] / result['nqSaleVelocity'] > 3:
            self.avgp = int(result['averagePriceHQ'])
        else:
            self.avgp = int(result['averagePriceNQ'])
        self.nqs = result['nqSaleVelocity']
        self.hqs = result['hqSaleVelocity']
        return result

    def query_every_server(self, server_list):
        """
        大区内服务器比价
        """
        self.every_server = []

        def query_single_server(server, item_id):
            query_url = '/api/%s/%s?listings=1&noGst=true' % (server, item_id)
            result = self.init_query_result(query_url, 'universalis')
            # 重新组织比价用的数据
            if len(result['listings']) != 0:
                server_sale = {
                    'server': server,
                    'pricePerUnit': result['listings'][0]['pricePerUnit'],
                    'hq': result['listings'][0]['hq'],
                    'quantity': result['listings'][0]['quantity'],
                    'total': result['listings'][0]['total'],
                    'retainerName': result['listings'][0]['retainerName'],
                    'lastReviewTime': result['listings'][0]['lastReviewTime']
                }
                self.every_server.append(server_sale)

        threads = []
        for server in server_list:
            thread = threading.Thread(target=query_single_server, args=(server, self.id))
            thread.start()
            threads.append(thread)
        for t in threads:
            t.join()

    def query_item_craft(self):
        """
        查询物品的制作材料
        """
        if len(self.stuff) == 0:
            if self.static is False:
                query_url = 'https://garlandtools.cn/api/get.php?type=item&lang=chs&version=3&id=' + str(self.id)
                self.stuff = self.init_query_result(query_url)['item']
                if 'craft' in self.stuff:
                    if 'yield' in self.stuff['craft'][0]:
                        self.yields = self.stuff['craft'][0]['yield']
                        self.stuff['yield'] = self.stuff['craft'][0]['yield']
                    self.stuff['craft'] = self.stuff['craft'][0]['ingredients']
                    self.make_item_craft(self.stuff['craft'])
                else:
                    self.stuff = {}
            elif self.static is True:
                self.stuff = copy.deepcopy(self.item_data[str(self.id)])
                if 'craft' in self.stuff:
                    if 'yield' in self.stuff:
                        self.yields = self.stuff['yield']
                    self.make_item_craft(self.stuff['craft'])
                else:
                    self.stuff = {}

    def make_child_item_craft(self, unit):
        """
        材料树递归查询的线程函数
        """
        result = self.query_item_detial(unit['id'])
        unit['name'] = result['name']
        self.query_item_cost_min(unit)
        if self.static is False:
            if 'vendors' in result:
                unit['priceFromNpc'] = result['price']
            if 'craft' in result:
                unit['craft'] = result['craft']
                if 'yield' in result:
                    unit['yield'] = result['yield']
                self.make_item_craft(unit['craft'])
        elif self.static is True:
            if 'priceFromNpc' in result:
                unit['priceFromNpc'] = result['priceFromNpc']
            if 'craft' in result:
                unit['craft'] = result['craft']
                if 'yield' in result:
                    unit['yield'] = result['yield']
                self.make_item_craft(unit['craft'])

    def make_child_item_craft_new(self, unit):
        result = self.query_item_detial(unit['id'])
        unit['name'] = result['name']
        items = []
        if 'pricePerUnit' not in unit:
            self.query_item_cost_min(unit)
        if self.static is False:
            if 'vendors' in result:
                unit['priceFromNpc'] = result['price']
        elif self.static is True:
            if 'priceFromNpc' in result:
                unit['priceFromNpc'] = result['priceFromNpc']
        if 'craft' in result:
            unit['craft'] = result['craft']
            for i in unit['craft']:
                items.append(i)
                r = self.query_item_detial(i['id'])
                i['name'] = r['name']
                if 'craft' in r:
                    i['craft'] = r['craft']
                    if 'yield' in r:
                        i['yield'] = r['yield']
            self.query_item_cost_min(items)
            self.make_item_craft(unit['craft'])

    def make_item_craft(self, stuff_list):
        """
        统计物品的制作材料
        新旧两种查询方法在大量查询的时候都会产生返回429的现象，导致查询速度慢，但新的查询方法在查询复杂配方的时候速度提升明显。
        """
        threads = []
        if len(stuff_list) > 5:
            for unit in stuff_list:
                thread_make_child_craft = threading.Thread(target=self.make_child_item_craft_new, args=[unit])
                thread_make_child_craft.start()
                threads.append(thread_make_child_craft)
                # debug
                # thread_make_child_craft.join()
        else:
            for unit in stuff_list:
                thread_make_child_craft = threading.Thread(target=self.make_child_item_craft, args=[unit])
                thread_make_child_craft.start()
                threads.append(thread_make_child_craft)
                # debug
                # thread_make_child_craft.join()
        for i in threads:
            i.join()

    def query_item_detial(self, itemid):
        """
        查询物品的详细信息，查询制作配方和统计成本的前置方法
        """
        if self.static is False:
            query_url = 'https://garlandtools.cn/api/get.php?type=item&lang=chs&version=3&id=' + str(itemid)
            result = self.init_query_result(query_url)['item']
            if 'craft' in result:
                if 'yield' in result['craft'][0]:
                    result['yield'] = result['craft'][0]['yield']
                result['craft'] = result['craft'][0]['ingredients']
            return result
        elif self.static is True:
            # 重要： 采用深复制来避免成本树的计算波及到保存在内存中的静态原始数据
            return copy.deepcopy(self.item_data[str(itemid)])

    def query_item_cost_min(self, item):
        """
        查询单项物品的板子价格
        """
        select_server_zhu = ['莫古力', '白银乡', '白金幻象', '神拳痕', '潮风亭', '旅人栈桥', '拂晓之间', '龙巢神殿', '梦羽宝境']
        select_server_niao = ['陆行鸟', '红玉海', '神意之地', '拉诺西亚', '幻影群岛', '萌芽池', '宇宙和音', '沃仙曦染', '晨曦王座']
        select_server_gou = ['豆豆柴', '水晶塔', '银泪湖', '太阳海岸', '伊修加德', '红茶川']
        if self.server in select_server_niao:
            server = '陆行鸟'
        elif self.server in select_server_zhu:
            server = '莫古力'
        elif self.server in select_server_gou:
            server = '豆豆柴'
        else:
            server = '猫小胖'
        if type(item) is not list:
            if item['id'] not in self.price_cache:
                query_url = '/api/%s/%s?listings=1&noGst=true' % (server, item['id'])
                result = self.init_query_result(query_url, 'universalis')
                x = abs(result['averagePrice'] - result['listings'][0]['pricePerUnit'])
                if int(item['id']) < 20:
                    # 碎晶，水晶，晶簇
                    item['pricePerUnit'] = result['listings'][0]['pricePerUnit']
                elif x > 300:
                    item['pricePerUnit'] = int(result['averagePrice'])
                else:
                    item['pricePerUnit'] = result['listings'][0]['pricePerUnit']
                self.price_cache[int(item['id'])] = copy.deepcopy(item['pricePerUnit'])
            else:
                item['pricePerUnit'] = self.price_cache[item['id']]
        elif type(item) is list:
            ids = []
            for i in item:
                if i['id'] not in self.price_cache:
                    ids.append(str(i['id']))
                else:
                    i['pricePerUnit'] = self.price_cache[i['id']]
            idss = ','.join(ids)
            if len(ids) > 1:
                query_url = '/api/%s/%s?listings=1&noGst=true' % (server, idss)
                result = self.init_query_result(query_url, 'universalis')['items']
            elif len(ids) == 1:
                query_url = '/api/%s/%s?listings=1&noGst=true' % (server, idss)
                result = [self.init_query_result(query_url, 'universalis')]
            for i in item:
                if i['id'] not in self.price_cache:
                    for r in result:
                        if str(r['itemID']) == str(i['id']):
                            x = abs(r['averagePrice'] - r['listings'][0]['pricePerUnit'])
                            if int(i['id']) < 20:
                                # 碎晶，水晶，晶簇
                                i['pricePerUnit'] = r['listings'][0]['pricePerUnit']
                            elif x > 300:
                                i['pricePerUnit'] = int(r['averagePrice'])
                            else:
                                i['pricePerUnit'] = r['listings'][0]['pricePerUnit']
                            self.price_cache[int(i['id'])] = copy.deepcopy(i['pricePerUnit'])

    def query_item_cost(self, stuff_list, count=1, tab=0):
        """
        查询物品的制作成本的计算器
        """

        def c_tab(c_str='', tab=0):
            i = 0
            f_str = c_str
            m_str = '\t\t\t\t'
            while i < 5:
                if i == tab:
                    break
                else:
                    f_str = f_str + '\t'
                    # m_str = m_str[:-1]
                    m_str = m_str + '\t'
                    i += 1
            return f_str, m_str

        d_cost = 0
        for stuff in stuff_list:
            # n_count 每次生产产出材料为1个时 直接用所需数量 * 产出
            n_count = (stuff['amount'] * count)
            if 'priceFromNpc' in stuff:
                price = min(stuff['priceFromNpc'], stuff['pricePerUnit']) * n_count
            else:
                price = stuff['pricePerUnit'] * n_count
            stuff['amount'] = n_count
            stuff['pricePerUnit'] = price
            d_cost += price

            f_str, m_str = c_tab(tab=tab)
            self.clipboard = self.clipboard + '%s%s%s%d\t%d' % (f_str, stuff['name'], m_str, n_count, price) + '\n'
            # 如果这个东西可以被制作
            if 'craft' in stuff and 'yield' in stuff:
                # c_count 每次生产产出材料为多个时 'yield' 为单次生产产出数量
                c_count = 0
                if n_count > stuff['yield']:
                    # ceil  向上取整
                    c_count = ceil(n_count / stuff['yield'])
                elif n_count <= stuff['yield']:
                    c_count = 1
                self.query_item_cost(stuff['craft'], c_count, tab=tab + 1)
                # self.o_cost += self.query_item_cost(stuff['craft'], c_count, tab=tab + 1)
            elif 'craft' in stuff and 'yield' not in stuff:
                self.query_item_cost(stuff['craft'], n_count, tab=tab + 1)
                # self.o_cost += self.query_item_cost(stuff['craft'], n_count, tab=tab + 1)
            elif 'craft' not in stuff:
                self.o_cost += price
        return d_cost

    def show_item_cost(self):
        """
        显示物品的制作成本的外壳
        """
        self.clipboard = '直接材料\t二级材料\t三级材料\t四级材料\t直接材料数量\t直接材料价值\t二级材料数量\t二级材料价值\t三级材料数量\t三级材料价值\t四级材料数量\t四级材料价值\n'
        start = time.time()
        # del self.stuff
        self.stuff = {}
        self.d_cost = 0
        self.o_cost = 0
        self.query_item_craft()
        if len(self.stuff) > 0:
            self.d_cost = self.query_item_cost(self.stuff['craft'])
            end = time.time()
            print('材料树计算用时', end - start)
            self.clipboard = '%s\t\t直接材料成本\t%d\t\t原始材料成本\t%d\t\t更新时间\t%s\n\n' % (
                self.name, self.d_cost, self.o_cost, self.timestamp_to_time(time.time())) + self.clipboard
            return self.d_cost, self.o_cost
        else:
            return None, None

    def get_online_version(self):
        """
        通过github拉取程序版本
        """
        try:
            url = 'https://raw.githubusercontent.com/NagaResst/Paissa/master/Data/version'
            result = get(url, timeout=5, headers=self.header)
        except:
            url = 'http://43.142.142.18/version'
            result = get(url, timeout=3, headers=self.header)
        return loads(result.text)


if __name__ == '__main__':
    # 初始化测试数据
    # item = '群星壁挂'
    server = '猫小胖'
    itemObj = Queryer(server)
    with open('Data/item.Pdt', 'r', encoding='utf8') as item_list_file:
        itemObj.item_data = load(item_list_file)
    # 物品选择器列表
    # itemObj.query_item_id(item)
    # print(itemObj.item_list)
    # 价格查询
    # itemObj.id = '35814'
    itemObj.id = '22893'
    itemObj.hq = True
    # https://universalis.app/api/v2/猫小胖/33283?listings=50&hq=true&noGst=true
    # http://43.142.142.18/universalis/api/v2/猫小胖/33283?listings=50&hq=true&noGst=true

    # price_list = itemObj.query_item_price()
    # print(price_list)
    # server_list = itemObj.server_list()
    # itemObj.query_every_server(server_list)
    # print(itemObj.every_server)
    # itemObj.query_item_craft()
    # print(itemObj.stuff)
    # itemObj.query_item_craft()
    itemObj.show_item_cost()
    print(itemObj.stuff)
    # with open('Data/item.Pdt', 'r', encoding='utf8') as item_list:
    #     item_str = item_list.read()
    #     item_data = eval(item_str)
    #     print(type(item_data))
    #     print(len(item_data))
    # version = itemObj.get_online_version()
    # print(version)
