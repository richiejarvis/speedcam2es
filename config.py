# ---------------- User Configuration Settings for speedcam2es.py ---------------------------------
#         Ver 0.0.1 speedcam2es.py Variable Configuration Settings
version = "0.1.6"
username = "uk_chailey_grantham_3"
password = "MB4brekky"
elasticsearch_url = "https://6e6ab47cc78742cbbc275240f3edc97d.europe-west1.gcp.cloud.es.io:9243/chailey/"
timezone = "Europe/London"
db_path = '/home/pi/speed-camera/data/speed_cam.db'
db_table = 'speed'
report_query = ('''select * from speed order by idx desc limit 1''')
#report_query = ('''select * from speed where log_hour > strftime('%H',time('now')) and log_date = strftime('%Y%m%d',date('now')) order by idx desc''')
#report_query = ('''select * from speed where log_date = "20190629" order by idx desc''')
#report_query = ('''select * from speed where log_date = "20190629" order by idx ''')
#report_query = ('''select * from speed where log_date = "20190630" order by idx ''')
lat = "50.930"
lng = "-0.02"
speed_unit = "mph"
ssl_verify = False
debug = True
