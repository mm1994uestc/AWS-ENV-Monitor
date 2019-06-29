from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import serial
import time
import os 

Mashine_Name = 'P1'
print 'Mashine_Name:',Mashine_Name
print 'Raspberry GPIO initial...'

print 'X Motor:4000 pulse ===> 159mm : 0.06956 mm/pulse'
print 'Y Motor:4000 pulse ===> 159mm : 0.03975 mm/pulse'
x_mm_pp = 0.0711
y_mm_pp = 0.0625

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
y_n = 7

x_distance = [43,100,100] # Unit:mm
y_distance = [75,115,115,115,115,115,60]

x_step = [0]
y_step = [0]

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
#camera.framerate = 32
camera.hflip = True
camera.vflip = True
#camera.shutter_speed=6000000
camera.iso=20
camera.saturation=0
camera.brightness=50
camera.sharpness=0

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
            motor_control('left',15)
            time.sleep(0.2)
        print 'axis x initial finished!'
        Motor_PowerOff('x')
    if axis == 'y':
        while GPIO.input(y_limit_trigger_pin) == 1:
            motor_control('up',15)
            time.sleep(0.2)
        print 'axis y initial finished!'
        Motor_PowerOff('y')

print 'Initial the system...'
system_init('x')
# system_init('y')

x_axis_lable = 0
y_axis_lable = 0

Position = [['A1','B1','C1','D1'],['A2','B2','C2','D2'],['A3','B3','C3','D3']\
        ,['A4','B4','C4','D4'],['A5','B5','C5','D5'],['A6','B6','C6','D6']\
        ,['A7','B7','C7','D7'],['A8','B8','C8','D8']]

Start_Date = time.localtime(time.time())

if Start_Date.tm_mon >= 10:
    Start_month = str(Start_Date.tm_mon)
else:
    Start_month = '0' + str(Start_Date.tm_mon)

if Start_Date.tm_mday >= 10:
    Start_day = str(Start_Date.tm_mday)
else:
    Start_day = '0' + str(Start_Date.tm_mday)

ser = serial.Serial("/dev/ttyUSB0", 9600)
CMD = ['A','B','C','D','E','F','N']
while True:
    date = time.localtime(time.time())
    if pre_min != date.tm_min:
        min_update = 1
        pre_min = date.tm_min
    if date.tm_hour % 1 == 0 and date.tm_min % 59 == 0 and min_update:
        min_update = 0
        print 'Current time:',date.tm_year,':',date.tm_mon,':',date.tm_mday,':',date.tm_hour,':',date.tm_min,':',date.tm_sec
        if date.tm_mon >= 10:
            Current_month = str(date.tm_mon)
        else:
            Current_month = '0' + str(date.tm_mon)
        if date.tm_mday >= 10:
            Current_day = str(date.tm_mday)
        else:
            Current_day = '0' + str(date.tm_mday)
        if date.tm_hour >= 10:
            Current_hour = str(date.tm_hour)
        else:
            Current_hour = '0' + str(date.tm_hour)
        if date.tm_min >= 10:
            Current_min = str(date.tm_min)
        else:
            Current_min = '0' + str(date.tm_min)
        print 'image sampling...'
        
        for x in x_step:
            CMD_Send = CMD[0] + chr(x_distance[x]) + '\0'
            print  CMD_Send
            ser.write(CMD_Send) # X-axis Going ON Positive
            CMD_Send = CMD[7]
            time.sleep(1)
            # Motor_PowerOff('x')
            for y in y_step:
                CMD_Send = CMD[2] + chr(y_distance[y]) + '\0'
                print  CMD_Send
                ser.write(CMD_Send) # X-axis Going ON Positive
                CMD_Send = CMD[7]
                # Motor_PowerOff('y')
                time.sleep(1)
                print x_axis_lable,y_axis_lable
                path = "/home/pi/nexgen_pro/image_sample_pro/image_data/"+Mashine_Name+'_'+str(Start_Date.tm_year)+Start_month+Start_day+'_'+str(date.tm_year)+Current_month+Current_day+'_'+Current_hour+Current_min+'_'+Position[y_axis_lable][x_axis_lable]+'_V'+'_NU'+'.jpg'
                y_axis_lable += 1
                camera.capture(path,use_video_port = False)
            x_axis_lable += 1
            y_axis_lable = 0
            CMD_Send = CMD[4] + '\0'
            ser.write(CMD_Send)
            # motor_control('up',sum(y_step))
            time.sleep(0.5)
            # Motor_PowerOff('y')
        # motor_control('left',sum(x_step)-100)
        CMD_Send = CMD[5] + '\0'
        ser.write(CMD_Send)
        system_init('x')
        x_axis_lable = 0
        y_axis_lable = 0