import os
import sys
import json

from PyQt5 import QtWidgets, QtGui, QtCore

from Paissa import Ui_mainWindow
from Queryer import Queryer
from cost_page import Ui_cost_page
from history_page import Ui_history_Window
from loading_page import Ui_load_page
from query_item_id import Ui_query_item_id
from select_item_list import Ui_select_item_list
from show_price import Ui_show_price

"""
.ui文件是使用 QT desginer 生成的文件，通过 pyuic 将 .ui 文件转换为 .py 文件。 
所以 ui文件 和成对出现的 py文件 不会做任何修改，界面行为在这里进行重新定义，后台查询功能在 Queryer 内实现。
"""


class RQMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(RQMainWindow, self).__init__(parent)

    def closeEvent(self, event):
        global query_history
        for i in query_history:
            if i['itemName'] is None:
                query_history.remove(i)
        history = {"history": query_history}
        with open(history_file, 'w', encoding='utf-8') as his:
            his.write(json.dumps(history))
        event.accept()
        sys.exit(0)  # 退出程序


class MainWindow(Ui_mainWindow):
    def __int__(self):
        super().__init__()

    def setupMenu(self):
        """
        选择服务器菜单栏行为
        """
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


def query_item():
    """
    模糊搜索查询物品
    """
    global query_history
    global first_query
    input_name = query_item_page.input_item_name.text()
    # 如果与上一次查询结果一致，那么直接使用上次查询的列表
    if {"itemName": input_name} == query_history[-1]['itemName'] and len(item.item_list) > 1 and first_query is False:
        ui.show_data_box.setCurrentIndex(1)
    elif input_name == query_history[-1]['itemName'] and item.hq == query_history[-1]['HQ'] \
            and item.server == query_history[-1]['server'] and len(item.item_list) == 1 and first_query is False:
        ui.item_icon.show()
        ui.jump_to_wiki.show()
        ui.show_cost.show()
        ui.back_query.show()
        ui.show_data_box.setCurrentIndex(2)
    else:
        first_query = False
        item.query_item_id(input_name)
        if len(item.item_list) > 1:
            r = 0
            select_item_page.items_list_widget.clearContents()
            select_item_page.items_list_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            select_item_page.items_list_widget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
            select_item_page.items_list_widget.setColumnWidth(0, 120)
            select_item_page.items_list_widget.setRowCount(len(item.item_list))
            for i in item.item_list:
                item_id = QtWidgets.QTableWidgetItem(str(i['ID']))
                item_id.setTextAlignment(4 | 128)
                item_name = QtWidgets.QTableWidgetItem(i['Name'])
                item_name.setTextAlignment(4 | 128)
                select_item_page.items_list_widget.setItem(r, 0, item_id)
                select_item_page.items_list_widget.setItem(r, 1, item_name)
                r += 1
            select_item_page.items_list_widget.repaint()
            ui.show_data_box.setCurrentIndex(1)
        elif len(item.item_list) == 1:
            item.id = item.item_list[0]['ID']
            item.name = item.item_list[0]['Name']
            queru_price()
        else:
            show_message()


def select_item(selectd):
    """
    模糊搜索如果返回多个结果，选择其中一个
    """
    global item
    if type(selectd) is list and len(selectd) > 0:
        item.id = selectd[0].text()
        item.name = selectd[1].text()
    elif type(selectd) is list and len(selectd) == 0:
        item.id = select_item_page.items_list_widget.item(0, 0).text()
        item.name = select_item_page.items_list_widget.item(0, 1).text()
    else:
        table_row = selectd.row()
        item.id = select_item_page.items_list_widget.item(table_row, 0).text()
        item.name = select_item_page.items_list_widget.item(table_row, 1).text()
    queru_price()


def queru_price():
    """
    价格查询
    """
    global query_history
    global server_list
    # 设置wiki链接
    ui.jump_to_wiki.setText(
        '<a href="https://ff14.huijiwiki.com/wiki/%E7%89%A9%E5%93%81:{}">在灰机wiki中查看</a>'.format(item.name))
    widget.setWindowTitle("猴面雀 - FF14市场查询工具 - " + item.name)
    query_sale_list()
    get_item_icon()
    # 如果玩家选择了不在同一个大区的服务器，或者查询其他物品，就重新查询全服比价的数据
    if item.server not in server_list or item.id != query_history[-1]['itemID']:
        server_list = item.server_list()
        # 查询全服比价的数据
        item.query_every_server(server_list)
        query_every_server(item.every_server)
    # 查询完成之后将查询记录加入历史记录
    this_query = {"itemID": item.id, "itemName": item.name, "HQ": item.hq, "server": item.server}
    if this_query in query_history:
        item_name = item.name
        if this_query['HQ'] is True:
            item_name = item.name + 'HQ'
        history_item = history_board.history_list.findItems(item_name, QtCore.Qt.MatchExactly)
        if len(history_item) > 0:
            history_board.history_list.takeItem(history_board.history_list.row(history_item[0]))
        query_history.remove(this_query)
    if item.hq is not True:
        history_board.history_list.insertItem(0, item.name)
    elif item.hq is True:
        history_board.history_list.insertItem(0, item.name + 'HQ')
    query_history.append(this_query)
    query_item_page.query_is_hq.setChecked(item.hq)
    cost_page.cost_tree.clear()
    item.stuff = {}


def query_sale_list():
    """
    正在售出列表填充
    """
    global query_history
    hq_icon = QtGui.QIcon(resource_path(os.path.join("Images", "hq.png")))
    # 查询正在售出的记录
    price_list = item.query_item_price()
    # 更新界面的部分数据
    ui.show_update_time.setText(item.timestamp_to_time(price_list["lastUploadTime"]))
    show_price_page.seven_day.setText("当前大区近七天平均售出价格： " + str("{:,.0f}".format(price_list["averagePrice"])))
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
    ui.show_data_box.setCurrentIndex(2)


def query_every_server(all_server_list):
    """
    全服比价列表填充
    """
    hq_icon = QtGui.QIcon(resource_path(os.path.join("Images", "hq.png")))
    # 设置表格样式
    show_price_page.all_server.clearContents()
    show_price_page.all_server.setRowCount(len(all_server_list))
    # 准备数据
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
    # TODO： 成本树 ： 查询初始化 → 锁定成本按钮 → 查询价格 → 查询配方和材料单价 → 构建成本树 → 解锁成本按钮
    """

    def make_tree(material, father):
        node = QtWidgets.QTreeWidgetItem(father)
        node.setText(0, material['name'])
        node.setText(1, str(material['amount']))
        node.setText(2, str(material['pricePerUnit']))
        if 'craft' in material:
            for i in material['craft']:
                make_tree(i, node)

    if ui.show_data_box.currentIndex() == 3:
        ui.show_data_box.setCurrentIndex(2)
    elif ui.show_data_box.currentIndex() == 2 and len(cost_page.cost_tree.children()) > 7:
        ui.show_data_box.setCurrentIndex(3)
    elif len(cost_page.cost_tree.children()) <= 7:
        if len(item.stuff) > 0:
            ui.show_data_box.setCurrentIndex(3)
        elif len(item.stuff) == 0:
            item.show_item_cost()
            for i in item.stuff:
                make_tree(i, cost_page.cost_tree)
            cost_page.d_cost.setText(str(item.d_cost))
            cost_page.o_cost.setText(str(item.o_cost))
            cost_page.cost_tree.expandAll()
            ui.show_data_box.setCurrentIndex(3)


def click_history_query(selected):
    global query_history
    global first_query
    if selected.row() == 0 and first_query is not True and ui.show_data_box.currentIndex() != 0:
        pass
    else:
        item_name = history_board.history_list.item(selected.row()).text()
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
        queru_price()


def click_select_server(server):
    """
    菜单栏选择服务器重新查询的事件
    """
    global query_server
    query_server = server
    # 修改界面上显示的当前服务器
    ui.show_server.setText(server)
    item.server = server
    # 立刻刷新价格显示的界面
    if item.name is not None and ui.show_data_box.currentIndex() != 0:
        queru_price()


def click_copy_item_name(selected):
    clipboard = QtWidgets.QApplication.clipboard()
    clipboard.setText(selected.text(0))


def select_hq_ornot(status):
    """
    查询HQ的CheckButton
    """
    global query_history
    item.hq = status


def get_item_icon():
    """
    物品图标的地址在查询item_list中包含了
    """
    if len(item.item_list) > 1:
        for i in item.item_list:
            if str(i['ID']) == str(item.id):
                item.get_icon("https://cafemaker.wakingsands.com" + i['Icon'])
                break
    else:
        item.query_item_id(item.name)
        item.get_icon("https://cafemaker.wakingsands.com" + item.item_list[0]['Icon'])
    ui.item_icon.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage.fromData(item.icon)))
    ui.item_icon.setScaledContents(True)
    ui.item_icon.show()


def back_to_index():
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
    if widget2.isVisible():
        widget2.hide()
    elif widget2.isHidden():
        widget2.show()


def create_widget2_page():
    widget2 = QtWidgets.QMainWindow()
    history_board = HistoryPage()
    history_board.setupUi(widget2)


def resource_path(relative_path):
    """
    静态资源打包功能，在spec文件的datas中写入目录名
    """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


"""
公共数据部分
"""
if os.name == 'nt':
    history_file = resource_path(os.path.join(os.getenv('HOMEPATH'), ".Paissa_query_history.txt"))
else:
    history_file = resource_path(os.path.join(os.getenv('HOME'), ".Paissa_query_history.txt"))
try:
    with open(history_file, 'r', encoding='utf-8') as his:
        query_history = json.load(his)['history']
except:
    query_history = [{"itemName": None, "HQ": None, "server": "猫小胖"}]
query_server = '猫小胖'
item = Queryer(query_server)
first_query = True
server_list = []
server_area = ['陆行鸟', '猫小胖', '莫古力', '豆豆柴']

"""
主程序开始
"""
app = QtWidgets.QApplication(sys.argv)
widget = RQMainWindow()
ui = MainWindow()
ui.setupUi(widget)
ui.setupMenu()
ui.jump_to_wiki.setOpenExternalLinks(True)
ui.item_icon.hide()
ui.jump_to_wiki.hide()
ui.show_cost.hide()
ui.back_query.hide()
ui.query_history.show()
ui.back_query.clicked.connect(back_to_index)
ui.show_data_box.setCurrentIndex(0)
ui.query_history.clicked.connect(hidden_history_board)
ui.show_cost.clicked.connect(make_cost_tree)
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
cost_page.cost_tree.horizontalOffset()
cost_page.cost_tree.setColumnWidth(0, 500)
cost_page.cost_tree.itemClicked.connect(click_copy_item_name)

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
history_board.history_list.clicked.connect(click_history_query)
for i in query_history:
    if i['HQ'] is not True:
        history_board.history_list.insertItem(0, i["itemName"])
    elif i['HQ'] is True:
        history_board.history_list.insertItem(0, i["itemName"] + 'HQ')

sys.exit(app.exec_())
