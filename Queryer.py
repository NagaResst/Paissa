import time
from json import loads

from requests import get


class Queryer(object):
    def __init__(self, query_server, item_id=None):
        """
        对象初始化
        """
        self.name = None
        self.id = item_id
        self.stuff = {}
        self.d_cost = 0
        self.o_cost = 0
        self.server = query_server
        self.result = None

    @staticmethod
    def init_query_result(url):
        """
        查询结果序列化成字典
        """
        while True:
            try:
                result = get(url, timeout=10)
                break
            except:
                time.sleep(3)
        # 当属性的值为null的时候，无法转换成字典，将其替换为None
        result = result.text.replace('null', '"None"')
        result = loads(result)
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
        itemde = result["Results"]
        return sorted(itemde, key=lambda e: e.__getitem__('ID'), reverse=False)

    def query_item_price(self, hq):
        """
        查询市场价格，根据传入的HQ参数选择查询方法
        """
        if hq is True:
            query_url = 'https://universalis.app/api/v2/%s/%s?listings=50&hq=true&noGst=true' % (
                self.server, self.id)
        elif hq is False:
            query_url = 'https://universalis.app/api/v2/%s/%s?listings=50&hq=false&noGst=true' % (
                self.server, self.id)
        else:
            query_url = 'https://universalis.app/api/%s/%s?listings=50&noGst=true' % (self.server, self.id)
        self.result = self.init_query_result(query_url)
        return self.result

    def query_every_server(self, server_list):
        """
        大区内服务器比价
        """
        listings = []
        for server in server_list:
            # 查询单个服务器的第一个售卖记录
            query_url = 'https://universalis.app/api/%s/%s?listings=1&noGst=true' % (server, self.id)
            result = self.init_query_result(query_url)
            # 为前端界面重新组织本服的最低价数据
            server_sale = {
                'server': server,
                'pricePerUnit': result['listings'][0]['pricePerUnit'],
                'hq': result['listings'][0]['hq'],
                'quantity': result['listings'][0]['quantity'],
                'total': result['listings'][0]['total'],
                'retainerName': result['listings'][0]['retainerName'],
                'lastReviewTime': result['listings'][0]['lastReviewTime']
            }
            listings.append(server_sale)
        return listings


if __name__ == '__main__':
    # 初始化测试数据
    item = '水晶'
    server = '猫小胖'
    itemObj = Queryer(server)
    # 物品选择器列表
    item_list = itemObj.query_item_id(item)
    print(item_list)
    # 价格查询
    hq = False
    itemObj.id = '21697'
    price_list = itemObj.query_item_price(hq)
    print(price_list)
