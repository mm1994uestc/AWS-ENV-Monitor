import os
import sys
import RPi.GPIO as GPIO
import time

#fans_Control pin initial
fans_pin = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(fans_pin,GPIO.OUT)

# Return CPU temperature as a character string                                     
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

Temp = getCPUtemperature()
Temp_Value = float(Temp)

print "The Tempratrue is:",Temp_Value
