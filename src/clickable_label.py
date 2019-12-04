from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QVBoxLayout


class QLabelClickable(QLabel):
    clicked = pyqtSignal(QLabel)

    def __init__(self, name, parent=None):
        QLabel.__init__(self, parent)
        self.name = name

    def mousePressEvent(self, ev):
        self.clicked.emit(self)
