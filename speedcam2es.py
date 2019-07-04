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

def Main():
    print("%s %s   Author:Richie Jarvis to work with Claude Pageau's speed_cam available here: https://github.com/pageauc/speed-camera" % (prog_name, version))
    print("Version: %s" % (version))
    print("Author: Richie Jarvis")
    print("Date: 2019-07-01")
    print("GitHub: https://github.com/richiejarvis/speedcam2es")
    print("Description: Convert speed-camera.py sqlite3 db to Elasticsearch Document")
    print("             speed-camera.py written by Claude Pageau:  https://github.com/pageauc/speed-camera")

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(report_query)
    row_count = 0
    while True:
      row_count += 1
      row = cursor.fetchone()
      if row is None:
        break
      if row["direction"] == "L2R":
        direction = l2r_direction
      else:
        direction = r2l_direction
      timestamp = make_date(row["idx"])
      speed = row["ave_speed"]
      record = {
        '@timestamp' : timestamp,
        'speed' : speed,
        'direction' : direction,
        'source' : username,
        'lat': lat,
        'lng': lng
      }
      retry = 0
      unique_hash = hashlib.sha1(str(tuple(row)) + username).hexdigest()
      the_url = (elasticsearch_url + '/record/' + unique_hash).lower()
      if es_post(the_url,record,speed,retry) == 0:
         es_post(the_url,record,speed,retry)
    cursor.close()
    connection.close
    print("Completed")

def make_date(string):
    # 0123456789012345
    # YYYYMMDD-hhmmsss
    YYYY = string[0:4] 
    MM = string[4:6]
    DD = string[6:8]
    hh = string[9:11]
    mm = string[11:13]
    string = (YYYY + '-' + MM + '-' + DD + 'T' + hh + ':'+ mm + ':00' + timezone).strip()
    return string

def es_post(es,record,speed,retry):
    try:
      resp = requests.post(es,auth=(username,password),verify=False,json=record)  
      print(" retry: " + str(retry) + " speed: " + str(speed) + " " + es )
    except:
      print(" retry: " + str(retry) + " : " + es + " : " + resp.text)
      return 0
    return 1


if __name__ == "__main__":
    Main()
