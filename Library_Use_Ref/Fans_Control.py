# Author mm1994uestc
import os
import sys
import RPi.GPIO as GPIO

Fans_pin = 17

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(Fans_pin,GPIO.OUT)

def get_CPU_Temprature():
    res = os.popen('vcgencmd measure_temp').readline()
    return res.replace("temp=","").replace("'C\n","")

Temp = get_CPU_Temprature()
CPU_Temp_val = float(Temp)
print CPU_Temp_val

if CPU_Temp_val > 58.0:
    GPIO.output(Fans_pin,False)
elif CPU_Temp_val < 40.0:
    GPIO.output(Fans_pin,True)
