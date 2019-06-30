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
        url = 'https://172.24.42.100:9243/chailey-' + IP_ADDRESS + '-' + row["log_date"] + '/record/'+unique_hash
        resp = requests.post(url,auth=('elastic','yF1PQEh8AfiMquEG0sSW'),verify=False,json=record)
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
    string = string[:19].strip() + 'Europe/London'
    return string


if __name__ == "__main__":
    Main()
