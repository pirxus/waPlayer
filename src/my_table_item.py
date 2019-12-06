from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import controller

class MyTableItem(QTableWidgetItem):

    def __init__(self, itemType, path, artist, album, name, time, parent=None):
        QTableWidgetItem.__init__(self, parent)
        self.itemType = itemType
        self.path = path
        self.artist = artist
        self.album = album
        self.name = name
        self.time = str(controller.hhmmss(int(str(int(time)) + '000')))
