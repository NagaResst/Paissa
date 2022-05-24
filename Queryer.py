import threading
import time
from json import loads
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

    @staticmethod
    def init_query_result(url):
        """
        查询结果序列化成字典
        """
        while True:
            try:
                result = get(url, timeout=5)
                # 当属性的值为null的时候，无法转换成字典，将其替换为None
                # result = result.text.replace('null', '"None"')
                result = loads(result.text)
                break
            except:
                pass
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

    def get_icon(self, url):
        while True:
            try:
                result = get(url)
                break
            except:
                print('图标获取失败')
        self.icon = result.content

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
            server_list = ['紫水栈桥', '延夏', '静语庄园', '摩杜纳', '海猫茶屋', '柔风海湾', '琥珀原']
        elif self.server in select_server_niao:
            server_list = ['红玉海', '神意之地', '拉诺西亚', '幻影群岛', '萌芽池', '宇宙和音', '沃仙曦染', '晨曦王座']
        elif self.server in select_server_zhu:
            server_list = ['白银乡', '白金幻象', '神拳痕', '潮风亭', '旅人栈桥', '拂晓之间', '龙巢神殿', '梦羽宝境']
        elif self.server in select_server_gou:
            server_list = ['水晶塔', '银泪湖', '太阳海岸', '伊修加德', '红茶川']
        return server_list

    def query_item_id(self, name):
        """
        查询官方的物品ID，为后面的查询提供支持
        """
        query_url = 'https://cafemaker.wakingsands.com/search?indexes=item&string=' + name
        result = self.init_query_result(query_url)
        all_list = result["Results"]
        item_list = []
        # 过滤掉不可在市场上交易的物品
        for item in all_list:
            if item['ID'] in marketable:
                item_list.append(item)
        self.item_list = sorted(item_list, key=lambda e: e.__getitem__('ID'), reverse=False)

    def query_item_price(self):
        """
        查询市场价格，根据传入的HQ参数选择查询方法
        """
        if self.hq is True:
            query_url = 'https://universalis.app/api/v2/%s/%s?listings=50&hq=true&noGst=true' % (
                self.server, self.id)
        # elif hq is False:
        #     query_url = 'https://universalis.app/api/v2/%s/%s?listings=50&hq=false&noGst=true' % (
        #         self.server, self.id)
        else:
            query_url = 'https://universalis.app/api/%s/%s?listings=50&noGst=true' % (self.server, self.id)
        result = self.init_query_result(query_url)
        if self.hq is True and len(result['listings']) == 0:
            self.hq = False
            query_url = 'https://universalis.app/api/%s/%s?listings=50&noGst=true' % (self.server, self.id)
            result = self.init_query_result(query_url)
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
            query_url = 'https://universalis.app/api/%s/%s?listings=1&noGst=true' % (server, item_id)
            result = self.init_query_result(query_url)
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
            # query_single_server(server, self.id)
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
            self.stuff = self.query_item_detial(self.id)
            if 'craft' in self.stuff:
                if 'yield' in self.stuff['craft'][0]:
                    self.yields = self.stuff['craft'][0]['yield']
                self.stuff = self.stuff['craft'][0]['ingredients']
                self.make_item_craft(self.stuff)
            else:
                self.stuff = {}

    def make_child_item_craft(self, unit):
        result = self.query_item_detial(unit['id'])
        unit['name'] = result['name']
        query_result = self.query_item_cost_min(unit['id'])
        x = abs(query_result['averagePrice'] - query_result['listings'][0]['pricePerUnit'])
        if x < 300:
            unit['pricePerUnit'] = query_result['listings'][0]['pricePerUnit']
        else:
            unit['pricePerUnit'] = int(query_result['averagePrice'])
        if 'vendors' in result:
            unit['priceFromNpc'] = result['price']
        if 'craft' in result:
            unit['craft'] = result['craft'][0]['ingredients']
            if 'yield' in result['craft'][0]:
                unit['yield'] = result['craft'][0]['yield']
            self.make_item_craft(unit['craft'])

    def make_item_craft(self, stuff_list):
        """
        统计物品的制作材料
        """
        threads = []
        for unit in stuff_list:
            thread_make_child_craft = threading.Thread(target=self.make_child_item_craft, args=[unit])
            thread_make_child_craft.start()
            threads.append(thread_make_child_craft)
        for i in threads:
            i.join()

    def query_item_detial(self, itemid):
        """
        查询物品的详细信息，查询制作配方和统计成本的前置方法
        """
        query_url = 'https://garlandtools.cn/api/get.php?type=item&lang=chs&version=3&id=' + str(itemid)
        result = self.init_query_result(query_url)
        return result['item']

    def query_item_cost_min(self, itemid):
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
        query_url = 'https://universalis.app/api/%s/%s?listings=1&noGst=true' % (server, itemid)
        result = self.init_query_result(query_url)
        return result

    def query_item_cost(self, stuff_list, count=1, tab=''):
        """
        查询物品的制作成本的计算器
        """
        d_cost = 0
        self.query_item_craft()
        for stuff in stuff_list:
            # n_count 每次生产产出材料为1个时 直接用所需数量 * 产出
            n_count = (stuff['amount'] * count)
            if 'priceFromNpc' in stuff:
                price = min(stuff['priceFromNpc'], stuff['pricePerUnit']) * n_count
            else:
                price = stuff['pricePerUnit'] * n_count
            stuff['amount'] = n_count
            stuff['pricePerUnit'] = price
            d_cost = d_cost + price
            if 'yield' in stuff and 'craft' in stuff:
                # c_count 每次生产产出材料为多个时 'yield' 为单次生产产出数量
                c_count = 0
                if n_count > stuff['yield']:
                    c_count = ceil(n_count / stuff['yield'])
                elif n_count <= stuff['yield']:
                    c_count = 1
                self.o_cost = self.o_cost + self.query_item_cost(stuff['craft'], c_count, tab=tab + '\t')
            elif 'craft' in stuff and 'yield' not in stuff:
                self.o_cost = self.o_cost + self.query_item_cost(stuff['craft'], n_count, tab=tab + '\t')
            else:
                self.o_cost = self.o_cost + price
        return d_cost

    def show_item_cost(self):
        """
        显示物品的制作成本的外壳
        """
        self.stuff = {}
        self.query_item_craft()
        if len(self.stuff) > 0:
            self.d_cost = 0
            self.o_cost = 0
            self.d_cost = self.query_item_cost(self.stuff)
            return self.d_cost, self.o_cost
        else:
            return None, None


if __name__ == '__main__':
    # 初始化测试数据
    # item = '群星壁挂'
    server = '猫小胖'
    itemObj = Queryer(server)
    # 物品选择器列表
    # itemObj.query_item_id(item)
    # print(itemObj.item_list)
    # 价格查询
    itemObj.id = '22885'
    itemObj.hq = True
    # price_list = itemObj.query_item_price()
    # print(price_list)
    # server_list = itemObj.server_list()
    # itemObj.query_every_server(server_list)
    # print(itemObj.every_server)
    # itemObj.query_item_craft()
    # print(itemObj.stuff)
    itemObj.show_item_cost()
