
from PyQt5 import QtCore, QtGui, QtWidgets, uic

class View(QtWidgets.QMainWindow):

    def __init__(self):
        super(View, self).__init__()
        self.view = uic.loadUi('player.ui', self)

        self.view.actionOpen_File.triggered.connect(self.openFile)
        self.view.pushButtonPlay.clicked.connect(self.playPresed)

        self.view.listAll_Songs.itemDoubleClicked.connect(self.openFile)

        self.show()

    def openFile(self):
        print(self.view.listAll_Songs.currentItem().text())
        self.view.listAll_Songs.addItem('suh')

    def playPresed(self):
        self.view.listAll_Songs.addItem('hello')
