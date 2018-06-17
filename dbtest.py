#dbtest.py


import sqlite3
db = sqlite3.connect(dbLocation)
cursor = db.cursor()
# make sqlite3 return bytestrings not unicode
db.text_factory = bytes


