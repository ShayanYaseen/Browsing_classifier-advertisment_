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
    # results[r].append(0)
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
            last_visit_update.append(i)
    else:
        new_entries.append(i)
# print(len(new_entries),new_entries[1:4])
# print(len(last_visit_update))
# print(last_visit_update,'\n', len(last_visit_update))


curr_direct = str(pathlib.Path(__file__).parent.absolute()) # get name of current directory
curr_direct = curr_direct[:-3]
curr_direct += 'ML MODEL/Pickle_MNB_Model.pkl'

# print(curr_direct)
import pickle
# import sklearn
# Load the Model back from file
with open(curr_direct, 'rb') as file:
    Pickled_MNB_Model = pickle.load(file)

# print(Pickled_LR_Model)

# Use the Reloaded Model to
# Calculate the accuracy score and predict target values

for i in new_entries:
    X_test = [i[2],]

    # Predict the Labels using the reloaded Model
    Y_pred = Pickled_MNB_Model.predict(X_test)
    Y_pred = str(Y_pred[0])
    i.append(Y_pred)
    # print(Y_pred)
    ads_cur.execute('INSERT INTO title VALUES (?,?,?,?,?)',i)








for i in last_visit_update:
    ads_cur.execute("SELECT * FROM title WHERE id=?", (i[0],))
    # print(ads_cur.fetchall())
    ads_cur.execute("UPDATE title SET last_visit_time =? WHERE id=?",(i[3],i[0]))
    ads_cur.execute("SELECT * FROM title WHERE id =?",(i[0],))
    # print(ads_cur.fetchall())
ads.commit()


curr_direct = str(pathlib.Path(__file__).parent.absolute()) # get name of current directory
web_dest = curr_direct[:-3] + "/web-app/dashboard/static/data/"

import pandas as pd
ads = sqlite3.connect('ads')
db_df = pd.read_sql_query("SELECT url,title,category FROM title", ads)
db_df.to_html(web_dest+'ad.htm', justify='left', render_links=True)


ads.close()