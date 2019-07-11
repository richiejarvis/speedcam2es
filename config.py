# ---------------- User Configuration Settings for speedcam2es.py ---------------------------------
#          speedcam2es.py Variable Configuration Settings
version = "0.3.0"
username = "username"
password = "password"
elasticsearch_url = "https://host:port/index"
timezone = "Europe/London"
db_path = './data/speed_cam.db'
db_table = 'speed'
report_query = ('''select * from speed order by idx desc limit 1''')
#report_query = ('''select * from speed where log_hour > strftime('%H',time('now')) and log_date = strftime('%Y%m%d',date('now')) order by idx desc''')
#report_query = ('''select * from speed where log_date = "20190629" order by idx desc''')
#report_query = ('''select * from speed where log_date = "20190629" order by idx ''')
#report_query = ('''select * from speed where log_date = "20190630" order by idx ''')
lat = "50.0"
lng = "-0.00"
speed_unit = "mph"
ssl_verify = True
debug = True
