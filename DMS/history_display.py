import os
import sqlite3
import shutil
import getpass
import pathlib
#comment
username = getpass.getuser()

#copy the database file to local storage
source = "/home/{}/.config/google-chrome/Default/History".format(username)
curr_direct = str(pathlib.Path(__file__).parent.absolute()) # get name of current directory
destination = curr_direct+"/history"
dest = shutil.copyfile(source, destination)
# print(source)
# print( curr_direct)
# print(destination)
# print(dest)

history_con = sqlite3.connect(destination)
c = history_con.cursor()
# Change this to your prefered queryresults = c.fetchall()
c.execute("select url, title, visit_count, last_visit_time from urls")
results = c.fetchall()
# for r in results:
#  print(r)


#database to store clean data
local_con = sqlite3.connect('local')
local_cur = local_con.cursor()
#dropping table and closing cursors
local_cur.execute("DROP TABLE IF EXISTS url")

#extracting required table from the history db to our local db
local_cur.execute("ATTACH DATABASE 'history' AS history;")
local_cur.execute("CREATE TABLE IF NOT EXISTS url(id INTEGER PRIMARY KEY AUTOINCREMENT,url LONGVARCHAR,title LONGVARCHAR,visit_count INTEGER NOT NULL DEFAULT 0,last_visit_time INTEGER NOT NULL)")
local_cur.execute("INSERT INTO url SELECT id,url,title,visit_count,last_visit_time FROM history.urls")


local_con.commit()
local_con.close()
history_con.close()
