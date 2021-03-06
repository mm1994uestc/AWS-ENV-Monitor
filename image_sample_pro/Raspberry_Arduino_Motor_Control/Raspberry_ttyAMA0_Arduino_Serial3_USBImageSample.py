# -*- coding:utf-8 -*-
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import serial
import time
import os 
import cv2

import socket
import urllib
import thread
import threading
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-+8')

host = '192.168.101.121'
print(host)
port = 5000

ENV_Len = 8
ENV_Status = [0,10000,2,23,43,321,498,54]

def isfloat(f_str):
    part = f_str.partition('.')
    if (part[0].isdigit() and part[1] == '.' and part[2].isdigit()) or (part[0].isdigit() and part[1] == '' and part[2] == '') or (part[0] == '' and part[1] == '.' and part[2].isdigit()) or (part[0].isdigit() and part[1] == '.' and part[2] == ''):
        return 1
    else:
        return 0

def Communicate(info):
    if info == 'G' or  info == 'Get' or  info == 'GET':
        threadLock.acquire()
        ENV_DATA = ''
        for i in range(ENV_Len):
            ENV_DATA += str(ENV_Status[i])
            ENV_DATA += '|'
        threadLock.release()
        return ENV_DATA
    else:
        return ''
def Server_Socket(host,port):
    Socket_status = 'BUSY'
    while True:
        while Socket_status == 'BUSY':
            try:
                clnt = ''
                addr = ''
                Sk = socket.socket()
                Sk.bind((host, port))
                Sk.listen(1)
                clnt, addr = Sk.accept()
                # print('Address is:', addr)
                # print('I am waiting for Client...')
                Socket_status = 'FREE'
                pass
            except Exception:
                print('Try Socket Error:',Exception)
                Socket_status = 'BUSY'
                pass
        print('Getting a new Connect!')
        while Socket_status == 'FREE':
            data = clnt.recv(1024)
            recv_n = len(data)
            # print('Going to:', data , ' Len: ', recv_n)
            if recv_n == 0:
                Sk.close()
                print('Server Socket Closed!')
                Socket_status = 'BUSY'
                break
            result = Communicate(data)
            if len(result) == 0:
                result = 'EXD'
            clnt.sendall(result)
    Sk.close()


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

# CO2_ser = CO2_USART_Initial(CO2_dev,CO2_baud) # Before you use the RPi-CO2 Sensor Please Initial the USART-ttyAMA0
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

Motor_CMD = dict({'x-right':'A','x-left':'B','y-down':'C','y-up':'D','x-init':'E','y-init':'F','stop':'S','Hold':'N'})
System_CMD = dict({'CO2-ON':'G','CO2-OFF':'H'})
print Motor_CMD,type(Motor_CMD),Motor_CMD['x-right']
timeout_count = 0
recv_data = 'N'
recv_n = 0

abs_path = "/home/pi/nexgen_pro/image_sample_pro/Raspberry_Arduino_Motor_Control/image_sample_Journal.log" # ADD-line

def Journal_log(log,path='?'):
    DefaultPath = "/home/pi/nexgen_pro/image_sample_pro/Raspberry_Arduino_Motor_Control/image_sample_Journal.log"
    if path == '?':
        path = DefaultPath
    Journal = open(path,'a')
    Journal.write(log)
    Journal.close()
def Get_time_str(separator,struct=''):
    if struct == '':
        time_struct_val = time.localtime(time.time())
        return str(time_struct_val.tm_year) + separator + str(time_struct_val.tm_mon) + separator + str(time_struct_val.tm_mday)+ separator + str(time_struct_val.tm_hour) + separator + str(time_struct_val.tm_min) + separator + str(time_struct_val.tm_sec) 
    return str(struct.tm_year) + separator + str(struct.tm_mon) + separator + str(struct.tm_mday)+ separator + str(struct.tm_hour) + separator + str(struct.tm_min) + separator + str(struct.tm_sec)

Journal_log(log="################################## System Start:" + Get_time_str(':',Start_Date) + "###########################################\n")

def ASK_Slave(serial,cmd_data):
    global recv_data,recv_n
    global abs_path
    timeout_count = 0
    timeout_total = 0
    #print 'recv_n',recv_n
    #print 'recv_data_B',recv_data
    recv_n = 0
    recv_data = 'N'
    while True:
        #print "Motor is moving: ",timeout_count," times"
        time.sleep(0.5)
        USART_Status = 'BUSY'
        inWaiting_count = 0
        while USART_Status == 'BUSY':
            try:
                recv_n = serial.inWaiting()
                USART_Status = 'FREE'
                inWaiting_count = 0
                pass
            except Exception,e:
                #print 'USART Wrong!'
                USART_Status = 'BUSY'
                Journal_log(log=Get_time_str(':')+"-USART Error:"+str(Exception)+str(e)+'\n')
                inWaiting_count += 1
                if inWaiting_count > 3:
                    inWaiting_count = 0
                    #print 'Goto Repeate CMD Send.'
                    break
                time.sleep(3)
                pass
        #print cmd_data,'&& recv_n:',recv_n
        if recv_n >= 2:
            recv_data = serial.read(recv_n)
            #print recv_n,' && ',recv_data
            serial.flushInput()
            if 'OK' in recv_data and cmd_data[0] in recv_data:
                #print 'recv_data_A',recv_data,'+',recv_n
                #print 'Moving Finished.'
                recv_data_return = recv_data
                recv_n = 0
                recv_data = 'N'
                serial.flushOutput()
                time.sleep(0.5) # 1
                return recv_data_return
            else:
                #print "Wrong Control,Break!"
                recv_n = 0
                recv_data = 'N'
                serial.flushOutput()
        timeout_count += 1
        if timeout_count >= 30:
            #print "No response Slave,Repeat send cmd please."
            serial.write(cmd_data)
            timeout_total += timeout_count
            timeout_count = 0
            if timeout_total <= 60:
                Journal_log(log="Slave No response for CMD:" + cmd_data[0] + " " + str(timeout_total) + " times,Repeat Send CMD...\n")
            else:
                Journal_log(log="Slave No response for CMD:" + cmd_data[0] + " " + str(timeout_total) + " times,Shutdown System...\n")
                died_time = time.localtime(time.time())
                Journal_log(log="System died at: "+ Get_time_str(':') +'.\n')
                os.system('sync')
                #print 'sudo shutdown -r now'
                time.sleep(1)
                os.system('sudo shutdown -r now')

def Test_Motor(serial):
    #print 'Testing Motor...'
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
    #print 'Testing Motor Finished.'

def Motor_Control(serial,CMD_IN,distance):
    global Motor_CMD
    ser_state = 1
    CMD_Res = "Error"
    CMD_Send = CMD_IN + chr(distance) + '\0'
    #print CMD_Send
    try:
        if 'S' == CMD_Send[0]:
            serial.write(Motor_CMD['stop'])
            ASK_Slave(serial,Motor_CMD['stop'])
            time.sleep(1.5)
        else:
            serial.write(CMD_Send)
            CMD_Res = ASK_Slave(serial,CMD_Send)
            time.sleep(1)
            pass
    except:
            #print "ser is wrong!"
            Journal_log(log=Get_time_str(':')+"Motor_Control(ser," + CMD_Send + ") Func Failed\n")
            ser_state = 0
    time.sleep(1)
    return CMD_Res,ser_state

def Serial_Get():
    USB_dev = ''
    find_count = 0
    while USB_dev == '':
        dev_list = os.listdir('/dev/')
        for dev in dev_list:
            if 'ttyAMA' in dev: # If use the ttyUSBx device please change it to be 'USB'
                USB_dev = dev
                #print 'USB device founded:',USB_dev
                find_count = 0
                break
        find_count += 1
        if find_count >= 30:
            Journal_log(log=Get_time_str(':')+'-Error:Arduino Device Not Founded.Restart Arduino.\n')
            #print 'Restart the Arduino Power supply by raspberry\'s GPIO Directly.'
            find_count = 0
        time.sleep(1)
    serial_dev = '/dev/' +  USB_dev
    Serial_Status = 'BUSY'
    while Serial_Status == 'BUSY':
        try:
            ser = serial.Serial(serial_dev, 9600)
            Serial_Status = 'FREE'
            #print 'Serial Opened Successful.'
            pass
        except Exception,e:
            #print 'Serial Opend Failed!Try again.'
            Serial_Status = 'BUSY'
            Journal_log(log=Get_time_str(':')+'-Serial Error:'+str(Exception)+str(e)+'\n')
            time.sleep(5)
            pass
    ser.flushInput()
    ser.flushOutput()
    return ser

print 'System Start Monitor...'
CO2_Status = '?'
RPi_CO2 = False
ser = Serial_Get()
Motor_Control(ser,'M',0) # Close the whilt light.
Motor_Control(ser,'O',0) # Close the UV.
CO2_PPM = 0
PH_val = 0
EC_val = 0
Humi_val = 0
Temp_val = 0
while True:
    threadLock = threading.Lock()
    try:
        thread.start_new_thread(Server_Socket,(host,port,))
        pass
    except e:
        #print('Thread Create Failed! Main Finished.')
        break
    time.sleep(2)
    #os.system('python2 /home/pi/nexgen_pro/image_sample_pro/Raspberry_Arduino_Motor_Control/Sys_Status_MysqlSave.py > /dev/null &')
    while True:
        date = time.localtime(time.time())
        if date.tm_sec % 5 == 0:
            #print 'Start ENV_TABLE Updating...'
            if RPi_CO2:
                CO2_PPM = CO2_USART_GetValue(CO2_ser,CO2_CMD) # Get the CO2-Values form Raspiberry<--->CO2_Sensor.
            else:
                #ser = Serial_Get()
                CMD_Res = Motor_Control(ser,'K',0) # K CO2:493OK-KCO2
                #ser.close()
                if CMD_Res[1] == 0:
                    ser.close()
                    time.sleep(2)
                    ser = Serial_Get()
                    CO2_STR = "CO2:1500OK-KCO2" # the CO2 Value should bigger than 1200.
                else:
                    CO2_STR = CMD_Res[0]
                CO2_Start_Index = CO2_STR.find(':') + 1
                CO2_End_Index = CO2_STR.find('OK')
                CO2_PPM = int(float(CO2_STR[CO2_Start_Index:CO2_End_Index]))

            CMD_Res = Motor_Control(ser,'I',0)
            # print type(CMD_Res),':',CMD_Res
            PH_Start_Index = CMD_Res[0].find(':') + 1
            PH_End_Index = CMD_Res[0].find('OK')
            f_str = CMD_Res[0][PH_Start_Index:PH_End_Index]
            if isfloat(f_str) == 1:
                PH_val = int(float(CMD_Res[0][PH_Start_Index:PH_End_Index]) * 10)
            else:
                Journal_log(log=Get_time_str(':')+'-PH Val Error:'+f_str+'\n')
                PH_val = 8

            CMD_Res = Motor_Control(ser,'J',0)
            # print type(CMD_Res),':',CMD_Res,
            EC_Start_Index = CMD_Res[0].find(':') + 1
            EC_End_Index = CMD_Res[0].find('OK')
            f_str = CMD_Res[0][EC_Start_Index:EC_End_Index]
            if isfloat(f_str) == 1:
                EC_val = int(float(CMD_Res[0][EC_Start_Index:EC_End_Index]) * 100)
            else:
                Journal_log(log=Get_time_str(':')+'-EC Val Error:'+f_str+'\n')
                EC_val = 111

            CMD_Res = Motor_Control(ser,'Y',0)
            Humi_Start_Index = CMD_Res[0].find(':') + 1
            Humi_End_Index = CMD_Res[0].find('OK')
            f_str = CMD_Res[0][Humi_Start_Index:Humi_End_Index]
            if isfloat(f_str) == 1:
                Humi_val = int(float(CMD_Res[0][Humi_Start_Index:Humi_End_Index]) * 100)
            else:
                Journal_log(log=Get_time_str(':')+'-Humi Val Error:'+f_str+'\n')
                Humi_val = 9999

            CMD_Res = Motor_Control(ser,'Z',0)
            Temp_Start_Index = CMD_Res[0].find(':') + 1
            Temp_End_Index = CMD_Res[0].find('OK')
            f_str = CMD_Res[0][Temp_Start_Index:Temp_End_Index]
            if isfloat(f_str) == 1:
                Temp_val = int(float(CMD_Res[0][Temp_Start_Index:Temp_End_Index]) * 100)
            else:
                Journal_log(log=Get_time_str(':')+'-Temp Val Error:'+f_str+'\n')
                Temp_val = 9999

            time_stamp = date.tm_mon * 100000000 + date.tm_mday * 1000000 + date.tm_hour * 10000 + date.tm_min * 100 + date.tm_sec
            threadLock.acquire()
            ENV_Status[0] = time_stamp
            ENV_Status[1] = Temp_val
            ENV_Status[2] = Humi_val
            ENV_Status[3] = CO2_PPM
            ENV_Status[4] = PH_val
            ENV_Status[5] = EC_val
            ENV_Status[6] = 100
            threadLock.release()
            #print('ENV VALUE:',ENV_Status[0],'|',ENV_Status[1],'|',ENV_Status[2],'|',ENV_Status[3],'|',ENV_Status[4],'|',ENV_Status[5],'|',ENV_Status[6],'|',ENV_Status[7])
        if pre_min != date.tm_min:
            #print "minutes update..."
            if date.tm_hour % 6 == 0 and date.tm_min == 20:
                Motor_Control(ser,'N',0) # Open the UV.
            if date.tm_hour % 6 == 0 and date.tm_min == 40:
                Motor_Control(ser,'O',0) # Close the UV.
            if date.tm_hour >= 8 and date.tm_hour < 22: # Judge the CO2 detect time. 8-19
                if CO2_PPM < 1000: # Judge the CO2 ppm
                    if CO2_Status != 'G':
                        #ser = Serial_Get()
                        Motor_Control(ser,'G',0) # Control the CO2-Delay status:ON
                        #ser.close()
                        CO2_Status = 'G'
                elif CO2_PPM > 1200:
                    if CO2_Status != 'H':
                        #ser = Serial_Get()
                        Motor_Control(ser,'H',0) # Control the CO2-Delay status:OFF
                        CO2_Status = 'H'
                        #ser.close()
            else:
                if CO2_Status != 'H':
                    #ser = Serial_Get()
                    Motor_Control(ser,'H',0) # Control the CO2-Delay status:OFF
                    CO2_Status = 'H'
                    #ser.close()
            min_update = 1
            pre_min = date.tm_min # >=8 <19
        if date.tm_hour % 1 == 0 and date.tm_min % 59 == 0 and min_update and date.tm_hour >= 7 and date.tm_hour < 19: # 19
            ser.close() # Add line
            time.sleep(2) # Wait for Serial been closed.
            ser = Serial_Get()
            Motor_Control(ser,'H',0); # Control the CO2-Delay status:OFF
            Motor_Control(ser,'L',0); # ON the whilte light.
            # Motor_Control(ser,'N',0); # UV.
            Motor_Control(ser,'P',0); # OFF the GrowLight2.
            CO2_Status = 'H'
            if date.tm_hour > 19 or date.tm_hour < 8: # Set the Camera's IR Capture func.
                GPIO.output(Camera_IR_Pin,False)
                #print 'IR mode is ON!'
            else:
                GPIO.output(Camera_IR_Pin,True)
                #print 'IR mode is OFF!'
            Time_Start = time.time()
            Time_NOW = Get_time_str('-',date)
            Journal_log(log="Start sampling images:"+Time_NOW+'\n') # ADD-line
            min_update = 0
            #print 'Current time:',Time_NOW
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

            #print 'image sampling...'
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
                    #print x_axis_lable,y_axis_lable
                    path_prefix = "/home/pi/nexgen_pro/image_sample_pro/Raspberry_Arduino_Motor_Control/image_data/"
                    path = path_prefix + Position[y_axis_lable][x_axis_lable]+'/'+Mashine_Name+'_'+str(Start_Date.tm_year)+Start_month+Start_day+'_'+str(date.tm_year)+Current_month+Current_day+'_'+Current_hour+Current_min+'_'+Position[y_axis_lable][x_axis_lable]+'_V'+'_NU'+'.jpg'
                    #print 'Camera initilize...'
                    if os.path.exists('/dev/video0') == False:
                        #print "No vodeo0 device!Try agine."
                        Journal_log(log="Camera Device Not Exist.")
                        sys.exit(2)
                    Camera_Status = 'BUSY'
                    cap = cv2.VideoCapture(0)
                    time.sleep(0.2) # Unit:s
                    while Camera_Status == 'BUSY':
                        #print "Try USB-Camera..."
                        try:
                            ret,frame = cap.read()
                            cv2.imwrite(path,frame)
                            cap.release()
                            #print 'Sample Successfully.'
                            Camera_Status = 'FREE'
                            pass
                        except Exception,e:
                            #print 'Camera Wrong!'
                            Camera_Status = 'BUSY'
                            Journal_log(log=Get_time_str(':') + "-USBCamera Wrong? "+str(Exception)+':'+str(e)+'\n')
                            time.sleep(10)
                            pass
                    Journal_log(log=path[83:]+'\n') # ADD-line
                    #print path
                x_axis_lable += 1
            Motor_Control(ser,Motor_CMD['x-init'],0)
            Motor_Control(ser,'M',0)
            # Motor_Control(ser,'O',0) # OFF UV
            Motor_Control(ser,'Q',0)
            # ser.close()
            #print "Serial been Closed now."
            x_axis_lable = 0
            y_axis_lable = 0
            Time_End = time.time()
            TimeCost = (Time_End-Time_Start)/60
            #print '################ Time cost: ',TimeCost,' minutes. ####################'
            Journal_log(log="Sample Finished.(TimeCost:"+str(TimeCost)+" mins)\n")
