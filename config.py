--
#         speedcam2es.py Variable Configuration Settings
version = "0.0.3"
username = "grantham_close_1"
password = "MunchSpeedForBrekky"
elasticsearch_url = "https://e5fc3b57281449cf9b43aea35fb519fc.europe-west1.gcp.cloud.es.io:9243/chailey"
timezone = "Europe/London"
db_path = '/home/pi/speedcam2es/data/speed_cam.db'
db_table = 'speed'
report_query = ('''select * from speed order by idx''')
#report_query = ('''select * from speed order by idx desc''')
report_query = ('''select * from speed order by idx desc limit 100''')
#report_query = ('''select * from speed where log_hour = strftime('%H',time('now','+01:00')) and log_date = strftime('%Y%m%d',date('now')) order by idx desc''')
#report_query = ('''select * from speed where log_date = strftime('%Y%m%d',date('now')) order by idx desc''')
l2r_direction = "Southbound"
r2l_direction = "Northbound"
lat = 50.937186
lng = -0.029988
