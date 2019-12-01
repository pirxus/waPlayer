
from PyQt5 import QtCore, QtGui, QtWidgets, uic

class View(QtWidgets.QMainWindow):

    def __init__(self):
        super(View, self).__init__()
        self.view = uic.loadUi('player.ui', self)
        self.show()
