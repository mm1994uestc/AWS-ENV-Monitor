from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import serial
import time
import os 

Mashine_Name = 'P1'
print 'Mashine_Name:',Mashine_Name
print 'Raspberry GPIO initial...'

Camera_IR_Pin = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Camera_IR_Pin,GPIO.OUT)

def rpi2_usart_open(device,baudrate):
    return serial.Serial(device,baudrate)
def rpi2_usart_send(serial,data):
    # serial.flushOutput()
    serial.write(data)
    # serial.flushOutput()
def rpi2_usart_recv(serial,lenght):
    buffers = ''
    while True:
        FIFO_len = serial.inWaiting()
        # print "Waiting data:",FIFO_len
        if lenght <= FIFO_len:
            buffers = serial.read(FIFO_len)
            # serial.flushInput()
            break
    return buffers

CO2_dev = "/dev/ttyAMA0"
CO2_baud = 9600

def CO2_USART_Initial(CO2_dev,CO2_baud):
    return rpi2_usart_open(CO2_dev,CO2_baud)
def CO2_USART_GetValue(CO2_ser,CO2_CMD):
    CO2_BUF = ''
    rpi2_usart_send(CO2_ser,CO2_CMD)
    CO2_BUF = rpi2_usart_recv(CO2_ser,7)
                            
    H_Bits = ord(CO2_BUF[3])
    L_Bits = ord(CO2_BUF[4])
                            
    H_Bits_H = H_Bits>>4
    H_Bits_L = H_Bits&0x0F
    L_Bits_H = L_Bits>>4
    L_Bits_L = L_Bits&0x0F
                        
    return H_Bits_H*4096 + H_Bits_L*256 + L_Bits_H*16 + L_Bits_L

CO2_ser = CO2_USART_Initial(CO2_dev,CO2_baud)
CO2_CMD = chr(254)+chr(4)+chr(0)+chr(3)+chr(0)+chr(1)+chr(213)+chr(197)

x_n = 4
y_n = 8

x_distance = [0,58,100,100] # Unit:mm
y_distance = [0,20,115,115,115,115,115,35] # [0,60,115,115,115,115,115,40]

pre_min = 0
min_update = 0

print 'Initial the system...'

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
ser.flushInput()
ser.flushOutput()
Motor_CMD = dict({'x-right':'A','x-left':'B','y-down':'C','y-up':'D','x-init':'E','y-init':'F','stop':'S','Hold':'N'})
System_CMD = dict({'CO2-ON':'G','CO2-OFF':'H'})
print Motor_CMD,type(Motor_CMD),Motor_CMD['x-right']
timeout_count = 0
recv_data = 'N'
recv_n = 0

abs_path = "/home/pi/nexgen_pro/image_sample_pro/Raspberry_Arduino_Motor_Control/image_sample_Journal.log" # ADD-line
Journal = open(abs_path,'a')
Journal.write("################################## System Start:" + str(Start_Date.tm_year) + ':' + str(Start_Date.tm_mon) + ':' + str(Start_Date.tm_mday)+':' + str(Start_Date.tm_hour) + ':' + str(Start_Date.tm_min) + ':' + str(Start_Date.tm_sec) + " ###########################################\n")
Journal.close()

def ASK_Slave(serial,cmd_data):
    global recv_data,recv_n
    global abs_path
    timeout_count = 0
    timeout_total = 0
    print 'recv_n',recv_n
    print 'recv_data_B',recv_data
    while True:
        print "Motor is moving: ",timeout_count," times"
        time.sleep(0.5)
        recv_n = serial.inWaiting()
        print cmd_data,'&& recv_n:',recv_n
        if recv_n >= 2:
            recv_data = serial.read(recv_n)
            print recv_n,' && ',recv_data
            serial.flushInput()
            if 'OK' in recv_data and cmd_data[0] in recv_data:
                print 'recv_data_A',recv_data,'+',recv_n
                print 'Moving Finished.'
                recv_n = 0
                recv_data = 'N'
                serial.flushOutput()
                time.sleep(0.5) # 1
                Journal = open(abs_path,'a')
                Journal.write(cmd_data[0] + "->")
                Journal.close()
                break
            else:
                print "Wrong Control,Break!"
                recv_n = 0
                recv_data = 'N'
                serial.flushOutput()
        timeout_count += 1
        if timeout_count >= 600:
            print "No response Slave,Repeat send cmd please."
            serial.write(cmd_data)
            timeout_total += timeout_count
            timeout_count = 0
            Journal = open(abs_path,'a')
            if timeout_total <= 600:
                Journal.write("\nSlave No response for CMD:" + cmd_data[0] + " " + str(timeout_total) + " times,Repeat Send CMD...\n")
            else:
                Journal.write("\nSlave No response for CMD:" + cmd_data[0] + " " + str(timeout_total) + " times,Shutdown System...\n")
                died_time = time.localtime(time.time())
                Journal.write("System died at: "+str(died_time.tm_year)+':'+str(died_time.tm_mon)+':'+str(died_time.tm_mday)+':'+str(died_time.tm_hour)+':'+str(died_time.tm_min)+':'+str(died_time.tm_sec)+'.\n')
                os.system('sudo shudown -h now')
            Journal.close()

def Test_Motor(serial):
    print 'Testing Motor...'
    CMD_Send = Motor_CMD['x-left'] + chr(0)
    serial.write(CMD_Send)
    time.sleep(1.5)
    serial.write(Motor_CMD['x-init'])
    time.sleep(2)
    CMD_Send = Motor_CMD['y-down'] + chr(0)
    serial.write(CMD_Send)
    time.sleep(1.5)
    serial.write(Motor_CMD['y-init'])
    time.sleep(2)
    print 'Testing Motor Finished.'

def Motor_Control(serial,CMD_IN,distance):
    global Motor_CMD
    CMD_Send = CMD_IN + chr(distance) + '\0'
    print CMD_Send
    if 'S' == CMD_Send[0]:
        serial.write(Motor_CMD['stop'])
        ASK_Slave(serial,Motor_CMD['stop'])
        time.sleep(1.5)
    else:
        serial.write(CMD_Send)
        ASK_Slave(serial,CMD_Send)
        time.sleep(1)
    time.sleep(1)

print 'System Start Monitor...'
while True:
    date = time.localtime(time.time())
    if pre_min != date.tm_min:
        print "minutes update..."
        if date.tm_hour >= 8 and date.tm_hour < 19: # Judge the CO2 detect time.
            print "Monitor CO2..."
            Time_Point = str(date.tm_year)+'-'+str(date.tm_mon)+'-'+str(date.tm_mday)+'-'+str(date.tm_hour)+'-'+str(date.tm_min)+'-'+str(date.tm_sec) # ADD-line
            CO2_PPM = CO2_USART_GetValue(CO2_ser,CO2_CMD) # Get the CO2-Values form Raspiberry<--->CO2_Sensor.
            print Time_Point,':',CO2_PPM,'ppm'
            if CO2_PPM < 1000: # Judge the CO2 ppm
                Motor_Control(ser,'G',0); # Control the CO2-Delay status:ON
            elif CO2_PPM > 1200:
                Motor_Control(ser,'H',0); # Control the CO2-Delay status:OFF
        else:
            Motor_Control(ser,'H',0); # Control the CO2-Delay status:OFF
        min_update = 1
        pre_min = date.tm_min
    if date.tm_hour % 1 == 0 and date.tm_min % 59 == 0 and min_update:
        Motor_Control(ser,'H',0); # Control the CO2-Delay status:OFF
        if date.tm_hour > 19 or date.tm_hour < 8: # Set the Camera's IR Capture func.
            GPIO.output(Camera_IR_Pin,False)
            print 'IR mode is ON!'
        else:
            GPIO.output(Camera_IR_Pin,True)
            print 'IR mode is OFF!'
        Time_Start = time.time()
        Time_NOW = str(date.tm_year)+'-'+str(date.tm_mon)+'-'+str(date.tm_mday)+'-'+str(date.tm_hour)+'-'+str(date.tm_min)+'-'+str(date.tm_sec) # ADD-line
        Journal = open(abs_path,'a') # ADD-line
        Journal.write("Start sampling images:"+Time_NOW+'\n') # ADD-line
        Journal.close()
        min_update = 0
        print 'Current time:',Time_NOW
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
        Test_Motor(ser)
        for x in range(x_n):
            Motor_Control(ser,Motor_CMD['x-left'],x_distance[x]) # X-axis Going ON Positive
            for y in range(y_n):
                if x%2 == 0 and y == 0:
                    Motor_Control(ser,Motor_CMD['y-init'],0)
                if x%2 == 0 and y != 0:
                    Motor_Control(ser,Motor_CMD['y-down'],y_distance[y])
                    y_axis_lable += 1
                if x%2 != 0 and y != 0:
                    Motor_Control(ser,Motor_CMD['y-up'],y_distance[-y])
                    y_axis_lable -= 1
                print x_axis_lable,y_axis_lable
                path = "/home/pi/nexgen_pro/image_sample_pro/Raspberry_Arduino_Motor_Control/image_data/"+Position[y_axis_lable][x_axis_lable]+'/'+Mashine_Name+'_'+str(Start_Date.tm_year)+Start_month+Start_day+'_'+str(date.tm_year)+Current_month+Current_day+'_'+Current_hour+Current_min+'_'+Position[y_axis_lable][x_axis_lable]+'_V'+'_NU'+'.jpg'
                print 'Camera initilize...'
                Camera_Status = 'BUSY'
                while Camera_Status == 'BUSY':
                    print "Try RPi-Camera..."
                    try:
                        camera = PiCamera()
                        camera.resolution = (640,480)
                        camera.framerate = 32
                        camera.hflip = True
                        camera.vflip = True
                        camera.shutter_speed = 6000000
                        camera.iso = 20
                        camera.saturation = 0
                        camera.brightness = 50
                        camera.sharpness = 0
                        time.sleep(1)
                        camera.capture(path,use_video_port = False)
                        camera.close()
                        print 'Sample Successfully.'
                        Camera_Status = 'FREE'
                        pass
                    except Exception,e:
                        print 'Camera Wrong!'
                        Camera_Status = 'BUSY'
                        Journal = open(abs_path,'a')
                        Journal.write("Camera Wrong? "+str(Exception)+':'+str(e)+'\n')
                        Journal.close()
                        time.sleep(5)
                        pass
                Journal = open(abs_path,'a')
                Journal.write(path[83:]+'\n') # ADD-line
                Journal.close()
                print path
            x_axis_lable += 1
        Motor_Control(ser,Motor_CMD['x-init'],0)
        x_axis_lable = 0
        y_axis_lable = 0
        Time_End = time.time()
        TimeCost = (Time_End-Time_Start)/60
        print '################ Time cost: ',TimeCost,' minutes. ####################'
        Journal = open(abs_path,'a')
        Journal.write("Sample Finished.(TimeCost:"+str(TimeCost)+" mins)\n")
        Journal.close() # ADD-line
