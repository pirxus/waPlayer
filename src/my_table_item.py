from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

class MyTableItem(QTableWidgetItem):

    def __init__(self, itemType, path, artist, album, name, parent=None):
        QTableWidgetItem.__init__(self, parent)
        self.itemType = itemType
        self.path = path
        self.artist = artist
        self.album = album
        self.name = name
