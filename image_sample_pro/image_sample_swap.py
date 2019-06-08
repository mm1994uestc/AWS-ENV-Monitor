from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import os 

print 'Raspberry GPIO initial...'
x_motor_pin_DIR = 15
x_motor_pin_STEP = 14
x_motor_pin_EN = 17

x_motor_speed = 0.005

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(x_motor_pin_DIR,GPIO.OUT)
GPIO.setup(x_motor_pin_STEP,GPIO.OUT)
GPIO.setup(x_motor_pin_EN,GPIO.OUT)

def motor_control(direction,step):
    if direction == 'up':
        print 'up',step
        #motor_4line_2phase(step,'CCW')
    if direction == 'down':
        print 'down',step
        #motor_4line_2phase(step,'CW')
    if direction == 'left':
        print 'left',step
        GPIO.output(x_motor_pin_EN,False)
        GPIO.output(x_motor_pin_DIR,True)
        for i in range(step):
            # print 'left circle'
            GPIO.output(x_motor_pin_STEP,True)
            time.sleep(x_motor_speed)
            GPIO.output(x_motor_pin_STEP,False)
            time.sleep(x_motor_speed)
        GPIO.output(x_motor_pin_EN,True)
    if direction == 'right':
        print 'right',step
        GPIO.output(x_motor_pin_EN,False)
        GPIO.output(x_motor_pin_DIR,False)
        for i in range(step):
            # print 'right circle!'
            GPIO.output(x_motor_pin_STEP,True)
            time.sleep(x_motor_speed)
            GPIO.output(x_motor_pin_STEP,False)
            time.sleep(x_motor_speed)
        GPIO.output(x_motor_pin_EN,True)

print 'Raspiberry Camera initial...'
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
camera.hflip = True
camera.vflip = True

pre_min = 0
min_update = 0

while True:
    date = time.localtime(time.time())
    if pre_min != date.tm_min:
        min_update = 1
        pre_min = date.tm_min
    if date.tm_hour % 1 == 0 and date.tm_min % 3 == 0 and min_update:
        min_update = 0
        print 'Current time:',date.tm_year,':',date.tm_mon,':',date.tm_mday,':',date.tm_hour,':',date.tm_min,':',date.tm_sec
        print 'image sampling...'

        for x in range(5):
            for y in range(5):
                motor_control('down',10)
                camera.capture(str(date.tm_hour)+'\''+str(date.tm_min)+'-X-'+str(x)+'Y-'+str(y)+'.jpg',use_video_port = False)
            motor_control('up',10)
            motor_control('right',1000)
        motor_control('left',1000)
