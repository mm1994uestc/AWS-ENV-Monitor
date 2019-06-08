from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import os

print 'Raspiberry Camera initial...'
camera = PiCamera()
camera.resolution = (240,190)
camera.framerate = 32
camera.hflip = True
camera.vflip = True

date = time.localtime(time.time())
print 'Current time:',date.tm_year,':',date.tm_mon,':',date.tm_mday,':',date.tm_hour,':',date.tm_min,':',date.tm_sec
camera.capture(str(date.tm_hour)+'\''+str(date.tm_min)+'.jpg',use_video_port = False)
