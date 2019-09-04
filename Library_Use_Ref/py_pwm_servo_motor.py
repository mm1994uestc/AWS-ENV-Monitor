import RPi.GPIO as GPIO
import os
import sys
import time

PWM_Pin = 14
PWM_Fre =  50 # Unit is Hz
PWM_Duty = 5.0 # Range is:0~100

'''
The Steering engine Param:
The PWM Period:20ms
The pulse's width:
	0.5ms ---- 0 degree
	1.0ms ---- 45 degree
	1.5ms ---- 90 degree
	2.0ms ---- 135 degree
	2.5ms ---- 180 degree
The percent of the pulse:
	0.5/20 = 2.5%
	1.0/20 = 5.0%
	1.5/20 = 7.5%
	2.0/20 = 10.0%
	2.5/20 = 12.5%
'''

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_Pin, GPIO.OUT)
GPIO.setwarnings(False)

p = GPIO.PWM(PWM_Pin, PWM_Fre)

Command = 'N'

while Command != 'q':
	Command = input('Please Enter The Command:')
	if Command == 'q':
		break
	if Command == 's':
		p.start(5)
	if Command == 'f':
		print('The Current Frequence is:',PWM_Fre)
		PWM_Fre = float(input('Please Enter New Freq:'))
		p.ChangeFrequency(PWM_Fre)
	if Command == 'd':
		print('The Current Duty is:',PWM_Duty)
		PWM_Duty = float(input('Please Enter New Duty:'))
		p.ChangeDutyCycle(PWM_Duty)
p.stop()
GPIO.cleanup()
