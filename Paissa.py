import json
import logging
import os
import sys

from PyQt5 import QtWidgets, QtGui, QtCore

from Queryer import Queryer
from UI.check_update import Ui_check_update
from UI.cost_page import Ui_cost_page
from UI.history_page import Ui_history_Window
from UI.loading_page import Ui_load_page
from UI.main_window import Ui_mainWindow
from UI.query_item_id import Ui_query_item_id
from UI.select_item_list import Ui_select_item_list
from UI.show_price import Ui_show_price

"""
.ui文件是使用 QT desginer 生成的文件，通过 pyuic 将 .ui 文件转换为 .py 文件。 
所以 ui文件 和成对出现的 py文件 不会做任何修改，界面行为在这里进行重新定义，后台查询功能在 Queryer 内实现。
"""
# 解决中文路径的问题  https://github.com/skywind3000/PyStand/issues/6
QtCore.QCoreApplication.addLibraryPath(r'.\site-packages\PyQt5\Qt5\plugins')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s : <%(module)s>  [%(levelname)s]  %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )


class RQMainWindow(QtWidgets.QMainWindow):
    """
    重写窗口关闭的事件用来保存查询历史记录
    """

    def __init__(self, parent=None):
        super(RQMainWindow, self).__init__(parent)

    def closeEvent(self, event):
        global query_history
        # 移除空查询
        for i in query_history:
            if i['itemName'] == 'None' or i['itemName'] is None:
                query_history.remove(i)
        # 查询服务器，是否使用静态资源加速，查询历史
        history = {"server": item.server, 'use_static': item.static, "history": query_history}
        with open(history_file, 'w', encoding='utf-8') as his:
            his.write(json.dumps(history))
            logging.info("数据文件回写成功，准备关闭主程序")
        event.accept()
        sys.exit(0)  # 退出程序


class MainWindow(Ui_mainWindow):
    def __int__(self):
        super().__init__()

    def setup_menu(self):
        """
        菜单栏行为
        """
        self.select_server_china.triggered.connect(lambda: click_select_server('国服'))
        self.select_server_luxingniao.triggered.connect(lambda: click_select_server('陆行鸟'))
        self.select_server_hongyuhai.triggered.connect(lambda: click_select_server("红玉海"))
        self.select_server_shenyizhidi.triggered.connect(lambda: click_select_server("神意之地"))
        self.select_server_lanuoxiya.triggered.connect(lambda: click_select_server("拉诺西亚"))
        self.select_server_huanyignqundao.triggered.connect(lambda: click_select_server("幻影群岛"))
        self.select_server_mengyachi.triggered.connect(lambda: click_select_server("萌芽池"))
        self.select_server_yuzhouheyin.triggered.connect(lambda: click_select_server("宇宙和音"))
        self.select_server_woxianxiran.triggered.connect(lambda: click_select_server("沃仙曦染"))
        self.select_server_chenxiwangzuo.triggered.connect(lambda: click_select_server("晨曦王座"))
        self.select_server_baiyinxiang.triggered.connect(lambda: click_select_server("白银乡"))
        self.select_server_baijinhuanxiang.triggered.connect(lambda: click_select_server("白金幻象"))
        self.select_server_shenquanhen.triggered.connect(lambda: click_select_server("神拳痕"))
        self.select_server_chaofengting.triggered.connect(lambda: click_select_server("潮风亭"))
        self.select_server_lvrenzhanqiao.triggered.connect(lambda: click_select_server("旅人栈桥"))
        self.select_server_fuxiaozhijian.triggered.connect(lambda: click_select_server("拂晓之间"))
        self.select_server_longchaoshendian.triggered.connect(lambda: click_select_server("龙巢神殿"))
        self.select_server_mengyubaojing.triggered.connect(lambda: click_select_server("梦羽宝境"))
        self.select_server_zishuizhanqiao.triggered.connect(lambda: click_select_server("紫水栈桥"))
        self.select_server_yanxia.triggered.connect(lambda: click_select_server("延夏"))
        self.select_server_jingyuzhuagnyuan.triggered.connect(lambda: click_select_server("静语庄园"))
        self.select_server_moduna.triggered.connect(lambda: click_select_server("摩杜纳"))
        self.select_server_haimaochawu.triggered.connect(lambda: click_select_server("海猫茶屋"))
        self.select_server_roufenghaiwan.triggered.connect(lambda: click_select_server("柔风海湾"))
        self.select_server_hupoyuan.triggered.connect(lambda: click_select_server("琥珀原"))
        self.select_server_shuijingta.triggered.connect(lambda: click_select_server("水晶塔"))
        self.select_server_yinleihu.triggered.connect(lambda: click_select_server("银泪湖"))
        self.select_server_taiyanghaian.triggered.connect(lambda: click_select_server("太阳海岸"))
        self.select_server_yixiujiade.triggered.connect(lambda: click_select_server("伊修加德"))
        self.select_server_hongchachuan.triggered.connect(lambda: click_select_server("红茶川"))
        self.select_server_luxingniao.triggered.connect(lambda: click_select_server("陆行鸟"))
        self.select_server_moguli.triggered.connect(lambda: click_select_server("莫古力"))
        self.select_server_maoxiaopang.triggered.connect(lambda: click_select_server("猫小胖"))
        self.select_server_doudouchai.triggered.connect(lambda: click_select_server("豆豆柴"))
        self.use_static_file.triggered.connect(use_static_file_or_not)
        self.check_update.triggered.connect(show_check_update_window)
        self.filter_item.triggered.connect(filter_item_or_not)


"""
为将来重写类型方法预留，可删除
"""


class QueryItemId(Ui_query_item_id):
    def __int__(self):
        super().__init__()


class SelectItemList(Ui_select_item_list):
    def __int__(self):
        super().__init__()


class ShowPrice(Ui_show_price):
    def __int__(self):
        super().__init__()


class LoadingPage(Ui_load_page):
    def __int__(self):
        super().__init__()


class CostPage(Ui_cost_page):
    def __int__(self):
        super().__init__()


class HistoryPage(Ui_history_Window):
    def __int__(self):
        super().__init__()


class CheckUpdate(Ui_check_update):
    def __int__(self):
        super().__init__()


def query_item():
    """
    模糊搜索查询物品
    """
    global query_history
    input_name = query_item_page.input_item_name.text()
    # 如果与上一次查询结果一致，那么直接使用上次查询的列表
    if {"itemName": input_name} == query_history[-1]['itemName'] and len(item.item_list) > 1 and first_query is False:
        logging.info("与上次查询结果一致，切换到物品选择页面")
        ui.show_data_box.setCurrentIndex(1)
    elif input_name == query_history[-1]['itemName'] and item.hq == query_history[-1]['HQ'] \
            and item.server == query_history[-1]['server'] and len(item.item_list) == 1 and first_query is False:
        logging.info("与上次查询结果一致，切换到价格显示页面")
        ui.item_icon.show()
        ui.jump_to_wiki.show()
        ui.show_cost.show()
        ui.back_query.show()
        ui.show_data_box.setCurrentIndex(2)
    else:
        logging.info("开始查找道具")
        item.query_item_id(input_name)
        # 查询到的道具数量大于1
        if len(item.item_list) > 1:
            logging.info("查询到多个道具，开始渲染物品选择界面")
            # 绘制表格，让玩家选择道具
            r = 0
            # 绘制前 清空上次查询结果
            select_item_page.items_list_widget.clearContents()
            # 设置表格样式
            select_item_page.items_list_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            select_item_page.items_list_widget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
            select_item_page.items_list_widget.setColumnWidth(0, 120)
            select_item_page.items_list_widget.setRowCount(len(item.item_list))
            logging.debug("表格填充数据")
            for i in item.item_list:
                item_id = QtWidgets.QTableWidgetItem(str(i['id']))
                item_id.setTextAlignment(4 | 128)
                item_name = QtWidgets.QTableWidgetItem(i['name'])
                item_name.setTextAlignment(4 | 128)
                select_item_page.items_list_widget.setItem(r, 0, item_id)
                select_item_page.items_list_widget.setItem(r, 1, item_name)
                r += 1
            select_item_page.items_list_widget.repaint()
            # 切换到选择物品的界面
            ui.show_data_box.setCurrentIndex(1)
        # 只查询到一个道具
        elif len(item.item_list) == 1:
            logging.info("查询到一个道具，准备进行网络测试")
            item.id = item.item_list[0]['id']
            item.name = item.item_list[0]['name']
            test_network()
        # 查询不到道具
        else:
            logging.warning("查询不到道具")
            show_message()


def select_item(selectd):
    """
    模糊搜索如果返回多个结果，选择其中一个
    判断传入对象的类型，兼容双击条目和点击按钮
    """
    if type(selectd) is list and len(selectd) > 0:
        item.id = selectd[0].text()
        item.name = selectd[1].text()
    # 如果使用者没有选择条目就点击了查询按钮，默认查询第一个
    elif type(selectd) is list and len(selectd) == 0:
        item.id = select_item_page.items_list_widget.item(0, 0).text()
        item.name = select_item_page.items_list_widget.item(0, 1).text()
    else:
        table_row = selectd.row()
        item.id = select_item_page.items_list_widget.item(table_row, 0).text()
        item.name = select_item_page.items_list_widget.item(table_row, 1).text()
    logging.info("选择了一个道具，准备进行网络测试")
    test_network()


def query_price():
    """
    价格查询
    """
    global query_history
    global server_list
    global first_query
    # 设置wiki链接
    first_query = False
    ui.jump_to_wiki.setText(
        '<a href="https://ff14.huijiwiki.com/wiki/%E7%89%A9%E5%93%81:{}">在灰机wiki中查看</a>'.format(item.name))
    widget.setWindowTitle("猴面雀 - FF14市场查询工具 - " + item.name)
    logging.info("开始查询{}的{}".format(item.server, item.name))
    query_sale_list()
    get_item_icon()
    # 如果玩家选择了不在同一个大区的服务器，或者查询其他物品，就重新查询全服比价的数据
    if item.server not in server_list or item.id != query_history[-1]['itemID']:
        server_list = item.server_list()
        # 查询全服比价的数据
        item.query_every_server(server_list)
        query_every_server(item.every_server)
    # 查询完成之后将查询记录加入历史记录。如果已经存在，删除旧的纪录，新的纪录添加到末尾
    this_query = {"itemID": item.id, "itemName": item.name, "HQ": item.hq, "server": item.server}
    if this_query in query_history:
        item_name = item.name + ' - ' + item.server
        if this_query['HQ'] is True:
            item_name = item.name + 'HQ' + ' - ' + item.server
        while True:
            history_item = history_board.history_list.findItems(item_name, QtCore.Qt.MatchExactly)
            if len(history_item) > 0:
                history_board.history_list.takeItem(history_board.history_list.row(history_item[0]))
            else:
                break
        query_history.remove(this_query)
    if item.hq is not True:
        history_board.history_list.insertItem(0, item.name + ' - ' + item.server)
    elif item.hq is True:
        history_board.history_list.insertItem(0, item.name + 'HQ' + ' - ' + item.server)
    query_history.append(this_query)
    logging.debug("查询历史更新完毕")
    query_item_page.query_is_hq.setChecked(item.hq)
    cost_page.cost_tree.clear()


def query_sale_list():
    """
    正在售出列表填充
    """
    hq_icon = QtGui.QIcon(os.path.join("Data", "hq.png"))
    # 查询正在售出的记录
    price_list = item.query_item_price()
    logging.info("物品的售出价格查询完毕，开始绘制价格表格")
    # 更新界面的部分数据
    ui.show_update_time.setText(item.timestamp_to_time(price_list["lastUploadTime"]))
    show_price_page.seven_day.setText(
        "当前大区近七天平均售出价格： " + str("{:,.0f}".format(price_list["averagePrice"])))
    if item.hqs == 0 and item.nqs <= 0.3:
        sv = '这个东西很难卖出去'
    elif item.nqs <= 0.14285715 and item.hqs > 8.88:
        sv = '大家都在买HQ，几乎不买NQ (销量指数：%d)' % item.hqs
    elif item.nqs <= 0.14285715 and 0 < item.hqs < 2:
        sv = '大家只买HQ，并且不太好卖 (销量指数：%d)' % item.hqs
    elif item.hqs == 0 and item.nqs > 12:
        sv = '这个东西很受欢迎 (销量指数：%d)' % item.nqs
    elif item.hqs == 0 and 2 <= item.nqs <= 12:
        sv = '这个东西一定卖得出去 (销量指数：%d)' % item.nqs
    elif item.hqs == 0 and item.nqs == 0:
        sv = '看不出来销量好不好，感觉不太行'
    else:
        sv = "HQ走货量指数为: %.2f ,  NQ走货量指数为: %.2f" % (item.hqs, item.nqs)
    show_price_page.sale_velocity.setText(sv)
    # 开始设置正在售出表格
    r = 0
    # 设定表格行数
    if len(price_list['listings']) > 9:
        show_price_page.sale_list.setRowCount(len(price_list['listings']))
    else:
        show_price_page.sale_list.setRowCount(9)
    # 清空所有数据
    show_price_page.sale_list.clearContents()
    # 开始填充数据
    logging.debug("为价格表格填充数据")
    for i in price_list["listings"]:
        # 准备数据
        pricePerUnit = QtWidgets.QTableWidgetItem("{:,.0f}".format(i['pricePerUnit']))
        pricePerUnit.setTextAlignment(4 | 128)
        hqicon = QtWidgets.QTableWidgetItem()
        hqicon.setIcon(hq_icon)
        hqicon.setTextAlignment(4 | 128)
        quantity = QtWidgets.QTableWidgetItem(str(i['quantity']))
        quantity.setTextAlignment(4 | 128)
        total = QtWidgets.QTableWidgetItem("{:,.0f}".format(i['total'] * 1.05))
        total.setTextAlignment(4 | 128)
        retainerName = QtWidgets.QTableWidgetItem(i['retainerName'])
        retainerName.setTextAlignment(4 | 128)
        lastReviewTime = QtWidgets.QTableWidgetItem(item.timestamp_to_time(i['lastReviewTime']))
        lastReviewTime.setTextAlignment(4 | 128)
        if 'worldName' in i:
            worldName = QtWidgets.QTableWidgetItem(i['worldName'])
        else:
            worldName = QtWidgets.QTableWidgetItem(item.server)
        worldName.setTextAlignment(4 | 128)
        # 填充数据 r = row
        show_price_page.sale_list.setItem(r, 0, pricePerUnit)
        if i['hq'] is True:
            show_price_page.sale_list.setItem(r, 1, hqicon)
        show_price_page.sale_list.setItem(r, 2, quantity)
        show_price_page.sale_list.setItem(r, 3, total)
        show_price_page.sale_list.setItem(r, 4, worldName)
        show_price_page.sale_list.setItem(r, 5, retainerName)
        show_price_page.sale_list.setItem(r, 6, lastReviewTime)
        r += 1
    # 表格绘制
    show_price_page.sale_list.repaint()
    ui.jump_to_wiki.show()
    ui.show_cost.show()
    ui.back_query.show()
    ui.query_history.show()
    ui.show_cost.setText('成本计算')
    ui.show_data_box.setCurrentIndex(2)


def query_every_server(all_server_list):
    """
    全服比价列表填充
    """
    hq_icon = QtGui.QIcon(os.path.join("Data", "hq.png"))
    # 设置表格样式
    show_price_page.all_server.clearContents()
    show_price_page.all_server.setRowCount(len(all_server_list))
    # 准备数据
    logging.debug("绘制全服比价数据表格")
    t = 0
    for i in all_server_list:
        server = QtWidgets.QTableWidgetItem(i['server'])
        server.setTextAlignment(4 | 128)
        pricePerUnit = QtWidgets.QTableWidgetItem("{:,.0f}".format(i['pricePerUnit']))
        pricePerUnit.setTextAlignment(4 | 128)
        hqicon = QtWidgets.QTableWidgetItem()
        hqicon.setIcon(hq_icon)
        hqicon.setTextAlignment(4 | 128)
        quantity = QtWidgets.QTableWidgetItem(str(i['quantity']))
        quantity.setTextAlignment(4 | 128)
        total = QtWidgets.QTableWidgetItem("{:,.0f}".format(i['total'] * 1.05))
        total.setTextAlignment(4 | 128)
        retainerName = QtWidgets.QTableWidgetItem(i['retainerName'])
        retainerName.setTextAlignment(4 | 128)
        lastReviewTime = QtWidgets.QTableWidgetItem(item.timestamp_to_time(i['lastReviewTime']))
        lastReviewTime.setTextAlignment(4 | 128)
        # 填充数据   t = row
        show_price_page.all_server.setItem(t, 0, server)
        show_price_page.all_server.setItem(t, 1, pricePerUnit)
        if i['hq'] is True:
            show_price_page.all_server.setItem(t, 2, hqicon)
        show_price_page.all_server.setItem(t, 3, quantity)
        show_price_page.all_server.setItem(t, 4, total)
        show_price_page.all_server.setItem(t, 5, retainerName)
        show_price_page.all_server.setItem(t, 6, lastReviewTime)
        t += 1
    show_price_page.all_server.repaint()


def make_cost_tree():
    """
    成本树，显示这个物品的制作材料和成本
    """

    def make_tree(material, father):
        """
        材料树的绘制方法
        """
        node = QtWidgets.QTreeWidgetItem(father)
        node.setText(0, material['name'])
        node.setText(1, str(material['amount']))
        node.setText(2, str(material['pricePerUnit']))
        if 'craft' in material:
            for i in material['craft']:
                make_tree(i, node)

    if ui.show_data_box.currentIndex() == 3:
        ui.show_cost.setText('成本计算')
        ui.show_data_box.setCurrentIndex(2)
    elif ui.show_data_box.currentIndex() == 2 and len(item.stuff) > 0:
        logging.debug("材料树中有内容，判断已经查询过材料树，切换界面")
        ui.show_cost.setText('市场价格')
        ui.show_data_box.setCurrentIndex(3)
    elif len(item.stuff) == 0:
        logging.debug("材料树是空的，开始查询")
        item.show_item_cost()
        logging.info("开始绘制材料树")
        cost_page.cost_tree.clear()
        for i in item.stuff['craft']:
            make_tree(i, cost_page.cost_tree)
        cost_page.d_cost.setText(str(item.d_cost))
        cost_page.o_cost.setText(str(item.o_cost))
        # 1级子材料数量不超过9个的时候展开材料树
        if len(item.stuff['craft']) < 9:
            cost_page.cost_tree.expandAll()
        # 如果这个道具一次生产制作多个的利润算法兼容
        if item.yields > 1:
            p = item.avgp * item.yields - item.d_cost
            cost_page.profit.setText('%d = ( %d * %d - %d )' % (p, item.avgp, item.yields, item.d_cost))
        else:
            p = item.avgp - item.d_cost
            cost_page.profit.setText('%d = ( %d - %d )' % (p, item.avgp, item.d_cost))
        ui.show_cost.setText('市场价格')
        ui.show_data_box.setCurrentIndex(3)


def click_history_query(selected):
    """
    通过点击历史面板查询物品
    """
    # print(selected, isinstance(selected, QtCore.QModelIndex))
    global query_history
    # 最顶端的记录为本次查询的结果，do nothing
    if selected.row() == 0 and first_query is not True:
        pass
    else:
        # 重新查询
        recode1 = history_board.history_list.item(selected.row()).text().split()
        item_name = recode1[0]
        item.server = recode1[-1]
        if item.server == 'Japan':
            ui.show_server.setText('日服')
        elif item.server == 'Europe':
            ui.show_server.setText('欧服')
        elif item.server == 'North-America':
            ui.show_server.setText('美服')
        elif item.server == 'Oceania':
            ui.show_server.setText("太平洋服")
        elif item.server == "China":
            ui.show_server.setText("国服")
        else:
            ui.show_server.setText(item.server)
        logging.info("通过点击历史面板进行查询 {} 的 {}".format(item.server, item_name))
        if item_name[-2:] == 'HQ':
            item_name = item_name[0:-2]
            item.hq = True
        else:
            item.hq = False
        for i in query_history:
            if i["itemName"] == item_name:
                item.id = i['itemID']
                item.name = item_name
                break
        query_item_page.input_item_name.setText(item.name)
        item.item_list = []
        test_network()


def click_select_server(server):
    """
    菜单栏选择服务器重新查询的事件
    """
    global server_list
    # 修改界面上显示的当前服务器
    ui.show_server.setText(server)
    if server == "欧服":
        item.server = 'Europe'
    elif server == "日服":
        item.server = 'Japan'
    elif server == "美服":
        item.server = 'North-America'
    elif server == "太平洋服":
        item.server = 'Oceania'
    elif server == "国服":
        item.server = 'China'
    else:
        item.server = server
    server_list = item.server_list()
    # 立刻刷新价格显示的界面
    if item.name is not None and ui.show_data_box.currentIndex() != 0:
        logging.info("重新选择了服务器为{}，开始进行{}价格查询".format(item.server, item.name))
        item.price_cache = {}
        query_price()


def click_query_item_name(selected):
    # 点击材料树的条目将道具名复制到剪贴板
    if selected.text(0) != '该物品不能被制作':
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(selected.text(0))
        item.name = selected.text(0)
        logging.info("材料名称 {} 已经复制到粘贴板".format(item.name))
        for i in item.item_data.values():
            if i['name'] == item.name:
                item.id = i['id']
        query_item_page.input_item_name.setText(item.name)
        item.item_list = []
        logging.info("通过点击材料树重新查询材料 {}".format(item.name))
        query_price()
    else:
        back_to_index()


def click_copy_cost_tree():
    # 点击材料树的条目将道具名复制到剪贴板
    clipboard = QtWidgets.QApplication.clipboard()
    clipboard.setText(item.clipboard)


def select_hq_ornot(status):
    """
    查询HQ的CheckButton
    """
    item.hq = status


def use_static_file_or_not(status):
    """
    是否启用静态资源加速
    """
    item.static = status


def filter_item_or_not(status):
    """
    过滤不可在市场上交易的物品
    """
    item.filter_item = status


def get_item_icon():
    """
    绘制物品图标的方法
    """
    item.get_icon()
    ui.item_icon.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage.fromData(item.icon)))
    ui.item_icon.setScaledContents(True)
    ui.item_icon.show()


def back_to_index():
    """
    返回首页的按钮事件
    """
    ui.item_icon.hide()
    ui.jump_to_wiki.hide()
    ui.show_cost.hide()
    ui.back_query.hide()
    ui.show_data_box.setCurrentIndex(0)


def show_message():
    """
    首页查询不到物品的提示
    """
    ui.show_data_box.setCurrentIndex(0)
    QtWidgets.QMessageBox.warning(ui.query_item, "物品名称错误", "查询不到任何物品")


def hidden_history_board():
    """
    显示或者隐藏查询历史面板
    """
    if widget2.isVisible():
        widget2.hide()
    elif widget2.isHidden():
        widget2.show()


def show_check_update_window():
    """
    显示或者隐藏关于面板，包含检查更新的事件
    """
    # 如果没有查询过版本，就开始一次版本检查
    if check_update_window.latest_program_version.text() == 'N/A':
        version_online = item.get_online_version()
        check_update_window.latest_program_version.setText(version_online['program'])
        check_update_window.latest_data_version.setText(version_online['data'])
    c_p_v = check_update_window.current_program_version.text()
    c_d_v = check_update_window.current_data_verison.text()
    l_p_v = check_update_window.latest_program_version.text()
    l_d_v = check_update_window.latest_data_version.text()
    # 数据文件可以单独更新
    if c_p_v == l_p_v and c_d_v == l_d_v:
        check_update_window.update_text.hide()
    elif c_p_v == l_p_v and c_d_v != l_d_v:
        check_update_window.update_text.setText('数据文件需要更新')
    else:
        check_update_window.update_text.setText(
            '请点击 <a href=\"http://43.142.142.18/Paissa.zip\"><span style=\" text-decoration: underline; color:#0000ff;\">这里</span></a> 下载最新版本')
        check_update_window.update_text.setOpenExternalLinks(True)
    # 面板隐藏或者显示
    if widget3.isVisible():
        widget3.hide()
    elif widget3.isHidden():
        widget3.show()


def test_network():
    global first_query
    if first_query is True:
        result = item.test_network()
        logging.info('网络测试结果，{}'.format(result))
        if result == "success":
            query_price()
        else:
            QtWidgets.QMessageBox.warning(ui.query_item, "网络错误", "无法连接价格查询网站或连接速度过慢")
    else:
        logging.info('跳过网络测试')
        query_price()


"""
公共数据部分
"""
logging.info("主程序启动，开始处理公共数据")
# 与 Data/version 文件中的版本对应
program_version = '0.9.4'
# 加载查询历史
history_file = os.path.join('Data', "Paissa_query_history.log")
try:
    with open(history_file, 'r', encoding='utf-8') as his:
        history_json = json.load(his)
        query_history = history_json['history']
        # 如果使用者点开过软件，却没有查询道具，会生成空查询记录的历史文件。
        if len(query_history) == 0:
            # 加入None条目，后面的切换界面判断方法就不用判空了
            query_history = [{"itemName": 'None', "HQ": None, "server": 'None'}]
        item = Queryer(history_json['server'])
        logging.info("读取查询历史成功")
except FileNotFoundError:
    history_json = {"server": '猫小胖', 'use_static': True, "history": []}
    query_history = [{"itemName": 'None', "HQ": None, "server": 'None'}]
    item = Queryer('猫小胖')
    logging.warning("没有发现历史数据，初始化历史数据")
# 加载本地静态文件
with open('Data/item.Pdt', 'r', encoding='utf8') as item_list_file:
    item.item_data = json.load(item_list_file)
date_version = item.item_data['data-version']
item.header = {'User-Agent': 'Paissa {}'.format(program_version)}
logging.info("数据文件加载完毕，程序版本{}，数据版本{}".format(program_version, date_version))
if 'use_static' not in history_json:
    history_json['use_static'] = True
item.static = history_json['use_static']
item.item_data.pop('data-version')
first_query = True
server_list = []
logging.debug("主程序数据初始化完成")

"""
主程序开始
"""
app = QtWidgets.QApplication(sys.argv)
desktop = app.desktop()
logging.debug("获取到桌面大小为{} * {}".format(desktop.width(), desktop.height()))
app.setStyle("Fusion")
widget = RQMainWindow()
ui = MainWindow()
ui.setupUi(widget)
widget.resize(int(desktop.width()*0.6), int(desktop.height()*0.6))
ui.setup_menu()
ui.jump_to_wiki.setOpenExternalLinks(True)
ui.show_server.setText(item.server)
ui.item_icon.hide()
ui.jump_to_wiki.hide()
ui.show_cost.hide()
ui.back_query.hide()
ui.query_history.show()
ui.back_query.clicked.connect(back_to_index)
ui.show_data_box.setCurrentIndex(0)
ui.query_history.clicked.connect(hidden_history_board)
ui.show_cost.clicked.connect(make_cost_tree)
ui.use_static_file.setChecked(history_json['use_static'])
widget.show()

"""
物品查询首页
"""
query_item_page = QueryItemId()
query_item_page.setupUi(ui.query_item)
query_item_page.query_button.clicked.connect(query_item)
query_item_page.input_item_name.returnPressed.connect(query_item)
query_item_page.query_is_hq.clicked.connect(select_hq_ornot)

"""
模糊搜索时选择物品的界面
"""
select_item_page = SelectItemList()
select_item_page.setupUi(ui.select_item)
select_item_page.back.clicked.connect(lambda: ui.show_data_box.setCurrentIndex(0))
select_item_page.items_list_widget.doubleClicked.connect(select_item)
# 在选择物品界面选中物品后点击“选择物品”的按钮，把选中行作为对象传给价格查询模块
select_item_page.select_this.clicked.connect(lambda: select_item(select_item_page.items_list_widget.selectedItems()))

"""
价格显示界面
"""
show_price_page = ShowPrice()
show_price_page.setupUi(ui.show_price)
# 设定在售表格样式
show_price_page.sale_list.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
show_price_page.sale_list.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
show_price_page.sale_list.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
# HQ列
show_price_page.sale_list.setColumnWidth(1, 20)
# 设定比价表格样式
show_price_page.all_server.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
show_price_page.all_server.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
# HQ列
show_price_page.all_server.setColumnWidth(2, 20)
show_price_page.all_server.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
"""
材料成本树
"""
cost_page = CostPage()
cost_page.setupUi(ui.show_craft)
cost_page.cost_tree.setColumnWidth(0, 500)
cost_page.cost_tree.itemDoubleClicked.connect(click_query_item_name)
cost_page.click_c.clicked.connect(click_copy_cost_tree)

"""
loading界面
"""
loading_page = LoadingPage()
loading_page.setupUi(ui.loading_ui)

"""
查询历史面板
"""
widget2 = QtWidgets.QMainWindow()
history_board = HistoryPage()
history_board.setupUi(widget2)
widget2.resize(int(desktop.width()*0.15), int(desktop.height()*0.6))
history_board.history_list.doubleClicked.connect(click_history_query)
for i in query_history:
    if i['HQ'] is not True and i["itemName"] != 'None':
        history_board.history_list.insertItem(0, i["itemName"] + ' - ' + i['server'])
    elif i['HQ'] is True and i["itemName"] != 'None':
        history_board.history_list.insertItem(0, i["itemName"] + 'HQ' + ' - ' + i['server'])

"""
check update
"""
widget3 = QtWidgets.QMainWindow()
check_update_window = CheckUpdate()
check_update_window.setupUi(widget3)
# 关于面板的超链接激活
check_update_window.label_8.setOpenExternalLinks(True)
check_update_window.current_program_version.setText(program_version)
check_update_window.current_data_verison.setText(date_version)

sys.exit(app.exec_())
