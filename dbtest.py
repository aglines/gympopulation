import sqlite3
import time
import datetime
from secrets import *

db = sqlite3.connect(dbLocation)
cursor = db.cursor()
# make sqlite3 return bytestrings not unicode
# db.text_factory = bytes

currPop = '142'

currTime = time.time()
# currTime = str(currTime)
print "curr time", currTime

cursor.execute('INSERT INTO times (timestamp, pop) VALUES (?,?)', (currTime, currPop))
db.commit()


cursor.execute("SELECT timestamp FROM times WHERE id = 2")
result = cursor.fetchone()[0]
print result
newresult = datetime.datetime.fromtimestamp(result)
print "newresult = ", newresult

db.close()
