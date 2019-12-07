from database import Database, Song
from view import View

import eyed3, eyed3.id3, json, threading
from clickable_label import QLabelClickable
from my_table_item import MyTableItem

from PyQt5 import QtGui
from PyQt5.QtCore import QUrl, QDirIterator, Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QFileDialog, QAction, QHBoxLayout, QVBoxLayout, QSlider, QGraphicsScene, QGraphicsView, QTableWidgetItem, QTableWidget, QMenu, QGridLayout, QLabel, QSpacerItem, QSizePolicy, QWidgetItem
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent, QMediaMetaData

FRONT_COVER = eyed3.id3.frames.ImageFrame.FRONT_COVER

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
        self.view.actionPlay_selected.triggered.connect(self.playLibraryItem)
        self.view.actionPlay_next.triggered.connect(self.playNext)
        self.view.actionAdd_to_up_next.triggered.connect(self.addToUpNext)
        self.view.actionClear_up_next.triggered.connect(self.clearQueue)
        self.view.actionCreate_playlist.triggered.connect(self.view.createPlaylistDialog)

        self.view.tabLibrary.tabBarClicked.connect(self.view.goBackAlbumTab)

        self.view.pushButtonPlay.clicked.connect(self.playButtonPressed)
        self.view.pushButtonPrev.clicked.connect(self.prevButtonPressed)
        self.view.pushButtonNext.clicked.connect(self.nextButtonPressed)
        self.view.pushButtonShuffle.clicked.connect(self.playlist.shuffle)
        self.view.pushButtonAddToPlaylist.clicked.connect(self.addToPlaylistPressed)

        self.view.sliderVolume.valueChanged[int].connect(self.changeVolume)
        self.view.sliderSongProgress.valueChanged[int].connect(self.player.setPosition)
        self.createAlbumGrid()

        self.view.listArtistNames.itemClicked.connect(self.artistSelected)
        self.view.tableAllSongs.itemDoubleClicked.connect(self.songSelectedFromAllSongs)
        self.view.tableAlbumContent.itemDoubleClicked.connect(self.songSelectedFromArtistAlbum)
        self.view.albumSongs.itemDoubleClicked.connect(self.songSelectedFromArtistAlbum)
        # has icon?

        # custom context menus
        self.view.tableAllSongs.customContextMenuRequested.connect(self.allSongsMenu)
        self.view.tableAlbumContent.customContextMenuRequested.connect(self.artistTableMenu)
        #dialogs
        self.view.dialog.buttonBox.accepted.connect(self.createNewPlaylist)



    # This method sets up the signals for the player class
    def setupPlayer(self):
        self.player.setPlaylist(self.playlist)

        self.player.metaDataChanged.connect(self.metaDataChanged)
        self.player.durationChanged.connect(self.updateDuration)
        self.player.positionChanged.connect(self.updateSongProgress)
        self.player.stateChanged.connect(self.updatePlayerState)

        self.player.metaDataChanged.connect(self.metaDataChanged)


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
        self.view.listArtistNames.clear()
        dataList = self.database.get_all(self.database.database)
        artistList = self.database.get_artists()
        if dataList:
            i = 0
            for item in dataList: #populate the all songs tab
                self.view.tableAllSongs.insertRow(i)
                self.view.tableAllSongs.setItem(i, 0, QTableWidgetItem(item["name"]))
                time = QTableWidgetItem(str(hhmmss(int(str(int(item["time"])) + '000'))))
                time.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter) # align time to the right
                self.view.tableAllSongs.setItem(i, 1, time)
                self.view.tableAllSongs.setItem(i, 2, QTableWidgetItem(item["album"]))
                self.view.tableAllSongs.setItem(i, 3, QTableWidgetItem(item["artist"]))
                i += 1


        if artistList:
            for artist in artistList: #populate the artist list
                self.view.listArtistNames.addItem(artist)
            self.view.listArtistNames.sortItems()
            self.loadArtistAlbums(artistList[0])
        self.createAlbumGrid()

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
                        song = Song(url, af.tag.title, af.tag.artist, af.tag.album, af.tag.getBestDate(), af.info.time_secs, af.tag.track_num)
                        self.database.insert_song(song)

                elif it.fileInfo().isDir() == True and it.fileName() != '..' and it.fileName() != '.':
                    self.importRecursiveIterator(it.filePath())
                it.next()
            if it.fileInfo().isDir() == False and it.filePath() != '.':
                fInfo = it.fileInfo()
                if fInfo.suffix() in ('mp3'):
                    url = it.filePath()
                    af = eyed3.load(url) # audiofile
                    song = Song(url, af.tag.title, af.tag.artist, af.tag.album, af.tag.getBestDate(), af.info.time_secs, af.tag.track_num)
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
                self.view.labelPlayerAlbumArt.setPixmap(QPixmap('../assets/stock_album_cover.jpg'))
            else:
                self.view.labelPlayerAlbumArt.setPixmap(QPixmap.fromImage(coverArt))

            if songName != None:
                self.view.labelPlayerSongName.setText(songName)
            else:
                self.view.labelPlayerSongName.setText(self.player.currentMedia().canonicalUrl().fileName())

            if artistName != None:
                self.view.labelPlayerSongAlbumArtist.setText(artistName)
                if albumName != None:
                    self.view.labelPlayerSongAlbumArtist.setText(
                            artistName + '\n' + albumName)


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
            self.playerState = 0
            self.view.pushButtonPlay.setIcon(
                QIcon('../assets/icons/actions/gtk-media-play-ltr.png'))
            #self.view.labelPlayerAlbumArt.setPixmap(QPixmap('../assets/stock_album_cover.jpg'))
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
        path = self.database.get_path_track_number(name, album, artist)[0] #get path from database

        if path != None:
            url = QUrl.fromLocalFile(path)
            self.playlist.clear()
            self.playlist.addMedia(QMediaContent(url))
            self.view.pushButtonPlay.setIcon(
                QIcon('../assets/icons/actions/media-playback-pause.png'))
            self.player.play()
            self.playerState = 1

    def songSelectedFromArtistAlbum(self, item):
        if item.itemType == 'song':
            print('Now playing: ' + item.name + ' by ' + item.artist)
            url = QUrl.fromLocalFile(item.path)
            self.playlist.clear()
            self.playlist.addMedia(QMediaContent(url))
            self.view.pushButtonPlay.setIcon(
                QIcon('../assets/icons/actions/media-playback-pause.png'))
            self.player.play()
            self.playerState = 1

    def addToUpNext(self):
        tabIndex = self.view.tabLibrary.currentIndex()
        if tabIndex == 0: # all songs tab
            items = self.view.tableAllSongs.selectedItems()
            for i in range(len(items) // 4):
                name = items[4 * i + 0].text()
                album = items[4 * i + 2].text()
                artist = items[4 * i + 3].text()
                print('Adding to up next: ' + name + ' by ' + artist)
                path = self.database.get_path_track_number(name, album, artist) #get path from database

                if path != None:
                    url = QUrl.fromLocalFile(path)
                    if self.playlist.mediaCount() == 0:
                        self.playlist.addMedia(QMediaContent(url))
                        self.view.pushButtonPlay.setIcon(
                            QIcon('../assets/icons/actions/media-playback-pause.png'))
                        self.player.play()
                        self.playerState = 1
                    else:
                        self.playlist.addMedia(QMediaContent(url))
        elif tabIndex == 2: # artists tab

            items = self.view.tableAlbumContent.selectedItems()
            for i in range(len(items) // 2):
                item = items[2 * i]
                if item.itemType == 'song':
                    print('Adding to up next: ' + item.name + ' by ' + item.artist)

                    url = QUrl.fromLocalFile(item.path)
                    if self.playlist.mediaCount() == 0:
                        self.playlist.addMedia(QMediaContent(url))
                        self.view.pushButtonPlay.setIcon(
                            QIcon('../assets/icons/actions/media-playback-pause.png'))
                        self.player.play()
                        self.playerState = 1
                    else:
                        self.playlist.addMedia(QMediaContent(url))

    def playNext(self):
        tabIndex = self.view.tabLibrary.currentIndex()
        if tabIndex == 0: # all songs tab
            items = self.view.tableAllSongs.selectedItems()
            for i in range(len(items) // 4):
                name = items[4 * i + 0].text()
                album = items[4 * i + 2].text()
                artist = items[4 * i + 3].text()
                print('Playing next: ' + name + ' by ' + artist)
                path = self.database.get_path_track_number(name, album, artist) #get path from database

                if path != None:
                    url = QUrl.fromLocalFile(path)
                    if self.playlist.mediaCount() == 0:
                        self.playlist.insertMedia(self.playlist.nextIndex() + i,
                                QMediaContent(url))
                        self.view.pushButtonPlay.setIcon(
                            QIcon('../assets/icons/actions/media-playback-pause.png'))
                        self.player.play()
                        self.playerState = 1
                    else:
                        self.playlist.insertMedia(self.playlist.nextIndex() + i,
                                QMediaContent(url))

        elif tabIndex == 2: # artists tab
            items = self.view.tableAlbumContent.selectedItems()
            for i in range(len(items) // 2):
                item = items[2 * i]
                if item.itemType == 'song':
                    print('Playing next: ' + item.name + ' by ' + item.artist)

                    url = QUrl.fromLocalFile(item.path)
                    if self.playlist.mediaCount() == 0:
                        self.playlist.addMedia(QMediaContent(url))
                        self.view.pushButtonPlay.setIcon(
                            QIcon('../assets/icons/actions/media-playback-pause.png'))
                        self.player.play()
                        self.playerState = 1
                    else:
                        self.playlist.addMedia(QMediaContent(url))



    def playLibraryItem(self):
        self.playlist.removeMedia(self.playlist.nextIndex(), #clear the queue
            self.playlist.mediaCount() - 1)
        mediaCount = self.playlist.mediaCount()

        tabIndex = self.view.tabLibrary.currentIndex()
        if tabIndex == 0: # all songs tab
            items = self.view.tableAllSongs.selectedItems()

            for i in range(len(items) // 4):
                name = items[4 * i + 0].text()
                album = items[4 * i + 2].text()
                artist = items[4 * i + 3].text()
                print('Now playing: ' + name + ' by ' + artist)
                path = self.database.get_path_track_number(name, album, artist)[0] #get path from database

                if path != None:
                    url = QUrl.fromLocalFile(path)
                    self.playlist.addMedia(QMediaContent(url))

        elif tabIndex == 2: # artists tab
            items = self.view.tableAlbumContent.selectedItems()
            for i in range(len(items) // 2):
                item = items[2 * i]
                if item.itemType == 'song':
                    print('Now playing: ' + item.name + ' by ' + item.artist)

                    url = QUrl.fromLocalFile(item.path)
                    self.playlist.addMedia(QMediaContent(url))
        elif tabIndex == 1: # albums tab
            pass
        elif tabIndex == 3: # playlists tab
            pass

        if mediaCount != 0: # jump to next song 
            self.playlist.next()
        self.player.play()
        self.view.pushButtonPlay.setIcon(
            QIcon('../assets/icons/actions/media-playback-pause.png'))
        self.playerState = 1

    def clearQueue(self):
        if self.playlist.currentIndex() < self.playlist.mediaCount() - 1:
            self.playlist.removeMedia(
                    self.playlist.currentIndex() + 1,
                    self.playlist.mediaCount() - 1)

    def allSongsMenu(self, pos):
        allSongsTable = AllSongsMenuHandler(parent=self)
        allSongsTable.rightClick()

    def artistTableMenu(self, pos):
        artistTable = AllSongsMenuHandler(parent=self)
        artistTable.rightClick()

    def createAlbumGrid(self):
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setStyleSheet('QWidget {background-color: #ffffff;}')

        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)

        self.view.scrollAreaAlbums.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.setColumnStretch(0,1)
        self.gridLayout.setColumnStretch(1,1)
        self.gridLayout.setColumnStretch(2,1)
        self.gridLayout.setColumnStretch(3,1)

        alb = self.database.get_albums()
        if alb == []:
            return
        alb.sort()

        num = len(alb)
        counter = 0
        offset = 2
        if num > 4:
            offset = 0
        # i = number of albums  divided by 4 +1  times 2 because of album title
        for i in range(num//4 + offset):
            for j in range(4):
                if (counter < num):
                    name = alb[counter]
                    path = self.database.search_by_album(name)[0]['path']
                else:
                    path = None
                    name = ''

                albumCover = QLabelClickable(name)
                albumCover.setMaximumWidth(141)
                albumCover.setMaximumHeight(141)
                albumCover.setMinimumWidth(141)
                albumCover.setMinimumHeight(141)
                albumCover.setScaledContents(True)

                # load album art
                albumCover.setPixmap(self.getAlbumCover(path))

                albumCover.clicked.connect(self.albumLabelClicked)

                title = QLabel()
                title.setWordWrap(True)
                title.setMaximumHeight(58)
                title.setMinimumHeight(58)
                title.setMaximumWidth(141)
                title.setMinimumWidth(141)
                title.setText(name)
                title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

                subLayout = QVBoxLayout()
                if(counter < num):
                    subLayout.addWidget(albumCover)
                    subLayout.addWidget(title)
                else:
                    self.spaceItem = QSpacerItem(138, 138, QSizePolicy.Fixed)
                    subLayout.addSpacerItem(self.spaceItem)
                    subLayout.addWidget(title)

                self.gridLayout.addLayout(subLayout, i, j)
                counter = counter +1

    def albumLabelClicked(self, label):
        album_songs = self.database.search_by_album(label.name)
        self.view.albumSongs.clearContents() #clear the table
        for i in range(self.view.albumSongs.rowCount()):
            self.view.albumSongs.removeRow(0)
        self.view.openAlbum()
        self.view.albumsButton.clicked.connect(self.view.goBackAlbum)
        self.view.albumCover.clicked.connect(self.playAlbum)

        if album_songs != []:
            counter = 0
            self.view.albumCover.setPixmap(self.getAlbumCover(album_songs[0]['path']))
            self.view.albumName.setText(album_songs[0]['album'])
            self.view.albumYear.setText(str(album_songs[0]['year']['_year']))
            for song in album_songs:
                item = MyTableItem('song' ,song['path'], song['artist'], song['album'], song['name'], song['time'])
                item.setText(song['name'])
                self.view.albumSongs.insertRow(counter)
                self.view.albumSongs.setRowHeight(10, 10)
                self.view.albumSongs.setItem(counter, 0, item)
                time = QTableWidgetItem(item.time)
                time.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.view.albumSongs.setItem(counter, 1, time)
                counter += 1

    def artistSelected(self, item):
        self.loadArtistAlbums(item.text())

    def loadArtistAlbums(self, artist):
        albumList = self.database.get_albums_by_artist(artist)
        for i in range(self.view.tableAlbumContent.rowCount()):
            self.view.tableAlbumContent.removeRow(0)

        if albumList != []:
            i = 0
            for album in albumList:
                self.view.tableAlbumContent.insertRow(i)
                songs = self.database.search_by_album(album)
                if songs != []:

                    item = MyTableItem('album', songs[0]['path'], artist, album,
                            songs[0]['name'], 0)
                    item.setIcon(QIcon(self.getAlbumCover(songs[0]['path'])))
                    text = album + ' - ' + str(songs[0]['year']['_year'])
                    item.setText(text)

                    self.view.tableAlbumContent.setItem(i, 0, item)

                    i += 1
                    for song in songs:
                        self.view.tableAlbumContent.insertRow(i)
                        item = MyTableItem('song', song['path'], artist, album,
                                song['name'], song['time'])
                        item.setText(item.name)
                        self.view.tableAlbumContent.setItem(i, 0, item)
                        time = QTableWidgetItem(item.time)
                        time.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        self.view.tableAlbumContent.setItem(i, 1, time)
                        i += 1

    def getAlbumCover(self, song): # returns QPixmap
        coverArt = None
        if song != None:
            af = eyed3.load(song)
            images = af.tag.images
            for image in images:
                if image.picture_type == FRONT_COVER:
                    coverArt = image.image_data
            if coverArt != None:
                return QPixmap.fromImage(QImage.fromData(coverArt))
        return QPixmap('../assets/stock_album_cover.jpg')

    def playAlbum(self):
        pass

    def createNewPlaylist(self):
        name = self.view.dialog.lineEditNewPlaylist.text()
        if name != '':
            self.database.createNewPlaylist(name)


class AllSongsMenuHandler:
    def __init__(self, parent=None):
            self.parent = parent

    def rightClick(self):
        top_menu = QMenu(self.parent)

        menu = top_menu.addMenu("Menu")
        play = menu.addAction("Play")
        menu.addSeparator()

        playNext = menu.addAction("Play next")
        addToUpNext = menu.addAction("Add to up next")
        menu.addSeparator()

        addToPlaylist = menu.addAction("Add to playlist...")
        config = menu.addMenu("Configuration ...")
        _load = config.addAction("&Load ...")
        config.addSeparator()
        config1 = config.addAction("Config1")

        action = menu.exec_(QtGui.QCursor.pos())

        if action == play: # play
            index = self.parent.view.tabLibrary.currentIndex()
            #if index == 0:
            self.parent.playLibraryItem()
            #elif index == 2:
                #self.parent.playLibraryItem()

        elif action == playNext: # play next
            self.parent.playNext()

        elif action == addToUpNext: # add to up next
            self.parent.addToUpNext()


def hhmmss(ms):
    h, r = divmod(ms, 3600000)
    m, r = divmod(r, 60000)
    s, _ = divmod(r, 1000)
    return ("%d:%02d:%02d" % (h,m,s)) if h else ("%d:%02d" % (m,s))
