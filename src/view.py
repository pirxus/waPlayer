from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap

class View(QtWidgets.QMainWindow):

    def __init__(self):
        super(View, self).__init__()
        self.view = uic.loadUi('player.ui', self)
        self.view.label.setPixmap(QPixmap('../assets/stock_album_cover.jpg'))
        self.show()

    def addControls(self):
        self.button = QtWidgets.QPushButton(self)
        self.button.setText('suh')
        self.button.move(50, 40)
        self.button.show()


