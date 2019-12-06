from PyQt5 import QtCore, uic, QtWidgets, sip

from PyQt5.QtWidgets import QPushButton, QMenu, QFrame, QTableWidget, QFrame, QWidget, QVBoxLayout, QLabel, QListView, QListWidget, QListWidgetItem, QTableWidgetItem, QHeaderView, QAbstractItemView

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from clickable_label import QLabelClickable, QLabelClickableWithParent

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

    def createAlbumView(self, songs):
            #frame that overwrites albums preview
            self.view.albumView = QFrame(self.view.tab_albums)
            self.view.albumView.setMaximumHeight(412)
            self.view.albumView.setMinimumHeight(412)
            self.view.albumView.setMaximumWidth(641)
            self.view.albumView.setMinimumWidth(641)
            self.view.albumView.setStyleSheet("background-color: #ffffff")

            #cover of album
            self.view.albumCover = QLabelClickableWithParent(songs[0]['album'], self.view.albumView)
            self.view.albumCover.setMaximumWidth(140)
            self.view.albumCover.setMinimumWidth(140)
            self.view.albumCover.setMaximumHeight(140)
            self.view.albumCover.setMinimumHeight(140)
            self.view.albumCover.setScaledContents(True)
            self.view.albumCover.setStyleSheet('border: 2px solid black;')
            self.view.albumCover.move(5, 40)

            # album year
            self.view.albumName = QLabel(self.view.albumView)
            self.view.albumName.move(5, 190)
            self.view.albumName.setMaximumWidth(140)
            self.view.albumName.setMinimumWidth(140)
            self.view.albumName.setWordWrap(True)
            self.view.albumName.setText(str(songs[0]['year']['_year']))
            self.view.albumName.setAlignment(Qt.AlignHCenter)

            # album name
            self.view.albumName = QLabel(self.view.albumView)
            self.view.albumName.move(5, 213)
            self.view.albumName.setMaximumWidth(140)
            self.view.albumName.setMinimumWidth(140)
            self.view.albumName.setWordWrap(True)
            self.view.albumName.setText(songs[0]['album'])
            self.view.albumName.setAlignment(Qt.AlignHCenter)

            #back button
            self.view.albumsButton = QPushButton(self.view.albumView)
            self.view.albumsButton.setStyleSheet('background-color: rgb(173, 127, 168);')
            self.view.albumsButton.setText('back')
            self.view.albumsButton.setMinimumWidth(60)
            self.view.albumsButton.setMinimumHeight(30)
            self.view.albumsButton.move(50, 5)

            #songs list
            self.view.albumSongs = QTableWidget(self.view.albumView)
            self.view.albumSongs.move(150, -2)
            self.view.albumSongs.setMinimumHeight(405)
            self.view.albumSongs.setMinimumWidth(487)
            self.view.albumSongs.setMaximumWidth(487)

            self.view.albumSongs.setShowGrid(False)
            self.view.albumSongs.setFocusPolicy(Qt.NoFocus)
            self.view.albumSongs.setEditTriggers(QAbstractItemView.NoEditTriggers)

            self.view.albumSongs.setColumnCount(2)
            self.view.albumSongs.horizontalHeader().setSortIndicatorShown(False)
            self.view.albumSongs.horizontalHeader().setStretchLastSection(True)
            self.view.albumSongs.horizontalHeader().setVisible(False)
            self.view.albumSongs.verticalHeader().setVisible(False)
            self.view.albumSongs.setColumnWidth(0, 350)
            self.view.albumSongs.setColumnWidth(1, 90)
            self.view.albumSongs.setSelectionBehavior(QAbstractItemView.SelectRows)

            self.view.albumView.show()

    def goBackAlbum(self):
        sip.delete(self.view.albumView)
