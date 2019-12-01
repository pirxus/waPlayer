
from database import Database
from view import View
from model import Model

class Controller():

    def __init__(self):
        self.view = View()
        self.model = Model()

        self.view.actionOpen_File.triggered.connect(self.openFile)
        self.view.pushButtonPlay.clicked.connect(self.playPresed)
        self.view.listAll_Songs.itemDoubleClicked.connect(self.openFile)

    def openFile(self):
        print(self.view.listAll_Songs.currentItem().text())
        self.view.listAll_Songs.addItem('suh')

    def playPresed(self):
        self.view.listAll_Songs.addItem('hello')
