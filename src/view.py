from PyQt5 import QtCore, uic, QtWidgets

from PyQt5.QtWidgets import QPushButton, QMenu, QFrame, QTableWidget, QFrame, QWidget, QVBoxLayout, QLabel, QListView, QListWidget, QListWidgetItem, QTableWidgetItem, QHeaderView, QAbstractItemView

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from clickable_label import QLabelClickable, QLabelClickableWithParent

class View(QtWidgets.QMainWindow):

    def __init__(self):
        super(View, self).__init__()
        self.view = uic.loadUi('player.ui', self)
        self.dialog = uic.loadUi('new_playlist.ui')
        self.view.labelPlayerAlbumArt.setPixmap(QPixmap('../assets/stock_album_cover.jpg'))
        self.createAlbumView()
        self.createPlaylistView()
        self.adjustWidgets()
        self.show()

    def adjustWidgets(self):
        self.view.tableAllSongs.setColumnWidth(0, 265)
        self.view.tableAllSongs.setColumnWidth(1, 75)
        self.view.tableAlbumContent.setColumnWidth(0, 350)
        self.view.labelPlayerSongName.setStyleSheet("font-weight: bold;")

    def createAlbumView(self):
            #cover of album
            self.view.albumCover = QLabelClickableWithParent('', self.view.tabAlbums)
            self.view.albumCover.setMaximumWidth(140)
            self.view.albumCover.setMinimumWidth(140)
            self.view.albumCover.setMaximumHeight(140)
            self.view.albumCover.setMinimumHeight(140)
            self.view.albumCover.setScaledContents(True)
            self.view.albumCover.setStyleSheet('border: 2px solid black;')
            self.view.albumCover.move(5, 70)

            # album year
            self.view.albumYear = QLabel(self.view.tabAlbums)
            self.view.albumYear.move(5, 50)
            self.view.albumYear.setMaximumWidth(140)
            self.view.albumYear.setMinimumWidth(140)
            self.view.albumYear.setWordWrap(True)
            self.view.albumYear.setAlignment(Qt.AlignHCenter)

            # album name
            self.view.albumName = QLabel(self.view.tabAlbums)
            self.view.albumName.move(5, 213)
            self.view.albumName.setMaximumWidth(140)
            self.view.albumName.setMinimumWidth(140)
            self.view.albumName.setMaximumHeight(200)
            self.view.albumName.setMinimumHeight(200)
            self.view.albumName.setWordWrap(True)
            self.view.albumName.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            self.view.albumName.setStyleSheet("font-weight: bold;")

            # artist name TODO
            #self.view.artistName = QLabel(self.view.tabAlbums)
            #self.view.artistName.move(5, 213)
            #self.view.artistName.setMaximumWidth(140)
            #self.view.artistName.setMinimumWidth(140)
            #self.view.artistName.setMaximumHeight(200)
            #self.view.artistName.setMinimumHeight(200)
            #self.view.artistName.setWordWrap(True)
            #self.view.artistName.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

            #back button
            self.view.albumsButton = QPushButton(self.view.tabAlbums)
            self.view.albumsButton.setFocusPolicy(Qt.NoFocus)
            self.view.albumsButton.setText('<< Back')
            self.view.albumsButton.setMinimumWidth(70)
            self.view.albumsButton.setMinimumHeight(30)
            self.view.albumsButton.move(40, 5)

            #songs list
            self.view.albumSongs.setColumnWidth(0, 350)
            self.view.albumSongs.setColumnWidth(1, 90)

            self.view.albumSongs.hide()
            self.view.albumsButton.hide()
            self.view.albumName.hide()
            self.view.albumCover.hide()

    def createPlaylistView(self):
        # cover of album
        self.view.playlistCover = QLabelClickableWithParent('', self.view.tab_playlists)
        self.view.playlistCover.setMaximumWidth(140)
        self.view.playlistCover.setMinimumWidth(140)
        self.view.playlistCover.setMaximumHeight(140)
        self.view.playlistCover.setMinimumHeight(140)
        self.view.playlistCover.setScaledContents(True)
        self.view.playlistCover.setStyleSheet('border: 2px solid black;')
        self.view.playlistCover.move(5, 70)

        # album year
        #self.view.albumYear = QLabel(self.view.tab_playlists)
        #self.view.albumYear.move(5, 50)
        #self.view.albumYear.setMaximumWidth(140)
        #self.view.albumYear.setMinimumWidth(140)
        #self.view.albumYear.setWordWrap(True)
        #self.view.albumYear.setAlignment(Qt.AlignHCenter)

        # album name
        self.view.playlistName = QLabel(self.view.tab_playlists)
        self.view.playlistName.move(5, 213)
        self.view.playlistName.setMaximumWidth(140)
        self.view.playlistName.setMinimumWidth(140)
        self.view.playlistName.setMaximumHeight(200)
        self.view.playlistName.setMinimumHeight(200)
        self.view.playlistName.setWordWrap(True)
        self.view.playlistName.setStyleSheet("font-weight: bold;")
        self.view.playlistName.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # artist name TODO
        # self.view.artistName = QLabel(self.view.tabAlbums)
        # self.view.artistName.move(5, 213)
        # self.view.artistName.setMaximumWidth(140)
        # self.view.artistName.setMinimumWidth(140)
        # self.view.artistName.setMaximumHeight(200)
        # self.view.artistName.setMinimumHeight(200)
        # self.view.artistName.setWordWrap(True)
        # self.view.artistName.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # back button
        self.view.playlistButton = QPushButton(self.view.tab_playlists)
        self.view.playlistButton.setFocusPolicy(Qt.NoFocus)
        self.view.playlistButton.setText('<< Back')
        self.view.playlistButton.setMinimumWidth(70)
        self.view.playlistButton.setMinimumHeight(30)
        self.view.playlistButton.move(40, 5)

        # songs list
        self.view.playlistSongs.setColumnWidth(0, 200)
        self.view.playlistSongs.setColumnWidth(1, 150)
        self.view.playlistSongs.setColumnWidth(2, 90)

        self.view.playlistSongs.hide()
        self.view.playlistButton.hide()
        self.view.playlistName.hide()
        self.view.playlistCover.hide()


    def goBackAlbum(self):
        self.view.albumSongs.hide()
        self.view.albumsButton.hide()
        self.view.albumName.hide()
        self.view.albumCover.hide()
        self.view.albumYear.hide()
        self.view.scrollAreaAlbums.show()

    def goBackAlbumTab(self, index):
        if self.tabLibrary.currentIndex() == index:
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

    def createPlaylistDialog(self):
        self.dialog.lineEditNewPlaylist.clear()
        self.dialog.show()

    def openPlaylist(self):
        self.view.scrollAreaPlaylists.hide()
        self.view.playlistSongs.show()
        self.view.playlistButton.show()
        self.view.playlistName.show()
        self.view.playlistCover.show()

    def goBackPlaylist(self):
        self.view.playlistSongs.hide()
        self.view.playlistButton.hide()
        self.view.playlistName.hide()
        self.view.playlistCover.hide()
        self.view.albumYear.hide()
        self.view.scrollAreaPlaylists.show()