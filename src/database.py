# Player database module

from tinydb import TinyDB, Query
import json


class Database(TinyDB, Query):
    def __init__(self):
        self.database = TinyDB('../db_files/database.json')

    # inserts new song into the database
    def insert_song(self, song):
        self.database.insert(song.to_json())

    def search_by_name(self, name):
        query = Query()
        name = self.fix_str(name)
        return self.database.search(query.name.search(name))

    def search_by_artist(self, artist):
        artist = self.fix_str(artist)
        query = Query()
        return self.database.search(query.artist.search(artist))

    def search_by_album(self, album):
        if album == '':
            return None
        album = self.fix_str(album)
        query = Query()
        return self.database.search(query.album.search(album))

    # returns json list of all song in database
    def get_all(self):
        return self.database.all()

    def get_path_track_number(self, name, album, artist):
        query = Query()

        name = self.fix_str(name)
        album = self.fix_str(album)
        artist = self.fix_str(artist)
        
        if album == '':
            result = self.database.search(query.name.search(name) & query.artist.search(artist))
        else:   
            result = self.database.search(query.name.search(name)
                    & query.album.search(album) & query.artist.search(artist))

        if result:
            if result[0] != '':
                return (result[0])['path'], (result[0])['track_no']
        return None, None

    def fix_str(self, string):
        string = string.replace('(', '\(')
        string = string.replace(')', '\)')
        string = string.replace('[', '\[')
        string = string.replace(']', '\]')
        string = string.replace('{', '\{')
        string = string.replace('}', '\}')
        string = string.replace('+', '\+')
        return string

    def get_artists(self):
        artistList = []
        query = Query()
        search = self.database.search(query.artist.exists())
        for entry in search:
            name = entry['artist']
            if name not in artistList:
                artistList.append(name)

        return artistList

    def get_albums(self):
        albumList = []
        query = Query()
        search = self.database.search(query.album.exists())
        for entry in search:
            name = entry['album']
            if name not in albumList:
                albumList.append(name)

        return albumList

    def get_albums_by_artist(self, artist):
        albumList = []
        query = Query()
        search = self.search_by_artist(artist)
        for entry in search:
            name = entry['album']
            if name not in albumList:
                albumList.append(name)

        return albumList

    # deletes all item matching name
    def delete_by_name(self, name):
        query = Query()
        name = self.fix_str(name)
        self.database.remove(query.name == name)
    
    # clears the database
    def db_purge(self):
        self.database.purge()


class Song:
    def __init__(self, path, name, artist, album, year, time, track_no):
        self.path = path
        self.name = name
        self.artist = artist
        self.album = album
        self.year = year
        self.time = time
        self.track_no = track_no
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

    def update_time(self, time):
        self.time = time

    def update_track_no(self, track_no):
        self.track_no = track_no

    # converts song to json so it can be stored into the database
    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))
