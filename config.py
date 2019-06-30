# ---------------- User Configuration Settings for speedcam2es.py ---------------------------------
#         Ver 0.0.1 speedcam2es.py Variable Configuration Settings
version = "0.0.1"
username = "chailey"
password = "chailey123"
elasticsearch_url = "https://jd:9243/chailey-"
timezone = "Europe/London"
db_path = '/home/pi/speed-camera/data/speed_cam.db'
db_table = 'speed'
report_query = ('''select * from speed order by idx desc''')
camera_name = "grantham_close_1"
