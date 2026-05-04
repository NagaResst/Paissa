import copy
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from json import load
from math import ceil

from config import Config
from network.client import http_client
from Data.marketable import marketable
from Data.logger import logger
from cache.manager import cache_manager


class Queryer(object):
    def __init__(self, query_server='猫小胖', item_id=None):
        """
        对象初始化
        """
        self.name = None
        self.hq = False
        # item_list 代表本次模糊查询的结果集
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
        self.world = 'maoxiaopang'
        self.every_server = []
        # 物品图标
        self.icon = None
        # 通过查询获得到的物品数据
        self.item_data = {}
        # 静态资源加速
        self.static = True
        # 是否过滤掉不可在市场上查询的物品
        self.filter_item = True
        # 成本查询复制到剪贴板的容器变量
        self.clipboard = ''
        # 网络查询失败标志
        self.query_network_failed = False
        self.craft_query_failed = False
        # 当前正在查询的物品名称
        self.cq = None
        self.server_config = None
        self.load_server_config()
        logger.info("查询物品槽位初始化")

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
        :return self.icon:request.get().content
        """
        self.icon = None
        if len(self.item_list) == 0:
            self.query_item_id(self.name)
        logger.debug('查询到的物品数量：{}'.format(len(self.item_list)))
        # 静态加速的数据来源于garlandtools,在线查询的数据来源于cafemaker,所以取图标的API不同
        if len(self.item_list) > 1 and self.static is False:
            for i in self.item_list:
                if str(i['id']) == str(self.id):
                    icon_url = Config.CAFEMAKER_BASE_URL + i['icon']
        elif len(self.item_list) > 1 and self.static is True:
            icon_url = Config.GARLANDTOOLS_BASE_URL + "/files/icons/item/t/" + self.item_data[str(self.id)]['icon'] + '.png'
        elif len(self.item_list) == 1 and self.static is False:
            icon_url = Config.CAFEMAKER_BASE_URL + self.item_list[0]['icon']
        elif len(self.item_list) == 1 and self.static is True:
            icon_url = Config.GARLANDTOOLS_BASE_URL + "/files/icons/item/t/" + self.item_data[str(self.id)]['icon'] + '.png'
        # item_list 为空时，通过garlandtools API获取图标ID再构造URL
        elif len(self.item_list) == 0 and self.id:
            result = http_client.get_json(
                Config.GARLANDTOOLS_BASE_URL + '/api/get.php?type=item&lang=chs&version=3&id=' + str(self.id))
            if result and 'item' in result and 'icon' in result['item']:
                icon_url = Config.GARLANDTOOLS_BASE_URL + "/files/icons/item/t/" + str(result['item']['icon']) + '.png'
        if icon_url is None:
            logger.debug('无法构造图标URL，跳过图标获取')
            return
        content = http_client.get_content(icon_url)
        if content:
            self.icon = content
            logger.debug('图标获取成功')
        else:
            self.icon = None
            logger.debug('图标获取失败')

    def load_server_config(self):
        """加载服务器配置"""
        self.server_config = Config.SERVER_CONFIG
    
    def get_server_with_region(self, server_name):
        """
        获取带大区后缀的服务器名称
        :param server_name: 服务器名称
        :return str: 格式为 "服务器（大区）" 或 "服务器"（如果找不到对应大区）
        """
        region_servers = self.server_config['world_regions']
        
        # 国服大区映射
        region_names = {
            'maoxiaopang': '猫小胖',
            'moguli': '莫古力',
            'luxingniao': '陆行鸟',
            'doudouchai': '豆豆柴'
        }
        
        # 查找服务器所属的大区
        for world_key, servers in region_servers.items():
            if server_name in servers:
                region_name = region_names.get(world_key, world_key)
                return f"{server_name}（{region_name}）"
        
        # 如果是国际服或其他情况，直接返回服务器名
        return server_name

    def server_list(self):
        """
        根据当前查询的大区或者服务器，为查询所有区服最低价提供支持
        :return server_list -> list:包含多个服务器的str的列表，去掉了大区名称
        """
        region_servers = self.server_config['world_regions']
        area_to_world = self.server_config['area_mappings']

        # 默认值
        server_list = region_servers['maoxiaopang'][1:]
        self.world = 'maoxiaopang'

        # 查找匹配的区域
        for world_key, servers in region_servers.items():
            if self.server in servers:
                server_list = servers[1:]  # 去掉大区名
                self.world = world_key
                break
        else:
            # 如果 self.server 属于大区名称（如 Japan）
            if self.server in area_to_world:
                server_list = []
                for world_key in area_to_world[self.server]:
                    # 合并所有子区域服务器
                    server_list.extend(region_servers.get(world_key, []))
                self.world = self.server
            else:
                logger.warning(f"未知的服务器名称: {self.server}，使用默认服务器列表")
                return server_list

        return server_list

    def query_item_id(self, name):
        """
        查询官方的物品ID，为后面的查询提供支持
        :param name:玩家输入的道具名称 可以仅为道具名的关键字
        :return self.item_list -> list
        """
        logger.debug("物品查找阶段")
        self.item_list = []
        self.query_network_failed = False
        logger.debug('静态资源加速 {}'.format(self.static))
        if self.static is False:
            # cafemaker可以正确的模糊查询
            query_url = Config.CAFEMAKER_BASE_URL + '/search?indexes=item&string=' + name
            result = http_client.get_json(query_url)
            if result is None:
                logger.error("物品查询请求失败")
                self.query_network_failed = True
                return
            # 返回的数据是个json,将其中的结果列表取出
            all_list = result["Results"]
            logger.debug('物品列表已从远端取回')
            logger.debug('物品过滤 {}'.format(self.filter_item))
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
        根据物品ID查询市场价格，根据HQ参数选择查询方法
        :return dist：universalis返回的查询结果
        """
        # 初始化数据 清除上次查询的结果对以后查询的影响
        logger.debug('价格查询阶段')

        # 初始化数据 清除上次查询的结果对以后查询的影响
        self.stuff = {}
        self.yields = 1

        def safe_get(d, key, default=None):
            return d.get(key, default)

        if self.hq is True:
            logger.debug('锁定查询HQ')
            query_url = f'{Config.UNIVERSALIS_BASE_URL}/api/{self.server}/{self.id}?listings=50&hq=true&noGst=true'
        else:
            logger.info("全品质查询")
            query_url = f'{Config.UNIVERSALIS_BASE_URL}/api/v2/{self.server}/{self.id}?listings=50&noGst=true'

        result = http_client.get_json(query_url)

        # 只有当首次 HQ 查询无结果时尝试切换为全品质查询
        if self.hq and isinstance(result, dict) and not result.get('listings'):
            logger.info("查询不到物品，强制一次全品质查询")
            query_url = f'{Config.UNIVERSALIS_BASE_URL}/api/v2/{self.server}/{self.id}?listings=50&noGst=true'
            self.hq = False
            result = http_client.get_json(query_url)

        if result is None:
            logger.error("价格查询请求失败")
            return None
        # 将查询结果的销量指数和平均售价取出
        nq_velocity = safe_get(result, 'nqSaleVelocity', 0)
        hq_velocity = safe_get(result, 'hqSaleVelocity', 0)
        min_nq = safe_get(result, 'minPriceNQ', 0)
        min_hq = safe_get(result, 'minPriceHQ', 0)
        logger.debug(f"nqSaleVelocity:{safe_get(result, 'nqSaleVelocity', 0)}, hqSaleVelocity:{hq_velocity}")

        try:
            if hq_velocity > 0 and nq_velocity == 0:
                self.avgp = int(min_hq)
                logger.debug('平均价格取出 minPriceHQ')
            elif nq_velocity > 0 and hq_velocity == 0:
                self.avgp = int(min_nq)
                logger.debug('平均价格取出 minPriceNQ')
            elif nq_velocity > 0 and hq_velocity / nq_velocity > 3:
                self.avgp = int(min_hq)
                logger.debug('平均价格取出 minPriceHQ')
            elif hq_velocity == 0 and nq_velocity == 0 and min_nq == 0:
                self.avgp = int(min_hq)
                logger.debug('平均价格取出 minPriceHQ')
            else:
                self.avgp = int(min_nq)
                logger.debug('平均价格取出 minPriceNQ')
        except (TypeError, ValueError):
            logger.warning("无法解析价格字段，使用默认值 0")
            self.avgp = 0

        self.nqs = result.get('nqSaleVelocity', 0)
        self.hqs = result.get('hqSaleVelocity', 0)
        return result

    def query_every_server(self, server_list):
        """
        大区内服务器比价，根据服务器列表查询每个区的最低价
        :param server_list: list 服务器列表
        :return self.every_server -> list
        """
        # 清空全服差价的结果列表
        self.every_server = []

        # 线程安全锁
        result_lock = threading.Lock()

        # 单个服务器查询最低价格的方法
        def query_single_server(server, item_id):
            try:
                result = http_client.get_json(f'{Config.UNIVERSALIS_BASE_URL}/api/v2/{server}/{item_id}?listings=1&noGst=true')

                if result is None or not result or 'listings' not in result or not result['listings']:
                    logger.debug(f"{server} 返回空结果")
                    return
                # 重新组织比价用的数据，并加入全服查价的结果列表，如果不重新组织数据，某些区服查询出空集时，会报错
                server_sale = {
                    'server': server,
                    'pricePerUnit': result['listings'][0]['pricePerUnit'],
                    'hq': result['listings'][0]['hq'],
                    'quantity': result['listings'][0]['quantity'],
                    'total': result['listings'][0]['total'],
                    'retainerName': result['listings'][0]['retainerName'],
                    'lastReviewTime': result['listings'][0]['lastReviewTime']
                }
                with result_lock:
                    self.every_server.append(server_sale)
                    logger.debug(f"{server} 的数据已加入池中")

            except Exception as e:
                logger.exception(f"查询 {server} 时发生异常: {e}")

        # 使用线程池
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(query_single_server, server, self.id) for server in server_list]
            for future in as_completed(futures):
                future.result()  # 触发异常传播

        logger.info("全部服务器查询完成，池中数据样本数 {}".format(len(self.every_server)))

    def query_item_craft(self):
        """
        查询物品的制作材料
        :return self.stuff -> dist 这个道具的制作配方
        """
        self.craft_query_failed = False
        if len(self.stuff) == 0:
            # 先查配方缓存
            cached_craft = cache_manager.get_craft(str(self.id))
            if cached_craft is not None:
                self.stuff = cached_craft
                if 'craft' in self.stuff:
                    if 'yield' in self.stuff:
                        self.yields = self.stuff['yield']
                    self.make_item_craft(self.stuff['craft'])
                    logger.info("物品制作配方从缓存加载成功")
                else:
                    self.stuff = {}
                    logger.warning("物品制作配方缓存中无配方，清空配方池")
                return
            if self.static is False:
                query_url = Config.GARLANDTOOLS_BASE_URL + '/api/get.php?type=item&lang=chs&version=3&id=' + str(self.id)
                result = http_client.get_json(query_url)
                if result is None:
                    self.stuff = {}
                    self.craft_query_failed = True
                    logger.error("制作配方查询请求失败")
                    return
                self.stuff = result['item']
                if 'craft' in self.stuff and len(self.stuff['craft']) > 0:
                    if 'yield' in self.stuff['craft'][0]:
                        self.yields = self.stuff['craft'][0]['yield']
                        self.stuff['yield'] = self.stuff['craft'][0]['yield']
                    self.stuff['craft'] = self.stuff['craft'][0]['ingredients']
                    self.make_item_craft(self.stuff['craft'])
                    logger.info("物品制作配方已查询成功")
                    # 写入配方缓存
                    cache_manager.set_craft(str(self.id), self.stuff)
                else:
                    self.stuff = {}
                    logger.warning("物品制作配方已查询失败，清空配方池")
            elif self.static is True:
                if str(self.id) not in self.item_data:
                    logger.warning(f"静态数据中未找到物品ID: {self.id}")
                    self.stuff = {}
                    return
                self.stuff = copy.deepcopy(self.item_data[str(self.id)])
                if 'craft' in self.stuff:
                    if 'yield' in self.stuff:
                        self.yields = self.stuff['yield']
                    self.make_item_craft(self.stuff['craft'])
                    logger.info("物品制作配方已查询成功")
                    # 写入配方缓存
                    cache_manager.set_craft(str(self.id), self.stuff)
                else:
                    self.stuff = {}
                    logger.warning("物品制作配方已查询失败，清空配方池")

    def make_child_item_craft(self, unit):
        """
        新的材料树递归查询的线程函数 这个方法会在一次接口请求中查询多个物品
        :param unit -> dist 道具的数据
        """
        result = self.query_item_detial(unit['id'])
        unit['name'] = result['name']
        if self.static is False:
            if 'vendors' in result:
                unit['priceFromNpc'] = result['price']
        elif self.static is True:
            if 'priceFromNpc' in result:
                unit['priceFromNpc'] = result['priceFromNpc']
        if 'craft' in result:
            unit['craft'] = result['craft']
            if 'yield' in result:
                unit['yield'] = result['yield']
            self.make_item_craft(unit['craft'])

    def make_item_craft(self, stuff_list):
        """
        统计物品的制作材料
        :param stuff_list -> list 包含多个unit的列表
        """
        threads = []
        for unit in stuff_list:
            thread_make_child_craft = threading.Thread(target=self.make_child_item_craft, args=[unit])
            thread_make_child_craft.start()
            threads.append(thread_make_child_craft)
            # thread_make_child_craft.join()  # debug
        for i in threads:
            i.join()

    def query_item_detial(self, itemid):
        """
        查询物品的详细信息，查询制作配方和统计成本的前置方法
        :param itemid 需要初始化成字符串使用
        :return result -> dist 物品的数据
        """
        logger.debug("材料递归查询，物品ID {} ".format(itemid))
        # 先查配方缓存
        cached = cache_manager.get_craft(str(itemid))
        if cached is not None:
            return cached
        if self.static is False:
            query_url = Config.GARLANDTOOLS_BASE_URL + '/api/get.php?type=item&lang=chs&version=3&id=' + str(itemid)
            result = http_client.get_json(query_url)
            if result is None:
                logger.error(f"物品详情查询请求失败, ID: {itemid}")
                return {'name': '未知', 'id': str(itemid)}
            result = result['item']
            if 'craft' in result and len(result['craft']) > 0:
                if 'yield' in result['craft'][0]:
                    result['yield'] = result['craft'][0]['yield']
                result['craft'] = result['craft'][0]['ingredients']
            cache_manager.set_craft(str(itemid), result)
            return result
        elif self.static is True:
            # 重要： 采用深复制来避免成本树的计算波及到保存在内存中的静态原始数据
            if str(itemid) not in self.item_data:
                logger.warning(f"静态数据中未找到物品ID: {itemid}")
                return {'name': '未知材料', 'id': str(itemid)}
            result = copy.deepcopy(self.item_data[str(itemid)])
            cache_manager.set_craft(str(itemid), result)
            return result

    def query_item_cost_min(self, item):
        """
        查询单项物品的板子价格，调用缓存或者是在线查询物品的最低价
        :param item -> dist 物品的数据
        """

        def select_item_cost(result, item):
            """
            选择最价样品
            :param result -> list 价格网站查询结果
            :param item -> dist 物品的数据
            :return result -> dist 最价样品的数据
            """
            if len(result['listings']) == 0:
                result['listings'].append({'pricePerUnit': 0})
                # x参数  抗人为干扰
            x = abs(result['averagePrice'] - result['listings'][0]['pricePerUnit'])
            logger.debug("{}在市场上平均价格和最低价格的差价为{}".format(item['name'], x))
            if int(item['id']) < 20:
                item['pricePerUnit'] = result['listings'][0]['pricePerUnit']
                item['lowestPriceServer'] = result['listings'][0]['worldName']
                logger.debug("{}物品ID小于20 推测为水晶类，无视差价，使用最低价格，服务器{}".format(item['name'], item['lowestPriceServer']))
            elif 'priceFromNpc' in item and item['priceFromNpc'] < result['averagePrice']:
                logger.debug("NPC贩售价格{}低于板子平均价格{}，使用NPC贩售价格计算"
                             .format(item['priceFromNpc'], result['averagePrice']))
                item['pricePerUnit'] = item['priceFromNpc']
                item['lowestPriceServer'] = "NPC"
            elif x > 300 and result['listings'][0]['pricePerUnit'] < 666:
                item['pricePerUnit'] = int(result['averagePrice'])
                item['lowestPriceServer'] = result['listings'][0]['worldName']
                logger.debug("{}价差较高，但是物品价格便宜，推测为材料类，使用平均价格，服务器{}".format(item['name'], item['lowestPriceServer']))
            elif x > 300 and result['listings'][0]['pricePerUnit'] > 666:
                try:
                    item['pricePerUnit'] = result['listings'][3]['pricePerUnit']
                    item['lowestPriceServer'] = result['listings'][3]['worldName']
                    logger.debug("{}价差较高，但是物品比较贵，排除前三，使用第4位的价格进行参考，服务器{}".format(item['name'],item['lowestPriceServer']))
                except (IndexError, KeyError) as e:
                    logger.debug(f"第4位价格不可用，使用平均价格: {e}")
                    item['pricePerUnit'] = int(result['averagePrice'])
                    item['lowestPriceServer'] = result['listings'][0]['worldName']
                    logger.debug("{}价差较高，但是市场上比较稀缺，使用平均价格{}，服务器{}"
                                 .format(item['name'], result['averagePrice'], item['lowestPriceServer']))
            else:
                item['pricePerUnit'] = result['listings'][0]['pricePerUnit']
                item['lowestPriceServer'] = result['listings'][0]['worldName']
                logger.debug("{}差价较低，使用最低价格，服务器{}".format(item['name'],item['lowestPriceServer']))
            # 更新缓存
            logger.info("更新缓存 {}".format(item['name']))
            cache_manager.set_price(str(item['id']), item['pricePerUnit'], item['lowestPriceServer'])

        if type(item) is not list:
            # 先查缓存
            cached = cache_manager.get_price(str(item['id']))
            if cached is not None:
                item['pricePerUnit'] = cached['pricePerUnit']
                item['lowestPriceServer'] = cached['lowestPriceServer']
                logger.debug("{} 缓存命中，使用缓存".format(item['name']))
            else:
                logger.debug("{}缓存中没有数据，进行在线查询".format(item['name']))
                self.cq = item['name']
                query_url = f'{Config.UNIVERSALIS_BASE_URL}/api/v2/{self.world}/{item["id"]}?listings=5&noGst=true'
                result = http_client.get_json(query_url)
                if result is None:
                    item['pricePerUnit'] = 0
                    item['lowestPriceServer'] = '查询失败'
                    logger.error(f"{item['name']} 价格查询失败")
                    cache_manager.set_price(str(item['id']), 0, '查询失败')
                    return
                select_item_cost(result, item)
        # 一次查询多个物品 ，在计算成本的时候会用到
        elif type(item) is list:
            ids = []
            # 先提取出没有缓存的物品ID,有缓存直接用缓存
            for i in item:
                cached = cache_manager.get_price(str(i['id']))
                if cached is not None:
                    i['pricePerUnit'] = cached['pricePerUnit']
                    i['lowestPriceServer'] = cached['lowestPriceServer']
                    logger.debug("{} 缓存命中，使用缓存".format(i['name']))
                else:
                    ids.append(str(i['id']))
                    logger.debug("{} 没有查询到缓存 ，在线查询".format(i['name']))
                    self.cq = str(i['name'])
            # 把list转换成字符串，准备在线查询
            idss = ','.join(ids)
            if len(ids) > 1:
                query_url = f'{Config.UNIVERSALIS_BASE_URL}/api/{self.world}/{idss}?listings=5&noGst=true'
                result_json = http_client.get_json(query_url)
                if result_json is None:
                    logger.error(f"批量价格查询失败，IDs: {idss}")
                    result = []
                else:
                    result = result_json.get('items', [])
            elif len(ids) == 1:
                query_url = f'{Config.UNIVERSALIS_BASE_URL}/api/{self.world}/{idss}?listings=5&noGst=true'
                result_json = http_client.get_json(query_url)
                if result_json is None:
                    logger.error(f"单个价格查询失败，ID: {idss}")
                    result = []
                else:
                    result = [result_json]
            else:
                result = []
            for i in item:
                # 把在线查询到的结果更新到缓存中
                if cache_manager.get_price(str(i['id'])) is None:
                    matched = False
                    for r in result:
                        if str(r['itemID']) == str(i['id']):
                            select_item_cost(r, i)
                            matched = True
                            break
                    if not matched:
                        i['pricePerUnit'] = 0
                        i['lowestPriceServer'] = '查询失败'
                        cache_manager.set_price(str(i['id']), 0, '查询失败')
                        logger.debug(f"{i['name']} 未匹配到价格数据，缓存失败标记")

    def calibration_quantity(self, stuff_list, count=1):
        """
        材料树原材料数量校准
        :param stuff_list -> list 材料列表，包含多个unit
        :param count -> int 制作次数
        """
        for stuff in stuff_list:
            # n_count 每次生产产出材料为1个时 直接用所需数量 * 产出
            n_count = (stuff['amount'] * count)
            stuff['amount'] = n_count
            if 'craft' in stuff and 'yield' in stuff:
                logger.debug("{}每次可以生产的个数为{}".format(stuff['name'], stuff['yield']))
                # c_count 每次生产产出材料为多个时 'yield' 为单次生产产出数量
                c_count = 0
                if n_count > stuff['yield']:
                    # ceil  向上取整
                    c_count = ceil(n_count / stuff['yield'])
                    logger.debug("{}需要多次生产，生产次数 {}".format(stuff['name'], c_count))
                elif n_count <= stuff['yield']:
                    c_count = 1
                    logger.debug("只生产一次")
                self.calibration_quantity(stuff['craft'], c_count)
            elif 'craft' in stuff and 'yield' not in stuff:
                logger.debug("{}每次只生产一个".format(stuff['name']))
                self.calibration_quantity(stuff['craft'], n_count)
            elif 'craft' not in stuff:
                logger.debug("{} 这玩意不能制作".format(stuff["name"]))

    def query_item_cost(self, stuff_list, tab=0):
        """
        查询物品的制作成本的计算器
        :param stuff_list -> list 材料列表，包含多个unit
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
        self.query_item_cost_min(stuff_list)
        for stuff in stuff_list:
            if 'pricePerUnit' not in stuff:
                self.query_item_cost_min(stuff)
            stuff['priceTotal'] = stuff['pricePerUnit'] * stuff['amount']
            d_cost += stuff['priceTotal']
            f_str, m_str = c_tab(tab=tab)
            self.clipboard = self.clipboard + '%s%s%s%d\t%d' % (
                f_str, stuff['name'], m_str, stuff['amount'], stuff['pricePerUnit']) + '\n'
            if 'craft' in stuff:
                self.query_item_cost(stuff['craft'], tab=tab + 1)
            elif 'pricePerUnit' in stuff:
                self.o_cost += stuff['priceTotal']
        return d_cost

    def show_item_cost(self):
        """
        显示物品的制作成本的外壳
        :return self.d_cost -> int 物品的直接材料制作成本
        :return self.o_cost -> int 物品的原始材料成本
        """
        logger.info("开始查询物品的制作材料价格")
        # 确保 world 设置为当前服务器所属的大区，而不是具体服务器
        # 这样成本查询会基于整个大区的价格，而不是单个服务器
        self.server_list()
        logger.info(f"成本查询使用大区: {self.world} (当前服务器: {self.server})")
        
        self.clipboard = '直接材料\t二级材料\t三级材料\t四级材料\t直接材料数量\t直接材料价值\t二级材料数量\t二级材料价值\t三级材料数量\t三级材料价值\t四级材料数量\t四级材料价值\n'
        start = time.time()
        # del self.stuff
        logger.info("材料树重置")
        self.stuff = {}
        self.d_cost = 0
        self.o_cost = 0
        # 查询配方
        self.query_item_craft()
        # 网络查询失败时提前返回，不显示"不可制作"
        if self.craft_query_failed:
            return None, None
        # 确认到有配方
        if len(self.stuff) > 0:
            self.calibration_quantity(self.stuff['craft'])
            self.d_cost = self.query_item_cost(self.stuff['craft'])
            # debug 计算查询用时
            end = time.time()
            logger.info('材料树计算用时 {}'.format(end - start))
            self.clipboard = '%s\t\t直接材料成本\t%d\t\t原始材料成本\t%d\t\t更新时间\t%s\n\n' % (
                self.stuff['name'], self.d_cost, self.o_cost, self.timestamp_to_time(time.time())) + self.clipboard
            return self.d_cost, self.o_cost
        else:
            self.stuff['craft'] = [{'name': '该物品不能被制作', 'amount': '', 'pricePerUnit': ''}]
            return None, None

    def get_online_version(self):
        """
        通过gitee拉取程序版本
        """
        url = Config.GITEE_RAW_BASE_URL + '/Data/version'
        result = http_client.get_json(url, timeout=5)
        if result is None:
            url = Config.OSS_DATA_BASE_URL + '/version'
            result = http_client.get_json(url, timeout=5)
        if result is None:
            logger.error("版本更新检查失败")
            return {}
        logger.debug("版本更新检查 {} success".format(url))
        return result



if __name__ == '__main__':
    # 初始化测试数据
    # item = '群星壁挂'
    logger.setLevel("DEBUG")
    server = '猫小胖'
    itemObj = Queryer(server)
    with open('Data/item.Pdt', 'r', encoding='utf8') as item_list_file:
        itemObj.item_data = load(item_list_file)
    # 物品选择器列表
    # itemObj.query_item_id(item)
    # 价格查询
    # 35814 大型咖啡馆外墙  29426 伊修加德新型御敌锁甲靴
    # itemObj.id = '35814'
    itemObj.id = '35814'
    itemObj.hq = True
    # https://universalis.app/api/v2/猫小胖/33283?listings=50&hq=true&noGst=true
    # price_list = itemObj.query_item_price()
    # server_list = itemObj.server_list()
    # itemObj.query_every_server(server_list)
    # itemObj.query_item_craft()
    # itemObj.calibration_quantity(itemObj.stuff['craft'])
    itemObj.show_item_cost()
    print(itemObj.stuff)
    # print('直接材料成本{}，原始材料成本{}'.format(itemObj.d_cost, itemObj.o_cost))
    print(itemObj.clipboard)
    # with open('Data/item.Pdt', 'r', encoding='utf8') as item_list:
    #     item_str = item_list.read()
    #     item_data = eval(item_str)
    # version = itemObj.get_online_version()
