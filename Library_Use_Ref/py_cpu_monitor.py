import os
import sys
import RPi.GPIO as GPIO
import time
import psutil

#fans_Control pin initial
fans_pin = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(fans_pin,GPIO.OUT)

# Return CPU temperature as a character string                                     
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

def getCPUstate(interval=1):
    return ("CPU:"+str(psutil.cpu_percent(interval)) + "%")

def getMemorystate():
    phymem = psutil.virtual_memory()
    line = "Memory: %5s%% %6s/%s"%(phymem.percent,str(int(phymem.used/1024/1024))+"M",str(int(phymem.total/1024/1024))+"M")
    return line,phymem.percent

T1 = time.time()
Temp = getCPUtemperature()
Temp_Value = float(Temp)
CPU_percent = getCPUstate()
Mem_State = getMemorystate()
T2 = time.time()

print "Time Cost:",(T2-T1)
print "The Tempratrue is:",Temp_Value
print "The CPU_percent:",CPU_percent
print "The Memory_percent:",type(Mem_State[1]),"%"
