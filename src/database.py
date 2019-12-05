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
        name = name.replace('(', '\(')
        name = name.replace(')', '\)')
        name = name.replace('+', '\+')
        return self.database.search(query.name.search(name))

    def search_by_artist(self, artist):
        query = Query()
        artist = artist.replace('(', '\(')
        artist = artist.replace(')', '\)')
        return self.database.search(query.artist.search(artist))

    def search_by_album(self, album):
        query = Query()
        album = album.replace('(', '\(')
        album = album.replace(')', '\)')
        return self.database.search(query.albums.search(album))

    def get_album_songs(self):
        query = Query()
        return self.database.search(query.name.search('Permanence'))


    # returns json list of all song in database
    def get_all(self):
        return self.database.all()

    def get_all_albums(self):
        songs = self.database.all()
        all_albums = []
        for song in songs:
            if song['album']:
                all_albums.append(song['album'])
        albums = list(set(all_albums))
        return albums

    def get_path(self, name, album, artist):
        query = Query()

        name = name.replace('(', '\(')
        name = name.replace(')', '\)')
        name = name.replace('+', '\+')
        album = album.replace('(', '\(')
        album = album.replace(')', '\)')
        artist = artist.replace('(', '\(')
        artist = artist.replace(')', '\)')
        
        if album == '':
            result = self.database.search(query.name.search(name) & query.artist.search(artist))
        else:   
            result = self.database.search(query.name.search(name)
                    & query.album.search(album) & query.artist.search(artist))

        if result[0] != '':
            return (result[0])['path']
        else:
            return None

    # deletes all item matching name
    def delete_by_name(self, name):
        query = Query()
        name = name.replace('(', '\(')
        name = name.replace(')', '\)')
        self.database.remove(query.name == name)
    
    # clears the database
    def db_purge(self):
        self.database.purge()


class Song:
    def __init__(self, path, name, artist, album, year, time): #TODO - add track number
        self.path = path
        self.name = name
        self.artist = artist
        self.album = album
        self.year = year
        self.time = time
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

    # converts song to json so it can be stored into the database
    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))
