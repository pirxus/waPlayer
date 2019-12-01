# Player database module

from tinydb import TinyDB, Query

class Database(TinyDB, Query):

    def __init__(self):
        self.database = TinyDB('database.json')
