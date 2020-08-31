##
# authors: xsedla1h, xsarva00, xosval03
#

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QListWidgetItem, QLineEdit
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

class MyListItem(QListWidgetItem):

    def __init__(self, path, name, parent=None):
        QListWidgetItem.__init__(self, parent)
        self.path = path
        self.name = name

"""class MytableItemDragDrop(QTableWidgetItem):

    def __init__(self, itemType, path, artist, album, name, time, parent=None):
        QTableWidgetItem.__init__(self, parent)
        edit = QLineEdit('', self)
        edit.setDragEnabled(True)
        self.itemType = itemType
        self.path = path
        self.artist = artist
        self.album = album
        self.name = name
        self.time = str(controller.hhmmss(int(str(int(time)) + '000')))

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.setText(e.mimeData().text())"""