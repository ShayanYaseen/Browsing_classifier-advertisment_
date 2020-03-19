import os
import sqlite3
import shutil
import getpass
import pathlib
curr_direct = str(pathlib.Path(__file__).parent.absolute()
                  )  # get name of current directory

web_dest = curr_direct[:-3] + "/web-app/dashboard/static/data/"
print(web_dest)
