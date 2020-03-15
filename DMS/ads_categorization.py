import os
import sqlite3
import shutil
import getpass
import pathlib

history_con = sqlite3.connect('local')
local = history_con.cursor()
local.execute("SELECT id,url, title,last_visit_time FROM url")
results = local.fetchall()
for r in range(len(results)):
    results[r] = list(results[r])
    results[r].append(0)
    # print(results[r])

#database to store clean data
ads = sqlite3.connect('ads')
ads_cur = ads.cursor()

#extracting required table from the history db to our local db
ads_cur.execute("ATTACH DATABASE 'local' AS local;")
ads_cur.execute("CREATE TABLE IF NOT EXISTS title(id INTEGER PRIMARY KEY AUTOINCREMENT,url LONGVARCHAR,title LONGVARCHAR,last_visit_time INTEGER NOT NULL,category LONG VARCHAR)")
ads_cur.execute("SELECT id,last_visit_time FROM title")
ids  = ads_cur.fetchall()
# print(ids)
time_stamp = 0
for i in range(len(ids)):
    if ids[i][1]>time_stamp:
        time_stamp = ids[i][1]
    ids[i] = ids[i][0]

# print(ids)
# print(time_stamp)
new_entries = []
last_visit_update = []
for i in results:
    if i[0] in ids:
        if i[3]>time_stamp:
            last_visit_update.append(tuple(i))
    else:
        new_entries.append(tuple(i))
# print(len(new_entries),new_entries[1:4])
# print(len(last_visit_update))
# print(last_visit_update,'\n', len(last_visit_update))

for i in new_entries:
    # print(i)
    ads_cur.execute('INSERT INTO title VALUES (?,?,?,?,?)',i)

for i in last_visit_update:
    ads_cur.execute("SELECT * FROM title WHERE id=?", (i[0],))
    # print(ads_cur.fetchall())
    ads_cur.execute("UPDATE title SET last_visit_time =? WHERE id=?",(i[3],i[0]))
    ads_cur.execute("SELECT * FROM title WHERE id =?",(i[0],))
    # print(ads_cur.fetchall())

ads.commit()
ads.close()