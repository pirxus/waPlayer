from database import Database
from view import View
from model import Model
from player import Player
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent

class Controller():

    def __init__(self):
        self.view = View()
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.database = Database()
        self.linkView()

    # This method sets up the connections between the ui and the backend
    def linkView():
        self.view.actionOpen_File.triggered.connect(self.openFile)
        self.view.pushButtonPlay.clicked.connect(self.playPresed)
        self.view.listAll_Songs.itemDoubleClicked.connect(self.openFile)

    def openFile(self):
        print(self.view.listAll_Songs.currentItem().text())
        self.view.listAll_Songs.addItem('suh')

    def playPresed(self):
        self.view.listAll_Songs.addItem('hello')

