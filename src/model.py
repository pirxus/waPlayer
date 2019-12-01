
from database import Database
from player import Player
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent


class Model():

    def __init__(self):
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.database = Database()

