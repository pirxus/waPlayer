from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class QLabelClickable(QLabel):
    clicked = pyqtSignal(QLabel)

    def __init__(self, name, parent=None):
        QLabel.__init__(self, parent)
        self.name = name

    def mousePressEvent(self, ev):
        if ev.button() == Qt.RightButton:
            QLabel.mousePressEvent(self, ev)
        else:
            self.clicked.emit(self)

    def enterEvent(self, ev):
        self.setStyleSheet("border-color: #B14B88;")

    def leaveEvent(self, ev):
        self.setStyleSheet("border-color: black;")

class QLabelClickableWithParent(QLabel):
    clicked = pyqtSignal(QLabel)

    def __init__(self, name, parent):
        QLabel.__init__(self, parent)
        self.name = name

    def mousePressEvent(self, ev):
        if ev.button() == Qt.RightButton:
            QLabel.mousePressEvent(self, ev)
        else:
            self.clicked.emit(self)


    #def enterEvent(self, ev):
        #self.setStyleSheet("border-color: #B14B88;")

    #def leaveEvent(self, ev):
       # self.setStyleSheet("border-color: black;")
