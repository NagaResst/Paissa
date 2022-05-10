import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets as QW

from Paissa import Ui_mainWindow
from Queryer import Queryer
from query_item_id import Ui_query_item_id
from select_item_list import Ui_select_item_list


class mainWindow(Ui_mainWindow):
    def __int__(self):
        super().__init__()
        self.uptime = None
        self.query_item = None
        self.is_hq = None

    def click_select_server(self, server):
        self.query_server = server
        self.show_server.setText(server)

    def setupMenu(self):
        """选择服务器菜单栏行为"""
        self.query_server = '猫小胖'
        self.select_server_luxingniao.triggered.connect(lambda: self.click_select_server('陆行鸟'))
        self.select_server_hongyuhai.triggered.connect(lambda: self.click_select_server("红玉海"))
        self.select_server_shenyizhidi.triggered.connect(lambda: self.click_select_server("神意之地"))
        self.select_server_lanuoxiya.triggered.connect(lambda: self.click_select_server("拉诺西亚"))
        self.select_server_huanyignqundao.triggered.connect(lambda: self.click_select_server("幻影群岛"))
        self.select_server_mengyachi.triggered.connect(lambda: self.click_select_server("萌芽池"))
        self.select_server_yuzhouheyin.triggered.connect(lambda: self.click_select_server("宇宙和音"))
        self.select_server_woxianxiran.triggered.connect(lambda: self.click_select_server("沃仙曦染"))
        self.select_server_chenxiwangzuo.triggered.connect(lambda: self.click_select_server("晨曦王座"))
        self.select_server_baiyinxiang.triggered.connect(lambda: self.click_select_server("白银乡"))
        self.select_server_baijinhuanxiang.triggered.connect(lambda: self.click_select_server("白金幻象"))
        self.select_server_shenquanhen.triggered.connect(lambda: self.click_select_server("神拳痕"))
        self.select_server_chaofengting.triggered.connect(lambda: self.click_select_server("潮风亭"))
        self.select_server_lvrenzhanqiao.triggered.connect(lambda: self.click_select_server("旅人栈桥"))
        self.select_server_fuxiaozhijian.triggered.connect(lambda: self.click_select_server("拂晓之间"))
        self.select_server_longchaoshendian.triggered.connect(lambda: self.click_select_server("龙巢神殿"))
        self.select_server_mengyubaojing.triggered.connect(lambda: self.click_select_server("梦羽宝境"))
        self.select_server_zishuizhanqiao.triggered.connect(lambda: self.click_select_server("紫水栈桥"))
        self.select_server_yanxia.triggered.connect(lambda: self.click_select_server("延夏"))
        self.select_server_jingyuzhuagnyuan.triggered.connect(lambda: self.click_select_server("静语庄园"))
        self.select_server_moduna.triggered.connect(lambda: self.click_select_server("摩杜纳"))
        self.select_server_haimaochawu.triggered.connect(lambda: self.click_select_server("海猫茶屋"))
        self.select_server_roufenghaiwan.triggered.connect(lambda: self.click_select_server("柔风海湾"))
        self.select_server_hupoyuan.triggered.connect(lambda: self.click_select_server("琥珀原"))
        self.select_server_shuijingta.triggered.connect(lambda: self.click_select_server("水晶塔"))
        self.select_server_yinleihu.triggered.connect(lambda: self.click_select_server("银泪湖"))
        self.select_server_taiyanghaian.triggered.connect(lambda: self.click_select_server("太阳海岸"))
        self.select_server_yixiujiade.triggered.connect(lambda: self.click_select_server("伊修加德"))
        self.select_server_hongchachuan.triggered.connect(lambda: self.click_select_server("红茶川"))
        self.select_server_luxingniao.triggered.connect(lambda: self.click_select_server("陆行鸟"))
        self.select_server_moguli.triggered.connect(lambda: self.click_select_server("莫古力"))
        self.select_server_maoxiaopang.triggered.connect(lambda: self.click_select_server("猫小胖"))
        self.select_server_doudouchai.triggered.connect(lambda: self.click_select_server("豆豆柴"))
        """选择服务器菜单栏行为结束"""


class query_item_id(Ui_query_item_id):
    def __int__(self):
        super().__init__()


class select_item_list(Ui_select_item_list):
    def __int__(self):
        super().__init__()


def query_item():
    input_name = query_item_page.input_item_name.text()
    item = Queryer(input_name, ui.query_server)
    item_list = item.query_item_id()
    if len(item_list) > 1:
        select_item_page = select_item_list()
        select_item_page.setupUi(ui.select_item)
        r = 0
        select_item_page.items_list_widget.horizontalHeader().setSectionResizeMode(QW.QHeaderView.Stretch)
        select_item_page.items_list_widget.horizontalHeader().setSectionResizeMode(0, QW.QHeaderView.Fixed)
        select_item_page.items_list_widget.setColumnWidth(0, 120)
        select_item_page.items_list_widget.setRowCount(len(item_list))
        for i in item_list:
            item_id = QW.QTableWidgetItem(str(i['ID']))
            item_id.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item_name = QW.QTableWidgetItem(i['Name'])
            item_name.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            select_item_page.items_list_widget.setItem(r, 0, item_id)
            select_item_page.items_list_widget.setItem(r, 1, item_name)
            r += 1
        select_item_page.items_list_widget.repaint()
        ui.show_data_box.setCurrentIndex(1)


"""
公共数据部分
"""

"""
主程序开始
"""
app = QW.QApplication(sys.argv)
widget = QW.QMainWindow()
ui = mainWindow()
ui.setupUi(widget)
ui.setupMenu()
widget.show()
query_item_page = query_item_id()
query_item_page.setupUi(ui.query_item)
query_item_page.query_button.clicked.connect(query_item)
sys.exit(app.exec_())
