from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

class AlbumSongItem(QTableWidgetItem):

    def __init__(self, path, artist, album, name, time, parent=None):
        QTableWidgetItem.__init__(self, parent)
        self.path = path
        self.artist = artist
        self.album = album
        self.name = name
        self.time = time