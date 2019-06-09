from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import os 

print 'Raspberry GPIO initial...'

print 'X Motor:4000 pulse ===> 159mm : 0.03975 mm/pulse'
print 'Y Motor:4000 pulse ===> 159mm : 0.03975 mm/pulse'
x_mm_pp = 0.03975
y_mm_pp = 0.03975

x_motor_pin_DIR = 15
x_motor_pin_STEP = 14
x_motor_pin_EN = 17

y_motor_pin_AP = 18
y_motor_pin_AN = 23
y_motor_pin_BP = 24
y_motor_pin_BN = 25

x_motor_speed = 0.01
y_motor_speed = 0.0018

x_limit_trigger_pin  = 2
y_limit_trigger_pin  = 3

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(x_motor_pin_DIR,GPIO.OUT)
GPIO.setup(x_motor_pin_STEP,GPIO.OUT)
GPIO.setup(x_motor_pin_EN,GPIO.OUT)

GPIO.setup(y_motor_pin_AP,GPIO.OUT)
GPIO.setup(y_motor_pin_AN,GPIO.OUT)
GPIO.setup(y_motor_pin_BP,GPIO.OUT)
GPIO.setup(y_motor_pin_BN,GPIO.OUT)

GPIO.setup(x_limit_trigger_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(y_limit_trigger_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)

x_n = 3
y_n = 0

x_distance = [53,100,100] # Unit:mm
y_distance = [0]

x_step = []
y_step = []

for i in x_distance:
    x_step.append(int(i / x_mm_pp))
    
for i in y_distance:
    y_step.append(int(i / y_mm_pp))

print x_step,y_step

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
camera.hflip = False
camera.vflip = False

pre_min = 0
min_update = 0

def Motor_PowerOff(Motor):
    if Motor == 'x':
        GPIO.output(x_motor_pin_EN,True)
    if Motor == 'y':
        GPIO.output(y_motor_pin_AP,False)
        GPIO.output(y_motor_pin_AN,False)
        GPIO.output(y_motor_pin_BP,False)
        GPIO.output(y_motor_pin_BN,False)

def system_init(axis):
    if axis == 'x':
        while GPIO.input(x_limit_trigger_pin) == 1:
            motor_control('left',20)
            time.sleep(0.2)
        print 'axis x initial finished!'
        Motor_PowerOff('x')
    if axis == 'y':
        while GPIO.input(y_limit_trigger_pin) == 1:
            motor_control('up',20)
            time.sleep(0.2)
        print 'axis y initial finished!'
        Motor_PowerOff('y')

print 'Initial the system...'
system_init('x')
# system_init('y')

x_axis_lable = 1
y_axis_lable = 1

while True:
    date = time.localtime(time.time())
    if pre_min != date.tm_min:
        min_update = 1
        pre_min = date.tm_min
    if date.tm_hour % 1 == 0 and date.tm_min % 59 == 0 and min_update:
        min_update = 0
        print 'Current time:',date.tm_year,':',date.tm_mon,':',date.tm_mday,':',date.tm_hour,':',date.tm_min,':',date.tm_sec
        print 'image sampling...'

        for x in x_step:
            motor_control('right',x)
            time.sleep(1)
            Motor_PowerOff('x')
            for y in y_step:
                motor_control('down',y)
                Motor_PowerOff('y')
                time.sleep(1)
                path = "/home/pi/nexgen_pro/image_sample_pro/image_data/"+str(date.tm_hour)+'\''+str(date.tm_min)+'-X-'+str(x_axis_lable)+'Y-'+str(y_axis_lable)+'.jpg'
                y_axis_lable += 1
                camera.capture(path,use_video_port = False)
            x_axis_lable += 1
            motor_control('up',sum(y_step))
            time.sleep(0.5)
            Motor_PowerOff('y')
        motor_control('left',sum(x_step))
        system_init('x')
        x_axis_lable = 1
        y_axis_lable = 1
        # system_init('y')
