import copy
import logging
import re
import threading
import time
# from concurrent.futures import ThreadPoolExecutor
from json import loads, load
from math import ceil

from requests import get

from Data.marketable import marketable

logging.basicConfig(level=logging.DEBUG)


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
        # 物品的制作配方
        self.stuff = {}
        # 物品在市场上的平均售价
        self.avgp = 0
        # 查询物品的单次制作产出数量
        self.yields = 1
        # NQ和HQ销售指数
        self.nqs = 0
        self.hqs = 0
        # 物品的直接材料制作成本
        self.d_cost = 0
        # 物品的原始材料成本
        self.o_cost = 0
        # 当前查询的服务器
        self.server = query_server
        self.every_server = []
        # 物品图标
        self.icon = None
        # 通过查询获得到的物品数据
        self.item_data = {}
        # 静态资源加速
        self.static = True
        # 反向代理
        self.proxy = False
        # 是否过滤掉不可在市场上查询的物品
        self.filter_item = True
        # 成本查询复制到剪贴板的容器变量
        self.clipboard = ''
        self.header = {'User-Agent': 'Paissa 0.8.5'}
        self.price_cache = {}
        logging.info("查询物品槽位初始化")

    def init_query_result(self, url, site=None):
        """
        查询结果序列化成字典
        :param url:要调用的接口path
        :param site:是否启用反代加速决定调用API访问网站
        :return dist：universalis返回的查询结果
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
                    logging.debug("{} success".format(url))
                    break
                else:
                    logging.warning(url + result.status_code)
            except:
                logging.error('{} timeout'.format(url))
        return result

    @staticmethod
    def timestamp_to_time(timestamp):
        """
        时间戳转换方法
        :param timestamp: 时间戳
        :return str:有格式的时间
        """
        if timestamp > 9999999999:
            timestamp = float(timestamp / 1000)
        timearray = time.localtime(timestamp)
        result = time.strftime("%Y-%m-%d %H:%M:%S", timearray)
        return result

    def get_icon(self, icon_url=None):
        """
        获取图标的方法，数据源不一致，获取图标的地址也不同
        通过 item_list 的项目来获取物品ID可以保证在任何情况下都可以取到值
        :return self.icon
        """
        self.icon = None
        if len(self.item_list) == 0:
            self.query_item_id(self.name)
        # 静态加速的数据来源于garlandtools,在线查询的数据来源于cafemaker,所以取图标的API不同
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
            logging.info('图标获取成功')
        except:
            logging.info('图标获取失败')

    def server_list(self):
        """
        根据当前查询的大区或者服务器，为查询所有区服最低价提供支持
        https://ff.web.sdo.com/web8/index.html#/servers
        跨大区开放后 server_list 将返回所有区服的列表
        :return server_list -> list:包含多个服务器的str的列表，去掉了大区名称
        """
        select_server_mao = ['猫小胖', '紫水栈桥', '延夏', '静语庄园', '摩杜纳', '海猫茶屋', '柔风海湾', '琥珀原']
        select_server_zhu = ['莫古力', '白银乡', '白金幻象', '神拳痕', '潮风亭', '旅人栈桥', '拂晓之间', '龙巢神殿',
                             '梦羽宝境']
        select_server_niao = ['陆行鸟', '红玉海', '神意之地', '拉诺西亚', '幻影群岛', '萌芽池', '宇宙和音', '沃仙曦染',
                              '晨曦王座']
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
        logging.info('服务器列表初始化为{}'.format(server_list))
        return server_list

    def query_item_id(self, name):
        """
        查询官方的物品ID，为后面的查询提供支持
        :param name:玩家输入的道具名称 可以仅为道具名的关键字
        :return self.item_list -> list
        """
        logging.debug("物品查找阶段")
        self.item_list = []
        logging.debug('静态资源加速 {}'.format(self.static))
        if self.static is False:
            # cafemaker可以正确的模糊查询
            query_url = 'https://cafemaker.wakingsands.com/search?indexes=item&string=' + name
            result = self.init_query_result(query_url)
            # 返回的数据是个json,将其中的结果列表取出
            all_list = result["Results"]
            logging.debug('物品列表已从远端取回')
            logging.debug('物品过滤 {}'.format(self.filter_item))
            for item in all_list:
                # 过滤掉不可在市场上交易的物品
                if self.filter_item is True and item['ID'] in marketable:
                    this_item = {'id': item['ID'], 'name': item['Name'], 'icon': item['Icon']}
                    self.item_list.append(this_item)
                elif self.filter_item is False:
                    this_item = {'id': item['ID'], 'name': item['Name'], 'icon': item['Icon']}
                    self.item_list.append(this_item)
            self.item_list = sorted(self.item_list, key=lambda e: e.__getitem__('id'), reverse=False)
        # 使用本地资源查询
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
        :return dist：universalis返回的查询结果
        """
        # 初始化数据 清除上次查询的结果对以后查询的影响
        logging.debug('价格查询阶段')
        self.stuff = {}
        self.yields = 1
        if self.hq is True:
            logging.debug('锁定查询HQ')
            query_url = '/api/v2/%s/%s?listings=50&hq=true&noGst=true' % (
                self.server, self.id)
        else:
            logging.info("全品质查询")
            query_url = '/api/%s/%s?listings=50&noGst=true' % (self.server, self.id)
        result = self.init_query_result(query_url, 'universalis')
        # 如果查询不到物品，强制重查一次NQ
        if self.hq is True and len(result['listings']) == 0:
            logging.info("查询不到物品，强制重查一次NQ")
            self.hq = False
            query_url = '/api/%s/%s?listings=50&noGst=true' % (self.server, self.id)
            result = self.init_query_result(query_url, 'universalis')
        # 将查询结果的销量指数和平均售价取出
        if result['nqSaleVelocity'] == 0 and result['hqSaleVelocity'] > 0:
            self.avgp = int(result['minPriceHQ'])
            logging.debug('平均价格取出 minPriceHQ')
        elif result['hqSaleVelocity'] == 0 and result['nqSaleVelocity'] > 0:
            self.avgp = int(result['minPriceNQ'])
            logging.debug('平均价格取出 minPriceNQ')
        elif result['nqSaleVelocity'] > 0 and result['hqSaleVelocity'] / result['nqSaleVelocity'] > 3:
            self.avgp = int(result['minPriceHQ'])
            logging.debug('平均价格取出 minPriceHQ')
        else:
            self.avgp = int(result['minPriceNQ'])
            logging.debug('平均价格取出 minPriceNQ')
        self.nqs = result['nqSaleVelocity']
        self.hqs = result['hqSaleVelocity']
        return result

    def query_every_server(self, server_list):
        """
        大区内服务器比价，
        :param server_list: list 服务器列表
        :return self.every_server -> list 根据服务器列表查询每个区的最低价
        """
        # 清空全服差价的结果列表
        self.every_server = []

        # 单个服务器查询最低价格的方法
        def query_single_server(server, item_id):
            query_url = '/api/%s/%s?listings=1&noGst=true' % (server, item_id)
            result = self.init_query_result(query_url, 'universalis')
            # 重新组织比价用的数据，并加入全服查价的结果列表，如果不重新组织数据，某些区服查询出空集时，会报错
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
                logging.info("{}的数据已加入池中".format(server))

        # 多线程操作
        threads = []
        for server in server_list:
            thread = threading.Thread(target=query_single_server, args=(server, self.id))
            thread.start()
            threads.append(thread)
        for t in threads:
            t.join()
        logging.info("全部服务器查询完成，池中数据样本数 {}".format(len(self.every_server)))

    def query_item_craft(self):
        """
        查询物品的制作材料
        :return self.stuff -> dist 这个道具的制作配方
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
                    logging.info("物品制作配方已查询成功")
                else:
                    self.stuff = {}
                    logging.info("物品制作配方已查询失败，清空配方池")
            elif self.static is True:
                self.stuff = copy.deepcopy(self.item_data[str(self.id)])
                if 'craft' in self.stuff:
                    if 'yield' in self.stuff:
                        self.yields = self.stuff['yield']
                    self.make_item_craft(self.stuff['craft'])
                    logging.info("物品制作配方已查询成功")
                else:
                    self.stuff = {}
                    logging.info("物品制作配方已查询失败，清空配方池")

    def make_child_item_craft(self, unit):
        """
        材料树递归查询的线程函数 这个方法会直接把价格更新到实例的stuff属性里
        :param unit -> dist 道具的数据
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
        """
        新的材料树递归查询的线程函数 这个方法会在一次接口请求中查询多个物品
        :param unit -> dist 道具的数据
        """
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
        :param stuff_list -> list 包含多个unit的列表
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
        :param itemid 需要初始化成字符串使用
        :return result -> dist 物品的数据
        """
        logging.debug("材料递归查询，物品ID{} ".format(itemid))
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
        查询单项物品的板子价格，调用缓存或者是在线查询物品的最低价
        :param item -> dist 物品的数据
        """
        # 确定查询的服务器所在大区
        select_server_zhu = ['莫古力', '白银乡', '白金幻象', '神拳痕', '潮风亭', '旅人栈桥', '拂晓之间', '龙巢神殿',
                             '梦羽宝境']
        select_server_niao = ['陆行鸟', '红玉海', '神意之地', '拉诺西亚', '幻影群岛', '萌芽池', '宇宙和音', '沃仙曦染',
                              '晨曦王座']
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
            # 缓存中没有数据，进行在线查询
            logging.debug("{}缓存中没有数据，进行在线查询".format(item['name']))
            if item['id'] not in self.price_cache:
                query_url = '/api/%s/%s?listings=5&noGst=true' % (server, item['id'])
                result = self.init_query_result(query_url, 'universalis')
                if len(result['listings']) == 0:
                    result['listings'].append({'pricePerUnit': 0})
                # x参数  抗人为干扰
                x = abs(result['averagePrice'] - result['listings'][0]['pricePerUnit'])
                logging.debug("{}在市场上平均价格和最低价格的差价为{}".format(item['name'], x))
                if int(item['id']) < 20:
                    # 碎晶，水晶，晶簇
                    item['pricePerUnit'] = result['listings'][0]['pricePerUnit']
                    logging.debug("{}物品ID小于20 推测为水晶类，无视差价，使用最低价格".format(item['name']))
                elif x > 300 and result['listings'][0]['pricePerUnit'] < 666:
                    item['pricePerUnit'] = int(result['averagePrice'])
                    logging.debug("{}价差较高，但是物品价格便宜，推测为材料类，使用平均价格".format(item['name']))
                elif x > 300 and result['listings'][0]['pricePerUnit'] > 666:
                    item['pricePerUnit'] = result['listings'][4]['pricePerUnit']
                    logging.debug("{}价差较高，但是物品比较贵，排除前三，使用第4位的价格进行参考".format(item['name']))
                else:
                    item['pricePerUnit'] = result['listings'][0]['pricePerUnit']
                    logging.debug("{}差价较低，使用最低价格".format(item['name']))
                # 更新缓存
                logging.info("更新缓存 {}".format(item['name']))
                self.price_cache[int(item['id'])] = copy.deepcopy(item['pricePerUnit'])
            # 缓存命中，直接读取数据。
            # 缓存没有超时时间，但是不会有人开一整天猴面雀吧
            else:
                item['pricePerUnit'] = self.price_cache[item['id']]
        # 一次查询多个物品 ，在计算成本的时候会用到
        elif type(item) is list:
            ids = []
            # 先提取出没有缓存的物品ID,有缓存直接用缓存
            for i in item:
                logging.debug("{} 缓存命中，使用缓存".format(i['name']))
                if i['id'] not in self.price_cache:
                    ids.append(str(i['id']))
                else:
                    i['pricePerUnit'] = self.price_cache[i['id']]
            # 把list转换成字符串，准备在线查询
            idss = ','.join(ids)
            if len(ids) > 1:
                query_url = '/api/%s/%s?listings=5&noGst=true' % (server, idss)
                result = self.init_query_result(query_url, 'universalis')['items']
            elif len(ids) == 1:
                query_url = '/api/%s/%s?listings=5&noGst=true' % (server, idss)
                result = [self.init_query_result(query_url, 'universalis')]
            for i in item:
                # 把在线查询到的结果更新到缓存中
                if i['id'] not in self.price_cache:
                    for r in result:
                        if str(r['itemID']) == str(i['id']):
                            if len(r['listings']) == 0:
                                r['listings'].append({'pricePerUnit': 0})
                            x = abs(r['averagePrice'] - r['listings'][0]['pricePerUnit'])
                            logging.debug("{}平均价格和最低价格的差价为{}".format(i['name'], x))
                            if int(i['id']) < 20:
                                # 碎晶，水晶，晶簇
                                logging.debug("{}物品ID小于20 推测为水晶类，无视差价，使用最低价格".format(i['name']))
                                i['pricePerUnit'] = r['listings'][0]['pricePerUnit']
                            elif x > 300 and r['listings'][0]['pricePerUnit'] < 666:
                                logging.debug("{}价差较高，但是物品价格便宜，推测为材料类，使用平均价格".format(i['name']))
                                i['pricePerUnit'] = int(r['averagePrice'])
                            elif x > 300 and r['listings'][0]['pricePerUnit'] > 666:
                                logging.debug(
                                    "{}价差较高，但是物品比较贵，排除前三，使用第4位的价格进行参考".format(i['name']))
                                i['pricePerUnit'] = r['listings'][4]['pricePerUnit']
                            else:
                                logging.debug("{}差价较低，使用最低价格".format(i['name']))
                                i['pricePerUnit'] = r['listings'][0]['pricePerUnit']
                            logging.info("查询材料{}成功，更新缓存".format(i['name']))
                            self.price_cache[int(i['id'])] = copy.deepcopy(i['pricePerUnit'])

    def query_item_cost(self, stuff_list, count=1, tab=0):
        """
        查询物品的制作成本的计算器
        :param stuff_list -> list 材料列表，包含多个unit
        :param count -> int 制作次数
        :param tab -> str 文本输出格式控制
        """

        def c_tab(c_str='', tab=0):
            # 格式控制
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
                logging.debug("{}NPC出售，使用比价，采用最低价".format(stuff['name']))
                price = min(stuff['priceFromNpc'], stuff['pricePerUnit']) * n_count
            else:
                price = stuff['pricePerUnit'] * n_count
            stuff['amount'] = n_count
            stuff['pricePerUnit'] = price
            d_cost += price
            # 准备复制到剪贴板
            f_str, m_str = c_tab(tab=tab)
            self.clipboard = self.clipboard + '%s%s%s%d\t%d' % (f_str, stuff['name'], m_str, n_count, price) + '\n'
            # 如果这个东西可以被制作
            if 'craft' in stuff and 'yield' in stuff:
                logging.debug("{}每次可以生产的个数为{}".format(stuff['name'], stuff['yield']))
                # c_count 每次生产产出材料为多个时 'yield' 为单次生产产出数量
                c_count = 0
                if n_count > stuff['yield']:
                    # ceil  向上取整
                    c_count = ceil(n_count / stuff['yield'])
                    logging.debug("{}需要多次生产，生产次数 {}".format(stuff['name'], c_count))
                elif n_count <= stuff['yield']:
                    c_count = 1
                    logging.debug("只生产一次")
                self.query_item_cost(stuff['craft'], c_count, tab=tab + 1)
                # self.o_cost += self.query_item_cost(stuff['craft'], c_count, tab=tab + 1)
            elif 'craft' in stuff and 'yield' not in stuff:
                logging.debug("{}每次只生产一个".format(stuff['name']))
                self.query_item_cost(stuff['craft'], n_count, tab=tab + 1)
                # self.o_cost += self.query_item_cost(stuff['craft'], n_count, tab=tab + 1)
            elif 'craft' not in stuff:
                self.o_cost += price
                logging.debug("{} 这玩意不能制作".format(stuff["name"]))
        return d_cost

    def show_item_cost(self):
        """
        显示物品的制作成本的外壳
        :return self.d_cost -> int 物品的直接材料制作成本
        :return self.o_cost -> int 物品的原始材料成本
        """
        logging.info("开始查询物品的制作材料价格")
        self.clipboard = '直接材料\t二级材料\t三级材料\t四级材料\t直接材料数量\t直接材料价值\t二级材料数量\t二级材料价值\t三级材料数量\t三级材料价值\t四级材料数量\t四级材料价值\n'
        start = time.time()
        # del self.stuff
        logging.info("材料树重置")
        self.stuff = {}
        self.d_cost = 0
        self.o_cost = 0
        # 查询配方
        self.query_item_craft()
        # 确认到有配方
        if len(self.stuff) > 0:
            self.d_cost = self.query_item_cost(self.stuff['craft'])
            # debug 计算查询用时
            end = time.time()
            logging.info('材料树计算用时 {}'.format(end - start))
            self.clipboard = '%s\t\t直接材料成本\t%d\t\t原始材料成本\t%d\t\t更新时间\t%s\n\n' % (
                self.name, self.d_cost, self.o_cost, self.timestamp_to_time(time.time())) + self.clipboard
            return self.d_cost, self.o_cost
        else:
            self.stuff['craft'] = [{'name': '该物品不能被制作', 'amount': '', 'pricePerUnit': ''}]
            return None, None

    def get_online_version(self):
        """
        通过github拉取程序版本
        """
        try:
            url = 'https://raw.githubusercontent.com/NagaResst/Paissa/master/Data/version'
            result = get(url, timeout=5, headers=self.header)
            logging.debug("{} success".format(url))
        except:
            url = 'http://43.142.142.18/version'
            result = get(url, timeout=3, headers=self.header)
            logging.debug("{} success".format(url))
        return loads(result.text)

    def test_network(self):
        """网络测试方法"""
        if self.proxy is False:
            url = "https://universalis.app/api/maoxiaopang/5069?listings=1"
        else:
            url = 'http://43.142.142.18/universalis/api/maoxiaopang/5069?listings=1'
        c = 0
        while c < 3:
            try:
                result = get(url, timeout=5, headers=self.header)
                if result.status_code == 200:
                    return "success"
                else:
                    logging.warning(url + str(result.status_code))
                    c += 1
            except:
                logging.error('{} timeout'.format(url))
                c += 1
        if c >= 3:
            return "failed"


if __name__ == '__main__':
    # 初始化测试数据
    # item = '群星壁挂'
    server = '猫小胖'
    itemObj = Queryer(server)
    with open('Data/item.Pdt', 'r', encoding='utf8') as item_list_file:
        itemObj.item_data = load(item_list_file)
    # 物品选择器列表
    # itemObj.query_item_id(item)
    # logging.(itemObj.item_list)
    # 价格查询
    # itemObj.id = '35814'
    itemObj.id = '22893'
    itemObj.hq = True
    # https://universalis.app/api/v2/猫小胖/33283?listings=50&hq=true&noGst=true
    # http://43.142.142.18/universalis/api/v2/猫小胖/33283?listings=50&hq=true&noGst=true

    # price_list = itemObj.query_item_price()
    # logging.(price_list)
    # server_list = itemObj.server_list()
    # itemObj.query_every_server(server_list)
    # logging.(itemObj.every_server)
    # itemObj.query_item_craft()
    # logging.(itemObj.stuff)
    # itemObj.query_item_craft()
    itemObj.show_item_cost()
    print(itemObj.stuff)
    # with open('Data/item.Pdt', 'r', encoding='utf8') as item_list:
    #     item_str = item_list.read()
    #     item_data = eval(item_str)
    #     logging.(type(item_data))
    #     logging.(len(item_data))
    # version = itemObj.get_online_version()
    # logging.(version)
