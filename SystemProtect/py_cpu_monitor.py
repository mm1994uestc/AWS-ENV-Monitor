import os
import sys
# import RPi.GPIO as GPIO
import time
import psutil

#fans_Control pin initial

heart_pin = 17
'''
def heart_led_init(PinNum):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PinNum,GPIO.OUT)
def heart_led_blink(PinNum,speed):
    GPIO.output(PinNum,False)
    time.sleep(speed)
    GPIO.output(PinNum,True)
    time.sleep(speed)

def HC595_init(PinNum1,PinNum2,PinNum3):
    # print PinNum1,PinNum2,PinNum3
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PinNum1,GPIO.OUT)
    GPIO.setup(PinNum2,GPIO.OUT)
    GPIO.setup(PinNum3,GPIO.OUT)
'''
def HC595_SetState(data):
    print(data)

# Return CPU temperature as a character string                                     
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return res.replace("temp=","").replace("'C\n","")

def getCPUstate(interval=1):
    percent = psutil.cpu_percent(interval)
    return percent,("CPU:"+str(percent) + "%")

def getMemorystate():
    phymem = psutil.virtual_memory()
    line = "Memory: %5s%% %6s/%s"%(phymem.percent,str(int(phymem.used/1024/1024))+"M",str(int(phymem.total/1024/1024))+"M")
    return phymem.percent,line

def getAllstate(): # Temprature CPU-Percent Mem-Percent
    # Temp_cpu = getCPUtemperature()
    Perc_cpu = getCPUstate()
    Memo_cpu = getMemorystate()
    return Perc_cpu[0],Memo_cpu[0]

while True:
    Perc_cpu,Memo_cpu = getAllstate()
    # print(Temp_cpu,'-',type(Temp_cpu))
    print(Perc_cpu)
    print(Memo_cpu)
    time.sleep(15)
'''
def process_heart_status(PinNum): # Need code the watchdog processing!
    Emegency_Flag = {"CPU-Temp":0x01,"CPU-Perc":0x02,"CPU-Memo":0x04}
    Emegency_Sate = 0x00
    print("Thread to blink a led:blink if process alive.")
    # heart_led_init()
    blink_speed = 0.1
    blink_count = 0
    monitor_gap = 15 # Unit:s
    while True:
        Emegency_Sate = 0x00
        Allstate = getAllstate()
        print ("CPU-Temp/Perc/Memo",Allstate)
        if Allstate[0] > 60:
            Emegency_Sate |= Emegency_Flag["CPU-Temp"]
        if Allstate[1] > 0.8:
            Emegency_Sate |= Emegency_Flag["CPU-Perc"]
        if Allstate[2] > 70:
            Emegency_Sate |= Emegency_Flag["CPU-Memo"]
        HC595_SetState(Emegency_Sate)
        print('{TEMP:',Allstate[0],',PERC:',Allstate[1],',MEMO:',Allstate[2],'}')
        blink_count = 0
        blink_speed = (100.1 - Allstate[1])/100.0
        print('Blink Speed:',blink_speed)
        limit = monitor_gap/blink_speed/2
        
        while blink_count <= limit:
            blink_count += 1
            # heart_led_blink(PinNum,blink_speed)
            print(blink_count)
            time.sleep(2*blink_speed)



T1 = time.time()
Temp_Value = getCPUtemperature()
CPU_percent = getCPUstate()
Mem_State = getMemorystate()
T2 = time.time()

print("Time Cost:",(T2-T1))
print("The Tempratrue is:",Temp_Value)
print("The CPU_percent:",CPU_percent[0])
print("The Memory_percent:",Mem_State[0],"%")
print("The CPU Number:",psutil.cpu_count(logical=False))

# HC595_init(12,13,14)
# heart_led_init(heart_pin)
process_heart_status(heart_pin)
'''
