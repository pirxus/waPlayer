from PyQt5 import QtCore, uic, QtWidgets
from PyQt5.QtWidgets import QPushButton, QMenu
from PyQt5.QtGui import QPixmap

class View(QtWidgets.QMainWindow):

    def __init__(self):
        super(View, self).__init__()
        self.view = uic.loadUi('player.ui', self)
        self.view.labelPlayerAlbumArt.setPixmap(QPixmap('../assets/stock_album_cover.jpg'))
        self.show()

    def addControls(self):
        self.button = QtWidgets.QPushButton(self)
        self.button.setText('suh')
        self.button.move(50, 40)
        self.button.show()

    #def contextMenuEvent(self, event):
    #    self.view.contextMenuSongSelection = QMenu(self)
    #    playSongs = self.view.contextMenuSongSelection.addAction("Add to queue...")
    #    addToQueue = self.view.contextMenuSongSelection.addAction("Add to queue...")

    #    action = self.view.contextMenuSongSelection.exec_(self.view.mapToGlobal(event.pos()))

