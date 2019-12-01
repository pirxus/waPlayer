# Player database module

from tinydb import TinyDB, Query
import json


class Database(TinyDB, Query):
    def __init__(self):
        self.database = TinyDB('db_files/database.json')

    def insert_song(self, song):
        self.database.insert(song.to_json())

    def search_by_name(self, name):
        query = Query()
        return self.database.search(query.name.search(name))

    def search_by_artist(self, artist):
        query = Query()
        return self.database.search(query.artist.search(artist))

    def search_by_album(self, name):
        query = Query()
        return self.database.search(query.name.search(name))

    def get_all(self):
        return self.database.all()


class Song:
    def __init__(self, path, name, artist, album, year):
        self.path = path
        self.name = name
        self.artist = artist
        self.album = album
        self.year = year
        self.picture = None

    def update_name(self, name):
        self.name = name

    def update_picture(self, picture):
        self.picture = picture

    def update_path(self, path):
        self.path = path

    def update_interpret(self, interpret):
        self.interpret = interpret

    def update_album(self, album):
        self.album = album

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))
