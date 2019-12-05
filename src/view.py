from PyQt5 import QtCore, uic, QtWidgets, sip
from PyQt5.QtWidgets import QPushButton, QMenu, QTableWidget, QFrame, QWidget, QVBoxLayout, QLabel, QListView, \
    QListWidget, QListWidgetItem, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
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

    def createAlbumView(self):
        #frame that overwrites albums preview
        self.view.albumView = QFrame(self.view.tab_albums)
        self.view.albumView.setMaximumHeight(412)
        self.view.albumView.setMinimumHeight(412)
        self.view.albumView.setMaximumWidth(641)
        self.view.albumView.setMinimumWidth(641)
        self.view.albumView.setStyleSheet("background-color: #ffffff")

        #cover of album
        self.view.albumCover = QLabel(self.view.albumView)
        self.view.albumCover.setScaledContents(True)
        self.view.albumCover.setPixmap(QPixmap('../assets/cover.jpg').scaled(141, 141, Qt.KeepAspectRatio, Qt.FastTransformation))
        self.view.albumCover.setStyleSheet('padding: 40px 0px 0px 0px')
        self.view.albumCover.move(5, 0)

        #back button
        self.view.albumsButton = QPushButton(self.view.albumView)
        self.view.albumsButton.setStyleSheet('background-color: rgb(173, 127, 168);')
        self.view.albumsButton.setText('back')
        self.view.albumsButton.setMinimumWidth(60)
        self.view.albumsButton.setMinimumHeight(30)
        self.view.albumsButton.move(40, 5)

        self.view.albumSongs = QTableWidget(self.view.albumView)
        self.view.albumSongs.move(150, 0)
        self.view.albumSongs.setMinimumHeight(412)
        self.view.albumSongs.setMinimumWidth(490)

        for i in range(100):
            song = QTableWidgetItem()
            song.setText("FUCK YEAH" + str(i))
            self.view.albumSongs.setItem(i, 0, song)


        self.view.albumView.show()
