# ---------------- User Configuration Settings for speedcam2es.py ---------------------------------
#         Ver 0.0.1 speedcam2es.py Variable Configuration Settings
version = "0.0.1"
username = "chailey"
password = "chailey123"
elasticsearch_url = "https://jd:9243/chailey-"
timezone = "Europe/London"
db_path = '/home/pi/speed-camera/data/speed_cam.db'
db_table = 'speed'
#report_query = ('''select * from speed order by idx desc''')
report_query = ('''select * from speed where log_hour > strftime('%H',time('now')) and log_date = strftime('%Y%m%d',date('now')) order by idx desc''')
#report_query = ('''select * from speed where log_date = "20190629" order by idx desc''')
#report_query = ('''select * from speed where log_date = "20190629" order by idx ''')
#report_query = ('''select * from speed where log_date = "20190630" order by idx ''')
camera_name = "grantham_close_2"
lat = "50.930"
long = "-0.02"
