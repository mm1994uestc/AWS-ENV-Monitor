import os
import sys
import RPi.GPIO as GPIO
import time

led_pin=17

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin,GPIO.OUT)

print 'linker led pin 17 (BCM GPIO)'

while True:
    GPIO.output(led_pin,True)
    time.sleep(0.2)
    GPIO.output(led_pin,False)
    time.sleep(0.2)
