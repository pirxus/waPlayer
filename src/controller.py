from database import Database
from view import View
from PyQt5.QtCore import QUrl, QDirIterator, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QFileDialog, QAction, QHBoxLayout, QVBoxLayout, QSlider
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent

class Controller(QWidget):

    def __init__(self):
        super().__init__()
        self.view = View()
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.database = Database()
        self.linkView()


        self.playerState = -1 # 0 - stopped, 1 - playing, 2 - paused

    # This method sets up the connections between the ui and the backend
    def linkView(self):
        self.view.actionOpen_File.triggered.connect(self.openFile)
        self.view.pushButtonPlay.clicked.connect(self.playPauseHandlerg)
        self.view.sliderVolume.valueChanged[int].connect(self.changeVolume)

    def changeVolume(self, value):
        self.player.setVolume(value)

    def openFile(self):
        song = QFileDialog.getOpenFileName(self, "Open Song", "~/Music", "Sound Files (*.mp3 *.ogg *.wav *.m4a)")

        if song[0] != '':
            url = QUrl.fromLocalFile(song[0])
            if self.playlist.mediaCount() == 0:
                self.playlist.addMedia(QMediaContent(url))
                self.player.setPlaylist(self.playlist)
                self.view.pushButtonPlay.setText('pause')
                self.player.play()
                self.playerState = 1
            else:
                self.playlist.addMedia(QMediaContent(url))

    def playPauseHandlerg(self):
        if self.playerState == -1:
            self.openFile()

        elif self.playerState == 1:
            self.player.pause()
            self.playerState = 2
            self.view.pushButtonPlay.setText('play')

        elif self.playerState == 2 or self.playerState == 0:
            self.player.play()
            self.playerState = 1
            self.view.pushButtonPlay.setText('pause')
