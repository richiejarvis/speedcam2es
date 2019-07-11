#!/usr/bin/python3
import simplejson
import sqlite3
import time
import sys
import os
import hashlib
import urllib3

from elasticsearch import Elasticsearch
from elasticsearch import helpers

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

if ssl_verify == False:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

horz_line = "----------------------------------------------------------------------"
print(horz_line)
print("%s %s   written by Richie Jarvis to work with Claude Pageau's speed_cam available here: https://github.com/pageauc/speed-camera" % (prog_name, version))

def Main():
    records = read_db()
    debug_mode(records)  


def read_db():
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(report_query + " limit " + str(rows_limit))
    records = ""
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        if row["direction"] == "L2R":
            direction = "Southbound"
        else:
            direction = "Northbound"
        actual_time =  row["idx"]
        timestamp =  make_date(actual_time)
        speed = row["ave_speed"] 
        speed_unit = row["speed_units"]
        record = {"@timestamp" : timestamp,"actual_time": actual_time,"speed" : speed,"direction" : direction,"source" : es_username,"speed_unit" : speed_unit}
        records = records + str(record)
        debug_mode("t:%s" % (str(timestamp)))
        debug_mode("t:%s" % (str(record)))
    cursor.close()
    connection.close
    return records

def write_to_es(records):
    es = Elasticsearch([url],use_ssl=True,verify_certs=True,ssl_show_warn=True)
    # Could add a cacerts path here ^^
    es.indices.create(index=index_name,ignore=400)
        

        



def es_post(actual_time,record):
        hash_text = username + actual_time
        hash_obj = hashlib.md5(hash_text.encode())
        hash_obj = hash_obj.hexdigest()
        debug_mode("DEBUG: hash:%s" % (str(hash_obj)))

        url = (elasticsearch_url + hash_obj).lower()
        debug_mode("DEBUG: url:%s" % (str(url)))
        debug_mode("DEBUG: rec:%s" % (str(record)))
        resp = requests.post(url,auth=(username,password),verify=ssl_verify,data=record)
        debug_mode(resp.text)
        debug_mode("DEBUG: %s" % resp)
        resp_status_code = resp.status_code
        while resp_status_code not in (201,200):
            time.sleep(5)
            debug_mode("DEBUG: retry %s" % resp_status_code)
            es_post(actual_time,record)
            break
        return resp

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

def debug_mode(string):
    print("DBG:" + str(string))
    while True: break


if __name__ == "__main__":
    Main()
