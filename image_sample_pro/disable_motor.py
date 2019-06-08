import os
import sys
import RPi.GPIO as GPIO
import time

x_motor_pin_EN = 17
y_motor_pin_AP = 18
y_motor_pin_AN = 23
y_motor_pin_BP = 24
y_motor_pin_BN = 25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(x_motor_pin_EN,GPIO.OUT)

GPIO.setup(y_motor_pin_AP,GPIO.OUT)
GPIO.setup(y_motor_pin_AN,GPIO.OUT)
GPIO.setup(y_motor_pin_BP,GPIO.OUT)
GPIO.setup(y_motor_pin_BN,GPIO.OUT)


GPIO.output(x_motor_pin_EN,True)

GPIO.output(y_motor_pin_AP,False)
GPIO.output(y_motor_pin_AN,False)
GPIO.output(y_motor_pin_BP,False)
GPIO.output(y_motor_pin_BN,False)

print 'Motor_pin_17_18_23_24_25_Disable Finished'
