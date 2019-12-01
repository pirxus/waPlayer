from tinydb import TinyDB, Query
from src.database import *
import json
db = TinyDB('db_files/database.json')

song1 = Song(None, 'What I\'ve Done', 'Linkin Park', 'Minutes to Midnight', 2009)
song2 = Song(None, 'Leave out all the rest', 'Linkin Park', 'Minutes to Midnight', 2009)

db_t = Database()
#db_t.insert_song(song2)

wanted = Query()

list1 = db_t.search_by_name('What')
list2 = db_t.get_all()
for item in list2:
    print(item['name'])




