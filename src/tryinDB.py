from tinydb import TinyDB, Query
from database import *
import json
db = TinyDB('../db_files/database.json')

#song1 = Song(None, 'What I\'ve Done', 'Linkin Park', 'Minutes to Midnight', 2009)
#song2 = Song(None, 'Name(1234fgh)', 'Linkin Park', 'Minutes to Midnight', 2009)

db_t = Database()
#db_t.insert_song(song2)

wanted = Query()

list1 = db_t.search_by_album('Permanence')
print(list1)
#db_t.delete_by_name('Leave out all the rest')
list2 = db_t.get_all()
for item in list1:
    print(item['name'])




