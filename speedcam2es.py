#!/usr/bin/python
import simplejson
import sqlite3
import time
import sys
import os
import hashlib
import requests
import urllib3
import socket
from subprocess import check_output
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DB_PATH = '/home/pi/speed-camera/data/speed_cam.db'
DB_TABLE = 'speed'
REPORT_QUERY = ('''select * from speed order by idx desc''')
IP_ADDRESS = check_output(['hostname', '--all-ip-addresses']).strip()

mypath = os.path.abspath(__file__)  # Find the full path of this python script
# get the path location only (excluding script name)
baseDir = mypath[0:mypath.rfind("/")+1]
baseFileName = mypath[mypath.rfind("/")+1:mypath.rfind(".")]
progName = os.path.basename(__file__)
horz_line = "----------------------------------------------------------------------"
print(horz_line)
print("%s %s   written by Richie Jarvis to work with Claude Pageau's speed_cam available here: https://github.com/pageauc/speed-camera" % (progName, version))

# Check for variable file to import and error out if not found.
configFilePath = os.path.join(baseDir, "config.py")
if not os.path.exists(configFilePath):
    print("ERROR : Missing config.py file - File Not Found %s"
          % configFilePath)
    import urllib2
    config_url = "https://raw.githubusercontent.com/richiejarvis/speedcam2es/master/config.py"
    print("INFO  : Attempting to Download config.py file from %s" % config_url)
    try:
        wgetfile = urllib2.urlopen(config_url)
    except:
        print("ERROR : Download of config.py Failed")
        print("        %s %s Exiting Due to Error" % (progName, progVer))
        sys.exit(1)
    f = open('config.py', 'wb')
    f.write(wgetfile.read())
    f.close()
# Read Configuration variables from config.py file
from config import *


def Main():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(REPORT_QUERY)
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        unique_hash = hashlib.sha1(str(tuple(row)) + IP_ADDRESS).hexdigest()
        if row["direction"] == "L2R":
            direction = "Southbound"
        else:
            direction = "Northbound"
        record = {
                '@timestamp' : make_date(row["idx"]),
                'speed' : row["ave_speed"],
                'direction' : direction,
                'source' : IP_ADDRESS
                }
        #print(repr(record))
        url = elasticsearch_url + IP_ADDRESS + '-' + row["log_date"] + '/record/'+unique_hash
        resp = requests.post(url,auth=(username,password),verify=False,json=record)
        print(unique_hash + ": " + str(resp.status_code))
        if resp.status_code == 200:
            break
    cursor.close()
    connection.close

def make_date(string):
    # yyyymmdd-hhmmsss
    string = string[:4] + '-' + string[4:]
    # yyyy-mmdd-hhmmsss
    string = string[:7] + '-' + string[7:]
    # yyyy-mm-dd-hhmmsss
    string = string[:10] + 'T' + string[11:]
    # yyyy-mm-ddThhmmsss
    string = string[:13] + ':' + string[13:]
    # yyyy-mm-dd-hh:mmsss
    string = string[:16] + ':00'
    # yyyy-mm-dd-hh:mm:sss
    string = string[:19].strip() + timezone
    return string


if __name__ == "__main__":
    Main()
