# speedcam2es.py Variable Configuration Settings
version = "0.1.4"
retry_count = 2
username = "grantham_close_1"
password = "MunchSpeedForBrekky"
elasticsearch_url = "https://e5fc3b57281449cf9b43aea35fb519fc.europe-west1.gcp.cloud.es.io:9243/chailey"
timezone = "Europe/London"
db_path = "/home/pi/speedcam2es/data/speed_cam.db"
db_table = "speed"
report_query = ('''select * from speed''')
l2r_direction = "Southbound"
r2l_direction = "Northbound"
lat = 50.937186
lng = -0.029988
