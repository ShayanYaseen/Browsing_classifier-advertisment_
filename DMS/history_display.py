import os
import sqlite3
import shutil
import getpass
import pathlib
import pandas as pd
#comment
username = getpass.getuser()
print("Running the History DMS script")
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

web_dest = curr_direct[:-3] + "/web-app/dashboard/static/data/"

#storing data for web app
db_df = pd.read_sql_query("SELECT url, title, visit_count, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') AS last_visit_time FROM url ORDER BY last_visit_time DESC", local_con)
db_df.to_html(web_dest+'history.htm',justify='left', render_links=True)

db_df = pd.read_sql_query("SELECT url,visit_count from url ORDER BY visit_count DESC LIMIT 10", local_con)
db_df.to_html(web_dest+'visit.htm')

ad_con = sqlite3.connect('ads')
db_df = pd.read_sql_query("SELECT category,title from title", ad_con)
db_df.to_html(web_dest+'ad.htm', justify='left', render_links=True)




local_con.commit()
local_con.close()
history_con.close()
