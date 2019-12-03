from database import Database
from view import View
from PyQt5.QtCore import QUrl, QDirIterator, Qt
from PyQt5.QtGui import QPixmap, QIcon

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QFileDialog, QAction, QHBoxLayout, QVBoxLayout, QSlider, QGraphicsScene, QGraphicsView
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent, QMediaMetaData

class Controller(QWidget):

    def __init__(self):
        super().__init__()
        self.view = View()
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.database = Database()
        self.setupView()
        self.setupPlayer()

        self.playerState = -1 # 0 - stopped, 1 - playing, 2 - paused

    # This method sets up the connections between the ui and the backend
    def setupView(self):
        self.view.actionOpen_File.triggered.connect(self.openFile)
        self.view.actionOpen_Files.triggered.connect(self.openFiles)
        self.view.pushButtonPlay.clicked.connect(self.playButtonPressed)
        self.view.pushButtonPrev.clicked.connect(self.prevButtonPressed)
        self.view.pushButtonNext.clicked.connect(self.nextButtonPressed)
        self.view.pushButtonShuffle.clicked.connect(self.playlist.shuffle)

        self.view.sliderVolume.valueChanged[int].connect(self.changeVolume)
        self.view.sliderSongProgress.valueChanged[int].connect(self.player.setPosition)


    # This method sets up the signals for the player class
    def setupPlayer(self):
        self.player.setPlaylist(self.playlist)

        self.player.metaDataChanged.connect(self.metaDataChanged)
        self.player.durationChanged.connect(self.updateDuration)
        self.player.positionChanged.connect(self.updateSongProgress)
        self.player.stateChanged.connect(self.updatePlayerState)


    def openFile(self):
        song = QFileDialog.getOpenFileName(self, "Open Song", "/home/pirx/Music", "Sound Files (*.mp3 *.ogg *.wav *.m4a)")

        if song[0] != '':
            url = QUrl.fromLocalFile(song[0])
            self.playlist.addMedia(QMediaContent(url))
            self.view.pushButtonPlay.setIcon(
                QIcon('../assets/icons/actions/media-playback-pause.png'))
            self.player.play()
            self.playerState = 1

            #print(self.player.metaData(QMediaMetaData.ContributingArtist))
            self.view.listAllSongs.addItem(url.fileName())

    def openFiles(self):
        if self.playlist.mediaCount() != 0:
            self.folderIterator()
        else:
            self.folderIterator()
            self.player.setPlaylist(self.playlist)
            self.player.playlist().setCurrentIndex(0)
            self.player.play()
            self.playerState = 1
    
        self.view.listAllSongs.sortItems()
        self.view.pushButtonPlay.setIcon(
                QIcon('../assets/icons/actions/media-playback-pause.png'))

    def folderIterator(self):
        folderChosen = QFileDialog.getExistingDirectory(self, 'Open Music Folder', '~')
        if folderChosen != None:
            it = QDirIterator(folderChosen)
            it.next()
            while it.hasNext():
                if it.fileInfo().isDir() == False and it.filePath() != '.':
                    fInfo = it.fileInfo()
                    if fInfo.suffix() in ('mp3', 'ogg', 'wav', 'm4a'):
                        url = QUrl.fromLocalFile(it.filePath())
                        self.playlist.addMedia(QMediaContent(url))
                        self.view.listAllSongs.addItem(url.fileName())

                it.next()
            if it.fileInfo().isDir() == False and it.filePath() != '.':
                fInfo = it.fileInfo()
                if fInfo.suffix() in ('mp3', 'ogg', 'wav', 'm4a'):
                    url = QUrl.fromLocalFile(it.filePath())
                    self.playlist.addMedia(QMediaContent(url))
                    self.view.listAllSongs.addItem(url.fileName())

    def playButtonPressed(self):
        if self.playerState == -1:
            self.openFile()

        elif self.playerState == 1:
            self.player.pause()
            self.playerState = 2
            self.view.pushButtonPlay.setIcon(
                QIcon('../assets/icons/actions/gtk-media-play-ltr.png'))

        elif self.playerState == 2 or self.playerState == 0:
            self.player.play()
            self.playerState = 1
            self.view.pushButtonPlay.setIcon(
                QIcon('../assets/icons/actions/media-playback-pause.png'))

    def nextButtonPressed(self):
        self.player.playlist().next()

    def prevButtonPressed(self):
        if self.player.position() < 5000 or self.player.playlist():
            self.player.setPosition(0)
        else:
            self.player.playlist().previous()

    def metaDataChanged(self):
        artUrl = None

        if self.player.isMetaDataAvailable():
            #print(self.player.metaData(QMediaMetaData.Artist))
            #print(self.player.metaData(QMediaMetaData.CoverArtUrlLarge))
            self.view.listAllSongs.addItem(self.player.metaData(QMediaMetaData.Author))
            artUrl = self.player.metaData(QMediaMetaData.CoverArtUrlSmall)

        if artUrl == None:
            artUrl = '../assets/cover.jpg'

        self.view.label.setPixmap(QPixmap(artUrl))

    def updateDuration(self, duration):
        self.view.sliderSongProgress.setMaximum(duration)
        self.view.labelSongDuration.setText(hhmmss(duration))

    def updateSongProgress(self, time):
        self.view.labelSongProgress.setText(hhmmss(time))

        self.view.sliderSongProgress.blockSignals(True)
        self.view.sliderSongProgress.setValue(time)
        self.view.sliderSongProgress.blockSignals(False)

    def updatePlayerState(self, state):
        if state == QMediaPlayer.StoppedState:
            self.playerState = 0;
            self.view.pushButtonPlay.setIcon(
                QIcon('../assets/icons/actions/gtk-media-play-ltr.png'))

    def changeVolume(self, value):
        self.player.setVolume(value)

def hhmmss(ms):
    h, r = divmod(ms, 3600000)
    m, r = divmod(r, 60000)
    s, _ = divmod(r, 1000)
    return ("%d:%02d:%02d" % (h,m,s)) if h else ("%d:%02d" % (m,s))
