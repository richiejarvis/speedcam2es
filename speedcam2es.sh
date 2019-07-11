#!/bin/bash
# Make a copy of the db prior to reading it, to avoid lock issues
rm -f /home/pi/speedcam2es/*.pyc
cp /home/pi/speed-camera/data/speed_cam.db /home/pi/speedcam2es/data/speed_cam.db >> /home/pi/speedcam2es/log/speed_cam.log
/home/pi/speedcam2es/speedcam2es.py
