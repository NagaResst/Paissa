from Paissa import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

# class MainWindow(Ui_MainWindow):




app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(widget)
widget.show()
sys.exit(app.exec_())

