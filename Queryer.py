from requests import get
from json import loads
import math
import time


class Queryer(object):
    def __init__(self, query_server):
        """
        对象初始化
        """
        self.name = None
        self.id = None
        self.stuff = {}
        self.d_cost = 0
        self.o_cost = 0
        self.server = query_server
        self.result = None
        self.hq = None

    @staticmethod
    def init_query_result(url):
        """
        查询结果序列化成字典
        """
        result = None
        try:
            result = get(url)
        except ConnectionError:
            time.sleep(15)
            result = get(url)
        finally:
            # 当属性的值为null的时候，无法转换成字典，将其替换为None
            result = result.text.replace('null', '"None"')
            result = loads(result)
        return result

    @staticmethod
    def timestamp_to_time(timestamp):
        """
        时间戳转换工具
        """
        if timestamp > 9999999999:
            timestamp = float(timestamp / 1000)
        timearray = time.localtime(timestamp)
        result = time.strftime("%Y-%m-%d %H:%M:%S", timearray)
        return result

    def server_list(self):
        """
        为查询所有区服最低价提供支持
        https://ff.web.sdo.com/web8/index.html#/servers
        跨大区开放后 server_list 将返回所有区服的列表
        """
        server_list = ['猫小胖']
        select_server_mao = ['猫小胖', '紫水栈桥', '延夏', '静语庄园', '摩杜纳', '海猫茶屋', '柔风海湾', '琥珀原']
        select_server_zhu = ['莫古力', '白银乡', '白金幻象', '神拳痕', '潮风亭', '旅人栈桥', '拂晓之间', '龙巢神殿', '梦羽宝境']
        select_server_niao = ['陆行鸟', '红玉海', '神意之地', '拉诺西亚', '幻影群岛', '萌芽池', '宇宙和音', '沃仙曦染', '晨曦王座']
        select_server_gou = ['豆豆柴', '水晶塔', '银泪湖', '太阳海岸', '伊修加德', '红茶川']
        if self.server in select_server_mao:
            server_list = ['紫水栈桥', '延夏', '静语庄园', '摩杜纳', '海猫茶屋', '柔风海湾', '琥珀原']
        elif self.server in select_server_niao:
            server_list = ['红玉海', '神意之地', '拉诺西亚', '幻影群岛', '萌芽池', '宇宙和音', '沃仙曦染', '晨曦王座']
        elif self.server in select_server_zhu:
            server_list = ['白银乡', '白金幻象', '神拳痕', '潮风亭', '旅人栈桥', '拂晓之间', '龙巢神殿', '梦羽宝境']
        elif self.server in select_server_gou:
            server_list = ['水晶塔', '银泪湖', '太阳海岸', '伊修加德', '红茶川']
        return server_list

    def query_item_id(self):
        """
        查询官方的物品ID，为后面的查询提供支持
        """
        query_url = 'https://cafemaker.wakingsands.com/search?indexes=item&string=' + self.name
        try:
            result = get(query_url)
        except:
            time.sleep(10)
            result = get(query_url)
        itemstr = result.text.replace('null', '"None"')
        itemde = (loads(itemstr))["Results"]
        if len(itemde) == 1:
            self.id = itemde[0]['ID']
            self.name = itemde[0]['Name']
            return 1
        elif len(itemde) > 1:
            return itemde

    def query_item_price(self):
        pass

    def query_sale_history(self):
        pass

    def query_every_server(self):
        pass
