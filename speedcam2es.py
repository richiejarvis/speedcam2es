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



my_path = os.path.abspath(__file__)  # Find the full path of this python script
# get the path location only (excluding script name)
base_dir = my_path[0:my_path.rfind("/")+1]
base_file_name = my_path[my_path.rfind("/")+1:my_path.rfind(".")]
prog_name = os.path.basename(__file__)

# Check for variable file to import and error out if not found.
config_file_path = os.path.join(base_dir, "config.py")
if not os.path.exists(config_file_path):
    print("ERROR : Missing config.py file - File Not Found %s"
          % config_file_path)
    import urllib2
    config_url = "https://raw.githubusercontent.com/richiejarvis/speedcam2es/master/config.py"
    print("INFO  : Attempting to Download config.py file from %s" % config_url)
    try:
        wgetfile = urllib2.urlopen(config_url)
    except:
        print("ERROR : Download of config.py Failed")
        print("        %s %s Exiting Due to Error" % (prog_name, version))
        sys.exit(1)
    f = open('config.py', 'wb')
    f.write(wgetfile.read())
    f.close()
# Read Configuration variables from config.py file
from config import *

horz_line = "----------------------------------------------------------------------"
print(horz_line)
print("%s %s   written by Richie Jarvis to work with Claude Pageau's speed_cam available here: https://github.com/pageauc/speed-camera" % (prog_name, version))

def Main():
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(report_query)
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        unique_hash = hashlib.sha1(str(tuple(row)) + ip_address).hexdigest()
        if row["direction"] == "L2R":
            direction = "Southbound"
        else:
            direction = "Northbound"
        record = {
                '@timestamp' : make_date(row["idx"]),
                'speed' : row["ave_speed"],
                'direction' : direction,
                'source' : ip_address
                }
        #print(repr(record))
        url = elasticsearch_url + ip_address + '-' + row["log_date"] + '/record/'+unique_hash
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
