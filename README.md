# speedcam2es

A simple python util to import data from the sqlite3 speed-cam database to Elasticsearch.

# Installation

git clone or unzip to preference.  Package `python-simplejson`,`python-requests` and their dependancies are required.

```
pi@pi:~/speedcam2es$ sudo apt install python-simplejson python-requests -y
```

# Execution

```
pi@picam2:~/speedcam2es$ ./speedcam2es.py
----------------------------------------------------------------------
speedcam2es.py 0.0.1   written by Richie Jarvis to work with Claude Pageau's speed_cam available here: https://github.com/pageauc/speed-camera
{'source': 'grantham_close_2', '@timestamp': u'2019-07-01T02:24:00Europe/London', 'speed': 47.19, 'direction': 'Northbound'}<Response [201]>
{'source': 'grantham_close_2', '@timestamp': u'2019-07-01T02:03:00Europe/London', 'speed': 66.59, 'direction': 'Southbound'}<Response [201]>
```
Response codes:
  * 200 => Record already exists - ignored
  * 201 => Record added
# Config
See config.py for the configuration options.  They should be mostly explanatory.  The SQL can be tweaked to taste.
# Todo
Work in progress...


