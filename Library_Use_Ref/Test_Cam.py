from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import os 

print 'Raspiberry Camera initial...'
'''
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
camera.hflip = True
camera.vflip = True
camera.close()
'''
while True:
    date = time.localtime(time.time())
    path = "/home/pi/"+str(date.tm_hour)+'\''+str(date.tm_min)+'.jpg'
    print path

    try:
        camera = PiCamera()
        print 'Camera Is OK!'
        camera.capture(path,use_video_port = False)
        camera.close()
        pass
    except Exception, e:
        print str(Exception),':',str(e)
        pass

    #camera = PiCamera()
    #camera.capture(path,use_video_port = False)
    time.sleep(5)
    #camera.close()
