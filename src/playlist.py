from PyQt5.QtCore import QAbstractListModel, Qt
import eyed3, eyed3.id3, json, threading

class PlaylistModel(QAbstractListModel):
    def __init__(self, playlist, *args, **kwargs):
        super(PlaylistModel, self).__init__(*args, **kwargs)
        self.playlist = playlist

    def data(self, index, role):
        if role == Qt.DisplayRole:
            media = self.playlist.media(index.row())
            af = eyed3.load(media.canonicalUrl().toLocalFile()) # audiofile
            return af.tag.title + ' - ' + af.tag.artist


    def rowCount(self, index):
        return self.playlist.mediaCount()
