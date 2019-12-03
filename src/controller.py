
from database import Database, Song
from view import View

import eyed3, json, threading

from PyQt5.QtCore import QUrl, QDirIterator, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QFileDialog, QAction, QHBoxLayout, QVBoxLayout, QSlider, QGraphicsScene, QGraphicsView, QTableWidgetItem, QTableWidget
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
        self.populateLibrary()

        self.playerState = -1 # 0 - stopped, 1 - playing, 2 - paused

    # This method sets up the connections between the ui and the backend
    def setupView(self):
        self.view.actionOpen_File.triggered.connect(self.openFile)
        self.view.actionOpen_Files.triggered.connect(self.openFiles)
        self.view.actionImport_Library.triggered.connect(self.importLibrary)

        self.view.pushButtonPlay.clicked.connect(self.playButtonPressed)
        self.view.pushButtonPrev.clicked.connect(self.prevButtonPressed)
        self.view.pushButtonNext.clicked.connect(self.nextButtonPressed)
        self.view.pushButtonShuffle.clicked.connect(self.playlist.shuffle)
        self.view.pushButtonAddToPlaylist.clicked.connect(self.addToPlaylistPressed)

        self.view.sliderVolume.valueChanged[int].connect(self.changeVolume)
        self.view.sliderSongProgress.valueChanged[int].connect(self.player.setPosition)

        self.view.tableAllSongs.itemDoubleClicked.connect(self.songSelectedFromAllSongs)



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

    def openFiles(self):
        if self.playlist.mediaCount() != 0:
            self.folderIterator()
        else:
            self.folderIterator()
            self.player.setPlaylist(self.playlist)
            self.player.playlist().setCurrentIndex(0)
            self.player.play()
            self.playerState = 1
    
        self.view.tableAllSongs.sortItems()
        self.view.pushButtonPlay.setIcon(
                QIcon('../assets/icons/actions/media-playback-pause.png'))

    def folderIterator(self):
        folderChosen = QFileDialog.getExistingDirectory(self, 'Open Music Folder', '~/')
        if folderChosen != None:
            it = QDirIterator(folderChosen)
            it.next()
            while it.hasNext():
                if it.fileInfo().isDir() == False and it.filePath() != '.':
                    fInfo = it.fileInfo()
                    if fInfo.suffix() in ('mp3', 'ogg', 'wav', 'm4a'):
                        url = QUrl.fromLocalFile(it.filePath())
                        self.playlist.addMedia(QMediaContent(url))
                        self.view.tableAllSongs.addItem(url.fileName())

                it.next()
            if it.fileInfo().isDir() == False and it.filePath() != '.':
                fInfo = it.fileInfo()
                if fInfo.suffix() in ('mp3', 'ogg', 'wav', 'm4a'):
                    url = QUrl.fromLocalFile(it.filePath())
                    self.playlist.addMedia(QMediaContent(url))
                    self.view.tableAllSongs.addItem(url.fileName())

    def importLibrary(self):
        self.database.db_purge()
        folder = QFileDialog.getExistingDirectory(self, 'Open Music Folder', '~/')
        thread = threading.Thread(target = self.importRecursiveIterator, args = (folder, ), daemon = True)
        thread.start()
        thread.join()
        self.populateLibrary()

    def populateLibrary(self):
        self.view.tableAllSongs.clearContents()
        dataList = self.database.get_all()
        if dataList:
            i = 0
            for item in dataList: #populate the all songs tab
                self.view.tableAllSongs.insertRow(i)
                self.view.tableAllSongs.setItem(i, 0, QTableWidgetItem(item["name"]))
                self.view.tableAllSongs.setItem(i, 1,
                        QTableWidgetItem(str(hhmmss(int(str(int(item["time"])) + '000')))))
                self.view.tableAllSongs.setItem(i, 2, QTableWidgetItem(item["album"]))
                self.view.tableAllSongs.setItem(i, 3, QTableWidgetItem(item["artist"]))
                i += 1

    def importRecursiveIterator(self, folder):
        if folder!= None:
            it = QDirIterator(folder)
            it.Subdirectories = True
            it.next()
            while it.hasNext():
                if it.fileInfo().isDir() == False and it.filePath() != '.':
                    fInfo = it.fileInfo()
                    if fInfo.suffix() in ('mp3'):
                        url = it.filePath()
                        af = eyed3.load(url) # audiofile
                        song = Song(url, af.tag.title, af.tag.artist, af.tag.album, af.tag.getBestDate(), af.info.time_secs)
                        self.database.insert_song(song)

                elif it.fileInfo().isDir() == True and it.fileName() != '..' and it.fileName() != '.':
                    self.importRecursiveIterator(it.filePath())
                it.next()
            if it.fileInfo().isDir() == False and it.filePath() != '.':
                fInfo = it.fileInfo()
                if fInfo.suffix() in ('mp3'):
                    url = it.filePath()
                    af = eyed3.load(url) # audiofile
                    song = Song(url, af.tag.title, af.tag.artist, af.tag.album, af.tag.getBestDate(), af.info.time_secs)
                    self.database.insert_song(song)
            elif it.fileInfo().isDir() == True and it.fileName() != '..' and it.fileName() != '.':
                self.importRecursiveIterator(it.filePath())


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
        if self.player.position() > 5000:
            self.player.setPosition(0)
        else:
            self.player.playlist().previous()

    def metaDataChanged(self):
        self.view.labelPlayerSongName.clear()
        self.view.labelPlayerSongAlbumArtist.clear()

        if self.player.isMetaDataAvailable():
            coverArt = self.player.metaData(QMediaMetaData.CoverArtImage)
            artistName = self.player.metaData(QMediaMetaData.ContributingArtist)
            albumName = self.player.metaData(QMediaMetaData.AlbumTitle)
            songName = self.player.metaData(QMediaMetaData.Title)

            if coverArt == None:
                self.view.label.setPixmap(QPixmap('../assets/stock_album_cover.jpg'))
            else:
                self.view.label.setPixmap(QPixmap.fromImage(coverArt))

            if songName != None:
                self.view.labelPlayerSongName.setText(songName)
            else:
                self.view.labelPlayerSongName.setText(self.player.currentMedia().canonicalUrl().fileName())

            if artistName != None:
                self.view.labelPlayerSongAlbumArtist.setText(artistName)
                if albumName != None:
                    self.view.labelPlayerSongAlbumArtist.setText(
                            artistName + ' - ' + albumName)


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

    def addToPlaylistPressed(self):
        pass
    
    def songSelectedFromAllSongs(self, item):
        row = self.view.tableAllSongs.currentRow() 
        name = self.view.tableAllSongs.item(row, 0).text()
        album = self.view.tableAllSongs.item(row, 2).text()
        artist = self.view.tableAllSongs.item(row, 3).text()
        print('Now playing: ' + name + ' by ' + artist)
        path = self.database.get_path(name, album, artist) #get path from database

        if path != None:
            url = QUrl.fromLocalFile(path)
            self.playlist.clear()
            self.playlist.addMedia(QMediaContent(url))
            self.view.pushButtonPlay.setIcon(
                QIcon('../assets/icons/actions/media-playback-pause.png'))
            self.player.play()
            self.playerState = 1

def hhmmss(ms):
    h, r = divmod(ms, 3600000)
    m, r = divmod(r, 60000)
    s, _ = divmod(r, 1000)
    return ("%d:%02d:%02d" % (h,m,s)) if h else ("%d:%02d" % (m,s))
