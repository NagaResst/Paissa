import sys

from PyQt5 import QtWidgets

from Paissa import Ui_mainWindow
from Queryer import Queryer
from query_item_id import Ui_query_item_id
from select_item_list import Ui_select_item_list
from show_price import Ui_show_price

"""
.ui文件是使用 QT desginer 生成的文件，通过 pyuic 将 .ui 文件转换为 .py 文件。 
所以 ui文件 和成对出现的 py文件 不会做任何修改，界面行为在这里进行重新定义，后台查询功能在 Queryer 内实现。
"""


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


def click_select_server(server):
    """
    菜单栏选择服务器重新查询的事件
    """
    global item
    global query_server
    query_server = server
    # 修改界面上显示的当前服务器
    ui.show_server.setText(server)
    item.server = server
    # 立刻刷新价格显示的界面
    queru_price()


def query_item():
    """
    模糊搜索查询物品
    """
    global item
    global last_query
    global item_count
    input_name = query_item_page.input_item_name.text()
    # 如果与上一次查询结果一致，那么直接使用上次查询的列表
    if input_name == last_query and item_count > 1:
        ui.show_data_box.setCurrentIndex(1)
    elif input_name == last_query and item_count == 1:
        ui.show_data_box.setCurrentIndex(2)
    else:
        last_query = input_name
        item_list = item.query_item_id(input_name)
        item_count = len(item_list)
        if item_count > 1:
            r = 0
            select_item_page.items_list_widget.clearContents()
            select_item_page.items_list_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            select_item_page.items_list_widget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
            select_item_page.items_list_widget.setColumnWidth(0, 120)
            select_item_page.items_list_widget.setRowCount(len(item_list))
            for i in item_list:
                item_id = QtWidgets.QTableWidgetItem(str(i['ID']))
                item_id.setTextAlignment(4 | 128)
                item_name = QtWidgets.QTableWidgetItem(i['Name'])
                item_name.setTextAlignment(4 | 128)
                select_item_page.items_list_widget.setItem(r, 0, item_id)
                select_item_page.items_list_widget.setItem(r, 1, item_name)
                r += 1
            select_item_page.items_list_widget.repaint()
            ui.show_data_box.setCurrentIndex(1)
        elif item_count == 1:
            item.id = item_list[0]['ID']
            item.name = item_list[0]['Name']
            queru_price()
        else:
            # TODO: 加入一个弹出提示框，提示用户输入错误，查询不到数据
            pass


def select_item(selectd):
    """
    模糊搜索如果返回多个结果，选择其中一个
    """
    global item
    if type(selectd) is list:
        item.id = selectd[0].text()
        item.name = selectd[1].text()
    else:
        table_row = selectd.row()
        item.id = select_item_page.items_list_widget.item(table_row, 0).text()
        item.name = select_item_page.items_list_widget.item(table_row, 1).text()
    queru_price()


def queru_price():
    """
    价格查询
    TODO: HQ图标的显示
    """
    global hq
    price_list = item.query_item_price(hq)
    ui.show_update_time.setText(item.timestamp_to_time(price_list["lastUploadTime"]))
    show_price_page.seven_day.setText("当前大区近七天平均售出价格： " + str("{:,.0f}".format(price_list["averagePrice"])))
    """
    正在售出列表填充
    """
    r = 0
    # 设定表格行数
    if len(price_list['listings']) > 9:
        show_price_page.sale_list.setRowCount(len(price_list['listings']))
    else:
        show_price_page.sale_list.setRowCount(9)
    # 清空所有数据
    show_price_page.sale_list.clearContents()
    # 设定表格样式
    show_price_page.sale_list.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    show_price_page.sale_list.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
    show_price_page.sale_list.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    show_price_page.sale_list.setColumnWidth(1, 20)
    # 开始填充数据
    for i in price_list["listings"]:
        # 准备数据
        pricePerUnit = QtWidgets.QTableWidgetItem("{:,.0f}".format(i['pricePerUnit']))
        pricePerUnit.setTextAlignment(4 | 128)
        quantity = QtWidgets.QTableWidgetItem(i['quantity'])
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
        show_price_page.sale_list.setItem(r, 2, quantity)
        show_price_page.sale_list.setItem(r, 3, total)
        show_price_page.sale_list.setItem(r, 4, worldName)
        show_price_page.sale_list.setItem(r, 5, retainerName)
        show_price_page.sale_list.setItem(r, 6, lastReviewTime)
        r += 1
    # 表格重绘
    show_price_page.sale_list.repaint()
    """
    全服比价列表填充
    """
    # 查询全服比价的数据
    server_list = item.server_list()
    all_server_list = item.query_every_server(server_list)
    show_price_page.all_server.setRowCount(len(all_server_list))
    show_price_page.all_server.clearContents()
    show_price_page.all_server.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    show_price_page.all_server.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
    show_price_page.all_server.setColumnWidth(2, 20)
    show_price_page.all_server.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    t = 0
    for i in all_server_list:
        server = QtWidgets.QTableWidgetItem(i['server'])
        server.setTextAlignment(4 | 128)
        pricePerUnit = QtWidgets.QTableWidgetItem("{:,.0f}".format(i['pricePerUnit']))
        pricePerUnit.setTextAlignment(4 | 128)
        quantity = QtWidgets.QTableWidgetItem(i['quantity'])
        quantity.setTextAlignment(4 | 128)
        total = QtWidgets.QTableWidgetItem("{:,.0f}".format(i['total'] * 1.05))
        total.setTextAlignment(4 | 128)
        retainerName = QtWidgets.QTableWidgetItem(i['retainerName'])
        retainerName.setTextAlignment(4 | 128)
        lastReviewTime = QtWidgets.QTableWidgetItem(item.timestamp_to_time(i['lastReviewTime']))
        lastReviewTime.setTextAlignment(4 | 128)
        show_price_page.all_server.setItem(t, 0, server)
        show_price_page.all_server.setItem(t, 1, pricePerUnit)
        show_price_page.all_server.setItem(t, 3, quantity)
        show_price_page.all_server.setItem(t, 4, total)
        show_price_page.all_server.setItem(t, 5, retainerName)
        show_price_page.all_server.setItem(t, 6, lastReviewTime)
        t += 1
    show_price_page.all_server.repaint()
    ui.jump_to_wiki.setText(
        '<a href="https://ff14.huijiwiki.com/wiki/%E7%89%A9%E5%93%81:{}">在灰机wiki中查看</a>'.format(item.name))
    ui.item_icon.show()
    # TODO: 加入物品的图标给 ui.item_icon
    ui.jump_to_wiki.show()
    ui.show_cost.show()
    ui.back_query.show()
    ui.show_data_box.setCurrentIndex(2)


def select_hq_ornot(status):
    """
    查询HQ的CheckButton
    """
    global hq
    hq = status


def back_to_index():
    ui.item_icon.hide()
    ui.jump_to_wiki.hide()
    ui.show_cost.hide()
    ui.back_query.hide()
    ui.show_data_box.setCurrentIndex(0)


"""
公共数据部分
"""
query_server = '猫小胖'
item = Queryer(query_server)
query_history = []
hq = None
last_query = None
item_count = 1

"""
主程序开始
"""
app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QMainWindow()
ui = MainWindow()
ui.setupUi(widget)
ui.setupMenu()
ui.jump_to_wiki.setOpenExternalLinks(True)
ui.item_icon.hide()
ui.jump_to_wiki.hide()
ui.show_cost.hide()
ui.back_query.hide()
ui.back_query.clicked.connect(lambda: ui.show_data_box.setCurrentIndex(0))
ui.show_data_box.setCurrentIndex(0)
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
sys.exit(app.exec_())
