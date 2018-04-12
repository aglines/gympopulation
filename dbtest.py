import sqlite3
import time
import datetime
from secrets import *

db = sqlite3.connect(dbLocation)
cursor = db.cursor()
currPop = '142'
currTime = time.time()

cursor.execute('INSERT INTO times (timestamp, pop) VALUES (?,?)', (currTime, currPop))
db.commit()

# look at stored data once it's captured
cursor.execute("SELECT timestamp FROM times WHERE id = 2")
result = cursor.fetchone()[0]
newresult = datetime.datetime.fromtimestamp(result)
print "newresult = ", newresult
db.close()
