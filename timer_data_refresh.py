import os
import time
from datetime import datetime
from subprocess import Popen

while True:
    print("ran at {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    p = Popen("run.bat", cwd=r"C:/Users/Administrator/Desktop/db2/")
    stdout, stderr = p.communicate()
    print("refreshed at {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    time.sleep(3600)