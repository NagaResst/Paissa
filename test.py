"""
Date:2021/4/21 14:49
Author :四翼妄为
"""
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QHBoxLayout, QGridLayout, QPushButton, QVBoxLayout, QListWidget, QStackedLayout)
from PyQt5.QtGui import QPalette, QColor
from PyQt5 import QtWidgets


class One(QWidget):
    def __init__(self):
        super(One, self).__init__()
        self.create_ui()

    def create_ui(self):
        box = QHBoxLayout(self)

        left_box = QVBoxLayout()
        list_v = QListWidget(self)  # 列表框控件用来加载并显示多个列表项
        list_v.addItems(['释义', '例句'])  # 添加文字选项
        list_v.setCurrentRow(0)  # 设置默认选中
        list_v.currentItemChanged.connect(self.item_change)  # 关联切换事件
        left_box.addWidget(list_v)

        self.right_box = QStackedLayout()
        l1 = QLabel('释义的界面', self)
        l2 = QLabel('例句的界面', self)
        self.right_box.addWidget(l1)
        self.right_box.addWidget(l2)

        box.addLayout(left_box, 1)
        box.addLayout(self.right_box, 3)

    def item_change(self, value: QtWidgets.QListWidgetItem):
        print('改变', value.text())
        if value.text() == '释义':
            self.right_box.setCurrentIndex(0)
        else:
            self.right_box.setCurrentIndex(1)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.create_ui()

        self.setGeometry(200, 100, 800, 600)
        self.setWindowTitle('图书管理系统')
        self.show()

    def btn1_action(self):
        self.bottom_box.setCurrentIndex(0)

    def btn2_action(self):
        self.bottom_box.setCurrentIndex(1)

    def btn3_action(self):
        self.bottom_box.setCurrentIndex(2)

    def create_ui(self):
        box = QVBoxLayout(self)  # 整体的盒子必关联self呀，不然后边没法玩了

        # 1.顶部视图
        top_box = QHBoxLayout()
        btn1 = QPushButton('页面一', self)
        btn2 = QPushButton('页面二', self)
        btn3 = QPushButton('页面三', self)

        top_box.addWidget(btn1)
        top_box.addWidget(btn2)
        top_box.addWidget(btn3)

        btn1.clicked.connect(self.btn1_action)
        btn2.clicked.connect(self.btn2_action)
        btn3.clicked.connect(self.btn3_action)

        # 底部视图
        self.bottom_box = QStackedLayout()
        page1 = One()
        page2 = QLabel('页面二', self)
        page3 = QLabel('页面三', self)

        self.bottom_box.addWidget(page1)
        self.bottom_box.addWidget(page2)
        self.bottom_box.addWidget(page3)

        box.addLayout(top_box)
        box.addLayout(self.bottom_box)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

