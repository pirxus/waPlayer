from PyQt5 import QtCore, uic, QtWidgets

from PyQt5.QtWidgets import QPushButton, QMenu, QFrame, QTableWidget, QFrame, QWidget, QVBoxLayout, QLabel, QListView, QListWidget, QListWidgetItem, QTableWidgetItem, QHeaderView, QAbstractItemView

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from clickable_label import QLabelClickable, QLabelClickableWithParent

class View(QtWidgets.QMainWindow):

    def __init__(self):
        super(View, self).__init__()
        self.view = uic.loadUi('player.ui', self)
        self.view.labelPlayerAlbumArt.setPixmap(QPixmap('../assets/stock_album_cover.jpg'))
        self.createAlbumView()
        self.adjustWidgets()
        self.show()

    def adjustWidgets(self):
        self.view.tableAllSongs.setColumnWidth(0, 265)
        self.view.tableAllSongs.setColumnWidth(1, 75)
        self.view.tableAlbumContent.setColumnWidth(0, 350)

    def createAlbumView(self):
            #cover of album
            self.view.albumCover = QLabelClickableWithParent('', self.view.tabAlbums)
            self.view.albumCover.setMaximumWidth(140)
            self.view.albumCover.setMinimumWidth(140)
            self.view.albumCover.setMaximumHeight(140)
            self.view.albumCover.setMinimumHeight(140)
            self.view.albumCover.setScaledContents(True)
            self.view.albumCover.setStyleSheet('border: 2px solid black;')
            self.view.albumCover.move(5, 40)

            # album year
            self.view.albumYear = QLabel(self.view.tabAlbums)
            self.view.albumYear.move(5, 190)
            self.view.albumYear.setMaximumWidth(140)
            self.view.albumYear.setMinimumWidth(140)
            self.view.albumYear.setWordWrap(True)
            self.view.albumYear.setAlignment(Qt.AlignHCenter)

            # album name
            self.view.albumName = QLabel(self.view.tabAlbums)
            self.view.albumName.move(5, 213)
            self.view.albumName.setMaximumWidth(140)
            self.view.albumName.setMinimumWidth(140)
            self.view.albumName.setWordWrap(True)
            self.view.albumName.setAlignment(Qt.AlignHCenter)

            #back button
            self.view.albumsButton = QPushButton(self.view.tabAlbums)
            self.view.albumsButton.setFocusPolicy(Qt.NoFocus)
            self.view.albumsButton.setText('<< Back')
            self.view.albumsButton.setMinimumWidth(70)
            self.view.albumsButton.setMinimumHeight(30)
            self.view.albumsButton.move(45, 5)

            #songs list
            self.view.albumSongs.setColumnWidth(0, 350)
            self.view.albumSongs.setColumnWidth(1, 90)

            self.view.albumSongs.hide()
            self.view.albumsButton.hide()
            self.view.albumName.hide()
            self.view.albumCover.hide()

    def goBackAlbum(self):
        self.view.albumSongs.hide()
        self.view.albumsButton.hide()
        self.view.albumName.hide()
        self.view.albumCover.hide()
        self.view.albumYear.hide()
        self.view.scrollAreaAlbums.show()

    def openAlbum(self):
        self.view.scrollAreaAlbums.hide()
        self.view.albumSongs.show()
        self.view.albumsButton.show()
        self.view.albumName.show()
        self.view.albumCover.show()
        self.view.albumYear.show()
