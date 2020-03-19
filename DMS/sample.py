# 13228910451442258
import os
import sqlite3
import shutil
import getpass
import pathlib
import pandas as pd

local_con = sqlite3.connect('local')
local_cur = local_con.cursor()

#extracting required table from the history db to our local db
local_cur.execute("SELECT datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') ,title from url ORDER BY last_visit_time DESC")
results = local_cur.fetchall()

import datetime
def date_from_timestamp(timestamp):
    epoch_start = datetime.datetime(1601,1,1)
    delta = datetime.timedelta(microseconds=int(timestamp))
    return epoch_start + delta

for i in results[:10]:
    print(i)