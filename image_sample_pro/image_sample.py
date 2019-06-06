from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import os 

print 'Raspberry GPIO initial...'
x_motor_pin_DIR = 15
x_motor_pin_STEP = 14
x_motor_pin_EN = 17

y_motor_pin_AP = 18
y_motor_pin_AN = 23
y_motor_pin_BP = 24
y_motor_pin_BN = 25

x_motor_speed = 0.005
y_motor_speed = 0.002

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(x_motor_pin_DIR,GPIO.OUT)
GPIO.setup(x_motor_pin_STEP,GPIO.OUT)
GPIO.setup(x_motor_pin_EN,GPIO.OUT)

GPIO.setup(y_motor_pin_AP,GPIO.OUT)
GPIO.setup(y_motor_pin_AN,GPIO.OUT)
GPIO.setup(y_motor_pin_BP,GPIO.OUT)
GPIO.setup(y_motor_pin_BN,GPIO.OUT)

x_n = 5
y_n = 10
x_distance = 1000
y_distance = 1000

def motor_4line_2phase(step, direction):
    if direction == 'CW': # Clockwise direction
        for i in range(step):
            GPIO.output(y_motor_pin_AP,True)
            GPIO.output(y_motor_pin_AN,False)
            GPIO.output(y_motor_pin_BP,False)
            GPIO.output(y_motor_pin_BN,True)
            time.sleep(y_motor_speed)
            GPIO.output(y_motor_pin_AP,True)
            GPIO.output(y_motor_pin_AN,False)
            GPIO.output(y_motor_pin_BP,True)
            GPIO.output(y_motor_pin_BN,False)
            time.sleep(y_motor_speed)
            GPIO.output(y_motor_pin_AP,False)
            GPIO.output(y_motor_pin_AN,True)
            GPIO.output(y_motor_pin_BP,True)
            GPIO.output(y_motor_pin_BN,False)
            time.sleep(y_motor_speed)
            GPIO.output(y_motor_pin_AP,False)
            GPIO.output(y_motor_pin_AN,True)
            GPIO.output(y_motor_pin_BP,False)
            GPIO.output(y_motor_pin_BN,True)
            time.sleep(y_motor_speed)
    if direction == 'CCW': # Counter-clockwise direcion
        for i in range(step):
            GPIO.output(y_motor_pin_AP,False)
            GPIO.output(y_motor_pin_AN,True)
            GPIO.output(y_motor_pin_BP,False)
            GPIO.output(y_motor_pin_BN,True)
            time.sleep(y_motor_speed)
            GPIO.output(y_motor_pin_AP,False)
            GPIO.output(y_motor_pin_AN,True)
            GPIO.output(y_motor_pin_BP,True)
            GPIO.output(y_motor_pin_BN,False)
            time.sleep(y_motor_speed)
            GPIO.output(y_motor_pin_AP,True)
            GPIO.output(y_motor_pin_AN,False)
            GPIO.output(y_motor_pin_BP,True)
            GPIO.output(y_motor_pin_BN,False)
            time.sleep(y_motor_speed)
            GPIO.output(y_motor_pin_AP,True)
            GPIO.output(y_motor_pin_AN,False)
            GPIO.output(y_motor_pin_BP,False)
            GPIO.output(y_motor_pin_BN,True)
            time.sleep(y_motor_speed)

def motor_control(direction,step):
    if direction == 'up':
        print 'up',step
        motor_4line_2phase(step,'CCW')
    if direction == 'down':
        print 'down',step
        motor_4line_2phase(step,'CW')
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

while True:
    date = time.localtime(time.time())
    if pre_min != date.tm_min:
        min_update = 1
        pre_min = date.tm_min
    if date.tm_hour % 1 == 0 and date.tm_min % 2 == 0 and min_update:
        min_update = 0
        print 'Current time:',date.tm_year,':',date.tm_mon,':',date.tm_mday,':',date.tm_hour,':',date.tm_min,':',date.tm_sec
        print 'image sampling...'

        for x in range(5):
            for y in range(5):
                motor_control('down',y_distance)
                camera.capture(str(date.tm_hour)+'\''+str(date.tm_min)+'-X-'+str(x)+'Y-'+str(y)+'.jpg',use_video_port = False)
            motor_control('up',y_n*y_distance)
            motor_control('right',x_distance)
        motor_control('left',x_n*x_distance)
