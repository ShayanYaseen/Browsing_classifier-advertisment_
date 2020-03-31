import plotly
import plotly.express as px
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
curr_direct = str(pathlib.Path(__file__).parent.absolute()
                  )  # get name of current directory
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
local_cur.execute(
    "INSERT INTO url SELECT id,url,title,visit_count,last_visit_time FROM history.urls")

web_dest = curr_direct[:-3] + "/web-app/dashboard/static/data/"

#storing data for web app
db_df = pd.read_sql_query(
    "SELECT url, title, visit_count, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') AS last_visit_time FROM url ORDER BY last_visit_time DESC", local_con)
pd.set_option('display.max_colwidth', 100)
db_df.to_csv(web_dest+'history.csv')

db_df = pd.read_sql_query(
    "SELECT url,visit_count from url ORDER BY visit_count DESC LIMIT 10", local_con)

# Stats for top 10 sites
fig = px.pie(db_df, values="visit_count", names="url",
             title="Most visited websites", hover_data=['visit_count'],
             labels={'url': 'url'})
fig.update_traces(textposition='inside', textinfo='percent+label')
fig_loc = curr_direct[:-3] + "web-app/dashboard/static/data/"
plotly.offline.plot(fig, filename=fig_loc+'pie_embed.html', auto_open=False)


fig = px.bar(db_df, x='url', y='visit_count',
             hover_data=['url', 'visit_count'], color='visit_count', height=600)
plotly.offline.plot(fig, filename=fig_loc+'bar_embed.html', auto_open=False)

db_df.to_csv(web_dest+'visit.csv')

db_df = pd.read_sql_query(
    "SELECT url from url ORDER BY visit_count DESC LIMIT 10", local_con)
db_df.to_html(web_dest+'prod_data.html')
# ad_con = sqlite3.connect('ads')
# db_df = pd.read_sql_query("SELECT category,title from title", ad_con)
# db_df.to_html(web_dest+'ad.htm', justify='left', render_links=True)

local_con.commit()
local_con.close()
history_con.close()
