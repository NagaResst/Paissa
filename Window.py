import json
import os
import sys
import time

from PyQt5 import QtWidgets, QtGui, QtCore

from Data.logger import logger
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
        history = {"program_version": program_version, "server": item.server, 'use_static': item.static,
                   "history": query_history}
        with open(history_file, 'w', encoding='utf-8') as his:
            his.write(json.dumps(history))
            logger.info("数据文件回写成功，准备关闭主程序")
        event.accept()
        sys.exit(0)  # 退出程序


class MainWindow(Ui_mainWindow):
    def __int__(self):
        super().__init__()

    def setup_menu(self):
        """
        菜单栏行为
        """
        self.select_server_china.triggered.connect(lambda: self.click_select_server('国服'))
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
        try:
            self.select_server_Elemental.triggered.connect(lambda: self.click_select_server("Elemental"))
            self.select_server_Carbuncle.triggered.connect(lambda: self.click_select_server("Carbuncle"))
            self.select_server_Kujata.triggered.connect(lambda: self.click_select_server("Kujata"))
            self.select_server_Typhon.triggered.connect(lambda: self.click_select_server("Typhon"))
            self.select_server_Garuda.triggered.connect(lambda: self.click_select_server("Garuda"))
            self.select_server_Atomos.triggered.connect(lambda: self.click_select_server("Atomos"))
            self.select_server_Tonberry.triggered.connect(lambda: self.click_select_server("Tonberry"))
            self.select_server_Aegis.triggered.connect(lambda: self.click_select_server("Aegis"))
            self.select_server_Gungnir.triggered.connect(lambda: self.click_select_server("Gungnir"))
            self.select_server_Gaia.triggered.connect(lambda: self.click_select_server("Gaia"))
            self.select_server_Alexander.triggered.connect(lambda: self.click_select_server("Alexander"))
            self.select_server_Fenrir.triggered.connect(lambda: self.click_select_server("Fenrir"))
            self.select_server_Ultima.triggered.connect(lambda: self.click_select_server("Ultima"))
            self.select_server_Ifrit.triggered.connect(lambda: self.click_select_server("Ifrit"))
            self.select_server_Bahamut.triggered.connect(lambda: self.click_select_server("Bahamut"))
            self.select_server_Tiamat.triggered.connect(lambda: self.click_select_server("Tiamat"))
            self.select_server_Durandal.triggered.connect(lambda: self.click_select_server("Durandal"))
            self.select_server_Ridill.triggered.connect(lambda: self.click_select_server("Ridill"))
            self.select_server_Mana.triggered.connect(lambda: self.click_select_server("Mana"))
            self.select_server_Asura.triggered.connect(lambda: self.click_select_server("Asura"))
            self.select_server_Pandaemonium.triggered.connect(lambda: self.click_select_server("Pandaemonium"))
            self.select_server_Anima.triggered.connect(lambda: self.click_select_server("Anima"))
            self.select_server_Hades.triggered.connect(lambda: self.click_select_server("Hades"))
            self.select_server_Ixion.triggered.connect(lambda: self.click_select_server("Ixion"))
            self.select_server_Titan.triggered.connect(lambda: self.click_select_server("Titan"))
            self.select_server_Chocobo.triggered.connect(lambda: self.click_select_server("Chocobo"))
            self.select_server_Masamune.triggered.connect(lambda: self.click_select_server("Masamune"))
            self.select_server_Aether.triggered.connect(lambda: self.click_select_server("Aether"))
            self.select_server_Jenova.triggered.connect(lambda: self.click_select_server("Jenova"))
            self.select_server_Faerie.triggered.connect(lambda: self.click_select_server("Faerie"))
            self.select_server_Siren.triggered.connect(lambda: self.click_select_server("Siren"))
            self.select_server_Gilgamesh.triggered.connect(lambda: self.click_select_server("Gilgamesh"))
            self.select_server_Midgardsormr.triggered.connect(lambda: self.click_select_server("Midgardsormr"))
            self.select_server_Adamantoise.triggered.connect(lambda: self.click_select_server("Adamantoise"))
            self.select_server_Cactuar.triggered.connect(lambda: self.click_select_server("Cactuar"))
            self.select_server_Sargatanas.triggered.connect(lambda: self.click_select_server("Sargatanas"))
            self.select_server_Primal.triggered.connect(lambda: self.click_select_server("Primal"))
            self.select_server_Famfrit.triggered.connect(lambda: self.click_select_server("Famfrit"))
            self.select_server_Exodus.triggered.connect(lambda: self.click_select_server("Exodus"))
            self.select_server_Lamia.triggered.connect(lambda: self.click_select_server("Lamia"))
            self.select_server_Leviathan.triggered.connect(lambda: self.click_select_server("Leviathan"))
            self.select_server_Ultros.triggered.connect(lambda: self.click_select_server("Ultros"))
            self.select_server_Behemoth.triggered.connect(lambda: self.click_select_server("Behemoth"))
            self.select_server_Excalibur.triggered.connect(lambda: self.click_select_server("Excalibur"))
            self.select_server_Hyperion.triggered.connect(lambda: self.click_select_server("Hyperion"))
            self.select_server_Chaos.triggered.connect(lambda: self.click_select_server("Chaos"))
            self.select_server_Omega.triggered.connect(lambda: self.click_select_server("Omega"))
            self.select_server_Moogle.triggered.connect(lambda: self.click_select_server("Moogle"))
            self.select_server_Cerberus.triggered.connect(lambda: self.click_select_server("Cerberus"))
            self.select_server_Louisoix.triggered.connect(lambda: self.click_select_server("Louisoix"))
            self.select_server_Spriggan.triggered.connect(lambda: self.click_select_server("Spriggan"))
            self.select_server_Ragnarok.triggered.connect(lambda: self.click_select_server("Ragnarok"))
            self.select_server_Sagittarius.triggered.connect(lambda: self.click_select_server("Sagittarius"))
            self.select_server_Phantom.triggered.connect(lambda: self.click_select_server("Phantom"))
            self.select_server_Light.triggered.connect(lambda: self.click_select_server("Light"))
            self.select_server_Twintania.triggered.connect(lambda: self.click_select_server("Twintania"))
            self.select_server_Lich.triggered.connect(lambda: self.click_select_server("Lich"))
            self.select_server_Zodiark.triggered.connect(lambda: self.click_select_server("Zodiark"))
            self.select_server_Phoenix.triggered.connect(lambda: self.click_select_server("Phoenix"))
            self.select_server_Odin.triggered.connect(lambda: self.click_select_server("Odin"))
            self.select_server_Shiva.triggered.connect(lambda: self.click_select_server("Shiva"))
            self.select_server_Alpha.triggered.connect(lambda: self.click_select_server("Alpha"))
            self.select_server_Raiden.triggered.connect(lambda: self.click_select_server("Raiden"))
            self.select_server_Crystal.triggered.connect(lambda: self.click_select_server("Crystal"))
            self.select_server_Brynhildr.triggered.connect(lambda: self.click_select_server("Brynhildr"))
            self.select_server_Mateus.triggered.connect(lambda: self.click_select_server("Mateus"))
            self.select_server_Zalera.triggered.connect(lambda: self.click_select_server("Zalera"))
            self.select_server_Diabolos.triggered.connect(lambda: self.click_select_server("Diabolos"))
            self.select_server_Coeurl.triggered.connect(lambda: self.click_select_server("Coeurl"))
            self.select_server_Malboro.triggered.connect(lambda: self.click_select_server("Malboro"))
            self.select_server_Goblin.triggered.connect(lambda: self.click_select_server("Goblin"))
            self.select_server_Balmung.triggered.connect(lambda: self.click_select_server("Balmung"))
            self.select_server_Materia.triggered.connect(lambda: self.click_select_server("Materia"))
            self.select_server_Ravana.triggered.connect(lambda: self.click_select_server("Ravana"))
            self.select_server_Bismarck.triggered.connect(lambda: self.click_select_server("Bismarck"))
            self.select_server_Sephirot.triggered.connect(lambda: self.click_select_server("Sephirot"))
            self.select_server_Sophia.triggered.connect(lambda: self.click_select_server("Sophia"))
            self.select_server_Zurvan.triggered.connect(lambda: self.click_select_server("Zurvan"))
            self.select_server_Meteor.triggered.connect(lambda: self.click_select_server("Meteor"))
            self.select_server_Belias.triggered.connect(lambda: self.click_select_server("Belias"))
            self.select_server_Shinryu.triggered.connect(lambda: self.click_select_server("Shinryu"))
            self.select_server_Unicorn.triggered.connect(lambda: self.click_select_server("Unicorn"))
            self.select_server_Yojimbo.triggered.connect(lambda: self.click_select_server("Yojimbo"))
            self.select_server_Zeromus.triggered.connect(lambda: self.click_select_server("Zeromus"))
            self.select_server_Valefor.triggered.connect(lambda: self.click_select_server(""))
            self.select_server_Ramuh.triggered.connect(lambda: self.click_select_server("Ramuh"))
            self.select_server_Mandragora.triggered.connect(lambda: self.click_select_server("Mandragora"))
            self.select_server_Dynamis.triggered.connect(lambda: self.click_select_server("Dynamis"))
            self.select_server_Marilith.triggered.connect(lambda: self.click_select_server("Marilith"))
            self.select_server_Seraph.triggered.connect(lambda: self.click_select_server("Seraph"))
            self.select_server_Halicarnassus.triggered.connect(lambda: self.click_select_server("Halicarnassus"))
            self.select_server_Maduin.triggered.connect(lambda: self.click_select_server("Maduin"))
            self.select_server_japan.triggered.connect(lambda: self.click_select_server("日服"))
            self.select_server_na.triggered.connect(lambda: self.click_select_server("美服"))
            self.select_server_europe.triggered.connect(lambda: self.click_select_server("欧服"))
            self.select_server_oceania.triggered.connect(lambda: self.click_select_server("太平洋服"))
        except:
            pass
        self.use_static_file.triggered.connect(self.use_static_file_or_not)
        self.check_update.triggered.connect(self.show_check_update_window)
        self.filter_item.triggered.connect(self.filter_item_or_not)

    def select_item_action(self, selectd):
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
        logger.info("选择了一个道具，准备进行网络测试")
        self.test_network()

    def test_network(self):
        global first_query
        if first_query is True:
            result = item.test_network()
            logger.info('网络测试结果，{}'.format(result))
            if result == "success":
                ui.query_price()
            else:
                QtWidgets.QMessageBox.warning(self.query_item, "网络故障",
                                              "您的网络无法连接在线数据源，请更换网络环境")
        else:
            logger.info('跳过网络测试')
            self.query_price()

    def query_every_server(self, all_server_list):
        """
        全服比价列表填充
        """
        hq_icon = QtGui.QIcon(os.path.join("Data", "hq.png"))
        # 设置表格样式
        show_price_page.all_server.clearContents()
        show_price_page.all_server.setRowCount(len(all_server_list))
        # 准备数据
        logger.debug("绘制全服比价数据表格")
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
        show_price_page.all_server.doubleClicked.connect(self.click_select_other_server)

    def click_select_other_server(self, selected):
        """
        通过点击全服比价的结果重新选择服务器
        """
        server = show_price_page.all_server.item(selected.row(), 0).text()
        item.server = server
        self.show_server.setText(server)
        # 立刻刷新价格显示的界面
        if item.name is not None and self.show_data_box.currentIndex() != 0:
            logger.info("通过点击全服比价重新选择了服务器为{}，开始进行{}价格查询".format(item.server, item.name))
            item.price_cache = {}
            self.query_price()

    def click_select_server(self, server):
        """
        菜单栏选择服务器重新查询的事件
        """
        # 修改界面上显示的当前服务器
        self.show_server.setText(server)
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
        # 立刻刷新价格显示的界面
        if item.name is not None and self.show_data_box.currentIndex() != 0:
            logger.info("重新选择了服务器为{}，开始进行{}价格查询".format(item.server, item.name))
            item.price_cache = {}
            self.query_price()

    def query_item_action(self):
        """
        模糊搜索查询物品
        """
        global query_history
        input_name = query_item_page.input_item_name.text()
        # 如果与上一次查询结果一致，那么直接使用上次查询的列表
        if {"itemName": input_name} == query_history[-1]['itemName'] and len(
                item.item_list) > 1 and first_query is False:
            logger.info("与上次查询结果一致，切换到物品选择页面")
            self.show_data_box.setCurrentIndex(1)
        elif input_name == query_history[-1]['itemName'] and item.hq == query_history[-1]['HQ'] \
                and item.server == query_history[-1]['server'] and len(item.item_list) == 1 and first_query is False:
            logger.info("与上次查询结果一致，切换到价格显示页面")
            self.item_icon.show()
            self.jump_to_wiki.show()
            self.show_cost.show()
            self.back_query.show()
            self.show_data_box.setCurrentIndex(2)
        else:
            logger.info("开始查找道具 {}".format(input_name))
            item.query_item_id(input_name)
            # 查询到的道具数量大于1
            if len(item.item_list) > 1:
                logger.info("查询到多个道具，开始渲染物品选择界面")
                # 绘制表格，让玩家选择道具
                r = 0
                # 绘制前 清空上次查询结果
                select_item_page.items_list_widget.clearContents()
                # 设置表格样式
                select_item_page.items_list_widget.horizontalHeader().setSectionResizeMode(
                    QtWidgets.QHeaderView.Stretch)
                select_item_page.items_list_widget.horizontalHeader().setSectionResizeMode(0,
                                                                                           QtWidgets.QHeaderView.Fixed)
                select_item_page.items_list_widget.setColumnWidth(0, 120)
                select_item_page.items_list_widget.setRowCount(len(item.item_list))
                logger.debug("表格填充数据")
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
                self.show_data_box.setCurrentIndex(1)
            # 只查询到一个道具
            elif len(item.item_list) == 1:
                logger.info("查询到一个道具，准备进行网络测试")
                item.id = item.item_list[0]['id']
                item.name = item.item_list[0]['name']
                self.test_network()
            # 查询不到道具
            else:
                logger.warning("查询不到道具")
                ui.show_message()

    def make_cost_tree(self):
        """
        成本树，显示这个物品的制作材料和成本
        """
        global show_query_item

        def start_tree(stuff):
            global query_check
            for i in stuff:
                make_tree(i, cost_page.cost_tree)
            self.show_cost.setText('市场价格')
            show_query_item.quit()
            self.item_icon.show()
            self.jump_to_wiki.show()
            self.show_cost.show()
            self.back_query.show()
            self.query_history.show()
            self.show_data_box.setCurrentIndex(3)
            query_check = False

        def make_tree(material, father):
            """
            材料树的绘制方法
            """
            node = QtWidgets.QTreeWidgetItem(father)
            
            # 处理特殊提示材料（不可制造的物品）
            if material.get('name') == '该物品不能被制作':
                node.setText(0, '该物品不能被制作')
                node.setText(1, 'N/A')
                node.setText(2, 'N/A')
                node.setText(3, 'N/A')
                node.setText(4, 'N/A')
                return
            
            # 正常材料处理
            node.setText(0, material.get('name', '未知材料'))
            node.setText(1, str(material.get('pricePerUnit', 'N/A')))
            node.setText(2, str(material.get('amount', 'N/A')))
            node.setText(3, str(material.get('priceTotal', 'N/A')))
            node.setText(4, str(material.get('lowestPriceServer', 'N/A')))
            
            if 'craft' in material:
                for i in material['craft']:
                    make_tree(i, node)

        global query_check
        if self.show_data_box.currentIndex() == 3:
            self.show_cost.setText('成本计算')
            self.show_data_box.setCurrentIndex(2)
        elif self.show_data_box.currentIndex() == 2 and len(item.stuff) > 0:
            logger.debug("材料树中有内容，判断已经查询过材料树，切换界面")
            self.show_cost.setText('市场价格')
            self.show_data_box.setCurrentIndex(3)
        elif len(item.stuff) == 0:
            logger.debug("材料树是空的，切换到查询中界面，开始查询")
            query_check = True
            self.show_data_box.setCurrentIndex(4)
            show_item_cost = ShowItemCost()
            show_item_cost.sinout.connect(start_tree)
            logger.info("开始绘制材料树")
            cost_page.cost_tree.clear()
            logger.debug("开始运行材料树线程")
            show_item_cost.start()
            logger.debug("开始载入界面线程")
            show_query_item.sinout.connect(ui.show_item)
            show_query_item.start()
            show_item_cost.exec()

    def click_query_item_name(self, selected):
        # 点击材料树的条目将道具名复制到剪贴板
        if selected.text(0) != '该物品不能被制作':
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(selected.text(0))
            item.name = selected.text(0)
            logger.info("材料名称 {} 已经复制到粘贴板".format(item.name))
            for i in item.item_data.values():
                if i['name'] == item.name:
                    item.id = i['id']
            query_item_page.input_item_name.setText(item.name)
            item.item_list = []
            logger.info("通过点击材料树重新查询材料 {}".format(item.name))
            self.query_price()
        else:
            self.back_to_index()

    def query_sale_list(self, price_list):
        """
        界面动作:售出列表填充
        """
        hq_icon = QtGui.QIcon(os.path.join("Data", "hq.png"))
        # 查询正在售出的记录
        logger.info("物品的售出价格查询完毕，开始绘制价格表格")
        # 更新界面的部分数据
        self.show_update_time.setText(item.timestamp_to_time(price_list["lastUploadTime"]))
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
        logger.debug("为价格表格填充数据")
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
        self.jump_to_wiki.show()
        self.show_cost.show()
        self.back_query.show()
        self.query_history.show()
        self.show_cost.setText('成本计算')
        self.show_data_box.setCurrentIndex(2)

    def query_price(self):
        """
        价格查询动作
        """
        global query_history
        global server_list
        global first_query
        # 设置wiki链接
        first_query = False
        self.jump_to_wiki.setText(
            '''
            <a href="https://ff14.huijiwiki.com/wiki/%E7%89%A9%E5%93%81:{}">灰机wiki</a> 
            | 
            <a href="https://garlandtools.cn/db/#item/{}">花环</a>
            '''.format(item.name, item.id))
        widget.setWindowTitle("猴面雀 - FF14市场查询工具 - " + item.name)
        logger.info("开始查询{}的{}".format(item.server, item.name))
        loading_page.loading_text.setText("猴面雀正在为您查找资料。")
        self.show_data_box.setCurrentIndex(4)
        query_item_price = QueryItemPrice()
        query_item_price.sinout.connect(ui.query_sale_list)
        query_item_price.start()
        get_item_icon = GetItemIcon()
        get_item_icon.sinout.connect(self.show_item_icon)
        get_item_icon.start()
        # 如果玩家选择了不在同一个大区的服务器，或者查询其他物品，就重新查询全服比价的数据
        if server_list != item.server_list() or item.id != query_history[-1]['itemID']:
            server_list = item.server_list()
            logger.info('查询区域为{}， 服务器列表初始化为{}'.format(item.world, server_list))
            # 查询全服比价的数据
            iquery_every_server = QueryEveryServer(server_list)
            iquery_every_server.sinout.connect(self.query_every_server)
            iquery_every_server.start()
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
        logger.debug("查询历史更新完毕")
        query_item_page.query_is_hq.setChecked(item.hq)
        cost_page.cost_tree.clear()
        get_item_icon.exec()
        query_item_price.exec()

    def click_history_query(self, selected):
        """
        通过点击历史面板查询物品
        """
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
                self.show_server.setText('日服')
            elif item.server == 'Europe':
                self.show_server.setText('欧服')
            elif item.server == 'North-America':
                self.show_server.setText('美服')
            elif item.server == 'Oceania':
                self.show_server.setText("太平洋服")
            elif item.server == "China":
                self.show_server.setText("国服")
            else:
                self.show_server.setText(item.server)
            logger.info("通过点击历史面板进行查询 {} 的 {}".format(item.server, item_name))
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
            self.test_network()

    @staticmethod
    def click_copy_cost_tree():
        # 点击材料树的按钮将整个材料树复制到剪贴板
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(item.clipboard)

    @staticmethod
    def select_hq_ornot(status):
        """
        查询HQ的CheckButton
        """
        item.hq = status

    @staticmethod
    def use_static_file_or_not(status):
        """
        是否启用静态资源加速
        """
        item.static = status

    @staticmethod
    def filter_item_or_not(status):
        """
        过滤不可在市场上交易的物品
        """
        item.filter_item = status

    def show_item_icon(self, icon):
        """
        绘制物品图标的方法
        """
        self.item_icon.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage.fromData(icon)))
        self.item_icon.setScaledContents(True)
        self.item_icon.show()

    @staticmethod
    def show_item(item_name):
        loading_page.loading_text.setText("猴面雀正在 universalis 上为您查询 {} 的价格，请稍等一下。。。".format(item_name))

    def back_to_index(self):
        """
        返回首页的按钮事件
        """
        self.item_icon.hide()
        self.jump_to_wiki.hide()
        self.show_cost.hide()
        self.back_query.hide()
        self.show_data_box.setCurrentIndex(0)

    def show_message(self):
        """
        首页查询不到物品的提示
        """
        self.show_data_box.setCurrentIndex(0)
        QtWidgets.QMessageBox.warning(self.query_item, "物品名称错误", "查询不到任何物品")

    @staticmethod
    def hidden_history_board():
        """
        显示或者隐藏查询历史面板
        """
        if widget2.isVisible():
            widget2.hide()
        elif widget2.isHidden():
            widget2.show()

    @staticmethod
    def show_check_update_window():
        """
        显示或者隐藏关于面板，包含检查更新的事件
        """
        # 如果没有查询过版本，就开始一次版本检查
        if check_update_window.latest_program_version.text() == 'N/A':
            version_online = item.get_online_version()
            check_update_window.latest_program_version.setText(str(version_online['program']))
            check_update_window.latest_data_version.setText(str(version_online['data']))
        c_p_v = check_update_window.current_program_version.text()
        c_d_v = check_update_window.current_data_verison.text()
        l_p_v = check_update_window.latest_program_version.text()
        l_d_v = check_update_window.latest_data_version.text()
        # 数据文件可以单独更新
        if c_p_v == l_p_v and c_d_v == l_d_v:
            check_update_window.update_text.hide()
        else:
            check_update_window.update_text.setText('有新版本可用，请重新启动猴面雀，若多次重启不能更新，请隔段时间再试。')
        # 面板隐藏或者显示
        if widget3.isVisible():
            widget3.hide()
        elif widget3.isHidden():
            widget3.show()


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


class QueryItemPrice(QtCore.QThread):
    sinout = QtCore.pyqtSignal(dict)

    def __init__(self):
        super(QueryItemPrice, self).__init__()

    def run(self):
        # 发出信号
        self.sinout.emit(item.query_item_price())


class QueryEveryServer(QtCore.QThread):
    sinout = QtCore.pyqtSignal(list)

    def __init__(self, server_list):
        super(QueryEveryServer, self).__init__()
        self.server_list = server_list

    def run(self):
        # 发出信号
        item.query_every_server(server_list)
        self.sinout.emit(item.every_server)


class ShowItemCost(QtCore.QThread):
    sinout = QtCore.pyqtSignal(list)

    def __init__(self):
        super(ShowItemCost, self).__init__()

    def run(self):
        logger.info("开始查询材料的成本价格")
        item.show_item_cost()
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
        logger.info("材料树计算完成")
        self.sinout.emit(item.stuff['craft'])


class ShowQueryItem(QtCore.QThread):
    sinout = QtCore.pyqtSignal(str)

    def __init__(self):
        super(ShowQueryItem, self).__init__()

    def run(self):
        global query_check
        logger.debug("面板切换显示当前查询材料")
        while query_check:
            time.sleep(0.3)
            self.sinout.emit(item.cq)


class GetItemIcon(QtCore.QThread):
    sinout = QtCore.pyqtSignal(bytes)

    def __init__(self):
        super(GetItemIcon, self).__init__()

    def run(self):
        logger.debug("请求物品图标")
        item.get_icon()
        # self.sinout.emit(QtGui.QPixmap.fromImage(QtGui.QImage.fromData(item.icon)))
        try:
            self.sinout.emit(item.icon)
        except TypeError:
            logger.error("图标请求失败")


"""
公共数据部分
"""
logger.info("主程序启动，开始处理公共数据")
# 与 Data/version 文件中的版本对应
program_version = '1.0.65'
# 加载查询历史
history_file = os.path.join('Data', "Paissa_query_history.log")
try:
    with open(history_file, 'r', encoding='utf-8') as his:
        history_json = json.load(his)
        query_history = history_json['history']
        # 如果使用者点开过软件，却没有查询道具，会生成空查询记录的历史文件。
        # 加入None条目，后面的切换界面判断方法就不用判空了
        if len(query_history) == 0:
            query_history = [{"itemID": None, "itemName": None, "HQ": None, "server": 'None'}]
        item = Queryer(history_json['server'])
        logger.info("读取查询历史成功")
except FileNotFoundError:
    history_json = {"server": '猫小胖', 'use_static': True, "history": []}
    query_history = [{"itemID": None, "itemName": None, "HQ": None, "server": None}]
    item = Queryer('猫小胖')
    logger.warning("没有发现历史数据，初始化历史数据")
except KeyError:
    with open(history_file, 'r', encoding='utf-8') as his:
        history_json = json.load(his)
        query_history = history_json['history']
        if len(query_history) == 0:
            query_history = [{"itemID": None, "itemName": None, "HQ": None, "server": 'None'}]
    item = Queryer(history_json['server'])
    logger.info("读取查询历史成功")

# 加载本地静态文件
with open('Data/item.Pdt', 'r', encoding='utf8') as item_list_file:
    item.item_data = json.load(item_list_file)
date_version = item.item_data['data-version']
item.header = {'User-Agent': 'Paissa {}'.format(program_version)}
logger.info("数据文件加载完毕")
if 'use_static' not in history_json:
    history_json['use_static'] = True
item.static = history_json['use_static']
logger.info(f"静态数据加速：{item.static}")
item.item_data.pop('data-version')
first_query = True
server_list = []
query_check = False
logger.info("主程序数据初始化完成")

"""
主程序开始
"""
app = QtWidgets.QApplication(sys.argv)
desktop = app.primaryScreen().size()
logger.debug("获取到桌面大小为{} * {}".format(desktop.width(), desktop.height()))
app.setStyle("Fusion")
widget = RQMainWindow()
ui = MainWindow()
ui.setupUi(widget)
widget.resize(int(desktop.width() * 0.6), int(desktop.height() * 0.6))
ui.setup_menu()
ui.jump_to_wiki.setOpenExternalLinks(True)
ui.show_server.setText(item.server)
ui.item_icon.hide()
ui.jump_to_wiki.hide()
ui.show_cost.hide()
ui.back_query.hide()
ui.query_history.show()
ui.back_query.clicked.connect(ui.back_to_index)
ui.show_data_box.setCurrentIndex(0)
ui.query_history.clicked.connect(ui.hidden_history_board)
ui.show_cost.clicked.connect(ui.make_cost_tree)
ui.use_static_file.setChecked(history_json['use_static'])
widget.show()

"""
物品查询首页
"""
query_item_page = QueryItemId()
query_item_page.setupUi(ui.query_item)
query_item_page.query_button.clicked.connect(ui.query_item_action)
query_item_page.input_item_name.returnPressed.connect(ui.query_item_action)
query_item_page.query_is_hq.clicked.connect(ui.select_hq_ornot)

"""
模糊搜索时选择物品的界面
"""
select_item_page = SelectItemList()
select_item_page.setupUi(ui.select_item)
select_item_page.back.clicked.connect(lambda: ui.show_data_box.setCurrentIndex(0))
select_item_page.items_list_widget.doubleClicked.connect(ui.select_item_action)
# 在选择物品界面选中物品后点击“选择物品”的按钮，把选中行作为对象传给价格查询模块
select_item_page.select_this.clicked.connect(lambda: ui.select_item_action(select_item_page.items_list_widget.selectedItems()))

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
cost_page.cost_tree.itemDoubleClicked.connect(ui.click_query_item_name)
cost_page.click_c.clicked.connect(ui.click_copy_cost_tree)
show_query_item = ShowQueryItem()

"""
loading界面
"""
loading_page = LoadingPage()
loading_page.setupUi(ui.loading_ui)
loading_page.loading_text.setText("猴面雀正在为您查找资料。")

"""
查询历史面板
"""
widget2 = QtWidgets.QMainWindow()
history_board = HistoryPage()
history_board.setupUi(widget2)
widget2.resize(int(desktop.width() * 0.15), int(desktop.height() * 0.6))
widget2.setMaximumSize(QtCore.QSize(int(desktop.width() * 0.3), int(desktop.height() * 0.6)))
history_board.history_list.doubleClicked.connect(ui.click_history_query)
try:
    for i in query_history:
        if i['HQ'] is not True and i["itemName"] != 'None':
            history_board.history_list.insertItem(0, i["itemName"] + ' - ' + i['server'])
        elif i['HQ'] is True and i["itemName"] != 'None':
            history_board.history_list.insertItem(0, i["itemName"] + 'HQ' + ' - ' + i['server'])
except:
    pass

"""
check update
"""
widget3 = QtWidgets.QMainWindow()
check_update_window = CheckUpdate()
check_update_window.setupUi(widget3)
# 关于面板的超链接激活
check_update_window.label_8.setOpenExternalLinks(True)
check_update_window.current_program_version.setText(program_version)
check_update_window.current_data_verison.setText(str(date_version))

sys.exit(app.exec_())
