#!/bin/bash
watch -d "sqlite3 /home/pi/speed-camera/data/speed_cam.db 'select * from speed order by idx desc limit 10'"
