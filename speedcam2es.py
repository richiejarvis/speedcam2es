#!/usr/bin/python
import simplejson
import sqlite3
import time
import sys
import os
import hashlib
import requests
import urllib3
from config import *
# Retry Counter
retry = 0
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Find the full path of this python script
my_path = os.path.abspath(__file__)  # Find the full path of this python script
# get the path location only (excluding script name)
base_dir = my_path[0:my_path.rfind("/")+1]
base_file_name = my_path[my_path.rfind("/")+1:my_path.rfind(".")]
prog_name = os.path.basename(__file__)
# Check for variable file to import and error out if not found.
config_file_path = os.path.join(base_dir, "config.py")
if not os.path.exists(config_file_path):
  print("ERROR : Someone nicked my config.py file - File Not Found %s" % config_file_path)
  config_url = "https://raw.githubusercontent.com/richiejarvis/speedcam2es/master/config.py"
  print("INFO  : Auto-restore of config.py file from %s" % config_url)
  try:
    wgetfile = urllib2.urlopen(config_url)
  except:
    print("ERROR : D'oh Download of config.py Failed")
    print("        %s Exiting Due to Error" % version)
    sys.exit(1)
  f = open("config.py", "wb")
  f.write(wgetfile.read())
  f.close()

def Main():
  print("Author: My attempt at an Elasticsearch ingestion engine")
  print("Version: %s" % (version))
  print("Author: Richie Jarvis")
  print("Date: 2019-07-01")
  print("GitHub: https://github.com/richiejarvis/speedcam2es")
  print("Description: Convert speed-camera.py sqlite3 db to Elasticsearch Document.  With thanks to speed-camera.py written by Claude Pageau:  https://github.com/pageauc/speed-camera")
  while retry_count >= retry:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(report_query)
    row_count = 0
    record = ""
    print("Retries left: %s" % retry_count)
    while True:
      row_count += 1
      row = cursor.fetchone()
      if row is None: 
        break
      direction = row["direction"]
      timestamp = make_date(row["idx"])
      speed = row["ave_speed"]
  # DB scrape done... mv alng
  unique_hash = hashlib.sha1(str(speed)).hexdigest()
  print("DEBUG: speed: %s hash: %s" % (speed, unique_hash))
  if direction == "L2R": 
    direction = r2l_direction 
  else:
    direction = l2r_direction 
  # Got everything we need - print it
  record = { '@timestamp' : timestamp, 'speed' : speed, 'direction' : direction, 'source' : username, 'lat': lat, 'lng': lng }
  url = str(elasticsearch_url + "/record/")
  status == 1
  while status == 0:
    status = es_post(url,record,speed,retry)
  cursor.close()
  connection.close
  print("voila")

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
 unique_hash = hashlib.sha1(es + str(retry_count)).hexdigest()
 try:
  resp = requests.post(es,auth=(username,password),verify=False,json=record)
  print(" Rtry: " + str(retry) + " spd: " + str(speed) + " " + unique_hash )
  retry =+ 1
 except:
  return 0
  pass
 return 1
if __name__ == "__main__":
    Main()
