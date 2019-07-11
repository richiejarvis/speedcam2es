# ---------------- User Configuration Settings for speedcam2es.py ---------------------------------
#          speedcam2es.py Variable Configuration Settings
version = "0.3.0"
username = "uk_chailey_grantham_3"
password = "MB4brekky"
elasticsearch_url = "https://jd:9243/chailey-"
timezone = "Europe/London"
db_path = './data/speed_cam.db'
db_table = 'speed'
report_query = ('''select * from speed order by idx desc limit 100''')
#report_query = ('''select * from speed where log_hour > strftime('%H',time('now')) and log_date = strftime('%Y%m%d',date('now')) order by idx desc''')
#report_query = ('''select * from speed where log_date = "20190629" order by idx desc''')
#report_query = ('''select * from speed where log_date = "20190629" order by idx ''')
#report_query = ('''select * from speed where log_date = "20190630" order by idx ''')
lat = "50.930"
lng = "-0.02"
speed_unit = "mph"
ssl_verify = False
debug = True
