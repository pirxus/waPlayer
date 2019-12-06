#!/usr/bin/python3

import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from view import View
from controller import Controller

# This class represents the main application class of the player
class App(QtWidgets.QApplication):

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyle('GTK+')
        self.controller = Controller()

    

if __name__ == '__main__':
    application = App()
    sys.exit(application.app.exec_())
